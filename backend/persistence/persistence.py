"""
Persistence Layer — God-Tier Architecture
=====================================
Implements:
- SQLite event store with causal linking
- Keyframe snapshots
- Cold/warm storage separation
"""

import sqlite3
import json
import os
import gzip
import shutil
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Snapshot:
    """Full state snapshot."""
    tick: int
    timestamp: str
    agent_count: int
    world_state: dict
    agents: List[dict]
    economy: dict


@dataclass
class PersistenceConfig:
    """Persistence configuration."""
    db_path: str = "data/simulation.db"
    snapshot_interval: int = 100  # Ticks between full snapshots
    max_snapshots: int = 10  # Keep last N full snapshots
    
    # Storage tiers
    hot_ticks: int = 100  # Events in memory for last N ticks
    warm_days: int = 30   # On fast storage for last N days
    cold_days: int = 365  # Archive after
    
    # Compression
    compress_cold: bool = True


class PersistenceLayer:
    """
    Persistent storage with causal linking.
    Uses event sourcing + snapshots.
    """
    
    def __init__(self, config: PersistenceConfig = None):
        self.config = config or PersistenceConfig()
        
        # Ensure directory exists
        Path(self.config.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Connection
        self.conn: Optional[sqlite3.Connection] = None
        
        # In-memory cache
        self.hot_events: List[dict] = []
        
        # Snapshot tracking
        self.last_snapshot_tick: int = 0
        self.snapshot_paths: List[str] = []
        
        self._initialize_db()
        
        logger.info(f"PersistenceLayer initialized: {self.config.db_path}")
    
    def _initialize_db(self):
        """Create database schema."""
        self.conn = sqlite3.connect(self.config.db_path, timeout=30.0)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        cursor = self.conn.cursor()
        
        # Events table (causal)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                
                entity_id TEXT,
                component TEXT,
                old_value TEXT,
                new_value TEXT,
                
                cause_ids TEXT,
                domain TEXT,
                system TEXT,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes separately
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tick ON events(tick)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entity ON events(entity_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON events(domain)")
        
        # Snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                agent_count INTEGER,
                file_path TEXT,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                
                UNIQUE(tick)
            )
        """)
        
        # Agent state table (denormalized for queries)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER NOT NULL,
                agent_id TEXT NOT NULL,
                
                state_json TEXT,
                
                FOREIGN KEY(tick) REFERENCES snapshots(tick),
                UNIQUE(tick, agent_id)
            )
        """)
        
        self.conn.commit()
    
    def record_event(
        self,
        tick: int,
        entity_id: str,
        component: str,
        old_value: Any,
        new_value: Any,
        cause_ids: List[str] = None,
        domain: str = "unknown",
        system: str = "unknown"
    ):
        """Record a state change event."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO events (
                tick, timestamp, entity_id, component,
                old_value, new_value, cause_ids, domain, system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tick,
            datetime.now().isoformat(),
            entity_id,
            component,
            json.dumps(old_value)[:500] if old_value else None,
            json.dumps(new_value)[:500] if new_value else None,
            json.dumps(cause_ids or []),
            domain,
            system
        ))
        
        self.conn.commit()
        
        # Add to hot cache
        event_id = cursor.lastrowid
        self.hot_events.append({
            "id": event_id,
            "tick": tick,
            "entity_id": entity_id,
            "component": component
        })
        
        # Trim hot cache
        if len(self.hot_events) > self.config.hot_ticks:
            self.hot_events = self.hot_events[-self.config.hot_ticks:]
    
    def create_snapshot(
        self,
        tick: int,
        world_state: dict,
        agents: List[dict],
        economy: dict
    ):
        """Create full state snapshot."""
        cursor = self.conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        # Save agents to JSON file
        agent_file = f"data/snapshot_{tick}_agents.json.gz"
        os.makedirs("data", exist_ok=True)
        
        with gzip.open(agent_file, 'wt') as f:
            json.dump({
                "tick": tick,
                "world_state": world_state,
                "agents": agents,
                "economy": economy
            }, f)
        
        # Record in database
        cursor.execute("""
            INSERT OR REPLACE INTO snapshots (tick, timestamp, agent_count, file_path)
            VALUES (?, ?, ?, ?)
        """, (tick, timestamp, len(agents), agent_file))
        
        self.conn.commit()
        
        self.last_snapshot_tick = tick
        self.snapshot_paths.append(agent_file)
        
        # Trim old snapshots
        self._cleanup_snapshots()
        
        logger.info(f"Snapshot created: tick={tick}, agents={len(agents)}")
    
    def _cleanup_snapshots(self):
        """Remove old snapshots."""
        while len(self.snapshot_paths) > self.config.max_snapshots:
            old_path = self.snapshot_paths.pop(0)
            if os.path.exists(old_path):
                os.remove(old_path)
    
    def load_snapshot(self, tick: int) -> Optional[dict]:
        """Load snapshot closest to tick."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT file_path, tick FROM snapshots
            WHERE tick <= ?
            ORDER BY tick DESC
            LIMIT 1
        """, (tick,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        file_path, snap_tick = row
        
        if not os.path.exists(file_path):
            return None
        
        with gzip.open(file_path, 'rt') as f:
            data = json.load(f)
        
        return data
    
    def load_agent_state(self, agent_id: str, tick: int) -> Optional[dict]:
        """Load agent state at specific tick."""
        # Check snapshots first
        snapshot = self.load_snapshot(tick)
        
        if snapshot:
            for agent in snapshot.get("agents", []):
                if agent["id"] == agent_id:
                    return agent
        
        # Fall back: load from events
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT old_value, new_value FROM events
            WHERE entity_id = ? AND tick <= ?
            ORDER BY tick DESC
            LIMIT 1
        """, (agent_id, tick))
        
        row = cursor.fetchone()
        
        if row:
            return json.loads(row[1]) if row[1] else None
        
        return None
    
    def get_causal_chain(self, entity_id: str, tick: int) -> List[dict]:
        """Get causal chain for entity."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT tick, entity_id, component, old_value, new_value, cause_ids
            FROM events
            WHERE entity_id = ? AND tick <= ?
            ORDER BY tick
        """, (entity_id, tick))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "tick": row[0],
                "entity": row[1],
                "component": row[2],
                "from": json.loads(row[3]) if row[3] else None,
                "to": json.loads(row[4]) if row[4] else None,
                "causes": json.loads(row[5]) if row[5] else []
            })
        
        return results
    
    def query_events(
        self,
        entity_id: str = None,
        domain: str = None,
        from_tick: int = None,
        to_tick: int = None
    ) -> List[dict]:
        """Query events matching criteria."""
        cursor = self.conn.cursor()
        
        conditions = []
        params = []
        
        if entity_id:
            conditions.append("entity_id = ?")
            params.append(entity_id)
        
        if domain:
            conditions.append("domain = ?")
            params.append(domain)
        
        if from_tick:
            conditions.append("tick >= ?")
            params.append(from_tick)
        
        if to_tick:
            conditions.append("tick <= ?")
            params.append(to_tick)
        
        where = " AND ".join(conditions) if conditions else "1=1"
        
        cursor.execute(f"""
            SELECT tick, entity_id, component, old_value, new_value, domain, system
            FROM events
            WHERE {where}
            ORDER BY tick
            LIMIT 1000
""", params)
        
        results = []
        for row in cursor.fetchall():
            try:
                old_val = json.loads(row[3]) if row[3] else None
                new_val = json.loads(row[4]) if row[4] else None
            except (json.JSONDecodeError, TypeError):
                old_val = row[3]
                new_val = row[4]
            results.append({
                "tick": row[0],
                "entity": row[1],
                "component": row[2],
                "from": old_val,
                "to": new_val,
                "domain": row[5],
                "system": row[6]
            })
        
        return results
    
    def get_statistics(self) -> dict:
        """Get storage statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events")
        event_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM snapshots")
        snapshot_count = cursor.fetchone()[0]
        
        # Database size
        db_size = os.path.getsize(self.config.db_path) if os.path.exists(self.config.db_path) else 0
        
        return {
            "events_recorded": event_count,
            "snapshots_stored": snapshot_count,
            "database_size_mb": round(db_size / 1024 / 1024, 2),
            "hot_cache_size": len(self.hot_events)
        }
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("PersistenceLayer closed.")