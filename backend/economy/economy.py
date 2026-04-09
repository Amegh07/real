"""
Economy System — Phase 2
------------------------
Manages the job market, wages, prices, and money flow.

Key responsibilities:
- Define job types with different wages and energy costs
- Assign agents to jobs based on availability and personality
- Track economic indicators (GDP, unemployment, inequality)
- Handle price inflation over time
- Support agent spending at shops/services
"""

import random
from typing import Dict, List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────
# Job Definitions
# Each job has: wage, energy_cost, happiness_bonus, required_personality (optional)
# ─────────────────────────────────────────────────────────────
JOB_REGISTRY: Dict[str, dict] = {
    "Farmer": {
        "wage": 18.0,
        "energy_cost": 8.0,
        "happiness_bonus": 5.0,
        "slots": 3,
        "description": "Grows food for the community",
    },
    "Merchant": {
        "wage": 30.0,
        "energy_cost": 5.0,
        "happiness_bonus": 8.0,
        "slots": 2,
        "description": "Buys and sells goods",
    },
    "Guard": {
        "wage": 22.0,
        "energy_cost": 10.0,
        "happiness_bonus": 3.0,
        "slots": 2,
        "description": "Keeps citizens safe",
    },
    "Teacher": {
        "wage": 20.0,
        "energy_cost": 4.0,
        "happiness_bonus": 12.0,
        "slots": 1,
        "description": "Educates the community",
    },
    "Laborer": {
        "wage": 14.0,
        "energy_cost": 12.0,
        "happiness_bonus": 1.0,
        "slots": 999,  # Unlimited — fallback job
        "description": "General manual work",
    },
}

# Spending categories agents can use money on
SPENDING_CATEGORIES: Dict[str, dict] = {
    "food": {"cost": 12.0, "hunger_boost": 40.0, "happiness_boost": 5.0},
    "luxury_food": {"cost": 25.0, "hunger_boost": 45.0, "happiness_boost": 20.0},
    "entertainment": {"cost": 15.0, "hunger_boost": 0.0, "happiness_boost": 25.0},
    "medicine": {"cost": 20.0, "hunger_boost": 0.0, "happiness_boost": 10.0, "energy_boost": 20.0},
}


