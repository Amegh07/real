"""
Political System - F1 State Formation & Legitimacy, F2 Democratic Mechanics, F3 International Relations
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class LegitimacySource(Enum):
    TRADITIONAL = "traditional"
    CHARISMATIC = "charismatic"
    LEGAL_RATIONAL = "legal_rational"
    PERFORMANCE = "performance"
    DIVINE = "divine"


class PoliticalStability(Enum):
    STABLE = "stable"
    UNSTABLE = "unstable"
    CRISIS = "crisis"
    CIVIL_WAR = "civil_war"


class ElectoralSystem(Enum):
    FPTP = "first_past_the_post"
    PROPORTIONAL = "proportional"
    MIXED = "mixed"


@dataclass
class StateFormation:
    monopoly_on_violence: bool = True
    territorial_control: float = 1.0
    tax_extraction_efficiency: float = 0.5
    bureaucratic_quality: float = 0.5
    rule_of_law: float = 0.5
    corruption_perceptions: float = 0.3
    regulatory_quality: float = 0.5
    government_effectiveness: float = 0.5
    political_stability: PoliticalStability = PoliticalStability.STABLE
    legitimacy_source: LegitimacySource = LegitimacySource.LEGAL_RATIONAL
    performance_legitimacy: float = 0.5
    nationalist_narrative: float = 0.5
    social_contract_fairness: float = 0.5
    consent_of_governed: float = 0.5
    revolutionary_potential: float = 0.0
    coup_proofing: float = 0.3
    clientelism_density: float = 0.3

    def tick(self, stress: float = 0.0):
        if stress > 0.7:
            self.political_stability = PoliticalStability.CRISIS
        elif stress > 0.4:
            self.political_stability = PoliticalStability.UNSTABLE
        else:
            self.political_stability = PoliticalStability.STABLE

        self.revolutionary_potential = min(1.0, self.revolutionary_potential + stress * 0.1)
        
        self.performance_legitimacy = max(0.0, min(1.0, 
            self.performance_legitimacy - stress * 0.05 + (1 - stress) * 0.02))
        
        self.consent_of_governed = max(0.0, min(1.0,
            self.consent_of_governed - stress * 0.03 + (1 - stress) * 0.01))

    def get_stability_score(self) -> float:
        base = 1.0
        base -= self.corruption_perceptions * 0.3
        base -= self.revolutionary_potential * 0.4
        base += self.bureaucratic_quality * 0.2
        base += self.government_effectiveness * 0.2
        return max(0.0, min(1.0, base))


@dataclass
class DemocraticMechanics:
    electoral_system: ElectoralSystem = ElectoralSystem.FPTP
    gerrymandering_level: float = 0.0
    voter_suppression: bool = False
    campaign_finance_restricted: bool = True
    pac_influence: float = 0.2
    lobbying_expenditure: float = 100000.0
    astroturfing_detected: bool = False
    primary_extremism: float = 0.3
    coalition_formed: bool = False
    gridlock: bool = False
    impeachment_process: bool = False
    judicial_review_power: float = 0.5
    federalism_degree: float = 0.5
    devolution_present: bool = False
    direct_democracy: bool = False
    civic_education: float = 0.6
    polarization_index: float = 0.3
    negative_partisanship: float = 0.2
    populist_appeal: float = 0.0
    authoritarian_backsliding_risk: float = 0.0

    def tick(self, external_stress: float = 0.0):
        self.polarization_index = min(1.0, self.polarization_index + external_stress * 0.05)
        self.negative_partisanship = min(1.0, self.negative_partisanship + external_stress * 0.03)
        
        if self.polarization_index > 0.7:
            self.gridlock = True
            self.primary_extremism = min(1.0, self.primary_extremism + 0.02)
        
        if self.populist_appeal > 0.6:
            self.authoritarian_backsliding_risk = min(1.0, 
                self.authoritarian_backsliding_risk + external_stress * 0.1)

    def get_democracy_score(self) -> float:
        score = 1.0
        score -= self.gerrymandering_level * 0.15
        score -= self.voter_suppression * 0.2
        score -= self.gridlock * 0.1
        score -= self.polarization_index * 0.2
        score -= self.authoritarian_backsliding_risk * 0.3
        score += self.civic_education * 0.1
        score += self.judicial_review_power * 0.05
        return max(0.0, min(1.0, score))


@dataclass
class InternationalRelations:
    balance_of_power_score: float = 0.5
    hegemon_present: bool = False
    hegemon_name: Optional[str] = None
    security_dilemma_active: bool = False
    deterrence_credibility: float = 0.7
    extended_deterrence_active: bool = False
    alliance_obligations: List[str] = field(default_factory=list)
    bandwagoning: bool = False
    free_rider_level: float = 0.2
    sanctions_effective: bool = False
    smart_sanctions_used: bool = True
    humanitarian_intervention: bool = False
    peacekeeping_deployed: bool = False
    arms_control_active: bool = True
    npt_compliant: bool = True
    diplomatic_recognition: List[str] = field(default_factory=list)
    extraterritorial_jurisdiction: bool = False
    icj_compliant: bool = True
    refugee_status_processing: float = 0.5
    asylum_backlog: int = 0
    remittance_flow: float = 0.0

    def tick(self, crisis_level: float = 0.0):
        if crisis_level > 0.5:
            self.security_dilemma_active = True
            self.balance_of_power_score = abs(self.balance_of_power_score - 0.5) + 0.3

        if self.free_rider_level > 0.5:
            alliance_satisfaction = 1.0 - self.free_rider_level
            if alliance_satisfaction < 0.3:
                self.alliance_obligations = [a for a in self.alliance_obligations if random.random() > 0.1]

        self.refugee_status_processing = max(0.1, min(1.0,
            self.refugee_status_processing - crisis_level * 0.05))
        self.asylum_backlog = int(self.asylum_backlog * 1.1 + crisis_level * 1000)

    def get_alliance_strength(self) -> float:
        if not self.alliance_obligations:
            return 0.0
        base = len(self.alliance_obligations) / 10.0
        base -= self.free_rider_level * 0.5
        base += self.deterrence_credibility * 0.3
        return max(0.0, min(1.0, base))


class PoliticalSystem:
    def __init__(self):
        self.state = StateFormation()
        self.democracy = DemocraticMechanics()
        self.international = InternationalRelations()
        self.treasury: float = 1000000.0
        self.public_goods: Dict[str, float] = {
            "defense": 0.5,
            "infrastructure": 0.5,
            "education": 0.5,
            "healthcare": 0.5,
            "justice": 0.5
        }

    def tick(self, economy_stress: float = 0.0, social_stress: float = 0.0):
        combined_stress = (economy_stress + social_stress) / 2.0
        
        self.state.tick(combined_stress)
        self.democracy.tick(combined_stress)
        self.international.tick(combined_stress)
        
        self._update_treasury()
        self._provide_public_goods(combined_stress)

    def _update_treasury(self):
        tax_revenue = self.state.tax_extraction_efficiency * 10000.0
        self.treasury += tax_revenue

    def _provide_public_goods(self, stress: float):
        for good in self.public_goods:
            effectiveness = self.state.government_effectiveness * (1 - stress)
            self.public_goods[good] = max(0.0, min(1.0, effectiveness))

    def get_governance_score(self) -> float:
        state_score = self.state.get_stability_score()
        democracy_score = self.democracy.get_democracy_score()
        intl_score = self.international.get_alliance_strength()
        
        return (state_score * 0.5) + (democracy_score * 0.3) + (intl_score * 0.2)

    def apply_policy(self, policy_type: str, intensity: float) -> Dict:
        results = {"implemented": True, "effects": {}}
        
        if policy_type == "anticorruption":
            self.state.corruption_perceptions = max(0.0, 
                self.state.corruption_perceptions - intensity * 0.2)
            results["effects"]["corruption"] = -intensity * 20
        
        elif policy_type == "education":
            self.democracy.civic_education = min(1.0, 
                self.democracy.civic_education + intensity * 0.1)
            results["effects"]["civic_knowledge"] = intensity * 10
        
        elif policy_type == "centralization":
            self.democracy.federalism_degree = max(0.0,
                self.democracy.federalism_degree - intensity * 0.2)
            results["effects"]["central_power"] = intensity * 20
        
        elif policy_type == "devolution":
            self.democracy.devolution_present = True
            self.democracy.federalism_degree = min(1.0,
                self.democracy.federalism_degree + intensity * 0.2)
            results["effects"]["regional_power"] = intensity * 20
        
        elif policy_type == "austerity":
            for good in self.public_goods:
                self.public_goods[good] = max(0.0, 
                    self.public_goods[good] - intensity * 0.1)
            results["effects"]["services"] = -intensity * 10
        
        elif policy_type == "stimulus":
            for good in self.public_goods:
                self.public_goods[good] = min(1.0,
                    self.public_goods[good] + intensity * 0.15)
            results["effects"]["services"] = intensity * 15
        
        return results