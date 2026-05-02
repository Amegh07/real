"""
Ontology and dimensional state helpers.

The simulator does not attempt to hand-author millions of features.
Instead, it maintains a stable dimensional vocabulary that can be
expanded with generated feature specifications over time.
"""

from dataclasses import asdict, dataclass, field
from typing import Dict, List

try:
    from ontology.biological_features import (
        get_bio_feature,
        get_features_by_system,
        get_all_feature_ids,
        get_feature_count,
        BioSystem,
    )
except ImportError:
    get_bio_feature = None
    get_features_by_system = None
    get_all_feature_ids = None
    get_feature_count = None
    BioSystem = None


@dataclass(frozen=True)
class MasterDimension:
    key: str
    name: str
    description: str
    examples: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class FeatureSpecificationTemplate:
    required_sections: List[str]
    taxonomy_axes: Dict[str, List[str]]
    constraints: List[str]


MASTER_DIMENSIONS: List[MasterDimension] = [
    MasterDimension(
        key="biophysical",
        name="Biophysical Entity States",
        description="Physiology, metabolism, illness burden, and bodily regulation.",
        examples=["hunger", "energy", "immune load", "sleep debt"],
    ),
    MasterDimension(
        key="cognitive",
        name="Cognitive Architecture",
        description="Attention, planning, learning, and adaptive control.",
        examples=["focus", "decision clarity", "planning horizon"],
    ),
    MasterDimension(
        key="affective",
        name="Emotional and Affective States",
        description="Mood, stress, resilience, and emotional volatility.",
        examples=["stress", "morale", "affective stability"],
    ),
    MasterDimension(
        key="social",
        name="Social Relationship Topology",
        description="Friendship, rivalry, trust, kinship, and social support.",
        examples=["friend_count", "rival_count", "social_support"],
    ),
    MasterDimension(
        key="economic",
        name="Economic Agent State",
        description="Wealth, income pressure, purchasing power, and scarcity.",
        examples=["cash", "job stability", "deprivation"],
    ),
    MasterDimension(
        key="institutional",
        name="Institutional Embeddedness",
        description="Employment role, civic position, and access to systems.",
        examples=["employment", "role legitimacy", "access"],
    ),
    MasterDimension(
        key="environmental",
        name="Physical Environment Interaction",
        description="Weather, climate strain, and local environmental exposure.",
        examples=["weather_load", "shelter quality", "resource access"],
    ),
    MasterDimension(
        key="temporal",
        name="Temporal Biography",
        description="Age, life stage, major events, and developmental trajectory.",
        examples=["age", "life_stage", "recent_events"],
    ),
    MasterDimension(
        key="pathology",
        name="Pathogen and Disease Space",
        description="Illness risk, severity, recovery, and vulnerability.",
        examples=["is_sick", "illness_severity", "frailty"],
    ),
    MasterDimension(
        key="material",
        name="Material Culture and Technology",
        description="Tools, job equipment, and productive material access.",
        examples=["tool_access", "job_capability", "consumption options"],
    ),
    MasterDimension(
        key="communication",
        name="Communication Acts",
        description="Interaction frequency, expressive bandwidth, and social signal.",
        examples=["expression_drive", "outreach_tendency", "narrative salience"],
    ),
    MasterDimension(
        key="causal",
        name="Causal History and Counterfactuals",
        description="Accumulated causes, recent shocks, and narrative momentum.",
        examples=["crisis_load", "life_event_pressure", "recovery_headroom"],
    ),
]


