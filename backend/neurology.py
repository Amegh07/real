"""
Neurological Systems — God-Tier Architecture
========================================
Section B1: Brain Structure & Function (20 features: 176-195)

Features:
176. Cortical Thickness — Gray matter measure; declines with age, faster in dementia
177. Hippocampal Volume — Memory formation; PTSD and depression cause atrophy
178. Amygdala Reactivity — Threat detection; hyperactive in anxiety disorders
179. Prefrontal Cortex Maturation — Last brain region to mature (age 25)
180. White Matter Integrity (FA) — Fractional anisotropy from DTI
181. Myelination Status — Saltatory conduction speed
182. Synaptic Density — Connections per neuron; highest in childhood
183. Neurotransmitter Turnover — 5-HIAA, HVA, MHPG in CSF
184. Blood-Brain Barrier Permeability — Tight junction integrity
185. Cerebral Blood Flow Autoregulation — Constant perfusion despite pressure changes
186. Glymphatic Clearance Rate — Waste removal during sleep
187. Brain-Derived Neurotrophic Factor (BDNF) — Neuroplasticity promoter
188. Default Mode Network Connectivity — Resting-state network
189. Salience Network Switching — Internal/external attention toggle
190. Central Executive Network Load — Working memory and goal maintenance
191. Cerebellar Function — Motor coordination and cognitive timing
192. Brainstem Vital Functions — Respiratory and cardiac centers
193. Thalamic Gating — Sensory relay filtering
194. Hypothalamic Integration — Homeostatic hub
195. Pineal Gland Calcification — Melatonin production decline

Based on spec Section B1: Neurological & Cognitive Systems
"""

import uuid
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class BrainRegion(Enum):
    """Major brain regions for tracking."""
    PREFRONTAL_CORTEX = auto()
    HIPPOCAMPUS = auto()
    AMYGDALA = auto()
    TEMPORAL_LOBES = auto()
    PARIETAL_LOBES = auto()
    OCCIPITAL_LOBES = auto()
    CEREBELLUM = auto()
    BRAINSTEM = auto()
    THALAMUS = auto()
    HYPOTHALAMUS = auto()
    PINAL_GLAND = auto()


@dataclass
class CorticalStructure:
    """
    Cortical Thickness and Gray Matter (Feature 176).
    Declines with age, faster in dementia.
    """
    thickness_mm: float = 2.5  # millimeters (normal adult cortex)
    gray_matter_volume_ml: float = 600.0
    sulcal_depth: float = 0.8  # 0-1 fold complexity
    cortical_surface_area_cm2: float = 2000.0
    
    def age_decline(self, age_years: float, stress_level: float = 0.0):
        """Apply age-related decline."""
        base_rate = 0.0002 * (age_years - 30) / 10 if age_years > 30 else 0
        stress_multiplier = 1.0 + stress_level * 0.5
        
        self.thickness_mm = max(1.5, self.thickness_mm - base_rate * stress_multiplier)
        self.gray_matter_volume_ml = max(400, self.gray_matter_volume_ml - base_rate * 100 * stress_multiplier)
    
    def get_snapshot(self) -> dict:
        return {
            "thickness_mm": round(self.thickness_mm, 2),
            "gray_matter_volume_ml": round(self.gray_matter_volume_ml, 1),
            "sulcal_depth": round(self.sulcal_depth, 2),
            "surface_area_cm2": round(self.cortical_surface_area_cm2, 0)
        }


@dataclass
class Hippocampus:
    """
    Hippocampal Volume (Feature 177).
    Memory formation; PTSD and depression cause atrophy.
    """
    volume_ml: float = 4.0  # bilateral
    ca1_neurons: float = 1.0  # relative health
    dentate_granule_cells: float = 1.0
    neurogenesis_rate: float = 0.01  # new neurons per day
    
    def apply_stress(self, cortisol_level: float):
        """High cortisol damages hippocampus (PTSD/depression)."""
        if cortisol_level > 0.7:
            damage = (cortisol_level - 0.7) * 0.02
            self.volume_ml = max(2.5, self.volume_ml - damage)
            self.ca1_neurons = max(0.5, self.ca1_neurons - damage * 0.5)
    
    def apply_exercise(self, bdnf_level: float):
        """Exercise promotes neurogenesis via BDNF."""
        if bdnf_level > 0.6:
            self.volume_ml = min(4.5, self.volume_ml + self.neurogenesis_rate * bdnf_level)
            self.dentate_granule_cells = min(1.0, self.dentate_granule_cells + 0.001)
    
    def get_snapshot(self) -> dict:
        return {
            "volume_ml": round(self.volume_ml, 2),
            "ca1_health": round(self.ca1_neurons, 2),
            "dentate_health": round(self.dentate_granule_cells, 2)
        }


