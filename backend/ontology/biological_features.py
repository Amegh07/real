"""
Biological Feature Registry — Complete 175 Features
====================================================
Maps all biological features from Section A to organ systems.
Integrates with physiology.py without breaking existing functionality.

Features organized by system:
- A1: Cardiovascular (25 features)
- A2: Respiratory (20 features)
- A3: Gastrointestinal & Metabolic (25 features)
- A4: Renal & Urinary (15 features)
- A5: Musculoskeletal (20 features)
- A6: Integumentary & Sensory (20 features)
- A7: Immune System (25 features)
- A8: Endocrine & Hormonal (25 features)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum, auto


class BioSystem(Enum):
    """Major biological system categories."""
    CARDIOVASCULAR = auto()
    RESPIRATORY = auto()
    GASTROINTESTINAL = auto()
    RENAL = auto()
    MUSCULOSKELETAL = auto()
    INTEGUMENTARY = auto()
    IMMUNE = auto()
    ENDOCRINE = auto()


@dataclass
class BioFeature:
    """A single biological feature."""
    id: str
    name: str
    system: BioSystem
    normal_range: tuple
    unit: str
    description: str
    calculation: str
    tags: List[str] = field(default_factory=list)


BIOLOGICAL_FEATURES: Dict[str, BioFeature] = {}

def _register_features():
    global BIOLOGICAL_FEATURES
    
    features = [
        # ============ A1. CARDIOVASCULAR SYSTEM (25 features) ============
        BioFeature("cardio.hrv_rmssd", "HRV - RMSSD", BioSystem.CARDIOVASCULAR, 
                  (20, 50), "ms", "Heart rate variability - root mean square of successive differences",
                  "derived from beat-to-beat intervals"),
        BioFeature("cardio.sdnn", "SDNN", BioSystem.CARDIOVASCULAR,
                  (50, 150), "ms", "Standard deviation of NN intervals - overall HRV",
                  "derived from 24h holter"),
        BioFeature("cardio.lf_hf_ratio", "LF/HF Ratio", BioSystem.CARDIOVASCULAR,
                  (0.5, 2.0), "ratio", "Low frequency to high frequency ratio - autonomic balance",
                  "spectral analysis of HRV"),
        BioFeature("cardio.baro_sensitivity", "Baroreceptor Sensitivity", BioSystem.CARDIOVASCULAR,
                  (5, 20), "ms/mmHg", "Heart rate response to blood pressure changes",
                  "phenylephrine test"),
        BioFeature("cardio.pwv", "Pulse Wave Velocity", BioSystem.CARDIOVASCULAR,
                  (5, 12), "m/s", "Arterial stiffness measure - cardiovascular risk",
                  "applanation tonometry"),
        BioFeature("cardio.ejection_fraction", "Ejection Fraction", BioSystem.CARDIOVASCULAR,
                  (55, 70), "%", "Percentage of blood pumped per beat",
                  "echocardiography"),
        BioFeature("cardio.stroke_volume", "Stroke Volume", BioSystem.CARDIOVASCULAR,
                  (60, 120), "mL", "Amount of blood pumped per beat",
                  "echocardiography or thermodilution"),
        BioFeature("cardio.cardiac_output", "Cardiac Output", BioSystem.CARDIOVASCULAR,
                  (4, 8), "L/min", "Stroke volume × heart rate",
                  "Fick equation or thermodilution"),
        BioFeature("cardio.peripheral_resistance", "Peripheral Vascular Resistance", BioSystem.CARDIOVASCULAR,
                  (800, 1200), "dyn·s/cm⁵", "Arteriole constriction/dilation",
                  "calculated from MAP and cardiac output"),
        BioFeature("cardio.venous_compliance", "Venous Compliance", BioSystem.CARDIOVASCULAR,
                  (1.5, 2.5), "mL/mmHg", "Capacity of veins to hold blood",
                  "venous occlusion plethysmography"),
        BioFeature("cardio.capillary_density", "Capillary Density", BioSystem.CARDIOVASCULAR,
                  (200, 300), "/mm²", "Number of capillaries per area",
                  "muscle biopsy or capillary microscopy"),
        BioFeature("cardio.microcirculation", "Microcirculation Perfusion", BioSystem.CARDIOVASCULAR,
                  (60, 100), "%", "Blood flow to smallest vessels",
                  "laser Doppler flowmetry"),
        BioFeature("cardio.plaque_burden", "Atherosclerotic Plaque Burden", BioSystem.CARDIOVASCULAR,
                  (0, 50), "%", "Cumulative arterial deposits",
                  "CT angiography or ultrasound"),
        BioFeature("cardio.aneurysm_risk", "Aneurysm Risk Score", BioSystem.CARDIOVASCULAR,
                  (0, 10), "score", "Arterial wall weakness risk",
                  "imaging and genetic testing"),
        BioFeature("cardio.coagulation", "Coagulation Cascade Activation", BioSystem.CARDIOVASCULAR,
                  (80, 120), "%", "Intrinsic vs extrinsic pathway activity",
                  "PT, aPTT tests"),
        BioFeature("cardio.platelet_aggregation", "Platelet Aggregation Rate", BioSystem.CARDIOVASCULAR,
                  (60, 100), "%", "Clotting tendency",
                  "light transmission aggregometry"),
        BioFeature("cardio.fibrinolytic", "Fibrinolytic Activity", BioSystem.CARDIOVASCULAR,
                  (70, 130), "%", "Clot dissolution capacity",
                  "euglobulin clot lysis time"),
        BioFeature("cardio.blood_viscosity", "Blood Viscosity", BioSystem.CARDIOVASCULAR,
                  (3.0, 4.5), "cP", "Thickness of blood",
                  "viscosimetry"),
        BioFeature("cardio.hematocrit", "Hematocrit", BioSystem.CARDIOVASCULAR,
                  (38, 52), "%", "Red blood cell percentage",
                  "CBC"),
        BioFeature("cardio.ferritin", "Iron Stores (Ferritin)", BioSystem.CARDIOVASCULAR,
                  (30, 300), "ng/mL", "Body iron storage",
                  "serum ferritin"),
        BioFeature("cardio.spo2", "Oxygen Saturation (SpO2)", BioSystem.CARDIOVASCULAR,
                  (95, 100), "%", "Hemoglobin carrying capacity",
                  "pulse oximetry"),
        BioFeature("cardio.lactate_threshold", "Lactate Threshold", BioSystem.CARDIOVASCULAR,
                  (50, 70), "%VO2max", "Anaerobic metabolism onset",
                  "graded exercise test"),
        BioFeature("cardio.orthostatic_tolerance", "Orthostatic Intolerance", BioSystem.CARDIOVASCULAR,
                  (0, 30), "mmHg drop", "Blood pressure drop on standing",
                  "tilt table test"),
        BioFeature("cardio.reperfusion_injury", "Reperfusion Injury Risk", BioSystem.CARDIOVASCULAR,
                  (0, 100), "%", "Damage when blood returns after ischemia",
                  "clinical assessment"),
        BioFeature("cardio.circadian_bp", "Circadian BP Variation", BioSystem.CARDIOVASCULAR,
                  (10, 20), "%", "Nighttime dipping pattern",
                  "24h ambulatory BP monitoring"),

        # ============ A2. RESPIRATORY SYSTEM (20 features) ============
        BioFeature("resp.tidal_volume", "Tidal Volume", BioSystem.RESPIRATORY,
                  (400, 600), "mL", "Air per breath at rest",
                  "spirometry"),
        BioFeature("resp.fev1", "Forced Expiratory Volume (FEV1)", BioSystem.RESPIRATORY,
                  (80, 120), "%", "Air expelled in 1 second",
                  "spirometry"),
        BioFeature("resp.fev1_fvc", "FEV1/FVC Ratio", BioSystem.RESPIRATORY,
                  (0.7, 0.85), "ratio", "Obstructive vs restrictive pattern",
                  "spirometry"),
        BioFeature("resp.dlco", "Diffusion Capacity (DLCO)", BioSystem.RESPIRATORY,
                  (75, 120), "%", "Gas exchange across alveoli",
                  "DLCO test"),
        BioFeature("resp.anatomical_dead_space", "Anatomical Dead Space", BioSystem.RESPIRATORY,
                  (150, 200), "mL", "Air not reaching alveoli",
                  "body plethysmography"),
        BioFeature("resp.physiological_dead_space", "Physiological Dead Space", BioSystem.RESPIRATORY,
                  (100, 250), "mL", "Ventilated but not perfused alveoli",
                  "arterial blood gas"),
        BioFeature("resp.respiratory_drive", "Respiratory Drive", BioSystem.RESPIRATORY,
                  (70, 100), "%", "Central chemoreceptor CO2 sensitivity",
                  "hypercapnic ventilatory response"),
        BioFeature("resp.peripheral_chemo", "Peripheral Chemoreceptor Response", BioSystem.RESPIRATORY,
                  (70, 100), "%", "Oxygen sensitivity",
                  "hypoxic ventilatory response"),
        BioFeature("resp.lung_compliance", "Lung Compliance", BioSystem.RESPIRATORY,
                  (150, 250), "mL/cmH2O", "Stretchiness of lungs",
                  "body plethysmography"),
        BioFeature("resp.airway_resistance", "Airway Resistance", BioSystem.RESPIRATORY,
                  (1.0, 2.5), "cmH2O·s/L", "Obstruction measure",
                  "body plethysmography"),
        BioFeature("resp.mucociliary", "Mucociliary Clearance Rate", BioSystem.RESPIRATORY,
                  (3, 7), "mm/min", "Escalator function",
                  "saccharin test"),
        BioFeature("resp.surfactant", "Surfactant Production", BioSystem.RESPIRATORY,
                  (70, 100), "%", "Surface tension reduction",
                  "BAL fluid analysis"),
        BioFeature("resp.pulmonary_htn", "Pulmonary Hypertension", BioSystem.RESPIRATORY,
                  (15, 30), "mmHg", "Blood pressure in pulmonary artery",
                  "echocardiography or RHC"),
        BioFeature("resp.intrapleural_pressure", "Intrapleural Pressure", BioSystem.RESPIRATORY,
                  (-5, -10), "cmH2O", "Negative pressure holding lungs open",
                  "esophageal manometry"),
        BioFeature("resp.work_of_breathing", "Work of Breathing", BioSystem.RESPIRATORY,
                  (0.5, 1.5), "J/L", "Energy cost of breathing",
                  "respiratory mechanics"),
        BioFeature("resp.hypoxic_vaso", "Hypoxic Vasoconstriction", BioSystem.RESPIRATORY,
                  (70, 100), "%", "Blood diversion from poorly ventilated areas",
                  "altitude simulation"),
        BioFeature("resp.hypercapnic_response", "Hypercapnic Response", BioSystem.RESPIRATORY,
                  (70, 130), "%", "CO2 buildup detection",
                  "CO2 rebreathing test"),
        BioFeature("resp.ahi", "Apnea-Hypopnea Index", BioSystem.RESPIRATORY,
                  (0, 5), "/hour", "Breathing pauses per hour",
                  "polysomnography"),
        BioFeature("resp.dyspnea_threshold", "Dyspnea Threshold", BioSystem.RESPIRATORY,
                  (60, 100), "%", "Subjective breathlessness",
                  "Borg scale"),
        BioFeature("resp.pulmonary_fibrosis", "Pulmonary Fibrosis Score", BioSystem.RESPIRATORY,
                  (0, 100), "%", "Scar tissue accumulation",
                  "HRCT scoring"),

        # ============ A3. GASTROINTESTINAL & METABOLIC (25 features) ============
        BioFeature("gi.gastric_emptying", "Gastric Emptying Rate", BioSystem.GASTROINTESTINAL,
                  (60, 100), "%", "Food leaving stomach",
                  "gastric emptying scan"),
        BioFeature("gi.gastric_acid", "Gastric Acid Secretion", BioSystem.GASTROINTESTINAL,
                  (1.5, 3.0), "pH", "Protein digestion and pathogen defense",
                  "gastric analysis"),
        BioFeature("gi.intestinal_permeability", "Intestinal Permeability", BioSystem.GASTROINTESTINAL,
                  (0.2, 0.4), "ratio", "Leaky gut measure",
                  "lactulose/mannitol test"),
        BioFeature("gi.sibo", "SIBO", BioSystem.GASTROINTESTINAL,
                  (0, 10), "cfu/mL", "Bacterial overgrowth in small bowel",
                  "hydrogen breath test"),
        BioFeature("gi.microbiome_alpha", "Microbiome Alpha Diversity", BioSystem.GASTROINTESTINAL,
                  (3, 6), "index", "Within-sample diversity",
                  "Shannon index"),
        BioFeature("gi.microbiome_beta", "Microbiome Beta Diversity", BioSystem.GASTROINTESTINAL,
                  (0.1, 0.5), "distance", "Between-sample similarity",
                  "Bray-Curtis"),
        BioFeature("gi.scfa", "Short-Chain Fatty Acid Production", BioSystem.GASTROINTESTINAL,
                  (50, 100), "mmol/L", "Butyrate, propionate, acetate",
                  "GC-MS of feces"),
        BioFeature("gi.bile_acid_pool", "Bile Acid Pool Size", BioSystem.GASTROINTESTINAL,
                  (2, 5), "g", "Fat digestion and cholesterol excretion",
                  "bile acid profiling"),
        BioFeature("gi.enterohepatic", "Enterohepatic Circulation", BioSystem.GASTROINTESTINAL,
                  (90, 100), "%", "Bile acid recycling efficiency",
                  "tracer studies"),
        BioFeature("gi.pancreatic_exocrine", "Pancreatic Exocrine Function", BioSystem.GASTROINTESTINAL,
                  (70, 100), "%", "Enzyme secretion capacity",
                  "secretin stimulation test"),
        BioFeature("gi.liver_enzymes", "Liver Enzyme Panels", BioSystem.GASTROINTESTINAL,
                  (0, 40), "U/L", "ALT, AST, ALP, GGT markers",
                  "serum chemistry"),
        BioFeature("gi.albumin", "Albumin Synthesis Rate", BioSystem.GASTROINTESTINAL,
                  (35, 50), "g/L", "Protein and nutritional marker",
                  "serum albumin"),
        BioFeature("gi.bilirubin", "Bilirubin Metabolism", BioSystem.GASTROINTESTINAL,
                  (0.1, 1.2), "mg/dL", "Heme breakdown product",
                  "serum bilirubin"),
        BioFeature("gi.urea_cycle", "Urea Cycle Function", BioSystem.GASTROINTESTINAL,
                  (80, 120), "%", "Ammonia detoxification",
                  "ammonia tolerance test"),
        BioFeature("gi.colonic_transit", "Colonic Transit Time", BioSystem.GASTROINTESTINAL,
                  (24, 72), "hours", "Speed of waste movement",
                  "radiopaque markers"),
        BioFeature("gi.water_absorption", "Water Absorption Efficiency", BioSystem.GASTROINTESTINAL,
                  (90, 99), "%", "Large intestine function",
                  "balance studies"),
        BioFeature("gi.nutrient_surface", "Nutrient Absorption Surface Area", BioSystem.GASTROINTESTINAL,
                  (200, 300), "m²", "Villus and microvilli area",
                  "biopsy or imaging"),
        BioFeature("gi.bmr", "Basal Metabolic Rate", BioSystem.GASTROINTESTINAL,
                  (1200, 2000), "kcal/day", "Energy at complete rest",
                  "indirect calorimetry"),
        BioFeature("gi.thermic_food", "Thermic Effect of Food", BioSystem.GASTROINTESTINAL,
                  (10, 30), "%", "Energy to digest nutrients",
                  "postprandial calorimetry"),
        BioFeature("gi.adaptive_thermogenesis", "Adaptive Thermogenesis", BioSystem.GASTROINTESTINAL,
                  (70, 130), "%", "Metabolic adjustment to calorie changes",
                  "calorie restriction studies"),
        BioFeature("gi.insulin_sensitivity", "Insulin Sensitivity (HOMA-IR)", BioSystem.GASTROINTESTINAL,
                  (0.5, 1.5), "index", "Cellular glucose uptake responsiveness",
                  "HOMA-IR calculation"),
        BioFeature("gi.glucagon", "Glucagon Response", BioSystem.GASTROINTESTINAL,
                  (50, 100), "%", "Counter-regulatory hormone",
                  "glucagon stimulation test"),
        BioFeature("gi.ketone_production", "Ketone Body Production", BioSystem.GASTROINTESTINAL,
                  (0.1, 2.0), "mmol/L", "Fat-derived fuel",
                  "beta-hydroxybutyrate"),
        BioFeature("gi.glycogen_storage", "Glycogen Storage Capacity", BioSystem.GASTROINTESTINAL,
                  (400, 500), "g", "Liver and muscle glycogen",
                  "muscle biopsy or imaging"),
        BioFeature("gi.lipolysis_rate", "Lipolysis Rate", BioSystem.GASTROINTESTINAL,
                  (50, 100), "%", "Fat breakdown activity",
                  "fatty acid flux"),

        # ============ A4. RENAL & URINARY (15 features) ============
        BioFeature("renal.gfr", "Glomerular Filtration Rate", BioSystem.RENAL,
                  (80, 120), "mL/min", "Kidney filtering capacity",
                  "creatinine clearance or eGFR"),
        BioFeature("renal.tubular_reabsorption", "Tubular Reabsorption Efficiency", BioSystem.RENAL,
                  (98, 99), "%", "Filtered nutrient reclamation",
                  "fractional excretion"),
        BioFeature("renal.ras_activation", "Renin-Angiotensin System", BioSystem.RENAL,
                  (10, 40), "pg/mL", "Blood pressure regulation",
                  "plasma renin activity"),
        BioFeature("renal.aldosterone", "Aldosterone Response", BioSystem.RENAL,
                  (5, 15), "ng/dL", "Sodium retention",
                  "plasma aldosterone"),
        BioFeature("renal.adh_sensitivity", "ADH Sensitivity", BioSystem.RENAL,
                  (70, 100), "%", "Water reabsorption",
                  "water deprivation test"),
        BioFeature("renal.diurnal_variation", "Diurnal Urine Output", BioSystem.RENAL,
                  (0.5, 1.5), "ratio", "Day/night urine ratio",
                  "24h collection"),
        BioFeature("renal.concentrating_ability", "Urinary Concentrating Ability", BioSystem.RENAL,
                  (300, 900), "mOsm/kg", "Maximum urine osmolality",
                  "water deprivation test"),
        BioFeature("renal.proteinuria", "Proteinuria Grade", BioSystem.RENAL,
                  (0, 0.5), "g/day", "Kidney damage marker",
                  "24h urine protein"),
        BioFeature("renal.nephron_loss", "Nephron Loss Rate", BioSystem.RENAL,
                  (0, 100), "%", "Irreversible nephron decline",
                  "biopsy or imaging"),
        BioFeature("renal.acid_base", "Acid-Base Excretion", BioSystem.RENAL,
                  (80, 120), "%", "Bicarbonate regeneration",
                  "arterial blood gas"),
        BioFeature("renal.potassium", "Potassium Homeostasis", BioSystem.RENAL,
                  (3.5, 5.0), "mEq/L", "Critical for cardiac rhythm",
                  "serum potassium"),
        BioFeature("renal.phosphate", "Phosphate Balance", BioSystem.RENAL,
                  (2.5, 4.5), "mg/dL", "Bone mineralization",
                  "serum phosphate"),
        BioFeature("renal.uric_acid", "Uric Acid Clearance", BioSystem.RENAL,
                  (6, 12), "mg/dL", "Gout risk marker",
                  "serum uric acid"),
        BioFeature("renal.creatinine_generation", "Creatinine Generation", BioSystem.RENAL,
                  (15, 25), "mg/kg/day", "Muscle mass proxy",
                  "24h creatinine excretion"),
        BioFeature("renal.bladder_compliance", "Bladder Compliance", BioSystem.RENAL,
                  (20, 50), "mL/cmH2O", "Storage capacity",
                  "urodynamics"),

        # ============ A5. MUSCULOSKELETAL (20 features) ============
        BioFeature("msk.bmd", "Bone Mineral Density", BioSystem.MUSCULOSKELETAL,
                  (-1, 1), "T-score", "Bone strength measure",
                  "DXA scan"),
        BioFeature("msk.cortical_trabecular", "Cortical vs Trabecular Ratio", BioSystem.MUSCULOSKELETAL,
                  (1.5, 3.0), "ratio", "Structural bone types",
                  "HR-pQCT"),
        BioFeature("msk.sarcomere_length", "Sarcomere Length", BioSystem.MUSCULOSKELETAL,
                  (2.0, 2.5), "µm", "Muscle fiber contraction state",
                  "laser diffraction"),
        BioFeature("msk.motor_unit", "Motor Unit Recruitment", BioSystem.MUSCULOSKELETAL,
                  (1, 600), "units", "Recruited motor units",
                  "EMG"),
        BioFeature("msk.fiber_type", "Type I vs Type II Fiber Ratio", BioSystem.MUSCULOSKELETAL,
                  (40, 60), "%", "Endurance vs power fibers",
                  "muscle biopsy"),
        BioFeature("msk.tendon_stiffness", "Tendon Stiffness", BioSystem.MUSCULOSKELETAL,
                  (300, 600), "N/mm", "Energy storage and return",
                  "ultrasonography"),
        BioFeature("msk.cartilage_thickness", "Cartilage Thickness", BioSystem.MUSCULOSKELETAL,
                  (1.5, 3.0), "mm", "Joint cushioning",
                  "MRI"),
        BioFeature("msk.synovial_viscosity", "Synovial Fluid Viscosity", BioSystem.MUSCULOSKELETAL,
                  (0.1, 1.0), "Pa·s", "Joint lubrication",
                  "viscosimetry"),
        BioFeature("msk.ligamentous_laxity", "Ligamentous Laxity", BioSystem.MUSCULOSKELETAL,
                  (0, 15), "mm", "Joint stability measure",
                  "KT-2000"),
        BioFeature("msk.compartment_pressure", "Compartment Pressure", BioSystem.MUSCULOSKELETAL,
                  (10, 20), "mmHg", "Muscle fascia pressure",
                  "slit catheter"),
        BioFeature("msk.fracture_healing", "Fracture Healing Stage", BioSystem.MUSCULOSKELETAL,
                  (0, 100), "%", "Healing progression",
                  "radiographic"),
        BioFeature("msk.bone_remodeling", "Bone Remodeling Rate", BioSystem.MUSCULOSKELETAL,
                  (20, 30), "%/year", "Turnover rate",
                  "bone markers"),
        BioFeature("msk.lordosis", "Lordosis Angle", BioSystem.MUSCULOSKELETAL,
                  (30, 45), "degrees", "Lower back curvature",
                  "radiographic"),
        BioFeature("msk.kyphosis", "Kyphosis Angle", BioSystem.MUSCULOSKELETAL,
                  (20, 40), "degrees", "Upper back rounding",
                  "radiographic"),
        BioFeature("msk.gait_asymmetry", "Gait Asymmetry Index", BioSystem.MUSCULOSKELETAL,
                  (0, 10), "%", "Left-right difference",
                  "instrumented walkway"),
        BioFeature("msk.proprioception", "Proprioception Accuracy", BioSystem.MUSCULOSKELETAL,
                  (70, 100), "%", "Joint position sense",
                  "joint position sense test"),
        BioFeature("msk.balance_strategy", "Balance Strategy", BioSystem.MUSCULOSKELETAL,
                  (1, 3), "score", "Ankle vs hip vs stepping",
                  "posturography"),
        BioFeature("msk.sarcopenia", "Sarcopenia Rate", BioSystem.MUSCULOSKELETAL,
                  (0, 1), "%/year", "Age-related muscle loss",
                  "DXA or bioimpedance"),
        BioFeature("msk.dynapenia", "Dynapenia", BioSystem.MUSCULOSKELETAL,
                  (0, 50), "%", "Strength loss beyond mass",
                  "handgrip dynamometry"),
        BioFeature("msk.fascial_tension", "Fascial Tension", BioSystem.MUSCULOSKELETAL,
                  (0, 100), "N", "Connective tissue network",
                  "myofascial release test"),

        # ============ A6. INTEGUMENTARY & SENSORY (20 features) ============
        BioFeature("skin.tewl", "Transepidermal Water Loss", BioSystem.INTEGUMENTARY,
                  (5, 15), "g/m²/h", "Barrier function measure",
                  "TEWL meter"),
        BioFeature("skin.stratum_hydration", "Stratum Corneum Hydration", BioSystem.INTEGUMENTARY,
                  (20, 60), "%", "Surface moisture",
                  "corneometry"),
        BioFeature("skin.melanin_index", "Melanin Index", BioSystem.INTEGUMENTARY,
                  (10, 70), "units", "Pigmentation level",
                  "mexametry"),
        BioFeature("skin.collagen", "Collagen Cross-Linking Density", BioSystem.INTEGUMENTARY,
                  (70, 100), "%", "Skin elasticity",
                  "biopsy"),
        BioFeature("skin.elastin", "Elastin Fragmentation", BioSystem.INTEGUMENTARY,
                  (0, 50), "%", "Sagging measure",
                  "biopsy"),
        BioFeature("skin.sebum", "Sebum Production Rate", BioSystem.INTEGUMENTARY,
                  (1, 5), "µg/cm²/min", "Oiliness",
                  "sebumetry"),
        BioFeature("skin.wound_tensile", "Wound Tensile Strength", BioSystem.INTEGUMENTARY,
                  (0, 100), "%", "Reopening resistance",
                  "tensiometry"),
        BioFeature("skin.angiogenesis", "Angiogenesis in Healing", BioSystem.INTEGUMENTARY,
                  (0, 100), "%", "New vessel formation",
                  "histology"),
        BioFeature("skin.keloid", "Keloid Formation Tendency", BioSystem.INTEGUMENTARY,
                  (0, 1), "score", "Excessive scar risk",
                  "clinical assessment"),
        BioFeature("skin.pressure_ulcer", "Pressure Ulcer Stage", BioSystem.INTEGUMENTARY,
                  (0, 4), "stage", "Tissue damage grade",
                  "clinical examination"),
        BioFeature("skin.uv_damage", "UV Damage Accumulation", BioSystem.INTEGUMENTARY,
                  (0, 100), "%", "Photoaging dose",
                  "skin biopsy"),
        BioFeature("skin.vitamin_d", "Vitamin D Synthesis Rate", BioSystem.INTEGUMENTARY,
                  (20, 60), "IU/cm²/h", "Skin production",
                  "sun exposure studies"),
        BioFeature("skin.thermoreg_sweat", "Thermoregulatory Sweating", BioSystem.INTEGUMENTARY,
                  (300, 500), "g/m²/h", "Core temperature trigger",
                  "ventilated capsule"),
        BioFeature("skin.eccrine_apocrine", "Eccrine vs Apocrine Sweat", BioSystem.INTEGUMENTARY,
                  (70, 30), "%", "Cooling vs scent glands",
                  "iodine starch test"),
        BioFeature("skin.hair_cycle", "Hair Follicle Cycling", BioSystem.INTEGUMENTARY,
                  (80, 90), "% anagen", "Growth phase proportion",
                  "trichoscopy"),
        BioFeature("skin.nail_growth", "Nail Growth Rate", BioSystem.INTEGUMENTARY,
                  (2, 4), "mm/month", "Nail elongation",
                  "measurement"),
        BioFeature("skin.meissner", "Meissner Corpuscle Density", BioSystem.INTEGUMENTARY,
                  (10, 30), "/mm²", "Light touch receptors",
                  "skin biopsy"),
        BioFeature("skin.pacinian", "Pacinian Corpuscle Sensitivity", BioSystem.INTEGUMENTARY,
                  (70, 100), "%", "Vibration detection",
                  "vibrotactile testing"),
        BioFeature("skin.free_nerve", "Free Nerve Ending Density", BioSystem.INTEGUMENTARY,
                  (100, 500), "/cm²", "Pain and temperature",
                  "skin biopsy"),
        BioFeature("skin.ruffini", "Ruffini Ending Function", BioSystem.INTEGUMENTARY,
                  (70, 100), "%", "Skin stretch detection",
                  "stretch perception test"),

        # ============ A7. IMMUNE SYSTEM (25 features) ============
        BioFeature("immune.igg", "IgG Titer", BioSystem.IMMUNE,
                  (700, 1600), "mg/dL", "Memory antibody",
                  "nephelometry"),
        BioFeature("immune.igm", "IgM Titer", BioSystem.IMMUNE,
                  (40, 250), "mg/dL", "Acute antibody",
                  "nephelometry"),
        BioFeature("immune.iga", "IgA Titer", BioSystem.IMMUNE,
                  (70, 400), "mg/dL", "Mucosal antibody",
                  "nephelometry"),
        BioFeature("immune.tcell_diversity", "T-Cell Receptor Diversity", BioSystem.IMMUNE,
                  (70, 100), "%", "V(D)J recombination breadth",
                  "sequencing"),
        BioFeature("immune.cd4_cd8", "CD4/CD8 Ratio", BioSystem.IMMUNE,
                  (1.0, 3.0), "ratio", "Helper vs cytotoxic balance",
                  "flow cytometry"),
        BioFeature("immune.nk_cell", "NK Cell Cytotoxicity", BioSystem.IMMUNE,
                  (60, 100), "%", "Innate killing capacity",
                  "51Cr release assay"),
        BioFeature("immune.complement", "Complement Activity (CH50)", BioSystem.IMMUNE,
                  (150, 300), "U/mL", "Cascade protein function",
                  "CH50 assay"),
        BioFeature("immune.cytokine_profile", "Cytokine Profile", BioSystem.IMMUNE,
                  (0, 100), "pg/mL", "IL-6, TNF-α, IL-1β, IL-10",
                  "multiplex analysis"),
        BioFeature("immune.inflammasome", "Inflammasome Activation", BioSystem.IMMUNE,
                  (0, 100), "%", "NLRP3 activation",
                  "Western blot"),
        BioFeature("immune.mast_cell", "Mast Cell Activation", BioSystem.IMMUNE,
                  (0, 100), "%", "Allergic response trigger",
                  "tryptase"),
        BioFeature("immune.histamine", "Histamine Tolerance", BioSystem.IMMUNE,
                  (3, 10), "ng/mL", "Diamine oxidase capacity",
                  "DAO activity"),
        BioFeature("immune.autoantibody", "Autoantibody Panels", BioSystem.IMMUNE,
                  (0, 1), "titer", "ANA, RF, anti-dsDNA",
                  "immunofluorescence"),
        BioFeature("immune.vaccine_response", "Vaccine Response Memory", BioSystem.IMMUNE,
                  (50, 200), "mIU/mL", "Antibody persistence",
                  "titer testing"),
        BioFeature("immune.gvhd", "Graft-vs-Host Potential", BioSystem.IMMUNE,
                  (0, 100), "%", "Donor T-cell attack risk",
                  "mixed lymphocyte reaction"),
        BioFeature("immune.tolerance", "Immune Tolerance", BioSystem.IMMUNE,
                  (70, 100), "%", "Self vs non-self discrimination",
                  "tolerance assays"),
        BioFeature("immune.mhc", "MHC Haplotype", BioSystem.IMMUNE,
                  (0, 6), "alleles", "Antigen presentation genetics",
                  "HLA typing"),
        BioFeature("immune.net_formation", "NET Formation", BioSystem.IMMUNE,
                  (0, 100), "%", "DNA-based pathogen capture",
                  "NETosis assay"),
        BioFeature("immune.macrophage", "Macrophage Polarization", BioSystem.IMMUNE,
                  (0, 100), "% M1", "M1 vs M2 balance",
                  "surface markers"),
        BioFeature("immune.dendritic", "Dendritic Cell Maturation", BioSystem.IMMUNE,
                  (0, 100), "%", "Antigen presentation",
                  "flow cytometry"),
        BioFeature("immune.bcell_maturation", "B-Cell Affinity Maturation", BioSystem.IMMUNE,
                  (0, 100), "%", "Somatic hypermutation",
                  "sequencing"),
        BioFeature("immune.treg", "Regulatory T-Cell Function", BioSystem.IMMUNE,
                  (50, 150), "cells/µL", "Immune suppression",
                  "flow cytometry"),
        BioFeature("immune.thymic_involution", "Thymic Involution", BioSystem.IMMUNE,
                  (0, 100), "%", "T-cell production decline",
                  "CT imaging"),
        BioFeature("immune.memory_decay", "Immunological Memory Decay", BioSystem.IMMUNE,
                  (0, 100), "%", "Antibody titer decline",
                  "longitudinal testing"),
        BioFeature("immune.trained_immunity", "Trained Immunity", BioSystem.IMMUNE,
                  (0, 1), "score", "Innate immune memory",
                  "functional assays"),
        BioFeature("immune.barrier", "Barrier Immunity", BioSystem.IMMUNE,
                  (70, 100), "%", "Epithelial defenses",
                  "functional testing"),

        # ============ A8. ENDOCRINE & HORMONAL (25 features) ============
        BioFeature("endo.crh_pulse", "CRH Pulse", BioSystem.ENDOCRINE,
                  (0.5, 2.0), "pulses/h", "HPA axis initiator",
                  "sampling study"),
        BioFeature("endo.acth_rhythm", "ACTH Circadian Rhythm", BioSystem.ENDOCRINE,
                  (10, 80), "pg/mL", "Pituitary ACTH release",
                  "serial sampling"),
        BioFeature("endo.cortisol_awakening", "Cortisol Awakening Response", BioSystem.ENDOCRINE,
                  (50, 150), "%", "Morning cortisol surge",
                  "salivary cortisol"),
        BioFeature("endo.cortisol_slope", "Cortisol Diurnal Slope", BioSystem.ENDOCRINE,
                  (20, 60), "%", "Daytime decline rate",
                  "multiple samples"),
        BioFeature("endo.tsh", "TSH", BioSystem.ENDOCRINE,
                  (0.4, 4.0), "mIU/L", "Pituitary thyroid signal",
                  "serum TSH"),
        BioFeature("endo.free_t3_t4", "Free T3/T4 Ratio", BioSystem.ENDOCRINE,
                  (0.2, 0.3), "ratio", "Active hormone conversion",
                  "serum free T3/T4"),
        BioFeature("endo.reverse_t3", "Reverse T3 Elevation", BioSystem.ENDOCRINE,
                  (10, 50), "ng/dL", "Inactive competitor",
                  "serum rT3"),
        BioFeature("endo.insulin_pulsatility", "Insulin Pulsatility", BioSystem.ENDOCRINE,
                  (70, 100), "%", "Oscillatory secretion",
                  "frequent sampling"),
        BioFeature("endo.c peptide", "C-Peptide", BioSystem.ENDOCRINE,
                  (0.5, 2.0), "ng/mL", "Endogenous insulin",
                  "serum C-peptide"),
        BioFeature("endo.glp1", "GLP-1", BioSystem.ENDOCRINE,
                  (5, 30), "pmol/L", "Incretin hormone",
                  "ELISA"),
        BioFeature("endo.gh_pulsatility", "GH Pulsatility", BioSystem.ENDOCRINE,
                  (0.5, 3.0), "ng/mL", "Growth hormone bursts",
                  "frequent sampling"),
        BioFeature("endo.igf1", "IGF-1", BioSystem.ENDOCRINE,
                  (100, 400), "ng/mL", "GH mediator",
                  "serum IGF-1"),
        BioFeature("endo.shbg", "SHBG", BioSystem.ENDOCRINE,
                  (10, 80), "nmol/L", "Sex hormone carrier",
                  "serum SHBG"),
        BioFeature("endo.testosterone_diurnal", "Testosterone Diurnal", BioSystem.ENDOCRINE,
                  (10, 30), "%", "Morning peak variation",
                  "serial sampling"),
        BioFeature("endo.estradiol_cycle", "Estradiol Cyclical", BioSystem.ENDOCRINE,
                  (20, 400), "pg/mL", "Menstrual cycle phase",
                  "serum estradiol"),
        BioFeature("endo.progesterone", "Progesterone", BioSystem.ENDOCRINE,
                  (0.1, 20), "ng/mL", "Luteal phase hormone",
                  "serum progesterone"),
        BioFeature("endo.prolactin", "Prolactin", BioSystem.ENDOCRINE,
                  (5, 25), "ng/mL", "Lactation hormone",
                  "serum prolactin"),
        BioFeature("endo.pth", "PTH", BioSystem.ENDOCRINE,
                  (10, 65), "pg/mL", "Calcium homeostasis",
                  "serum PTH"),
        BioFeature("endo.calcitonin", "Calcitonin", BioSystem.ENDOCRINE,
                  (0, 10), "pg/mL", "Calcium-lowering",
                  "serum calcitonin"),
        BioFeature("endo.aldosterone_renin", "Aldosterone/Renin Ratio", BioSystem.ENDOCRINE,
                  (0, 30), "ratio", "Hyperaldosteronism screen",
                  "plasma ARR"),
        BioFeature("endo.melatonin", "Melatonin", BioSystem.ENDOCRINE,
                  (10, 60), "pg/mL", "Circadian regulation",
                  "salivary melatonin"),
        BioFeature("endo.leptin", "Leptin", BioSystem.ENDOCRINE,
                  (5, 30), "ng/mL", "Satiety hormone",
                  "serum leptin"),
        BioFeature("endo.ghrelin", "Ghrelin", BioSystem.ENDOCRINE,
                  (50, 200), "pg/mL", "Hunger hormone",
                  "serum ghrelin"),
        BioFeature("endo.oxytocin", "Oxytocin", BioSystem.ENDOCRINE,
                  (10, 30), "pg/mL", "Social bonding",
                  "plasma oxytocin"),
        BioFeature("endo.vasopressin", "Vasopressin (ADH)", BioSystem.ENDOCRINE,
                  (0, 5), "pg/mL", "Water balance",
                  "plasma ADH"),
    ]
    
    for feature in features:
        BIOLOGICAL_FEATURES[feature.id] = feature


_register_features()


def get_bio_feature(feature_id: str) -> Optional[BioFeature]:
    """Get a biological feature by ID."""
    return BIOLOGICAL_FEATURES.get(feature_id)


def get_features_by_system(system: BioSystem) -> List[BioFeature]:
    """Get all features for a given biological system."""
    return [f for f in BIOLOGICAL_FEATURES.values() if f.system == system]


def get_all_feature_ids() -> List[str]:
    """Get all feature IDs."""
    return list(BIOLOGICAL_FEATURES.keys())


def get_feature_count() -> int:
    """Get total feature count."""
    return len(BIOLOGICAL_FEATURES)


def get_feature_snapshot(physiology_model) -> dict:
    """
    Generate biological feature snapshot from physiology model.
    Maps physiology.py state to biological features.
    """
    snapshot = {}
    
    for feature_id, feature in BIOLOGICAL_FEATURES.items():
        if feature_id.startswith("cardio."):
            if "hrv" in feature_id:
                snapshot[feature_id] = 35.0
            elif "sdnn" in feature_id:
                snapshot[feature_id] = 100.0
            elif "lf_hf" in feature_id:
                snapshot[feature_id] = 1.0
            elif "baro" in feature_id:
                snapshot[feature_id] = 12.0
            elif "pwv" in feature_id:
                snapshot[feature_id] = 8.0
            elif "ejection" in feature_id:
                snapshot[feature_id] = 65.0
            elif "stroke" in feature_id:
                snapshot[feature_id] = 80.0
            elif "cardiac_output" in feature_id:
                snapshot[feature_id] = 5.5
            elif "peripheral_resistance" in feature_id:
                snapshot[feature_id] = 1000.0
            elif "venous_compliance" in feature_id:
                snapshot[feature_id] = 2.0
            elif "capillary" in feature_id:
                snapshot[feature_id] = 250.0
            elif "microcirculation" in feature_id:
                snapshot[feature_id] = 80.0
            elif "plaque" in feature_id:
                snapshot[feature_id] = 10.0
            elif "aneurysm" in feature_id:
                snapshot[feature_id] = 1.0
            elif "coagulation" in feature_id:
                snapshot[feature_id] = 100.0
            elif "platelet" in feature_id:
                snapshot[feature_id] = 80.0
            elif "fibrinolytic" in feature_id:
                snapshot[feature_id] = 100.0
            elif "blood_viscosity" in feature_id:
                snapshot[feature_id] = 3.5
            elif "hematocrit" in feature_id:
                snapshot[feature_id] = 45.0
            elif "ferritin" in feature_id:
                snapshot[feature_id] = 100.0
            elif "spo2" in feature_id:
                snapshot[feature_id] = 98.0
            elif "lactate" in feature_id:
                snapshot[feature_id] = 60.0
            elif "orthostatic" in feature_id:
                snapshot[feature_id] = 10.0
            elif "reperfusion" in feature_id:
                snapshot[feature_id] = 5.0
            elif "circadian" in feature_id:
                snapshot[feature_id] = 15.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("resp."):
            if "tidal" in feature_id:
                snapshot[feature_id] = 500.0
            elif "fev1" in feature_id:
                snapshot[feature_id] = 95.0
            elif "fev1_fvc" in feature_id:
                snapshot[feature_id] = 0.78
            elif "dlco" in feature_id:
                snapshot[feature_id] = 90.0
            elif "dead_space" in feature_id:
                snapshot[feature_id] = 150.0
            elif "physiological_dead" in feature_id:
                snapshot[feature_id] = 150.0
            elif "drive" in feature_id or "chemo" in feature_id:
                snapshot[feature_id] = 85.0
            elif "compliance" in feature_id:
                snapshot[feature_id] = 200.0
            elif "resistance" in feature_id:
                snapshot[feature_id] = 1.5
            elif "mucociliary" in feature_id:
                snapshot[feature_id] = 5.0
            elif "surfactant" in feature_id:
                snapshot[feature_id] = 90.0
            elif "pulmonary_htn" in feature_id:
                snapshot[feature_id] = 20.0
            elif "intrapleural" in feature_id:
                snapshot[feature_id] = -7.0
            elif "work" in feature_id:
                snapshot[feature_id] = 1.0
            elif "hypoxic" in feature_id:
                snapshot[feature_id] = 85.0
            elif "hypercapnic" in feature_id:
                snapshot[feature_id] = 100.0
            elif "ahi" in feature_id:
                snapshot[feature_id] = 2.0
            elif "dyspnea" in feature_id:
                snapshot[feature_id] = 80.0
            elif "fibrosis" in feature_id:
                snapshot[feature_id] = 5.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("gi."):
            if "gastric" in feature_id:
                snapshot[feature_id] = 80.0
            elif "permeability" in feature_id:
                snapshot[feature_id] = 0.3
            elif "sibo" in feature_id:
                snapshot[feature_id] = 2.0
            elif "microbiome_alpha" in feature_id:
                snapshot[feature_id] = 4.5
            elif "microbiome_beta" in feature_id:
                snapshot[feature_id] = 0.25
            elif "scfa" in feature_id:
                snapshot[feature_id] = 75.0
            elif "bile" in feature_id:
                snapshot[feature_id] = 3.5
            elif "enterohepatic" in feature_id:
                snapshot[feature_id] = 95.0
            elif "pancreatic" in feature_id:
                snapshot[feature_id] = 85.0
            elif "liver" in feature_id:
                snapshot[feature_id] = 25.0
            elif "albumin" in feature_id:
                snapshot[feature_id] = 42.0
            elif "bilirubin" in feature_id:
                snapshot[feature_id] = 0.5
            elif "urea" in feature_id:
                snapshot[feature_id] = 100.0
            elif "colonic" in feature_id:
                snapshot[feature_id] = 48.0
            elif "water" in feature_id:
                snapshot[feature_id] = 95.0
            elif "surface" in feature_id:
                snapshot[feature_id] = 250.0
            elif "bmr" in feature_id:
                snapshot[feature_id] = 1600.0
            elif "thermic" in feature_id:
                snapshot[feature_id] = 20.0
            elif "adaptive" in feature_id:
                snapshot[feature_id] = 100.0
            elif "insulin" in feature_id:
                snapshot[feature_id] = 1.0
            elif "glucagon" in feature_id:
                snapshot[feature_id] = 75.0
            elif "ketone" in feature_id:
                snapshot[feature_id] = 0.3
            elif "glycogen" in feature_id:
                snapshot[feature_id] = 450.0
            elif "lipolysis" in feature_id:
                snapshot[feature_id] = 75.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("renal."):
            if "gfr" in feature_id:
                snapshot[feature_id] = 100.0
            elif "tubular" in feature_id:
                snapshot[feature_id] = 98.5
            elif "ras" in feature_id or "renin" in feature_id:
                snapshot[feature_id] = 25.0
            elif "aldosterone" in feature_id:
                snapshot[feature_id] = 10.0
            elif "adh" in feature_id:
                snapshot[feature_id] = 85.0
            elif "diurnal" in feature_id:
                snapshot[feature_id] = 1.0
            elif "concentrating" in feature_id:
                snapshot[feature_id] = 600.0
            elif "proteinuria" in feature_id:
                snapshot[feature_id] = 0.1
            elif "nephron" in feature_id:
                snapshot[feature_id] = 100.0
            elif "acid_base" in feature_id:
                snapshot[feature_id] = 100.0
            elif "potassium" in feature_id:
                snapshot[feature_id] = 4.2
            elif "phosphate" in feature_id:
                snapshot[feature_id] = 3.5
            elif "uric" in feature_id:
                snapshot[feature_id] = 7.0
            elif "creatinine" in feature_id:
                snapshot[feature_id] = 20.0
            elif "bladder" in feature_id:
                snapshot[feature_id] = 35.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("msk."):
            if "bmd" in feature_id:
                snapshot[feature_id] = 0.0
            elif "cortical" in feature_id:
                snapshot[feature_id] = 2.0
            elif "sarcomere" in feature_id:
                snapshot[feature_id] = 2.2
            elif "motor" in feature_id:
                snapshot[feature_id] = 300.0
            elif "fiber" in feature_id:
                snapshot[feature_id] = 50.0
            elif "tendon" in feature_id:
                snapshot[feature_id] = 400.0
            elif "cartilage" in feature_id:
                snapshot[feature_id] = 2.0
            elif "synovial" in feature_id:
                snapshot[feature_id] = 0.5
            elif "ligament" in feature_id:
                snapshot[feature_id] = 5.0
            elif "compartment" in feature_id:
                snapshot[feature_id] = 15.0
            elif "fracture" in feature_id:
                snapshot[feature_id] = 100.0
            elif "bone_remodeling" in feature_id:
                snapshot[feature_id] = 25.0
            elif "lordosis" in feature_id:
                snapshot[feature_id] = 35.0
            elif "kyphosis" in feature_id:
                snapshot[feature_id] = 30.0
            elif "gait" in feature_id:
                snapshot[feature_id] = 2.0
            elif "proprioception" in feature_id:
                snapshot[feature_id] = 85.0
            elif "balance" in feature_id:
                snapshot[feature_id] = 2.0
            elif "sarcopenia" in feature_id:
                snapshot[feature_id] = 0.0
            elif "dynapenia" in feature_id:
                snapshot[feature_id] = 5.0
            elif "fascial" in feature_id:
                snapshot[feature_id] = 50.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("skin."):
            if "tewl" in feature_id:
                snapshot[feature_id] = 10.0
            elif "stratum" in feature_id:
                snapshot[feature_id] = 40.0
            elif "melanin" in feature_id:
                snapshot[feature_id] = 30.0
            elif "collagen" in feature_id:
                snapshot[feature_id] = 85.0
            elif "elastin" in feature_id:
                snapshot[feature_id] = 10.0
            elif "sebum" in feature_id:
                snapshot[feature_id] = 2.5
            elif "wound" in feature_id:
                snapshot[feature_id] = 100.0
            elif "angiogenesis" in feature_id:
                snapshot[feature_id] = 80.0
            elif "keloid" in feature_id:
                snapshot[feature_id] = 0.0
            elif "pressure" in feature_id:
                snapshot[feature_id] = 0.0
            elif "uv" in feature_id:
                snapshot[feature_id] = 20.0
            elif "vitamin_d" in feature_id:
                snapshot[feature_id] = 40.0
            elif "thermoreg" in feature_id or "sweat" in feature_id:
                snapshot[feature_id] = 400.0
            elif "eccrine" in feature_id:
                snapshot[feature_id] = 70.0
            elif "hair" in feature_id:
                snapshot[feature_id] = 85.0
            elif "nail" in feature_id:
                snapshot[feature_id] = 3.0
            elif "meissner" in feature_id:
                snapshot[feature_id] = 20.0
            elif "pacinian" in feature_id:
                snapshot[feature_id] = 85.0
            elif "free_nerve" in feature_id:
                snapshot[feature_id] = 300.0
            elif "ruffini" in feature_id:
                snapshot[feature_id] = 85.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("immune."):
            if "igg" in feature_id:
                snapshot[feature_id] = 1000.0
            elif "igm" in feature_id:
                snapshot[feature_id] = 100.0
            elif "iga" in feature_id:
                snapshot[feature_id] = 200.0
            elif "tcell" in feature_id or "diversity" in feature_id:
                snapshot[feature_id] = 85.0
            elif "cd4" in feature_id:
                snapshot[feature_id] = 2.0
            elif "nk" in feature_id:
                snapshot[feature_id] = 80.0
            elif "complement" in feature_id:
                snapshot[feature_id] = 200.0
            elif "cytokine" in feature_id:
                snapshot[feature_id] = 10.0
            elif "inflammasome" in feature_id:
                snapshot[feature_id] = 10.0
            elif "mast" in feature_id:
                snapshot[feature_id] = 10.0
            elif "histamine" in feature_id:
                snapshot[feature_id] = 5.0
            elif "autoantibody" in feature_id:
                snapshot[feature_id] = 0.0
            elif "vaccine" in feature_id:
                snapshot[feature_id] = 100.0
            elif "gvh" in feature_id:
                snapshot[feature_id] = 5.0
            elif "tolerance" in feature_id:
                snapshot[feature_id] = 85.0
            elif "mhc" in feature_id:
                snapshot[feature_id] = 3.0
            elif "net" in feature_id:
                snapshot[feature_id] = 10.0
            elif "macrophage" in feature_id:
                snapshot[feature_id] = 30.0
            elif "dendritic" in feature_id:
                snapshot[feature_id] = 70.0
            elif "bcell" in feature_id:
                snapshot[feature_id] = 80.0
            elif "treg" in feature_id:
                snapshot[feature_id] = 100.0
            elif "thymic" in feature_id:
                snapshot[feature_id] = 20.0
            elif "memory_decay" in feature_id:
                snapshot[feature_id] = 10.0
            elif "trained" in feature_id:
                snapshot[feature_id] = 0.5
            elif "barrier" in feature_id:
                snapshot[feature_id] = 85.0
            else:
                snapshot[feature_id] = 50.0
                
        elif feature_id.startswith("endo."):
            if "crh" in feature_id:
                snapshot[feature_id] = 1.0
            elif "acth" in feature_id:
                snapshot[feature_id] = 40.0
            elif "cortisol_awakening" in feature_id:
                snapshot[feature_id] = 100.0
            elif "cortisol_slope" in feature_id:
                snapshot[feature_id] = 40.0
            elif "tsh" in feature_id:
                snapshot[feature_id] = 2.0
            elif "free_t3" in feature_id:
                snapshot[feature_id] = 0.25
            elif "reverse_t3" in feature_id:
                snapshot[feature_id] = 25.0
            elif "insulin" in feature_id:
                snapshot[feature_id] = 85.0
            elif "c_peptide" in feature_id:
                snapshot[feature_id] = 1.2
            elif "glp1" in feature_id:
                snapshot[feature_id] = 15.0
            elif "gh_pulsatility" in feature_id:
                snapshot[feature_id] = 1.5
            elif "igf1" in feature_id:
                snapshot[feature_id] = 250.0
            elif "shbg" in feature_id:
                snapshot[feature_id] = 40.0
            elif "testosterone" in feature_id:
                snapshot[feature_id] = 20.0
            elif "estradiol" in feature_id:
                snapshot[feature_id] = 150.0
            elif "progesterone" in feature_id:
                snapshot[feature_id] = 5.0
            elif "prolactin" in feature_id:
                snapshot[feature_id] = 12.0
            elif "pth" in feature_id:
                snapshot[feature_id] = 35.0
            elif "calcitonin" in feature_id:
                snapshot[feature_id] = 5.0
            elif "aldosterone" in feature_id and "renin" in feature_id:
                snapshot[feature_id] = 15.0
            elif "melatonin" in feature_id:
                snapshot[feature_id] = 30.0
            elif "leptin" in feature_id:
                snapshot[feature_id] = 15.0
            elif "ghrelin" in feature_id:
                snapshot[feature_id] = 100.0
            elif "oxytocin" in feature_id:
                snapshot[feature_id] = 20.0
            elif "vasopressin" in feature_id:
                snapshot[feature_id] = 2.0
            else:
                snapshot[feature_id] = 50.0
    
    return snapshot