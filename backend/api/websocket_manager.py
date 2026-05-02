"""
WebSocket API for Real-Time Streaming — God-Tier Architecture
====================================================
Replaces polling with WebSocket streaming.
Sends incremental updates, not full state.
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional, Set
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class MessageType(Enum):
    """WebSocket message types."""
    AGENT_UPDATE = auto()
    WORLD_STATE = auto()
    EVENT = auto()
    ECONOMY = auto()
    TICK = auto()
    COMMAND = auto()
    ERROR = auto()


@dataclass
class WSMessage:
    """WebSocket message wrapper."""
    type: MessageType
    data: Dict[str, Any]
    tick: int = 0
    
    def to_json(self) -> str:
        return json.dumps({
            "type": self.type.name,
            "data": self.data,
            "tick": self.tick
        })
    
    @classmethod
    def from_json(cls, raw: str) -> 'WSMessage':
        obj = json.loads(raw)
        return cls(
            type=MessageType[obj["type"]],
            data=obj["data"],
            tick=obj.get("tick", 0)
        )


class WebSocketManager:
    """
    Manages WebSocket connections for real-time streaming.
    """
    
    def __init__(self):
        # Connected clients
        self.clients: Set[Any] = set()
        
        # Subscription tracking
        self.subscriptions: Dict[str, Set[str]] = {}  # client_id -> subscribed_to
        
        # Message queues per client (with max size for backpressure)
        self.MAX_QUEUE_SIZE = 100
        self.message_queues: Dict[str, asyncio.Queue] = {}
        
        # Callbacks
        self.on_connect: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None
        self.on_message: Optional[Callable] = None
        
        # Broadcast buffer
        self.broadcast_buffer: List[WSMessage] = []
        
        logger.info("WebSocketManager initialized.")
    
    async def connect(self, client_id: str, websocket):
        """Client connected."""
        self.clients.add(websocket)
        self.message_queues[client_id] = asyncio.Queue(maxsize=self.MAX_QUEUE_SIZE)
        self.subscriptions[client_id] = {"all"}

        asyncio.create_task(self.process_queue(client_id, websocket))

        if self.on_connect:
            await self.on_connect(client_id)

        logger.info(f"Client {client_id} connected. Total: {len(self.clients)}")
    
    async def disconnect(self, client_id: str, websocket):
        """Client disconnected."""
        self.clients.discard(websocket)
        
        if client_id in self.message_queues:
            del self.message_queues[client_id]
        
        if client_id in self.subscriptions:
            del self.subscriptions[client_id]
        
        if self.on_disconnect:
            await self.on_disconnect(client_id)
        
        logger.info(f"Client {client_id} disconnected.")
    
    async def send(self, client_id: str, message: WSMessage):
        """Send message to specific client with backpressure."""
        if client_id not in self.message_queues:
            return
        
        queue = self.message_queues[client_id]
        
        # Backpressure: drop oldest message if queue full (non-blocking)
        if queue.full():
            try:
                queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
        
        # Non-blocking put
        try:
            queue.put_nowait(message)
        except asyncio.QueueFull:
            pass  # Already full, message dropped
        except Exception as e:
            logger.error(f"Send error: {e}")
    
    async def broadcast(self, message: WSMessage):
        """Broadcast to all subscribed clients."""
        disconnected = []
        
        for client_id in list(self.subscriptions.keys()):
            # Check subscriptions
            subs = self.subscriptions.get(client_id, set())
            
            if "all" not in subs:
                if message.type.name not in subs:
                    continue
            
            try:
                await self.send(client_id, message)
            except Exception:
                disconnected.append(client_id)
        
        # Clean up disconnected
        for client_id in disconnected:
            if client_id in self.message_queues:
                del self.message_queues[client_id]
    
    def subscribe(self, client_id: str, channels: List[str]):
        """Client subscribes to channels."""
        if client_id not in self.subscriptions:
            self.subscriptions[client_id] = set()
        
        self.subscriptions[client_id].update(channels)
    
    def unsubscribe(self, client_id: str, channels: List[str]):
        """Client unsubscribes from channels."""
        if client_id in self.subscriptions:
            for ch in channels:
                self.subscriptions[client_id].discard(ch)
    
    # ─────────────────────────────────────────────────────────────────
    # Simulation event handlers (call these from engine)
    # ─────────────────────────────────────────────────────────────────
    
    async def emit_tick(self, tick: int, stats: dict):
        """Emit tick update."""
        await self.broadcast(WSMessage(
            type=MessageType.TICK,
            data={"stats": stats},
            tick=tick
        ))
    
    async def emit_agent_update(self, tick: int, agent_id: str, snapshot: dict):
        """Emit agent state delta."""
        await self.broadcast(WSMessage(
            type=MessageType.AGENT_UPDATE,
            data={
                "agent_id": agent_id,
                "snapshot": snapshot
            },
            tick=tick
        ))
    
    async def emit_world_state(self, tick: int, state: dict):
        """Emit world state (less frequent)."""
        await self.broadcast(WSMessage(
            type=MessageType.WORLD_STATE,
            data=state,
            tick=tick
        ))
    
    async def emit_event(self, tick: int, event: dict):
        """Emit simulation event."""
        await self.broadcast(WSMessage(
            type=MessageType.EVENT,
            data=event,
            tick=tick
        ))
    
    async def emit_economy(self, tick: int, economy: dict):
        """Emit economy update."""
        await self.broadcast(WSMessage(
            type=MessageType.ECONOMY,
            data=economy,
            tick=tick
        ))
    
    async def emit_error(self, tick: int, error: str):
        """Emit error."""
        await self.broadcast(WSMessage(
            type=MessageType.ERROR,
            data={"error": error},
            tick=tick
        ))
    
    # ─────────────────────────────────────────────────────────────────
    # Queue processing (for background task)
    # ─────────────────────────────────────────────────────────────────
    
    async def process_queue(self, client_id: str, websocket):
        """Process outgoing queue for client."""
        if client_id not in self.message_queues:
            return

        queue = self.message_queues[client_id]

        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=1.0)

                await websocket.send(message.to_json())
                
            except asyncio.CancelledError:
                logger.info(f"Queue processing cancelled for {client_id}")
                break
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Queue processing error: {e}")
                break
    
    def get_statistics(self) -> dict:
        """Get WebSocket statistics."""
        return {
            "connected_clients": len(self.clients),
            "subscriptions": {
                k: list(v) for k, v in self.subscriptions.items()
            }
        }


# Singleton instance
ws_manager = WebSocketManager()