@dataclass
class Amygdala:
    """
    Amygdala Reactivity (Feature 178).
    Threat detection; hyperactive in anxiety disorders.
    """
    volume_ml: float = 1.5
    reactivity: float = 0.5  # 0-1 baseline
    threat_detection_sensitivity: float = 0.5
    fear_extinction_capacity: float = 0.7
    
    def apply_chronic_stress(self, stress_level: float):
        """Chronic stress increases amygdala reactivity."""
        if stress_level > 0.6:
            self.reactivity = min(1.0, self.reactivity + stress_level * 0.02)
            self.threat_detection_sensitivity = min(1.0, self.threat_detection_sensitivity + 0.01)
    
    def apply_extinction(self, successful: bool):
        """Fear extinction learning."""
        if successful:
            self.reactivity = max(0.3, self.reactivity - 0.05)
            self.fear_extinction_capacity = min(0.95, self.fear_extinction_capacity + 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "volume_ml": round(self.volume_ml, 2),
            "reactivity": round(self.reactivity, 2),
            "threat_sensitivity": round(self.threat_detection_sensitivity, 2),
            "fear_extinction": round(self.fear_extinction_capacity, 2)
        }


@dataclass
class PrefrontalCortex:
    """
    Prefrontal Cortex Maturation (Feature 179).
    Last brain region to mature (age 25); explains adolescent impulsivity.
    """
    maturity: float = 0.5  # 0-1 (full maturation at 25)
    dlpfc_efficiency: float = 0.8  # Dorsolateral PFC
    vmpfc_efficiency: float = 0.7  # Ventromedial PFC
    orbitofrontal_efficiency: float = 0.75
    
    def age_maturation(self, age_years: float):
        """Maturation completes around age 25."""
        if age_years < 25:
            self.maturity = min(1.0, age_years / 25)
            self.dlpfc_efficiency = min(1.0, 0.3 + age_years / 30)
            self.vmpfc_efficiency = min(1.0, 0.2 + age_years / 35)
        else:
            self.maturity = min(1.0, 1.0 - (age_years - 25) * 0.001)  # Very slow decline
            self.dlpfc_efficiency = max(0.5, self.dlpfc_efficiency - 0.0001)
    
    def get_snapshot(self) -> dict:
        return {
            "maturity": round(self.maturity, 2),
            "dlpfc_efficiency": round(self.dlpfc_efficiency, 2),
            "vmpfc_efficiency": round(self.vmpfc_efficiency, 2),
            "ofc_efficiency": round(self.orbitofrontal_efficiency, 2)
        }


@dataclass
class WhiteMatterTracts:
    """
    White Matter Integrity (Feature 180).
    Fractional anisotropy from DTI; declines with hypertension.
    """
    fractional_anisotropy: float = 0.75  # FA 0-1
    myelin_integrity: float = 0.9
    conduction_speed_factor: float = 1.0
    
    def apply_hypertension(self, bp_systolic: float, duration: float):
        """High BP damages white matter."""
        if bp_systolic > 140:
            years_exposed = duration / 365
            damage = (bp_systolic - 140) / 100 * years_exposed * 0.01
            self.fractional_anisotropy = max(0.4, self.fractional_anisotropy - damage)
            self.myelin_integrity = max(0.5, self.myelin_integrity - damage)
    
    def get_snapshot(self) -> dict:
        return {
            "fractional_anisotropy": round(self.fractional_anisotropy, 2),
            "myelin_integrity": round(self.myelin_integrity, 2),
            "conduction_speed": round(self.conduction_speed_factor, 2)
        }


