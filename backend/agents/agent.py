"""
Agent Model — Phase 10: Psychological & Affective Systems
------------------------------------------
Major additions (Section C & D features):
  - Core Affect: valence, arousal, dominance
  - Big Five personality traits (OCEAN)
  - Dark traits: Machiavellianism, Narcissism, Psychopathy
  - Attachment style: anxious/avoidant
  - Behavioral inhibition/activation systems
  - Sensation seeking, harm avoidance
  - Social systems: kinship, relationships
  - Physiology: embodied state with 175 biological features

All values are continuous [0.0 - 1.0] unless otherwise noted.
"""

import uuid
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from utils.logger import get_logger
from memory.memory_bank import MemoryBank
from ontology.dimensions import build_agent_dimension_state
from agents.physiology import PhysiologyModel

logger = get_logger(__name__)

PERSONALITY_TYPES = ["industrious", "lazy", "social", "reclusive", "reckless", "cautious"]

PERSONALITY_TRAITS: Dict[str, Dict[str, float]] = {
    "industrious": {"ambition": 0.9, "sociability": 0.4, "risk_tolerance": 0.3, "empathy": 0.5},
    "lazy":        {"ambition": 0.1, "sociability": 0.5, "risk_tolerance": 0.2, "empathy": 0.4},
    "social":      {"ambition": 0.5, "sociability": 0.9, "risk_tolerance": 0.4, "empathy": 0.8},
    "reclusive":   {"ambition": 0.6, "sociability": 0.1, "risk_tolerance": 0.2, "empathy": 0.3},
    "reckless":    {"ambition": 0.7, "sociability": 0.6, "risk_tolerance": 0.95, "empathy": 0.3},
    "cautious":    {"ambition": 0.5, "sociability": 0.5, "risk_tolerance": 0.05, "empathy": 0.7},
}

BIG_FIVE_DEFAULTS = {
    "industrious": {"openness": 0.7, "conscientiousness": 0.9, "extraversion": 0.4, "agreeableness": 0.5, "neuroticism": 0.3},
    "lazy":        {"openness": 0.4, "conscientiousness": 0.1, "extraversion": 0.5, "agreeableness": 0.5, "neuroticism": 0.4},
    "social":      {"openness": 0.6, "conscientiousness": 0.5, "extraversion": 0.9, "agreeableness": 0.8, "neuroticism": 0.3},
    "reclusive":   {"openness": 0.7, "conscientiousness": 0.6, "extraversion": 0.1, "agreeableness": 0.4, "neuroticism": 0.5},
    "reckless":    {"openness": 0.8, "conscientiousness": 0.3, "extraversion": 0.6, "agreeableness": 0.3, "neuroticism": 0.4},
    "cautious":    {"openness": 0.6, "conscientiousness": 0.8, "extraversion": 0.4, "agreeableness": 0.6, "neuroticism": 0.6},
}

# ── Age constants ────────────────────────────────────────────
TICKS_PER_SIM_YEAR = 5    # Time-Dilation applied! 5 ticks = 1 simulation year
ADULT_AGE_YEARS    = 18   # Become adult at 18 years
FERTILE_AGE_MAX    = 45   # Women can have children up to 45 years
OLD_AGE_START      = 65   # Death probability begins
OLD_AGE_MAX        = 85   # Near-certain death by 85 years


