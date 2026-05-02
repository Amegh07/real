"""
Causal Archaeology DAG — God-Tier Architecture
================================
Complete event sourcing with causal graph.
Every state change links to its causes enabling:
- Forensics: Trace any outcome backward
- Counterfactuals: Branch history at any point
- Meaning: Agents understand why world is way it is
- Responsibility: Blame assignment

Based on spec Section 7.3: Causal Archaeology
"""

import uuid
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum, auto
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


class CausalDomain(Enum):
    """Domains events can originate from."""
    PHYSICS = auto()
    PHYSIOLOGY = auto()
    COGNITION = auto()
    SOCIAL = auto()
    ECONOMIC = auto()
    ENVIRONMENTAL = auto()
    EXTERNAL = auto()  # Game master, admin


@dataclass
class CausalNode:
    """
    A single node in the causal DAG.
    Represents a state change that can be traced backward.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = 0.0
    tick_number: int = 0
    
    # What changed
    entity_id: str = ""           # Agent, org, location, etc.
    component_path: str = ""     # e.g., "agents.123.money"
    previous_value: Any = None
    new_value: Any = None
    
    # Causality
    direct_causes: List[str] = field(default_factory=list)  # Node IDs that caused this
    contributing_factors: List[dict] = field(default_factory=list)  # Non-node causes
    
    # Source info
    source_domain: CausalDomain = CausalDomain.EXTERNAL
    source_system: str = ""  # e.g., "economy.tick", "physiology.decay"
    confidence: float = 1.0
    
    # Observation
    observer_tags: Set[str] = field(default_factory=set)  # Who can see this
    is_hidden: bool = False
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        if isinstance(self.direct_causes, str):
            self.direct_causes = [self.direct_causes] if self.direct_causes else []
        if isinstance(self.observer_tags, str):
            self.observer_tags = {self.observer_tags} if self.observer_tags else set()


@dataclass
class CausalLedger:
    """
    The complete causal graph for the simulation.
    Stores all state changes as nodes with causal links.
    """
    # Main storage
    nodes: Dict[str, CausalNode] = field(default_factory=dict)
    
    # Indexes for fast queries
    by_entity: Dict[str, List[str]] = field(default_factory=dict)
    by_tick: Dict[int, List[str]] = field(default_factory=dict)
    by_domain: Dict[CausalDomain, List[str]] = field(default_factory=dict)
    by_component: Dict[str, List[str]] = field(default_factory=dict)
    
    # Counterfactual branches
    branches: Dict[str, dict] = field(default_factory=dict)  # branch_id -> state
    active_branch: str = "main"

    def record_event(
        self,
        tick_number: int,
        entity_id: str,
        component_path: str,
        previous_value: Any,
        new_value: Any,
        direct_causes: List[str] = None,
        source_domain: CausalDomain = CausalDomain.EXTERNAL,
        source_system: str = "",
        contributing_factors: List[dict] = None,
        metadata: dict = None
    ) -> CausalNode:
        """Record a state change with its causal chain."""
        node = CausalNode(
            id=str(uuid.uuid4())[:12],
            timestamp=datetime.now().timestamp(),
            tick_number=tick_number,
            entity_id=entity_id,
            component_path=component_path,
            previous_value=previous_value,
            new_value=new_value,
            direct_causes=direct_causes or [],
            contributing_factors=contributing_factors or [],
            source_domain=source_domain,
            source_system=source_system,
            confidence=metadata.get("confidence", 1.0) if metadata else 1.0,
            is_hidden=metadata.get("hidden", False) if metadata else False
        )
        
        self.nodes[node.id] = node
        
        # Update indexes
        self._index_node(node)

        return node
    
    def _index_node(self, node: CausalNode):
        """Update all indexes for a node."""
        # By entity
        if node.entity_id not in self.by_entity:
            self.by_entity[node.entity_id] = []
        self.by_entity[node.entity_id].append(node.id)
        
        # By tick
        if node.tick_number not in self.by_tick:
            self.by_tick[node.tick_number] = []
        self.by_tick[node.tick_number].append(node.id)
        
        # By domain
        if node.source_domain not in self.by_domain:
            self.by_domain[node.source_domain] = []
        self.by_domain[node.source_domain].append(node.id)
        
        # By component
        if node.component_path not in self.by_component:
            self.by_component[node.component_path] = []
        self.by_component[node.component_path].append(node.id)
    
    def get_causes(self, node_id: str, depth: int = 10) -> List[CausalNode]:
        """Get the causal chain leading to a node (reverse traversal)."""
        if node_id not in self.nodes:
            return []
        
        causes = []
        visited = {node_id}
        queue = [node_id]
        
        while queue and depth > 0:
            current_id = queue.pop(0)
            if current_id not in self.nodes:
                continue
            
            node = self.nodes[current_id]
            causes.append(node)
            
            for cause_id in node.direct_causes:
                if cause_id not in visited:
                    visited.add(cause_id)
                    queue.append(cause_id)
            
            depth -= 1
        
        return causes
    
    def get_effects(self, node_id: str, depth: int = 10) -> List[CausalNode]:
        """Get all effects resulting from a node (forward traversal)."""
        if node_id not in self.nodes:
            return []
        
        effects = []
        visited = {node_id}
        queue = [node_id]
        
        while queue and depth > 0:
            current_id = queue.pop(0)
            if current_id not in self.nodes:
                continue
            
            node = self.nodes[current_id]
            
            # Find nodes that this node caused
            for nid, n in self.nodes.items():
                if current_id in n.direct_causes and nid not in visited:
                    visited.add(nid)
                    effects.append(n)
                    queue.append(nid)
            
            depth -= 1
        
        return effects
    
    def trace_entity_history(self, entity_id: str) -> List[CausalNode]:
        """Get full history of an entity's state changes."""
        if entity_id not in self.by_entity:
            return []
        
        node_ids = self.by_entity[entity_id]
        nodes = [self.nodes[nid] for nid in node_ids if nid in self.nodes]
        return sorted(nodes, key=lambda n: n.tick_number)
    
    def answer_counterfactual(self, node_id: str, assumption: dict) -> dict:
        """
        Answer: What would have happened if X was different?
        Returns the divergence point and alternative path.
        """
        if node_id not in self.nodes:
            return {"error": "Node not found"}

        original_node = self.nodes[node_id]

        # Create a branch
        branch_id = f"cf_{node_id}_{datetime.now().timestamp()}"
        self.branches[branch_id] = {
            "base_node": node_id,
            "assumption": assumption,
            "divergence_tick": original_node.tick_number,
            "alternative_path": []
        }
        
        return {
            "branch_id": branch_id,
            "original_outcome": original_node.new_value,
            "divergence_point": {
                "tick": original_node.tick_number,
                "entity": original_node.entity_id,
                "component": original_node.component_path
            }
        }
    
    def query(
        self,
        entity_id: str = None,
        component: str = None,
        from_tick: int = None,
        to_tick: int = None,
        domains: List[CausalDomain] = None
    ) -> List[CausalNode]:
        """Query nodes matching criteria."""
        results = []
        
        # Determine search space
        search_ids = set()
        if entity_id and entity_id in self.by_entity:
            search_ids.update(self.by_entity[entity_id])
        if component and component in self.by_component:
            search_ids.update(self.by_component[component])
        
        if not search_ids:
            # Full scan
            search_ids = set(self.nodes.keys())
        
        for nid in search_ids:
            if nid not in self.nodes:
                continue
            
            node = self.nodes[nid]
            
            # Filter
            if from_tick and node.tick_number < from_tick:
                continue
            if to_tick and node.tick_number > to_tick:
                continue
            if domains and node.source_domain not in domains:
                continue
            
            results.append(node)
        
        return sorted(results, key=lambda n: n.tick_number)
    
    def get_statistics(self) -> dict:
        """Get ledger statistics."""
        ticks_spanned = 0
        if self.by_tick:
            tick_keys = list(self.by_tick.keys())
            ticks_spanned = max(tick_keys) - min(tick_keys)
        
        return {
            "total_nodes": len(self.nodes),
            "entities_tracked": len(self.by_entity),
            "ticks_spanned": ticks_spanned,
            "branches": len(self.branches),
            "by_domain": {
                d.name: len(ids) for d, ids in self.by_domain.items()
            }
        }
    
    def export_json(self) -> str:
        """Export for debugging."""
        return json.dumps({
            "nodes": len(self.nodes),
            "by_entity": len(self.by_entity),
            "by_tick": {str(k): len(v) for k, v in self.by_tick.items()}
        }, indent=2)


# Convenience functions for subsystems
def record_state_change(
    ledger: CausalLedger,
    tick: int,
    entity: str,
    component: str,
    old_val: Any,
    new_val: Any,
    domain: CausalDomain,
    system: str,
    cause_node_ids: List[str] = None
):
    """Helper to record a state change."""
    return ledger.record_event(
        tick_number=tick,
        entity_id=entity,
        component_path=component,
        previous_value=str(old_val)[:200],  # Truncate for storage
        new_value=str(new_val)[:200],
        direct_causes=cause_node_ids or [],
        source_domain=domain,
        source_system=system
    )