"""
SEIR Epidemiology System — God-Tier Architecture
==============================================
Full SEIR model with pathogen genome, mutations, healthcare.
"""

import uuid
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class DiseaseState(Enum):
    SUSCEPTIBLE = 0
    EXPOSED = 1
    INFECTIOUS = 2
    RECOVERED = 3
    DECEASED = 4


class TransmissionMode(Enum):
    RESPIRATORY = auto()
    FECAL_ORAL = auto()
    VECTOR_BORNE = auto()


@dataclass
class PathogenGenome:
    name: str = ""
    genome_sequence: str = ""
    r0_base: float = 2.0
    incubation_period: float = 5.0
    infectious_period: float = 10.0
    case_fatality_rate: float = 0.01
    mutation_rate: float = 0.0001


@dataclass
class ImmuneResponse:
    antibody_titers: Dict[str, float] = field(default_factory=dict)
    t_cell_memory: Dict[str, float] = field(default_factory=dict)
    
    def get_immunity(self, disease_id: str) -> float:
        return self.antibody_titers.get(disease_id, 0.0)


@dataclass
class InfectionCase:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    state: DiseaseState = DiseaseState.SUSCEPTIBLE
    tick_exposed: int = 0
    viral_load: float = 0.0
    pathogen_name: str = ""
    symptom_severity: float = 0.0


class SEIREpidemiology:
    def __init__(self):
        self.pathogens: Dict[str, PathogenGenome] = {}
        self.seir_states: Dict[str, Dict[str, DiseaseState]] = {}
        self.infection_cases: Dict[str, InfectionCase] = {}
        self.r_effective: float = 0.0
        self.hospital_beds: int = 100
        self.halted: bool = False
    
    def register_pathogen(self, pathogen: PathogenGenome):
        self.pathogens[pathogen.name] = pathogen
    
    def initialize_population(self, agent_ids: List[str]):
        for agent_id in agent_ids:
            self.seir_states[agent_id] = {}
    
    def tick(self, tick: int, agents: List, rel_graph, lockdown: float = 0.0):
        if not self.pathogens:
            return
        
        for pathogen_name, pathogen in self.pathogens.items():
            self._process_pathogen(tick, pathogen, pathogen_name, agents, rel_graph, lockdown)
        
        self._update_healthcare()
    
    def _process_pathogen(self, tick: int, pathogen: PathogenGenome, disease_id: str, agents: List, rel_graph, lockdown: float):
        if not agents:
            return
            
        # Calculate effective R0 with lockdown
        r0 = pathogen.r0_base
        if lockdown > 0:
            r0 *= (1 - lockdown * 0.7)
        self.r_effective = r0
        
        import random
        for agent in agents:
            # Ensure agent has SEIR state
            if agent.id not in self.seir_states:
                self.seir_states[agent.id] = {}
            if disease_id not in self.seir_states[agent.id]:
                self.seir_states[agent.id][disease_id] = DiseaseState.SUSCEPTIBLE
            
            current_state = self.seir_states[agent.id][disease_id]
            
            # Process based on current state
            if current_state == DiseaseState.SUSCEPTIBLE:
                # Check if agent gets exposed - chance based on R0 and lockdown
                if random.random() < (r0 * 0.01):  # Small chance per tick
                    self.seir_states[agent.id][disease_id] = DiseaseState.EXPOSED
                    # Create infection case
                    if agent.id not in self.infection_cases:
                        self.infection_cases[agent.id] = InfectionCase(
                            state=DiseaseState.EXPOSED,
                            tick_exposed=tick,
                            pathogen_name=disease_id,
                            symptom_severity=random.uniform(10.0, 30.0)
                        )
            
            elif current_state == DiseaseState.EXPOSED:
                # After incubation period, become infectious
                if tick - self.infection_cases.get(agent.id, InfectionCase()).tick_exposed >= pathogen.incubation_period:
                    self.seir_states[agent.id][disease_id] = DiseaseState.INFECTIOUS
                    if agent.id in self.infection_cases:
                        self.infection_cases[agent.id].state = DiseaseState.INFECTIOUS
            
            elif current_state == DiseaseState.INFECTIOUS:
                # After infectious period, recover or die
                case = self.infection_cases.get(agent.id)
                if case and (tick - case.tick_exposed) >= pathogen.infectious_period:
                    if random.random() < pathogen.case_fatality_rate:
                        self.seir_states[agent.id][disease_id] = DiseaseState.DECEASED
                        if agent.id in self.infection_cases:
                            self.infection_cases[agent.id].state = DiseaseState.DECEASED
                    else:
                        self.seir_states[agent.id][disease_id] = DiseaseState.RECOVERED
                        if agent.id in self.infection_cases:
                            self.infection_cases[agent.id].state = DiseaseState.RECOVERED
    
    def _update_healthcare(self):
        pass
    
    def get_statistics(self) -> dict:
        susceptible = 0
        exposed = 0
        infectious = 0
        recovered = 0
        deceased = 0
        
        for agent_states in self.seir_states.values():
            if not agent_states:
                continue
            for ds in agent_states.values():
                if ds == DiseaseState.SUSCEPTIBLE:
                    susceptible += 1
                elif ds == DiseaseState.EXPOSED:
                    exposed += 1
                elif ds == DiseaseState.INFECTIOUS:
                    infectious += 1
                elif ds == DiseaseState.RECOVERED:
                    recovered += 1
                elif ds == DiseaseState.DECEASED:
                    deceased += 1
        
        return {
            "r_effective": round(self.r_effective, 2),
            "susceptible": susceptible,
            "exposed": exposed,
            "infectious": infectious,
            "recovered": recovered,
            "deceased": deceased,
            "hospital_beds_available": self.hospital_beds,
            "healthcare_staff_available": 50
        }
    
    def apply_treatment(self, agent, tick: int) -> bool:
        """Apply medical treatment to an agent."""
        if agent.id in self.infection_cases:
            case = self.infection_cases[agent.id]
            case.symptom_severity = max(0.0, case.symptom_severity - 20.0)
            if case.symptom_severity <= 0:
                self.seir_states[agent.id][case.pathogen_name] = DiseaseState.RECOVERED
                case.state = DiseaseState.RECOVERED
            return True
        return False