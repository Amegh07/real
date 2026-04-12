"""
Agent Model — Phase 9: Human Life Cycle
------------------------------------------
Major additions:
  - gender: "male" or "female"
  - age_years: derived from age_ticks (100 ticks = 1 sim-year)
  - is_adult: False until age 18 sim-years (children can't work or marry)
  - marriage system: is_married, spouse_id
  - family system: parent_ids, children_ids
  - Realistic old-age death (65-80 sim-years)
  - Children inherit blended personality from both parents
"""

import uuid
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from utils.logger import get_logger
from memory.memory_bank import MemoryBank

logger = get_logger(__name__)

PERSONALITY_TYPES = ["industrious", "lazy", "social", "reclusive", "reckless", "cautious"]

# Fine-grained trait values per archetype
PERSONALITY_TRAITS: Dict[str, Dict[str, float]] = {
    "industrious": {"ambition": 0.9, "sociability": 0.4, "risk_tolerance": 0.3, "empathy": 0.5},
    "lazy":        {"ambition": 0.1, "sociability": 0.5, "risk_tolerance": 0.2, "empathy": 0.4},
    "social":      {"ambition": 0.5, "sociability": 0.9, "risk_tolerance": 0.4, "empathy": 0.8},
    "reclusive":   {"ambition": 0.6, "sociability": 0.1, "risk_tolerance": 0.2, "empathy": 0.3},
    "reckless":    {"ambition": 0.7, "sociability": 0.6, "risk_tolerance": 0.95, "empathy": 0.3},
    "cautious":    {"ambition": 0.5, "sociability": 0.5, "risk_tolerance": 0.05, "empathy": 0.7},
}

# ── Age constants ────────────────────────────────────────────
TICKS_PER_SIM_YEAR = 5    # Time-Dilation applied! 5 ticks = 1 simulation year
ADULT_AGE_YEARS    = 18   # Become adult at 18 years
FERTILE_AGE_MAX    = 45   # Women can have children up to 45 years
OLD_AGE_START      = 65   # Death probability begins
OLD_AGE_MAX        = 85   # Near-certain death by 85 years


