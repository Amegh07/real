"""
Event Bus
---------
A simple publish-subscribe message queue for the simulation.
Modules emit events; the bus collects and delivers them each tick.

This is the communication backbone. In later phases, events will
trigger Groq reasoning and dashboard notifications.
"""

from collections import deque
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

MAX_EVENT_HISTORY = 200  # Keep last N events in memory


class EventBus:
    """
    Lightweight event queue.
    Any part of the simulation can emit events; they are collected
    and flushed at the end of each tick.
    """

    def __init__(self):
        self._pending: List[str] = []
        self._history: deque = deque(maxlen=MAX_EVENT_HISTORY)

    def emit(self, message: str):
        """Queue an event to be flushed at end of tick."""
        self._pending.append(message)
        logger.debug(f"Event queued: {message}")

    def flush(self, tick: int):
        """
        Move all pending events to history.
        Called once per tick by the engine.
        """
        for msg in self._pending:
            stamped = f"[T{tick}] {msg}"
            self._history.append(stamped)
        self._pending.clear()

    def get_recent_events(self, n: int = 10) -> List[str]:
        """Return the N most recent events from history."""
        history = list(self._history)
        return history[-n:]

    def get_all_events(self) -> List[str]:
        """Return full history as list."""
        return list(self._history)
