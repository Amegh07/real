"""
Relationship System — Phase 3
------------------------------
Tracks bonds between agents: friendship, rivalry, and neutral acquaintance.
Relationships form through repeated interactions (socializing, working together).
They influence decision scoring and emotional state.

In Phase 4, Groq will be used for relationship conversations and conflict resolution.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from utils.logger import get_logger
import random

logger = get_logger(__name__)

# Bond strength thresholds
FRIEND_THRESHOLD  =  30   # bond >= 30 → friend
RIVAL_THRESHOLD   = -30   # bond <= -30 → rival
MAX_BOND          =  100
MIN_BOND          = -100


@dataclass
class Relationship:
    """Directed bond between two agents (source → target)."""
    target_id: str
    target_name: str
    bond: float = 0.0                   # -100 to +100
    interactions: int = 0
    last_interaction_tick: int = 0

    @property
    def status(self) -> str:
        if self.bond >= FRIEND_THRESHOLD:
            return "friend"
        elif self.bond <= RIVAL_THRESHOLD:
            return "rival"
        return "acquaintance"

    def strengthen(self, amount: float = 5.0):
        self.bond = min(MAX_BOND, self.bond + amount)
        self.interactions += 1

    def weaken(self, amount: float = 5.0):
        self.bond = max(MIN_BOND, self.bond - amount)
        self.interactions += 1


class RelationshipGraph:
    """
    Manages all agent-to-agent relationships.
    Relationships are directional but typically symmetric unless conflicts arise.
    """

    def __init__(self, event_bus):
        self.event_bus = event_bus
        # agent_id → { other_id → Relationship }
        self._graph: Dict[str, Dict[str, Relationship]] = {}

    def register_agent(self, agent_id: str):
        """Call when a new agent is added to the world."""
        if agent_id not in self._graph:
            self._graph[agent_id] = {}

    def get_or_create(self, source_id: str, source_name: str,
                      target_id: str, target_name: str) -> Relationship:
        """Get the relationship from source→target, creating it if needed."""
        if source_id not in self._graph:
            self._graph[source_id] = {}
        if target_id not in self._graph[source_id]:
            self._graph[source_id][target_id] = Relationship(
                target_id=target_id,
                target_name=target_name,
                bond=random.uniform(-5, 5),   # Slight random initial impression
            )
        return self._graph[source_id][target_id]

    def interact(self, agent_a, agent_b, tick: int, context: str = "social") -> Tuple[float, float]:
        """
        Record a social interaction between two agents.
        Returns (bond_change_a, bond_change_b).
        """
        rel_ab = self.get_or_create(agent_a.id, agent_a.name, agent_b.id, agent_b.name)
        rel_ba = self.get_or_create(agent_b.id, agent_b.name, agent_a.id, agent_a.name)

        # Base bond change depends on interaction type
        base = {"social": 6.0, "work": 3.0, "conflict": -10.0}.get(context, 4.0)

        # Personality compatibility modifies the gain
        compat = self._compatibility(agent_a.personality, agent_b.personality)
        change = base * compat + random.uniform(-2, 2)

        prev_status_ab = rel_ab.status
        rel_ab.strengthen(change) if change > 0 else rel_ab.weaken(-change)
        rel_ba.strengthen(change) if change > 0 else rel_ba.weaken(-change)
        rel_ab.last_interaction_tick = tick
        rel_ba.last_interaction_tick = tick

        # Emit milestone events
        new_status = rel_ab.status
        if prev_status_ab != new_status:
            if new_status == "friend":
                self.event_bus.emit(
                    f"{agent_a.name} and {agent_b.name} have become friends!"
                )
            elif new_status == "rival":
                self.event_bus.emit(
                    f"{agent_a.name} and {agent_b.name} have become rivals."
                )

        return change, change

    def _compatibility(self, p1: str, p2: str) -> float:
        """
        Returns a modifier (0.5 – 1.5) based on personality pair.
        Some personalities clash; some gel.
        """
        clashing = {
            ("social", "reclusive"), ("reclusive", "social"),
            ("reckless", "cautious"), ("cautious", "reckless"),
        }
        synergizing = {
            ("social", "social"), ("industrious", "industrious"),
            ("cautious", "cautious"),
        }
        pair = (p1, p2)
        if pair in clashing:
            return 0.4
        if pair in synergizing:
            return 1.4
        return 1.0

    # ─────────────────────────────────────────────────────────
    # Queries
    # ─────────────────────────────────────────────────────────

    def get_friends(self, agent_id: str) -> List[Relationship]:
        return [r for r in self._graph.get(agent_id, {}).values()
                if r.status == "friend"]

    def get_rivals(self, agent_id: str) -> List[Relationship]:
        return [r for r in self._graph.get(agent_id, {}).values()
                if r.status == "rival"]

    def get_all_relationships(self, agent_id: str) -> List[Relationship]:
        return list(self._graph.get(agent_id, {}).values())

    def get_best_friend(self, agent_id: str) -> object | None:
        rels = self.get_friends(agent_id)
        return max(rels, key=lambda r: r.bond) if rels else None

    def get_snapshot(self, agent_id: str) -> list:
        return [
            {
                "target": r.target_name,
                "bond": round(r.bond, 1),
                "status": r.status,
                "interactions": r.interactions,
            }
            for r in self.get_all_relationships(agent_id)
        ]