FEATURE_SPEC_TEMPLATE = FeatureSpecificationTemplate(
    required_sections=[
        "feature_name",
        "mechanism",
        "state_space",
        "measurement",
        "upstream_causes",
        "downstream_effects",
        "interaction_rules",
        "pathological_extremes",
        "real_world_validation",
        "implementation_notes",
    ],
    taxonomy_axes={
        "domain": [
            "Biophysical",
            "Cognitive",
            "Affective",
            "Social",
            "Economic",
            "Political",
            "Environmental",
            "Technological",
            "Informational",
            "Temporal",
        ],
        "scale": [
            "Molecular",
            "Cellular",
            "Organ",
            "Organism",
            "Dyad",
            "Group",
            "Institution",
            "Population",
            "Ecosystem",
            "Planetary",
        ],
        "timescale": [
            "Instantaneous",
            "Seconds",
            "Minutes",
            "Hours",
            "Days",
            "Weeks",
            "Months",
            "Years",
            "Decades",
            "Centuries",
            "Millennia",
        ],
        "observability": [
            "Directly measurable",
            "Instrument-dependent",
            "Self-report only",
            "Latent/inferential",
            "Counterfactual",
        ],
        "reversibility": [
            "Fully reversible",
            "Partially reversible",
            "Hysteretic",
            "Irreversible",
            "Catastrophic",
        ],
        "emergence_class": [
            "Compositional",
            "Synergistic",
            "Phase transition",
            "Self-organizing",
            "Evolutionary",
        ],
    },
    constraints=[
        "No magic numbers without derivation.",
        "No globally visible omniscient state.",
        "No symmetric relationships by default.",
        "No instant propagation without delay.",
        "No assumption of equilibrium.",
    ],
)


