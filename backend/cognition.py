"""
Cognitive Systems — God-Tier Architecture
================================
Section B2: Cognitive Modules (30 features: 196-225)

Features:
196. Sustained Attention (Vigilance) — Maintaining focus over time; vigilance decrement after 30 minutes
197. Selective Attention — Filtering irrelevant stimuli; cocktail party effect
198. Divided Attention — Parallel processing; driving while talking degrades both
199. Task-Switching Cost — Residual activation of previous task; switch cost 200-500ms
200. Attentional Blink — Miss second target 200-500ms after first
201. Change Blindness — Failure to notice large changes
202. Inattentional Blindness — Missing unexpected events while focused
203. Working Memory Span (Verbal) — Digit span ~7±2; chunking expands capacity
204. Working Memory Span (Spatial) — Corsi block tapping
205. Working Memory (Executive) — Manipulation, not just storage; n-back task
206. Chunking Efficiency — Pattern recognition expanding capacity
207. Encoding Specificity — Context-dependent memory
208. Consolidation Speed — Transfer to long-term; sleep-dependent
209. Reconsolidation Window — Memories become labile on retrieval
210. Retrieval-Induced Forgetting — Recalling suppresses related items
211. Proactive Interference — Old memories disrupt new learning
212. Retroactive Interference — New learning disrupts old memories
213. False Memory Susceptibility — DRM paradigm; semantically related lures
214. Flashbulb Memory Accuracy — Confidence high, accuracy variable
215. Autobiographical Coherence — Life story integration; disrupted in PTSD
216. Semantic Network Density — Conceptual associations
217. Procedural Automatization — Skill without conscious control
218. Priming Effects — Unconscious influence of prior exposure
219. Metamemory Calibration — Knowing what you know
220. Inhibitory Control (Go/No-Go) — Suppressing prepotent responses
221. Cognitive Flexibility — Shifting between rules
222. Planning Depth — Look-ahead in problem solving
223. Wisconsin Card Sorting Perseveration — Continuing wrong rule
224. Verbal Fluency (Phonemic) — Words beginning with F/A/S in 1 minute
225. Verbal Fluency (Semantic) — Animals in 1 minute

Based on spec Section B2: Cognitive Modules
"""

import uuid
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SustainedAttention:
    """
    Sustained Attention / Vigilance (Feature 196).
    Maintaining focus over time; vigilance decrement after 30 minutes.
    """
    vigilance_level: float = 0.9  # 0-1
    decrement_rate: float = 0.001  # per minute
    lapses: int = 0
    response_time_ms: float = 250.0
    
    def apply_time_on_task(self, minutes: float):
        """Vigilance decrement over time."""
        if minutes > 30:
            decay = (minutes - 30) * self.decrement_rate
            self.vigilance_level = max(0.3, self.vigilance_level - decay)
            self.response_time_ms = min(800, self.response_time_ms + decay * 10)
    
    def apply_stimulus_change(self):
        """Novel stimuli restore attention."""
        self.vigilance_level = min(1.0, self.vigilance_level + 0.1)
        self.response_time_ms = max(200, self.response_time_ms - 20)
    
    def get_snapshot(self) -> dict:
        return {
            "vigilance": round(self.vigilance_level, 2),
            "lapses": self.lapses,
            "response_time_ms": round(self.response_time_ms, 0)
        }


@dataclass
class SelectiveAttention:
    """
    Selective Attention (Feature 197).
    Filtering irrelevant stimuli; cocktail party effect.
    """
    filtering_efficiency: float = 0.85
    target_selection_speed: float = 0.8
    distractor_suppression: float = 0.7
    
    def apply_distractor_richness(self, num_distractors: int):
        """More distractors reduce efficiency."""
        if num_distractors > 5:
            decay = (num_distractors - 5) * 0.02
            self.filtering_efficiency = max(0.4, self.filtering_efficiency - decay)
            self.distractor_suppression = max(0.3, self.distractor_suppression - decay * 0.5)
    
    def apply_attentional_cue(self):
        """Valid cue improves selection."""
        self.filtering_efficiency = min(1.0, self.filtering_efficiency + 0.1)
        self.target_selection_speed = min(1.0, self.target_selection_speed + 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "filtering_efficiency": round(self.filtering_efficiency, 2),
            "selection_speed": round(self.target_selection_speed, 2),
            "distractor_suppression": round(self.distractor_suppression, 2)
        }


@dataclass
class DividedAttention:
    """
    Divided Attention (Feature 198).
    Parallel processing; driving while talking degrades both.
    """
    dual_task_cost: float = 0.15  # 15% performance drop
    parallel_efficiency: float = 0.8
    
    def apply_dual_task(self, task_difficulty_1: float, task_difficulty_2: float):
        """Dual task cost."""
        combined_difficulty = (task_difficulty_1 + task_difficulty_2) / 2
        self.dual_task_cost = min(0.5, combined_difficulty * 0.2)
        self.parallel_efficiency = max(0.3, 1.0 - self.dual_task_cost)
    
    def apply_practice(self, practice_rounds: int):
        """Practice reduces dual task cost."""
        self.dual_task_cost = max(0.05, self.dual_task_cost - practice_rounds * 0.01)
        self.parallel_efficiency = min(0.95, self.parallel_efficiency + practice_rounds * 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "dual_task_cost": round(self.dual_task_cost, 2),
            "parallel_efficiency": round(self.parallel_efficiency, 2)
        }


