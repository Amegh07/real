"""
Embodied Agent Physiology — God-Tier Architecture
===========================================
Replaces simple stat cards (hunger/energy/happiness) with:
- 11 organ systems with real physiological markers
- Hormone system (cortisol, dopamine, serotonin, testosterone, oxytocin)
- Microbiome model (Gut-brain axis)
- Neurochemistry (reward prediction error)
- Interoception (feeling the body)
- NEW: Neurology and Cognition systems (Section B1 & B2)

Based on spec Section 6: Hyper-Realistic Human Agent Architecture
"""

import uuid
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from utils.logger import get_logger

# Import neurology and cognition systems (in backend module)
try:
    from backend.neurology import NeurologyModel
    from backend.cognition import CognitionModel
except ImportError:
    NeurologyModel = None
    CognitionModel = None

logger = get_logger(__name__)


class OrganSystem(Enum):
    """The 11 major organ systems."""
    CARDIOVASCULAR = auto()
    RESPIRATORY = auto()
    GASTROINTESTINAL = auto()
    RENAL = auto()
    MUSCULOSKELETAL = auto()
    INTEGUMENTARY = auto()
    HEMATOLOGIC = auto()
    ENDOCRINE = auto()
    IMMUNE = auto()
    NERVOUS = auto()
    REPRODUCTIVE = auto()


@dataclass
class OrganState:
    """State for a single organ system (0-100 scale, 50 = healthy adult baseline)."""
    system: OrganSystem
    health: float = 50.0  # Overall system health
    efficiency: float = 1.0  # 0.0-1.0 capacity multiplier
    
    # System-specific markers (as defined in spec)
    markers: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize baseline markers for each system
        self.markers = self._get_default_markers()
    
    def _get_default_markers(self) -> Dict[str, float]:
        defaults = {
            OrganSystem.CARDIOVASCULAR: {
                "heart_rate": 72.0, "hrv": 50.0, "blood_pressure_systolic": 120.0,
                "blood_pressure_diastolic": 80.0, "arterial_stiffness": 0.3
            },
            OrganSystem.RESPIRATORY: {
                "fev1": 95.0, "fvc_ratio": 0.8, "oxygen_saturation": 98.0,
                "respiratory_rate": 14.0, "lung_compliance": 0.8
            },
            OrganSystem.GASTROINTESTINAL: {
                "gastric_emptying": 1.0, "intestinal_permeability": 0.1,
                "microbiome_diversity": 0.8, "bile_acid_pool": 1.0
            },
            OrganSystem.RENAL: {
                "gfr": 90.0, "creatinine": 1.0, "sodium_balance": 0.5,
                "water_balance": 0.5, "acid_base": 0.5
            },
            OrganSystem.MUSCULOSKELETAL: {
                "bone_density": 1.0, "muscle_mass": 1.0, "tendon_stiffness": 0.8,
                "cartilage_health": 1.0, "fracture_healing": 1.0
            },
            OrganSystem.INTEGUMENTARY: {
                "skin_elasticity": 0.8, "melanin": 0.5, "wound_healing": 1.0,
                "thermoregulation": 0.9, "barrier_integrity": 1.0
            },
            OrganSystem.HEMATOLOGIC: {
                "hematocrit": 45.0, "iron_stores": 0.8, "coagulation": 1.0,
                "platelet_function": 1.0, "white_blood_cells": 1.0
            },
            OrganSystem.ENDOCRINE: {
                "cortisol": 0.5, "thyroid": 1.0, "insulin_sensitivity": 1.0,
                "testosterone": 0.5, "estrogen": 0.5, "growth_hormone": 0.5
            },
            OrganSystem.IMMUNE: {
                "igG": 1.0, "igM": 1.0, "igA": 1.0, "t_cell_diversity": 0.9,
                "nk_cell_activity": 0.8, "complement": 1.0, "inflammatory_markers": 0.1
            },
            OrganSystem.NERVOUS: {
                "cortical_thickness": 1.0, "hippocampal_volume": 1.0,
                "myelination": 1.0, "synaptic_density": 1.0, "bdnf": 0.8
            },
            OrganSystem.REPRODUCTIVE: {
                "follicle_count": 100000, "sperm_motility": 0.8,
                "testosterone": 0.5, "estrogen": 0.5, "fertility": 1.0
            }
        }
        return defaults.get(self.system, {})