@dataclass
class Agent:
    """
    A single simulated person living in the world.
    Phase 10: Psychological & Affective Systems — Full psychological profile.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""

    # Core needs (0 = critical, 100 = fully satisfied)
    hunger:    float = 80.0
    energy:    float = 80.0
    happiness: float = 70.0

    # Economy
    money: float = 100.0
    income_per_tick: float = 0.0

    # Personality
    personality: str = "industrious"
    traits: Dict[str, float] = field(default_factory=dict)

    # State
    current_action: str = "idle"
    job: Optional[str] = None
    goal: str = "survive"

    # Skills & Health
    skills: Dict[str, float] = field(default_factory=dict)
    is_dead: bool = False
    death_reason: str = ""
    is_sick: bool = False
    illness_severity: float = 0.0
    active_disease: Optional[str] = None
    disease_name: str = ""
    sick_since_tick: Optional[int] = None
    last_treatment_tick: Optional[int] = None

    # Physiology (175 biological features)
    physiology: PhysiologyModel = field(default_factory=PhysiologyModel)

    # Memory
    memory: Optional[MemoryBank] = None

    # Life history
    age_ticks: int = 0
    life_events: List[str] = field(default_factory=list)

    # ── Phase 9: Human Life Cycle ───────────────────────────
    gender: str = "male"          # "male" or "female"
    is_adult: bool = True         # False for newborns until age 18
    is_married: bool = False
    spouse_id: Optional[str] = None
    parent_ids: List[str] = field(default_factory=list)
    children_ids: List[str] = field(default_factory=list)

    # Social counters (updated by RelationshipGraph)
    friend_count: int = 0
    rival_count:  int = 0
    dimension_state: Dict[str, dict] = field(default_factory=dict)
    
    # ── Section E: Financial System Integration ─────────────────
    portfolio_value: float = 0.0
    asset_holdings: Dict[str, float] = field(default_factory=dict)
    debt: float = 0.0
    credit_score: float = 0.7
    
    # ── Section F: Political System Integration ──────────────────
    political_affiliation: str = "independent"
    political_engagement: float = 0.3
    civic_duty: float = 0.5
    trust_government: float = 0.5
    trust_institutions: float = 0.5

    # ── Section C1: Core Affect & Emotional States ───────────
    affect_valence: float = 0.6       # Pleasant vs unpleasant [0-1]
    affect_arousal: float = 0.5         # Activated vs deactivated [0-1]
    affect_dominance: float = 0.6      # In control vs overwhelmed [0-1]
    emotional_granularity: float = 0.5  # Ability to distinguish emotions
    reappraisal_frequency: float = 0.4  # Cognitive reinterpretation
    suppression_tendency: float = 0.2   # Inhibiting expression
    rumination_depth: float = 0.3     # Repetitive negative thought
    acceptance_capacity: float = 0.5   # Allow emotions without judgment
    distraction_efficacy: float = 0.5  # Shifting attention
    social_sharing_intensity: float = 0.4  # Talking about emotions
    experiential_avoidance: float = 0.3 # Escape private experiences
    behavioral_activation_level: float = 0.5  # Engagement with rewarding activities
    anhedonia_severity: float = 0.0   # Inability to feel pleasure
    psychomotor_retardation: float = 0.0  # Slowed movement/thought
    diurnal_mood_variation: float = 0.5    # 0=morning worst, 1=evening worst
    mixed_features: float = 0.0         # Simultaneous depression/mania
    seasonal_pattern: float = 0.5       # 0=winter SAD, 1=summer SAD
    peripartum_onset: float = 0.0      # Pregnancy/postpartum depression
    catatonia_signs: float = 0.0       # Motor immobility
    emotional_blunting: float = 0.0       # Reduced emotional range
    alexithymia: float = 0.2           # Cannot identify emotions
    emotional_contagion_susceptibility: float = 0.5  # Catching others' emotions
    mood_congruent_memory: float = 0.4   # Sad recalls sad
    affective_forecasting_error: float = 0.3  # Predicting future emotions
    hedonic_adaptation_rate: float = 0.3   # Return to baseline

    # ── Section C2: Big Five Personality ───────────────────────
    big_five: Dict[str, float] = field(default_factory=dict)

    # ── Section C2: Dark Traits ────────────────────────────────
    machiavellianism: float = 0.2      # Strategic manipulation
    narcissism_grandiose: float = 0.2      # Dominance, entitlement
    narcissism_vulnerable: float = 0.1    # Hypersensitivity
    psychopathy_primary: float = 0.0    # Callousness, lack of empathy
    psychopathy_secondary: float = 0.0   # Impulsivity, reactive aggression

    # ── Section C2: HEXACO ────────────────────────────────
    honesty_humility: float = 0.6       # Sincerity, fairness

    # ── Section C2: Attachment & Behavioral Systems ────
    attachment_anxiety: float = 0.3    # Fear of abandonment
    attachment_avoidance: float = 0.3  # Fear of intimacy
    behavioral_inhibition: float = 0.4   # Sensitivity to punishment
    behavioral_activation: float = 0.6    # Sensitivity to reward
    sensation_seeking: float = 0.4       # Thrill seeking
    harm_avoidance: float = 0.5          # Anticipatory worry
    novelty_seeking: float = 0.4          # Exploratory excitability
    reward_dependence: float = 0.5     # Sentimentality, persistence

    # ── Section C2: Character (TCI) ────────────────────────
    self_directedness: float = 0.5          # Responsibility, purpose
    cooperativeness: float = 0.5         # Social acceptance
    self_transcendence: float = 0.3       # Spiritual acceptance

    # ── Section C2: Perfectionism ────────────────────────────
    perfectionism_self_oriented: float = 0.5  # High personal standards
    perfectionism_socially_prescribed: float = 0.3  # Others demand perfection

    # ── Section C2: Locus of Control ────────────────────────
    locus_of_control: float = 0.5           # 0=external, 1=internal

    # ── Section D1: Kinship & Family ────────────────────────
    genetic_relatedness: float = 0.0      # r coefficient for relations
    lineage_depth: int = 0              # Generations tracked
    inheritance_expectation: float = 0.3 # Anticipated share
    caregiving_obligation: float = 0.5    # Cultural norm for parent support
    rivalry_intensity: float = 0.3        # Sibling competition
    alliance_history: float = 0.5          # Past cooperation
    estrangement_duration: int = 0          # Time since contact
    reconciliation_potential: float = 0.5  # Willingness to repair
    surrogate_parent: bool = False         # Non-parent as primary caregiver
    step_relation_tension: float = 0.0    # Cinderella effect
    half_sibling: bool = False              # Shared one parent
    adoptive_bond_strength: float = 0.0       # Non-genetic attachment
    foster_care_instability: float = 0.0   # Multiple placements
    orphan_status: bool = False          # Parental loss
    family_size: int = 0                # Number of children
    birth_order: int = 0               # 1=firstborn
    only_child: bool = False             # No siblings
    twin_zygosity: str = "none"         # identical, fraternal, none
    incest_tabo_strength: float = 0.8     # Westermarck effect

    # ── Section D2: Romantic & Sexual ────────────────────────
    attraction_physical: float = 0.5     # Physical attractiveness
    attraction_intellectual: float = 0.5   # Intellectual attraction
    attraction_emotional: float = 0.5      # Emotional safety
    attraction_status: float = 0.5        # Resource potential
    attachment_style_match: float = 0.5       # Partner compatibility
    passion_intensity: float = 0.6        # Lust and infatuation
    intimacy_depth: float = 0.3           # Self-disclosure
    commitment_level: float = 0.5         # Intention to persist
    satisfaction_trajectory: float = 0.5    # U-shaped over marriage
    alternative_monitoring: float = 0.3     # Awareness of alternatives
    investment_size: float = 0.2          # Resources invested
    idealization_degree: float = 0.4        # Positive illusions
    sexual_compatibility: float = 0.5      # Desire match
    jealousy_triggers: str = "emotional"  # emotional vs sexual
    betrayal_sensitivity: float = 0.5    # Threshold for feeling betrayed
    forgiveness_capacity: float = 0.5   # Ability to move on
    breakup_grief_intensity: float = 0.6 # Proportional to investment
    replacement_latency: float = 0.4     # Time to new relationship
    mate_poaching_attempts: float = 0.1  # Pursuing partnered
    infidelity_probability: float = 0.2   # Opportunity + motivation
    contraceptive_knowledge: float = 0.6   # Awareness of methods
    sexual_orientation: str = "straight"   # Orientation
    libido: float = 0.5                 # Sex drive
    reproductive_coercion: float = 0.0     # Partner controlling fertility
    domestic_violence_risk: float = 0.0     # Cycle indicators

    # ── Section D3: Professional & Economic ────────────────
    hierarchy_direction: str = "peer"        # reports_to, supervised_by, peer
    power_asymmetry: float = 0.5          # Authority difference
    dependency_ratio: float = 0.3         # Resource reliance
    expertise_complementarity: float = 0.5    # Skill overlap
    credit_allocation_fairness: float = 0.6  # Who gets recognized
    collaboration_frequency: float = 0.4      # How often work together
    competition_intensity: float = 0.3           # Zero-sum resources
    networking_value: float = 0.4            # Social capital
    reference_potential: float = 0.5         # Willingness to recommend
    blackmail_vulnerability: float = 0.1    # Secrets weaponized
    mentorship_quality: float = 0.0           # Skill transfer
    sponsorship_activation: float = 0.0         # Using influence
    job_referral_likelihood: float = 0.3     # Informal hiring
    information_asymmetry: float = 0.5         # Who knows more
    workload_comparison: float = 0.5            # Perceived fairness
    promotion_race: float = 0.2              # Direct competition
    union_solidarity: float = 0.4              # Collective action
    whistleblower_protection: float = 0.5        # Willingness to report
    non_compete_enforcement: float = 0.3         # Legal restriction
    ip_dispute_risk: float = 0.0              # Who owns ideas

    def __post_init__(self):
        # Validate personality type
        if self.personality not in PERSONALITY_TRAITS:
            self.personality = "industrious"  # Default to valid personality

        if self.memory is None:
            self.memory = MemoryBank(self.name)
        if not self.traits:
            base = PERSONALITY_TRAITS.get(self.personality, PERSONALITY_TRAITS["industrious"])
            self.traits = {
                k: max(0.0, min(1.0, v + random.uniform(-0.1, 0.1)))
                for k, v in base.items()
            }
        if not self.big_five:
            base_b5 = BIG_FIVE_DEFAULTS.get(self.personality, BIG_FIVE_DEFAULTS["industrious"])
            self.big_five = {
                k: max(0.0, min(1.0, v + random.uniform(-0.1, 0.1)))
                for k, v in base_b5.items()
            }
        self._refresh_dimension_state()

    # ─────────────────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────────────────

    @property
    def age_years(self) -> float:
        """Convert raw ticks to simulation years."""
        return self.age_ticks / TICKS_PER_SIM_YEAR

    def _refresh_dimension_state(self):
        self.dimension_state = build_agent_dimension_state(self)

    def is_fertile(self) -> bool:
        """Women aged 18–45 can bear children."""
        return (
            self.gender == "female"
            and self.is_adult
            and self.is_married
            and ADULT_AGE_YEARS <= self.age_years <= FERTILE_AGE_MAX
        )

    # ─────────────────────────────────────────────────────────
    # Tick-level updates
    # ─────────────────────────────────────────────────────────

    def decay_needs(self, tick: int):
        """
        Decay needs each tick. Children decay more slowly.
        Non-linear starvation: hunger drops 2x faster below 30.
        """
        if self.is_dead:
            return

        if not self.is_adult:
            # Children are taken care of — decay at 30% rate
            self.hunger    = max(0.0, self.hunger    - 0.6)
            self.energy    = max(0.0, self.energy    - 0.5)
            self.happiness = max(0.0, self.happiness - 0.3)
            self.age_ticks += 1
            # Check if child has grown into an adult
            if self.age_years >= ADULT_AGE_YEARS and not self.is_adult:
                self.is_adult = True
                self.life_events.append(f"Came of age at {self.age_years:.0f} years old.")
                self.memory.record(tick, "I have become an adult today.", importance=9, emotion="happy")
            self._refresh_dimension_state()
            return

        # ── Normal Needs Decay ────────────────────────────────
        hunger_rate   = 2.0 + self.traits.get("risk_tolerance", 0.3)
        energy_rate   = 1.5 + self.traits.get("ambition", 0.5) * 1.2
        loneliness_penalty = self.traits.get("sociability", 0.5) * 0.5 \
                             if self.friend_count == 0 else 0.0
        happiness_rate = 1.0 + loneliness_penalty

        # Sickness accelerates needs dropping
        if self.is_sick:
            hunger_rate *= 1.5
            energy_rate *= 2.0
            happiness_rate += 1.0

        # Anhedonia deepens sadness
        if self.anhedonia_severity > 0.3:
            happiness_rate *= (1.0 + self.anhedonia_severity * 0.5)
        if self.rumination_depth > 0.4:
            happiness_rate *= (1.0 + self.rumination_depth * 0.3)

        # Experiential avoidance increases needs decay rate
        if self.experiential_avoidance > 0.5:
            energy_rate *= 1.2
            happiness_rate += 1.0

        # Psychomotor retardation slows action
        if self.psychomotor_retardation > 0.3:
            energy_rate *= (1.0 - self.psychomotor_retardation * 0.3)

        # Emotional blunting reduces happiness response
        if self.emotional_blunting > 0.3:
            happiness_rate *= (1.0 + self.emotional_blunting * 0.2)

        # Suppression increases emotional decay
        if self.suppression_tendency > 0.5:
            happiness_rate *= 1.15

        # Non-linear starvation panic
        if self.hunger < 30.0:
            hunger_rate *= 2.0

        self.hunger    = max(0.0, self.hunger    - hunger_rate)
        self.energy    = max(0.0, self.energy    - energy_rate)
        self.happiness = max(0.0, self.happiness - happiness_rate)
        self.age_ticks += 1

        # Core Affect Updates
        valence_shift = (50.0 - self.happiness) * 0.003
        if self.rumination_depth > 0.3:
            valence_shift -= self.rumination_depth * 0.01
        if self.anhedonia_severity > 0.2:
            valence_shift -= self.anhedonia_severity * 0.015
        self.affect_valence = max(0.0, min(1.0, self.affect_valence + valence_shift))

        arousal_shift = (self.is_sick * 0.01) + (self.energy < 30.0 * -0.005)
        self.affect_arousal = max(0.0, min(1.0, self.affect_arousal + arousal_shift))

        if self.hunger < 20.0 or self.energy < 20.0:
            self.affect_dominance = max(0.0, self.affect_dominance - 0.01)
        elif self.happiness > 70.0 and self.energy > 60.0:
            self.affect_dominance = min(1.0, self.affect_dominance + 0.005)

        if self.happiness < 30.0:
            self.emotional_granularity = max(0.0, self.emotional_granularity - 0.005)

        if self.happiness < 40.0:
            self.mood_congruent_memory = min(1.0, self.mood_congruent_memory + 0.002)

        self.affect_valence = self.affect_valence + (0.5 - self.affect_valence) * self.hedonic_adaptation_rate * 0.001

        # ── Death checks ──────────────────────────────────────
        if self.hunger <= 0.0:
            self.is_dead = True
            self.death_reason = "Starvation"
            self.hunger = 0.0

        # Old age: probability ramps from 65 to 85 years
        if self.age_years >= OLD_AGE_START:
            years_over = self.age_years - OLD_AGE_START
            death_prob = min(0.001 + years_over * 0.0003, 0.02)
            if random.random() < death_prob:
                self.is_dead = True
                self.death_reason = "Old Age"

        # ── Memory triggers ───────────────────────────────────
        if self.hunger < 15 and self.hunger > 12:
            self.memory.record(tick, "Getting very hungry.", importance=6, emotion="fearful")
        if self.energy < 15 and self.energy > 12:
            self.memory.record(tick, "Feeling exhausted.", importance=5, emotion="sad")
        self._refresh_dimension_state()

    def apply_action_effect(self, action: str, world_state):
        """Apply the concrete effect of the chosen action."""
        tick = world_state.tick_number

        if action == "eat":
            paid = world_state.charge_food(self)
            if paid:
                self.hunger = min(100.0, self.hunger + 40.0)
                self.happiness = min(100.0, self.happiness + 5.0)
                self.memory.record(tick, "Had a solid meal.", importance=3, emotion="happy")
            else:
                self.hunger = min(100.0, self.hunger + 10.0)
                self.happiness = max(0.0, self.happiness - 10.0)
                self.life_events.append("Couldn't afford food.")
                self.memory.record_critical(tick, "Could not afford food. Went hungry.")

        elif action == "work":
            wage = world_state.pay_wage(self)
            self.money += wage
            self.income_per_tick = wage
            self.energy = max(0.0, self.energy - 5.0)
            self.happiness = min(100.0, self.happiness + 2.0)
            if wage > 0:
                self.memory.record(tick, f"Worked as {self.job} and earned ${wage:.0f}.",
                                   importance=3, emotion="neutral")

        elif action == "sleep":
            self.energy = min(100.0, self.energy + 30.0)
            self.happiness = min(100.0, self.happiness + 4.0)

        elif action == "socialize":
            self.happiness = min(100.0, self.happiness + 8.0)
            self.energy = max(0.0, self.energy - 3.0)

        elif action == "idle":
            self.energy = min(100.0, self.energy + 5.0)

        elif action == "seek_job":
            self.energy = max(0.0, self.energy - 2.0)

        elif action == "spend_luxury":
            pass  # Handled by Economy.spend()

        self._refresh_dimension_state()

    # ─────────────────────────────────────────────────────────
    # Snapshot
    # ─────────────────────────────────────────────────────────

    def get_snapshot(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age_years": round(self.age_years, 1),
            "is_adult": self.is_adult,
            "is_married": self.is_married,
            "spouse_id": self.spouse_id,
            "children_count": len(self.children_ids),
            "hunger": round(self.hunger, 1),
            "energy": round(self.energy, 1),
            "happiness": round(self.happiness, 1),
            "money": round(self.money, 2),
            "personality": self.personality,
            "traits": {k: round(v, 2) for k, v in self.traits.items()},
            "current_action": self.current_action,
            "goal": self.goal,
            "job": self.job,
            "age_ticks": self.age_ticks,
            "friend_count": self.friend_count,
            "rival_count": self.rival_count,
            "life_events": self.life_events[-5:],
            "memory": self.memory.get_snapshot(),
            "skills": self.skills.copy(),
            "is_dead": self.is_dead,
            "death_reason": self.death_reason,
            "is_sick": self.is_sick,
            "illness_severity": round(self.illness_severity, 1),
            "active_disease": self.active_disease,
            "disease_name": self.disease_name,
            "dimensions": self.dimension_state,
            # Section E: Financial
            "financial": {
                "portfolio_value": round(self.portfolio_value, 2),
                "asset_holdings": {k: round(v, 2) for k, v in self.asset_holdings.items()},
                "debt": round(self.debt, 2),
                "credit_score": round(self.credit_score, 2),
            },
            # Section F: Political
            "political": {
                "affiliation": self.political_affiliation,
                "engagement": round(self.political_engagement, 2),
                "civic_duty": round(self.civic_duty, 2),
                "trust_government": round(self.trust_government, 2),
                "trust_institutions": round(self.trust_institutions, 2),
            },
            # Section C1: Core Affect & Emotional States
            "core_affect": {
                "valence": round(self.affect_valence, 3),
                "arousal": round(self.affect_arousal, 3),
                "dominance": round(self.affect_dominance, 3),
            },
            "emotional_regulation": {
                "granularity": round(self.emotional_granularity, 3),
                "reappraisal_frequency": round(self.reappraisal_frequency, 3),
                "suppression_tendency": round(self.suppression_tendency, 3),
                "rumination_depth": round(self.rumination_depth, 3),
                "acceptance_capacity": round(self.acceptance_capacity, 3),
                "distraction_efficacy": round(self.distraction_efficacy, 3),
                "social_sharing_intensity": round(self.social_sharing_intensity, 3),
                "experiential_avoidance": round(self.experiential_avoidance, 3),
            },
            "depression_symptoms": {
                "anhedonia_severity": round(self.anhedonia_severity, 3),
                "psychomotor_retardation": round(self.psychomotor_retardation, 3),
                "diurnal_mood_variation": round(self.diurnal_mood_variation, 3),
                "emotional_blunting": round(self.emotional_blunting, 3),
                "alexithymia": round(self.alexithymia, 3),
            },
            # Section C2: Big Five & Dark Traits
            "big_five": {k: round(v, 3) for k, v in self.big_five.items()},
            "dark_traits": {
                "machiavellianism": round(self.machiavellianism, 3),
                "narcissism_grandiose": round(self.narcissism_grandiose, 3),
                "narcissism_vulnerable": round(self.narcissism_vulnerable, 3),
                "psychopathy_primary": round(self.psychopathy_primary, 3),
                "psychopathy_secondary": round(self.psychopathy_secondary, 3),
            },
            "attachment": {
                "anxiety": round(self.attachment_anxiety, 3),
                "avoidance": round(self.attachment_avoidance, 3),
            },
            "behavioral_systems": {
                "inhibition": round(self.behavioral_inhibition, 3),
                "activation": round(self.behavioral_activation, 3),
                "sensation_seeking": round(self.sensation_seeking, 3),
                "harm_avoidance": round(self.harm_avoidance, 3),
            },
            # Section D2: Romantic
            "romantic": {
                "attraction_physical": round(self.attraction_physical, 3),
                "attraction_intellectual": round(self.attraction_intellectual, 3),
                "attraction_emotional": round(self.attraction_emotional, 3),
                "attraction_status": round(self.attraction_status, 3),
                "passion_intensity": round(self.passion_intensity, 3),
                "intimacy_depth": round(self.intimacy_depth, 3),
                "commitment_level": round(self.commitment_level, 3),
                "sexual_compatibility": round(self.sexual_compatibility, 3),
                "jealousy_triggers": self.jealousy_triggers,
                "forgiveness_capacity": round(self.forgiveness_capacity, 3),
                "infidelity_probability": round(self.infidelity_probability, 3),
                "libido": round(self.libido, 3),
            },
            # Section D3: Professional
            "professional": {
                "hierarchy_direction": self.hierarchy_direction,
                "power_asymmetry": round(self.power_asymmetry, 3),
                "collaboration_frequency": round(self.collaboration_frequency, 3),
                "competition_intensity": round(self.competition_intensity, 3),
                "networking_value": round(self.networking_value, 3),
                "information_asymmetry": round(self.information_asymmetry, 3),
                "workload_comparison": round(self.workload_comparison, 3),
            },
            # Section A: Biological Features (175 features)
            "biological_features": self.physiology.get_snapshot().get("biological_features", {}),
        }

    def __repr__(self):
        age_str = f"{self.age_years:.0f}yr"
        return (
            f"Agent({self.name}[{self.gender[0].upper()},{age_str},{self.personality}], "
            f"H:{self.hunger:.0f} E:{self.energy:.0f} "
            f"HA:{self.happiness:.0f} ${self.money:.0f})"
        )
