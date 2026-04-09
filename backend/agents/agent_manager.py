"""
Agent Manager — Phase 3 Update
--------------------------------
Now manages the RelationshipGraph.
When agents socialize, it picks a random partner and records the bond update.
Memory is triggered from here for critical life events.
"""

import random
from typing import List, Dict, Optional
from agents.agent import Agent, PERSONALITY_TYPES
from memory.relationships import RelationshipGraph
from utils.logger import get_logger

logger = get_logger(__name__)

FIRST_NAMES = [
    "Aria", "Blaze", "Cora", "Dex", "Ember", "Flynn", "Grace", "Halo",
    "Ivan", "Jade", "Knox", "Luna", "Mace", "Nova", "Oslo", "Priya",
    "Quinn", "Rex", "Sage", "Tara", "Uma", "Vex", "Wren", "Xen", "Yuki", "Zane"
]


class AgentManager:
    """
    Creates, tracks, and manages all agents.
    Phase 3: Owns RelationshipGraph + memory event triggers.
    """

    def __init__(self, config: dict, world_state, event_bus, groq_client=None):
        self.config     = config
        self.world_state = world_state
        self.event_bus  = event_bus
        self.groq_client = groq_client
        self.agents: Dict[str, Agent] = {}
        self.rel_graph  = RelationshipGraph(event_bus)

    # ─────────────────────────────────────────────────────────
    # Spawning
    # ─────────────────────────────────────────────────────────

    def spawn_initial_agents(self):
        count = self.config.get("initial_agents", 8)
        used_names = set()
        for _ in range(count):
            name = self._unique_name(used_names)
            used_names.add(name)
            agent = self._create_agent(name)
            self.agents[agent.id] = agent
            self.rel_graph.register_agent(agent.id)
            logger.debug(f"Spawned: {agent}")
        logger.info(f"Spawned {count} agents.")

    def _unique_name(self, used: set) -> str:
        available = [n for n in FIRST_NAMES if n not in used]
        return random.choice(available) if available else f"Agent_{len(used)}"

    def _create_agent(self, name: str) -> Agent:
        personality = random.choice(PERSONALITY_TYPES)
        hunger_offset = {"reckless": -15, "cautious": 5}.get(personality, 0)
        energy_offset = {"industrious": 10, "lazy": -10}.get(personality, 0)
        return Agent(
            name=name,
            hunger=max(30.0, min(100.0, random.uniform(50.0, 90.0) + hunger_offset)),
            energy=max(20.0, min(100.0, random.uniform(50.0, 90.0) + energy_offset)),
            happiness=random.uniform(50.0, 80.0),
            money=random.uniform(50.0, 200.0),
            personality=personality,
        )

    # ─────────────────────────────────────────────────────────
    # Registry
    # ─────────────────────────────────────────────────────────

    def get_all_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def get_all_snapshots(self) -> list:
        snapshots = []
        for agent in self.get_all_agents():
            snap = agent.get_snapshot()
            snap["relationships"] = self.rel_graph.get_snapshot(agent.id)
            snapshots.append(snap)
        return snapshots

    # ─────────────────────────────────────────────────────────
    # Action Execution
    # ─────────────────────────────────────────────────────────

    def execute_action(self, agent: Agent):
        action = agent.current_action
        eco    = self.world_state.economy
        tick   = self.world_state.tick_number

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
                agent.memory.record(tick, f"Enjoyed some {category}.", importance=4, emotion="happy")
            else:
                agent.current_action = "idle"

        elif action == "socialize":
            # Pick a random other agent to socialize with
            others = [a for a in self.get_all_agents() if a.id != agent.id]
            if others:
                partner = random.choice(others)
                change, _ = self.rel_graph.interact(agent, partner, tick, "social")
                agent.apply_action_effect("socialize", self.world_state)
                partner.happiness = min(100.0, partner.happiness + 5.0)
                
                # --- Phase 4: Groq Conversation ---
                convo_snippet = ""
                if self.groq_client and self.groq_client.enabled and random.random() < 0.02:
                    convo_snippet = self._generate_conversation(agent, partner)
                
                log_msg = f"Spent time with {partner.name}." if not convo_snippet else f"Chatted with {partner.name}: \"{convo_snippet}\""
                
                agent.memory.record(
                    tick, log_msg,
                    importance=4, emotion="happy" if change > 0 else "neutral"
                )
                if convo_snippet:
                    self.event_bus.emit(f"🗣️ {agent.name} -> {partner.name}: \"{convo_snippet}\"")
                
                # Update friend/rival counts
                self._refresh_social_counts(agent)
                self._refresh_social_counts(partner)
            else:
                agent.apply_action_effect("idle", self.world_state)

        else:
            # Standard stat-driven actions
            agent.apply_action_effect(action, self.world_state)

        # ── Critical state alerts + memory ───────────────────
        self._check_critical_states(agent, tick)

    def _refresh_social_counts(self, agent: Agent):
        agent.friend_count = len(self.rel_graph.get_friends(agent.id))
        agent.rival_count  = len(self.rel_graph.get_rivals(agent.id))

    def _check_critical_states(self, agent: Agent, tick: int):
        if agent.hunger < 10:
            self.event_bus.emit(f"[ALERT] {agent.name} is starving! (hunger={agent.hunger:.0f})")
        if agent.energy < 10:
            self.event_bus.emit(f"[ALERT] {agent.name} is exhausted! (energy={agent.energy:.0f})")
        if agent.happiness < 10:
            self.event_bus.emit(f"[ALERT] {agent.name} is miserable! (happiness={agent.happiness:.0f})")
            agent.memory.record_critical(tick, "Reached rock bottom. Happiness is near zero.")
        if agent.money <= 0:
            self.event_bus.emit(f"[ALERT] {agent.name} is broke!")
            agent.memory.record_critical(tick, "Ran out of money entirely.")

    def _generate_conversation(self, agent: Agent, partner: Agent) -> str:
        """
        Phase 4: Generates a 1-sentence conversation snippet between two agents using Groq.
        """
        try:
            rel = self.rel_graph.get_or_create(agent.id, agent.name, partner.id, partner.name)
            prompt = f"""
Agent '{agent.name}' (Personality: {agent.personality}) is talking to '{partner.name}' (Relationship: {rel.status}, Bond: {rel.bond:.0f}).
Agent Memory Context: {agent.memory.build_context_string(2, 1)}

Write ONE short, highly characterful sentence that {agent.name} says to {partner.name}.
Respond ONLY with the exact words spoken, no quotes or prefix.

Respond strictly in JSON format:
{{
  "dialogue": "..."
}}
"""
            import json
            response = self.groq_client.complete(prompt)
            data = json.loads(response)
            return data.get("dialogue", "Hey there.")
        except Exception as e:
            logger.debug(f"Failed to generate conversation: {e}")
            return ""
