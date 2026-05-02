"""
Multi-Scale Time Scheduler — God-Tier Architecture
============================================
Implements the 9 temporal domains from the spec:
- Physics:     Continuous / 1000 Hz (collision, fluid flow)
- Physiology: 1 Hz (heartbeat, metabolism, hormone pulses)
- Cognition:  10 Hz (perception, decision)
- Social:      Daily (relationships, gossip)
- Economic:   Weekly (market clearing, wages)
- Agricultural: Seasonal (planting, harvest)
- Demographic: Annual (births, deaths, migration)
- Geological: Century (erosion, tectonic)
- Evolutionary: Millennial (allele frequency)
"""

import uuid
import heapq
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class TimeDomain(Enum):
    """The 9 temporal scales of reality."""
    PHYSICS = auto()       # Milliseconds - collision, fluid
    PHYSIOLOGY = auto()   # Seconds - heartbeat, metabolism
    COGNITION = auto()   # Milliseconds - perception, decision
    SOCIAL = auto()       # Hours - relationship updates
    ECONOMIC = auto()    # Days - market clearing
    AGRICULTURAL = auto() # Weeks - planting, growth
    DEMOGRAPHIC = auto() # Years - births, deaths
    GEOLOGICAL = auto()   # Centuries - erosion
    EVOLUTIONARY = auto() # Millennia - speciation


