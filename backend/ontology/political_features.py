"""
Political Feature Registry — Sections F1, F2, F3
================================================
Features 401-460 covering:
- F1: State Formation & Legitimacy (20 features)
- F2: Democratic Mechanics (20 features)
- F3: International Relations (20 features)

Total: 60 political features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class PoliticalSystem(Enum):
    STATE_FORMATION = auto()
    DEMOCRATIC_MECHANICS = auto()
    INTERNATIONAL_RELATIONS = auto()


@dataclass
class PoliticalFeature:
    feature_id: str
    feature_name: str
    system: PoliticalSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


POLITICAL_FEATURES: dict = {}


def _register_political_features():
    global POLITICAL_FEATURES
    
    features = [
        # ============ F1. STATE FORMATION & LEGITIMACY (20 features) ============
        PoliticalFeature("pol.monopoly_violence", "Monopoly on Violence", PoliticalSystem.STATE_FORMATION,
                         (0, 100), "%", "Weber's definition - contested in failed states",
                         "Conflict assessment"),
        PoliticalFeature("pol.territorial_control", "Territorial Control Percentage", PoliticalSystem.STATE_FORMATION,
                         (0, 100), "%", "Government vs. rebel/terrorist control",
                         "Control mapping"),
        PoliticalFeature("pol.tax_efficiency", "Tax Extraction Efficiency", PoliticalSystem.STATE_FORMATION,
                         (0, 100), "%", "Actual vs. potential revenue - fiscal capacity",
                         "Revenue data"),
        PoliticalFeature("pol.bureaucratic_quality", "Bureaucratic Quality", PoliticalSystem.STATE_FORMATION,
                         (0, 100), "%", "Meritocracy vs. patronage - predicts development",
                         "Governance index"),
        PoliticalFeature("pol.rule_of_law", "Rule of Law Index", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "score", "Contract enforcement, property rights, judicial independence",
                         "WGI"),
        PoliticalFeature("pol.corruption_perception", "Corruption Perceptions", PoliticalSystem.STATE_FORMATION,
                         (0, 100), "score", "Transparency International - self-fulfilling",
                         "TI index"),
        PoliticalFeature("pol.regulatory_quality", "Regulatory Quality", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "score", "Market-friendly regulation - not captured by incumbents",
                         "WGI"),
        PoliticalFeature("pol.gov_effectiveness", "Government Effectiveness", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "score", "Policy implementation quality - not just intention",
                         "WGI"),
        PoliticalFeature("pol.political_stability", "Political Stability", PoliticalSystem.STATE_FORMATION,
                         (-3, 3), "score", "No violence or unconstitutional change",
                         "WGI"),
        PoliticalFeature("pol.voice_accountability", "Voice and Accountability", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "score", "Democratic participation - human rights protection",
                         "WGI"),
        PoliticalFeature("pol.legitimacy_source", "Legitimacy Source", PoliticalSystem.STATE_FORMATION,
                         (0, 3), "type", "Traditional, charismatic, legal-rational (Weber)",
                         "Political analysis"),
        PoliticalFeature("pol.performance_legitimacy", "Performance Legitimacy", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Economic growth buys compliance - China model",
                         "Growth and compliance"),
        PoliticalFeature("pol.nationalist_narrative", "Nationalist Narrative Strength", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Shared identity - external threat amplifies",
                         "Narrative analysis"),
        PoliticalFeature("pol.divine_right", "Divine Right Claims", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "binary", "Religious sanction - monarchies and theocracies",
                         "Political tradition"),
        PoliticalFeature("pol.mandate_of_heaven", "Mandate of Heaven", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Chinese cyclical legitimacy - disasters as withdrawal",
                         "Historical analysis"),
        PoliticalFeature("pol.social_contract", "Social Contract Perception", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Citizens' view of fairness",
                         "Public opinion"),
        PoliticalFeature("pol.consent_governed", "Consent of the Governed", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Election turnout and satisfaction",
                         "Electoral data"),
        PoliticalFeature("pol.revolutionary_potential", "Revolutionary Potential", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Relative deprivation + mobilization + opportunity",
                         "Risk assessment"),
        PoliticalFeature("pol.coup_proofing", "Coup-Proofing Investment", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Parallel military structures - reduces coup risk",
                         "Military structure"),
        PoliticalFeature("pol.clientelism", "Clientelism Network Density", PoliticalSystem.STATE_FORMATION,
                         (0, 1), "scale", "Patronage distribution - vote buying and loyalty",
                         "Network analysis"),

        # ============ F2. DEMOCRATIC MECHANICS (20 features) ============
        PoliticalFeature("pol.electoral_system", "Electoral System Type", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 3), "type", "FPTP, proportional, mixed - shapes party system",
                         "Electoral law"),
        PoliticalFeature("pol.gerrymandering", "District Gerrymandering", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Boundary manipulation - efficiency gap measure",
                         "Redistricting analysis"),
        PoliticalFeature("pol.voter_suppression", "Voter Suppression Tactics", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "ID laws, polling place reduction, felon disenfranchisement",
                         "Voting rights"),
        PoliticalFeature("pol.campaign_finance", "Campaign Finance Rules", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Contribution limits - Citizens United effect",
                         "Finance law"),
        PoliticalFeature("pol.pac_activity", "Political Action Committee (PAC)", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 100000000), "money", "Money aggregation - super PAC unlimited",
                         "Donor tracking"),
        PoliticalFeature("pol.lobbying_expenditure", "Lobbying Expenditure", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 10000000000), "money", "Industry influence - revolving door effect",
                         "Lobbyist disclosure"),
        PoliticalFeature("pol.astroturfing", "Astroturfing", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Fake grassroots movement - corporate or state funded",
                         "Social media analysis"),
        PoliticalFeature("pol.primary_dynamics", "Primary Election Dynamics", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Base vs. general electorate - extremism incentive",
                         "Primary results"),
        PoliticalFeature("pol.coalition_formation", "Coalition Government Formation", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Multi-party bargaining - policy compromise",
                         "Government formation"),
        PoliticalFeature("pol.hung_parliament", "Hung Parliament/Gridlock", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "binary", "No majority - policy stagnation or crisis response",
                         "Election result"),
        PoliticalFeature("pol.impeachment_process", "Impeachment Process", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Political, not criminal - partisan threshold",
                         "Constitutional"),
        PoliticalFeature("pol.judicial_review", "Judicial Review Power", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Courts overturn legislation - Marbury v. Madison",
                         "Constitutional"),
        PoliticalFeature("pol.federalism", "Federalism Degree", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Central vs. state power - policy experimentation",
                         "Constitutional"),
        PoliticalFeature("pol.devolution", "Devolution", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Power transfer to regions - Scotland, Catalonia",
                         "Devolution acts"),
        PoliticalFeature("pol.direct_democracy", "Direct Democracy Tools", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Referendum, initiative, recall",
                         "Ballot measures"),
        PoliticalFeature("pol.civic_education", "Civic Education Level", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Political knowledge - affects democratic quality",
                         "Knowledge survey"),
        PoliticalFeature("pol.polarization_index", "Polarization Index", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Distance between party medians - affective vs. ideological",
                         "Voter survey"),
        PoliticalFeature("pol.negative_partisanship", "Negative Partisanship", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Hating other side more than liking own - primary driver",
                         "Partisan affect"),
        PoliticalFeature("pol.populist_appeal", "Populist Appeal", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Pure people vs. corrupt elite - charismatic leader",
                         "Rhetoric analysis"),
        PoliticalFeature("pol.authoritarian_reversion", "Authoritarian Reversion Risk", PoliticalSystem.DEMOCRATIC_MECHANICS,
                         (0, 1), "scale", "Democratic backsliding - Hungary, Turkey examples",
                         "Democracy index"),

        # ============ F3. INTERNATIONAL RELATIONS (20 features) ============
        PoliticalFeature("ir.balance_power", "Balance of Power", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "No single dominant state - alliance formation",
                         "Power distribution"),
        PoliticalFeature("ir.hegemonic_stability", "Hegemonic Stability", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Single power provides public goods - British then American",
                         "Hegemon status"),
        PoliticalFeature("ir.security_dilemma", "Security Dilemma", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Defensive buildup seen as threat - arms race spiral",
                         "Threat perception"),
        PoliticalFeature("ir.deterrence_credibility", "Deterrence Credibility", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Threat must be believable - commitment problem",
                         "Alliance analysis"),
        PoliticalFeature("ir.extended_deterrence", "Extended Deterrence", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Protecting allies - nuclear umbrella",
                         "Security guarantee"),
        PoliticalFeature("ir.alliance_treaty", "Alliance Treaty Obligation", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "NATO Article 5 - collective defense",
                         "Treaty text"),
        PoliticalFeature("ir.bandwagoning", "Bandwagoning vs. Balancing", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (-1, 1), "scale", "Joining strong side vs. opposing - threat level decides",
                         "Strategy choice"),
        PoliticalFeature("ir.free_rider", "Free-Rider Problem", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Alliance members under-contribute - burden-sharing",
                         "Defense spending"),
        PoliticalFeature("ir.sanctions_efficacy", "Economic Sanctions Efficacy", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Coercion through trade restriction - rarely work alone",
                         "Outcome analysis"),
        PoliticalFeature("ir.smart_sanctions", "Smart Sanctions", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Targeted on leaders vs. comprehensive - humanitarian",
                         "Sanction type"),
        PoliticalFeature("ir.humanitarian_intervention", "Humanitarian Intervention", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "R2P doctrine - Libya vs. Syria divergence",
                         "Intervention record"),
        PoliticalFeature("ir.peacekeeping", "Peacekeeping Mission", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Blue helmets - consent of parties required",
                         "Mission status"),
        PoliticalFeature("ir.arms_control", "Arms Control Treaty", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Verification challenges - cheating incentives",
                         "Treaty compliance"),
        PoliticalFeature("ir.nuclear_proliferation", "Nuclear Non-Proliferation", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "NPT bargain - recognized vs. non-recognized weapons",
                         "Nuclear status"),
        PoliticalFeature("ir.diplomatic_recognition", "Diplomatic Recognition", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Statehood criteria - Montevideo Convention",
                         "Recognition count"),
        PoliticalFeature("ir.extraterritorial_jurisdiction", "Extraterritorial Jurisdiction", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "Laws applied abroad - US sanctions example",
                         "Legal scope"),
        PoliticalFeature("ir.icj_compliance", "International Court Compliance", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "ICJ rulings - enforcement absent",
                         "Compliance record"),
        PoliticalFeature("ir.refugee_status", "Refugee Status Determination", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1), "scale", "1951 Convention criteria - persecution vs. economic",
                         "Asylum decision"),
        PoliticalFeature("ir.asylum_backlog", "Asylum Processing Backlog", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 1000000), "cases", "Years-long waits - mental health deterioration",
                         "Case inventory"),
        PoliticalFeature("ir.remittance_corridor", "Remittance Corridor", PoliticalSystem.INTERNATIONAL_RELATIONS,
                         (0, 100000000000), "value", "Money transfer routes - fees and regulatory barriers",
                         "Flow tracking"),
    ]
    
    for f in features:
        POLITICAL_FEATURES[f.feature_id] = f


_register_political_features()


def get_political_feature(feature_id: str) -> PoliticalFeature:
    return POLITICAL_FEATURES.get(feature_id)


def get_features_by_political_system(system: PoliticalSystem) -> list:
    return [f for f in POLITICAL_FEATURES.values() if f.system == system]


def get_all_political_feature_ids() -> list:
    return list(POLITICAL_FEATURES.keys())


def get_political_feature_count() -> int:
    return len(POLITICAL_FEATURES)