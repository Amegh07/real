"""
Disease progression and contagion.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class DiseaseProfile:
    disease_id: str
    display_name: str
    infectiousness: float
    base_severity_gain: float
    recovery_rate: float
    mortality_threshold: float
    min_duration_ticks: int
    treatment_effect: float
    weather_risk: Dict[str, float]


DISEASE_REGISTRY: Dict[str, DiseaseProfile] = {
    "common_cold": DiseaseProfile(
        disease_id="common_cold",
        display_name="Common Cold",
        infectiousness=0.06,
        base_severity_gain=1.2,
        recovery_rate=2.2,
        mortality_threshold=95.0,
        min_duration_ticks=2,
        treatment_effect=8.0,
        weather_risk={"Cloudy": 0.004, "Rainy": 0.007, "Stormy": 0.010},
    ),
    "stomach_flu": DiseaseProfile(
        disease_id="stomach_flu",
        display_name="Stomach Flu",
        infectiousness=0.04,
        base_severity_gain=2.0,
        recovery_rate=1.8,
        mortality_threshold=90.0,
        min_duration_ticks=3,
        treatment_effect=10.0,
        weather_risk={"Rainy": 0.005, "Stormy": 0.006},
    ),
    "lung_fever": DiseaseProfile(
        disease_id="lung_fever",
        display_name="Lung Fever",
        infectiousness=0.025,
        base_severity_gain=2.6,
        recovery_rate=1.4,
        mortality_threshold=82.0,
        min_duration_ticks=4,
        treatment_effect=13.0,
        weather_risk={"Cloudy": 0.003, "Rainy": 0.007, "Stormy": 0.012},
    ),
}


class HealthSystem:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def infect(self, agent, disease_id: str, tick: int, cause: str = "exposure") -> bool:
        if agent.is_dead or agent.is_sick:
            return False
        disease = DISEASE_REGISTRY[disease_id]
        agent.is_sick = True
        agent.active_disease = disease_id
        agent.disease_name = disease.display_name
        agent.illness_severity = max(agent.illness_severity, random.uniform(8.0, 18.0))
        agent.sick_since_tick = tick
        agent.last_treatment_tick = None
        agent.memory.record(
            tick,
            f"I came down with {disease.display_name.lower()}.",
            importance=7,
            emotion="fearful",
        )
        agent._refresh_dimension_state()
        self.event_bus.emit(f"[HEALTH] {agent.name} contracted {disease.display_name}.")
        self.event_bus.emit_causal(
            tick=tick,
            category="pathology",
            source=cause,
            target=agent.name,
            summary=f"{agent.name} contracted {disease.display_name}.",
            mechanism="Disease exposure exceeded the agent's resistance threshold.",
            confidence=0.8,
            reversibility="partial",
            evidence=[f"disease={disease_id}", f"severity={round(agent.illness_severity, 1)}"],
        )
        return True

    def apply_treatment(self, agent, tick: int) -> bool:
        if not agent.is_sick or not agent.active_disease:
            return False
        disease = DISEASE_REGISTRY[agent.active_disease]
        agent.illness_severity = max(0.0, agent.illness_severity - disease.treatment_effect)
        agent.last_treatment_tick = tick
        agent.happiness = min(100.0, agent.happiness + 6.0)
        agent.energy = min(100.0, agent.energy + 8.0)
        if agent.illness_severity <= 0.0:
            recovered_name = disease.display_name
            agent.is_sick = False
            agent.active_disease = None
            agent.disease_name = ""
            agent.sick_since_tick = None
            agent.last_treatment_tick = None
            agent.memory.record(tick, f"I recovered from {recovered_name.lower()} after treatment.", importance=7, emotion="happy")
        agent._refresh_dimension_state()
        self.event_bus.emit_causal(
            tick=tick,
            category="pathology",
            source="treatment",
            target=agent.name,
            summary=f"{agent.name} received treatment for {disease.display_name}.",
            mechanism="Medical intervention reduced illness severity and improved recovery odds.",
            confidence=0.95,
            reversibility="reversible",
            evidence=[f"severity={round(agent.illness_severity, 1)}"],
        )
        return True

    def tick(self, tick: int, agents: List, rel_graph, weather: str):
        self._seed_weather_illness(tick, agents, weather)
        self._spread_contagion(tick, agents, rel_graph)
        self._progress_illness(tick, agents)

    def _seed_weather_illness(self, tick: int, agents: List, weather: str):
        for agent in agents:
            if agent.is_dead or agent.is_sick:
                continue
            weakness = max(0.0, (40.0 - agent.energy) * 0.0004) + max(0.0, (40.0 - agent.hunger) * 0.0003)
            for disease_id, profile in DISEASE_REGISTRY.items():
                risk = profile.weather_risk.get(weather, 0.0) + weakness
                if random.random() < risk:
                    self.infect(agent, disease_id, tick, cause=f"weather:{weather.lower()}")
                    break

    def _spread_contagion(self, tick: int, agents: List, rel_graph):
        alive = [agent for agent in agents if not agent.is_dead]
        agent_by_id = {agent.id: agent for agent in alive}
        for carrier in alive:
            if not carrier.is_sick or not carrier.active_disease:
                continue
            profile = DISEASE_REGISTRY[carrier.active_disease]
            contacts = []
            if carrier.spouse_id and carrier.spouse_id in agent_by_id:
                contacts.append(agent_by_id[carrier.spouse_id])
            contacts.extend(
                agent_by_id[rel.target_id]
                for rel in rel_graph.get_friends(carrier.id)[:2]
                if rel.target_id in agent_by_id
            )
            if alive:
                contacts.append(random.choice(alive))

            seen = set()
            for target in contacts:
                if target.id == carrier.id or target.id in seen or target.is_sick or target.is_dead:
                    continue
                seen.add(target.id)
                vulnerability = 1.0 + max(0.0, (35.0 - target.energy) / 50.0) + max(0.0, (35.0 - target.hunger) / 60.0)
                chance = profile.infectiousness * vulnerability
                if random.random() < chance:
                    relation_cause = f"contact:{carrier.name}"
                    self.infect(target, carrier.active_disease, tick, cause=relation_cause)
                    self.event_bus.emit_causal(
                        tick=tick,
                        category="pathology",
                        source=carrier.name,
                        target=target.name,
                        summary=f"{carrier.name} likely spread {profile.display_name} to {target.name}.",
                        mechanism="Repeated social proximity transferred an infectious disease between agents.",
                        confidence=0.65,
                        reversibility="partial",
                        evidence=[f"disease={carrier.active_disease}"],
                    )

    def _progress_illness(self, tick: int, agents: List):
        for agent in agents:
            if not agent.is_sick or not agent.active_disease or agent.is_dead:
                continue
            profile = DISEASE_REGISTRY[agent.active_disease]
            resilience = agent.dimension_state.get("affective", {}).get("resilience", 50.0)
            support = agent.dimension_state.get("social", {}).get("social_support", 0.0)
            treatment_bonus = 1.5 if agent.last_treatment_tick == tick else 0.0
            recovery_force = profile.recovery_rate + (resilience * 0.035) + (support * 0.015) + treatment_bonus
            illness_force = profile.base_severity_gain + max(0.0, (30.0 - agent.energy) * 0.06) + max(0.0, (30.0 - agent.hunger) * 0.05)
            net = illness_force - recovery_force
            agent.illness_severity = max(0.0, min(100.0, agent.illness_severity + net))

            duration = tick - (agent.sick_since_tick or tick)
            if duration >= profile.min_duration_ticks and agent.illness_severity <= 6.0:
                agent.is_sick = False
                recovered_name = profile.display_name
                agent.active_disease = None
                agent.disease_name = ""
                agent.illness_severity = 0.0
                agent.sick_since_tick = None
                agent.last_treatment_tick = None
                agent.memory.record(tick, f"I recovered from {recovered_name.lower()}.", importance=6, emotion="happy")
                agent._refresh_dimension_state()
                self.event_bus.emit(f"[HEALTH] {agent.name} recovered from {recovered_name}.")
                self.event_bus.emit_causal(
                    tick=tick,
                    category="pathology",
                    source=recovered_name,
                    target=agent.name,
                    summary=f"{agent.name} recovered from {recovered_name}.",
                    mechanism="Recovery forces exceeded disease progression long enough for symptoms to resolve.",
                    confidence=0.92,
                    reversibility="reversible",
                    evidence=[f"duration={duration}"],
                )
                continue

            if agent.illness_severity >= profile.mortality_threshold:
                death_roll = 0.12 + max(0.0, (agent.illness_severity - profile.mortality_threshold) * 0.01)
                if random.random() < death_roll:
                    agent.is_dead = True
                    agent.death_reason = profile.display_name
            agent._refresh_dimension_state()
