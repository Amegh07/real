"""
Psychological Feature Registry — Sections C1 & C2
================================================
Features 226-275 covering:
- C1: Emotional States & Regulation (25 features)
- C2: Personality & Individual Differences (25 features)

Total: 50 psychological features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class PsychologicalSystem(Enum):
    EMOTIONAL_STATES = auto()
    PERSONALITY = auto()


@dataclass
class PsychologicalFeature:
    feature_id: str
    feature_name: str
    system: PsychologicalSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


PSYCHOLOGICAL_FEATURES: dict = {}


def _register_psychological_features():
    global PSYCHOLOGICAL_FEATURES
    
    features = [
        # ============ C1. EMOTIONAL STATES & REGULATION (25 features) ============
        PsychologicalFeature("emotion.affect_valence", "Core Affect Valence", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Pleasant vs. unpleasant - continuous dimension",
                              "SAM or PANAS"),
        PsychologicalFeature("emotion.affect_arousal", "Core Affect Arousal", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Activated vs. deactivated - orthogonal to valence",
                              "SAM or PANAS"),
        PsychologicalFeature("emotion.affect_dominance", "Core Affect Dominance", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "In control vs. overwhelmed - third dimension",
                              "SAM"),
        PsychologicalFeature("emotion.emotional_granularity", "Emotional Granularity", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Ability to distinguish similar emotions",
                              "Trait meta-emotion plan"),
        PsychologicalFeature("emotion.reappraisal_frequency", "Reappraisal Frequency", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 100), "%", "Cognitive reinterpretation - most effective strategy",
                              "ERQ reappraisal"),
        PsychologicalFeature("emotion.suppression_tendency", "Suppression Tendency", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 100), "%", "Inhibiting emotional expression",
                              "ERQ suppression"),
        PsychologicalFeature("emotion.rumination_depth", "Rumination Depth", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Repetitive negative thought - predicts depression",
                              "RRS"),
        PsychologicalFeature("emotion.acceptance_capacity", "Acceptance Capacity", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Allowing emotions without judgment",
                              "AAQ"),
        PsychologicalFeature("emotion.distraction_efficacy", "Distraction Efficacy", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Shifting attention away from emotions",
                              "Experimental paradigm"),
        PsychologicalFeature("emotion.social_sharing", "Social Sharing Intensity", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 100), "%", "Talking about emotions",
                              "Diary study"),
        PsychologicalFeature("emotion.experiential_avoidance", "Experiential Avoidance", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Efforts to escape private experiences",
                              "AAQ-II"),
        PsychologicalFeature("emotion.behavioral_activation", "Behavioral Activation", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Engagement with rewarding activities",
                              "BADS"),
        PsychologicalFeature("emotion.anhedonia_severity", "Anhedonia Severity", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Inability to feel pleasure - core depression symptom",
                              "SHAPS"),
        PsychologicalFeature("emotion.psychomotor_retardation", "Psychomotor Retardation", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Slowed movement and thought - melancholic feature",
                              "Clinical rating"),
        PsychologicalFeature("emotion.diurnal_mood", "Diurnal Mood Variation", PsychologicalSystem.EMOTIONAL_STATES,
                              (-1, 1), "scale", "Worse morning (melancholic) vs. evening (atypical)",
                              "Mood diary"),
        PsychologicalFeature("emotion.mixed_features", "Mixed Features", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Simultaneous depression and mania symptoms",
                              "DSM criteria"),
        PsychologicalFeature("emotion.seasonal_pattern", "Seasonal Pattern", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Winter depression (SAD) vs. summer",
                              "Seasonal pattern inventory"),
        PsychologicalFeature("emotion.peripartum_onset", "Peripartum Onset", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "binary", "Depression/anxiety during pregnancy or postpartum",
                              "EPDS"),
        PsychologicalFeature("emotion.catatonia_signs", "Catatonia Signs", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 12), "score", "Motor immobility, waxy flexibility - medical emergency",
                              "Bush-Francis scale"),
        PsychologicalFeature("emotion.emotional_blunting", "Emotional Blunting", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Reduced emotional range - SSRI side effect",
                              "BIS"),
        PsychologicalFeature("emotion.alexithymia", "Alexithymia", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Inability to identify and describe emotions",
                              "TAS-20"),
        PsychologicalFeature("emotion.emotional_contagion", "Emotional Contagion Susceptibility", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Catching others' emotions",
                              "Emotional contagion scale"),
        PsychologicalFeature("emotion.mood_congruent_memory", "Mood Congruent Memory", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "r", "Sad mood recalls sad memories",
                              "Memory paradigm"),
        PsychologicalFeature("emotion.affective_forecasting", "Affective Forecasting Error", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 100), "%", "Predicting future emotions poorly",
                              "Forecast vs. experience"),
        PsychologicalFeature("emotion.hedonic_adaptation", "Hedonic Adaptation Rate", PsychologicalSystem.EMOTIONAL_STATES,
                              (0, 1), "scale", "Return to baseline after events",
                              "Adaptation tracking"),

        # ============ C2. PERSONALITY & INDIVIDUAL DIFFERENCES (25 features) ============
        PsychologicalFeature("personality.openness", "Openness to Experience", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Fantasy, aesthetics, feelings, actions, ideas, values",
                              "NEO-PI-R"),
        PsychologicalFeature("personality.conscientiousness", "Conscientiousness", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Competence, order, dutifulness, achievement, self-discipline",
                              "NEO-PI-R"),
        PsychologicalFeature("personality.extraversion", "Extraversion", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Warmth, gregariousness, assertiveness, activity, excitement",
                              "NEO-PI-R"),
        PsychologicalFeature("personality.agreeableness", "Agreeableness", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Trust, straightforwardness, altruism, compliance, modesty",
                              "NEO-PI-R"),
        PsychologicalFeature("personality.neuroticism", "Neuroticism", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Anxiety, angry hostility, depression, self-consciousness",
                              "NEO-PI-R"),
        PsychologicalFeature("personality.machiavellianism", "Machiavellianism", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Strategic manipulation, cynical worldview, moral flexibility",
                              "MACH-IV"),
        PsychologicalFeature("personality.narcissism_grandiose", "Narcissism (Grandiose)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Dominance, entitlement, exhibitionism; fragile underneath",
                              "NPI"),
        PsychologicalFeature("personality.narcissism_vulnerable", "Narcissism (Vulnerable)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Hypersensitivity, defensiveness, covert entitlement",
                              "PNI"),
        PsychologicalFeature("personality.psychopathy_primary", "Primary Psychopathy", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Callousness, lack of empathy, predatory; low anxiety",
                              "PCL-R"),
        PsychologicalFeature("personality.psychopathy_secondary", "Secondary Psychopathy", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Impulsivity, reactive aggression; high anxiety",
                              "PCL-R"),
        PsychologicalFeature("personality.honesty_humility", "Honesty-Humility (HEXACO)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Sincere, fair, greed avoidance, modesty",
                              "HEXACO-PI"),
        PsychologicalFeature("personality.attachment_anxiety", "Attachment Anxiety", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Fear of abandonment; hyperactivating strategies",
                              "ECR"),
        PsychologicalFeature("personality.attachment_avoidance", "Attachment Avoidance", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Fear of intimacy; deactivating strategies",
                              "ECR"),
        PsychologicalFeature("personality.behavioral_inhibition", "Behavioral Inhibition (BIS)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Sensitivity to punishment and novelty",
                              "BIS/BAS scales"),
        PsychologicalFeature("personality.behavioral_activation", "Behavioral Activation (BAS)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Sensitivity to reward",
                              "BIS/BAS scales"),
        PsychologicalFeature("personality.sensation_seeking", "Sensation Seeking", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Thrill, experience seeking, disinhibition, boredom",
                              "SSS"),
        PsychologicalFeature("personality.harm_avoidance", "Harm Avoidance", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Anticipatory worry, fear of uncertainty, shyness",
                              "TPQ"),
        PsychologicalFeature("personality.novelty_seeking", "Novelty Seeking", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Exploratory excitability, impulsiveness, extravagance",
                              "TPQ"),
        PsychologicalFeature("personality.reward_dependence", "Reward Dependence", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Sentimentality, persistence, attachment, dependence",
                              "TPQ"),
        PsychologicalFeature("personality.self_directedness", "Self-Directedness", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Responsibility, purposefulness, resourcefulness",
                              "TCI"),
        PsychologicalFeature("personality.cooperativeness", "Cooperativeness", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Social acceptance, empathy, helpfulness, compassion",
                              "TCI"),
        PsychologicalFeature("personality.self_transcendence", "Self-Transcendence", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Self-forgetfulness, transpersonal identification",
                              "TCI"),
        PsychologicalFeature("personality.perfectionism_self", "Perfectionism (Self-Oriented)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "High personal standards; adaptive or maladaptive",
                              "MPS"),
        PsychologicalFeature("personality.perfectionism_social", "Perfectionism (Socially Prescribed)", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Belief others demand perfection - linked to depression",
                              "MPS"),
        PsychologicalFeature("personality.locus_control", "Locus of Control", PsychologicalSystem.PERSONALITY,
                              (0, 1), "scale", "Internal vs. external attribution of life outcomes",
                              "I-E scale"),
    ]
    
    for f in features:
        PSYCHOLOGICAL_FEATURES[f.feature_id] = f


_register_psychological_features()


def get_psychological_feature(feature_id: str) -> PsychologicalFeature:
    return PSYCHOLOGICAL_FEATURES.get(feature_id)


def get_features_by_psychological_system(system: PsychologicalSystem) -> list:
    return [f for f in PSYCHOLOGICAL_FEATURES.values() if f.system == system]


def get_all_psychological_feature_ids() -> list:
    return list(PSYCHOLOGICAL_FEATURES.keys())


def get_psychological_feature_count() -> int:
    return len(PSYCHOLOGICAL_FEATURES)