@dataclass
class HormoneState:
    """
    Hormone levels (0-1 normalized, 0.5 = baseline).
    Based on spec Section 6.10: endocrine system as emotional infrastructure.
    """
    # Primary hormones
    cortisol: float = 0.5      # Stress response (0.5 = baseline, high = chronic stress)
    dopamine: float = 0.5       # Reward/motivation
    serotonin: float = 0.5       # Mood regulation
    testosterone: float = 0.5     # Risk-taking, aggression
    oxytocin: float = 0.5        # Trust, bonding
    estrogen: float = 0.5          # (female)
    progesterone: float = 0.5        # (female)
    
    # Metabolic
    insulin: float = 0.5
    leptin: float = 0.5        # Satiety signal
    ghrelin: float = 0.5        # Hunger signal
    thyroid_t3: float = 0.5       # Metabolism
    
    # Neuromodulators
    adrenaline: float = 0.5      # Fight-or-flight
    noradrenaline: float = 0.5
    acetylcholine: float = 0.5      # Memory, attention
    
    def apply_stress_response(self, stress_level: float):
        """Sympathetic activation: fight-or-flight mode."""
        # Cortisol spike
        self.cortisol = min(1.0, self.cortisol + stress_level * 0.3)
        # Adrenaline
        self.adrenaline = min(1.0, self.adrenaline + stress_level * 0.4)
        self.noradrenaline = min(1.0, self.noradrenaline + stress_level * 0.3)
        # Suppress non-emergency systems
        self.serotonin = max(0.1, self.serotonin - stress_level * 0.1)
        self.dopamine = max(0.1, self.dopamine - stress_level * 0.1)
    
    def apply_rest_response(self):
        """Parasympathetic activation: rest-and-digest."""
        self.cortisol = max(0.2, self.cortisol - 0.1)
        self.adrenaline = max(0.1, self.adrenaline - 0.2)
        self.oxytocin = min(1.0, self.oxytocin + 0.1)
    
    def get_all_levels(self) -> Dict[str, float]:
        return {
            "cortisol": self.cortisol,
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "testosterone": self.testosterone,
            "oxytocin": self.oxytocin,
            "estrogen": self.estrogen,
            "progesterone": self.progesterone,
            "insulin": self.insulin,
            "leptin": self.leptin,
            "ghrelin": self.ghrelin,
            "thyroid_t3": self.thyroid_t3,
            "adrenaline": self.adrenaline,
        }


@dataclass
class MicrobiomeState:
    """
    Gut microbiome model (spec Section 6.11).
    Affects mood via gut-brain axis (GABA precursors, serotonin).
    """
    # Key bacterial populations (0-1 relative abundance)
    bacteroides: float = 0.3      # Polysaccharide digestion
    akkermansia: float = 0.2       # Mucus maintenance
    lactobacillus: float = 0.2         # Immune modulation
    bifidobacterium: float = 0.15      # Fiber fermentation
    clostridium: float = 0.1         # (can be pathogenic)
    firmicutes: float = 0.25
    proteobacteria: float = 0.05
    
    # Metabolites produced
    short_chain_fatty_acids: float = 0.6  # Butyrate, propionate, acetate
    gaba_precursors: float = 0.5        # For anxiety
    b12_production: float = 0.7
    
    # Health markers
    diversity_index: float = 0.7   # Shannon diversity
    dysbiosis_level: float = 0.1   # 0 = healthy, 1 = severe
    
    def apply_diet(self, fiber_intake: float, antibiotic_exposure: float):
        """Update microbiome based on diet and exposure."""
        # Antibiotics devastate populations
        if antibiotic_exposure > 0.3:
            self.lactobacillus *= max(0.1, 1 - antibiotic_exposure * 0.8)
            self.bifidobacterium *= max(0.1, 1 - antibiotic_exposure * 0.7)
            self.diversity_index *= max(0.2, 1 - antibiotic_exposure * 0.5)
            self.dysbiosis_level = min(1.0, self.dysbiosis_level + antibiotic_exposure * 0.4)
        
        # Fiber promotes beneficial bacteria
        if fiber_intake > 0.5:
            self.short_chain_fatty_acids = min(1.0, self.short_chain_fatty_acids + fiber_intake * 0.1)
            self.bifidobacterium = min(1.0, self.bifidobacterium + fiber_intake * 0.1)
            self.lactobacillus = min(1.0, self.lactobacillus + fiber_intake * 0.05)
    
    def get_gut_brain_signal(self) -> float:
        """GABA precursor availability affecting anxiety (0-1)."""
        # Low diversity = less GABA = more anxiety
        return self.diversity_index * self.short_chain_fatty_acids * (1 - self.dysbiosis_level)