@dataclass
class TaskSwitching:
    """
    Task-Switching Cost (Feature 199).
    Residual activation of previous task; switch cost 200-500ms.
    """
    switch_cost_ms: float = 250.0  # average
    residual_activation: float = 0.3  # 0-1
    flexibility: float = 0.75
    
    def apply_switch(self, similar_tasks: bool):
        """Switching between tasks."""
        if similar_tasks:
            self.switch_cost_ms = min(500, self.switch_cost_ms + 100)
            self.residual_activation = min(0.6, self.residual_activation + 0.2)
        else:
            self.switch_cost_ms = max(150, self.switch_cost_ms - 50)
            self.residual_activation = max(0.1, self.residual_activation - 0.1)
    
    def apply_practice(self):
        """Practice improves flexibility."""
        self.flexibility = min(1.0, self.flexibility + 0.02)
        self.switch_cost_ms = max(150, self.switch_cost_ms - 10)
    
    def get_snapshot(self) -> dict:
        return {
            "switch_cost_ms": round(self.switch_cost_ms, 0),
            "residual_activation": round(self.residual_activation, 2),
            "flexibility": round(self.flexibility, 2)
        }


@dataclass
class AttentionalBlink:
    """
    Attentional Blink (Feature 200).
    Miss second target 200-500ms after first; temporal processing limit.
    """
    blink_duration_ms: float = 300.0
    blink_severity: float = 0.0  # 0-1
    recovery_speed: float = 0.8
    
    def apply_temporal_proximity(self, target_interval_ms: float):
        """Close targets trigger blink."""
        if 200 <= target_interval_ms <= 500:
            self.blink_severity = min(0.8, 0.5 + (500 - target_interval_ms) / 600)
        else:
            self.blink_severity = max(0, self.blink_severity - 0.2)
    
    def apply_recovery(self):
        """Time allows recovery."""
        self.blink_severity = max(0, self.blink_severity - 0.3)
    
    def get_snapshot(self) -> dict:
        return {
            "blink_duration_ms": round(self.blink_duration_ms, 0),
            "blink_severity": round(self.blink_severity, 2),
            "recovery_speed": round(self.recovery_speed, 2)
        }


@dataclass
class ChangeBlindness:
    """
    Change Blindness (Feature 201).
    Failure to notice large changes; demonstrates sparse representation.
    """
    detection_rate: float = 0.6
    change_magnitude_threshold: float = 0.3  # % change needed
    
    def apply_change_size(self, magnitude: float):
        """Larger changes more detectable."""
        if magnitude > self.change_magnitude_threshold:
            self.detection_rate = min(1.0, magnitude * 2)
    
    def get_snapshot(self) -> dict:
        return {
            "detection_rate": round(self.detection_rate, 2),
            "threshold": round(self.change_magnitude_threshold, 2)
        }


@dataclass
class InattentionalBlindness:
    """
    Inattentional Blindness (Feature 202).
    Missing unexpected events while focused; gorilla experiment.
    """
    blindness_rate: float = 0.5  # 50% miss unexpected
    attentional_load: float = 0.0
    
    def apply_load(self, load_level: float):
        """High load increases blindness."""
        self.attentional_load = load_level
        self.blindness_rate = min(0.9, 0.3 + load_level * 0.5)
    
    def get_snapshot(self) -> dict:
        return {
            "blindness_rate": round(self.blindness_rate, 2),
            "attentional_load": round(self.attentional_load, 2)
        }


@dataclass
class WorkingMemoryVerbal:
    """
    Working Memory Span (Verbal) (Feature 203).
    Digit span ~7±2; chunking expands effective capacity.
    """
    span: float = 7.0  # items
    chunking_efficiency: float = 0.7
    encoding_speed: float = 0.8
    
    def apply_chunking(self, pattern_complexity: float):
        """Pattern recognition expands capacity."""
        if pattern_complexity > 0.5:
            self.chunking_efficiency = min(1.0, self.chunking_efficiency + 0.05)
            self.span = min(10, self.span + 0.5)
    
    def apply_load(self, items: int):
        """Load affects performance."""
        if items > self.span:
            decay = (items - self.span) / self.span
            self.encoding_speed = max(0.3, self.encoding_speed - decay * 0.2)
    
    def get_snapshot(self) -> dict:
        return {
            "span": round(self.span, 1),
            "chunking_efficiency": round(self.chunking_efficiency, 2),
            "encoding_speed": round(self.encoding_speed, 2)
        }


