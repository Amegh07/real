"""
God-Tier Simulation Engine
========================
Complete integration of all God-Tier systems:
- Multi-Scale Time Scheduler
- Embodied Physiology 
- Continuous Topology
- SEIR Epidemiology
- Causal Archaeology DAG
- Information Physics
- Continuous Double Auction Market
- WebSocket Streaming
- Persistence
"""

import time
import os
from collections import deque
from typing import Optional, Dict, List, Any

from simulation.world_state import WorldState
from simulation.time_scheduler import MultiScaleScheduler, TimeDomain
from agents.agent_manager import AgentManager
from agents.physiology import PhysiologyModel
from decisions.decision_engine import DecisionEngine
from events.event_bus import EventBus
from events.causal_ledger import CausalLedger, CausalDomain
from economy.economy import Economy, JOB_REGISTRY
from economy.double_auction import Market, OrderSide, OrderType
from economy.financial_system import FinancialSystem
from politics.political_system import PoliticalSystem
from groq_client.groq_client import GroqClient
from utils.logger import get_logger
from ontology.feature_registry import FeatureRegistry
from health.seir_epidemiology import SEIREpidemiology, PathogenGenome
from world.world_map import WorldMap, Location
from world.information_physics import InformationPhysics
from api.websocket_manager import ws_manager
from persistence.persistence import PersistenceLayer, PersistenceConfig

logger = get_logger(__name__)