@dataclass
class Agent:
    """
    A single simulated person living in the world.
    Phase 9: Full human life cycle — gender, marriage, children, aging, death.
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
    traits: Dict[str, float] = field(default_factory=dict)

    # State
    current_action: str = "idle"
    job: Optional[str] = None
    goal: str = "survive"

    # Skills & Health
    skills: Dict[str, float] = field(default_factory=dict)
    is_dead: bool = False
    death_reason: str = ""
    is_sick: bool = False
    illness_severity: float = 0.0

    # Memory
    memory: MemoryBank = field(default=None)

    # Life history
    age_ticks: int = 0
    life_events: List[str] = field(default_factory=list)

    # ── Phase 9: Human Life Cycle ───────────────────────────
    gender: str = "male"          # "male" or "female"
    is_adult: bool = True         # False for newborns until age 18
    is_married: bool = False
    spouse_id: Optional[str] = None
    parent_ids: List[str] = field(default_factory=list)
    children_ids: List[str] = field(default_factory=list)

    # Social counters (updated by RelationshipGraph)
    friend_count: int = 0
    rival_count:  int = 0

    def __post_init__(self):
        if self.memory is None:
            self.memory = MemoryBank(self.name)
        if not self.traits:
            base = PERSONALITY_TRAITS.get(self.personality, {})
            self.traits = {
                k: max(0.0, min(1.0, v + random.uniform(-0.1, 0.1)))
                for k, v in base.items()
            }

    # ─────────────────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────────────────

    @property
    def age_years(self) -> float:
        """Convert raw ticks to simulation years."""
        return self.age_ticks / TICKS_PER_SIM_YEAR

    def is_fertile(self) -> bool:
        """Women aged 18–45 can bear children."""
        return (
            self.gender == "female"
            and self.is_adult
            and self.is_married
            and ADULT_AGE_YEARS <= self.age_years <= FERTILE_AGE_MAX
        )

    # ─────────────────────────────────────────────────────────
    # Tick-level updates
    # ─────────────────────────────────────────────────────────

    def decay_needs(self, tick: int):
        """
        Decay needs each tick. Children decay more slowly.
        Non-linear starvation: hunger drops 2x faster below 30.
        """
        if self.is_dead:
            return

        if not self.is_adult:
            # Children are taken care of — decay at 30% rate
            self.hunger    = max(0.0, self.hunger    - 0.6)
            self.energy    = max(0.0, self.energy    - 0.5)
            self.happiness = max(0.0, self.happiness - 0.3)
            self.age_ticks += 1
            # Check if child has grown into an adult
            if self.age_years >= ADULT_AGE_YEARS and not self.is_adult:
                self.is_adult = True
                self.life_events.append(f"Came of age at {self.age_years:.0f} years old.")
                self.memory.record(tick, "I have become an adult today.", importance=9, emotion="happy")
            return

        # ── Illness Mechanics ──────────────────────────────────
        if not self.is_sick:
            base_sick_chance = 0.003
            if self.energy < 40 or self.hunger < 40:
                base_sick_chance = 0.02  # significantly higher chance if weak
            if random.random() < base_sick_chance:
                self.is_sick = True
                self.illness_severity = 10.0
                self.memory.record(tick, "I've caught a terrible sickness. I feel very weak.", importance=7, emotion="fearful")
        else:
            self.illness_severity += 0.5  # worsens over time
            if self.illness_severity >= 100.0:
                self.is_dead = True
                self.death_reason = "Disease"
                self.energy = 0.0
                return

        # ── Normal Needs Decay ────────────────────────────────
        hunger_rate   = 2.0 + self.traits.get("risk_tolerance", 0.3)
        energy_rate   = 1.5 + self.traits.get("ambition", 0.5) * 1.2
        loneliness_penalty = self.traits.get("sociability", 0.5) * 0.5 \
                             if self.friend_count == 0 else 0.0
        happiness_rate = 1.0 + loneliness_penalty

        # Sickness accelerates needs dropping
        if self.is_sick:
            hunger_rate *= 1.5
            energy_rate *= 2.0
            happiness_rate += 1.0

        # Married agents are happier (smaller happiness decay)
        if self.is_married:
            happiness_rate = max(0.0, happiness_rate - 0.5)

        # Non-linear starvation panic
        if self.hunger < 30.0:
            hunger_rate *= 2.0

        self.hunger    = max(0.0, self.hunger    - hunger_rate)
        self.energy    = max(0.0, self.energy    - energy_rate)
        self.happiness = max(0.0, self.happiness - happiness_rate)
        self.age_ticks += 1

        # ── Death checks ──────────────────────────────────────
        if self.hunger <= 0.0:
            self.is_dead = True
            self.death_reason = "Starvation"
            self.hunger = 0.0

        # Old age: probability ramps from 65 to 85 years
        if self.age_years >= OLD_AGE_START:
            years_over = self.age_years - OLD_AGE_START
            death_prob = min(0.001 + years_over * 0.0003, 0.02)
            if random.random() < death_prob:
                self.is_dead = True
                self.death_reason = "Old Age"

        # ── Memory triggers ───────────────────────────────────
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
            "gender": self.gender,
            "age_years": round(self.age_years, 1),
            "is_adult": self.is_adult,
            "is_married": self.is_married,
            "spouse_id": self.spouse_id,
            "children_count": len(self.children_ids),
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
            "skills": self.skills.copy(),
            "is_dead": self.is_dead,
            "death_reason": self.death_reason,
        }

    def __repr__(self):
        age_str = f"{self.age_years:.0f}yr"
        return (
            f"Agent({self.name}[{self.gender[0].upper()},{age_str},{self.personality}], "
            f"H:{self.hunger:.0f} E:{self.energy:.0f} "
            f"HA:{self.happiness:.0f} ${self.money:.0f})"
        )
