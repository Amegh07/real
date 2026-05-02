"""
Ontology primitives for the reality simulator.

This package defines the high-level dimensional model that lets the
simulation grow via generated feature families instead of disconnected
booleans and one-off stats.

Feature Sections:
- biological_features.py: Section A (175 features) - Biological & Physiological
- extended_features.py: Sections G-R (340 features) - Climate, Technology, Warfare, etc.
- cognitive_features.py: Section B (50 features) - Brain Structure & Cognitive Modules
- psychological_features.py: Section C (50 features) - Emotional States & Personality
- social_features.py: Section D (65 features) - Kinship, Romantic, Professional
- economic_features.py: Section E (60 features) - Assets, Markets, Banking
- political_features.py: Section F (60 features) - State Formation, Democracy, International
- remaining_features.py: Sections S-AY (~300 features) - Demographics, Crime, Education, etc.

Total: ~1100 features across 30+ domains
"""

from .dimensions import (
    FEATURE_SPEC_TEMPLATE,
    MASTER_DIMENSIONS,
    build_agent_dimension_state,
    build_world_dimension_state,
    get_master_dimensions_snapshot,
)
from .feature_registry import FeatureRegistry, FeatureSpec
from .biological_features import (
    BIOLOGICAL_FEATURES,
    BioFeature,
    BioSystem,
    get_bio_feature,
    get_features_by_system,
    get_all_feature_ids,
    get_feature_count,
    get_feature_snapshot,
)

try:
    from .cognitive_features import (
        COGNITIVE_FEATURES,
        CognitiveFeature,
        CognitiveSystem,
        get_cognitive_feature,
        get_all_cognitive_feature_ids,
        get_cognitive_feature_count,
    )
except ImportError:
    COGNITIVE_FEATURES = {}
    CognitiveFeature = None
    CognitiveSystem = None
    get_cognitive_feature = None
    get_all_cognitive_feature_ids = lambda: []
    get_cognitive_feature_count = lambda: 0

try:
    from .psychological_features import (
        PSYCHOLOGICAL_FEATURES,
        PsychologicalFeature,
        PsychologicalSystem,
        get_psychological_feature,
        get_all_psychological_feature_ids,
        get_psychological_feature_count,
    )
except ImportError:
    PSYCHOLOGICAL_FEATURES = {}
    PsychologicalFeature = None
    PsychologicalSystem = None
    get_psychological_feature = None
    get_all_psychological_feature_ids = lambda: []
    get_psychological_feature_count = lambda: 0

try:
    from .social_features import (
        SOCIAL_FEATURES,
        SocialFeature,
        SocialSystem,
        get_social_feature,
        get_all_social_feature_ids,
        get_social_feature_count,
    )
except ImportError:
    SOCIAL_FEATURES = {}
    SocialFeature = None
    SocialSystem = None
    get_social_feature = None
    get_all_social_feature_ids = lambda: []
    get_social_feature_count = lambda: 0

try:
    from .economic_features import (
        ECONOMIC_FEATURES,
        EconomicFeature,
        EconomicSystem,
        get_economic_feature,
        get_all_economic_feature_ids,
        get_economic_feature_count,
    )
except ImportError:
    ECONOMIC_FEATURES = {}
    EconomicFeature = None
    EconomicSystem = None
    get_economic_feature = None
    get_all_economic_feature_ids = lambda: []
    get_economic_feature_count = lambda: 0

try:
    from .political_features import (
        POLITICAL_FEATURES,
        PoliticalFeature,
        PoliticalSystem,
        get_political_feature,
        get_all_political_feature_ids,
        get_political_feature_count,
    )
except ImportError:
    POLITICAL_FEATURES = {}
    PoliticalFeature = None
    PoliticalSystem = None
    get_political_feature = None
    get_all_political_feature_ids = lambda: []
    get_political_feature_count = lambda: 0

try:
    from .remaining_features import (
        REMAINING_FEATURES,
        RemainingFeature,
        RemainingSystem,
        get_remaining_feature,
        get_all_remaining_feature_ids,
        get_remaining_feature_count,
    )
except ImportError:
    REMAINING_FEATURES = {}
    RemainingFeature = None
    RemainingSystem = None
    get_remaining_feature = None
    get_all_remaining_feature_ids = lambda: []
    get_remaining_feature_count = lambda: 0

try:
    from .complete_features import (
        FINAL_FEATURES,
        FinalFeature,
        FinalSystem,
        get_final_feature,
        get_final_feature_count,
        get_total_all_features,
    )