@dataclass
class WorkingMemorySpatial:
    """
    Working Memory Span (Spatial) (Feature 204).
    Corsi block tapping; visuospatial sketchpad capacity.
    """
    span: float = 6.0
    spatial_accuracy: float = 0.8
    mental_rotation_speed: float = 0.7
    
    def apply_spatial_practice(self, practice_trials: int):
        """Practice improves spatial WM."""
        if practice_trials > 10:
            self.span = min(9, self.span + practice_trials * 0.01)
            self.spatial_accuracy = min(1.0, self.spatial_accuracy + 0.02)
    
    def apply_load(self, items: int):
        """Load affects spatial accuracy."""
        if items > self.span:
            self.spatial_accuracy = max(0.4, self.spatial_accuracy - 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "span": round(self.span, 1),
            "spatial_accuracy": round(self.spatial_accuracy, 2),
            "mental_rotation": round(self.mental_rotation_speed, 2)
        }


@dataclass
class WorkingMemoryExecutive:
    """
    Working Memory (Executive) (Feature 205).
    Manipulation, not just storage; n-back task measures this.
    """
    n_back_level: int = 2
    manipulation_efficiency: float = 0.75
    updating_speed: float = 0.8
    
    def apply_n_back_task(self, level: int, accuracy: float):
        """N-back training."""
        if accuracy > 0.9 and level > self.n_back_level:
            self.n_back_level = min(4, level)
            self.manipulation_efficiency = min(1.0, self.manipulation_efficiency + 0.05)
    
    def apply_update_load(self):
        """Continuous updating drains resources."""
        self.updating_speed = max(0.4, self.updating_speed - 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "n_back_level": self.n_back_level,
            "manipulation_efficiency": round(self.manipulation_efficiency, 2),
            "updating_speed": round(self.updating_speed, 2)
        }


@dataclass
class ChunkingEfficiency:
    """
    Chunking Efficiency (Feature 206).
    Pattern recognition expanding capacity; expertise effect.
    """
    chunk_size: float = 3.0  # items per chunk
    pattern_recognition_speed: float = 0.7
    expertise_bonus: float = 0.0
    
    def apply_expertise(self, domain_exposure_hours: float):
        """Domain expertise improves chunking."""
        if domain_exposure_hours > 100:
            self.expertise_bonus = min(1.0, domain_exposure_hours / 500)
            self.chunk_size = min(8, 3.0 + self.expertise_bonus * 5)
            self.pattern_recognition_speed = min(1.0, self.pattern_recognition_speed + self.expertise_bonus * 0.3)
    
    def apply_pattern_detection(self):
        """Pattern detection."""
        self.pattern_recognition_speed = min(1.0, self.pattern_recognition_speed + 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "chunk_size": round(self.chunk_size, 1),
            "recognition_speed": round(self.pattern_recognition_speed, 2),
            "expertise_bonus": round(self.expertise_bonus, 2)
        }


@dataclass
class EncodingSpecificity:
    """
    Encoding Specificity (Feature 207).
    Context-dependent memory; underwater learning best recalled underwater.
    """
    context_dependence: float = 0.5  # 0-1
    retrieval_context_match: float = 0.6
    
    def apply_encoding_context(self, context: str):
        """Encode with context."""
        self.context_dependence = min(1.0, self.context_dependence + 0.05)
    
    def apply_retrieval_context(self, original_context: str, current_context: str):
        """Match retrieval context."""
        if original_context == current_context:
            self.retrieval_context_match = min(1.0, self.retrieval_context_match + 0.2)
        else:
            self.retrieval_context_match = max(0.2, self.retrieval_context_match - 0.2)
    
    def get_snapshot(self) -> dict:
        return {
            "context_dependence": round(self.context_dependence, 2),
            "context_match": round(self.retrieval_context_match, 2)
        }


@dataclass
class Consolidation:
    """
    Consolidation Speed (Feature 208).
    Transfer to long-term; sleep-dependent and replay-mediated.
    """
    consolidation_rate: float = 0.5  # per hour
    sleep_enhancement: float = 1.5  # multiplier during SWS
    replay_count: int = 0
    
    def apply_sleep(self, slow_wave_minutes: float, rem_minutes: float):
        """Sleep enhances consolidation."""
        if slow_wave_minutes > 20:
            self.consolidation_rate = min(1.0, slow_wave_minutes / 60 * self.sleep_enhancement)
        if rem_minutes > 30:
            self.replay_count += int(rem_minutes / 10)
    
    def apply_wake_rest(self):
        """Wake rest has low consolidation."""
        self.consolidation_rate = max(0.1, self.consolidation_rate - 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "consolidation_rate": round(self.consolidation_rate, 2),
            "sleep_enhancement": round(self.sleep_enhancement, 1),
            "replay_count": self.replay_count
        }