@dataclass
class MyelinSheath:
    """
    Myelination Status (Feature 181).
    Saltatory conduction speed; multiple sclerosis causes demyelination.
    """
    thickness_ratio: float = 1.0  # relative to normal
    node_length: float = 1.0  # mm
    conduction_velocity_mps: float = 50.0  # m/s
    
    def apply_demyelination(self, autoimmune_activity: float):
        """MS-like demyelination."""
        if autoimmune_activity > 0.3:
            self.thickness_ratio = max(0.3, self.thickness_ratio - autoimmune_activity * 0.1)
            self.conduction_velocity_mps = max(10, self.conduction_velocity_mps * 0.9)
    
    def apply_remyelination(self, recovery_factor: float):
        """Remyelination (partial)."""
        self.thickness_ratio = min(1.0, self.thickness_ratio + recovery_factor * 0.02)
        self.conduction_velocity_mps = min(50, self.conduction_velocity_mps + recovery_factor * 2)
    
    def get_snapshot(self) -> dict:
        return {
            "myelin_thickness": round(self.thickness_ratio, 2),
            "node_length_mm": round(self.node_length, 2),
            "conduction_mps": round(self.conduction_velocity_mps, 1)
        }


@dataclass
class SynapticConnections:
    """
    Synaptic Density (Feature 182).
    Connections per neuron; highest in childhood, pruned in adolescence.
    """
    density_per_neuron: float = 10000.0
    pruning_rate: float = 0.0
    spine_density: float = 1.0
    dendritic_branches: int = 12
    
    def apply_pruning(self, age_years: float):
        """Adolescent synaptic pruning."""
        if 12 <= age_years <= 25:
            self.density_per_neuron = max(5000, self.density_per_neuron - 100)
            self.spine_density = max(0.5, self.spine_density - 0.01)
    
    def apply_enrichment(self, learning_activity: float):
        """Learning increases spines."""
        if learning_activity > 0.7:
            self.density_per_neuron = min(15000, self.density_per_neuron + 10)
            self.spine_density = min(1.2, self.spine_density + 0.005)
    
    def get_snapshot(self) -> dict:
        return {
            "synaptic_density": round(self.density_per_neuron, 0),
            "spine_density": round(self.spine_density, 2),
            "dendritic_branches": self.dendritic_branches
        }


@dataclass
class NeurotransmitterSystems:
    """
    Neurotransmitter Turnover (Feature 183).
    5-HIAA (serotonin), HVA (dopamine), MHPG (norepinephrine) in CSF.
    """
    serotonin_5hiaa: float = 50.0  # ng/mL CSF
    dopamine_hva: float = 40.0
    norepinephrine_mhpg: float = 30.0
    
    turnover_rate: float = 0.1
    
    def apply_depletion(self, stress_level: float):
        """Stress depletes neurotransmitters."""
        self.serotonin_5hiaa = max(10, self.serotonin_5hiaa - stress_level * 2)
        self.dopamine_hva = max(8, self.dopamine_hva - stress_level * 1.5)
        self.norepinephrine_mhpg = max(6, self.norepinephrine_mhpg - stress_level * 1)
    
    def apply_synthesis(self, precursor_availability: float):
        """Diet/precursors restore."""
        self.serotonin_5hiaa = min(80, self.serotonin_5hiaa + precursor_availability * 3 * self.turnover_rate)
        self.dopamine_hva = min(60, self.dopamine_hva + precursor_availability * 2 * self.turnover_rate)
        self.norepinephrine_mhpg = min(45, self.norepinephrine_mhpg + precursor_availability * 1.5 * self.turnover_rate)
    
    def get_snapshot(self) -> dict:
        return {
            "5HIAA": round(self.serotonin_5hiaa, 1),
            "HVA": round(self.dopamine_hva, 1),
            "MHPG": round(self.norepinephrine_mhpg, 1)
        }