except ImportError:
    FINAL_FEATURES = {}
    FinalFeature = None
    FinalSystem = None
    get_final_feature = None
    get_final_feature_count = lambda: 0
    get_total_all_features = lambda: 0

try:
    from .missing_features import (
        MISSING_FEATURES,
        MissingFeature,
        MissingSystem,
        get_missing_feature,
        get_all_missing_feature_ids,
        get_missing_feature_count,
    )
except ImportError:
    MISSING_FEATURES = {}
    MissingFeature = None
    MissingSystem = None
    get_missing_feature = None
    get_all_missing_feature_ids = lambda: []
    get_missing_feature_count = lambda: 0

try:
    from .additional_missing_features import (
        ADDITIONAL_FEATURES,
        AdditionalFeature,
        AdditionalSystem,
        get_additional_feature,
        get_all_additional_feature_ids,
        get_additional_feature_count,
    )
except ImportError:
    ADDITIONAL_FEATURES = {}
    AdditionalFeature = None
    AdditionalSystem = None
    get_additional_feature = None
    get_all_additional_feature_ids = lambda: []
    get_additional_feature_count = lambda: 0

try:
    from .extended_features import EXTENDED_FEATURES
    _EXTENDED_COUNT = len(EXTENDED_FEATURES) if EXTENDED_FEATURES else 0
except ImportError:
    EXTENDED_FEATURES = {}
    _EXTENDED_COUNT = 0


def get_total_feature_count() -> int:
    """Get total count of all registered features across all modules."""
    total = 0
    try:
        total += get_feature_count()
    except Exception:
        pass
    try:
        total += get_cognitive_feature_count()
    except Exception:
        pass
    try:
        total += get_psychological_feature_count()
    except Exception:
        pass
    try:
        total += get_social_feature_count()
    except Exception:
        pass
    try:
        total += get_economic_feature_count()
    except Exception:
        pass
    try:
        total += get_political_feature_count()
    except Exception:
        pass
    try:
        total += get_remaining_feature_count()
    except Exception:
        pass
    try:
        total += get_final_feature_count()
    except Exception:
        pass
    try:
        total += get_missing_feature_count()
    except Exception:
        pass
    try:
        total += get_additional_feature_count()
    except Exception:
        pass
    total += _EXTENDED_COUNT
    return total


__all__ = [
    "FEATURE_SPEC_TEMPLATE",
    "FeatureRegistry",
    "FeatureSpec",
    "MASTER_DIMENSIONS",
    "build_agent_dimension_state",
    "build_world_dimension_state",
    "get_master_dimensions_snapshot",
    "BIOLOGICAL_FEATURES",
    "BioFeature",
    "BioSystem",
    "get_bio_feature",
    "get_features_by_system",
    "get_all_feature_ids",
    "get_feature_count",
    "get_feature_snapshot",
    "EXTENDED_FEATURES",
    "COGNITIVE_FEATURES",
    "CognitiveFeature",
    "CognitiveSystem",
    "get_cognitive_feature",
    "get_all_cognitive_feature_ids",
    "get_cognitive_feature_count",
    "PSYCHOLOGICAL_FEATURES",
    "PsychologicalFeature",
    "PsychologicalSystem",
    "get_psychological_feature",
    "get_all_psychological_feature_ids",
    "get_psychological_feature_count",
    "SOCIAL_FEATURES",
    "SocialFeature",
    "SocialSystem",
    "get_social_feature",
    "get_all_social_feature_ids",
    "get_social_feature_count",
    "ECONOMIC_FEATURES",
    "EconomicFeature",
    "EconomicSystem",
    "get_economic_feature",
    "get_all_economic_feature_ids",
    "get_economic_feature_count",
    "POLITICAL_FEATURES",
    "PoliticalFeature",
    "PoliticalSystem",
    "get_political_feature",
    "get_all_political_feature_ids",
    "get_political_feature_count",
    "REMAINING_FEATURES",
    "RemainingFeature",
    "RemainingSystem",
    "get_remaining_feature",
    "get_all_remaining_feature_ids",
    "get_remaining_feature_count",
    "FINAL_FEATURES",
    "FinalFeature",
    "FinalSystem",
    "get_final_feature",
    "get_final_feature_count",
    "get_total_all_features",
    "MISSING_FEATURES",
    "MissingFeature",
    "MissingSystem",
    "get_missing_feature",
    "get_all_missing_feature_ids",
    "get_missing_feature_count",
    "ADDITIONAL_FEATURES",
    "AdditionalFeature",
    "AdditionalSystem",
    "get_additional_feature",
    "get_all_additional_feature_ids",
    "get_additional_feature_count",
    "get_total_feature_count",
]