@dataclass
class Reconsolidation:
    """
    Reconsolidation Window (Feature 209).
    Memories become labile on retrieval; amnesic agents block update.
    """
    lability_duration_minutes: float = 60.0
    reconsolidation_threshold: float = 0.7
    update_success_rate: float = 0.6
    
    def apply_retrieval(self, reminders: int):
        """Retrieval triggers lability."""
        if reminders > 0:
            self.lability_duration_minutes = min(120, 30 + reminders * 20)
    
    def apply_update(self, disruptors_present: bool):
        """Update window."""
        if disruptors_present:
            self.update_success_rate = max(0.2, self.update_success_rate - 0.3)
        else:
            self.update_success_rate = min(0.9, self.update_success_rate + 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "lability_minutes": round(self.lability_duration_minutes, 0),
            "threshold": round(self.reconsolidation_threshold, 2),
            "update_success": round(self.update_success_rate, 2)
        }


@dataclass
class RetrievalInducedForgetting:
    """
    Retrieval-Induced Forgetting (Feature 210).
    Recalling some items suppresses related others.
    """
    suppression_strength: float = 0.4
    retrieval_practice_benefit: float = 0.3
    
    def apply_retrieval_practice(self, practiced_items: int, related_items: int):
        """RIF magnitude."""
        if related_items > 0:
            self.suppression_strength = min(0.7, 0.2 + practiced_items / 20)
    
    def apply_independence_cues(self):
        """Cue-independent retrieval reduces RIF."""
        self.suppression_strength = max(0.1, self.suppression_strength - 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "suppression_strength": round(self.suppression_strength, 2),
            "practice_benefit": round(self.retrieval_practice_benefit, 2)
        }


@dataclass
class ProactiveInterference:
    """
    Proactive Interference (Feature 211).
    Old memories disrupt new learning; release from PI in category shifts.
    """
    interference_strength: float = 0.3
    release_point: float = 0.8  # category shift helps
    
    def apply_old_learning(self, old_item_strength: float):
        """Old items interfere."""
        if old_item_strength > 0.7:
            self.interference_strength = min(0.8, old_item_strength * 0.5)
    
    def apply_category_shift(self):
        """New category releases from PI."""
        self.interference_strength = max(0.1, self.interference_strength - 0.3)
    
    def get_snapshot(self) -> dict:
        return {
            "interference_strength": round(self.interference_strength, 2),
            "release_point": round(self.release_point, 2)
        }


@dataclass
class RetroactiveInterference:
    """
    Retroactive Interference (Feature 212).
    New learning disrupts old memories; similar material worst.
    """
    interference_strength: float = 0.35
    similarity_penalty: float = 0.0
    
    def apply_new_learning(self, similarity: float, new_strength: float):
        """Similar new learning interferes most."""
        self.similarity_penalty = similarity
        self.interference_strength = min(0.8, similarity * new_strength * 0.5)
    
    def apply_spaced_practice(self):
        """Spacing reduces RI."""
        self.interference_strength = max(0.1, self.interference_strength - 0.15)
    
    def get_snapshot(self) -> dict:
        return {
            "interference_strength": round(self.interference_strength, 2),
            "similarity_penalty": round(self.similarity_penalty, 2)
        }


@dataclass
class FalseMemory:
    """
    False Memory Susceptibility (Feature 213).
    DRM paradigm; semantically related lures falsely recalled.
    """
    susceptibility: float = 0.4  # 0-1
    suggestion_impact: float = 0.3
    
    def apply_drm_list(self, list_strength: float, lure_relatedness: float):
        """DRM paradigm."""
        if lure_relatedness > 0.8:
            self.susceptibility = min(0.8, 0.2 + list_strength * 0.3)
    
    def apply_contradiction(self):
        """Contradiction reduces false memory."""
        self.susceptibility = max(0.2, self.susceptibility - 0.15)
    
    def get_snapshot(self) -> dict:
        return {
            "susceptibility": round(self.susceptibility, 2),
            "suggestion_impact": round(self.suggestion_impact, 2)
        }


@dataclass
class FlashbulbMemory:
    """
    Flashbulb Memory Accuracy (Feature 214).
    Confidence high, accuracy variable; 9/11 study showed distortion.
    """
    confidence: float = 0.85
    accuracy: float = 0.5
    detail_retention: float = 0.4
    
    def apply_emotional_event(self, intensity: float):
        """Emotional event."""
        self.confidence = min(1.0, intensity + 0.1)
        self.detail_retention = min(0.8, intensity * 0.6)
    
    def apply_time(self, weeks_elapsed: float):
        """Time degrades accuracy."""
        if weeks_elapsed > 1:
            self.accuracy = max(0.2, self.accuracy - weeks_elapsed * 0.01)
            self.detail_retention = max(0.1, self.detail_retention - weeks_elapsed * 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "confidence": round(self.confidence, 2),
            "accuracy": round(self.accuracy, 2),
            "detail_retention": round(self.detail_retention, 2)
        }


