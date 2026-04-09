"""
Agent Model — Phase 3 Update
------------------------------
Added:
  - memory: MemoryBank (short + long term memories)
  - goal: current goal string (used in Phase 4 for Groq prompting)
  - personality_traits: dict of trait strengths (more granular than archetype)
  - Happiness influenced by relationship count
"""

import uuid
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from utils.logger import get_logger
from memory.memory_bank import MemoryBank

logger = get_logger(__name__)

PERSONALITY_TYPES = ["industrious", "lazy", "social", "reclusive", "reckless", "cautious"]

# Fine-grained trait values per archetype (used to modulate decisions + Groq prompts)
PERSONALITY_TRAITS: Dict[str, Dict[str, float]] = {
    "industrious": {"ambition": 0.9, "sociability": 0.4, "risk_tolerance": 0.3, "empathy": 0.5},
    "lazy":        {"ambition": 0.1, "sociability": 0.5, "risk_tolerance": 0.2, "empathy": 0.4},
    "social":      {"ambition": 0.5, "sociability": 0.9, "risk_tolerance": 0.4, "empathy": 0.8},
    "reclusive":   {"ambition": 0.6, "sociability": 0.1, "risk_tolerance": 0.2, "empathy": 0.3},
    "reckless":    {"ambition": 0.7, "sociability": 0.6, "risk_tolerance": 0.95, "empathy": 0.3},
    "cautious":    {"ambition": 0.5, "sociability": 0.5, "risk_tolerance": 0.05, "empathy": 0.7},
}


@dataclass
class Agent:
    """
    A single simulated person living in the world.
    Phase 3: Now has memory, goals, and personality traits.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""

    # Core needs (0 = critical, 100 = fully satisfied)
    hunger:    float = 80.0
    energy:    float = 80.0
    happiness: float = 70.0

    # Economy
    money: float = 100.0
    income_per_tick: float = 0.0

    # Personality
    personality: str = "industrious"
    traits: Dict[str, float] = field(default_factory=dict)  # populated post-init

    # State
    current_action: str = "idle"
    job: Optional[str] = None
    goal: str = "survive"   # high-level goal, updated by decision engine / Groq

    # Phase 3: Memory
    memory: MemoryBank = field(default=None)  # initialized in __post_init__

    # Life history
    age_ticks: int = 0
    life_events: List[str] = field(default_factory=list)

    # Social counters (updated by RelationshipGraph)
    friend_count: int = 0
    rival_count:  int = 0

    def __post_init__(self):
        # Initialize memory with agent's name
        if self.memory is None:
            self.memory = MemoryBank(self.name)
        # Load trait template from personality archetype
        if not self.traits:
            base = PERSONALITY_TRAITS.get(self.personality, {})
            # Add ±10% noise to each trait for individuality
            self.traits = {
                k: max(0.0, min(1.0, v + random.uniform(-0.1, 0.1)))
                for k, v in base.items()
            }

    # ─────────────────────────────────────────────────────────
    # Tick-level updates
    # ─────────────────────────────────────────────────────────

    def decay_needs(self, tick: int):
        """
        Decay needs each tick. Rates vary by personality traits.
        Social agents become unhappy faster when lonely.
        """
        hunger_rate   = 2.0 + self.traits.get("risk_tolerance", 0.3)
        energy_rate   = 1.5 + self.traits.get("ambition", 0.5) * 1.2
        # Loneliness penalty for social agents
        loneliness_penalty = self.traits.get("sociability", 0.5) * 0.5 \
                             if self.friend_count == 0 else 0.0
        happiness_rate = 1.0 + loneliness_penalty

        self.hunger    = max(0.0, self.hunger    - hunger_rate)
        self.energy    = max(0.0, self.energy    - energy_rate)
        self.happiness = max(0.0, self.happiness - happiness_rate)
        self.age_ticks += 1

        # Record notable decay events in memory
        if self.hunger < 15 and self.hunger > 12:
            self.memory.record(tick, "Getting very hungry.", importance=6, emotion="fearful")
        if self.energy < 15 and self.energy > 12:
            self.memory.record(tick, "Feeling exhausted.", importance=5, emotion="sad")

    def apply_action_effect(self, action: str, world_state):
        """Apply the concrete effect of the chosen action."""
        tick = world_state.tick_number

        if action == "eat":
            paid = world_state.charge_food(self)
            if paid:
                self.hunger = min(100.0, self.hunger + 40.0)
                self.happiness = min(100.0, self.happiness + 5.0)
                self.memory.record(tick, "Had a solid meal.", importance=3, emotion="happy")
            else:
                self.hunger = min(100.0, self.hunger + 10.0)
                self.happiness = max(0.0, self.happiness - 10.0)
                self.life_events.append("Couldn't afford food.")
                self.memory.record_critical(tick, "Could not afford food. Went hungry.")

        elif action == "work":
            wage = world_state.pay_wage(self)
            self.money += wage
            self.income_per_tick = wage
            self.energy = max(0.0, self.energy - 5.0)
            self.happiness = min(100.0, self.happiness + 2.0)
            if wage > 0:
                self.memory.record(tick, f"Worked as {self.job} and earned ${wage:.0f}.",
                                   importance=3, emotion="neutral")

        elif action == "sleep":
            self.energy = min(100.0, self.energy + 30.0)
            self.happiness = min(100.0, self.happiness + 4.0)

        elif action == "socialize":
            # Actual bond updates done by AgentManager via RelationshipGraph
            self.happiness = min(100.0, self.happiness + 8.0)
            self.energy = max(0.0, self.energy - 3.0)

        elif action == "idle":
            self.energy = min(100.0, self.energy + 5.0)

        elif action == "seek_job":
            self.energy = max(0.0, self.energy - 2.0)

        elif action == "spend_luxury":
            pass  # Handled by Economy.spend()

    # ─────────────────────────────────────────────────────────
    # Snapshot
    # ─────────────────────────────────────────────────────────

    def get_snapshot(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "hunger": round(self.hunger, 1),
            "energy": round(self.energy, 1),
            "happiness": round(self.happiness, 1),
            "money": round(self.money, 2),
            "personality": self.personality,
            "traits": {k: round(v, 2) for k, v in self.traits.items()},
            "current_action": self.current_action,
            "goal": self.goal,
            "job": self.job,
            "age_ticks": self.age_ticks,
            "friend_count": self.friend_count,
            "rival_count": self.rival_count,
            "life_events": self.life_events[-5:],
            "memory": self.memory.get_snapshot(),
        }

    def __repr__(self):
        return (
            f"Agent({self.name}[{self.personality}], "
            f"H:{self.hunger:.0f} E:{self.energy:.0f} "
            f"HA:{self.happiness:.0f} ${self.money:.0f})"
        )
