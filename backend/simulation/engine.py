"""
Simulation Engine — Phase 2 Update
------------------------------------
Now wires: WorldState, Economy, AgentManager, DecisionEngine, EventBus.
Economy is injected into WorldState so agents can call world_state.pay_wage() etc.
Treasury now refills via Economy instead of WorldState.
"""

import time
from collections import deque
from typing import Optional

from simulation.world_state import WorldState
from simulation.game_master import AIGameMaster
from agents.agent_manager import AgentManager
from decisions.decision_engine import DecisionEngine
from events.event_bus import EventBus
from economy.economy import Economy, JOB_REGISTRY
from groq_client.groq_client import GroqClient
from utils.logger import get_logger

logger = get_logger(__name__)


class SimulationEngine:
    """
    Master controller for the simulation world.
    Drives the tick loop and orchestrates all subsystems.
    """

    def __init__(self, config: dict):
        self.config = config
        self.tick_number: int = 0
        self.is_running: bool = False
        self.tick_delay: float = config.get("tick_delay_seconds", 1.0)
        self.max_ticks: Optional[int] = config.get("max_ticks", None)

        # Build subsystems in dependency order
        self.event_bus = EventBus()
        self.world_state = WorldState(config, self.event_bus)
        self.economy = Economy(config, self.event_bus)
        self.world_state.inject_economy(self.economy)           # Wire economy in

        self.groq_client = GroqClient(config)                  # Must come before AgentManager
        self.agent_manager = AgentManager(config, self.world_state, self.event_bus, self.groq_client)
        self.decision_engine = DecisionEngine(config, self.event_bus, self.groq_client)

        # Economy and UI state
        self.economy_history: deque = deque(maxlen=200)

        # Phase 8: AI Task Queue + Game Master
        self.ai_task_queue: deque = deque()
        self.game_master = AIGameMaster(self.groq_client, self.world_state, self.event_bus)

        logger.info("SimulationEngine initialized (Phase 8).")

    def setup(self):
        """Populate the world with initial agents and assign starting jobs."""
        logger.info("Setting up world...")
        self.agent_manager.spawn_initial_agents()
        self.world_state.initialize()

        # Assign jobs to all starting agents
        for agent in self.agent_manager.get_all_agents():
            self.economy.assign_job(agent)

        logger.info(f"World ready: {len(self.agent_manager.agents)} agents created.")

    def tick(self):
        """
        Advance the simulation by one step.

        Tick order (critical — do not reorder):
        1. Decay agent needs
        2. Decision engine picks actions
        3. Execute actions (stats + economy effects)
        4. World state & economy update
        5. Flush event bus
        """
        self.tick_number += 1
        logger.debug(f"--- Tick {self.tick_number} ---")

        agents = self.agent_manager.get_all_agents()

        # 1. Decay needs for all agents
        for agent in agents:
            agent.decay_needs(self.tick_number)

        # 1b. Prune dead agents (starvation/old age)
        self.agent_manager.prune_dead_agents(self.tick_number)
        agents = self.agent_manager.get_all_agents()  # refresh after deaths

        # 2. Decide actions (economy-aware in Phase 2)
        for agent in agents:
            action = self.decision_engine.decide(agent, self.world_state)
            agent.current_action = action

        # 3. Execute actions
        for agent in agents:
            self.agent_manager.execute_action(agent)

        # 4. Update world (time, weather, economy tick, taxes)
        self.world_state.tick(self.tick_number, agents)

        # Phase 5: Trigger reflection at the start of a new day
        if self.tick_number > 1 and (self.tick_number - 1) % self.config.get("ticks_per_day", 10) == 0:
            self._run_nightly_reflections()

        # Phase 9: Human Lifecycle — marriage & births (run every 5 ticks for performance)
        if self.tick_number % 5 == 0:
            self.agent_manager.run_marriage_checks(self.tick_number)
            self.agent_manager.run_birth_checks(self.tick_number)

        # 5. Flush events
        self.event_bus.flush(self.tick_number)

        # 6. Record economy history for chart API
        self.economy_history.append({
            "tick": self.tick_number,
            "treasury": round(self.economy.treasury, 2),
            "inflation": round(self.economy.inflation_rate, 4),
            "employed": self.economy._employment_count(),
            "population": len(agents),
        })

        # 7. Process AI Queue (1 request every 3 ticks ~ 25 RPM at 1.2s tick delay)
        if self.tick_number % 3 == 0 and self.ai_task_queue:
            task = self.ai_task_queue.popleft()
            self._process_ai_task(task)

        # 8. Game Master: check for world events (queued so they respect rate limits)
        if self.game_master.should_trigger(self.tick_number):
            self.ai_task_queue.append({
                "type": "world_event",
                "tick": self.tick_number,
                "agents": [a.id for a in agents],
            })

    def run(self):
        """Start the main simulation loop."""
        self.setup()
        self.is_running = True
        logger.info("Simulation started.")

        try:
            while self.is_running:
                self.tick()
                self._print_tick_summary()

                if self.max_ticks and self.tick_number >= self.max_ticks:
                    logger.info(f"Reached max ticks ({self.max_ticks}). Stopping.")
                    self.is_running = False
                    break

                time.sleep(self.tick_delay)

        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user.")
        finally:
            self.is_running = False
            self._print_final_summary()

    def _run_nightly_reflections(self):
        """Phase 5/8: Agents queue up for reflection instead of blocking all at once."""
        agents = self.agent_manager.get_all_agents()
        import random
        # Pick 2 random agents per night to queue up for reflection (smoothly processed later)
        if not agents:
            return
        
        reflectors = random.sample(agents, min(2, len(agents)))
        for agent in reflectors:
            self.ai_task_queue.append({"type": "reflection", "agent_id": agent.id})

    def _process_ai_task(self, task: dict):
        """Consume a queued AI task synchronously."""
        from agents.agent import Agent
        
        if task["type"] == "reflection":
            agent = self.agent_manager.get_agent(task["agent_id"])
            if not agent: return
            
            logger.info(f"[AI Queue] Processing reflection for {agent.name}")
            current_state = {
                "hunger": round(agent.hunger),
                "energy": round(agent.energy),
                "happiness": round(agent.happiness),
                "money": round(agent.money),
                "job": agent.job
            }
            new_goal = agent.memory.generate_reflection(self.groq_client, current_state)
            if new_goal:
                agent.goal = new_goal

        elif task["type"] == "world_event":
            logger.info("[AI Queue] Processing Global Game Master event.")
            agents = self.agent_manager.get_all_agents()
            self.game_master.generate_and_apply_event(task["tick"], agents, self.economy)

    # ─────────────────────────────────────────────────────────
    # Console Output
    # ─────────────────────────────────────────────────────────

    def _print_tick_summary(self):
        """Rich console snapshot each tick."""
        agents = self.agent_manager.get_all_agents()
        world  = self.world_state
        eco    = self.economy

        print(f"\n{'='*70}")
        print(
            f"  TICK {self.tick_number:>4}  |  Day {world.day}  |  "
            f"{world.time_of_day:<10}  |  {world.weather:<8}"
        )
        print(
            f"  Treasury: ${eco.treasury:>8.0f}  |  "
            f"Inflation: {eco.inflation_rate:.3f}  |  "
            f"Employed: {eco._employment_count()}/{len(agents)}"
        )
        print(f"{'='*70}")
        print(f"  {'Name':<12} {'HUN':>4} {'ENG':>4} {'HAP':>4} {'Money':>8}  {'Job':<12}  {'Fr':>3} {'Rv':>3}  Action")
        print(f"  {'-'*70}")

        rel = self.agent_manager.rel_graph
        for agent in agents:
            friends = len(rel.get_friends(agent.id))
            rivals  = len(rel.get_rivals(agent.id))
            print(
                f"  {agent.name:<12} "
                f"{agent.hunger:>4.0f} "
                f"{agent.energy:>4.0f} "
                f"{agent.happiness:>4.0f} "
                f"${agent.money:>7.0f}  "
                f"{(agent.job or 'Unemployed'):<12}  "
                f"{friends:>3} {rivals:>3}  "
                f"{agent.current_action}"
            )

        recent = self.event_bus.get_recent_events(4)
        if recent:
            print(f"\n  Events:")
            for ev in recent:
                print(f"    > {ev}")

    def _print_final_summary(self):
        """Economic + agent final report."""
        agents = self.agent_manager.get_all_agents()
        eco    = self.economy

        print(f"\n{'#'*70}")
        print(f"  SIMULATION ENDED  |  Ticks: {self.tick_number}  |  Days: {self.world_state.day}")
        print(f"  Treasury: ${eco.treasury:.2f}")
        print(f"  Total wages paid:  ${eco.total_wages_paid:.2f}")
        print(f"  Total spending:    ${eco.total_spending:.2f}")
        print(f"  Inflation:         {eco.inflation_rate:.4f}x")
        print(f"\n  FINAL AGENT STATUS (sorted by happiness):")
        print(f"  {'Name':<12} {'Happiness':>10} {'Money':>8}  {'Job':<12}")
        print(f"  {'-'*50}")
        for agent in sorted(agents, key=lambda a: a.happiness, reverse=True):
            print(
                f"  {agent.name:<12} "
                f"{agent.happiness:>10.1f} "
                f"${agent.money:>7.0f}  "
                f"{(agent.job or 'Unemployed'):<12}"
            )
        print(f"\n  JOB MARKET:")
        for job, workers in eco.job_assignments.items():
            slots = JOB_REGISTRY[job]["slots"] if JOB_REGISTRY[job]["slots"] < 999 else "inf"
            print(f"    {job:<12}  filled={len(workers)}  slots={slots}")
        print(f"{'#'*70}\n")
