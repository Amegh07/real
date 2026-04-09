"""
AI Game Master (Phase 8)
------------------------
Scans world health every N ticks and uses Groq to generate a
narrative Global World Event based on real simulation metrics.

Events can:
  - Change the treasury (gold rush, famine, trade deal)
  - Affect all agents' happiness (festival, disaster)
  - Change weather dramatically
  - Trigger new job waves (construction boom)

The Game Master pushes its event into the main AI Task Queue
so it respects the 25-RPM rate limiting.
"""

import json
import random
from utils.logger import get_logger

logger = get_logger(__name__)

WORLD_EVENT_INTERVAL = 100   # Ticks between world event evaluations

# Fallback events if Groq is unavailable
FALLBACK_EVENTS = [
    {
        "headline": "A merchant caravan arrives!",
        "treasury_delta": 3000,
        "happiness_delta": 8,
        "narrative": "Traders from the east have brought exotic goods. The market booms.",
    },
    {
        "headline": "A long drought dries up the fields.",
        "treasury_delta": -2000,
        "happiness_delta": -10,
        "narrative": "Crops are failing. Food prices are rising and morale is low.",
    },
    {
        "headline": "The town hosts a grand festival!",
        "treasury_delta": -1500,
        "happiness_delta": 20,
        "narrative": "Music, dancing, and feasting fill the streets for three days.",
    },
    {
        "headline": "A new vein of ore is discovered.",
        "treasury_delta": 5000,
        "happiness_delta": 5,
        "narrative": "Miners have struck gold. The treasury overflows with new revenue.",
    },
    {
        "headline": "A plague sweeps through the town.",
        "treasury_delta": -1000,
        "happiness_delta": -20,
        "narrative": "Sickness spreads. The healers are overwhelmed. People are afraid.",
    },
    {
        "headline": "The King levies a new tax.",
        "treasury_delta": 4000,
        "happiness_delta": -8,
        "narrative": "Royal tax collectors have arrived. Agents grumble but comply.",
    },
]


class AIGameMaster:
    """
    Monitors World State and injects narrative Global Events.
    Uses Groq for event generation based on economic conditions.
    Falls back to curated events if Groq is unavailable.
    """

    def __init__(self, groq_client, world_state, event_bus):
        self.groq_client = groq_client
        self.world_state = world_state
        self.event_bus = event_bus
        self._last_event_tick = 0

    def should_trigger(self, tick: int) -> bool:
        """Check if it's time to generate a world event."""
        if tick - self._last_event_tick >= WORLD_EVENT_INTERVAL:
            # Add slight randomness so events don't feel mechanical
            return random.random() < 0.6
        return False

    def generate_and_apply_event(self, tick: int, agents: list, economy) -> dict:
        """Generate a world event and apply it. Returns the event dict."""
        self._last_event_tick = tick

        # Build world context snapshot for the AI
        avg_happiness = sum(a.happiness for a in agents) / max(len(agents), 1)
        employed = sum(1 for a in agents if a.job)
        unemployment_rate = 1.0 - (employed / max(len(agents), 1))

        context = {
            "tick": tick,
            "population": len(agents),
            "treasury": round(economy.treasury),
            "inflation": round(economy.inflation_rate, 3),
            "avg_happiness": round(avg_happiness, 1),
            "unemployment_rate": round(unemployment_rate, 2),
            "weather": self.world_state.weather,
        }

        event = self._call_ai_event(context)
        if event is None:
            event = random.choice(FALLBACK_EVENTS)
            logger.info(f"[GameMaster] Using fallback event: {event['headline']}")

        # Apply the event's effects to the world
        self._apply_event(event, agents, economy)
        return event

    def _call_ai_event(self, context: dict) -> dict:
        """Call Groq to generate a creative world event based on current metrics."""
        if not self.groq_client or not self.groq_client.enabled:
            return None

        # Decide tone based on conditions
        if context["treasury"] < 5000:
            tone = "dire financial situation. Focus drama on economic hardship."
        elif context["avg_happiness"] < 40:
            tone = "widespread unhappiness. Generate an uplifting opportunity or a further disaster."
        elif context["unemployment_rate"] > 0.3:
            tone = "high unemployment. Generate a job-creating event."
        elif context["inflation"] > 1.5:
            tone = "dangerous inflation. Generate a deflationary event."
        else:
            tone = "stable but uneventful period. Generate excitement or change."

        prompt = f"""You are the Game Master of a medieval village simulation. 
Current world state: {json.dumps(context)}
The mood: {tone}

Generate a surprising, creative world event. Respond ONLY with valid JSON:
{{
  "headline": "Short punchy headline (max 10 words)",
  "narrative": "2-3 sentence story description of what happened",
  "treasury_delta": <integer, positive=gains, negative=loss, range: -8000 to 10000>,
  "happiness_delta": <float, positive=joy, negative=sadness, range: -25 to 25>
}}"""

        try:
            result = self.groq_client.complete(prompt)
            data = json.loads(result)
            # Validate and sanitize
            return {
                "headline": str(data.get("headline", "Something happened"))[:120],
                "narrative": str(data.get("narrative", ""))[:500],
                "treasury_delta": max(-10000, min(15000, int(data.get("treasury_delta", 0)))),
                "happiness_delta": max(-30, min(30, float(data.get("happiness_delta", 0)))),
            }
        except Exception as e:
            logger.warning(f"[GameMaster] AI event generation failed: {e}")
            return None

    def _apply_event(self, event: dict, agents: list, economy):
        """Apply the event's numerical effects to the simulation."""
        # Treasury change
        delta = event.get("treasury_delta", 0)
        economy.treasury = max(0.0, economy.treasury + delta)

        # Happiness change for all agents
        happiness_delta = event.get("happiness_delta", 0)
        for agent in agents:
            agent.happiness = max(0.0, min(100.0, agent.happiness + happiness_delta))

        # Emit the world event to the ledger
        headline = event.get("headline", "A world event occurred.")
        narrative = event.get("narrative", "")
        treasury_str = (f"+${abs(delta):,}" if delta >= 0 else f"-${abs(delta):,}")
        self.event_bus.emit(
            f"[WORLD EVENT] {headline} | Treasury: {treasury_str} | "
            f"Happiness: {'+' if happiness_delta >= 0 else ''}{happiness_delta:.0f}"
        )
        if narrative:
            self.event_bus.emit(f"  [GameMaster] {narrative}")

        logger.info(f"[GameMaster] Applied event: '{headline}' | Treasury: {treasury_str}")