@dataclass
class AutobiographicalMemory:
    """
    Autobiographical Coherence (Feature 215).
    Life story integration; disrupted in PTSD and borderline personality.
    """
    coherence: float = 0.7  # 0-1 narrative coherence
    episodic_detail: float = 0.6
    identity_integration: float = 0.65
    
    def apply_narrative_building(self, events_integrated: int):
        """Narrative construction."""
        if events_integrated > 5:
            self.coherence = min(1.0, self.coherence + events_integrated * 0.02)
            self.identity_integration = min(1.0, self.identity_integration + 0.02)
    
    def apply_trauma(self, trauma_severity: float):
        """Trauma disrupts coherence."""
        if trauma_severity > 0.7:
            self.coherence = max(0.3, self.coherence - trauma_severity * 0.3)
            self.episodic_detail = max(0.2, self.episodic_detail - trauma_severity * 0.2)
    
    def get_snapshot(self) -> dict:
        return {
            "coherence": round(self.coherence, 2),
            "episodic_detail": round(self.episodic_detail, 2),
            "identity_integration": round(self.identity_integration, 2)
        }


@dataclass
class SemanticNetwork:
    """
    Semantic Network Density (Feature 216).
    Conceptual associations; semantic dementia degrades this.
    """
    density: float = 0.75
    retrieval_speed: float = 0.8
    category_fluency: float = 0.8
    
    def apply_category_learning(self, categories_learned: int):
        """Learning categories."""
        if categories_learned > 0:
            self.density = min(1.0, self.density + categories_learned * 0.01)
            self.category_fluency = min(1.0, self.category_fluency + categories_learned * 0.02)
    
    def apply_semantic_dementia(self, temporal_atrophy: float):
        """Temporal lobe degradation."""
        if temporal_atrophy > 0.3:
            self.density = max(0.3, self.density - temporal_atrophy * 0.3)
            self.retrieval_speed = max(0.4, self.retrieval_speed - temporal_atrophy * 0.2)
    
    def get_snapshot(self) -> dict:
        return {
            "density": round(self.density, 2),
            "retrieval_speed": round(self.retrieval_speed, 2),
            "category_fluency": round(self.category_fluency, 2)
        }


@dataclass
class ProceduralMemory:
    """
    Procedural Automatization (Feature 217).
    Skill without conscious control; Stroop task demonstrates.
    """
    automaticity: float = 0.0  # starts untrained
    reaction_time_ms: float = 800.0
    conscious_control: float = 1.0
    
    def apply_practice(self, repetitions: int):
        """Practice automatizes."""
        if repetitions > 0:
            max_auto = min(1.0, repetitions / 100)
            self.automaticity = max(self.automaticity, max_auto)
            self.reaction_time_ms = max(200, self.reaction_time_ms - repetitions * 3)
            self.conscious_control = max(0.1, self.conscious_control - repetitions * 0.01)
    
    def apply_stroop_conflict(self):
        """Stroop shows automatization."""
        if self.automaticity > 0.6:
            self.reaction_time_ms = min(600, self.reaction_time_ms + 50)
    
    def get_snapshot(self) -> dict:
        return {
            "automaticity": round(self.automaticity, 2),
            "reaction_time_ms": round(self.reaction_time_ms, 0),
            "conscious_control": round(self.conscious_control, 2)
        }


@dataclass
class PrimingEffects:
    """
    Priming Effects (Feature 218).
    Unconscious influence of prior exposure; lexical decision speedup.
    """
    priming_strength: float = 0.3  # 0-1
    response_speedup: float = 0.15  # % faster
    conceptual_priming: float = 0.4
    
    def apply_repetition(self, exposures: int):
        """Repetition priming."""
        if exposures > 1:
            self.priming_strength = min(0.7, 0.1 + exposures * 0.05)
            self.response_speedup = min(0.4, exposures * 0.03)
    
    def apply_conceptual(self):
        """Conceptual priming."""
        self.priming_strength = min(0.8, self.priming_strength + 0.1)
    
    def apply_time_delay(self, minutes: float):
        """Priming decays."""
        if minutes > 30:
            decay = (minutes - 30) / 120
            self.priming_strength = max(0.1, self.priming_strength - decay)
    
    def get_snapshot(self) -> dict:
        return {
            "priming_strength": round(self.priming_strength, 2),
            "response_speedup": round(self.response_speedup, 2),
            "conceptual_priming": round(self.conceptual_priming, 2)
        }


@dataclass
class Metamemory:
    """
    Metamemory Calibration (Feature 219).
    Knowing what you know; overconfidence in Dunning-Kruger.
    """
    calibration: float = 0.6  # accuracy of confidence
    overconfidence: float = 0.2  # bias in judgment
    judgment_speed: float = 0.7
    
    def apply_accuracy_check(self, correct: bool, confidence: float):
        """Calibration update."""
        if correct:
            if confidence > 0.8:
                self.overconfidence = min(0.5, self.overconfidence + 0.05)
            else:
                self.overconfidence = max(0, self.overconfidence - 0.02)
        else:
            if confidence > 0.8:
                self.overconfidence = min(0.6, self.overconfidence + 0.15)
            
        self.calibration = max(0.3, 1.0 - self.overconfidence)
    
    def apply_experience(self, accuracy: float):
        """Experience improves calibration."""
        if accuracy > 0.7:
            self.calibration = min(0.9, self.calibration + 0.02)
            self.overconfidence = max(0, self.overconfidence - 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "calibration": round(self.calibration, 2),
            "overconfidence": round(self.overconfidence, 2),
            "judgment_speed": round(self.judgment_speed, 2)
        }