@dataclass
class BloodBrainBarrier:
    """
    Blood-Brain Barrier Permeability (Feature 184).
    Tight junction integrity; inflammation increases leakiness.
    """
    permeability: float = 0.05  # 0-1 (low = healthy)
    tight_junction_integrity: float = 0.95
    transporter_efficiency: float = 0.9
    
    def apply_inflammation(self, inflammatory_markers: float):
        """Inflammation increases permeability."""
        if inflammatory_markers > 0.5:
            self.permeability = min(0.4, self.permeability + (inflammatory_markers - 0.5) * 0.1)
            self.tight_junction_integrity = max(0.6, self.tight_junction_integrity - (inflammatory_markers - 0.5) * 0.05)
    
    def apply_repair(self):
        """Repair mechanisms."""
        self.permeability = max(0.02, self.permeability - 0.005)
        self.tight_junction_integrity = min(0.98, self.tight_junction_integrity + 0.01)
    
    def get_snapshot(self) -> dict:
        return {
            "permeability": round(self.permeability, 3),
            "tight_junction_integrity": round(self.tight_junction_integrity, 2),
            "transporter_efficiency": round(self.transporter_efficiency, 2)
        }


@dataclass
class CerebralBloodFlow:
    """
    Cerebral Blood Flow Autoregulation (Feature 185).
    Constant perfusion despite pressure changes; fails in stroke.
    """
    cerebral_blood_flow_ml_min: float = 750.0
    autoregulation_range: tuple = (60, 150)  # MAP mmHg
    autoregulation_efficiency: float = 0.95
    
    mean_arterial_pressure: float = 90.0
    
    def apply_hypotension(self, map_level: float):
        """Low MAP triggers autoregulation."""
        if map_level < self.autoregulation_range[0]:
            vasodilation = (self.autoregulation_range[0] - map_level) / 20
            self.cerebral_blood_flow_ml_min = min(1000, self.cerebral_blood_flow_ml_min + vasodilation * 50)
    
    def apply_ischemia(self, duration_hours: float):
        """Stroke-like ischemia."""
        if duration_hours > 1:
            damage = duration_hours * 0.01
            self.cerebral_blood_flow_ml_min = max(300, self.cerebral_blood_flow_ml_min - damage * 100)
            self.autoregulation_efficiency = max(0.5, self.autoregulation_efficiency - damage * 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "cbf_ml_min": round(self.cerebral_blood_flow_ml_min, 0),
            "autoregulation_efficiency": round(self.autoregulation_efficiency, 2),
            "map_mmHg": round(self.mean_arterial_pressure, 0)
        }


@dataclass
class GlymphaticSystem:
    """
    Glymphatic Clearance Rate (Feature 186).
    Waste removal during sleep; impaired in Alzheimer's.
    """
    clearance_rate: float = 1.0  # relative to baseline
    aquaporin4_expression: float = 1.0
    interstitial_volume_fraction: float = 0.2
    
    def apply_sleep_deprivation(self, hours_awake: float):
        """Sleep deprivation impairs glymphatic."""
        if hours_awake > 20:
            self.clearance_rate = max(0.3, self.clearance_rate - 0.05)
            self.aquaporin4_expression = max(0.5, self.aquaporin4_expression - 0.02)
    
    def apply_deep_sleep(self, slow_wave_hours: float):
        """Slow wave sleep enhances clearance."""
        if slow_wave_hours > 1:
            self.clearance_rate = min(1.5, self.clearance_rate + slow_wave_hours * 0.1)
            self.aquaporin4_expression = min(1.2, self.aquaporin4_expression + 0.02)
    
    def apply_age_decline(self, age_years: float):
        """Age impairs glymphatic function."""
        if age_years > 60:
            decline = (age_years - 60) / 100
            self.clearance_rate = max(0.4, self.clearance_rate - decline * 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "clearance_rate": round(self.clearance_rate, 2),
            "aq4_expression": round(self.aquaporin4_expression, 2),
            "interstitial_fraction": round(self.interstitial_volume_fraction, 2)
        }


