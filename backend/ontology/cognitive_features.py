"""
Cognitive Feature Registry — Sections B1 & B2
============================================
Features 176-225 covering:
- B1: Brain Structure & Function (20 features)
- B2: Cognitive Modules (30 features)

Total: 50 cognitive features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class CognitiveSystem(Enum):
    BRAIN_STRUCTURE = auto()
    COGNITIVE_MODULES = auto()


@dataclass
class CognitiveFeature:
    feature_id: str
    feature_name: str
    system: CognitiveSystem
    normal_range: tuple
    unit: str
    description: str
    calculation: str
    tags: List[str] = field(default_factory=list)


COGNITIVE_FEATURES: dict = {}


def _register_cognitive_features():
    global COGNITIVE_FEATURES
    
    features = [
        # ============ B1. BRAIN STRUCTURE & FUNCTION (20 features) ============
        CognitiveFeature("brain.cortical_thickness", "Cortical Thickness", CognitiveSystem.BRAIN_STRUCTURE,
                         (2.5, 4.5), "mm", "Gray matter measure - declines with age",
                         "MRI measurement"),
        CognitiveFeature("brain.hippocampal_volume", "Hippocampal Volume", CognitiveSystem.BRAIN_STRUCTURE,
                         (3000, 4500), "mm³", "Memory formation center - PTSD/depression cause atrophy",
                         "MRI volumetric analysis"),
        CognitiveFeature("brain.amygdala_reactivity", "Amygdala Reactivity", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Threat detection - hyperactive in anxiety",
                         "fMRI BOLD response"),
        CognitiveFeature("brain.prefrontal_maturity", "Prefrontal Cortex Maturation", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Last region to mature at age 25 - adolescent impulsivity",
                         "MRI structural"),
        CognitiveFeature("brain.white_matter_fa", "White Matter Integrity (FA)", CognitiveSystem.BRAIN_STRUCTURE,
                         (0.4, 0.8), "ratio", "Fractional anisotropy - declines with hypertension",
                         "DTI tractography"),
        CognitiveFeature("brain.myelination_status", "Myelination Status", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Saltatory conduction speed - MS causes demyelination",
                         "MRI myelin water"),
        CognitiveFeature("brain.synaptic_density", "Synaptic Density", CognitiveSystem.BRAIN_STRUCTURE,
                         (10, 100), "%", "Connections per neuron - highest in childhood",
                         "Microscopy or PET"),
        CognitiveFeature("brain.neurotransmitter_turnover", "Neurotransmitter Turnover", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "5-HIAA, HVA, MHPG in CSF",
                         "CSF analysis"),
        CognitiveFeature("brain.bbb_permeability", "Blood-Brain Barrier Permeability", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 10), "Ktrans", "Tight junction integrity - inflammation increases",
                         "Dynamic contrast MRI"),
        CognitiveFeature("brain.cerebral_autoreg", "Cerebral Blood Flow Autoregulation", CognitiveSystem.BRAIN_STRUCTURE,
                         (50, 150), "mmHg", "Constant perfusion despite pressure changes",
                         "Transcranial Doppler"),
        CognitiveFeature("brain.glymphatic_clearance", "Glymphatic Clearance Rate", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Waste removal during sleep - impaired in Alzheimer's",
                         "Dynamic PET"),
        CognitiveFeature("brain.bdnf_level", "BDNF Level", CognitiveSystem.BRAIN_STRUCTURE,
                         (10, 50), "ng/mL", "Neuroplasticity promoter - exercise increases",
                         "Blood or CSF assay"),
        CognitiveFeature("brain.default_mode_connectivity", "Default Mode Network Connectivity", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 1), "r", "Resting-state network - overactive in depression",
                         "fMRI correlation"),
        CognitiveFeature("brain.salience_network", "Salience Network Switching", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Internal/external attention toggle",
                         "fMRI activation"),
        CognitiveFeature("brain.central_executive_load", "Central Executive Network Load", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Working memory and goal maintenance capacity",
                         "fMRI load parametric"),
        CognitiveFeature("brain.cerebellar_function", "Cerebellar Function", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Motor coordination and cognitive timing",
                         "Behavioral and fMRI"),
        CognitiveFeature("brain.brainstem_vital", "Brainstem Vital Functions", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Respiratory and cardiac centers",
                         "Clinical assessment"),
        CognitiveFeature("brain.thalamic_gating", "Thalamic Gating", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Sensory relay filtering",
                         "EEG and fMRI"),
        CognitiveFeature("brain.hypothalamic_integration", "Hypothalamic Integration", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Homeostatic hub - connects nervous and endocrine",
                         "Endocrine correlation"),
        CognitiveFeature("brain.pineal_calcification", "Pineal Gland Calcification", CognitiveSystem.BRAIN_STRUCTURE,
                         (0, 100), "%", "Melatonin production decline with age",
                         "CT imaging"),

        # ============ B2. COGNITIVE MODULES (30 features) ============
        CognitiveFeature("cog.sustained_attention", "Sustained Attention (Vigilance)", CognitiveSystem.COGNITIVE_MODULES,
                         (70, 100), "%", "Maintaining focus over time - decrement after 30 min",
                         "Continuous attention task"),
        CognitiveFeature("cog.selective_attention", "Selective Attention", CognitiveSystem.COGNITIVE_MODULES,
                         (70, 100), "%", "Filtering irrelevant stimuli",
                         "Visual search task"),
        CognitiveFeature("cog.divided_attention", "Divided Attention", CognitiveSystem.COGNITIVE_MODULES,
                         (60, 100), "%", "Parallel processing - degrades when overloaded",
                         "Dual task paradigm"),
        CognitiveFeature("cog.task_switch_cost", "Task-Switching Cost", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 500), "ms", "Residual activation of previous task",
                         "Switch cost paradigm"),
        CognitiveFeature("cog.attentional_blink", "Attentional Blink", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Miss second target 200-500ms after first",
                         "RSVP paradigm"),
        CognitiveFeature("cog.change_blindness", "Change Blindness", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Failure to notice large changes",
                         "Flicker task"),
        CognitiveFeature("cog.inattentional_blindness", "Inattentional Blindness", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Missing unexpected events while focused",
                         "Selective attention task"),
        CognitiveFeature("cog.working_memory_span", "Working Memory Span (Verbal)", CognitiveSystem.COGNITIVE_MODULES,
                         (5, 9), "items", "Digit span ~7±2 - chunking expands capacity",
                         "Digit span test"),
        CognitiveFeature("cog.spatial_memory_span", "Working Memory Span (Spatial)", CognitiveSystem.COGNITIVE_MODULES,
                         (4, 7), "items", "Corsi block tapping",
                         "Corsi block test"),
        CognitiveFeature("cog.executive_working_memory", "Working Memory (Executive)", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Manipulation not just storage",
                         "N-back task"),
        CognitiveFeature("cog.chunking_efficiency", "Chunking Efficiency", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Pattern recognition expanding capacity",
                         "Free recall clustering"),
        CognitiveFeature("cog.encoding_specificity", "Encoding Specificity", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 1), "r", "Context-dependent memory",
                         "Context reinstatement"),
        CognitiveFeature("cog.consolidation_speed", "Consolidation Speed", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Transfer to long-term - sleep-dependent",
                         "Recall delay comparison"),
        CognitiveFeature("cog.reconsolidation_window", "Reconsolidation Window", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 6), "hours", "Memories labile on retrieval",
                         "Amnesic agent paradigm"),
        CognitiveFeature("cog.retrieval_forgetting", "Retrieval-Induced Forgetting", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 50), "%", "Recalling items suppresses related ones",
                         "ROP paradigm"),
        CognitiveFeature("cog.proactive_interference", "Proactive Interference", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Old memories disrupt new learning",
                         "PI release paradigm"),
        CognitiveFeature("cog.retroactive_interference", "Retroactive Interference", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "New learning disrupts old memories",
                         "RI paradigm"),
        CognitiveFeature("cog.false_memory", "False Memory Susceptibility", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Semantically related lures falsely recalled",
                         "DRM paradigm"),
        CognitiveFeature("cog.flashbulb_accuracy", "Flashbulb Memory Accuracy", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "High confidence, variable accuracy",
                         "Recall consistency"),
        CognitiveFeature("cog.autobiographical_coherence", "Autobiographical Coherence", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Life story integration",
                         "Narrative analysis"),
        CognitiveFeature("cog.semantic_density", "Semantic Network Density", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Conceptual associations",
                         "Word association test"),
        CognitiveFeature("cog.procedural_automatization", "Procedural Automatization", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Skill without conscious control",
                         "Stroop task facilitation"),
        CognitiveFeature("cog.priming_effect", "Priming Effects", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Unconscious influence of prior exposure",
                         "Lexical decision"),
        CognitiveFeature("cog.metamemory_calibration", "Metamemory Calibration", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 1), "r", "Knowing what you know",
                         "JOL and recall"),
        CognitiveFeature("cog.inhibitory_control", "Inhibitory Control (Go/No-Go)", CognitiveSystem.COGNITIVE_MODULES,
                         (70, 100), "%", "Suppressing prepotent responses",
                         "Go/No-Go task"),
        CognitiveFeature("cog.cognitive_flexibility", "Cognitive Flexibility", CognitiveSystem.COGNITIVE_MODULES,
                         (70, 100), "%", "Shifting between rules",
                         "Wisconsin Card Sort"),
        CognitiveFeature("cog.planning_depth", "Planning Depth", CognitiveSystem.COGNITIVE_MODULES,
                         (1, 10), "moves", "Look-ahead in problem solving",
                         "Tower of Hanoi"),
        CognitiveFeature("cog.perseveration", "Wisconsin Card Sorting Perseveration", CognitiveSystem.COGNITIVE_MODULES,
                         (0, 100), "%", "Continuing wrong rule despite feedback",
                         "WCST errors"),
        CognitiveFeature("cog.verbal_fluency_phonemic", "Verbal Fluency (Phonemic)", CognitiveSystem.COGNITIVE_MODULES,
                         (10, 30), "words/min", "Words beginning with F/A/S",
                         "FAS test"),
        CognitiveFeature("cog.verbal_fluency_semantic", "Verbal Fluency (Semantic)", CognitiveSystem.COGNITIVE_MODULES,
                         (15, 40), "words/min", "Animals in 1 minute",
                         "Category fluency"),
    ]
    
    for f in features:
        COGNITIVE_FEATURES[f.feature_id] = f


_register_cognitive_features()


def get_cognitive_feature(feature_id: str) -> CognitiveFeature:
    return COGNITIVE_FEATURES.get(feature_id)


def get_features_by_cognitive_system(system: CognitiveSystem) -> list:
    return [f for f in COGNITIVE_FEATURES.values() if f.system == system]


def get_all_cognitive_feature_ids() -> list:
    return list(COGNITIVE_FEATURES.keys())


def get_cognitive_feature_count() -> int:
    return len(COGNITIVE_FEATURES)