@dataclass
class InhibitoryControl:
    """
    Inhibitory Control (Go/No-Go) (Feature 220).
    Suppressing prepotent responses; right inferior frontal gyrus.
    """
    inhibition_strength: float = 0.75
    response_suppression_speed: float = 0.7
    false_alarm_rate: float = 0.1
    
    def apply_no_go_trial(self, should_inhibit: bool, success: bool):
        """No-Go trials."""
        if should_inhibit and success:
            self.inhibition_strength = min(1.0, self.inhibition_strength + 0.05)
        elif should_inhibit and not success:
            self.false_alarm_rate = min(0.4, self.false_alarm_rate + 0.05)
    
    def apply_fatigue(self):
        """Fatigue impairs inhibition."""
        self.inhibition_strength = max(0.3, self.inhibition_strength - 0.05)
        self.response_suppression_speed = max(0.4, self.response_suppression_speed - 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "inhibition_strength": round(self.inhibition_strength, 2),
            "suppression_speed": round(self.response_suppression_speed, 2),
            "false_alarm_rate": round(self.false_alarm_rate, 2)
        }


@dataclass
class CognitiveFlexibility:
    """
    Cognitive Flexibility (Feature 221).
    Shifting between rules; Wisconsin Card Sorting Test.
    """
    flexibility: float = 0.75
    set_shifting_speed: float = 0.7
    perseveration_tendency: float = 0.2
    
    def apply_rule_shift(self, feedback_conflict: bool):
        """Feedback-driven shifting."""
        if feedback_conflict:
            self.set_shifting_speed = min(1.0, self.set_shifting_speed + 0.1)
            self.perseveration_tendency = max(0.05, self.perseveration_tendency - 0.05)
        else:
            self.perseveration_tendency = min(0.5, self.perseveration_tendency + 0.05)
    
    def apply_wcst_practice(self, correct_shifts: int):
        """WCST practice."""
        if correct_shifts > 3:
            self.flexibility = min(1.0, self.flexibility + correct_shifts * 0.02)
    
    def get_snapshot(self) -> dict:
        return {
            "flexibility": round(self.flexibility, 2),
            "shifting_speed": round(self.set_shifting_speed, 2),
            "perseveration": round(self.perseveration_tendency, 2)
        }


@dataclass
class PlanningDepth:
    """
    Planning Depth (Feature 222).
    Look-ahead in problem solving; Tower of Hanoi and chess.
    """
    depth: int = 3  # moves ahead
    plan_accuracy: float = 0.6
    subgoal_creation: float = 0.7
    
    def apply_problem_solving(self, problem_complexity: float):
        """Problem complexity affects depth."""
        max_depth = int(problem_complexity * 5) + 1
        self.depth = min(max_depth, self.depth + 1)
        if self.plan_accuracy > 0.5:
            self.plan_accuracy = min(0.9, self.plan_accuracy + 0.02)
    
    def apply_failure(self):
        """Failed plan reduces depth."""
        self.depth = max(1, self.depth - 1)
        self.plan_accuracy = max(0.3, self.plan_accuracy - 0.1)
    
    def get_snapshot(self) -> dict:
        return {
            "depth": self.depth,
            "plan_accuracy": round(self.plan_accuracy, 2),
            "subgoal_creation": round(self.subgoal_creation, 2)
        }


@dataclass
class WCS_Perseveration:
    """
    Wisconsin Card Sorting Perseveration (Feature 223).
    Continuing wrong rule despite feedback; frontal lobe marker.
    """
    perseveration_score: float = 0.15  # low = good
    feedback_utilization: float = 0.8
    
    def apply_feedback(self, feedback_conflict: bool, correct_response: bool):
        """Feedback processing."""
        if feedback_conflict and not correct_response:
            self.perseveration_score = min(0.6, self.perseveration_score + 0.1)
            self.feedback_utilization = max(0.4, self.feedback_utilization - 0.1)
        elif feedback_conflict and correct_response:
            self.perseveration_score = max(0.05, self.perseveration_score - 0.05)
    
    def apply_correct(self):
        """Correct use of feedback."""
        self.feedback_utilization = min(1.0, self.feedback_utilization + 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "perseveration_score": round(self.perseveration_score, 2),
            "feedback_utilization": round(self.feedback_utilization, 2)
        }


