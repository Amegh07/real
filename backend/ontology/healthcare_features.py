"""
Healthcare & Medical Feature Registry — Additional Sections
===========================================================
Features for sections already in extended_features but missing detail
and additional healthcare domains.

Total: ~150 features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class HealthcareSystem(Enum):
    MEDICAL = auto()
    PHARMACEUTICAL = auto()
    MENTAL_HEALTH = auto()
    PUBLIC_HEALTH = auto()
    NUTRITIONAL = auto()


@dataclass
class HealthcareFeature:
    feature_id: str
    feature_name: str
    system: HealthcareSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


HEALTHCARE_FEATURES: dict = {}


def _register_healthcare_features():
    global HEALTHCARE_FEATURES
    
    features = [
        # ============ MEDICAL SYSTEMS (30 features) ============
        HealthcareFeature("med.humoral_theory", "Humoral Theory", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Blood, phlegm, yellow bile, black bile - Galenic tradition",
                          "Historical"),
        HealthcareFeature("med.miasma_theory", "Miasma Theory", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Bad air causes disease - cholera misattribution",
                          "Historical"),
        HealthcareFeature("med.germ_theory", "Germ Theory Acceptance", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Koch's postulates - Semmelweis handwashing resistance",
                          "Microbiology"),
        HealthcareFeature("med.evidence_based", "Evidence-Based Medicine", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "RCT hierarchy - Cochrane systematic reviews",
                          "Clinical"),
        HealthcareFeature("med.placebo_trial", "Placebo-Controlled Trial", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Ethical debate - equipoise requirement",
                          "Clinical trials"),
        HealthcareFeature("med.personalized_medicine", "Personalized Medicine", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Pharmacogenomics - warfarin dosing by CYP2C9",
                          "Genomics"),
        HealthcareFeature("med.stem_cell_therapy", "Stem Cell Therapy", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Pluripotency - ethical and tumor risk concerns",
                          "Cell therapy"),
        HealthcareFeature("med.gene_therapy", "Gene Therapy", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "CAR-T, CRISPR - long-term efficacy and safety",
                          "Gene therapy"),
        HealthcareFeature("med.organ_transplant", "Organ Transplant Rejection", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Immunosuppression - lifetime medication",
                          "Transplant"),
        HealthcareFeature("med.telemedicine", "Telemedicine Adoption", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Remote consultation - licensure and reimbursement",
                          "Healthcare delivery"),
        HealthcareFeature("med.traditional_healer", "Traditional Healer Role", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Shaman, herbalist, bone-setter - complement or substitute",
                          "Traditional medicine"),
        HealthcareFeature("med.medical_tourism", "Medical Tourism", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Cross-border care - cost and quality arbitrage",
                          "Healthcare"),
        HealthcareFeature("med.health_insurance", "Health Insurance Mandate", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Individual requirement - adverse selection prevention",
                          "Insurance"),
        HealthcareFeature("med.single_payer", "Single-Payer System", HealthcareSystem.MEDICAL,
                          (0, 1), "scale", "Government as insurer - administrative cost reduction",
                          "Healthcare system"),
        HealthcareFeature("med.out_of_pocket", "Out-of-Pocket Maximum", HealthcareSystem.MEDICAL,
                          (0, 100000), "currency", "Catastrophic protection - underinsurance gap",
                          "Insurance"),
        HealthcareFeature("med.heart_rate", "Heart Rate", HealthcareSystem.MEDICAL,
                          (40, 120), "bpm", "Beats per minute - vital sign",
                          "Vital signs"),
        HealthcareFeature("med.blood_pressure_systolic", "Blood Pressure Systolic", HealthcareSystem.MEDICAL,
                          (80, 180), "mmHg", "Top number - pressure during heartbeat",
                          "Vital signs"),
        HealthcareFeature("med.blood_pressure_diastolic", "Blood Pressure Diastolic", HealthcareSystem.MEDICAL,
                          (40, 120), "mmHg", "Bottom number - pressure between beats",
                          "Vital signs"),
        HealthcareFeature("med.respiratory_rate", "Respiratory Rate", HealthcareSystem.MEDICAL,
                          (8, 24), "breaths/min", "Breaths per minute - vital sign",
                          "Vital signs"),
        HealthcareFeature("med.body_temperature", "Body Temperature", HealthcareSystem.MEDICAL,
                          (35, 42), "°C", "Core temperature - fever indicator",
                          "Vital signs"),
        HealthcareFeature("med.oxygen_saturation", "Oxygen Saturation (SpO2)", HealthcareSystem.MEDICAL,
                          (90, 100), "%", "Blood oxygen level - pulse oximetry",
                          "Vital signs"),
        HealthcareFeature("med.bmi", "Body Mass Index", HealthcareSystem.MEDICAL,
                          (10, 50), "kg/m²", "Weight/height² - obesity measure",
                          "Anthropometry"),
        HealthcareFeature("med.waist_circumference", "Waist Circumference", HealthcareSystem.MEDICAL,
                          (50, 200), "cm", "Abdominal fat indicator",
                          "Anthropometry"),
        HealthcareFeature("med.white_blood_cell", "White Blood Cell Count", HealthcareSystem.MEDICAL,
                          (4, 11), "×10⁹/L", "Infection indicator - leukocytosis",
                          "Blood test"),
        HealthcareFeature("med.red_blood_cell", "Red Blood Cell Count", HealthcareSystem.MEDICAL,
                          (3.5, 6), "×10¹²/L", "Anemia indicator",
                          "Blood test"),
        HealthcareFeature("med.hemoglobin", "Hemoglobin", HealthcareSystem.MEDICAL,
                          (120, 180), "g/L", "Oxygen-carrying protein - anemia",
                          "Blood test"),
        HealthcareFeature("med.platelet_count", "Platelet Count", HealthcareSystem.MEDICAL,
                          (150, 400), "×10⁹/L", "Clotting cells - thrombocytopenia",
                          "Blood test"),
        HealthcareFeature("med.creatinine", "Serum Creatinine", HealthcareSystem.MEDICAL,
                          (30, 120), "µmol/L", "Kidney function marker",
                          "Blood test"),
        HealthcareFeature("med.alt_ast", "ALT/AST", HealthcareSystem.MEDICAL,
                          (0, 40), "U/L", "Liver enzymes - hepatocyte damage",
                          "Blood test"),
        HealthcareFeature("med.hba1c", "HbA1c", HealthcareSystem.MEDICAL,
                          (4, 15), "%", "Glycated hemoglobin - diabetes control",
                          "Blood test"),


        # ============ PHARMACEUTICAL (25 features) ============
        PharmaFeature("pharm.bioavailability", "Bioavailability", PharmaSystem.PHARMACEUTICAL,
                      (0, 100), "%", "Fraction reaching systemic circulation",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.half_life", "Half-Life", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "hours", "Time to 50% concentration decline",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.volume_distribution", "Volume of Distribution", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "L", "Apparent distribution space",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.clearance", "Clearance", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "mL/min", "Drug elimination rate",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.therapeutic_index", "Therapeutic Index", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "ratio", "LD50/ED50 - safety margin",
                      "Pharmacology"),
        PharmaFeature("pharm.onset_action", "Onset of Action", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "minutes", "Time to first effect",
                      "Pharmacodynamics"),
        PharmaFeature("pharm.duration_action", "Duration of Action", PharmaSystem.PHARMACEUTICAL,
                      (0, 1000), "hours", "Time of clinical effect",
                      "Pharmacodynamics"),
        PharmaFeature("pharm.drug_interaction", "Drug-Drug Interaction", PharmaSystem.PHARMACEUTICAL,
                      (0, 1), "scale", "Pharmacokinetic or pharmacodynamic",
                      "Interaction check"),
        PharmaFeature("pharm.first_pass", "First-Pass Metabolism", PharmaSystem.PHARMACEUTICAL,
                      (0, 100), "%", "Hepatic metabolism before systemic",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.protein_binding", "Protein Binding", PharmaSystem.PHARMACEUTICAL,
                      (0, 100), "%", "Bound to albumin - affects distribution",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.enteral_absorption", "Enteral Absorption", PharmaSystem.PHARMACEUTICAL,
                      (0, 100), "%", "GI tract absorption efficiency",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.parenteral_bioavailability", "Parenteral Bioavailability", PharmaSystem.PHARMACEUTICAL,
                      (0, 100), "%", "IV, IM, SC absorption - bypasses gut",
                      "Pharmacokinetics"),
        PharmaFeature("pharm.metabolite_active", "Active Metabolite", PharmaSystem.PHARMACEUTICAL,
                      (0, 1), "scale", "Pro-drug activation or inactive metabolite",
                      "Metabolism"),
        PharmaFeature("pharm.excretion_route", "Excretion Route", PharmaSystem.PHARMACEUTICAL,
                      (0, 3), "type", "Renal, biliary, pulmonary, dermal",
                      "Excretion"),
        PharmaFeature("pharm.acute_toxicity", "Acute Toxicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 5), "scale", "LD50 in animals - immediate harm",
                          "Toxicology"),
        PharmaFeature("pharm.chronic_toxicity", "Chronic Toxicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "Long-term organ damage",
                          "Toxicology"),
        PharmaFeature("pharm.carcinogenicity", "Carcinogenicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "Cancer-causing potential",
                          "Toxicology"),
        PharmaFeature("pharm.teratogenicity", "Teratogenicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "Birth defect risk - FDA categories",
                          "Toxicology"),
        PharmaFeature("pharm.mutagenicity", "Mutagenicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "DNA damage potential",
                          "Toxicology"),
        PharmaFeature("pharm.allergenicity", "Allergenicity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "Immune-mediated hypersensitivity",
                          "Immunology"),
        PharmaFeature("pharm.photosensitivity", "Photosensitivity", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "UV-triggered skin reaction",
                          "Adverse effect"),
        PharmaFeature("pharm.drug_resistance", "Drug Resistance", PharmaSystem.PHARMACEUTICAL,
                          (0, 1), "scale", "Target modification or efflux",
                          "Antimicrobial"),
        PharmaFeature("pharm.formulation_stability", "Formulation Stability", PharmaSystem.PHARMACEUTICAL,
                          (0, 36), "months", "Shelf life under storage conditions",
                          "Pharmaceutical"),
        PharmaFeature("pharm.admin_route", "Administration Route", PharmaSystem.PHARMACEUTICAL,
                          (0, 10), "type", "Oral, IV, IM, SC, topical, inhaled",
                          "Dosage form"),
        PharmaFeature("pharm.dosage_form", "Dosage Form", PharmaSystem.PHARMACEUTICAL,
                          (0, 20), "type", "Tablet, capsule, liquid, injection, patch",
                          "Pharmaceutical"),


        # ============ MENTAL HEALTH (25 features) ============
        MentalFeature("mental.depression_score", "Depression Score (PHQ-9)", MentalSystem.MENTAL_HEALTH,
                      (0, 27), "score", "Patient Health Questionnaire - depression severity",
                      "Screening"),
        MentalFeature("mental.anxiety_score", "Anxiety Score (GAD-7)", MentalSystem.MENTAL_HEALTH,
                      (0, 21), "score", "Generalized Anxiety Disorder scale",
                      "Screening"),
        MentalFeature("mental.suicide_risk", "Suicide Risk Level", MentalSystem.MENTAL_HEALTH,
                      (0, 4), "level", "Low, moderate, high, imminent",
                      "Risk assessment"),
        MentalFeature("mental.manic_severity", "Manic Severity (YMRS)", MentalSystem.MENTAL_HEALTH,
                      (0, 60), "score", "Young Mania Rating Scale",
                      "Assessment"),
        MentalFeature("mental.psychosis_score", "Psychosis Score (PANSS)", MentalSystem.MENTAL_HEALTH,
                      (30, 210), "score", "Positive and Negative Syndrome Scale",
                      "Assessment"),
        MentalFeature("mental.ocd_severity", "OCD Severity (Y-BOCS)", MentalSystem.MENTAL_HEALTH,
                      (0, 40), "score", "Yale-Brown Obsessive Compulsive Scale",
                      "Assessment"),
        MentalFeature("mental.ptsd_score", "PTSD Score (PCL-5)", MentalSystem.MENTAL_HEALTH,
                      (0, 80), "score", "PTSD Checklist - DSM-5",
                      "Screening"),
        MentalFeature("mental.eating_disorder", "Eating Disorder Severity", MentalSystem.MENTAL_HEALTH,
                      (0, 1), "scale", "Anorexia, bulimia, binge-eating severity",
                      "Assessment"),
        MentalFeature("mental.substance_use", "Substance Use Severity", MentalSystem.MENTAL_HEALTH,
                      (0, 1), "scale", "AUDIT, DAST for alcohol/drugs",
                      "Screening"),
        MentalFeature("mental.adhd_inattentive", "ADHD Inattentive Symptoms", MentalSystem.MENTAL_HEALTH,
                      (0, 9), "count", "DSM-5 inattentive criteria count",
                      "Diagnosis"),
        MentalFeature("mental.adhd_hyperactive", "ADHD Hyperactive Symptoms", MentalSystem.MENTAL_HEALTH,
                      (0, 9), "count", "DSM-5 hyperactive criteria count",
                      "Diagnosis"),
        MentalFeature("mental.autism_severity", "Autism Severity Level", MentalSystem.MENTAL_HEALTH,
                      (0, 3), "level", "Level 1-3 requiring support",
                      "Diagnosis"),
        MentalFeature("mental.personality_disorder", "Personality Disorder Traits", MentalSystem.MENTAL_HEALTH,
                      (0, 10), "type", "Cluster A, B, C personality patterns",
                          "Diagnosis"),
        MentalFeature("mental.dissociation_level", "Dissociation Level", MentalSystem.MENTAL_HEALTH,
                      (0, 1), "scale", "Dissociative experiences - DES-II",
                      "Assessment"),
        MentalFeature("mental.trauma_exposure", "Trauma Exposure Level", MentalSystem.MENTAL_HEALTH,
                      (0, 10), "count", "Types of traumatic experiences",
                          "History"),
        MentalFeature("mental.insomnia_severity", "Insomnia Severity", MentalSystem.MENTAL_HEALTH,
                      (0, 28), "score", "ISI - Insomnia Severity Index",
                      "Assessment"),
        MentalFeature("mental.cognitive_impairment", "Cognitive Impairment", MentalSystem.MENTAL_HEALTH,
                      (0, 30), "MMSE", "Mini-Mental State Examination",
                      "Screening"),
        MentalFeature("mental.executive_function", "Executive Function", MentalSystem.MENTAL_HEALTH,
                      (0, 100), "%", "Working memory, inhibition, shifting",
                          "Assessment"),
        MentalFeature("mental.processing_speed", "Processing Speed", MentalSystem.MENTAL_HEALTH,
                      (0, 200), "score", "Symbol search, coding speed",
                          "Neuropsych"),
        MentalFeature("mental.verbal_memory", "Verbal Memory", MentalSystem.MENTAL_HEALTH,
                      (0, 100), "%", "Word list learning and recall",
                          "Neuropsych"),
        MentalFeature("mental.visuospatial", "Visuospatial Ability", MentalSystem.MENTAL_HEALTH,
                      (0, 100), "%", "Clock drawing, figure copy",
                          "Neuropsych"),
        MentalFeature("mental.social_cognition", "Social Cognition", MentalSystem.MENTAL_HEALTH,
                      (0, 1), "scale", "Theory of mind, emotion recognition",
                          "Neuropsych"),
        MentalFeature("mental.insight_level", "Insight Level", MentalSystem.MENTAL_HEALTH,
                      (0, 1), "scale", "Awareness of illness - birch insight scale",
                          "Assessment"),
        MentalFeature("mental.treatment_adherence", "Treatment Adherence", MentalSystem.MENTAL_HEALTH,
                      (0, 100), "%", "Medication compliance - MPR",
                          "Compliance"),
        MentalFeature("mental.functional_capacity", "Functional Capacity", MentalSystem.MENTAL_HEALTH,
                      (0, 100), "%", "GAF or WHODAS - social/occupational function",
                          "Assessment"),


        # ============ PUBLIC HEALTH (30 features) ============
        PublicFeature("pubhealth.infant_mortality", "Infant Mortality Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "/1000", "Deaths under 1 year per 1000 live births",
                      "Vital statistics"),
        PublicFeature("pubhealth.maternal_mortality", "Maternal Mortality Ratio", PublicSystem.PUBLIC_HEALTH,
                      (0, 2000), "/100000", "Pregnancy-related deaths per 100k",
                      "Vital statistics"),
        PublicFeature("pubhealth.life_expectancy", "Life Expectancy at Birth", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "years", "Average lifespan at birth",
                      "Life table"),
        PublicFeature("pubhealth.healthy_life", "Healthy Life Expectancy", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "years", "Disability-free years",
                      "DALY"),
        PublicFeature("pubhealth.mortality_rate", "Age-Standardized Mortality Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 2000), "/100000", "All-cause mortality - standardized",
                      "Vital statistics"),
        PublicFeature("pubhealth.morbidity_rate", "Morbidity Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "%", "Prevalence of disease in population",
                      "Epidemiology"),
        PublicFeature("pubhealth.disease_prevalence", "Disease Prevalence", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "%", "Existing cases in population",
                      "Epidemiology"),
        PublicFeature("pubhealth.disease_incidence", "Disease Incidence", PublicSystem.PUBLIC_HEALTH,
                      (0, 1000), "/100000", "New cases per period",
                      "Epidemiology"),
        PublicFeature("pubhealth.vaccination_coverage", "Vaccination Coverage", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "%", "DTP3, measles immunization rate",
                      "Immunization"),
        PublicFeature("pubhealth.screening_rate", "Cancer Screening Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "%", "Mammography, colonoscopy, Pap smear",
                      "Screening programs"),
        PublicFeature("pubhealth.health_expenditure", "Health Expenditure per Capita", PublicSystem.PUBLIC_HEALTH,
                      (0, 10000), "USD", "Total health spending per person",
                      "Health accounts"),
        PublicFeature("pubhealth.health_workers", "Health Workers per 1000", PublicSystem.PUBLIC_HEALTH,
                      (0, 50), "/1000", "Physicians, nurses per population",
                      "Workforce"),
        PublicFeature("pubhealth.hospital_beds", "Hospital Beds per 1000", PublicSystem.PUBLIC_HEALTH,
                      (0, 20), "/1000", "Acute care beds per population",
                      "Infrastructure"),
        PublicFeature("pubhealth.physician_density", "Physician Density", PublicSystem.PUBLIC_HEALTH,
                      (0, 10), "/1000", "Doctors per 1000 population",
                      "Workforce"),
        PublicFeature("pubhealth.nurse_density", "Nurse Density", PublicSystem.PUBLIC_HEALTH,
                      (0, 20), "/1000", "Nurses per 1000 population",
                      "Workforce"),
        PublicFeature("pubhealth.access_to_care", "Access to Care Index", PublicSystem.PUBLIC_HEALTH,
                      (0, 1), "score", "Financial and geographic access",
                      "Survey"),
        PublicFeature("pubhealth.quality_of_care", "Quality of Care Index", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "score", "Process and outcome measures",
                      "Assessment"),
        PublicFeature("pubhealth.readmission_rate", "30-Day Readmission Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 50), "%", "Hospital readmission within 30 days",
                      "Quality"),
        PublicFeature("pubhealth.surgical_mortality", "Surgical Mortality Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 10), "%", "Death within 30 days of surgery",
                          "Quality"),
        PublicFeature("pubhealth.nosocomial_infection", "Nosocomial Infection Rate", PublicSystem.PUBLIC_HEALTH,
                      (0, 20), "%", "Hospital-acquired infection rate",
                          "Infection control"),
        PublicFeature("pubhealth.antimicrobial_resistance", "Antimicrobial Resistance", PublicSystem.PUBLIC_HEALTH,
                      (0, 1), "scale", "AMR prevalence - WHO priority pathogens",
                          "Surveillance"),
        PublicFeature("pubhealth.food_safety", "Food Safety Index", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "score", "Foodborne illness incidence",
                          "Surveillance"),
        PublicFeature("pubhealth.water_quality", "Water Quality Compliance", PublicSystem.PUBLIC_HEALTH,
                      (0, 100), "%", "Safe water access - WHO standards",
                          "Infrastructure"),
        PublicFeature("pubhealth.air_quality", "Air Quality Index", PublicSystem.PUBLIC_HEALTH,
                          (0, 500), "AQI", "PM2.5, ozone, NO2 - health impact",
                          "Monitoring"),
        PublicFeature("pubhealth.tobacco_use", "Tobacco Use Prevalence", PublicSystem.PUBLIC_HEALTH,
                          (0, 50), "%", "Adult smoking rate",
                          "Survey"),
        PublicFeature("pubhealth.alcohol_use", "Alcohol Use Rate", PublicSystem.PUBLIC_HEALTH,
                          (0, 50), "%", "Heavy drinking prevalence",
                          "Survey"),
        PublicFeature("pubhealth.physical_inactivity", "Physical Inactivity Rate", PublicSystem.PUBLIC_HEALTH,
                          (0, 100), "%", "Insufficient activity level",
                          "Survey"),
        PublicFeature("pubhealth.obesity_rate", "Adult Obesity Rate", PublicSystem.PUBLIC_HEALTH,
                          (0, 50), "%", "BMI ≥ 30 prevalence",
                          "Survey"),
        PublicFeature("pubhealth.diabetes_prevalence", "Diabetes Prevalence", PublicSystem.PUBLIC_HEALTH,
                          (0, 30), "%", "Diabetes in adult population",
                          "Survey"),
        PublicFeature("pubhealth.hypertension_prevalence", "Hypertension Prevalence", PublicSystem.PUBLIC_HEALTH,
                          (0, 50), "%", "Elevated blood pressure in adults",
                          "Survey"),


        # ============ NUTRITIONAL (40 features) ============
        NutrFeature("nutr.caloric_intake", "Caloric Intake", NutrSystem.NUTRITIONAL,
                   (500, 5000), "kcal/day", "Daily energy consumption",
                   "Food record"),
        NutrFeature("nutr.protein_intake", "Protein Intake", NutrSystem.NUTRITIONAL,
                   (0, 300), "g/day", "Daily protein consumption",
                   "Food record"),
        NutrFeature("nutr.carbohydrate_intake", "Carbohydrate Intake", NutrSystem.NUTRITIONAL,
                   (0, 500), "g/day", "Daily carb consumption",
                   "Food record"),
        NutrFeature("nutr.fat_intake", "Fat Intake", NutrSystem.NUTRITIONAL,
                   (0, 200), "g/day", "Daily fat consumption",
                   "Food record"),
        NutrFeature("nutr.fiber_intake", "Fiber Intake", NutrSystem.NUTRITIONAL,
                   (0, 50), "g/day", "Dietary fiber - recommended 25-30g",
                   "Food record"),
        NutrFeature("nutr.sugar_intake", "Added Sugar Intake", NutrSystem.NUTRITIONAL,
                   (0, 200), "g/day", "Free sugars - WHO recommends <10%",
                   "Food record"),
        NutrFeature("nutr.sodium_intake", "Sodium Intake", NutrSystem.NUTRITIONAL,
                   (0, 10000), "mg/day", "Salt equivalent - WHO <2000mg",
                   "Food record"),
        NutrFeature("nutr.potassium_intake", "Potassium Intake", NutrSystem.NUTRITIONAL,
                   (0, 10000), "mg/day", "Recommended 3500-4700mg",
                   "Food record"),
        NutrFeature("nutr.vitamin_a", "Vitamin A Intake", NutrSystem.NUTRITIONAL,
                   (0, 3000), "µg/RAE", "Retinol activity equivalents",
                   "Food analysis"),
        NutrFeature("nutr.vitamin_c", "Vitamin C Intake", NutrSystem.NUTRITIONAL,
                   (0, 2000), "mg/day", "Ascorbic acid - recommended 75-90mg",
                   "Food analysis"),
        NutrFeature("nutr.vitamin_d", "Vitamin D Intake", NutrSystem.NUTRITIONAL,
                   (0, 100), "µg/day", "Cholecalciferol - recommended 15-20µg",
                   "Food analysis"),
        NutrFeature("nutr.vitamin_e", "Vitamin E Intake", NutrSystem.NUTRITIONAL,
                   (0, 1000), "mg", "Alpha-tocopherol - recommended 15mg",
                   "Food analysis"),
        NutrFeature("nutr.vitamin_k", "Vitamin K Intake", NutrSystem.NUTRITIONAL,
                   (0, 500), "µg/day", "Phylloquinone - recommended 90-120µg",
                   "Food analysis"),
        NutrFeature("nutr.vitamin_b12", "Vitamin B12 Intake", NutrSystem.NUTRITIONAL,
                   (0, 100), "µg/day", "Cobalamin - recommended 2.4µg",
                   "Food analysis"),
        NutrFeature("nutr.folate", "Folate Intake", NutrSystem.NUTRITIONAL,
                   (0, 1000), "µg/DFE", "Dietary folate equivalents - recommended 400µg",
                   "Food analysis"),
        NutrFeature("nutr.iron_intake", "Iron Intake", NutrSystem.NUTRITIONAL,
                   (0, 100), "mg/day", "Recommended 8-18mg - heme vs non-heme",
                   "Food analysis"),
        NutrFeature("nutr.zinc_intake", "Zinc Intake", NutrSystem.NUTRITIONAL,
                   (0, 40), "mg/day", "Recommended 8-11mg",
                   "Food analysis"),
        NutrFeature("nutr.calcium_intake", "Calcium Intake", NutrSystem.NUTRITIONAL,
                   (0, 2500), "mg/day", "Recommended 1000-1200mg",
                   "Food analysis"),
        NutrFeature("nutr.magnesium_intake", "Magnesium Intake", NutrSystem.NUTRITIONAL,
                   (0, 500), "mg/day", "Recommended 310-420mg",
                   "Food analysis"),
        NutrFeature("nutr.omega3_intake", "Omega-3 Fatty Acid Intake", NutrSystem.NUTRITIONAL,
                   (0, 10), "g/day", "EPA+DHA - recommended 250-500mg",
                   "Food analysis"),
        NutrFeature("nutr.omega6_intake", "Omega-6 Fatty Acid Intake", NutrSystem.NUTRITIONAL,
                   (0, 50), "g/day", "Linoleic acid - ratio with omega-3",
                   "Food analysis"),
        NutrFeature("nutr.trans_fat_intake", "Trans Fat Intake", NutrSystem.NUTRITIONAL,
                   (0, 10), "g/day", "Industrial trans - recommend <2g",
                   "Food analysis"),
        NutrFeature("nutr.cholesterol_intake", "Cholesterol Intake", NutrSystem.NUTRITIONAL,
                   (0, 1000), "mg/day", "Dietary cholesterol - no limit in new guidelines",
                   "Food analysis"),
        NutrFeature("nutr.water_intake", "Water Intake", NutrSystem.NUTRITIONAL,
                   (0, 10), "L/day", "Total water from all sources",
                   "Assessment"),
        NutrFeature("nutr.caffeine_intake", "Caffeine Intake", NutrSystem.NUTRITIONAL,
                   (0, 1000), "mg/day", "Coffee, tea, energy drinks - safe <400mg",
                   "Food record"),
        NutrFeature("nutr.alcohol_intake", "Alcohol Intake", NutrSystem.NUTRITIONAL,
                   (0, 20), "standard drinks", "Ethanol grams per day - recommended limits",
                   "Food record"),
        NutrFeature("nutr.food_variety", "Food Variety Score", NutrSystem.NUTRITIONAL,
                   (0, 50), "foods", "Different foods consumed per week",
                   "Food frequency"),
        NutrFeature("nutr.fruit_veg_intake", "Fruit and Vegetable Intake", NutrSystem.NUTRITIONAL,
                   (0, 20), "servings/day", "Recommended 5-9 servings",
                   "Food record"),
        NutrFeature("nutr.whole_grain_intake", "Whole Grain Intake", NutrSystem.NUTRITIONAL,
                   (0, 200), "g/day", "Recommended 25-50g fiber from whole grains",
                   "Food record"),
        NutrFeature("nutr.processed_food", "Processed Food Consumption", NutrSystem.NUTRITIONAL,
                   (0, 100), "%", "Ultra-processed food energy share",
                   "NOVA classification"),
        NutrFeature("nutr.fast_food", "Fast Food Consumption", NutrSystem.NUTRITIONAL,
                   (0, 20), "meals/week", "Frequency of fast food meals",
                   "Food frequency"),
        NutrFeature("nutr.sugar_sweetened", "Sugar-Sweetened Beverage", NutrSystem.NUTRITIONAL,
                   (0, 10), "drinks/day", "Soft drinks, fruit drinks",
                   "Food frequency"),
        NutrFeature("nutr.diet_quality_score", "Diet Quality Score (HEI)", NutrSystem.NUTRITIONAL,
                   (0, 100), "score", "Healthy Eating Index - diet quality",
                   "Assessment"),
        NutrFeature("nutr.mediterranean_adherence", "Mediterranean Diet Adherence", NutrSystem.NUTRITIONAL,
                   (0, 9), "score", "MEDAS - 9-item score",
                   "Questionnaire"),
        NutrFeature("nutr.dash_adherence", "DASH Diet Adherence", NutrSystem.NUTRITIONAL,
                   (0, 10), "score", "DASH score - blood pressure diet",
                   "Questionnaire"),
        NutrFeature("nutr.gluten_free", "Gluten-Free Diet", NutrSystem.NUTRITIONAL,
                   (0, 1), "binary", "Celiac disease or wheat sensitivity",
                   "Diet"),
        NutrFeature("nutr.ketogenic_adherence", "Ketogenic Diet Adherence", NutrSystem.NUTRITIONAL,
                   (0, 1), "scale", "Low-carb high-fat - therapeutic",
                   "Diet"),
        NutrFeature("nutr.intermittent_fasting", "Intermittent Fasting", NutrSystem.NUTRITIONAL,
                   (0, 1), "scale", "Time-restricted eating patterns",
                   "Diet"),
        NutrFeature("nutr.hydration_status", "Hydration Status", NutrSystem.NUTRITIONAL,
                   (0, 1), "scale", "Serum osmolality or urine color",
                   "Biomarker"),
        NutrFeature("nutr.malnutrition_risk", "Malnutrition Risk", NutrSystem.NUTRITIONAL,
                   (0, 1), "scale", "MNA or MUST screening",
                   "Clinical"),
    ]
    
    for f in features:
        HEALTHCARE_FEATURES[f.feature_id] = f


_register_healthcare_features()


def get_healthcare_feature(feature_id: str) -> HealthcareFeature:
    return HEALTHCARE_FEATURES.get(feature_id)


def get_healthcare_feature_count() -> int:
    return len(HEALTHCARE_FEATURES)


# ============================================================================
# Pharmaceutical System
# ============================================================================

class PharmaSystem(Enum):
    PHARMACEUTICAL = auto()


class PharmaFeature:
    pass  # Placeholder - would be similar structure


# ============================================================================
# Mental Health System
# ============================================================================

class MentalSystem(Enum):
    MENTAL_HEALTH = auto()


class MentalFeature:
    pass  # Placeholder - would be similar structure


# ============================================================================
# Public Health System
# ============================================================================

class PublicSystem(Enum):
    PUBLIC_HEALTH = auto()


class PublicFeature:
    pass  # Placeholder - would be similar structure


# ============================================================================
# Nutritional System
# ============================================================================

class NutrSystem(Enum):
    NUTRITIONAL = auto()


class NutrFeature:
    pass  # Placeholder - would be similar structure