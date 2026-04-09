"""
Agent Manager — Phase 9: Human Life Cycle
-------------------------------------------
New features:
  - Gendered name pools (male/female)
  - Marriage system: eligible adult friends of opposite gender can marry
  - Birth system: married fertile women have a chance of giving birth each tick
  - Children inherit blended personality from both parents
  - Dead agent pruning with full social graph cleanup
  - Decision engine guard: children only eat/sleep/idle
"""

import random
from typing import List, Dict, Optional
from agents.agent import (
    Agent, PERSONALITY_TYPES, PERSONALITY_TRAITS,
    TICKS_PER_SIM_YEAR, ADULT_AGE_YEARS
)
from memory.relationships import RelationshipGraph
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Gendered name pools ───────────────────────────────────────
MALE_NAMES = [
    "Blaze", "Dex", "Flynn", "Halo", "Ivan", "Knox", "Mace", "Oslo",
    "Quinn", "Rex", "Vex", "Xen", "Zane", "Leo", "Niko", "Orion",
    "Pax", "Quincy", "Rowan", "Silas", "Wyatt", "Xander", "Zion", "Axel",
    "Dane", "Ezra", "Gael", "Ira", "Jace", "Leon", "Nash",
    "Bram", "Cole", "Dorian", "Evan", "Felix", "Grant", "Heath", "Idris",
    "Jules", "Kieran", "Luca", "Milo", "Noel", "Owen", "Pierce", "Rhys",
    "Seth", "Theron", "Uri", "Victor", "Wade", "Xerxes", "York", "Zeph",
]

FEMALE_NAMES = [
    "Aria", "Cora", "Ember", "Grace", "Jade", "Luna", "Nova", "Priya",
    "Sage", "Tara", "Uma", "Wren", "Yuki", "Mia", "Talia", "Una",
    "Vera", "Yara", "Bria", "Cleo", "Faye", "Hope", "Kira", "Mila", "Opal",
    "Avery", "Belle", "Celia", "Diana", "Elena", "Freya", "Hana", "Iris",
    "June", "Kaia", "Lyra", "Maren", "Nina", "Petra", "Rosa", "Sera",
    "Thea", "Ursa", "Veda", "Willa", "Xena", "Ysa", "Zola", "Adira",
]

# Bond score threshold to be eligible for marriage proposal
MARRIAGE_BOND_THRESHOLD = 60.0
# Probability of marriage being proposed per tick (when eligible)
MARRIAGE_CHANCE_PER_TICK = 0.001
# Probability of a fertile woman having a baby per tick
BIRTH_CHANCE_PER_TICK = 0.0015
# Children a couple can have maximum
MAX_CHILDREN_PER_COUPLE = 4