@dataclass
class VerbalFluencyPhonemic:
    """
    Verbal Fluency (Phonemic) (Feature 224).
    Words beginning with F/A/S in 1 minute; left frontal function.
    """
    words_per_minute: int = 12
    clustering: float = 0.5
    switching_efficiency: float = 0.6
    
    def apply_timed_generation(self, duration_minutes: float):
        """Timed generation."""
        if duration_minutes > 0.5:
            self.words_per_minute = min(25, self.words_per_minute + int(duration_minutes))
    
    def apply_clustering(self, cluster_size: int):
        """Clustering strategy."""
        self.clustering = min(0.9, 0.3 + cluster_size * 0.1)
    
    def apply_switching(self):
        """Switching strategy."""
        self.switching_efficiency = min(0.9, self.switching_efficiency + 0.05)
    
    def get_snapshot(self) -> dict:
        return {
            "words_per_minute": self.words_per_minute,
            "clustering": round(self.clustering, 2),
            "switching": round(self.switching_efficiency, 2)
        }


@dataclass
class VerbalFluencySemantic:
    """
    Verbal Fluency (Semantic) (Feature 225).
    Animals in 1 minute; temporal lobe and semantic access.
    """
    category_words_per_minute: int = 15
    semantic_clustering: float = 0.6
    subcategory_switching: float = 0.5
    
    def apply_category_generation(self, unique_subcategories: int):
        """Generate within category."""
        if unique_subcategories > 3:
            self.subcategory_switching = min(0.8, 0.4 + unique_subcategories * 0.1)
            self.category_words_per_minute = min(30, self.category_words_per_minute + unique_subcategories)
    
    def apply_temporal_damage(self, atrophy: float):
        """Temporal lobe damage."""
        if atrophy > 0.2:
            self.category_words_per_minute = max(5, self.category_words_per_minute - int(atrophy * 20))
            self.semantic_clustering = max(0.3, self.semantic_clustering - atrophy * 0.3)
    
    def get_snapshot(self) -> dict:
        return {
            "words_per_minute": self.category_words_per_minute,
            "semantic_clustering": round(self.semantic_clustering, 2),
            "subcategory_switching": round(self.subcategory_switching, 2)
        }