@dataclass
class BDNFSystem:
    """
    Brain-Derived Neurotrophic Factor (Feature 187).
    Neuroplasticity promoter; exercise increases this.
    """
    bdnf_level: float = 0.8  # ng/mL serum
    trkb_receptor_occupancy: float = 0.7
    neuroplasticity_capacity: float = 0.8
    
    def apply_exercise(self, intensity: float, duration_minutes: float):
        """Exercise increases BDNF."""
        if intensity > 0.5 and duration_minutes > 20:
            self.bdnf_level = min(1.5, self.bdnf_level + intensity * duration_minutes / 1000)
            self.trkb_receptor_occupancy = min(1.0, self.trkb_receptor_occupancy + 0.01)
    
    def apply_learning(self, complexity: float):
        """Learning via BDNF."""
        if complexity > 0.7:
            self.neuroplasticity_capacity = min(1.0, self.neuroplasticity_capacity + complexity * 0.02)
    
    def apply_stress(self, cortisol: float):
        """Chronic stress suppresses BDNF."""
        if cortisol > 0.6:
            self.bdnf_level = max(0.3, self.bdnf_level - (cortisol - 0.6) * 0.3)
            self.trkb_receptor_occupancy = max(0.4, self.trkb_receptor_occupancy - (cortisol - 0.6) * 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "bdnf_level": round(self.bdnf_level, 2),
            "trkb_occupancy": round(self.trkb_receptor_occupancy, 2),
            "neuroplasticity": round(self.neuroplasticity_capacity, 2)
        }


@dataclass
class DefaultModeNetwork:
    """
    Default Mode Network Connectivity (Feature 188).
    Resting-state network; overactive in depression and rumination.
    """
    connectivity: float = 0.7  # 0-1 between regions
    medial_pfc_activity: float = 0.6
    posterior_cingulate_activity: float = 0.6
    angular_gyrus_activity: float = 0.5
    
    def apply_rumination(self, rumination_hours: float):
        """Rumination increases DMN."""
        if rumination_hours > 2:
            self.connectivity = min(1.0, self.connectivity + rumination_hours * 0.02)
            self.medial_pfc_activity = min(1.0, self.medial_pfc_activity + rumination_hours * 0.03)
    
    def apply_mindfulness(self, minutes: float):
        """Mediation reduces DMN."""
        if minutes > 10:
            self.connectivity = max(0.4, self.connectivity - minutes / 500)
            self.medial_pfc_activity = max(0.4, self.medial_pfc_activity - minutes / 300)
    
    def apply_depression(self, severity: float):
        """Depression increases DMN connectivity."""
        self.connectivity = min(1.0, self.connectivity + severity * 0.3)
    
    def get_snapshot(self) -> dict:
        return {
            "connectivity": round(self.connectivity, 2),
            "mpfc_activity": round(self.medial_pfc_activity, 2),
            "pcc_activity": round(self.posterior_cingulate_activity, 2),
            "angular_activity": round(self.angular_gyrus_activity, 2)
        }


@dataclass
class SalienceNetwork:
    """
    Salience Network Switching (Feature 189).
    Internal/external attention toggle; impaired in psychosis.
    """
    switching_efficiency: float = 0.85
    anterior_insula_activity: float = 0.7
    acc_activity: float = 0.75  # Anterior cingulate
    toggle_response_time_ms: float = 300.0
    
    def apply_psychosis(self, psychosis_factor: float):
        """Psychosis impairs switching."""
        self.switching_efficiency = max(0.3, self.switching_efficiency - psychosis_factor * 0.2)
        self.toggle_response_time_ms = min(2000, self.toggle_response_time_ms + psychosis_factor * 200)
    
    def apply_stress(self, stress_level: float):
        """Stress affects salience detection."""
        if stress_level > 0.7:
            self.anterior_insula_activity = min(1.0, self.anterior_insula_activity + 0.1)
            self.acc_activity = min(1.0, self.acc_activity + 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "switching_efficiency": round(self.switching_efficiency, 2),
            "insula_activity": round(self.anterior_insula_activity, 2),
            "acc_activity": round(self.acc_activity, 2),
            "response_time_ms": round(self.toggle_response_time_ms, 0)
        }


