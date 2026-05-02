"""
Event Bus - Simple pub-sub for simulation events
"""

from collections import deque
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

MAX_EVENT_HISTORY = 200


class EventBus:
    """Lightweight event queue for simulation."""
    
    def __init__(self):
        self._pending: List[str] = []
        self._history: deque = deque(maxlen=MAX_EVENT_HISTORY)
    
    def emit(self, message: str):
        """Queue an event."""
        self._pending.append(message)
        logger.debug(f"Event queued: {message}")
    
    def flush(self, tick: int):
        """Move pending events to history."""
        for msg in self._pending:
            stamped = f"[T{tick}] {msg}"
            self._history.append(stamped)
        self._pending.clear()
    
    def get_recent(self, n: int = 10) -> List[str]:
        """Get last n events."""
        history = list(self._history)
        return history[-n:]
    
    def get_all_events(self) -> List[str]:
        return list(self._history)
    
    def emit_causal(self, **kwargs):
        """Placeholder for causal events."""
        pass
    
    def get_recent_causal(self, limit: int = 50) -> List[dict]:
        return []