@dataclass
class CognitionModel:
    """
    Complete Cognitive Model.
    Integrates all cognitive module features.
    """
    # Attention systems
    sustained_attention: SustainedAttention = field(default_factory=SustainedAttention)
    selective_attention: SelectiveAttention = field(default_factory=SelectiveAttention)
    divided_attention: DividedAttention = field(default_factory=DividedAttention)
    task_switching: TaskSwitching = field(default_factory=TaskSwitching)
    attentional_blink: AttentionalBlink = field(default_factory=AttentionalBlink)
    change_blindness: ChangeBlindness = field(default_factory=ChangeBlindness)
    inattentional_blindness: InattentionalBlindness = field(default_factory=InattentionalBlindness)
    
    # Working memory
    wm_verbal: WorkingMemoryVerbal = field(default_factory=WorkingMemoryVerbal)
    wm_spatial: WorkingMemorySpatial = field(default_factory=WorkingMemorySpatial)
    wm_executive: WorkingMemoryExecutive = field(default_factory=WorkingMemoryExecutive)
    chunking: ChunkingEfficiency = field(default_factory=ChunkingEfficiency)
    
    # Memory processes
    encoding_specificity: EncodingSpecificity = field(default_factory=EncodingSpecificity)
    consolidation: Consolidation = field(default_factory=Consolidation)
    reconsolidation: Reconsolidation = field(default_factory=Reconsolidation)
    retrieval_forgetting: RetrievalInducedForgetting = field(default_factory=RetrievalInducedForgetting)
    proactive_interference: ProactiveInterference = field(default_factory=ProactiveInterference)
    retroactive_interference: RetroactiveInterference = field(default_factory=RetroactiveInterference)
    false_memory: FalseMemory = field(default_factory=FalseMemory)
    flashbulb_memory: FlashbulbMemory = field(default_factory=FlashbulbMemory)
    autobiographical: AutobiographicalMemory = field(default_factory=AutobiographicalMemory)
    semantic_network: SemanticNetwork = field(default_factory=SemanticNetwork)
    
    # Procedural & priming
    procedural: ProceduralMemory = field(default_factory=ProceduralMemory)
    priming: PrimingEffects = field(default_factory=PrimingEffects)
    
    # Metacognition
    metamemory: Metamemory = field(default_factory=Metamemory)
    inhibitory_control: InhibitoryControl = field(default_factory=InhibitoryControl)
    cognitive_flexibility: CognitiveFlexibility = field(default_factory=CognitiveFlexibility)
    
    # Executive function
    planning_depth: PlanningDepth = field(default_factory=PlanningDepth)
    wcst_perseveration: WCS_Perseveration = field(default_factory=WCS_Perseveration)
    verbal_fluency_phonemic: VerbalFluencyPhonemic = field(default_factory=VerbalFluencyPhonemic)
    verbal_fluency_semantic: VerbalFluencySemantic = field(default_factory=VerbalFluencySemantic)
    
    def tick(
        self,
        activity: str = "idle",
        stress_level: float = 0.0,
        sleep_hours: float = 7.0,
        fatigue: float = 0.0,
        age_years: float = 25.0,
        practice_repetitions: int = 0,
        domain_exposure_hours: float = 0.0
    ):
        """Update all cognitive systems each tick."""
        # Activity-based updates
        if activity == "work":
            self.wm_verbal.apply_load(5)
            self.wm_verbal.apply_chunking(0.6)
            self.sustained_attention.apply_time_on_task(8)  # minutes
            self.divided_attention.apply_dual_task(0.5, 0.3)
        
        elif activity == "study":
            self.consolidation.apply_sleep(sleep_hours * 0.5, sleep_hours * 0.2)
            self.chunking.apply_expertise(domain_exposure_hours)
            self.semantic_network.apply_category_learning(2)
            self.priming.apply_repetition(3)
            self.planning_depth.apply_problem_solving(0.6)
        
        elif activity == "socialize":
            self.inhibitory_control.apply_fatigue()
            self.wcst_perseveration.apply_correct()
        
        elif activity == "sleep":
            self.consolidation.apply_sleep(sleep_hours, sleep_hours * 0.25)
        
        elif activity == "idle":
            self.sustained_attention.apply_time_on_task(0)
            self.consolidation.apply_wake_rest()
        
        # Age effects
        if age_years > 60:
            decline = (age_years - 60) / 200
            self.sustained_attention.vigilance_level = max(0.4, self.sustained_attention.vigilance_level - decline * 0.1)
            self.wm_verbal.span = max(4, self.wm_verbal.span - decline * 0.5)
            self.wm_spatial.span = max(3, self.wm_spatial.span - decline * 0.3)
            self.wm_executive.manipulation_efficiency = max(0.4, self.wm_executive.manipulation_efficiency - decline * 0.1)
        
        # Practice effects
        if practice_repetitions > 0:
            self.procedural.apply_practice(practice_repetitions)
            self.task_switching.apply_practice()
            self.cognitive_flexibility.apply_wcst_practice(practice_repetitions // 10)
        
        # Stress effects
        if stress_level > 0.6:
            self.sustained_attention.vigilance_level = max(0.3, self.sustained_attention.vigilance_level - stress_level * 0.1)
            self.selective_attention.filtering_efficiency = max(0.4, self.selective_attention.filtering_efficiency - stress_level * 0.15)
            self.cognitive_flexibility.flexibility = max(0.4, self.cognitive_flexibility.flexibility - stress_level * 0.1)
        
        # Fatigue effects
        if fatigue > 0.7:
            self.sustained_attention.lapses += 1
            self.inhibitory_control.apply_fatigue()
            self.metamemory.overconfidence = min(0.6, self.metamemory.overconfidence + 0.05)
    
    def get_snapshot(self) -> dict:
        """Full cognitive state snapshot."""
        return {
            "attention": {
                "sustained": self.sustained_attention.get_snapshot(),
                "selective": self.selective_attention.get_snapshot(),
                "divided": self.divided_attention.get_snapshot(),
                "task_switching": self.task_switching.get_snapshot(),
                "blink": self.attentional_blink.get_snapshot(),
                "change_blindness": self.change_blindness.get_snapshot(),
                "inattentional": self.inattentional_blindness.get_snapshot()
            },
            "working_memory": {
                "verbal": self.wm_verbal.get_snapshot(),
                "spatial": self.wm_spatial.get_snapshot(),
                "executive": self.wm_executive.get_snapshot(),
                "chunking": self.chunking.get_snapshot()
            },
            "memory": {
                "encoding": self.encoding_specificity.get_snapshot(),
                "consolidation": self.consolidation.get_snapshot(),
                "reconsolidation": self.reconsolidation.get_snapshot(),
                "rif": self.retrieval_forgetting.get_snapshot(),
                "pi": self.proactive_interference.get_snapshot(),
                "ri": self.retroactive_interference.get_snapshot(),
                "false_memory": self.false_memory.get_snapshot(),
                "flashbulb": self.flashbulb_memory.get_snapshot(),
                "autobiographical": self.autobiographical.get_snapshot(),
                "semantic": self.semantic_network.get_snapshot()
            },
            "procedural": {
                "automatization": self.procedural.get_snapshot(),
                "priming": self.priming.get_snapshot()
            },
            "metacognition": {
                "metamemory": self.metamemory.get_snapshot(),
                "inhibitory": self.inhibitory_control.get_snapshot(),
                "flexibility": self.cognitive_flexibility.get_snapshot()
            },
            "executive": {
                "planning": self.planning_depth.get_snapshot(),
                "wcst": self.wcst_perseveration.get_snapshot(),
                "phonemic": self.verbal_fluency_phonemic.get_snapshot(),
                "semantic": self.verbal_fluency_semantic.get_snapshot()
            }
        }