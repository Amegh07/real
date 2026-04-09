"""
World State — Phase 2 Update
-----------------------------
Now delegates economy operations (wages, food, taxes) to the Economy subsystem.
WorldState focuses on: time, weather, environment.
Economy handles: money flow, jobs, spending.
"""

import random
from utils.logger import get_logger

logger = get_logger(__name__)

TIME_PHASES = ["Dawn", "Morning", "Afternoon", "Evening", "Night"]

WEATHER_OPTIONS = ["Clear", "Cloudy", "Rainy", "Stormy", "Sunny"]
WEATHER_EFFECTS = {
    "Clear":   {"happiness_delta": +1.0, "energy_delta": 0.0},
    "Sunny":   {"happiness_delta": +2.0, "energy_delta": +1.0},
    "Cloudy":  {"happiness_delta": -0.5, "energy_delta": 0.0},
    "Rainy":   {"happiness_delta": -1.0, "energy_delta": -0.5},
    "Stormy":  {"happiness_delta": -3.0, "energy_delta": -1.0},
}


class WorldState:
    """
    Global environment container.
    In Phase 2+, economic operations are delegated to Economy.
    This class is passed around as 'world_state'; agents call
    world_state.pay_wage() and world_state.charge_food() which forward to Economy.
    """

    def __init__(self, config: dict, event_bus):
        self.config = config
        self.event_bus = event_bus

        # Time
        self.tick_number: int = 0
        self.day: int = 1
        self.time_phase_index: int = 0
        self.ticks_per_day: int = config.get("ticks_per_day", 10)

        # Environment
        self.weather: str = "Clear"

        # Economy reference — injected after Economy is created in engine
        self.economy = None

        # Legacy stats (kept for backward compat with Phase 1 prints)
        self.total_transactions: int = 0
        self.total_money_circulated: float = 0.0

    def inject_economy(self, economy):
        """Called by SimulationEngine after Economy is constructed."""
        self.economy = economy

    def initialize(self):
        """Set initial world conditions."""
        self.weather = random.choice(WEATHER_OPTIONS)
        logger.info(f"World initialized | Day {self.day} | Weather: {self.weather}")

    # ─────────────────────────────────────────────────────────
    # Time
    # ─────────────────────────────────────────────────────────

    @property
    def time_of_day(self) -> str:
        return TIME_PHASES[self.time_phase_index % len(TIME_PHASES)]

    @property
    def treasury(self) -> float:
        """Delegate treasury read to Economy."""
        return self.economy.treasury if self.economy else 0.0

    @property
    def food_cost(self) -> float:
        return self.economy.inflation_rate * 12.0 if self.economy else 12.0

    # ─────────────────────────────────────────────────────────
    # Tick
    # ─────────────────────────────────────────────────────────

    def tick(self, tick_number: int, agents: list):
        """Advance world time and apply environmental effects."""
        self.tick_number = tick_number
        self.time_phase_index = (tick_number - 1) % len(TIME_PHASES)

        # New day
        if tick_number > 1 and (tick_number - 1) % self.ticks_per_day == 0:
            self.day += 1
            self._on_new_day()

        # Random weather shift
        if random.random() < 0.08:
            old = self.weather
            self.weather = random.choice(WEATHER_OPTIONS)
            if self.weather != old:
                self.event_bus.emit(f"Weather changed to {self.weather}.")

        # Apply weather effects to all agents
        effects = WEATHER_EFFECTS.get(self.weather, {})
        for agent in agents:
            if effects.get("happiness_delta"):
                agent.happiness = max(0.0, min(100.0, agent.happiness + effects["happiness_delta"]))
            if effects.get("energy_delta"):
                agent.energy = max(0.0, min(100.0, agent.energy + effects["energy_delta"]))

        # Tick economy subsystem
        if self.economy:
            self.economy.tick(tick_number, agents)

    def _on_new_day(self):
        logger.info(f"New day: Day {self.day}")
        self.event_bus.emit(f"=== Day {self.day} has begun. Weather: {self.weather} ===")

    # ─────────────────────────────────────────────────────────
    # Economy Delegation (called by Agent.apply_action_effect)
    # ─────────────────────────────────────────────────────────

    def pay_wage(self, agent) -> float:
        """Delegate to Economy. Agents call this when they work."""
        if self.economy:
            return self.economy.pay_wage(agent)
        # Phase 1 fallback
        amount = self.config.get("base_wage", 20.0)
        self.total_transactions += 1
        self.total_money_circulated += amount
        return amount

    def charge_food(self, agent) -> bool:
        """Delegate to Economy. Agents call this when they eat."""
        if self.economy:
            return self.economy.charge_food(agent)
        # Phase 1 fallback
        cost = self.config.get("food_cost", 12.0)
        if agent.money >= cost:
            agent.money -= cost
            self.total_transactions += 1
            return True
        return False

    # ─────────────────────────────────────────────────────────
    # Snapshot
    # ─────────────────────────────────────────────────────────

    def get_snapshot(self) -> dict:
        snap = {
            "tick": self.tick_number,
            "day": self.day,
            "time_of_day": self.time_of_day,
            "weather": self.weather,
        }
        if self.economy:
            snap["economy"] = self.economy.get_snapshot()
        return snap