def get_master_dimensions_snapshot() -> List[dict]:
    return [asdict(dimension) for dimension in MASTER_DIMENSIONS]


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def build_agent_dimension_state(agent) -> Dict[str, dict]:
    """
    Derive a higher-level dimensional state from the compact agent model.

    These are intentionally generated views rather than persisted master data,
    which keeps the current engine small while still exposing a richer ontology.
    """
    hunger_deficit = 100.0 - agent.hunger
    fatigue = 100.0 - agent.energy
    morale_gap = 100.0 - agent.happiness
    stress_load = _clamp((hunger_deficit * 0.45) + (fatigue * 0.35) + (morale_gap * 0.20))
    deprivation = _clamp((hunger_deficit * 0.5) + max(0.0, 150.0 - agent.money) * 0.12)
    social_support = _clamp(agent.friend_count * 18.0 - agent.rival_count * 8.0)
    illness_burden = _clamp(agent.illness_severity if getattr(agent, "is_sick", False) else 0.0)
    resilience = _clamp(
        (agent.traits.get("empathy", 0.5) * 25.0)
        + (agent.traits.get("ambition", 0.5) * 20.0)
        + (agent.happiness * 0.35)
        - (illness_burden * 0.25)
    )
    planning_horizon = _clamp(
        (agent.traits.get("ambition", 0.5) * 45.0)
        + (agent.traits.get("risk_tolerance", 0.5) * 10.0)
        + (agent.energy * 0.25)
    )
    job_capability = _clamp(
        (agent.skills.get(agent.job, 0.0) if agent.job else 0.0)
        + (agent.energy * 0.25)
        + (agent.traits.get("ambition", 0.5) * 20.0)
    )

    # ── Section C1: Core Affect & Emotional States ───────────
    affect_valence = getattr(agent, "affect_valence", 0.5)
    affect_arousal = getattr(agent, "affect_arousal", 0.5)
    affect_dominance = getattr(agent, "affect_dominance", 0.5)
    emotional_granularity = getattr(agent, "emotional_granularity", 0.5)
    rumination_depth = getattr(agent, "rumination_depth", 0.3)
    anhedonia_severity = getattr(agent, "anhedonia_severity", 0.0)
    emotional_blunting = getattr(agent, "emotional_blunting", 0.0)
    alexithymia = getattr(agent, "alexithymia", 0.2)
    mood_congruent_memory = getattr(agent, "mood_congruent_memory", 0.4)
    hedonic_adaptation = getattr(agent, "hedonic_adaptation_rate", 0.3)

    # ── Section C2: Big Five & Dark Traits ───────────
    big_five = getattr(agent, "big_five", {})
    openness = big_five.get("openness", 0.5)
    conscientiousness = big_five.get("conscientiousness", 0.5)
    extraversion = big_five.get("extraversion", 0.5)
    agreeableness = big_five.get("agreeableness", 0.5)
    neuroticism = big_five.get("neuroticism", 0.5)

    machiavellianism = getattr(agent, "machiavellianism", 0.2)
    narcissism = getattr(agent, "narcissism_grandiose", 0.2) + getattr(agent, "narcissism_vulnerable", 0.1)
    psychopathy = getattr(agent, "psychopathy_primary", 0.0) + getattr(agent, "psychopathy_secondary", 0.0)
    honesty_humility = getattr(agent, "honesty_humility", 0.6)

    # Attachment
    attachment_anxiety = getattr(agent, "attachment_anxiety", 0.3)
    attachment_avoidance = getattr(agent, "attachment_avoidance", 0.3)
    if attachment_anxiety > 0.4 and attachment_avoidance < 0.3:
        attachment_style_label = "anxious"
    elif attachment_anxiety < 0.3 and attachment_avoidance > 0.4:
        attachment_style_label = "avoidant"
    elif attachment_anxiety < 0.4 and attachment_avoidance < 0.4:
        attachment_style_label = "secure"
    else:
        attachment_style_label = "fearful-avoidant"

    # Behavioral systems
    behavioral_inhibition = getattr(agent, "behavioral_inhibition", 0.4)
    behavioral_activation = getattr(agent, "behavioral_activation", 0.6)
    sensation_seeking = getattr(agent, "sensation_seeking", 0.4)

    # ── Section D1: Kinship ───────────────────────────
    genetic_relatedness = getattr(agent, "genetic_relatedness", 0.0)
    lineage_depth = getattr(agent, "lineage_depth", 0)
    rivalry_intensity = getattr(agent, "rivalry_intensity", 0.3)
    family_size = getattr(agent, "family_size", 0)
    birth_order = getattr(agent, "birth_order", 0)

    # ── Section D2: Romantic ───────────────────────────
    passion_intensity = getattr(agent, "passion_intensity", 0.6)
    intimacy_depth = getattr(agent, "intimacy_depth", 0.3)
    commitment_level = getattr(agent, "commitment_level", 0.5)
    infidelity_prob = getattr(agent, "infidelity_probability", 0.2)

    # ── Section D3: Professional ───────────────────────
    power_asymmetry = getattr(agent, "power_asymmetry", 0.5)
    collaboration_freq = getattr(agent, "collaboration_frequency", 0.4)
    competition_int = getattr(agent, "competition_intensity", 0.3)
    networking_val = getattr(agent, "networking_value", 0.4)
    workload_comp = getattr(agent, "workload_comparison", 0.5)

    return {
        "biophysical": {
            "homeostasis": round(_clamp(100.0 - (hunger_deficit * 0.45 + fatigue * 0.40 + illness_burden * 0.30)), 1),
            "nutrition_stability": round(agent.hunger, 1),
            "sleep_reserve": round(agent.energy, 1),
            "stress_load": round(stress_load, 1),
        },
        "cognitive": {
            "planning_horizon": round(planning_horizon, 1),
            "decision_clarity": round(_clamp(agent.energy * 0.55 + agent.happiness * 0.30 - illness_burden * 0.20), 1),
            "risk_posture": round(agent.traits.get("risk_tolerance", 0.5) * 100.0, 1),
        },
        "affective": {
            "morale": round(agent.happiness, 1),
            "resilience": round(resilience, 1),
            "distress": round(_clamp(stress_load * 0.75 + illness_burden * 0.35 - social_support * 0.20), 1),
            # Section C1: Core Affect
            "valence": round(affect_valence, 3),
            "arousal": round(affect_arousal, 3),
            "dominance": round(affect_dominance, 3),
            "emotional_granularity": round(emotional_granularity, 3),
            "rumination": round(rumination_depth, 3),
            "anhedonia": round(anhedonia_severity, 3),
            "emotional_blunting": round(emotional_blunting, 3),
            "alexithymia": round(alexithymia, 3),
            "mood_congruent_memory": round(mood_congruent_memory, 3),
            "hedonic_adaptation": round(hedonic_adaptation, 3),
        },
        "social": {
            "friend_count": agent.friend_count,
            "rival_count": agent.rival_count,
            "social_support": round(social_support, 1),
            "bonded_status": "married" if agent.is_married else "single",
            # Section C2: Attachment
            "attachment_style": attachment_style_label,
            "attachment_anxiety": round(attachment_anxiety, 3),
            "attachment_avoidance": round(attachment_avoidance, 3),
            # Section D1: Kinship
            "genetic_relatedness": round(genetic_relatedness, 3),
            "lineage_depth": lineage_depth,
            "rivalry_intensity": round(rivalry_intensity, 3),
            "family_size": family_size,
            "birth_order": birth_order,
            # Section D2: Romantic
            "passion_intensity": round(passion_intensity, 3),
            "intimacy_depth": round(intimacy_depth, 3),
            "commitment_level": round(commitment_level, 3),
            "infidelity_risk": round(infidelity_prob, 3),
        },
        "economic": {
            "liquidity": round(agent.money, 2),
            "income_rate": round(agent.income_per_tick, 2),
            "deprivation_risk": round(deprivation, 1),
            "job_security": round(75.0 if agent.job else 15.0, 1),
        },
        "institutional": {
            "employment_status": "employed" if agent.job else "unemployed",
            "role": agent.job or "civilian",
            "civic_access": round(60.0 if agent.is_adult else 15.0, 1),
        },
        "environmental": {
            "weather_exposure": 50.0,
            "shelter_security": round(55.0 + (20.0 if agent.money > 150 else 0.0), 1),
        },
        "temporal": {
            "age_years": round(agent.age_years, 1),
            "life_stage": "adult" if agent.is_adult else "child",
            "recent_life_events": agent.life_events[-3:],
        },
        "pathology": {
            "is_sick": getattr(agent, "is_sick", False),
            "illness_burden": round(illness_burden, 1),
            "frailty": round(_clamp((agent.age_years / 85.0) * 100.0 + illness_burden * 0.25), 1),
        },
        "material": {
            "job_capability": round(job_capability, 1),
            "tool_access": round(65.0 if agent.job else 25.0, 1),
            "consumption_bandwidth": round(_clamp(agent.money * 0.35), 1),
        },
        "communication": {
            "outreach_drive": round(_clamp(agent.traits.get("sociability", 0.5) * 100.0 + max(0.0, 65.0 - agent.happiness) * 0.30), 1),
            "expressive_pressure": round(_clamp(stress_load * 0.55 + max(0.0, 70.0 - agent.happiness) * 0.45), 1),
        },
        "causal": {
            "crisis_load": round(_clamp(deprivation * 0.45 + illness_burden * 0.35 + max(0.0, 40.0 - social_support) * 0.20), 1),
            "recovery_headroom": round(_clamp(resilience - stress_load * 0.40), 1),
            "goal_vector": agent.goal,
        },
        # ── Section C2: Personality ───────────────────────
        "personality": {
            "big_five": {
                "openness": round(openness, 3),
                "conscientiousness": round(conscientiousness, 3),
                "extraversion": round(extraversion, 3),
                "agreeableness": round(agreeableness, 3),
                "neuroticism": round(neuroticism, 3),
            },
            "dark_triad": {
                "machiavellianism": round(machiavellianism, 3),
                "narcissism": round(narcissism, 3),
                "psychopathy": round(psychopathy, 3),
            },
            "honesty_humility": round(honesty_humility, 3),
            "behavioral_inhibition": round(behavioral_inhibition, 3),
            "behavioral_activation": round(behavioral_activation, 3),
            "sensation_seeking": round(sensation_seeking, 3),
        },
        # ── Section D3: Professional ───────────────────────
        "professional": {
            "hierarchy_direction": getattr(agent, "hierarchy_direction", "peer"),
            "power_asymmetry": round(power_asymmetry, 3),
            "collaboration_frequency": round(collaboration_freq, 3),
            "competition_intensity": round(competition_int, 3),
            "networking_value": round(networking_val, 3),
            "workload_comparison": round(workload_comp, 3),
            "information_asymmetry": round(getattr(agent, "information_asymmetry", 0.5), 3),
        },
    }