@dataclass
class CentralExecutiveNetwork:
    """
    Central Executive Network Load (Feature 190).
    Working memory and goal maintenance; capacity limited.
    """
    load: float = 0.3  # 0-1 current load
    capacity: float = 7.0  # items (Miller's 7±2)
    efficiency: float = 0.8
    prefrontal_activation: float = 0.7
    
    def apply_working_memory_task(self, items: int, load_level: float):
        """Working memory use."""
        self.load = min(1.0, items / self.capacity)
        self.prefrontal_activation = min(1.0, self.prefrontal_activation + load_level * 0.2)
    
    def apply_interference(self, interference_level: float):
        """Interference reduces capacity."""
        self.capacity = max(3, self.capacity - interference_level * 0.5)
        self.efficiency = max(0.4, self.efficiency - interference_level * 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "current_load": round(self.load, 2),
            "capacity_items": round(self.capacity, 1),
            "efficiency": round(self.efficiency, 2),
            "pfc_activation": round(self.prefrontal_activation, 2)
        }


@dataclass
class CerebellarSystem:
    """
    Cerebellar Function (Feature 191).
    Motor coordination and cognitive timing; "little brain" underestimated.
    """
    motor_coordination: float = 0.85
    timing_precision_ms: float = 20.0  # ms
    sequence_learning: float = 0.8
    cognitive_coupling: float = 0.6
    
    def apply_motor_practice(self, practice_hours: float):
        """Practice improves motor coordination."""
        if practice_hours > 0:
            self.motor_coordination = min(1.0, self.motor_coordination + practice_hours * 0.01)
            self.timing_precision_ms = max(5, self.timing_precision_ms - practice_hours * 0.5)
            self.sequence_learning = min(1.0, self.sequence_learning + practice_hours * 0.02)
    
    def apply_age_decline(self, age_years: float):
        """Age affects cerebellum."""
        if age_years > 60:
            decline = (age_years - 60) / 200
            self.motor_coordination = max(0.5, self.motor_coordination - decline)
            self.cognitive_coupling = max(0.3, self.cognitive_coupling - decline * 0.5)
    
    def get_snapshot(self) -> dict:
        return {
            "motor_coordination": round(self.motor_coordination, 2),
            "timing_ms": round(self.timing_precision_ms, 0),
            "sequence_learning": round(self.sequence_learning, 2),
            "cognitive_coupling": round(self.cognitive_coupling, 2)
        }


@dataclass
class BrainstemVital:
    """
    Brainstem Vital Functions (Feature 192).
    Respiratory and cardiac centers; locked-in syndrome if preserved.
    """
    respiratory_drive: float = 1.0
    cardiac_modulation: float = 1.0  # vagal tone
    arousal_level: float = 0.9
    sleep_wake_cycle: float = 0.8
    
    def apply_compression(self, lesion_factor: float):
        """Brainstem lesion."""
        self.respiratory_drive = max(0.2, self.respiratory_drive - lesion_factor * 0.3)
        self.cardiac_modulation = max(0.3, self.cardiac_modulation - lesion_factor * 0.2)
        self.arousal_level = max(0.2, self.arousal_level - lesion_factor * 0.3)
    
    def get_snapshot(self) -> dict:
        return {
            "respiratory_drive": round(self.respiratory_drive, 2),
            "cardiac_modulation": round(self.cardiac_modulation, 2),
            "arousal_level": round(self.arousal_level, 2),
            "sleep_wake": round(self.sleep_wake_cycle, 2)
        }


@dataclass
class ThalamicSystem:
    """
    Thalamic Gating (Feature 193).
    Sensory relay filtering; thalamocortical dysrhythmia in pain disorders.
    """
    gating_efficiency: float = 0.85
    sensory_filtering: float = 0.8
    relay_accuracy: float = 0.9
    thalamocortical_coherence: float = 0.75
    
    def apply_chronic_pain(self, pain_duration_days: float):
        """Chronic pain alters thalamic gating."""
        if pain_duration_days > 30:
            dysrhythmia = pain_duration_days / 1000
            self.gating_efficiency = max(0.4, self.gating_efficiency - dysrhythmia)
            self.thalamocortical_coherence = max(0.4, self.thalamocortical_coherence - dysrhythmia * 0.5)
    
    def get_snapshot(self) -> dict:
        return {
            "gating_efficiency": round(self.gating_efficiency, 2),
            "sensory_filtering": round(self.sensory_filtering, 2),
            "relay_accuracy": round(self.relay_accuracy, 2),
            "coherence": round(self.thalamocortical_coherence, 2)
        }


