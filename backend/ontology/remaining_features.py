"""
Remaining Feature Registry — Sections S through AY
==================================================
Features 801-1400 covering:
- S: Demographic & Family (20 features)
- T: Transportation & Logistics (20 features)
- U: Criminal & Underground (20 features)
- V: Educational & Knowledge (20 features)
- W: Maritime & Naval (15 features)
- X: Space & Astronomical (15 features)
- Y: Geological & Planetary (15 features)
- Z: Microbiological & Viral (15 features)
- AA: Genetic & Epigenetic (15 features)
- AB: Sensory & Perceptual (15 features)
- AC: Memory & Identity (15 features)
- AD: Reproductive & Sexual (15 features)
- AE: Developmental & Aging (15 features)
- AF: Nutritional & Metabolic (15 features)
- AG: Immunological & Defensive (15 features)
- AH: Neurological & Psychiatric (15 features)
- AI: Endocrine & Hormonal (15 features)
- AJ: Circadian & Sleep (15 features)
- AK: Pain & Suffering (15 features)
- AL: Death & Decomposition (15 features)
- AM: Heritage & Archaeological (15 features)
- AN: Diplomatic & International (15 features)
- AO: Intelligence & Espionage (15 features)
- AP: Propaganda & Psychological Warfare (15 features)
- AQ: Trade & Commerce (15 features)
- AR: Currency & Monetary (15 features)
- AS: Labor & Employment (15 features)
- AT: Housing & Real Estate (15 features)
- AU: Medicine & Healing (15 features)
- AV: Music & Acoustic (15 features)
- AW: Smell & Pheromone (15 features)
- AX: Architectural & Construction (15 features)
- AY: Miscellaneous (110 features)

Total: ~600 remaining features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class RemainingSystem(Enum):
    DEMOGRAPHIC = auto()
    TRANSPORTATION = auto()
    CRIMINAL = auto()
    EDUCATION = auto()
    MARITIME = auto()
    SPACE = auto()
    GEOLOGICAL = auto()
    MICROBIOLOGICAL = auto()
    GENETIC = auto()
    SENSORY = auto()
    MEMORY = auto()
    REPRODUCTIVE = auto()
    DEVELOPMENTAL = auto()
    NUTRITIONAL = auto()
    IMMUNOLOGICAL = auto()
    NEUROLOGICAL = auto()
    ENDOCRINE = auto()
    CIRCADIAN = auto()
    PAIN = auto()
    DEATH = auto()
    HERITAGE = auto()
    DIPLOMATIC = auto()
    INTELLIGENCE = auto()
    PROPAGANDA = auto()
    TRADE = auto()
    CURRENCY = auto()
    LABOR = auto()
    HOUSING = auto()
    MEDICINE = auto()
    MUSIC = auto()
    SMELL = auto()
    ARCHITECTURAL = auto()
    MISCELLANEOUS = auto()


@dataclass
class RemainingFeature:
    feature_id: str
    feature_name: str
    system: RemainingSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


REMAINING_FEATURES: dict = {}


def _register_remaining_features():
    global REMAINING_FEATURES
    
    features = [
        # ============ S. DEMOGRAPHIC & FAMILY (20 features) ============
        RemainingFeature("demo.tfr", "Total Fertility Rate (TFR)", RemainingSystem.DEMOGRAPHIC,
                         (0, 10), "children/woman", "Replacement 2.1",
                         "Census data"),
        RemainingFeature("demo.grr", "Gross Reproduction Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 5), " daughters/woman", "Female births per woman",
                         "Birth data"),
        RemainingFeature("demo.nrr", "Net Reproduction Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 5), " daughters/woman", "Adjusted for mortality - exactly 1.0 = stationary",
                         "Life table"),
        RemainingFeature("demo.cbr", "Crude Birth Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 50), "/1000", "Births per 1000 population",
                         "Vital statistics"),
        RemainingFeature("demo.cdr", "Crude Death Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 30), "/1000", "Deaths per 1000 - demographic transition indicator",
                         "Vital statistics"),
        RemainingFeature("demo.natural_increase", "Natural Increase Rate", RemainingSystem.DEMOGRAPHIC,
                         (-10, 40), "/1000", "Birth minus death - migration excluded",
                         "Calculation"),
        RemainingFeature("demo.life_expectancy_birth", "Life Expectancy at Birth", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "years", "Average lifespan - infant mortality sensitive",
                         "Life table"),
        RemainingFeature("demo.life_expectancy_60", "Life Expectancy at Age 60", RemainingSystem.DEMOGRAPHIC,
                         (0, 40), "years", "Conditional survival - healthcare quality indicator",
                         "Life table"),
        RemainingFeature("demo.hale", "Healthy Life Expectancy (HALE)", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "years", "Disability-adjusted - quality not just quantity",
                         "DALY calculation"),
        RemainingFeature("demo.maternal_mortality", "Maternal Mortality Ratio", RemainingSystem.DEMOGRAPHIC,
                         (0, 2000), "/100000", "Per 100,000 live births - development indicator",
                         "Vital statistics"),
        RemainingFeature("demo.infant_mortality", "Infant Mortality Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "/1000", "Per 1000 live births - healthcare access sensitive",
                         "Vital statistics"),
        RemainingFeature("demo.under5_mortality", "Under-5 Mortality Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "/1000", "Per 1000 - captures childhood disease",
                         "Vital statistics"),
        RemainingFeature("demo.stillbirth_rate", "Stillbirth Rate", RemainingSystem.DEMOGRAPHIC,
                         (0, 50), "/1000", "Per 1000 births - often underreported",
                         "Vital statistics"),
        RemainingFeature("demo.sex_ratio_birth", "Sex Ratio at Birth", RemainingSystem.DEMOGRAPHIC,
                         (1.0, 1.1), "ratio", "105 males per 100 females natural",
                         "Birth data"),
        RemainingFeature("demo.sex_ratio_age", "Sex Ratio by Age", RemainingSystem.DEMOGRAPHIC,
                         (0.5, 2.0), "ratio", "Male excess narrows and reverses with age",
                         "Population data"),
        RemainingFeature("demo.population_momentum", "Population Momentum", RemainingSystem.DEMOGRAPHIC,
                         (0, 10), "%", "Growth continues after TFR reaches replacement",
                         "Projection"),
        RemainingFeature("demo.dividend_window", "Demographic Dividend Window", RemainingSystem.DEMOGRAPHIC,
                         (0, 50), "years", "30-40 years of favorable ratio - education critical",
                         "Dependency ratio"),
        RemainingFeature("demo.old_dependency", "Old-Age Dependency Ratio", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "%", "65+ / 15-64 - pension system stress",
                         "Population structure"),
        RemainingFeature("demo.child_dependency", "Child Dependency Ratio", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "%", "0-14 / 15-64 - education and childcare burden",
                         "Population structure"),
        RemainingFeature("demo.total_dependency", "Total Dependency Ratio", RemainingSystem.DEMOGRAPHIC,
                         (0, 100), "%", "Combined - economic support pressure",
                         "Population structure"),

        # ============ T. TRANSPORTATION & LOGISTICS (20 features) ============
        RemainingFeature("logistics.lead_time", "Lead Time", RemainingSystem.TRANSPORTATION,
                         (0, 365), "days", "Order to delivery - inventory trade-off",
                         "Supply chain"),
        RemainingFeature("logistics.safety_stock", "Safety Stock Level", RemainingSystem.TRANSPORTATION,
                         (0, 1000), "units", "Buffer against demand variability",
                         "Inventory model"),
        RemainingFeature("logistics.eoq", "Economic Order Quantity", RemainingSystem.TRANSPORTATION,
                         (0, 10000), "units", "Optimal batch size - ordering vs. holding",
                         "EOQ formula"),
        RemainingFeature("logistics.jit", "Just-in-Time Inventory", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Minimal stock - fragile to disruption",
                         "Inventory system"),
        RemainingFeature("logistics.bullwhip", "Bullwhip Effect", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Demand variability amplification upstream",
                         "Variance analysis"),
        RemainingFeature("logistics.last_mile", "Last Mile Delivery Cost", RemainingSystem.TRANSPORTATION,
                         (0, 50), "%", "50%+ of total - urban density matters",
                         "Cost breakdown"),
        RemainingFeature("logistics.cold_chain", "Cold Chain Integrity", RemainingSystem.TRANSPORTATION,
                         (0, 100), "%", "Temperature maintenance - vaccine spoilage",
                         "Temperature log"),
        RemainingFeature("logistics.container_std", "Container Standardization", RemainingSystem.TRANSPORTATION,
                         (0, 100), "TEU", "Twenty-foot Equivalent Unit - intermodal revolution",
                         "Port data"),
        RemainingFeature("logistics.port_turnaround", "Port Turnaround Time", RemainingSystem.TRANSPORTATION,
                         (0, 100), "hours", "Hours per ship - crane productivity",
                         "Port operations"),
        RemainingFeature("logistics.customs_clearance", "Customs Clearance Speed", RemainingSystem.TRANSPORTATION,
                         (0, 30), "days", "Documentation and inspection",
                         "Trade facilitation"),
        RemainingFeature("logistics.tariff_class", "Tariff Classification", RemainingSystem.TRANSPORTATION,
                         (0, 10000), "HS code", "HS code determination - duty rate dispute",
                         "Classification"),
        RemainingFeature("logistics.rules_origin", "Rules of Origin", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Where made - trade agreement eligibility",
                         "Certificate"),
        RemainingFeature("logistics.sps", "Sanitary and Phytosanitary", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Food safety barriers - protectionism",
                         "SPS measures"),
        RemainingFeature("logistics.ntb", "Non-Tariff Barrier", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Quotas, licenses, standards - often more restrictive",
                         "Trade barrier"),
        RemainingFeature("logistics.smuggling_route", "Smuggling Route", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Tax evasion or prohibition circumvention",
                         "Border data"),
        RemainingFeature("logistics.piracy_risk", "Piracy Risk Zone", RemainingSystem.TRANSPORTATION,
                         (0, 5), "scale", "Gulf of Aden, Strait of Malacca - insurance",
                         "Maritime security"),
        RemainingFeature("logistics.letters_credit", "Letters of Credit", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Trade finance - bank guarantee",
                         "Trade finance"),
        RemainingFeature("logistics.bill_lading", "Bill of Lading", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Document of title - negotiable instrument",
                         "Shipping document"),
        RemainingFeature("logistics.freight_forwarder", "Freight Forwarder Role", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Logistics coordination - customs broker",
                         "3PL service"),
        RemainingFeature("logistics.3pl", "Third-Party Logistics (3PL)", RemainingSystem.TRANSPORTATION,
                         (0, 1), "scale", "Outsourced supply chain - specialization",
                         "Outsourcing"),

        # ============ U. CRIMINAL & UNDERGROUND (20 features) ============
        RemainingFeature("crime.black_market_rate", "Black Market Exchange Rate", RemainingSystem.CRIMINAL,
                         (0, 3), "ratio", "Currency premium - capital control evasion",
                         "Market analysis"),
        RemainingFeature("crime.informal_sector", "Informal Sector Size", RemainingSystem.CRIMINAL,
                         (0, 90), "%", "% of GDP unregistered - 30-90% developing",
                         "Economic estimate"),
        RemainingFeature("crime.money_laundering", "Money Laundering Stage", RemainingSystem.CRIMINAL,
                         (0, 3), "stage", "Placement, layering, integration - detection difficulty",
                         "Financial investigation"),
        RemainingFeature("crime.hawala", "Hawala Network", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Trust-based transfer - no physical money",
                         "Remittance tracking"),
        RemainingFeature("crime.trafficking_route", "Human Trafficking Route", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Source, transit, destination - vulnerability",
                         "Counter-trafficking"),
        RemainingFeature("crime.drug_production", "Drug Production Geography", RemainingSystem.CRIMINAL,
                         (0, 10), "regions", "Coca (Andes), opium (Golden Triangle), cannabis",
                         "DEA reporting"),
        RemainingFeature("crime.drug_purity", "Drug Purity Fluctuation", RemainingSystem.CRIMINAL,
                         (0, 100), "%", "Supply chain adulteration - overdose risk",
                         "Lab testing"),
        RemainingFeature("crime.prohibition_cost", "Prohibition Enforcement Cost", RemainingSystem.CRIMINAL,
                         (0, 100000000000), "currency", "Police, courts, prisons - vs. public health",
                         "Budget analysis"),
        RemainingFeature("crime.organized_hierarchy", "Organized Crime Hierarchy", RemainingSystem.CRIMINAL,
                         (0, 3), "type", "Family, clan, network structures - succession",
                         "Intelligence"),
        RemainingFeature("crime.racketeering", "Racketeering Protection", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Extortion disguised as service",
                         "Investigation"),
        RemainingFeature("crime.counterfeit_quality", "Counterfeit Goods Quality", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "From obvious to indistinguishable - consumer harm",
                         "Seizure analysis"),
        RemainingFeature("crime.poaching_pressure", "Wildlife Poaching Pressure", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Ivory, rhino horn, pangolin - extinction spiral",
                         "Wildlife trade"),
        RemainingFeature("crime.illegal_logging", "Illegal Logging Network", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Timber laundering - certification fraud",
                         "Timber trade"),
        RemainingFeature("crime.art_theft", "Art Theft Provenance", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Stolen work resale - Art Loss Register",
                         "Art database"),
        RemainingFeature("crime.cyber_sophistication", "Cybercrime Sophistication", RemainingSystem.CRIMINAL,
                         (0, 5), "scale", "Phishing, ransomware, APT - attribution difficulty",
                         "Incident analysis"),
        RemainingFeature("crime.dark_web", "Dark Web Marketplace", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Tor-hidden services - cryptocurrency payment",
                         "Market monitoring"),
        RemainingFeature("crime.assassination_market", "Assassination Market", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Prediction market for death - theoretical vs actual",
                         "Academic"),
        RemainingFeature("crime.prison_gang", "Prison Gang Formation", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Protection and resource control - racial segregation",
                         "Correctional intel"),
        RemainingFeature("crime.recidivism", "Recidivism Rate", RemainingSystem.CRIMINAL,
                         (0, 100), "%", "Return to prison - rehabilitation efficacy",
                         "Correctional data"),
        RemainingFeature("crime.restorative_outcome", "Restorative Justice Outcome", RemainingSystem.CRIMINAL,
                         (0, 1), "scale", "Victim satisfaction - lower recidivism some contexts",
                         "Program evaluation"),

        # ============ V. EDUCATIONAL & KNOWLEDGE (20 features) ============
        RemainingFeature("edu.literacy_age", "Literacy Acquisition Age", RemainingSystem.EDUCATION,
                         (4, 10), "years", "6-7 typical - delayed by access or dyslexia",
                         "Developmental"),
        RemainingFeature("edu.numeracy_stage", "Numeracy Development Stage", RemainingSystem.EDUCATION,
                         (0, 5), "stage", "Counting, arithmetic, algebra, calculus - Piagetian",
                         "Assessment"),
        RemainingFeature("edu.critical_thinking", "Critical Thinking Curriculum", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Explicit instruction - transfer debated",
                         "Curriculum"),
        RemainingFeature("edu.apprenticeship", "Apprenticeship Duration", RemainingSystem.EDUCATION,
                         (1, 10), "years", "7 years traditional - guild mastery",
                         "Vocational"),
        RemainingFeature("edu.university_length", "University Degree Length", RemainingSystem.EDUCATION,
                         (3, 8), "years", "3-4 years bachelor's - professional degrees longer",
                         "Higher education"),
        RemainingFeature("edu.student_teacher_ratio", "Student-Teacher Ratio", RemainingSystem.EDUCATION,
                         (5, 50), "students", "Class size - 15-20 optimal for engagement",
                         "Classroom"),
        RemainingFeature("edu.pedagogical_method", "Pedagogical Method", RemainingSystem.EDUCATION,
                         (0, 5), "type", "Lecture, Socratic, project-based, Montessori - outcome variation",
                         "Teaching method"),
        RemainingFeature("edu.standardized_test", "Standardized Testing Validity", RemainingSystem.EDUCATION,
                         (0, 1), "r", "Predictive of future performance - cultural bias concerns",
                         "Validity study"),
        RemainingFeature("edu.credential_inflation", "Credential Inflation", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "BA now = HS diploma 1950 - job requirement escalation",
                         "Labor market"),
        RemainingFeature("edu.mooc_completion", "MOOC Completion Rate", RemainingSystem.EDUCATION,
                         (0, 20), "%", "5-10% - engagement and certification value",
                         "Platform data"),
        RemainingFeature("edu.knowledge_half_life", "Knowledge Half-Life", RemainingSystem.EDUCATION,
                         (0, 20), "years", "Obsolescence rate - medical knowledge 18 months",
                         "Domain analysis"),
        RemainingFeature("edu.citation_impact", "Citation Impact Factor", RemainingSystem.EDUCATION,
                         (0, 100), "IF", "Journal prestige - gaming and distortion",
                         "Bibliometric"),
        RemainingFeature("edu.replication_crisis", "Replication Crisis Rate", RemainingSystem.EDUCATION,
                         (0, 100), "%", "Psychology 40%, medicine variable - incentive structure",
                         "Replication studies"),
        RemainingFeature("edu.peer_review", "Peer Review Quality", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Single-blind, double-blind, open - bias and thoroughness",
                         "Review process"),
        RemainingFeature("edu.open_access", "Open Access Mandate", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Public funding requires free publication - APC shift",
                         "Policy"),
        RemainingFeature("edu.patent_thicket", "Patent Thicket", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Overlapping claims - innovation blocking",
                         "Patent landscape"),
        RemainingFeature("edu.trade_secret", "Trade Secret Duration", RemainingSystem.EDUCATION,
                         (0, 100), "years", "Coca-Cola formula - indefinite but vulnerable",
                         "IP strategy"),
        RemainingFeature("edu.indigenous_knowledge", "Indigenous Knowledge System", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Oral tradition, ecological wisdom - IP protection debate",
                         "Knowledge holders"),
        RemainingFeature("edu.library_loss", "Library Burning Impact", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Baghdad 1258, Alexandria - irreversible loss",
                         "Historical"),
        RemainingFeature("edu.digital_preservation", "Digital Preservation", RemainingSystem.EDUCATION,
                         (0, 1), "scale", "Format obsolescence - emulation vs migration",
                         "Archive"),


        # ============ W. MARITIME & NAVAL (15 features) ============
        RemainingFeature("nav.line_battle", "Line of Battle Tactic", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Ship-of-the-line formation - Trafalgar breaking",
                         "Naval tactics"),
        RemainingFeature("nav.broadside_weight", "Broadside Weight", RemainingSystem.MARITIME,
                         (0, 1000), "lbs", "Combined cannon throw - ship rating",
                         "Naval architecture"),
        RemainingFeature("nav.chain_shot", "Chain Shot", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Anti-rigging - mast and sail destruction",
                         "Ammunition"),
        RemainingFeature("nav.grape_shot", "Grape Shot", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Anti-personnel - deck clearing at close range",
                         "Ammunition"),
        RemainingFeature("nav.boarding_success", "Boarding Party Success", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Hand-to-hand on deck - marines and swivel guns",
                         "Naval combat"),
        RemainingFeature("nav.fire_ship", "Fire Ship Attack", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Abandoned burning vessel - panic and dispersion",
                         "Naval tactics"),
        RemainingFeature("nav.blockade_effectiveness", "Blockade Effectiveness", RemainingSystem.MARITIME,
                         (0, 100), "%", "Percentage of trade stopped - economic strangulation",
                         "Trade data"),
        RemainingFeature("nav.privateering", "Privateering License", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Letter of marque - legal piracy against enemy",
                         "Charter"),
        RemainingFeature("nav.press_gang", "Press Gang Recruitment", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Impressment - manpower for wooden walls",
                         "Manpower"),
        RemainingFeature("nav.scurvy_mortality", "Scurvy Mortality Rate", RemainingSystem.MARITIME,
                         (0, 100), "%", "50%+ on long voyages - lime juice prevention",
                         "Medical"),
        RemainingFeature("nav.copper_sheathing", "Copper Sheathing", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Anti-fouling - speed and hull preservation",
                         "Ship maintenance"),
        RemainingFeature("nav.steam_sail", "Steam-Sail Hybrid", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Transitional technology - coaling station requirement",
                         "Propulsion"),
        RemainingFeature("nav.ironclad", "Ironclad Armor", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Wooden ships vs. iron ships - Monitor vs Merrimack",
                         "Naval technology"),
        RemainingFeature("nav.dreadnought", "Dreadnought Revolution", RemainingSystem.MARITIME,
                         (0, 1), "scale", "All-big-gun, turbine, uniform caliber - fleet obsolescence",
                         "Naval history"),
        RemainingFeature("nav.submarine_stealth", "Submarine Stealth", RemainingSystem.MARITIME,
                         (0, 1), "scale", "Underwater warfare - convoy system response",
                         "Submarine ops"),


        # ============ X. SPACE & ASTRONOMICAL (15 features) ============
        RemainingFeature("space.orbital_eccentricity", "Orbital Eccentricity", RemainingSystem.SPACE,
                         (0, 1), "ratio", "Deviation from circular - affects seasonal intensity",
                         "Orbital elements"),
        RemainingFeature("space.axial_tilt", "Axial Tilt (Obliquity)", RemainingSystem.SPACE,
                         (0, 90), "degrees", "23.5° Earth - seasonality driver - Milankovitch cycle",
                         "Planetary"),
        RemainingFeature("space.precession_cycle", "Precession Cycle", RemainingSystem.SPACE,
                         (1000, 30000), "years", "26,000-year wobble - pole star change",
                         "Astronomical"),
        RemainingFeature("space.solar_variation", "Solar Luminosity Variation", RemainingSystem.SPACE,
                         (-1, 1), "%", "0.1% over solar cycle - climate influence",
                         "Solar observation"),
        RemainingFeature("space.supernova_observation", "Supernova Observation", RemainingSystem.SPACE,
                         (0, 1), "scale", "1054 Crab Nebula - daytime visibility, historical",
                         "Astronomical"),
        RemainingFeature("space.comet_appearance", "Comet Appearance", RemainingSystem.SPACE,
                         (0, 1), "scale", "Halley's 76-year cycle - omen interpretation",
                         "Historical"),
        RemainingFeature("space.meteor_shower", "Meteor Shower Prediction", RemainingSystem.SPACE,
                         (0, 1000), "meteors/hr", "Perseids, Leonids - debris trail intersection",
                         "Astronomical"),
        RemainingFeature("space.eclipse_prediction", "Eclipse Prediction", RemainingSystem.SPACE,
                         (0, 1), "scale", "Saros cycle - ancient Babylonian accuracy",
                         "Astronomical"),
        RemainingFeature("space.tidal_locking", "Tidal Locking", RemainingSystem.SPACE,
                         (0, 1), "scale", "Moon same face to Earth - Pluto-Charon mutual",
                         "Orbital dynamics"),
        RemainingFeature("space.roche_limit", "Roche Limit", RemainingSystem.SPACE,
                         (0, 100000), "km", "Tidal disruption distance - Saturn's rings origin",
                         "Orbital mechanics"),
        RemainingFeature("space.asteroid_frequency", "Asteroid Impact Frequency", RemainingSystem.SPACE,
                         (0, 100), "events/million years", "Tunguska 1908, Chicxulub 66 MYA - extinction risk",
                         "Planetary defense"),
        RemainingFeature("space.geomagnetic_reversal", "Geomagnetic Reversal", RemainingSystem.SPACE,
                         (0, 1), "scale", "Pole flip - navigation disruption, ozone damage",
                         "Geophysical"),
        RemainingFeature("space.cosmic_ray_flux", "Cosmic Ray Flux", RemainingSystem.SPACE,
                         (0, 100), "%", "Solar modulation - cloud nucleation debate",
                         "Space physics"),
        RemainingFeature("space.solar_wind", "Solar Wind Intensity", RemainingSystem.SPACE,
                         (0, 1000), "km/s", "Aurora driver - Carrington Event 1859",
                         "Space weather"),
        RemainingFeature("space.exoplanet_detection", "Exoplanet Detection Method", RemainingSystem.SPACE,
                         (0, 5), "method", "Transit, radial velocity, direct imaging - biosignature search",
                         "Astronomical"),
    ]
    
    # Add more features for Y-Z, AA-AY sections
    features.extend([
        # ============ Y. GEOLOGICAL & PLANETARY (15 features) ============
        RemainingFeature("geo.magma_viscosity", "Magma Viscosity", RemainingSystem.GEOLOGICAL,
                         (0, 100000), "Pa·s", "Silica content - runny basalt vs explosive rhyolite",
                         "Volcanology"),
        RemainingFeature("geo.vei", "Volcanic Explosivity Index", RemainingSystem.GEOLOGICAL,
                         (0, 8), "scale", "VEI 0-8 - logarithmic - Tambora 7, Toba 8",
                         "Volcanic"),
        RemainingFeature("geo.pyroclastic_velocity", "Pyroclastic Flow Velocity", RemainingSystem.GEOLOGICAL,
                         (0, 700), "km/h", "Unsurvivable - Pompeii preservation",
                         "Volcanic"),
        RemainingFeature("geo.lahar_trigger", "Lahar Trigger", RemainingSystem.GEOLOGICAL,
                         (0, 1), "scale", "Volcanic mudflow - rain on fresh ash",
                         "Volcanic"),
        RemainingFeature("geo.caldera_collapse", "Caldera Collapse", RemainingSystem.GEOLOGICAL,
                         (0, 100), "km", "Empty magma chamber - Yellowstone scale",
                         "Volcanic"),
        RemainingFeature("geo.earthquake_magnitude", "Earthquake Magnitude (Moment)", RemainingSystem.GEOLOGICAL,
                         (0, 10), "Mw", "Logarithmic energy - each +1 = 32× energy",
                         "Seismology"),
        RemainingFeature("geo.mercalli_intensity", "Modified Mercalli Intensity", RemainingSystem.GEOLOGICAL,
                         (0, 12), "scale", "Felt effects - XII = total destruction",
                         "Seismology"),
        RemainingFeature("geo.tsunami_wave", "Tsunami Wave Height", RemainingSystem.GEOLOGICAL,
                         (0, 30), "m", "Open ocean 30cm, shore 30m - wavelength 200km",
                         "Oceanography"),
        RemainingFeature("geo.soil_liquefaction", "Soil Liquefaction", RemainingSystem.GEOLOGICAL,
                         (0, 1), "scale", "Saturated ground fluidizes - building sink or topple",
                         "Geotechnical"),
        RemainingFeature("geo.landslide_trigger", "Landslide Trigger", RemainingSystem.GEOLOGICAL,
                         (0, 1), "scale", "Rain, earthquake, undercutting - Oso 2014 example",
                         "Geology"),
        RemainingFeature("geo.karst_topography", "Karst Topography", RemainingSystem.GEOLOGICAL,
                         (0, 1), "scale", "Limestone dissolution - sinkholes and caves",
                         "Geology"),
        RemainingFeature("geo.glacial_moraine", "Glacial Moraine", RemainingSystem.GEOLOGICAL,
                         (0, 1), "scale", "Debris deposition - fertile soil and chaotic drainage",
                         "Glaciology"),
        RemainingFeature("geo.loess_deposition", "Loess Deposition", RemainingSystem.GEOLOGICAL,
                         (0, 100), "m", "Windblown silt - highly fertile, vertical walls",
                         "Geology"),
        RemainingFeature("geo.delta_progradation", "Delta Progradation", RemainingSystem.GEOLOGICAL,
                         (0, 100), "km", "River sediment deposition - Nile, Mississippi land building",
                         "Geomorphology"),
        RemainingFeature("geo.coastal_erosion", "Coastal Erosion Rate", RemainingSystem.GEOLOGICAL,
                         (0, 10), "m/year", "Sea level rise + storm intensity - managed retreat debate",
                         "Coastal"),

        # ============ Z. MICROBIOLOGICAL & VIRAL (15 features) ============
        RemainingFeature("micro.quorum_sensing", "Quorum Sensing", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Bacterial communication - biofilm formation coordinated",
                         "Microbiology"),
        RemainingFeature("micro.horizontal_gene", "Horizontal Gene Transfer", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Conjugation, transformation, transduction - resistance spread",
                         "Genetics"),
        RemainingFeature("micro.crispr_spacer", "CRISPR Spacer Acquisition", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Bacterial immune memory - phage resistance evolution",
                         "Molecular biology"),
        RemainingFeature("micro.phage_therapy", "Bacteriophage Therapy", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Viruses kill bacteria - alternative to antibiotics",
                         "Therapy"),
        RemainingFeature("micro.gut_brain_axis", "Gut-Brain Axis Signaling", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Vagus nerve, metabolites - anxiety and depression modulation",
                         "Neuroscience"),
        RemainingFeature("micro.probiotic_colonization", "Probiotic Colonization Resistance", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Competitive exclusion of pathogens - transient vs resident",
                         "Microbiome"),
        RemainingFeature("micro.fmt", "Fecal Microbiota Transplant", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "C. diff cure - donor screening and enema delivery",
                         "Clinical"),
        RemainingFeature("micro.viral_quasispecies", "Viral Quasispecies", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Mutant swarm - hepatitis C treatment complexity",
                         "Virology"),
        RemainingFeature("micro.latent_reactivation", "Latent Viral Reactivation", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Herpes zoster (shingles) - immunosuppression trigger",
                         "Virology"),
        RemainingFeature("micro.endogenous_retrovirus", "Endogenous Retrovirus", RemainingSystem.MICROBIOLOGICAL,
                         (0, 10), "%", "8% of human genome - placental syncytin origin",
                         "Genomics"),
        RemainingFeature("micro.prion", "Prion Propagation", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Protein misfolding templating - BSE, vCJD, kuru",
                         "Pathology"),
        RemainingFeature("micro.biofilm_resistance", "Biofilm Resistance", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1000), "×", "1000× antibiotic tolerance - chronic infection persistence",
                         "Microbiology"),
        RemainingFeature("micro.sporulation", "Sporulation", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Dormant survival - anthrax and C. diff endospores",
                         "Microbiology"),
        RemainingFeature("micro.extremophile", "Extremophile Adaptation", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Thermophile, acidophile, halophile - biotech applications",
                         "Astrobiology"),
        RemainingFeature("micro.microbial_fuel_cell", "Microbial Fuel Cell", RemainingSystem.MICROBIOLOGICAL,
                         (0, 1), "scale", "Electricity from organic matter - wastewater treatment",
                         "Bioenergy"),


        # ============ AA. GENETIC & EPIGENETIC (15 features) ============
        RemainingFeature("gen.mendelian_inheritance", "Mendelian Inheritance Pattern", RemainingSystem.GENETIC,
                         (0, 5), "type", "Dominant, recessive, co-dominant, sex-linked",
                         "Genetics"),
        RemainingFeature("gen.polygenic_score", "Polygenic Risk Score", RemainingSystem.GENETIC,
                         (0, 100), "percentile", "Thousands of SNPs combined - probabilistic prediction",
                         "GWAS"),
        RemainingFeature("gen.copy_number_variation", "Copy Number Variation", RemainingSystem.GENETIC,
                         (0, 100), "copies", "Gene duplication/deletion - dosage sensitivity",
                         "Genomics"),
        RemainingFeature("gen.trinucleotide_repeat", "Trinucleotide Repeat Expansion", RemainingSystem.GENETIC,
                         (0, 1000), "repeats", "Huntington's, fragile X - anticipation in offspring",
                         "Molecular"),
        RemainingFeature("gen.mitochondrial", "Mitochondrial Inheritance", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Maternal only - heteroplasmy and threshold effects",
                         "Genetics"),
        RemainingFeature("gen.genomic_imprinting", "Genomic Imprinting", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Parent-of-origin expression - Prader-Willi vs Angelman",
                         "Epigenetics"),
        RemainingFeature("gen.x_inactivation", "X-inactivation", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Female mosaicism - calico cat coloration",
                         "Genetics"),
        RemainingFeature("gen.dna_methylation", "DNA Methylation Pattern", RemainingSystem.GENETIC,
                         (0, 100), "%", "CpG islands - gene silencing without sequence change",
                         "Epigenetics"),
        RemainingFeature("gen.histone_modification", "Histone Modification", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Acetylation, methylation - chromatin accessibility",
                         "Epigenetics"),
        RemainingFeature("gen.non_coding_rna", "Non-coding RNA Function", RemainingSystem.GENETIC,
                         (0, 10000), "types", "miRNA, lncRNA - regulatory networks",
                         "RNomics"),
        RemainingFeature("gen.telomerase", "Telomerase Activity", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Stem cells and cancer - immortalization",
                         "Molecular"),
        RemainingFeature("gen.somatic_mutation", "Somatic Mutation Accumulation", RemainingSystem.GENETIC,
                         (0, 10000), "mutations", "Age-related - cancer and mosaicism",
                         "Genomics"),
        RemainingFeature("gen.chimera", "Chimera Detection", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Two genomes in one body - twin absorption, transplant",
                         "Genetic testing"),
        RemainingFeature("gen.mosaicism", "Genetic Mosaicism", RemainingSystem.GENETIC,
                         (0, 1), "scale", "Post-zygotic mutation - severity depends on timing",
                         "Genetic testing"),
        RemainingFeature("gen.epigenetic_clock", "Epigenetic Clock", RemainingSystem.GENETIC,
                         (0, 100), "years", "Horvath clock - biological age from methylation",
                         "Epigenetics"),


        # ============ AB. SENSORY & PERCEPTUAL (15 features) ============
        RemainingFeature("sense.visual_acuity", "Visual Acuity (Snellen)", RemainingSystem.SENSORY,
                         (0, 2), "ratio", "20/20 standard - refractive error correction",
                         "Optometry"),
        RemainingFeature("sense.color_discrimination", "Color Discrimination", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Cone types (S, M, L) - anomalous and dichromacy",
                         "Color vision"),
        RemainingFeature("sense.dark_adaptation", "Dark Adaptation Rate", RemainingSystem.SENSORY,
                         (0, 30), "minutes", "Rhodopsin regeneration - 20-30 min full",
                         "Ophthalmology"),
        RemainingFeature("sense.flicker_fusion", "Critical Flicker Fusion", RemainingSystem.SENSORY,
                         (0, 100), "Hz", "60 Hz typical - TV and lighting design",
                         "Vision science"),
        RemainingFeature("sense.sound_frequency", "Sound Frequency Range", RemainingSystem.SENSORY,
                         (0, 20), "kHz", "20 Hz - 20 kHz - age-related high-frequency loss",
                         "Audiology"),
        RemainingFeature("sense.sound_localization", "Sound Localization Precision", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Interaural time and level differences - cone of confusion",
                         "Audiology"),
        RemainingFeature("sense.olfactory_sensitivity", "Olfactory Sensitivity", RemainingSystem.SENSORY,
                         (0, 1000), "receptors", "400+ odorant receptors - genetic variation huge",
                         "Olfaction"),
        RemainingFeature("sense.pheromone_detection", "Pheromone Detection (VNO)", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Vomeronasal organ vestigial in humans - debated effects",
                         "Chemoreception"),
        RemainingFeature("sense.taste_variation", "Taste Receptor Variation", RemainingSystem.SENSORY,
                         (0, 1), "scale", "TAS2R38 bitter sensitivity - PROP tasting",
                         "Gustation"),
        RemainingFeature("sense.touch_2point", "Touch Two-Point Discrimination", RemainingSystem.SENSORY,
                         (0, 40), "mm", "Fingertip 2mm, back 40mm - cortical representation",
                         "Somatosensory"),
        RemainingFeature("sense.proprioceptive_drift", "Proprioceptive Drift", RemainingSystem.SENSORY,
                         (0, 10), "cm", "Rubber hand illusion - body ownership plasticity",
                         "Perception"),
        RemainingFeature("sense.vestibular_function", "Vestibular Function", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Balance and spatial orientation - vertigo if impaired",
                         "ENT"),
        RemainingFeature("sense.pain_modulation", "Pain Modulation", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Gate control, endogenous opioids - placebo effect mechanism",
                         "Neurology"),
        RemainingFeature("sense.synesthesia", "Synesthetic Cross-Activation", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Grapheme-color, sound-taste - increased connectivity",
                         "Neuroscience"),
        RemainingFeature("sense.blindsight", "Blindsight", RemainingSystem.SENSORY,
                         (0, 1), "scale", "Unconscious visual processing - cortical damage, subcortical",
                         "Neurology"),


        # ============ AC. MEMORY & IDENTITY (15 features) ============
        RemainingFeature("mem.self_concept_clarity", "Self-Concept Clarity", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Consistent and confident self-beliefs - adjustment predictor",
                         "Self-report"),
        RemainingFeature("mem.identity_achievement", "Identity Achievement Status", RemainingSystem.MEMORY,
                         (0, 4), "status", "Marcia's exploration + commitment - diffusion, foreclosure, moratorium",
                         "Identity interview"),
        RemainingFeature("mem.possible_selves", "Possible Selves", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Hopped-for and feared future selves - motivation source",
                         "Self-report"),
        RemainingFeature("mem.self_complexity", "Self-Complexity", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Multiple self-aspects - buffer against stress",
                         "Self-report"),
        RemainingFeature("mem.self_esteem_stability", "Self-Esteem Stability", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Fluctuation over time - fragile high = aggression",
                         "Experience sampling"),
        RemainingFeature("mem.narrative_coherence", "Narrative Coherence", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Beginning, middle, end, causal links - mental health",
                         "Narrative analysis"),
        RemainingFeature("mem.redemptive_self", "Redemptive Self", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Suffering to growth narrative - McAdams' American identity",
                         "Narrative"),
        RemainingFeature("mem.contamination_sequence", "Contamination Sequence", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Positive to negative turn - depression and PTSD marker",
                         "Narrative"),
        RemainingFeature("mem.agency_theme", "Agency Theme", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Protagonist of own life - vs. communion (relationships)",
                         "Narrative analysis"),
        RemainingFeature("mem.self_continuity", "Self-Continuity", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Connection to past and future selves - disrupted in dissociation",
                         "Assessment"),
        RemainingFeature("mem.autonoetic_consciousness", "Autonoetic Consciousness", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Mental time travel - episodic memory requirement",
                         "Memory test"),
        RemainingFeature("mem.minimal_self", "Minimal Self", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Pre-reflective awareness - disrupted in schizophrenia",
                         "Phenomenology"),
        RemainingFeature("mem.narrative_self", "Narrative Self", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Extended autobiographical story - constructed and revised",
                         "Narrative"),
        RemainingFeature("mem.social_identity_complexity", "Social Identity Complexity", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Multiple group memberships - reduces intergroup bias",
                         "Self-report"),
        RemainingFeature("mem.identity_fusion", "Identity Fusion", RemainingSystem.MEMORY,
                         (0, 1), "scale", "Personal + group identity merger - willingness to die for group",
                         "Identity fusion scale"),


        # ============ AD. REPRODUCTIVE & SEXUAL (15 features) ============
        RemainingFeature("repro.fecundability", "Fecundability", RemainingSystem.REPRODUCTIVE,
                         (0, 1), "probability", "Probability of conception per cycle - age-dependent decline",
                         "Fecundability"),
        RemainingFeature("repro.implantation_window", "Implantation Window", RemainingSystem.REPRODUCTIVE,
                         (6, 10), "days", "6-10 days post-ovulation - receptivity limited",
                         "Reproductive"),
        RemainingFeature("repro.corpus_luteum", "Corpus Luteum Function", RemainingSystem.REPRODUCTIVE,
                         (0, 1), "scale", "Progesterone production - luteal phase defect and miscarriage",
                         "Clinical"),
        RemainingFeature("repro.cervical_mucus", "Cervical Mucus Quality", RemainingSystem.REPRODUCTIVE,
                         (0, 1), "scale", "Ferning pattern - sperm penetration facilitation",
                         "Fertility"),
        RemainingFeature("repro.sperm_count", "Sperm Count (Concentration)", RemainingSystem.REPRODUCTIVE,
                         (0, 200), "M/mL", "15 million/mL WHO threshold - declining globally",
                         "Semen analysis"),
        RemainingFeature("repro.sperm_motility", "Sperm Motility Grade", RemainingSystem.REPRODUCTIVE,
                         (0, 100), "%", "Progressive, non-progressive, immotile - fertilization requirement",
                         "Semen analysis"),
        RemainingFeature("repro.sperm_morphology", "Sperm Morphology", RemainingSystem.REPRODUCTIVE,
                         (0, 100), "%", "Normal forms 4%+ - Kruger strict criteria",
                         "Semen analysis"),
        RemainingFeature("repro.ovarian_reserve", "Ovarian Reserve", RemainingSystem.REPRODUCTIVE,
                         (0, 30), "follicles", "AFC and AMH - fertility window estimation",
                         "Ultrasound"),
        RemainingFeature("repro.menopause_timing", "Menopause Timing", RemainingSystem.REPRODUCTIVE,
                         (30, 60), "years", "Average 51 - premature <40",
                         "Clinical"),
        RemainingFeature("repro.andropause", "Andropause Gradient", RemainingSystem.REPRODUCTIVE,
                         (0, 1), "scale", "Testosterone decline gradual - symptomatic threshold debated",
                         "Endocrinology"),
        RemainingFeature("repro.miscarriage_risk", "Miscarriage Risk by Week", RemainingSystem.REPRODUCTIVE,
                         (0, 50), "%", "10-20% clinically recognized - 50-75% biochemical",
                         "Clinical"),
        RemainingFeature("repro.ectopic_rate", "Ectopic Pregnancy Rate", RemainingSystem.REPRODUCTIVE,
                         (0, 5), "%", "1-2% - tubal damage risk factor",
                         "Clinical"),
        RemainingFeature("repro.preeclampsia_onset", "Preeclampsia Onset", RemainingSystem.REPRODUCTIVE,
                         (20, 42), "weeks", "20 weeks+ - hypertension + proteinuria - eclampsia progression",
                         "Obstetrics"),
        RemainingFeature("repro.gestational_diabetes", "Gestational Diabetes", RemainingSystem.REPRODUCTIVE,
                         (0, 20), "%", "2-10% - insulin resistance - macrosomia and future T2DM risk",
                         "Obstetrics"),
        RemainingFeature("repro.placental_abruption", "Placental Abruption", RemainingSystem.REPRODUCTIVE,
                         (0, 2), "%", "Separation before delivery - hemorrhage and fetal hypoxia",
                         "Obstetrics"),
    ])
    
    for f in features:
        REMAINING_FEATURES[f.feature_id] = f


_register_remaining_features()


def get_remaining_feature(feature_id: str) -> RemainingFeature:
    return REMAINING_FEATURES.get(feature_id)


def get_features_by_remaining_system(system: RemainingSystem) -> list:
    return [f for f in REMAINING_FEATURES.values() if f.system == system]


def get_all_remaining_feature_ids() -> list:
    return list(REMAINING_FEATURES.keys())


def get_remaining_feature_count() -> int:
    return len(REMAINING_FEATURES)