def build_world_dimension_state(world_state, economy, agents: List) -> Dict[str, dict]:
    population = len(agents)
    if population == 0:
        return {
            "population": 0,
            "dimensions": {},
        }

    avg = lambda values: round(sum(values) / len(values), 2) if values else 0.0

    stress_values = []
    deprivation_values = []
    support_values = []
    illness_values = []
    morale_values = []
    planning_values = []
    capability_values = []
    outreach_values = []
    crisis_values = []
    resilience_values = []
    age_values = []
    role_legibility_values = []

    derived_snapshots = []
    for agent in agents:
        derived = build_agent_dimension_state(agent)
        derived_snapshots.append(derived)
        stress_values.append(derived["biophysical"]["stress_load"])
        deprivation_values.append(derived["economic"]["deprivation_risk"])
        support_values.append(derived["social"]["social_support"])
        illness_values.append(derived["pathology"]["illness_burden"])
        morale_values.append(derived["affective"]["morale"])
        planning_values.append(derived["cognitive"]["planning_horizon"])
        capability_values.append(derived["material"]["job_capability"])
        outreach_values.append(derived["communication"]["outreach_drive"])
        crisis_values.append(derived["causal"]["crisis_load"])
        resilience_values.append(derived["affective"]["resilience"])
        age_values.append(derived["temporal"]["age_years"])
        role_legibility_values.append(80.0 if derived["institutional"]["employment_status"] == "employed" else 25.0)

    return {
        "population": population,
        "dimensions": {
            "biophysical": {
                "avg_stress_load": avg(stress_values),
                "avg_homeostasis": avg([d["biophysical"]["homeostasis"] for d in derived_snapshots]),
                "avg_sleep_reserve": avg([d["biophysical"]["sleep_reserve"] for d in derived_snapshots]),
            },
            "cognitive": {
                "avg_planning_horizon": avg(planning_values),
                "avg_decision_clarity": avg([d["cognitive"]["decision_clarity"] for d in derived_snapshots]),
                "avg_risk_posture": avg([d["cognitive"]["risk_posture"] for d in derived_snapshots]),
            },
            "affective": {
                "avg_morale": avg(morale_values),
                "avg_resilience": avg(resilience_values),
                "avg_distress": avg([d["affective"]["distress"] for d in derived_snapshots]),
            },
            "social": {
                "avg_support": avg(support_values),
                "friendship_density_hint": round(avg([a.friend_count for a in agents]), 2),
                "married_agents": sum(1 for a in agents if a.is_married),
            },
            "economic": {
                "treasury": round(economy.treasury, 2),
                "inflation_rate": round(economy.inflation_rate, 4),
                "avg_deprivation_risk": avg(deprivation_values),
                "avg_liquidity": avg([d["economic"]["liquidity"] for d in derived_snapshots]),
            },
            "institutional": {
                "employment_rate": round(sum(1 for a in agents if a.job) / population, 4),
                "avg_role_legibility": avg(role_legibility_values),
                "adult_share": round(sum(1 for a in agents if a.is_adult) / population, 4),
            },
            "environmental": {
                "weather": world_state.weather,
                "time_of_day": world_state.time_of_day,
                "day": world_state.day,
                "avg_shelter_security": avg([d["environmental"]["shelter_security"] for d in derived_snapshots]),
            },
            "temporal": {
                "avg_age_years": avg(age_values),
                "children": sum(1 for a in agents if not a.is_adult),
                "recent_life_events": sum(len(a.life_events[-3:]) for a in agents),
            },
            "pathology": {
                "avg_illness_burden": avg(illness_values),
                "active_cases": sum(1 for a in agents if getattr(a, "is_sick", False)),
            },
            "material": {
                "avg_job_capability": avg(capability_values),
                "avg_tool_access": avg([d["material"]["tool_access"] for d in derived_snapshots]),
            },
            "communication": {
                "avg_outreach_drive": avg(outreach_values),
                "avg_expressive_pressure": avg([d["communication"]["expressive_pressure"] for d in derived_snapshots]),
            },
            "causal": {
                "avg_crisis_load": avg(crisis_values),
                "avg_recovery_headroom": avg([d["causal"]["recovery_headroom"] for d in derived_snapshots]),
            },
        },
    }
