"""
Information Physics — God-Tier Architecture
===================================
Implements: Information is local, delayed, costly, asymmetric, corrupted
- No global truth accessible
- Observation affects reality (observer effect)
- Information has propagation delay
- Knowledge is imperfect

Based on spec Section 3.4: Observability Limits
"""

import uuid
import random
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class InformationSource(Enum):
    """Types of information sources."""
    DIRECT_OBSERVATION = auto()  # Seeing directly
    HEARSAY = auto()       # Heard from others
    RUMOR = auto()         # Unverified
    AUTHORITY = auto()      # Official source
    MEDIA = auto()          # News, social
    GOSSIP = auto()        # Social network
    INSTINCT = auto()       # Intuition


@dataclass
class InformationPacket:
    """A piece of information in the world."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    # Content (what it's about)
    subject: str = ""         # e.g., "Agent.123.health"
    predicate: str = ""      # e.g., "is_sick"
    value: Any = None         # The claimed value
    
    # Source info
    source_type: InformationSource = InformationSource.DIRECT_OBSERVATION
    source_agent: str = ""     # Who/where it came from
    reliability: float = 1.0   # 0-1 (accuracy probability)
    
    # Propagation
    tick_created: int = 0
    tick_disseminated: int = 0
    spread_distance: float = 0.0  # Degrees of separation
    
    # Truth
    is_actual_truth: bool = True  # Ground truth
    corruption_level: float = 0.0
    
    # Verification
    verification_count: int = 0
    is_verified: bool = False
    
    def corrupt(self, level: float):
        """Add noise/corruption to information."""
        self.corruption_level = level
        if self.is_actual_truth and random.random() < level:
            # Flip value with some probability
            if isinstance(self.value, (int, float)):
                self.value *= random.uniform(0.8, 1.2)
            elif isinstance(self.value, bool):
                self.value = random.random() < self.corruption_level
            # String values get garbled sometimes
            elif isinstance(self.value, str):
                if random.random() < self.corruption_level * 0.5:
                    self.value = "??? [CORRUPTED]"


@dataclass
class AgentKnowledge:
    """What an agent knows about the world."""
    known_facts: Dict[str, InformationPacket] = field(default_factory=dict)
    beliefs: Dict[str, float] = field(default_factory=dict)  # fact_id -> confidence
    
    # Observation state
    can_see_directly: bool = True
    perception_range: float = 100.0  # meters
    attention_capacity: int = 7  # Miller's 7±2
    
    # Information access
    known_by_proxy: Set[str] = field(default_factory=set)  # Other agents
    
    def learn(self, packet: InformationPacket, tick: int, observe_range: float):
        """Agent learns new information."""
        key = f"{packet.subject}.{packet.predicate}"
        
        # Calculate accuracy based on distance/corruption
        corruption = packet.corruption_level
        if packet.spread_distance > observe_range:
            corruption += 0.1 * (packet.spread_distance / observe_range)
        
        packet.corrupt(corruption)
        
        # Store with confidence
        self.known_facts[key] = packet
        accuracy = packet.reliability * (1 - corruption)
        self.beliefs[key] = min(1.0, max(0.0, accuracy))
    
    def get_belief(self, fact_key: str) -> float:
        """Get confidence in a fact."""
        return self.beliefs.get(fact_key, 0.0)
    
    def get_perceived_value(self, fact_key: str) -> Any:
        """Get what agent thinks is true (may be wrong)."""
        if fact_key not in self.known_facts:
            return None
        
        packet = self.known_facts[fact_key]
        if packet.corruption_level > 0.5:
            return None  # Too corrupted
        return packet.value


class InformationPhysics:
    """
    Manages information propagation with realistic constraints.
    """
    
    def __init__(self):
        self.all_information: Dict[str, InformationPacket] = {}
        self.knowledge_by_agent: Dict[str, AgentKnowledge] = {}
        
        # Propagation rules
        self.propagation_speed = 1.0  # Ticks per degree
        self.decay_rate = 0.02         # Accuracy loss per tick
        self.gossip_threshold = 5         # Ticks until shared
        self.verification_cost = 0.1
        
        logger.info("InformationPhysics initialized.")
    
    def register_agent(self, agent_id: str, perception_range: float = 100.0):
        """Agent joins the information network."""
        self.knowledge_by_agent[agent_id] = AgentKnowledge(
            perception_range=perception_range
        )
    
    def broadcast_event(
        self,
        tick: int,
        subject: str,
        predicate: str,
        actual_value: Any,
        source_domain: InformationSource,
        reliability: float = 1.0
    ) -> InformationPacket:
        """Create information about an event."""
        packet = InformationPacket(
            subject=subject,
            predicate=predicate,
            value=actual_value,
            source_type=source_domain,
            reliability=reliability,
            tick_created=tick,
            tick_disseminated=tick,
            is_actual_truth=True
        )
        
        self.all_information[packet.id] = packet
        return packet
    
    def propagate(
        self,
        tick: int,
        from_agent: str,
        to_agent: str,
        packet_id: str,
        relationship: str = "stranger"  # friend, rival, etc.
    ) -> bool:
        """Information propagates through relationship."""
        if packet_id not in self.all_information:
            return False
        
        packet = self.all_information[packet_id]
        
        # Relationship affects spread
        trust_weights = {
            "friend": 0.9,
            "family": 0.95,
            "colleague": 0.7,
            "stranger": 0.3,
            "rival": 0.1
        }
        trust = trust_weights.get(relationship, 0.5)
        
        # Delay based on relationship distance
        delay_ticks = int(1 / trust)
        if tick - packet.tick_disseminated < delay_ticks:
            return False
        
        # Create copy for receiver
        new_packet = InformationPacket(
            subject=packet.subject,
            predicate=packet.predicate,
            value=packet.value,
            source_type=InformationSource.HEARSAY,
            reliability=packet.reliability * trust,
            tick_created=packet.tick_created,
            tick_disseminated=tick,
            spread_distance=packet.spread_distance + 1,
            is_actual_truth=False
        )
        
        # Add to receiver's knowledge
        if to_agent in self.knowledge_by_agent:
            to_knowledge = self.knowledge_by_agent[to_agent]
            to_knowledge.learn(
                new_packet, 
                tick,
                to_knowledge.perception_range
            )
            to_knowledge.known_by_proxy.add(from_agent)
        
        return True
    
    def observe_directly(
        self,
        tick: int,
        agent_id: str,
        target_id: str,
        target_state: dict,
        range_distance: float
    ) -> int:
        """
        Agent observes another agent/entity directly.
        Returns: observations made (0 = failed)
        """
        if agent_id not in self.knowledge_by_agent:
            return 0
        
        knowledge = self.knowledge_by_agent[agent_id]
        
        # Check range
        if range_distance > knowledge.perception_range:
            return 0  # Too far
        
        observations = 0
        knowledge.can_see_directly = True
        
        # Observe what we can see (limited attention)
        for key, value in list(target_state.items())[:knowledge.attention_capacity]:
            # Create direct observation
            packet = InformationPacket(
                subject=target_id,
                predicate=key,
                value=value,
                source_type=InformationSource.DIRECT_OBSERVATION,
                source_agent=target_id,
                reliability=0.95 if range_distance < 10 else 0.7,
                tick_created=tick,
                tick_disseminated=tick,
                is_actual_truth=True
            )
            
            knowledge.learn(packet, tick, knowledge.perception_range)
            observations += 1
        
        return observations
    
    def query_belief(
        self,
        agent_id: str,
        fact_key: str
    ) -> tuple:
        """
        Agent asks about a fact.
        Returns: (believed_value, confidence)
        """
        if agent_id not in self.knowledge_by_agent:
            return None, 0.0
        
        knowledge = self.knowledge_by_agent[agent_id]
        
        if fact_key not in knowledge.known_facts:
            return None, 0.0
        
        packet = knowledge.known_facts[fact_key]
        
        # Some information becomes outdated
        age = knowledge.beliefs.get(fact_key, 1.0)
        if age > 0:
            confidence = age - self.decay_rate * age
            knowledge.beliefs[fact_key] = confidence
        
        return knowledge.get_perceived_value(fact_key), confidence
    
    def distribute_rumor(
        self,
        tick: int,
        agent_ids: List[str],
        subject: str,
        predicate: str,
        seed_value: Any,
        starting_agent: str
    ):
        """Start a rumor (false information propagates)."""
        # Create as "gossip" not verified
        packet = InformationPacket(
            subject=subject,
            predicate=predicate,
            value=seed_value,
            source_type=InformationSource.RUMOR,
            source_agent=starting_agent,
            reliability=0.3,  # Low reliability!
            tick_created=tick,
            tick_disseminated=tick,
            spread_distance=0,
            is_actual_truth=False
        )
        
        self.all_information[packet.id] = packet
        
        # First person learns it
        if starting_agent in self.knowledge_by_agent:
            self.knowledge_by_agent[starting_agent].learn(
                packet, tick,
                self.knowledge_by_agent[starting_agent].perception_range
            )
    
    def get_statistics(self) -> dict:
        """Information network statistics."""
        truth_count = sum(1 for p in self.all_information.values() if p.is_actual_truth)
        return {
            "total_packets": len(self.all_information),
            "actual_truth": truth_count,
            "corrupted": sum(1 for p in self.all_information.values() if p.corruption_level > 0),
            "agents_in_network": len(self.knowledge_by_agent)
        }