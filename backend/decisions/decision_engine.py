"""
Decision Engine — Phase 4 Update
----------------------------------
Now economy-aware and Groq-integrated:
- Agents seek jobs if unemployed
- Agents choose between basic and luxury spending
- Scores factor in job wages, inflation, and wealth levels
- Groq AI handles high-stakes decisions and dilemmas
"""

import json
import random
from typing import Dict
from agents.agent import Agent
from utils.logger import get_logger

logger = get_logger(__name__)

ACTIONS = ["eat", "work", "sleep", "socialize", "idle", "seek_job", "spend_luxury"]


class DecisionEngine:
    """
    Scores all available actions and picks the best one.
    Phase 4: Economy-aware scoring with Groq escalation.
    """

    def __init__(self, config: dict, event_bus, groq_client):
        self.config = config
        self.event_bus = event_bus
        self.groq_client = groq_client

    # ─────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────

    def decide(self, agent: Agent, world_state) -> str:
        """
        Return the best action for this agent this tick.
        Decision hierarchy:
          1. Emergency overrides (starving, collapsing)
          2. Phase 4 Groq escalation for complex state
          3. Rule-based scoring
        """
        # --- Hard overrides ---
        if agent.hunger < 10:
            return "eat"
        if agent.energy < 8:
            return "sleep"

        # Unemployed agents should seek a job first
        if agent.job is None and agent.energy > 30:
            return "seek_job"

        # --- Phase 4 AI Escalation ---
        if self._should_escalate_to_ai(agent, world_state):
            try:
                action = self._ai_decide(agent, world_state)
                if action in ACTIONS:
                    return action
                else:
                    logger.warning(f"[{agent.name}] AI returned invalid action '{action}'. Falling back.")
            except Exception as e:
                logger.debug(f"[{agent.name}] AI decision failed: {e}. Falling back.")

        # --- Rule-based fallback ---
        scores = self._score_actions(agent, world_state)
        return max(scores, key=lambda a: scores[a] + random.uniform(0, 1.5))

    # ─────────────────────────────────────────────────────────
    # Scoring
    # ─────────────────────────────────────────────────────────

    def _score_actions(self, agent: Agent, world_state) -> Dict[str, float]:
        scores: Dict[str, float] = {action: 0.0 for action in ACTIONS}
        eco = world_state.economy

        # ── EAT ──────────────────────────────────────────────
        hunger_need = 100.0 - agent.hunger
        food_cost = world_state.food_cost
        scores["eat"] = hunger_need * 0.75
        if agent.money < food_cost:
            scores["eat"] *= 0.4       # Poor agent hesitates

        # ── WORK ─────────────────────────────────────────────
        money_pressure = max(0, 200 - agent.money) * 0.4
        energy_penalty = max(0, 40 - agent.energy) * 0.8
        wage = 0.0
        if eco and agent.job:
            from economy.economy import JOB_REGISTRY
            wage = JOB_REGISTRY.get(agent.job, {}).get("wage", 15.0)
        scores["work"] = money_pressure + (wage * 0.3) - energy_penalty

        if agent.personality == "industrious":
            scores["work"] += 20
        elif agent.personality == "lazy":
            scores["work"] -= 20
        if world_state.time_of_day in ("Night", "Dawn"):
            scores["work"] -= 20

        # ── SLEEP ────────────────────────────────────────────
        energy_need = 100.0 - agent.energy
        scores["sleep"] = energy_need * 0.65
        if agent.personality == "lazy":
            scores["sleep"] += 10
        if world_state.time_of_day == "Night":
            scores["sleep"] += 30
        if world_state.time_of_day in ("Morning", "Afternoon"):
            scores["sleep"] -= 15

        # ── SOCIALIZE ────────────────────────────────────────
        happiness_need = max(0, 70 - agent.happiness) * 0.6
        scores["socialize"] = happiness_need
        if agent.personality == "social":
            scores["socialize"] += 25
        elif agent.personality == "reclusive":
            scores["socialize"] -= 30
        if agent.energy < 25:
            scores["socialize"] -= 20

        # ── SEEK JOB ─────────────────────────────────────────
        if agent.job is None:
            scores["seek_job"] = 60 if agent.energy > 30 else 10
        else:
            scores["seek_job"] = 0

        # ── SPEND LUXURY ─────────────────────────────────────
        is_wealthy = agent.money > 300
        is_happy_seeker = agent.happiness < 60
        if is_wealthy and is_happy_seeker:
            scores["spend_luxury"] = 30 + (60 - agent.happiness) * 0.5
        elif agent.personality == "reckless" and agent.money > 100:
            scores["spend_luxury"] = 20
        else:
            scores["spend_luxury"] = 0

        # ── IDLE ─────────────────────────────────────────────
        scores["idle"] = 4.0

        return {action: max(0.0, s) for action, s in scores.items()}

    # ─────────────────────────────────────────────────────────
    # Phase 4 Hooks 
    # ─────────────────────────────────────────────────────────

    def _should_escalate_to_ai(self, agent: Agent, world_state) -> bool:
        """
        AI is called if:
        - Groq is enabled AND
        - Agent faces a complex dilemma (e.g. tension between traits and needs)
        We limit this to a small random chance to save tokens and time.
        """
        if not self.groq_client.enabled:
            return False
            
        # Example condition 1: Very unhappy but wealthy (mid-life crisis)
        if agent.happiness < 40 and agent.money > 200 and random.random() < 0.05:
            return True
            
        # Example condition 2: High number of rivals, creating social tension
        if agent.rival_count > 1 and random.random() < 0.02:
            return True

        # Example condition 3: Starving but has no money 
        if agent.hunger < 30 and agent.money < world_state.food_cost and random.random() < 0.05:
            return True

        return False

    def _ai_decide(self, agent: Agent, world_state) -> str:
        """
        Builds a context-rich prompt and asks Groq to choose an action.
        """
        prompt = f"""
Agent Profile:
Name: {agent.name}
Personality Archetype: {agent.personality}
Traits: {agent.traits}
Current State: 
- Hunger: {agent.hunger:.0f}/100
- Energy: {agent.energy:.0f}/100
- Happiness: {agent.happiness:.0f}/100
- Money: ${agent.money:.0f}
Job: {agent.job or 'Unemployed'}
Social: {agent.friend_count} friends, {agent.rival_count} rivals.
Current Goal: {agent.goal}

Agent's Memory Context:
{agent.memory.build_context_string(n_recent=4, n_significant=3)}

World State: 
- Time: {world_state.time_of_day}
- Weather: {world_state.weather}
- Food Cost: ${world_state.food_cost:.2f}

Valid Options: {ACTIONS}

Based on the agent's complex current state, personality traits, and memories, choose the ONE best action from the Valid Options list above.

Think about what a real person with these traits and memories would do in this exact situation.
Then, provide your answer strictly in the following JSON format:

{{
  "reasoning": "brief 1-sentence explanation of why the action was chosen",
  "action": "exact_action_string"
}}
"""
        response_text = self.groq_client.complete(prompt)
        
        try:
            data = json.loads(response_text)
            action = data.get("action")
            reason = data.get("reasoning")
            
            # Announce the AI decision to the event bus if it's interesting
            if action and reason:
                logger.info(f"🧠 [AI] {agent.name} decided to '{action}': {reason}")
                
            return action
        except json.JSONDecodeError:
            raise ValueError(f"AI returned invalid JSON: {response_text}")