class GodTierEngine:
    """
    God-Tier Master Simulation Engine.
    Integrates all systems for maximum realism.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.tick_number: int = 0
        self.is_running: bool = False

        # Validate config
        self.tick_delay = config.get("tick_delay_seconds", 1.0)
        if self.tick_delay < 0:
            raise ValueError("tick_delay_seconds cannot be negative")
        if self.tick_delay > 60:
            logger.warning(f"tick_delay_seconds ({self.tick_delay}s) is very high, simulation will be slow")

        self.max_ticks = config.get("max_ticks", None)
        if self.max_ticks is not None and self.max_ticks < 1:
            raise ValueError("max_ticks must be positive")

        initial_agents = config.get("initial_agents", 30)
        if initial_agents < 1:
            raise ValueError("initial_agents must be at least 1")
        if initial_agents > 10000:
            logger.warning(f"initial_agents ({initial_agents}) is very high, may cause performance issues")
        config["initial_agents"] = initial_agents

        logger.info("="*60)
        logger.info("Initializing God-Tier Engine...")
        logger.info("="*60)
        
        # ─────────────────────────────────────────────────────────────
        # CORE SYSTEMS
        # ─────────────────────────────────────────────────────────────
        self.event_bus = EventBus()
        
        # Time scheduler (9 domains)
        self.time_scheduler = MultiScaleScheduler()
        
        # Causal archaeology (event sourcing)
        self.causal_ledger = CausalLedger()
        
        # Persistence
        if config.get("use_persistence", True):
            persist_config = PersistenceConfig(
                db_path=config.get("db_path", "data/god_tier.db"),
                snapshot_interval=config.get("snapshot_interval", 100)
            )
            self.persistence = PersistenceLayer(persist_config)
        else:
            self.persistence = None
        
        # ─────────────────────────────────────────────────────────────
        # WORLD SYSTEMS  
        # ─────────────────────────────────────────────────────────────
        self.world_state = WorldState(config, self.event_bus)
        
        # Continuous topology
        self.world_map = WorldMap(
            width=config.get("map_width", 10000),
            height=config.get("map_height", 10000),
            seed=config.get("map_seed", 42)
        )
        
        # Economy
        self.economy = Economy(config, self.event_bus)
        self.world_state.inject_economy(self.economy)

        # Double auction market - wrap in try/except for resilience
        try:
            self.market = Market(name="main")
            self.market.register_symbol("GOLD")
            self.market.register_symbol("FOOD")
            self.market.register_symbol("LABOR")
        except Exception as e:
            logger.warning(f"Failed to initialize market: {e}, continuing without market")
            self.market = None
        
        # Financial System (E1-E3)
        self.financial_system = FinancialSystem()
        
        # Political System (F1-F3)
        self.political_system = PoliticalSystem()
        
        # Ontology
        self.feature_registry = FeatureRegistry()
        
        # ─────────────────────────────────────────────────────────────
        # HEALTH SYSTEMS
        # ─────────────────────────────────────────────────────────────
        self.epidemiology = SEIREpidemiology()
        
        # Register default pathogen
        pathogen = PathogenGenome(
            name="influenza",
            genome_sequence="ATGC...",
            r0_base=2.0,
            incubation_period=2.0,
            infectious_period=5.0,
            case_fatality_rate=0.01
        )
        self.epidemiology.register_pathogen(pathogen)
        self.epidemiology.hospital_beds = config.get("hospital_beds", 50)
        self.epidemiology.icu_beds = config.get("icu_beds", 10)
        
        # ─────────────────────────────────────────────────────────────
        # INFORMATION SYSTEMS
        # ─────────────────────────────────────────────────────────────
        self.info_physics = InformationPhysics()
        
        # ─────────────────────────────────────────────────────────────
        # AGENT SYSTEMS
        # ─────────────────────────────────────────────────────────────
        self.groq_client = GroqClient(config)
        self.agent_manager = AgentManager(config, self.world_state, self.event_bus, self.groq_client)
        self.agent_manager.attach_health_system(self.epidemiology)
        
        # Decision engine
        self.decision_engine = DecisionEngine(config, self.event_bus, self.groq_client)
        
        # WebSocket manager
        self.ws_manager = ws_manager
        
        # History tracking
        self.economy_history: deque = deque(maxlen=500)
        
        # Statistics
        self.stats = {
            "total_events_recorded": 0,
            "causal_nodes": 0,
            "infections": 0,
            "deaths": 0,
            "market_trades": 0,
            "information_packets": 0
        }
        
        logger.info("God-Tier Engine initialized successfully.")
        logger.info(f"  - Time domains: {len(TimeDomain)}")
        logger.info(f"  - Map size: {len(self.world_map.cells)} cells")
        logger.info(f"  - Market symbols: {len(self.market.books) if self.market else 0}")
    
    def setup(self):
        """Initialize the world with agents."""
        logger.info("Setting up world...")
        
        # Spawn initial agents
        self.agent_manager.spawn_initial_agents()
        
        # Initialize agent positions on map
        for agent in self.agent_manager.get_all_agents():
            x = float(hash(agent.id) % 1000)
            y = float(hash(agent.id + "pos") % 1000)
            self.world_map.agent_locations[agent.id] = Location(x, y)
            
            # Register agent with information physics
            self.info_physics.register_agent(
                agent.id,
                perception_range=100.0
            )

            # Initialize tracking variables for causal ledger
            agent._last_hunger = agent.hunger
            agent._last_money = agent.money

        # Initialize epidemiology population
        agent_ids = [a.id for a in self.agent_manager.get_all_agents()]
        self.epidemiology.initialize_population(agent_ids)
        
        # Initialize world
        self.world_state.initialize()
        
        # Assign jobs
        for agent in self.agent_manager.get_all_agents():
            self.economy.assign_job(agent)
        
        # Create initial snapshot if persistence enabled
        if self.persistence:
            self._create_snapshot()
        
        logger.info(f"World ready: {len(self.agent_manager.agents)} agents")
    
    def tick(self):
        """Advance simulation by one tick."""
        self.tick_number += 1
        
        # 1. Multi-scale time scheduler processes domains
        updates = self.time_scheduler.tick()
        
        # 2. Get all agents
        agents = self.agent_manager.get_all_agents()
        
        # 3. Physiology tick for each agent
        self._tick_physiology(agents)
        
        # 4. Epidemiology update
        self._tick_epidemiology(agents)
        
        # 5. Prune dead agents
        dead_ids = self.agent_manager.prune_dead_agents(self.tick_number)
        agents = self.agent_manager.get_all_agents()

        # 5b. Clean up pruned agents from world map and info physics
        for aid in dead_ids:
            self.world_map.agent_locations.pop(aid, None)
            if aid in self.info_physics.agent_states:
                del self.info_physics.agent_states[aid]
        
        # 6. World movement and location updates
        self._tick_movement(agents)
        
        # 7. Decision making
        for agent in agents:
            action = self.decision_engine.decide(agent, self.world_state)
            agent.current_action = action if action is not None else "idle"
        
        # 8. Execute actions
        for agent in agents:
            self.agent_manager.execute_action(agent)
        
        # 8b. Run marriage and birth checks each tick
        self.agent_manager.run_marriage_checks(self.tick_number)
        self.agent_manager.run_birth_checks(self.tick_number)
        
        # 9. Market tick (double auction)
        if self.market:
            self.market.advance_tick()
        
        # 9b. Financial System tick (E1-E3)
        economy_stress = self._calculate_economy_stress(agents)
        self.financial_system.tick(economy_stress)
        
        # 9c. Political System tick (F1-F3)
        social_stress = self._calculate_social_stress(agents)
        self.political_system.tick(economy_stress, social_stress)
        
        # 10. World state update
        self.world_state.tick(self.tick_number, agents)
        
        # 11. Record causal events
        self._record_causal_events(agents)
        
        # 12. Information propagation
        self._tick_information(agents)
        
        # 13. Flush events
        self.event_bus.flush(self.tick_number)
        
        # 14. History tracking
        self.economy_history.append({
            "tick": self.tick_number,
            "treasury": round(self.economy.treasury, 2),
            "population": len(agents),
            "market_price": self.market.price if self.market else 0.0,
            "epidemiology": self.epidemiology.get_statistics()
        })
        
        # 15. Periodic persistence
        if self.persistence and self.tick_number % 50 == 0:
            self._create_snapshot()
        
        # 16. WebSocket broadcast
        if self.tick_number % 5 == 0:
            self._broadcast_state()
    
    def _tick_physiology(self, agents):
        """Process physiology for all agents."""
        for agent in agents:
            if hasattr(agent, 'physiology') and agent.physiology:
                # Get activity type
                activity = agent.current_action or "idle"
                
                # Get food availability
                food = 0
                if activity == "eat":
                    food = 30  # Assumes food available
                
                # Get sleep hours
                sleep = 8.0 if activity == "sleep" else 0
                
                # Tick physiology
                agent.physiology.tick(activity, food, sleep)
                
                # Update agent stats from physiology
                agent.hunger = agent.physiology.get_effective_hunger()
                agent.energy = agent.physiology.get_effective_energy()
                agent.happiness = agent.physiology.get_effective_happiness()
            else:
                # Fall back to old decay if no physiology
                agent.decay_needs(self.tick_number)
    
    def _tick_epidemiology(self, agents):
        """Process SEIR epidemiology."""
        # Get lockdown level
        lockdown = 0.5 if self.config.get("lockdown_active", False) else 0.0
        
        # Get relationship graph for contact tracing
        rel_graph = self.agent_manager.rel_graph
        
        self.epidemiology.tick(
            tick=self.tick_number,
            agents=agents,
            rel_graph=rel_graph,
            lockdown=lockdown
        )
        
        # Update agent health from epidemiology
        for agent in agents:
            if hasattr(agent, 'id') and agent.id in self.epidemiology.infection_cases:
                case = self.epidemiology.infection_cases[agent.id]
                if case:
                    agent.is_sick = case.state.value >= 2  # INFECTIOUS or worse
                    agent.disease_name = getattr(case, 'pathogen_name', '') or ""
                    agent.illness_severity = getattr(case, 'symptom_severity', 0.0) or 0.0
    
    def _tick_movement(self, agents):
        """Process agent movement on map."""
        for agent in agents:
            if agent.current_action in ["socialize", "work"] and hasattr(agent, 'id'):
                # Simple random walk for now
                if agent.id in self.world_map.agent_locations:
                    current = self.world_map.agent_locations[agent.id]
                    
                    # Small random movement
                    dx = (hash(f"{agent.id}_{self.tick_number}") % 21) - 10
                    dy = (hash(f"{agent.id}_{self.tick_number}_y") % 21) - 10
                    
                    new_loc = Location(
                        current.x + dx * 10,
                        current.y + dy * 10,
                        current.z
                    )
                    
                    self.world_map.move_agent(agent.id, current, new_loc)
    
    def _calculate_economy_stress(self, agents) -> float:
        """Calculate economy stress from agent states."""
        if not agents:
            return 0.0
        
        unemployed = sum(1 for a in agents if not a.job)
        low_money = sum(1 for a in agents if a.money < 50)
        hungry = sum(1 for a in agents if a.hunger < 30)
        
        unemployment_rate = unemployed / len(agents)
        poverty_rate = low_money / len(agents)
        hunger_rate = hungry / len(agents)
        
        return (unemployment_rate * 0.3 + poverty_rate * 0.3 + hunger_rate * 0.4)
    
    def _calculate_social_stress(self, agents) -> float:
        """Calculate social stress from agent states."""
        if not agents:
            return 0.0
        
        no_friends = sum(1 for a in agents if a.friend_count == 0)
        low_happiness = sum(1 for a in agents if a.happiness < 30)
        
        isolation_rate = no_friends / len(agents)
        misery_rate = low_happiness / len(agents)
        
        return (isolation_rate * 0.4 + misery_rate * 0.6)
    
    def _record_causal_events(self, agents):
        """Record causal events to ledger."""
        for agent in agents:
            # Record hunger changes
            if hasattr(agent, 'hunger') and hasattr(agent, '_last_hunger'):
                if agent.hunger != agent._last_hunger:
                    self.causal_ledger.record_event(
                        tick_number=self.tick_number,
                        entity_id=agent.id,
                        component_path="hunger",
                        previous_value=agent._last_hunger,
                        new_value=agent.hunger,
                        source_domain=CausalDomain.PHYSIOLOGY,
                        source_system="physiology.decay"
                    )
                    self.stats["causal_nodes"] += 1
            
            # Record money changes
            if hasattr(agent, 'money') and hasattr(agent, '_last_money'):
                if agent.money != agent._last_money:
                    self.causal_ledger.record_event(
                        tick_number=self.tick_number,
                        entity_id=agent.id,
                        component_path="money",
                        previous_value=agent._last_money,
                        new_value=agent.money,
                        source_domain=CausalDomain.ECONOMIC,
                        source_system="economy.transaction"
                    )
                    self.stats["causal_nodes"] += 1
            
            # Update last values
            agent._last_hunger = agent.hunger if hasattr(agent, 'hunger') else 0
            agent._last_money = agent.money if hasattr(agent, 'money') else 0
    
    def _tick_information(self, agents):
        """Process information physics."""
        # Simple gossip tick
        for agent in agents:
            # Observe neighbors
            if hasattr(agent, 'id') and agent.id in self.world_map.agent_locations:
                loc = self.world_map.agent_locations[agent.id]
                nearby = self.world_map.get_nearby_agents(agent.id, radius=50)
                
                for other_id in nearby[:3]:  # Limit
                    if other_id in self.world_map.agent_locations:
                        # Observe them directly
                        other_loc = self.world_map.agent_locations[other_id]
                        
                        if other_id in self.agent_manager.agents:
                            other = self.agent_manager.agents[other_id]
                            self.info_physics.observe_directly(
                                tick=self.tick_number,
                                agent_id=agent.id,
                                target_id=other_id,
                                target_state={
                                    "health": other.happiness,
                                    "status": other.current_action
                                },
                                range_distance=loc.distance_to(other_loc)
                            )
    
    def _create_snapshot(self):
        """Create persistence snapshot."""
        if not self.persistence:
            return
        
        agent_snapshots = []
        for agent in self.agent_manager.get_all_agents():
            agent_snapshots.append(agent.get_snapshot())
        
        # Get economy state safely
        economy_state = {
            "treasury": self.economy.treasury,
            "inflation": self.economy.inflation_rate,
            "market_price": self.market.price
        }
        
        self.persistence.create_snapshot(
            tick=self.tick_number,
            world_state=self.world_state.get_snapshot(),
            agents=agent_snapshots,
            economy=economy_state
        )
    
    def _broadcast_state(self):
        """Broadcast state via WebSocket."""
        if not self.ws_manager:
            return
        
        import asyncio
        try:
            # Emit tick
            asyncio.create_task(self.ws_manager.emit_tick(
                self.tick_number,
                self.stats
            ))
            
            # Emit economy
            asyncio.create_task(self.ws_manager.emit_economy(
                self.tick_number,
                self.economy.get_economy_state()
            ))
        except Exception as e:
            logger.debug(f"WebSocket broadcast failed: {e}")
    
    def run(self):
        """Main simulation loop."""
        self.setup()
        self.is_running = True
        
        logger.info("Starting God-Tier simulation...")
        
        try:
            while self.is_running:
                self.tick()
                
                if self.tick_number % 10 == 0:
                    self._print_summary()
                
                if self.max_ticks and self.tick_number >= self.max_ticks:
                    logger.info(f"Reached max ticks: {self.max_ticks}")
                    self.is_running = False
                    break
                
                time.sleep(self.tick_delay)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.is_running = False
            self._print_final_summary()
    
    def _print_summary(self):
        """Print tick summary."""
        agents = self.agent_manager.get_all_agents()

        print(f"\n{'='*70}")
        print(f"  TICK {self.tick_number:>5} | Pop: {len(agents):>3} | "
              f"Treasury: ${self.economy.treasury:>8.0f}")
        if self.market:
            print(f"  Market: ${self.market.price:.2f} | Vol: {self.market.volume:.0f} | "
                  f"Spread: {self.market.books['GOLD'].get_spread():.2f}")
        else:
            print(f"  Market: unavailable")

        epi = self.epidemiology.get_statistics()
        print(f"  R_eff: {epi['r_effective']:.2f} | "
              f"Infected: {epi['infectious']} | "
              f"Recovered: {epi['recovered']}")

        causal_stats = self.causal_ledger.get_statistics()
        print(f"  Causal nodes: {causal_stats['total_nodes']}")
        print(f"{'='*70}")
    
    def _print_tick_summary(self):
        """Alias for _print_summary."""
        return self._print_summary()
    
    def _print_final_summary(self):
        """Print final summary."""
        print(f"\n{'#'*70}")
        print(f"  SIMULATION ENDED | Ticks: {self.tick_number}")
        print(f"  Final Population: {len(self.agent_manager.get_all_agents())}")
        print(f"  Causal nodes: {self.stats['causal_nodes']}")
        
        if self.persistence:
            pstats = self.persistence.get_statistics()
            print(f"  Events: {pstats['events_recorded']}")
            print(f"  Snapshots: {pstats['snapshots_stored']}")
        
        print(f"{'#'*70}\n")
    
    def get_integration_stats(self) -> dict:
        """Get integration statistics."""
        return {
            "tick": self.tick_number,
            "population": len(self.agent_manager.get_all_agents()),
            
            # Time scheduler
            "time_domains": self.time_scheduler.get_domain_status(),
            
            # Map
            "map": self.world_map.get_statistics(),
            
            # Epidemiology
            "epidemiology": self.epidemiology.get_statistics(),
            
            # Causal ledger
            "causal": self.causal_ledger.get_statistics(),
            
            # Market
            "market": self.market.get_statistics() if self.market else {},
            
            # Information
            "information": self.info_physics.get_statistics()
        }


# Convenience function to create engine
def create_god_tier_engine(config: dict = None) -> GodTierEngine:
    """Create and return God-Tier engine."""
    default_config = {
        "tick_delay_seconds": 0.8,
        "max_ticks": None,
        "initial_agents": 50,
        "starting_treasury": 100000,
        "use_persistence": True,
        "snapshot_interval": 100,
        "map_width": 5000,
        "map_height": 5000,
        "map_seed": 42,
        "hospital_beds": 30,
        "icu_beds": 5
    }
    
    if config:
        default_config.update(config)
    
    return GodTierEngine(default_config)


if __name__ == "__main__":
    engine = create_god_tier_engine()
    engine.run()