@dataclass
class HypothalamicIntegration:
    """
    Hypothalamic Integration (Feature 194).
    Homeostatic hub; connects nervous and endocrine systems.
    """
    homeostatic_setpoint: float = 0.5  # balance
    temperature_regulation: float = 0.95
    hunger_satiety_balance: float = 0.5
    circadian_rhythm_strength: float = 0.8
    
    thyroid_axis: float = 0.8  # HPT axis
    adrenal_axis: float = 0.5  # HPA axis
    growth_axis: float = 0.8  # GH axis
    
    def apply_chronic_stress(self, cortisol: float):
        """HPA axis dysfunction."""
        if cortisol > 0.7:
            self.adrenal_axis = max(0.2, self.adrenal_axis - 0.05)
    
    def apply_sleep_disruption(self, nights_deprived: int):
        """Sleep loss affects all axes."""
        self.circadian_rhythm_strength = max(0.3, self.circadian_rhythm_strength - nights_deprived * 0.05)
        self.thyroid_axis = max(0.5, self.thyroid_axis - nights_deprived * 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "homeostatic_balance": round(self.homeostatic_setpoint, 2),
            "temperature_reg": round(self.temperature_regulation, 2),
            "hunger_balance": round(self.hunger_satiety_balance, 2),
            "circadian_strength": round(self.circadian_rhythm_strength, 2),
            "thyroid_axis": round(self.thyroid_axis, 2),
            "adrenal_axis": round(self.adrenal_axis, 2),
            "growth_axis": round(self.growth_axis, 2)
        }


@dataclass
class PinealGland:
    """
    Pineal Gland Calcification (Feature 195).
    Melatonin production decline; age-related sleep disruption.
    """
    calcification: float = 0.1  # 0-1 (1 = fully calcified)
    melatonin_production: float = 0.8  # pg/mL
    melatonin_peak_time: float = 2.0  # hours after sleep onset
    circadian_amplitude: float = 0.7
    
    def apply_age(self, age_years: float):
        """Age-related calcification."""
        if age_years > 40:
            self.calcification = min(1.0, (age_years - 40) / 100)
            self.melatonin_production = max(0.1, self.melatonin_production - self.calcification * 0.5)
            self.circadian_amplitude = max(0.2, self.circadian_amplitude - self.calcification * 0.3)
    
    def apply_light_exposure(self, lux_hours: float):
        """Light suppresses melatonin."""
        if lux_hours > 100:
            self.melatonin_production = max(0.2, self.melatonin_production - lux_hours / 1000)
    
    def get_snapshot(self) -> dict:
        return {
            "calcification": round(self.calcification, 2),
            "melatonin_production": round(self.melatonin_production, 2),
            "peak_time": round(self.melatonin_peak_time, 1),
            "circadian_amplitude": round(self.circadian_amplitude, 2)
        }


