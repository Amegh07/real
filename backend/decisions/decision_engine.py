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

ACTIONS = ["eat", "work", "sleep", "socialize", "idle", "seek_job", "spend_luxury", "visit_doctor"]


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
          1. Children → restricted to eat/sleep/idle
          2. Emergency overrides (starving, collapsing)
          3. Phase 4 Groq escalation for complex state
          4. Rule-based scoring
        """
        # --- Children only do basic things ---
        if not agent.is_adult:
            if agent.hunger < 30:
                return "eat"
            if agent.energy < 20:
                return "sleep"
            return "idle"

        # --- Hard overrides ---
        if agent.hunger < 10:
            return "eat"
        if getattr(agent, "is_sick", False) and getattr(agent, "illness_severity", 0) > 30 and agent.money >= 30:
            return "visit_doctor"
        if agent.energy < 8:
            return "sleep"

        # Unemployed adults should seek a job first
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
        # Deterministic tie-breaking using agent id hash instead of random
        return max(scores, key=lambda a: scores[a] + hash(f"{agent.id}_{a}") % 100 / 1000)

    # ─────────────────────────────────────────────────────────
    # Scoring
    # ─────────────────────────────────────────────────────────

    def _score_actions(self, agent: Agent, world_state) -> Dict[str, float]:
        scores: Dict[str, float] = {action: 0.0 for action in ACTIONS}
        eco = getattr(world_state, 'economy', None)
        dims = getattr(agent, "dimension_state", {})
        economic_pressure = dims.get("economic", {}).get("deprivation_risk", 0.0)
        distress = dims.get("affective", {}).get("distress", 0.0)
        social_support = dims.get("social", {}).get("social_support", 0.0)

        # ── EAT ──────────────────────────────────────────────
        hunger_need = 100.0 - agent.hunger
        food_cost = getattr(world_state, 'food_cost', 20) or 20
        scores["eat"] = hunger_need * 0.75 + economic_pressure * 0.05
        if agent.money < food_cost:
            scores["eat"] *= 0.4       # Poor agent hesitates

        # ── WORK ─────────────────────────────────────────────
        money_pressure = max(0, 200 - agent.money) * 0.4
        energy_penalty = max(0, 40 - agent.energy) * 0.8
        wage = 0.0
        if eco and agent.job:
            from economy.economy import JOB_REGISTRY
            wage = JOB_REGISTRY.get(agent.job, {}).get("wage", 15.0)
        scores["work"] = money_pressure + (wage * 0.3) - energy_penalty + economic_pressure * 0.25

        if agent.personality == "industrious":
            scores["work"] += 20
        elif agent.personality == "lazy":
            scores["work"] -= 20
        time_of_day = getattr(world_state, 'time_of_day', "Day") or "Day"
        if time_of_day in ("Night", "Dawn"):
            scores["work"] -= 20

        # ── SLEEP ────────────────────────────────────────────
        energy_need = 100.0 - agent.energy
        scores["sleep"] = energy_need * 0.65
        if agent.personality == "lazy":
            scores["sleep"] += 10
        if time_of_day == "Night":
            scores["sleep"] += 30
        if time_of_day in ("Morning", "Afternoon"):
            scores["sleep"] -= 15

        # ── SOCIALIZE ────────────────────────────────────────
        happiness_need = max(0, 70 - agent.happiness) * 0.6
        scores["socialize"] = happiness_need + max(0.0, 35.0 - social_support) * 0.35
        if agent.personality == "social":
            scores["socialize"] += 25
        elif agent.personality == "reclusive":
            scores["socialize"] -= 30
        if agent.energy < 25:
            scores["socialize"] -= 20
        # Single adults have a social drive to meet potential partners
        if not agent.is_married and agent.is_adult:
            scores["socialize"] += 10
        # Married agents socialise less urgently (they're content)
        if agent.is_married:
            scores["socialize"] -= 5
        if distress > 65:
            scores["socialize"] -= 8

        # ── SEEK JOB ─────────────────────────────────────────
        if agent.job is None:
            scores["seek_job"] = 60 if agent.energy > 30 else 10
        else:
            scores["seek_job"] = 0

        # ── SPEND LUXURY ─────────────────────────────────────
        is_wealthy = agent.money > 300
        is_happy_seeker = agent.happiness < 60
        if is_wealthy and is_happy_seeker:
            scores["spend_luxury"] = 30 + (60 - agent.happiness) * 0.5 + distress * 0.08
        elif agent.personality == "reckless" and agent.money > 100:
            scores["spend_luxury"] = 20
        else:
            scores["spend_luxury"] = 0

        # ── IDLE ─────────────────────────────────────────────
        scores["idle"] = 4.0 + max(0.0, distress - 70.0) * 0.12

        # ── VISIT DOCTOR ──────────────────────────────────────
        if getattr(agent, "is_sick", False):
            # Only go to doctor if you can afford it, or severity is very high and you risk it anyway
            if agent.money >= 30:
                scores["visit_doctor"] = 20 + getattr(agent, "illness_severity", 0) * 1.5
            else:
                scores["visit_doctor"] = getattr(agent, "illness_severity", 0) * 0.5
        else:
            scores["visit_doctor"] = 0.0

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
        if agent.happiness < 40 and agent.money > 200 and random.random() < 0.02:
            return True
            
        # Example condition 2: High number of rivals, creating social tension
        if agent.rival_count > 1 and random.random() < 0.01:
            return True

        # Example condition 3: Starving but has no money
        food_cost = getattr(world_state, 'food_cost', 50) or 50  # Default if missing
        if agent.hunger < 30 and agent.money < food_cost and random.random() < 0.02:
            return True

        return False

    def _ai_decide(self, agent: Agent, world_state) -> str:
        """
        Builds a context-rich prompt and asks Groq to choose an action.
        """
        prompt = f"""Agent Profile:
Name: {agent.name} | Gender: {agent.gender} | Age: {agent.age_years:.0f} years
Personality: {agent.personality} | Married: {agent.is_married}
Traits: {agent.traits}
State: Hunger={agent.hunger:.0f}/100, Energy={agent.energy:.0f}/100, Happiness={agent.happiness:.0f}/100, Money=${agent.money:.0f}
Job: {agent.job or 'Unemployed'} | Friends: {agent.friend_count} | Rivals: {agent.rival_count}
Goal: {agent.goal}

Memory:
{agent.memory.build_context_string(n_recent=4, n_significant=3)}

World: Time={getattr(world_state, 'time_of_day', 'Day')}, Weather={getattr(world_state, 'weather', 'Clear')}, Food=${getattr(world_state, 'food_cost', 20):.2f}

Valid Actions: {ACTIONS}
Choose the ONE best action for this agent right now. Respond only in JSON:
{{
  "reasoning": "brief 1-sentence why",
  "action": "exact_action_string"
}}"""
        try:
            response_text = self.groq_client.complete(prompt)
        except (ValueError, Exception) as e:
            logger.warning(f"Groq API call failed for {agent.name}: {e}")
            return None
        
        try:
            data = json.loads(response_text)
            action = data.get("action")
            reason = data.get("reasoning")
            
            # Validate action is in allowed list
            if action not in ACTIONS:
                logger.warning(f"AI returned invalid action '{action}' for {agent.name}")
                return None
            
            # Announce the AI decision to the event bus if it's interesting
            if action and reason:
                logger.info(f"🧠 [AI] {agent.name} decided to '{action}': {reason}")
            
            return action
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.warning(f"AI returned invalid JSON for {agent.name}: {e}")
            return None