class AgentManager:
    """
    Creates, tracks, and manages all agents.
    Phase 9: Owns the full human life cycle (birth, marriage, death).
    """

    def __init__(self, config: dict, world_state, event_bus, groq_client=None):
        self.config      = config
        self.world_state = world_state
        self.event_bus   = event_bus
        self.groq_client = groq_client
        self.agents: Dict[str, Agent] = {}
        self.rel_graph   = RelationshipGraph(event_bus)
        self._used_names: set = set()

    # ─────────────────────────────────────────────────────────
    # Spawning
    # ─────────────────────────────────────────────────────────

    def spawn_initial_agents(self):
        count = self.config.get("initial_agents", 30)
        for _ in range(count):
            gender = random.choice(["male", "female"])
            name = self._unique_name(gender)
            agent = self._create_agent(name, gender)
            # Give varied starting ages (20–50 sim-years, expressed in ticks)
            agent.age_ticks = random.randint(
                ADULT_AGE_YEARS * TICKS_PER_SIM_YEAR,
                50 * TICKS_PER_SIM_YEAR
            )
            self.agents[agent.id] = agent
            self.rel_graph.register_agent(agent.id)
            logger.debug(f"Spawned: {agent}")
        logger.info(f"Spawned {count} agents.")

    def _unique_name(self, gender: str) -> str:
        pool = MALE_NAMES if gender == "male" else FEMALE_NAMES
        available = [n for n in pool if n not in self._used_names]
        if not available:
            # Fallback: generate unique names with suffixes
            base = random.choice(pool)
            name = f"{base}{random.randint(2, 99)}"
        else:
            name = random.choice(available)
        self._used_names.add(name)
        return name

    def _create_agent(self, name: str, gender: str = "male", 
                      personality: str = None, age_ticks: int = 0,
                      parent_ids: list = None) -> Agent:
        if personality is None:
            personality = random.choice(PERSONALITY_TYPES)
        hunger_offset = {"reckless": -15, "cautious": 5}.get(personality, 0)
        energy_offset = {"industrious": 10, "lazy": -10}.get(personality, 0)

        agent = Agent(
            name=name,
            gender=gender,
            hunger=max(30.0, min(100.0, random.uniform(50.0, 90.0) + hunger_offset)),
            energy=max(20.0, min(100.0, random.uniform(50.0, 90.0) + energy_offset)),
            happiness=random.uniform(50.0, 80.0),
            money=random.uniform(50.0, 200.0),
            personality=personality,
            age_ticks=age_ticks,
            parent_ids=parent_ids or [],
            is_adult=(age_ticks >= ADULT_AGE_YEARS * TICKS_PER_SIM_YEAR),
        )
        return agent

    def spawn_child(self, mother: Agent, father: Agent, tick: int) -> Agent:
        """Create a new child agent as the offspring of two parents."""
        gender = random.choice(["male", "female"])
        name = self._unique_name(gender)

        # Personality: random blend of parents + mutation
        parent_personalities = [mother.personality, father.personality]
        personality = random.choice(parent_personalities)

        child = self._create_agent(
            name=name,
            gender=gender,
            personality=personality,
            age_ticks=0,
            parent_ids=[mother.id, father.id],
        )
        child.is_adult = False
        # Start child well-fed (parents provide)
        child.hunger = 95.0
        child.energy = 90.0
        child.happiness = 85.0
        child.money = 0.0

        # Register the child
        self.agents[child.id] = child
        self.rel_graph.register_agent(child.id)

        # Update parents
        mother.children_ids.append(child.id)
        father.children_ids.append(child.id)

        # Record memories + emit event
        mother.life_events.append(f"Gave birth to {name}.")
        father.life_events.append(f"Became father of {name}.")
        mother.memory.record(tick, f"I gave birth to {name}. My heart is full.", importance=10, emotion="happy")
        father.memory.record(tick, f"My child {name} was born today. I am overjoyed.", importance=10, emotion="happy")
        self.event_bus.emit(f"[BIRTH] {mother.name} & {father.name} welcomed baby {name} ({gender})!")

        logger.info(f"[Birth] {name} born to {mother.name} & {father.name}")
        return child

    # ─────────────────────────────────────────────────────────
    # Registry
    # ─────────────────────────────────────────────────────────

    def get_all_agents(self) -> List[Agent]:
        return [a for a in self.agents.values() if not a.is_dead]

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def get_all_snapshots(self) -> list:
        snapshots = []
        for agent in self.get_all_agents():
            snap = agent.get_snapshot()
            snap["relationships"] = self.rel_graph.get_snapshot(agent.id)
            snapshots.append(snap)
        return snapshots

    def prune_dead_agents(self, tick: int) -> list:
        """Remove dead agents from the registry and emit death events."""
        dead_ids = [aid for aid, a in self.agents.items() if a.is_dead]
        for aid in dead_ids:
            agent = self.agents.pop(aid)
            if agent.job and self.world_state.economy:
                self.world_state.economy.release_job(agent)
            # If married, free the spouse
            if agent.spouse_id and agent.spouse_id in self.agents:
                spouse = self.agents[agent.spouse_id]
                spouse.is_married = False
                spouse.spouse_id = None
                spouse.happiness = max(0.0, spouse.happiness - 20.0)
                spouse.life_events.append(f"Lost my beloved {agent.name} to {agent.death_reason}.")
                spouse.memory.record(tick, f"{agent.name} has died. I am heartbroken.", importance=9, emotion="sad")
            age_str = f"{agent.age_years:.0f}"
            self.event_bus.emit(
                f"[ALERT] {agent.name} ({agent.gender}, age {age_str}) has died from {agent.death_reason}."
            )
            self.rel_graph.remove_agent(aid)
            self._used_names.discard(agent.name)
        return dead_ids

    # ─────────────────────────────────────────────────────────
    # Life Cycle: Marriage
    # ─────────────────────────────────────────────────────────

    def run_marriage_checks(self, tick: int):
        """Check all single adults for potential marriage proposals."""
        adults = [a for a in self.get_all_agents() if a.is_adult and not a.is_married]
        single_males   = {a.id: a for a in adults if a.gender == "male"}
        single_females = {a.id: a for a in adults if a.gender == "female"}

        if not single_males or not single_females:
            return

        for male in list(single_males.values()):
            if male.is_married:  # might have been married earlier this tick
                continue
            if random.random() > MARRIAGE_CHANCE_PER_TICK:
                continue

            # Look for a high-bond female friend
            friends = self.rel_graph.get_friends(male.id)
            female_friends = [
                f for f in friends
                if f.target_id in single_females and f.bond >= MARRIAGE_BOND_THRESHOLD
            ]
            if not female_friends:
                continue

            # Marry the one with highest bond
            best = max(female_friends, key=lambda f: f.bond)
            female = single_females.get(best.target_id)
            if female is None or female.is_married:
                continue

            self._marry(male, female, tick)

    def _marry(self, male: Agent, female: Agent, tick: int):
        """Form a marriage between two agents."""
        male.is_married   = True
        male.spouse_id    = female.id
        female.is_married = True
        female.spouse_id  = male.id

        # Happiness boost
        male.happiness   = min(100.0, male.happiness   + 20.0)
        female.happiness = min(100.0, female.happiness + 20.0)

        male.life_events.append(f"Married {female.name}.")
        female.life_events.append(f"Married {male.name}.")
        male.memory.record(tick, f"I married {female.name} today. Best day of my life.", importance=10, emotion="happy")
        female.memory.record(tick, f"I married {male.name} today. So happy.", importance=10, emotion="happy")

        self.event_bus.emit(f"[MARRIAGE] {male.name} and {female.name} have gotten married!")
        logger.info(f"[Marriage] {male.name} wed {female.name}")

    # ─────────────────────────────────────────────────────────
    # Life Cycle: Births
    # ─────────────────────────────────────────────────────────

    def run_birth_checks(self, tick: int):
        """Check all fertile married women for a chance of giving birth."""
        for agent in self.get_all_agents():
            if not agent.is_fertile():
                continue
            if len(agent.children_ids) >= MAX_CHILDREN_PER_COUPLE:
                continue
            if random.random() > BIRTH_CHANCE_PER_TICK:
                continue

            father = self.agents.get(agent.spouse_id)
            if father is None or father.is_dead:
                continue

            self.spawn_child(mother=agent, father=father, tick=tick)

    # ─────────────────────────────────────────────────────────
    # Action Execution
    # ─────────────────────────────────────────────────────────

    def execute_action(self, agent: Agent):
        action = agent.current_action
        eco    = self.world_state.economy
        tick   = self.world_state.tick_number

        # Children can only eat/sleep/idle (enforced here and in decision engine)
        if not agent.is_adult and action not in ("eat", "sleep", "idle"):
            action = "idle"
            agent.current_action = "idle"

        # ── Economy-routed actions ────────────────────────────
        if action == "seek_job" and eco:
            result = eco.assign_job(agent)
            if result is None:
                self.event_bus.emit(f"{agent.name} looked for work but found nothing.")
                agent.happiness = max(0.0, agent.happiness - 5.0)
                agent.memory.record(tick, "Searched for a job but found nothing.", importance=6, emotion="sad")
            else:
                agent.memory.record_positive(tick, f"Got a job as {result}.")

        elif action == "spend_luxury" and eco:
            category = "entertainment" if agent.happiness > 30 else "medicine"
            success = eco.spend(agent, category)
            if success:
                self.event_bus.emit(f"{agent.name} spent money on {category}.")

        elif action == "visit_doctor":
            MEDICAL_COST = 30.0
            if getattr(agent, "is_sick", False) and agent.money >= MEDICAL_COST:
                # Find a random active healer
                healers = [a for a in self.get_all_agents() if a.job == "Healer" and a.id != agent.id]
                healer = random.choice(healers) if healers else None
                
                # Pay the money
                agent.money -= MEDICAL_COST
                
                if healer:
                    healer.money += MEDICAL_COST
                    self.event_bus.emit(f"{agent.name} paid ${MEDICAL_COST} to Dr. {healer.name} for treatment.")
                    agent.memory.record(tick, f"Visited Dr. {healer.name}. I feel much better.", importance=7, emotion="happy")
                    healer.memory.record(tick, f"Treated {agent.name} and earned ${MEDICAL_COST}.", importance=6, emotion="happy")
                else:
                    self.event_bus.emit(f"{agent.name} visited the apothecary and bought medicine for ${MEDICAL_COST}.")
                    agent.memory.record(tick, "Bought medicine. I feel much better.", importance=7, emotion="neutral")
                
                # Apply the cure
                agent.is_sick = False
                agent.illness_severity = 0.0

        # ── Physical action effects ───────────────────────────
        agent.apply_action_effect(action, self.world_state)

        # ── Socializing: bond both agents ─────────────────────
        if action == "socialize":
            others = [a for a in self.get_all_agents() if a.id != agent.id]
            if others:
                partner = random.choice(others)
                delta = random.uniform(3.0, 12.0) * agent.traits.get("sociability", 0.5)
                self.rel_graph.update_bond(agent.id, partner.id, partner.name, delta)
                self.rel_graph.update_bond(partner.id, agent.id, agent.name, delta * 0.8)
                # Sync social counters
                agent.friend_count = len(self.rel_graph.get_friends(agent.id))
                partner.friend_count = len(self.rel_graph.get_friends(partner.id))
                agent.rival_count  = len(self.rel_graph.get_rivals(agent.id))
                partner.rival_count = len(self.rel_graph.get_rivals(partner.id))