@dataclass
class TimeEvent:
    """An event scheduled for a future tick in a specific domain."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    domain: TimeDomain = TimeDomain.COGNITION
    target_tick: int = 0
    callback: Callable = field(default=None)
    data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0  # Lower = higher priority
    
    def __lt__(self, other):
        if self.target_tick != other.target_tick:
            return self.target_tick < other.target_tick
        return self.priority < other.priority


@dataclass
class DomainState:
    """Tracks the state of each time domain."""
    domain: TimeDomain
    last_tick: int = 0
    is_active: bool = True
    events_pending: int = 0


class MultiScaleScheduler:
    """
    Master time scheduler that manages 9 asynchronous domains.
    
    Key features:
    - Domain-specific tick rates
    - Cross-domain dependencies (war affects economics for years)
    - Event queuing with priority
    - Causal ordering guarantees
    """
    
    # Domain tick intervals (in main simulation ticks)
    DOMAIN_INTERVALS = {
        TimeDomain.PHYSICS: 1,         # Every tick
        TimeDomain.PHYSIOLOGY: 1,       # Every tick  
        TimeDomain.COGNITION: 1,         # Every tick
        TimeDomain.SOCIAL: 10,          # Daily (10 ticks/day)
        TimeDomain.ECONOMIC: 70,        # Weekly (weekly)
        TimeDomain.AGRICULTURAL: 365,     # Seasonal (~1 year)
        TimeDomain.DEMOGRAPHIC: 3650,     # Annual (10 years = 1 sim-year with TICKS_PER_SIM_YEAR=5)
        TimeDomain.GEOLOGICAL: 365000,    # Century
        TimeDomain.EVOLUTIONARY: 3650000,  # Millennium
    }
    
    # What runs in each domain
    DOMAIN_HANDLERS = {
        TimeDomain.PHYSICS: "physics_tick",
        TimeDomain.PHYSIOLOGY: "physiology_tick", 
        TimeDomain.COGNITION: "cognition_tick",
        TimeDomain.SOCIAL: "social_tick",
        TimeDomain.ECONOMIC: "economic_tick",
        TimeDomain.AGRICULTURAL: "agricultural_tick",
        TimeDomain.DEMOGRAPHIC: "demographic_tick",
        TimeDomain.GEOLOGICAL: "geological_tick",
        TimeDomain.EVOLUTIONARY: "evolutionary_tick",
    }
    
    def __init__(self):
        self.tick_number: int = 0
        self.domain_states: Dict[TimeDomain, DomainState] = {}
        self.event_queue: List[TimeEvent] = []  # Heap-based priority queue
        self.subscribers: Dict[TimeDomain, List[Callable]] = {d: [] for d in TimeDomain}
        
        # Initialize domain states
        for domain in TimeDomain:
            self.domain_states[domain] = DomainState(domain=domain)
        
        # Track cross-domain effects
        self.pending_effects: Dict[int, List[dict]] = {}  # tick -> effects to apply
        
        logger.info("MultiScaleScheduler initialized with 9 domains.")
    
    def register_handler(self, domain: TimeDomain, handler: Callable):
        """Register a callback for a specific domain."""
        if domain not in self.subscribers:
            self.subscribers[domain] = []
        self.subscribers[domain].append(handler)
    
    def schedule_event(self, domain: TimeDomain, ticks_ahead: int, 
                     callback: Callable, data: dict = None, priority: int = 0):
        """Schedule an event for future execution."""
        event = TimeEvent(
            domain=domain,
            target_tick=self.tick_number + ticks_ahead,
            callback=callback,
            data=data or {},
            priority=priority
        )
        heapq.heappush(self.event_queue, event)
        self.domain_states[domain].events_pending += 1
    
    def tick(self) -> Dict[TimeDomain, bool]:
        """
        Advance one main simulation tick.
        Returns which domains had updates this tick.
        """
        self.tick_number += 1
        updates = {}
        
        # Check each domain for updates
        for domain in TimeDomain:
            interval = self.DOMAIN_INTERVALS[domain]
            should_update = (self.tick_number % interval == 0)
            
            if should_update:
                self.domain_states[domain].last_tick = self.tick_number
                updates[domain] = True
                
                # Execute registered handlers for this domain
                for handler in self.subscribers.get(domain, []):
                    try:
                        handler(self.tick_number)
                    except Exception as e:
                        logger.error(f"Handler error in {domain}: {e}")
        
        # Process scheduled events
        while self.event_queue and self.event_queue[0].target_tick <= self.tick_number:
            event = heapq.heappop(self.event_queue)
            self.domain_states[event.domain].events_pending -= 1
            
            if event.callback:
                try:
                    event.callback(event.data)
                except Exception as e:
                    logger.error(f"Event callback error: {e}")
        
        # Apply cross-domain pending effects
        if self.tick_number in self.pending_effects:
            for effect in self.pending_effects[self.tick_number]:
                self._apply_cross_domain_effect(effect)
            del self.pending_effects[self.tick_number]
        
        return updates
    
    def queue_cross_domain_effect(self, source_domain: TimeDomain, 
                              target_domain: TimeDomain, ticks_later: int,
                              effect_type: str, magnitude: float, data: dict = None):
        """
        Queue an effect that ripples across domains.
        
        Example: War (cognition/tick) → Economy (years) → Demographics (decades)
        """
        effect = {
            "source": source_domain,
            "target": target_domain,
            "type": effect_type,
            "magnitude": magnitude,
            "data": data or {}
        }
        
        target_tick = self.tick_number + ticks_later
        if target_tick not in self.pending_effects:
            self.pending_effects[target_tick] = []
        self.pending_effects[target_tick].append(effect)
        
        logger.debug(f"Queued cross-domain effect: {source_domain.name} → {target_domain.name} "
                   f"in {ticks_later} ticks ({effect_type}, mag={magnitude})")
    
    def _apply_cross_domain_effect(self, effect: dict):
        """Apply a queued cross-domain effect."""
        # This would modify simulation state based on the effect
        logger.debug(f"Applying cross-domain effect: {effect}")
    
    def get_domain_status(self) -> Dict[str, dict]:
        """Get status of all domains."""
        return {
            domain.name: {
                "last_tick": state.last_tick,
                "is_active": state.is_active,
                "pending_events": state.events_pending
            }
            for domain, state in self.domain_states.items()
        }
    
    def get_next_event_tick(self) -> Optional[int]:
        """Get tick number of next scheduled event."""
        if self.event_queue:
            return self.event_queue[0].target_tick
        return None