"""
Social Feature Registry — Sections D1, D2, D3
=============================================
Features 276-320 covering:
- D1: Kinship & Family (20 features)
- D2: Romantic & Sexual (25 features)
- D3: Professional & Economic (20 features)

Total: 65 social features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class SocialSystem(Enum):
    KINSHIP = auto()
    ROMANTIC = auto()
    PROFESSIONAL = auto()


@dataclass
class SocialFeature:
    feature_id: str
    feature_name: str
    system: SocialSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


SOCIAL_FEATURES: dict = {}


def _register_social_features():
    global SOCIAL_FEATURES
    
    features = [
        # ============ D1. KINSHIP & FAMILY (20 features) ============
        SocialFeature("kinship.genetic_relatedness", "Genetic Relatedness (r)", SocialSystem.KINSHIP,
                      (0, 1), "coefficient", "Parent-child 0.5, siblings 0.5, cousins 0.125",
                      "Genealogical analysis"),
        SocialFeature("kinship.lineage_depth", "Lineage Depth", SocialSystem.KINSHIP,
                      (0, 10), "generations", "Generations tracked",
                      "Family tree"),
        SocialFeature("kinship.inheritance_expectation", "Inheritance Expectation", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Anticipated share - drives sibling rivalry",
                      "Survey"),
        SocialFeature("kinship.caregiving_obligation", "Caregiving Obligation", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Cultural norms for parent support",
                      "Cultural assessment"),
        SocialFeature("kinship.rivalry_intensity", "Rivalry Intensity", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Resource competition among siblings",
                      "Sibling relationship inventory"),
        SocialFeature("kinship.alliance_history", "Alliance History", SocialSystem.KINSHIP,
                      (-1, 1), "scale", "Past cooperation/conflict with kin",
                      "Relationship history"),
        SocialFeature("kinship.estrangement_duration", "Estrangement Duration", SocialSystem.KINSHIP,
                      (0, 50), "years", "Time since contact - repair difficulty",
                      "Self-report"),
        SocialFeature("kinship.reconciliation_potential", "Reconciliation Potential", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Willingness to resume relationship",
                      "Motivation assessment"),
        SocialFeature("kinship.surrogate_parent", "Surrogate Parent Status", SocialSystem.KINSHIP,
                      (0, 1), "binary", "Aunt/uncle/grandparent as primary caregiver",
                      "Living arrangement"),
        SocialFeature("kinship.step_tension", "Step-Relation Tension", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Higher abuse risk from non-genetic parents",
                      "Family assessment"),
        SocialFeature("kinship.half_sibling_dynamics", "Half-Sibling Dynamics", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Shared parent but not both - alliance patterns",
                      "Relationship quality"),
        SocialFeature("kinship.adoptive_bond", "Adoptive Bond Strength", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Non-genetic attachment - often indistinguishable",
                      "Attachment assessment"),
        SocialFeature("kinship.foster_instability", "Foster Care Instability", SocialSystem.KINSHIP,
                      (0, 20), "placements", "Multiple placements - developmental impact",
                      "Case record"),
        SocialFeature("kinship.orphan_status", "Orphan Status", SocialSystem.KINSHIP,
                      (0, 2), "type", "Parental loss - institutional vs. kinship care",
                      "Living situation"),
        SocialFeature("kinship.family_size_effect", "Family Size Effect", SocialSystem.KINSHIP,
                      (1, 20), "children", "Resource dilution - larger families",
                      "Census"),
        SocialFeature("kinship.birth_order", "Birth Order Personality", SocialSystem.KINSHIP,
                      (1, 10), "position", "Firstborn conscientious, later born agreeable",
                      "Self-report"),
        SocialFeature("kinship.only_child_status", "Only Child Status", SocialSystem.KINSHIP,
                      (0, 1), "binary", "No sibling socialization",
                      "Family composition"),
        SocialFeature("kinship.twin_zygosity", "Twin Zygosity", SocialSystem.KINSHIP,
                      (0, 1), "binary", "Identical vs. fraternal",
                      "Genetic testing"),
        SocialFeature("kinship.incest_taboo", "Incest Taboo Strength", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Westermarck effect - childhood co-residence",
                      "Cultural norm"),
        SocialFeature("kinship.kin_selection", "Kin Selection Altruism", SocialSystem.KINSHIP,
                      (0, 1), "scale", "Helping genetic relatives - Hamilton's rule",
                      "Behavioral economics"),

        # ============ D2. ROMANTIC & SEXUAL (25 features) ============
        SocialFeature("romantic.attraction_physical", "Attraction Vector (Physical)", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Facial symmetry, waist-hip ratio, height, voice",
                      "Preference assessment"),
        SocialFeature("romantic.attraction_intellectual", "Attraction Vector (Intellectual)", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Shared interests, wit, conversational quality",
                      "Interview"),
        SocialFeature("romantic.attraction_emotional", "Attraction Vector (Emotional)", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Vulnerability sharing, emotional attunement, safety",
                      "Relationship assessment"),
        SocialFeature("romantic.attraction_status", "Attraction Vector (Status)", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Resource potential, social standing, ambition",
                      "Status perception"),
        SocialFeature("romantic.attachment_style_match", "Attachment Style Match", SocialSystem.ROMANTIC,
                      (-1, 1), "scale", "Secure-secure best; anxious-avoidant worst",
                      "ECR matching"),
        SocialFeature("romantic.passion_intensity", "Passion Intensity", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Lust and infatuation - typically declines 6-18 months",
                      "PAS"),
        SocialFeature("romantic.intimacy_depth", "Intimacy Depth", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Self-disclosure and closeness - builds over time",
                              "Intimacy scale"),
        SocialFeature("romantic.commitment_level", "Commitment Level", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Intention to persist - investment model",
                      "Investment scale"),
        SocialFeature("romantic.satisfaction_trajectory", "Satisfaction Trajectory", SocialSystem.ROMANTIC,
                      (-1, 1), "scale", "U-shaped over marriage - declines during child-rearing",
                      "Longitudinal assessment"),
        SocialFeature("romantic.alternative_monitoring", "Alternative Monitoring", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Awareness of other potential partners",
                      "Jealousy scale"),
        SocialFeature("romantic.investment_size", "Investment Size", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Resources put into relationship",
                      "Investment items"),
        SocialFeature("romantic.idealization_degree", "Idealization Degree", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Positive illusions about partner",
                      "Idealization scale"),
        SocialFeature("romantic.sexual_compatibility", "Sexual Compatibility", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Desire frequency match, preference alignment",
                      "Sexual satisfaction"),
        SocialFeature("romantic.jealousy_triggers", "Jealousy Triggers", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Emotional vs. sexual jealousy - sex differences",
                      "Jealousy type"),
        SocialFeature("romantic.betrayal_sensitivity", "Betrayal Sensitivity", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Threshold for feeling betrayed",
                      "Betrayal scale"),
        SocialFeature("romantic.forgiveness_capacity", "Forgiveness Capacity", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Ability to move past transgressions",
                      "TFS"),
        SocialFeature("romantic.breakup_grief", "Breakup Grief Intensity", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Proportional to investment and attachment",
                      "Grief assessment"),
        SocialFeature("romantic.replacement_latency", "Replacement Latency", SocialSystem.ROMANTIC,
                      (0, 24), "months", "Time to new relationship",
                      "Relationship history"),
        SocialFeature("romantic.mate_poaching", "Mate Poaching Attempts", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Pursuing already-partnered individuals",
                      "Behavioral report"),
        SocialFeature("romantic.infidelity_probability", "Infidelity Probability", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Opportunity + motivation + low detection",
                      "Sociosexual inventory"),
        SocialFeature("romantic.contraceptive_knowledge", "Contraceptive Knowledge", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Awareness of methods",
                      "Knowledge test"),
        SocialFeature("romantic.sexual_orientation", "Sexual Orientation Stability", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Fixed vs. fluid - developmental patterns",
                      "Self-identification"),
        SocialFeature("romantic.libido_variation", "Libido Variation", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Sex drive - hormonal, relational, contextual",
                      "Desire assessment"),
        SocialFeature("romantic.reproductive_coercion", "Reproductive Coercion", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Partner controlling fertility",
                      "Reproductive coercion scale"),
        SocialFeature("romantic.domestic_violence", "Domestic Violence Pattern", SocialSystem.ROMANTIC,
                      (0, 1), "scale", "Cycle of tension, incident, reconciliation, calm",
                      "Danger assessment"),

        # ============ D3. PROFESSIONAL & ECONOMIC (20 features) ============
        SocialFeature("professional.hierarchy_direction", "Hierarchy Direction", SocialSystem.PROFESSIONAL,
                      (-1, 1), "scale", "Reports to vs. supervised by - power asymmetry",
                      "Organizational chart"),
        SocialFeature("professional.power_asymmetry", "Power Asymmetry Magnitude", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Degree of authority difference",
                      "Position comparison"),
        SocialFeature("professional.dependency_ratio", "Dependency Ratio", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "How much one relies on the other for resources",
                      "Resource analysis"),
        SocialFeature("professional.expertise_complementarity", "Expertise Complementarity", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Skill overlap vs. distinctiveness",
                      "Skill mapping"),
        SocialFeature("professional.credit_allocation", "Credit Allocation Fairness", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Who gets recognized for joint work",
                      "Perception survey"),
        SocialFeature("professional.collaboration_frequency", "Collaboration Frequency", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "How often they work together",
                      "Interaction log"),
        SocialFeature("professional.competition_intensity", "Competition Intensity", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Zero-sum resources - can coexist with collaboration",
                      "Competition perception"),
        SocialFeature("professional.networking_value", "Networking Value", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Connections the other provides",
                      "Network analysis"),
        SocialFeature("professional.reference_potential", "Reference Potential", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Willingness to recommend",
                      "Willingness scale"),
        SocialFeature("professional.blackmail_vulnerability", "Blackmail Vulnerability", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Knowledge of secrets that could be weaponized",
                      "Risk assessment"),
        SocialFeature("professional.mentorship_quality", "Mentorship Quality", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Skill transfer, emotional support, sponsorship",
                      "Mentoring assessment"),
        SocialFeature("professional.sponsorship_activation", "Sponsorship Activation", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Using influence to advance protégé",
                      "Career outcome"),
        SocialFeature("professional.job_referral", "Job Referral Likelihood", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Informal hiring channel - homophily bias",
                      "Referral behavior"),
        SocialFeature("professional.information_asymmetry", "Information Asymmetry", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Who knows more about work situation",
                      "Knowledge test"),
        SocialFeature("professional.workload_comparison", "Workload Comparison", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Perceived fairness of distribution",
                      "Equity perception"),
        SocialFeature("professional.promotion_race", "Promotion Race", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Direct competition for advancement",
                      "Competition status"),
        SocialFeature("professional.union_solidarity", "Union Solidarity", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Collective action willingness",
                      "Solidarity scale"),
        SocialFeature("professional.whistleblower_protection", "Whistleblower Protection", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Willingness to report wrongdoing",
                      "Whistleblowing intention"),
        SocialFeature("professional.non_compete", "Non-Compete Enforcement", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Legal restriction on future employment",
                      "Contract review"),
        SocialFeature("professional.ip_dispute", "Intellectual Property Dispute", SocialSystem.PROFESSIONAL,
                      (0, 1), "scale", "Who owns ideas developed together",
                      "Conflict history"),
    ]
    
    for f in features:
        SOCIAL_FEATURES[f.feature_id] = f


_register_social_features()


def get_social_feature(feature_id: str) -> SocialFeature:
    return SOCIAL_FEATURES.get(feature_id)


def get_features_by_social_system(system: SocialSystem) -> list:
    return [f for f in SOCIAL_FEATURES.values() if f.system == system]


def get_all_social_feature_ids() -> list:
    return list(SOCIAL_FEATURES.keys())


def get_social_feature_count() -> int:
    return len(SOCIAL_FEATURES)