@dataclass
class PhysiologyModel:
    """
    Complete embodied physiology for one agent.
    Replaces: hunger, energy, happiness (stat cards)
    """
    # Organ systems
    organs: Dict[OrganSystem, OrganState] = field(default_factory=dict)
    
    # Hormones
    hormones: HormoneState = field(default_factory=HormoneState)
    
    # Microbiome (gut-brain axis)
    microbiome: MicrobiomeState = field(default_factory=MicrobiomeState)
    
    # Metabolic state
    blood_glucose: float = 90.0    # mg/dL
    glycogen_stores: float = 100.0   # 100g capacity
    adipose_tissue: float = 2000.0     # kcal capacity
    blood_glucose_insulin: float = 1.0
    
    # Energy budgets
    metabolic_rate: float = 1500.0  # Base metabolic rate (kcal/day)
    basal_metabolic_rate: float = 1500.0  # Stored baseline
    energy_available: float = 100.0   # Derived from glycogen + fat
    
    # Interoceptive signals (what the body "feels")
    hunger_signal: float = 0.0
    thirst_signal: float = 0.0
    fatigue_signal: float = 0.0
    pain_signal: float = 0.0
    nausea_signal: float = 0.0
    
    # Autonomic state (sympathetic vs parasympathetic)
    autonomic_state: str = "balanced"  # "sympathetic", "parasympathetic", "balanced"
    
    # Sleep architecture
    sleep_debt: float = 0.0         # Cumulative sleep debt
    rem_pressure: float = 0.0         # REM rebound need
    slow_wave_pressure: float = 0.0     # Deep sleep need
    
    # Injury/damage
    injuries: List[dict] = field(default_factory=list)
    pain_level: float = 0.0
    
    # Cognitive state
    cognition_impairment: float = 0.0  # 0 = normal, 1 = completely impaired
    social_interactions: float = 0.0  # Track for serotonin update
    
    # Age-related decline
    biological_age: float = 20.0
    telomere_length: float = 1.0
    
    # Section B1: Neurology (Brain Structure & Function)
    neurology: Optional[NeurologyModel] = None
    
    # Section B2: Cognition (Cognitive Modules)
    cognition: Optional[CognitionModel] = None
    
    def __post_init__(self):
        # Initialize all organ systems
        for system in OrganSystem:
            self.organs[system] = OrganState(system=system)
        # Initialize neurology and cognition systems if available
        if NeurologyModel is not None:
            self.neurology = NeurologyModel()
        if CognitionModel is not None:
            self.cognition = CognitionModel()
        
        # Performance budget tracking
        self._tick_compute_time: float = 0.0
        self._last_tick_duration: float = 0.0
        self._skip_neurology: bool = False
        self._skip_cognition: bool = False
    
    @property
    def compute_budget_exceeded(self) -> bool:
        """Check if last tick exceeded performance budget."""
        return self._last_tick_duration > 5.0  # 5ms budget
    
    def _should_skip_expensive_updates(self) -> bool:
        """Dynamic fidelity: skip cognition/neurology if behind."""
        if self._last_tick_duration > 10.0:
            return True
        elif self._last_tick_duration > 5.0:
            self._skip_neurology = True
            self._skip_cognition = True
            return True
        return False
    
    def tick(self, tick: int, activity: str, food_available: float, sleep_hours: float):
        """Update physiology each simulation tick with fail-safe and tiered updates."""
        # TIER 1: Every tick (critical systems)
        try:
            self._update_metabolism(activity, food_available)
            self._update_autonomic(activity)
            self._update_interoception()
            self._update_sleep_architecture(sleep_hours)
            self._update_age()
            self._check_organ_system_damage()
            
            # TIER 2: Every 5 ticks (hormones)
            if tick % 5 == 0:
                self._update_hormones(tick)
            
            # TIER 3: Every 10 ticks (cognition + neurology)
            if tick % 10 == 0 and not self._should_skip_expensive_updates():
                self._update_neurology_and_cognition(activity, sleep_hours)
            elif tick % 10 != 0:
                self._skip_neurology = True
                self._skip_cognition = True

            if not self.validate_state():
                self._apply_fail_safe()
                
        except Exception as e:
            logger.error(f"Tick failure for agent: {e}")
            self._apply_fail_safe()
        self._check_failure_states()
    
    def validate_state(self) -> bool:
        """Validate biological invariants. Returns False if invalid."""
        if not (0 <= self.hormones.cortisol <= 1):
            return False
        if not (0 <= self.hormones.dopamine <= 1):
            return False
        if not (0 <= self.hormones.serotonin <= 1):
            return False
        if self.blood_glucose < 0:
            return False
        if self.blood_glucose > 500:
            return False
        if self.energy_available < 0:
            return False
        if self.adipose_tissue < 0:
            return False
        if self.glycogen_stores < 0:
            return False
        if self.sleep_debt < 0:
            return False
        for organ in self.organs.values():
            if not (0 <= organ.health <= 100):
                return False
        return True
    
    def is_dead(self) -> bool:
        """Check if agent has reached terminal state."""
        return (
            self.organs[OrganSystem.CARDIOVASCULAR].health <= 0 or
            self.organs[OrganSystem.NERVOUS].health <= 0 or
            self.blood_glucose < 20 or
            self.energy_available <= 0
        )
    
    def _apply_fail_safe(self):
        """Reset to stable baseline on failure."""
        self.blood_glucose = max(self.blood_glucose, 70)
        self.blood_glucose = min(self.blood_glucose, 140)
        
        self.hormones.cortisol = max(0.2, min(0.8, self.hormones.cortisol))
        self.hormones.dopamine = max(0.2, min(0.8, self.hormones.dopamine))
        self.hormones.serotonin = max(0.2, min(0.8, self.hormones.serotonin))
        self.hormones.adrenaline = max(0.1, min(0.9, self.hormones.adrenaline))
        
        self.energy_available = max(self.energy_available, 10)
        self.adipose_tissue = max(self.adipose_tissue, 500)
        self.glycogen_stores = max(self.glycogen_stores, 20)
        
        for organ in self.organs.values():
            organ.health = max(10, min(90, organ.health))
    
    def _check_failure_states(self):
        """Check for catastrophic failure conditions."""
        # Hypoglycemia - brain can't function
        if self.blood_glucose < 50:
            self.hormones.dopamine = 0.1
            self.hormones.serotonin = 0.1
            self.cognition_impairment = min(1.0, self.cognition_impairment + 0.3)
        
        # Hyperglycemia - organ damage
        if self.blood_glucose > 250:
            self.organs[OrganSystem.RENAL].health -= 0.5
            self.organs[OrganSystem.CARDIOVASCULAR].health -= 0.2
        
        # Organ system failure cascade
        if self.organs[OrganSystem.CARDIOVASCULAR].health < 10:
            self.hormones.adrenaline = 0.9
            self.hormones.cortisol = 0.9
        
        if self.organs[OrganSystem.NERVOUS].health < 10:
            self.cognition_impairment = 1.0
            self.hormones.dopamine = 0.1
        
        # Sleep debt cognitive collapse
        if self.sleep_debt > 20:
            self.cognition_impairment = min(1.0, self.cognition_impairment + 0.2)
        
        # Energy starvation
        if self.energy_available < 5:
            self.hormones.cortisol = min(1.0, self.hormones.cortisol + 0.1)
    
    def _update_metabolism(self, activity: str, food_available: float):
        """Metabolic processing based on food intake and activity."""
        basal_cost = self.metabolic_rate / 86400 * 0.8

        activity_costs = {
            "idle": 1.0,
            "sleep": 0.8,
            "work": 2.5,
            "exercise": 4.0,
            "socialize": 1.2,
            "combat": 6.0,
        }

        activity_cost = basal_cost * activity_costs.get(activity, 1.0)

        if food_available > 0:
            self.blood_glucose = min(140, self.blood_glucose + food_available * 1.2)
            insulin_response = min(1.0, (self.blood_glucose - 80) / 100)
            self.blood_glucose_insulin = 1 - insulin_response * 0.3

            glycogen_space = 100 - self.glycogen_stores
            if glycogen_space > 0:
                stored = min(glycogen_space, food_available * 0.5)
                self.glycogen_stores += stored
                food_available -= stored

            if food_available > 0:
                self.adipose_tissue = min(50000, self.adipose_tissue + food_available * 10)

        if self.glycogen_stores > 0:
            burned = min(activity_cost * 0.5, self.glycogen_stores)
            self.glycogen_stores -= burned
            activity_cost -= burned
            self.blood_glucose = max(70, self.blood_glucose - burned)

        if activity_cost > 0 and self.glycogen_stores <= 0:
            fat_burned = min(activity_cost * 0.01, self.adipose_tissue)
            self.adipose_tissue -= fat_burned

        # Calculate energy in consistent kcal units (GLUCOSE_KCAL_PER_MG_DL = 0.0035, GLYCOGEN_KCAL_PER_G = 4.0, FAT_KCAL_PER_UNIT = 1.0)
        glucose_kcal = self.blood_glucose * 0.0035
        glycogen_kcal = self.glycogen_stores * 4.0
        fat_kcal = self.adipose_tissue * 1.0
        
        self.energy_available = glucose_kcal + glycogen_kcal + fat_kcal

        self.hunger_signal = max(0, min(1, (100 - self.blood_glucose) / 50))
        self.hormones.leptin = min(1.0, self.adipose_tissue / 5000)
        if self.hormones.leptin > 0.7:
            self.hunger_signal *= 0.3

    def _update_autonomic(self, activity: str):
        """Update autonomic nervous system state."""
        if activity in ["combat", "exercise", "work"]:
            self.autonomic_state = "sympathetic"
            self.hormones.apply_stress_response(0.3)
        elif activity == "sleep":
            self.autonomic_state = "parasympathetic"
            self.hormones.apply_rest_response()
        else:
            self.autonomic_state = "balanced"

    def _update_interoception(self):
        """Update body feeling signals."""
        self.fatigue_signal = min(1.0, self.sleep_debt / 20)

        if self.injuries:
            self.pain_level = min(1.0, sum(i.get("severity", 0) for i in self.injuries) / 5)
            self.pain_signal = self.pain_level
        else:
            self.pain_signal = 0.0

    def _update_hormones(self, tick: int):
        """Real hormone dynamics with circadian rhythms and feedback loops."""
        tick_fraction = 1 / 86400
        
        # Circadian cortisol rhythm (peak at morning, lowest at night)
        hour = (tick % 1440) / 60  # Approximate hour within day
        circadian_cortisol = 0.3 + 0.4 * math.sin((hour - 6) * math.pi / 12)
        self.hormones.cortisol = self.hormones.cortisol * 0.95 + circadian_cortisol * 0.05
        
        # Blood glucose → insulin → leptin/ghrelin feedback
        if self.blood_glucose > 120:
            self.hormones.insulin = min(1.0, self.hormones.insulin + 0.2)
        elif self.blood_glucose < 80:
            self.hormones.insulin = max(0.1, self.hormones.insulin - 0.1)
        
        # Leptin tracks adipose tissue (delayed signal)
        target_leptin = min(1.0, self.adipose_tissue / 5000)
        self.hormones.leptin = self.hormones.leptin * 0.9 + target_leptin * 0.1
        
        # Ghrelin inversely tracks leptin (hunger signal)
        self.hormones.ghrelin = max(0.1, 1.0 - self.hormones.leptin)
        
        # Thyroid affects metabolic rate
        thyroid_factor = 0.5 + self.hormones.thyroid_t3 * 0.5
        self.metabolic_rate = self.basal_metabolic_rate * thyroid_factor
        
        # Dopamine decay without reward (motivation)
        self.hormones.dopamine = max(0.2, self.hormones.dopamine - 0.01)
        
        # Serotonin from social contact (mood)
        if self.social_interactions > 0:
            self.hormones.serotonin = min(0.9, self.hormones.serotonin + self.social_interactions * 0.05)
        
        # Testosterone slowly cycles
        self.hormones.testosterone = 0.5 + 0.1 * math.sin(tick / 10000)
        
        # Adrenaline decays naturally
        self.hormones.adrenaline = max(0.1, self.hormones.adrenaline - 0.05)
        
        # Acetylcholine for memory (wakefulness dependent)
        wakefulness = max(0, 1 - self.sleep_debt / 20)
        target_acetylcholine = 0.3 + wakefulness * 0.5
        self.hormones.acetylcholine = self.hormones.acetylcholine * 0.8 + target_acetylcholine * 0.2

    def _update_sleep_architecture(self, sleep_hours: float):
        """Track sleep debt and pressures."""
        ideal_sleep = 8.0
        
        if sleep_hours < ideal_sleep:
            self.sleep_debt += (ideal_sleep - sleep_hours)
            # REM debt accumulates faster
            self.rem_pressure += (ideal_sleep - sleep_hours) * 0.5
            self.slow_wave_pressure += (ideal_sleep - sleep_hours) * 0.3
        else:
            self.sleep_debt = max(0, self.sleep_debt - (sleep_hours - ideal_sleep) * 0.5)
            self.rem_pressure = max(0, self.rem_pressure - (sleep_hours - ideal_sleep) * 0.3)
            self.slow_wave_pressure = max(0, self.slow_wave_pressure - (sleep_hours - ideal_sleep) * 0.2)
        
        # Chronic sleep debt affects cognition
        if self.sleep_debt > 10:
            self.pain_signal = min(1.0, self.pain_signal + 0.1)
            self.hormones.cortisol = min(1.0, self.hormones.cortisol + 0.05)
    
    def _update_age(self):
        """Biological aging processes."""
        # Telomere shortening (accelerated by stress)
        stress_factor = self.hormones.cortisol * 0.0001
        self.telomere_length = max(0.1, self.telomere_length - 0.00001 - stress_factor)
        
        # Biological age from telomeres
        self.biological_age = 20 + (1 - self.telomere_length) * 80
    
    def _check_organ_system_damage(self):
        """Check for organ damage from extreme states."""
        # High cortisol damages hippocampus
        if self.hormones.cortisol > 0.8:
            self.organs[OrganSystem.NERVOUS].health -= 0.1
        
        # Sleep deprivation damages glymphatic
        if self.sleep_debt > 15:
            self.organs[OrganSystem.NERVOUS].health -= 0.05
        
        # High blood glucose damages kidneys
        if self.blood_glucose > 180:
            self.organs[OrganSystem.RENAL].health -= 0.05
        
        # Clamp health
        for organ in self.organs.values():
            organ.health = max(0, min(100, organ.health))
    
    def _update_neurology_and_cognition(self, activity: str, sleep_hours: float):
        """Update neurology and cognition systems (Features B1: 176-195, B2: 196-225)."""
        if self.neurology is None or self.cognition is None:
            return
        
        # Get blood pressure from cardiovascular system
        bp_systolic = self.organs.get(OrganSystem.CARDIOVASCULAR, None)
        blood_pressure = bp_systolic.markers.get("blood_pressure_systolic", 120.0) if bp_systolic else 120.0
        
        # Get inflammatory markers from immune system
        immune = self.organs.get(OrganSystem.IMMUNE, None)
        inflammatory_markers = immune.markers.get("inflammatory_markers", 0.1) if immune else 0.1
        
        # Calculate stress level from hormones
        stress_level = self.hormones.cortisol
        cortisol = self.hormones.cortisol
        
        # Get BDNF from neurology model (will be updated)
        bdnf_level = 0.6  # default
        
        # Update neurology (features 176-195)
        self.neurology.tick(
            age_years=self.biological_age,
            stress_level=stress_level,
            cortisol=cortisol,
            bdnf_level=bdnf_level,
            sleep_hours=sleep_hours,
            inflammatory_markers=inflammatory_markers,
            activity=activity,
            blood_pressure_systolic=blood_pressure,
            rumination_hours=0.0
        )
        
        # Update cognition (features 196-225)
        fatigue = 1.0 - (self.energy_available / 100)
        self.cognition.tick(
            activity=activity,
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            fatigue=fatigue,
            age_years=self.biological_age
        )
    
    # ── Derived Stats (for compatibility) ──────────────────────────
    
    def get_effective_hunger(self) -> float:
        """Generate hunger compatible stat (0-100)."""
        # Combined: blood glucose, ghrelin, leptin, microbiome
        h = self.hunger_signal * 100
        # Add microbiome signal (dysbiosis can cause false hunger)
        h += self.microbiome.dysbiosis_level * 20
        # Add fatigue
        h += self.fatigue_signal * 10
        return min(100, max(0, h))
    
    def get_effective_energy(self) -> float:
        """Generate energy compatible stat (0-100)."""
        # Based on metabolic state
        e = 50 + (self.energy_available / 50) * 50
        # Sleep debt penalty
        e -= self.sleep_debt * 2
        # Autonomic state
        if self.autonomic_state == "sympathetic":
            e += 10  # Adrenaline boost
        return min(100, max(0, e))
    
    def get_effective_happiness(self) -> float:
        """
        Generate happiness compatible stat.
        Based on neurochemistry, not positive thinking.
        """
        # Serotonin baseline
        h = self.hormones.serotonin * 50
        
        # Dopamine from rewards
        h += self.hormones.dopamine * 30
        
        # Oxytocin from social/bonding
        h += self.hormones.oxytocin * 20
        
        # Gut-brain (depression link)
        gut_signal = self.microbiome.get_gut_brain_signal()
        h += gut_signal * 10
        
        # Chronic stress lowers mood
        h -= self.hormones.cortisol * 15
        
        # Sleep debt causes irritability
        h -= self.sleep_debt * 1.5
        
        # Pain/nausea
        h -= self.pain_signal * 20
        h -= self.nausea_signal * 15
        
        return min(100, max(0, h))
    
    # ── Snapshot ───────────────────────────────────────────
    
    def get_snapshot(self) -> dict:
        return {
            "biological_age": round(self.biological_age, 1),
            "telomere_length": round(self.telomere_length, 3),
            "blood_glucose": round(self.blood_glucose, 1),
            "glycogen_stores": round(self.glycogen_stores, 1),
            "adipose_tissue": round(self.adipose_tissue, 0),
            "energy_available": round(self.energy_available, 1),
            "sleep_debt": round(self.sleep_debt, 2),
            "autonomic_state": self.autonomic_state,
            "hunger": round(self.get_effective_hunger(), 1),
            "energy": round(self.get_effective_energy(), 1),
            "happiness": round(self.get_effective_happiness(), 1),
            "hormones": self.hormones.get_all_levels(),
            "microbiome": {
                "diversity": round(self.microbiome.diversity_index, 2),
                "dysbiosis": round(self.microbiome.dysbiosis_level, 2)
            },
            "organ_health": {
                k.name: round(v.health, 1) 
                for k, v in self.organs.items()
            },
            "biological_features": self._generate_biological_features(),
            "neurology": self.neurology.get_snapshot() if self.neurology else {},
            "cognition": self.cognition.get_snapshot() if self.cognition else {},
        }
    
    def _generate_biological_features(self) -> dict:
        """Generate 175 biological features from physiology state."""
        features = {}
        
        for system, organ in self.organs.items():
            prefix = system.name.lower()[:4]
            
            if system == OrganSystem.CARDIOVASCULAR:
                features["cardio.hrv_rmssd"] = organ.markers.get("hrv", 35.0)
                features["cardio.sdnn"] = organ.markers.get("hrv", 100.0) * 2
                features["cardio.lf_hf_ratio"] = 1.0 + (self.hormones.cortisol - 0.5) * 0.5
                features["cardio.baro_sensitivity"] = 12.0 - (self.biological_age - 20) * 0.1
                features["cardio.pwv"] = 8.0 + (self.biological_age - 20) * 0.15
                features["cardio.ejection_fraction"] = 65.0 - (self.organs[OrganSystem.CARDIOVASCULAR].health - 50) * 0.2
                features["cardio.stroke_volume"] = 80.0 * self.organs[OrganSystem.CARDIOVASCULAR].efficiency
                features["cardio.cardiac_output"] = 5.5 * self.organs[OrganSystem.CARDIOVASCULAR].efficiency
                features["cardio.peripheral_resistance"] = 1000.0 * (1 + (self.hormones.cortisol - 0.5) * 0.3)
                features["cardio.venous_compliance"] = 2.0 - self.hormones.cortisol * 0.3
                features["cardio.capillary_density"] = 250.0 * self.organs[OrganSystem.CARDIOVASCULAR].efficiency
                features["cardio.microcirculation"] = 80.0 * (1 - self.hormones.cortisol * 0.2)
                features["cardio.plaque_burden"] = min(50, (self.biological_age - 30) * 0.5)
                features["cardio.aneurysm_risk"] = min(10, (self.biological_age - 40) * 0.1)
                features["cardio.coagulation"] = 100.0 * self.organs[OrganSystem.HEMATOLOGIC].efficiency
                features["cardio.platelet_aggregation"] = 80.0 * self.organs[OrganSystem.HEMATOLOGIC].efficiency
                features["cardio.fibrinolytic"] = 100.0 * self.organs[OrganSystem.HEMATOLOGIC].efficiency
                features["cardio.blood_viscosity"] = 3.5 + self.organs[OrganSystem.HEMATOLOGIC].markers.get("hematocrit", 45.0) / 100
                features["cardio.hematocrit"] = self.organs[OrganSystem.HEMATOLOGIC].markers.get("hematocrit", 45.0)
                features["cardio.ferritin"] = self.organs[OrganSystem.HEMATOLOGIC].markers.get("iron_stores", 0.8) * 150
                features["cardio.spo2"] = 98.0 - (self.biological_age - 20) * 0.02
                features["cardio.lactate_threshold"] = 60.0 + self.energy_available / 100 * 20
                features["cardio.orthostatic_tolerance"] = 10.0 + (self.biological_age - 20) * 0.5
                features["cardio.reperfusion_injury"] = 5.0 * self.hormones.cortisol
                features["cardio.circadian_bp"] = 15.0 - self.hormones.cortisol * 5
                
            elif system == OrganSystem.RESPIRATORY:
                features["resp.tidal_volume"] = 500.0 * organ.efficiency
                features["resp.fev1"] = organ.markers.get("fev1", 95.0) * organ.efficiency
                features["resp.fev1_fvc"] = organ.markers.get("fvc_ratio", 0.8)
                features["resp.dlco"] = 90.0 * organ.efficiency
                features["resp.anatomical_dead_space"] = 150.0 + (self.biological_age - 20) * 1.5
                features["resp.physiological_dead_space"] = 150.0 * organ.efficiency
                features["resp.respiratory_drive"] = 85.0 * organ.efficiency
                features["resp.peripheral_chemo"] = 85.0 * organ.efficiency
                features["resp.lung_compliance"] = organ.markers.get("lung_compliance", 0.8) * 250
                features["resp.airway_resistance"] = 1.5 / (organ.efficiency + 0.1)
                features["resp.mucociliary"] = 5.0 * self.organs[OrganSystem.RESPIRATORY].efficiency
                features["resp.surfactant"] = 90.0 * self.organs[OrganSystem.RESPIRATORY].efficiency
                features["resp.pulmonary_htn"] = 20.0 + self.hormones.cortisol * 10
                features["resp.intrapleural_pressure"] = -7.0
                features["resp.work_of_breathing"] = 1.0 + (1 - organ.efficiency) * 2
                features["resp.hypoxic_vaso"] = 85.0 * self.organs[OrganSystem.RESPIRATORY].efficiency
                features["resp.hypercapnic_response"] = 100.0 * self.organs[OrganSystem.RESPIRATORY].efficiency
                features["resp.ahi"] = 2.0 + self.sleep_debt / 10
                features["resp.dyspnea_threshold"] = 80.0 - self.energy_available / 100 * 30
                features["resp.pulmonary_fibrosis"] = 5.0 + (self.biological_age - 50) * 0.1
                
            elif system == OrganSystem.GASTROINTESTINAL:
                features["gi.gastric_emptying"] = organ.markers.get("gastric_emptying", 1.0) * 80
                features["gi.gastric_acid"] = 2.0
                features["gi.intestinal_permeability"] = organ.markers.get("intestinal_permeability", 0.1)
                features["gi.sibo"] = self.microbiome.dysbiosis_level * 10
                features["gi.microbiome_alpha"] = self.microbiome.diversity_index * 6
                features["gi.microbiome_beta"] = 0.25
                features["gi.scfa"] = self.microbiome.short_chain_fatty_acids * 100
                features["gi.bile_acid_pool"] = organ.markers.get("bile_acid_pool", 1.0) * 3.5
                features["gi.enterohepatic"] = 95.0 * organ.efficiency
                features["gi.pancreatic_exocrine"] = 85.0 * organ.efficiency
                features["gi.liver_enzymes"] = 25.0
                features["gi.albumin"] = 42.0
                features["gi.bilirubin"] = 0.5
                features["gi.urea_cycle"] = 100.0 * organ.efficiency
                features["gi.colonic_transit"] = 48.0
                features["gi.water_absorption"] = 95.0 * organ.efficiency
                features["gi.nutrient_surface"] = 250.0 * organ.efficiency
                features["gi.bmr"] = 1600.0
                features["gi.thermic_food"] = 20.0
                features["gi.adaptive_thermogenesis"] = 100.0 * organ.efficiency
                if self.blood_glucose > 0:
                    features["gi.insulin_sensitivity"] = self.blood_glucose_insulin
                else:
                    features["gi.insulin_sensitivity"] = 1.0
                features["gi.glucagon"] = 75.0
                features["gi.ketone_production"] = 0.3 + self.blood_glucose / 100
                features["gi.glycogen_storage"] = self.glycogen_stores
                features["gi.lipolysis_rate"] = 75.0 + (1 - self.blood_glucose_insulin) * 20
                
            elif system == OrganSystem.RENAL:
                features["renal.gfr"] = organ.markers.get("gfr", 90.0) * organ.efficiency
                features["renal.tubular_reabsorption"] = 98.5 * organ.efficiency
                features["renal.ras_activation"] = 25.0
                features["renal.aldosterone"] = 10.0
                features["renal.adh_sensitivity"] = 85.0 * organ.efficiency
                features["renal.diurnal_variation"] = 1.0
                features["renal.concentrating_ability"] = 600.0 * organ.efficiency
                features["renal.proteinuria"] = 0.1
                features["renal.nephron_loss"] = max(0, (self.biological_age - 40) * 0.5)
                features["renal.acid_base"] = organ.markers.get("acid_base", 0.5) * 200
                features["renal.potassium"] = 4.2
                features["renal.phosphate"] = 3.5
                features["renal.uric_acid"] = 7.0
                features["renal.creatinine_generation"] = 20.0
                features["renal.bladder_compliance"] = 35.0
                
            elif system == OrganSystem.MUSCULOSKELETAL:
                features["msk.bmd"] = organ.markers.get("bone_density", 1.0) - 1
                features["msk.cortical_trabecular"] = 2.0
                features["msk.sarcomere_length"] = 2.2
                features["msk.motor_unit"] = 300.0 * organ.efficiency
                features["msk.fiber_type"] = 50.0
                features["msk.tendon_stiffness"] = organ.markers.get("tendon_stiffness", 0.8) * 500
                features["msk.cartilage_thickness"] = organ.markers.get("cartilage_health", 1.0) * 2
                features["msk.synovial_viscosity"] = 0.5
                features["msk.ligamentous_laxity"] = 5.0 + (self.biological_age - 30) * 0.15
                features["msk.compartment_pressure"] = 15.0
                features["msk.fracture_healing"] = organ.markers.get("fracture_healing", 1.0) * 100
                features["msk.bone_remodeling"] = 25.0
                features["msk.lordosis"] = 35.0 + (self.biological_age - 40) * 0.2
                features["msk.kyphosis"] = 30.0 + (self.biological_age - 40) * 0.2
                features["msk.gait_asymmetry"] = 2.0
                features["msk.proprioception"] = 85.0 - (self.biological_age - 20) * 0.3
                features["msk.balance_strategy"] = 2.0
                features["msk.sarcopenia"] = max(0, (self.biological_age - 60) * 0.2)
                features["msk.dynapenia"] = 5.0 + (self.biological_age - 50) * 0.3
                features["msk.fascial_tension"] = 50.0
                
            elif system == OrganSystem.INTEGUMENTARY:
                features["skin.tewl"] = 10.0 + self.microbiome.dysbiosis_level * 10
                features["skin.stratum_hydration"] = organ.markers.get("barrier_integrity", 1.0) * 60
                features["skin.melanin_index"] = organ.markers.get("melanin", 0.5) * 60
                features["skin.collagen"] = organ.markers.get("skin_elasticity", 0.8) * 100
                features["skin.elastin"] = 10.0 + (self.biological_age - 30) * 0.5
                features["skin.sebum"] = 2.5
                features["skin.wound_tensile"] = organ.markers.get("wound_healing", 1.0) * 100
                features["skin.angiogenesis"] = 80.0 * organ.efficiency
                features["skin.keloid"] = 0.0
                features["skin.pressure_ulcer"] = 0.0
                features["skin.uv_damage"] = min(100, (self.biological_age - 20) * 1)
                features["skin.vitamin_d"] = 40.0
                features["skin.thermoreg_sweat"] = organ.markers.get("thermoregulation", 0.9) * 500
                features["skin.eccrine_apocrine"] = 70.0
                features["skin.hair_cycle"] = 85.0
                features["skin.nail_growth"] = 3.0
                features["skin.meissner"] = 20.0
                features["skin.pacinian"] = 85.0
                features["skin.free_nerve"] = 300.0
                features["skin.ruffini"] = 85.0
                
            elif system == OrganSystem.IMMUNE:
                features["immune.igg"] = organ.markers.get("igG", 1.0) * 1000
                features["immune.igm"] = organ.markers.get("igM", 1.0) * 100
                features["immune.iga"] = organ.markers.get("igA", 1.0) * 200
                features["immune.tcell_diversity"] = organ.markers.get("t_cell_diversity", 0.9) * 100
                features["immune.cd4_cd8"] = organ.markers.get("t_cell_diversity", 0.9) * 2.2
                features["immune.nk_cell"] = organ.markers.get("nk_cell_activity", 0.8) * 100
                features["immune.complement"] = organ.markers.get("complement", 1.0) * 200
                features["immune.cytokine_profile"] = organ.markers.get("inflammatory_markers", 0.1) * 100
                features["immune.inflammasome"] = organ.markers.get("inflammatory_markers", 0.1) * 100
                features["immune.mast_cell"] = 10.0
                features["immune.histamine"] = 5.0
                features["immune.autoantibody"] = 0.0
                features["immune.vaccine_response"] = 100.0 * organ.efficiency
                features["immune.gvhd"] = 5.0
                features["immune.tolerance"] = 85.0 * organ.efficiency
                features["immune.mhc"] = 3.0
                features["immune.net_formation"] = 10.0
                features["immune.macrophage"] = 30.0
                features["immune.dendritic"] = 70.0 * organ.efficiency
                features["immune.bcell_maturation"] = 80.0 * organ.efficiency
                features["immune.treg"] = 100.0 * organ.efficiency
                features["immune.thymic_involution"] = min(100, (self.biological_age - 20) * 1)
                features["immune.memory_decay"] = 10.0 + (self.biological_age - 30) * 0.3
                features["immune.trained_immunity"] = 0.5
                features["immune.barrier"] = 85.0 * organ.efficiency
                
            elif system == OrganSystem.ENDOCRINE:
                features["endo.crh_pulse"] = 1.0 + self.hormones.cortisol * 0.5
                features["endo.acth_rhythm"] = 40.0 * (1 + (1 - self.hormones.cortisol) * 0.5)
                features["endo.cortisol_awakening"] = 100.0 * (1 - self.hormones.cortisol * 0.2)
                features["endo.cortisol_slope"] = 40.0 * (1 - self.hormones.cortisol * 0.3)
                features["endo.tsh"] = 2.0
                features["endo.free_t3_t4"] = self.hormones.thyroid_t3 * 0.3
                features["endo.reverse_t3"] = 25.0 + self.hormones.cortisol * 20
                features["endo.insulin_pulsatility"] = self.blood_glucose_insulin * 100
                features["endo.c_peptide"] = 1.2 * self.blood_glucose_insulin
                features["endo.glp1"] = 15.0
                features["endo.gh_pulsatility"] = 1.5
                features["endo.igf1"] = 250.0
                features["endo.shbg"] = 40.0
                features["endo.testosterone_diurnal"] = 20.0
                features["endo.estradiol_cycle"] = 150.0
                features["endo.progesterone"] = 5.0
                features["endo.prolactin"] = 12.0
                features["endo.pth"] = 35.0
                features["endo.calcitonin"] = 5.0
                features["endo.aldosterone_renin"] = 15.0
                features["endo.melatonin"] = 30.0
                features["endo.leptin"] = 15.0 + self.adipose_tissue / 500
                features["endo.ghrelin"] = 100.0 + self.hunger_signal * 50
                features["endo.oxytocin"] = self.hormones.oxytocin * 30
                features["endo.vasopressin"] = 2.0
        
        return features