@dataclass
class NeurologyModel:
    """
    Complete Neurological Model.
    Integrates all brain structure and function features.
    """
    # Structural features
    cortex: CorticalStructure = field(default_factory=CorticalStructure)
    hippocampus: Hippocampus = field(default_factory=Hippocampus)
    amygdala: Amygdala = field(default_factory=Amygdala)
    prefrontal: PrefrontalCortex = field(default_factory=PrefrontalCortex)
    white_matter: WhiteMatterTracts = field(default_factory=WhiteMatterTracts)
    myelin: MyelinSheath = field(default_factory=MyelinSheath)
    synapses: SynapticConnections = field(default_factory=SynapticConnections)
    neurotransmitters: NeurotransmitterSystems = field(default_factory=NeurotransmitterSystems)
    bbb: BloodBrainBarrier = field(default_factory=BloodBrainBarrier)
    cerebral_blood_flow: CerebralBloodFlow = field(default_factory=CerebralBloodFlow)
    glymphatic: GlymphaticSystem = field(default_factory=GlymphaticSystem)
    bdnf: BDNFSystem = field(default_factory=BDNFSystem)
    
    # Network features
    dmn: DefaultModeNetwork = field(default_factory=DefaultModeNetwork)
    salience: SalienceNetwork = field(default_factory=SalienceNetwork)
    cen: CentralExecutiveNetwork = field(default_factory=CentralExecutiveNetwork)
    cerebellum: CerebellarSystem = field(default_factory=CerebellarSystem)
    brainstem: BrainstemVital = field(default_factory=BrainstemVital)
    thalamus: ThalamicSystem = field(default_factory=ThalamicSystem)
    hypothalamus: HypothalamicIntegration = field(default_factory=HypothalamicIntegration)
    pineal: PinealGland = field(default_factory=PinealGland)
    
    def tick(
        self,
        age_years: float,
        stress_level: float,
        cortisol: float,
        bdnf_level: float,
        sleep_hours: float,
        inflammatory_markers: float,
        activity: str = "idle",
        blood_pressure_systolic: float = 120.0,
        learning_complexity: float = 0.5,
        practice_hours: float = 0.0,
        rumination_hours: float = 0.0
    ):
        """Update all neurological systems each tick."""
        # Age-related changes
        self.cortex.age_decline(age_years, stress_level)
        self.prefrontal.age_maturation(age_years)
        self.synapses.apply_pruning(age_years)
        self.cerebellum.apply_age_decline(age_years)
        self.glymphatic.apply_age_decline(age_years)
        self.pineal.apply_age(age_years)
        
        # Stress and cortisol effects
        self.hippocampus.apply_stress(cortisol)
        self.amygdala.apply_chronic_stress(stress_level)
        self.neurotransmitters.apply_depletion(stress_level)
        self.bdnf.apply_stress(cortisol)
        self.hypothalamus.apply_chronic_stress(cortisol)
        
        # Activity effects
        if activity == "exercise":
            intensity = 0.7
            self.bdnf.apply_exercise(intensity, 30)
            self.hippocampus.apply_exercise(bdnf_level)
        
        if activity == "work":
            self.cen.apply_working_memory_task(3, 0.5)
            self.synapses.apply_enrichment(learning_complexity)
        
        if activity == "socialize":
            self.amygdala.apply_extinction(True)
        
        # Sleep effects
        if sleep_hours >= 7:
            slow_wave = max(0, sleep_hours - 5)
            self.glymphatic.apply_deep_sleep(slow_wave)
        else:
            self.glymphatic.apply_sleep_deprivation(16 - sleep_hours)
        
        # Inflammation
        self.bbb.apply_inflammation(inflammatory_markers)
        
        # Blood pressure
        self.white_matter.apply_hypertension(blood_pressure_systolic, 1)
        
        # Motor practice
        self.cerebellum.apply_motor_practice(practice_hours)
        
        # Rumination/DMN
        self.dmn.apply_rumination(rumination_hours)
    
    def get_snapshot(self) -> dict:
        """Full neurological state snapshot."""
        return {
            "cortical": self.cortex.get_snapshot(),
            "hippocampus": self.hippocampus.get_snapshot(),
            "amygdala": self.amygdala.get_snapshot(),
            "prefrontal": self.prefrontal.get_snapshot(),
            "white_matter": self.white_matter.get_snapshot(),
            "myelin": self.myelin.get_snapshot(),
            "synapses": self.synapses.get_snapshot(),
            "neurotransmitters": self.neurotransmitters.get_snapshot(),
            "bbb": self.bbb.get_snapshot(),
            "cerebral_blood_flow": self.cerebral_blood_flow.get_snapshot(),
            "glymphatic": self.glymphatic.get_snapshot(),
            "bdnf": self.bdnf.get_snapshot(),
            "dmn": self.dmn.get_snapshot(),
            "salience": self.salience.get_snapshot(),
            "cen": self.cen.get_snapshot(),
            "cerebellum": self.cerebellum.get_snapshot(),
            "brainstem": self.brainstem.get_snapshot(),
            "thalamus": self.thalamus.get_snapshot(),
            "hypothalamus": self.hypothalamus.get_snapshot(),
            "pineal": self.pineal.get_snapshot()
        }