class Economy:
    """
    The economic engine of the simulation world.
    Tracks the job market, spending, money supply, and economic health.
    """

    def __init__(self, config: dict, event_bus):
        self.config = config
        self.event_bus = event_bus

        # Job market: job_name → list of agent IDs currently holding it
        self.job_assignments: Dict[str, List[str]] = {
            job: [] for job in JOB_REGISTRY
        }

        # Economic ledger
        self.total_wages_paid: float = 0.0
        self.total_spending: float = 0.0
        self.tick_wages: float = 0.0
        self.tick_spending: float = 0.0

        # Price inflation multiplier (grows slowly over time)
        self.inflation_rate: float = 1.0
        self.inflation_growth: float = config.get("inflation_growth", 0.001)

        # Treasury
        self.treasury: float = config.get("starting_treasury", 10_000.0)

        logger.info("Economy system initialized.")

    # ─────────────────────────────────────────────────────────
    # Job Market
    # ─────────────────────────────────────────────────────────

    def assign_job(self, agent) -> Optional[str]:
        """
        Try to assign an agent to the best available job.
        Returns the job name if successful, None if no slots available.
        Priority: personality-preferred jobs → highest-wage available job.
        """
        preferred = self._preferred_jobs(agent.personality)

        # Try preferred first, then fallback to any available
        candidates = preferred + [j for j in JOB_REGISTRY if j not in preferred]

        for job_name in candidates:
            job = JOB_REGISTRY[job_name]
            current = self.job_assignments[job_name]
            if len(current) < job["slots"]:
                # Remove from old job if applicable
                if agent.job:
                    self._release_job(agent)
                self.job_assignments[job_name].append(agent.id)
                agent.job = job_name
                logger.debug(f"{agent.name} assigned to job: {job_name}")
                self.event_bus.emit(f"{agent.name} got a job as {job_name}.")
                return job_name

        return None  # No jobs available

    def release_job(self, agent):
        """Remove an agent from their current job (fired, quit, or idle)."""
        self._release_job(agent)

    def _release_job(self, agent):
        if agent.job and agent.job in self.job_assignments:
            try:
                self.job_assignments[agent.job].remove(agent.id)
            except ValueError:
                pass
        agent.job = None

    def _preferred_jobs(self, personality: str) -> List[str]:
        """Map personality types to preferred job types."""
        mapping = {
            "industrious": ["Farmer", "Guard", "Laborer"],
            "social": ["Teacher", "Merchant"],
            "reclusive": ["Farmer", "Laborer"],
            "reckless": ["Guard", "Laborer"],
            "cautious": ["Teacher", "Merchant"],
            "lazy": ["Merchant", "Teacher"],
        }
        return mapping.get(personality, ["Laborer"])

    # ─────────────────────────────────────────────────────────
    # Wages
    # ─────────────────────────────────────────────────────────

    def pay_wage(self, agent) -> float:
        """
        Pay an agent for working this tick.
        Wage depends on their assigned job (or base wage if unassigned).
        """
        if not agent.job:
            # Auto-assign if not employed
            self.assign_job(agent)

        job_name = agent.job or "Laborer"
        wage = JOB_REGISTRY.get(job_name, JOB_REGISTRY["Laborer"])["wage"]
        wage *= self.inflation_rate  # Wages grow with inflation

        if self.treasury >= wage:
            self.treasury -= wage
            self.total_wages_paid += wage
            self.tick_wages += wage
            agent.income_per_tick = wage
            return wage

        # Treasury empty — pay partial
        partial = max(0.0, self.treasury)
        self.treasury = 0.0
        self.total_wages_paid += partial
        self.tick_wages += partial
        agent.income_per_tick = partial
        if partial == 0:
            self.event_bus.emit("Treasury is empty! Workers unpaid this tick.")
        return partial

    # ─────────────────────────────────────────────────────────
    # Spending
    # ─────────────────────────────────────────────────────────

    def spend(self, agent, category: str) -> bool:
        """
        Agent spends money on a category (food, entertainment, etc.)
        Returns True if the purchase was successful.
        """
        if category not in SPENDING_CATEGORIES:
            return False

        item = SPENDING_CATEGORIES[category]
        cost = item["cost"] * self.inflation_rate

        if agent.money < cost:
            return False

        agent.money -= cost
        self.treasury += cost  # Money flows back to treasury (tax/shop)
        self.total_spending += cost
        self.tick_spending += cost

        # Apply effects
        if item.get("hunger_boost"):
            agent.hunger = min(100.0, agent.hunger + item["hunger_boost"])
        if item.get("happiness_boost"):
            agent.happiness = min(100.0, agent.happiness + item["happiness_boost"])
        if item.get("energy_boost"):
            agent.energy = min(100.0, agent.energy + item["energy_boost"])

        return True

    def charge_food(self, agent) -> bool:
        """Backward-compatible: charge food cost (used by world_state delegation)."""
        return self.spend(agent, "food")

    # ─────────────────────────────────────────────────────────
    # Tick Update
    # ─────────────────────────────────────────────────────────

    def tick(self, tick_number: int, agents: list):
        """Called once per tick to update economic state."""
        # Reset per-tick counters
        self.tick_wages = 0.0
        self.tick_spending = 0.0

        # Slowly inflate prices
        self.inflation_rate = min(2.0, self.inflation_rate + self.inflation_growth)

        # Replenish treasury slightly each tick (represents external trade/taxation)
        base_income = self.config.get("treasury_income_per_tick", 50.0)
        self.treasury += base_income

        # Monthly salary injection on new day ticks
        if tick_number % self.config.get("ticks_per_day", 10) == 0:
            self.event_bus.emit(
                f"Economy report: Treasury=${self.treasury:.0f} | "
                f"Inflation={self.inflation_rate:.3f} | "
                f"Employed={self._employment_count()}/{len(agents)}"
            )

    def _employment_count(self) -> int:
        return sum(len(v) for v in self.job_assignments.values())

    # ─────────────────────────────────────────────────────────
    # Snapshot
    # ─────────────────────────────────────────────────────────

    def get_snapshot(self) -> dict:
        """Serializable economic state for API."""
        return {
            "treasury": round(self.treasury, 2),
            "inflation_rate": round(self.inflation_rate, 4),
            "total_wages_paid": round(self.total_wages_paid, 2),
            "total_spending": round(self.total_spending, 2),
            "tick_wages": round(self.tick_wages, 2),
            "tick_spending": round(self.tick_spending, 2),
            "employment": {
                job: len(agents) for job, agents in self.job_assignments.items()
            },
            "job_registry": {
                name: {
                    "wage": round(d["wage"] * self.inflation_rate, 2),
                    "slots": d["slots"],
                    "filled": len(self.job_assignments[name]),
                }
                for name, d in JOB_REGISTRY.items()
            },
        }
