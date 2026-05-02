"""
Continuous Topology — God-Tier Architecture
===========================================
Implements:
- Continuous space with distance friction
- Location-based transmission costs
- Regional biomes and resources
- Movement costs based on terrain

Based on spec Section 7.2: Spatial Reality
"""

import uuid
import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from utils.logger import get_logger

logger = get_logger(__name__)


class TerrainType(Enum):
    """Terrain types with different properties."""
    PLAINS = auto()
    FOREST = auto()
    MOUNTAIN = auto()
    DESERT = auto()
    SWAMP = auto()
    WATER = auto()
    URBAN = auto()
    ROAD = auto()


@dataclass
class Location:
    """Continuous spatial location."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0  # Altitude
    
    def __hash__(self):
        return hash((round(self.x, 2), round(self.y, 2), round(self.z, 2)))
    
    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return (abs(self.x - other.x) < 0.01 and 
                abs(self.y - other.y) < 0.01 and 
                abs(self.z - other.z) < 0.01)
    
    def distance_to(self, other: 'Location') -> float:
        """Manhattan or Euclidean distance."""
        dx = other.x - self.x
        dy = other.y - self.y
        dz = other.z - self.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def manhattan_distance_to(self, other: 'Location') -> float:
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)


@dataclass
class TerrainCell:
    """A cell in the continuous world."""
    location: Location
    terrain_type: TerrainType
    
    # Movement costs (ticks per unit distance)
    move_cost: float = 1.0
    
    # Resources
    resources: Dict[str, float] = field(default_factory=dict)  # resource -> amount
    fertility: float = 0.5           # 0-1 agricultural potential
    mineral_grade: float = 0.0       # ore grade
    
    # Structures
    has_road: bool = False
    has_building: bool = False
    building_type: str = ""
    
    # Biome
    biome: str = ""
    temperature: float = 20.0       # Celsius
    rainfall: float = 1000.0        # mm/year
    
    def __post_init__(self):
        self._set_terrain_properties()
    
    def _set_terrain_properties(self):
        costs = {
            TerrainType.PLAINS: 1.0,
            TerrainType.FOREST: 1.5,
            TerrainType.MOUNTAIN: 2.5,
            TerrainType.DESERT: 1.3,
            TerrainType.SWAMP: 2.0,
            TerrainType.WATER: 10.0,  # Almost impassable
            TerrainType.URBAN: 0.8,
            TerrainType.ROAD: 0.5,
        }
        self.move_cost = costs.get(self.terrain_type, 1.0)


@dataclass
class WorldMap:
    """
    Continuous topology world.
    Not abstract nodes - actual distance matters.
    """
    width: float = 10000.0
    height: float = 10000.0
    
    # Terrain grid (sparse - only populated areas)
    cells: Dict[Tuple[float, float], TerrainCell] = field(default_factory=dict)
    
    # Spatial index for fast queries
    agent_locations: Dict[str, Location] = field(default_factory=dict)
    locations_by_agent: Dict[Location, str] = field(default_factory=dict)
    
    # Map generation
    seed: int = 42
    cell_resolution: float = 100.0  # meters per cell
    
    # Roads (paths between locations)
    roads: List[dict] = field(default_factory=list)
    
    # Resources spawn points
    resource_nodes: Dict[str, List[Location]] = field(default_factory=dict)
    
    def __post_init__(self):
        self._generate_terrain()
        self._place_resources()
    
    def _generate_terrain(self):
        """Generate terrain with biome."""
        random.seed(self.seed)
        
        # Simple Perlin-like generation
        for x in range(0, int(self.width), int(self.cell_resolution)):
            for y in range(0, int(self.height), int(self.cell_resolution)):
                # Simple noise
                noise = random.uniform(0, 1)
                
                # Determine terrain
                if noise < 0.3:
                    terrain = TerrainType.PLAINS
                elif noise < 0.5:
                    terrain = TerrainType.FOREST  
                elif noise < 0.65:
                    terrain = TerrainType.MOUNTAIN
                elif noise < 0.75:
                    terrain = TerrainType.DESERT
                elif noise < 0.85:
                    terrain = TerrainType.SWAMP
                else:
                    terrain = TerrainType.PLAINS  # Water omitted for simplicity
                
                cell = TerrainCell(
                    location=Location(x, y, random.uniform(0, 1000)),
                    terrain_type=terrain
                )
                
                # Set biome
                if terrain == TerrainType.FOREST:
                    cell.biome = "temperate_forest"
                    cell.resources["wood"] = random.uniform(50, 100)
                    cell.fertility = 0.6
                elif terrain == TerrainType.PLAINS:
                    cell.biome = "temperate_grassland"
                    cell.resources["food"] = random.uniform(30, 70)
                    cell.fertility = 0.8
                elif terrain == TerrainType.MOUNTAIN:
                    cell.biome = "alpine"
                    cell.mineral_grade = random.uniform(0, 0.3)
                    cell.resources["stone"] = random.uniform(50, 100)
                else:
                    cell.biome = "other"
                
                self.cells[(x, y)] = cell
    
    def _place_resources(self):
        """Place resource nodes."""
        random.seed(self.seed + 100)
        
        # Find ore-bearing cells
        for cell in self.cells.values():
            if cell.mineral_grade > 0.1:
                if "ore" not in self.resource_nodes:
                    self.resource_nodes["ore"] = []
                self.resource_nodes["ore"].append(cell.location)
    
    def get_terrain(self, location: Location) -> TerrainCell:
        """Get terrain at location."""
        # Snap to grid
        gx = round(location.x / self.cell_resolution) * self.cell_resolution
        gy = round(location.y / self.cell_resolution) * self.cell_resolution
        
        if (gx, gy) in self.cells:
            return self.cells[(gx, gy)]
        
        # Default
        return TerrainCell(
            location=location,
            terrain_type=TerrainType.PLAINS
        )
    
    def move_agent(
        self, 
        agent_id: str, 
        from_loc: Location, 
        to_loc: Location,
        max_distance: float = 100.0
    ) -> Tuple[bool, float, str]:
        """
        Move agent to new location.
        Returns: (success, actual_distance_traveled, reason)
        """
        # Calculate distance
        distance = from_loc.distance_to(to_loc)
        
        # Check max movement range
        if distance > max_distance:
            to_loc = self._interpolate(from_loc, to_loc, max_distance / distance)
            distance = max_distance
        
        # Get terrain costs
        from_terrain = self.get_terrain(from_loc)
        to_terrain = self.get_terrain(to_loc)
        
        # Base cost from distance
        move_cost = distance
        
        # Terrain penalty
        avg_cost = (from_terrain.move_cost + to_terrain.move_cost) / 2
        move_cost *= avg_cost
        
        # Road bonus
        if from_terrain.has_road and to_terrain.has_road:
            move_cost *= 0.5
        
        # Check if path exists (simple)
        if avg_cost > 2.0:
            return False, 0.0, "Terrain too difficult"
        
        # Remove old location if exists
        if agent_id in self.agent_locations:
            old_loc = self.agent_locations[agent_id]
            if old_loc in self.locations_by_agent:
                del self.locations_by_agent[old_loc]
        
        # Update position
        self.agent_locations[agent_id] = to_loc
        self.locations_by_agent[to_loc] = agent_id
        
        return True, distance, "moved"
    
    def _interpolate(
        self, 
        from_loc: Location, 
        to_loc: Location, 
        ratio: float
    ) -> Location:
        """Get point along path."""
        return Location(
            from_loc.x + (to_loc.x - from_loc.x) * ratio,
            from_loc.y + (to_loc.y - from_loc.y) * ratio,
            from_loc.z + (to_loc.z - from_loc.z) * ratio
        )
    
    def get_nearby_agents(
        self,
        agent_id: str,
        radius: float
    ) -> List[str]:
        """Get agents within radius."""
        if agent_id not in self.agent_locations:
            return []
        
        center = self.agent_locations[agent_id]
        nearby = []
        
        for other_id, loc in self.agent_locations.items():
            if other_id == agent_id:
                continue
            if center.distance_to(loc) <= radius:
                nearby.append(other_id)
        
        return nearby
    
    def get_travel_time(
        self,
        from_loc: Location,
        to_loc: Location
    ) -> float:
        """Calculate travel time in ticks."""
        distance = from_loc.distance_to(to_loc)
        terrain = self.get_terrain(to_loc)
        
        # Base: 1 tick per 100 units, modified by terrain
        base_ticks = distance / 100
        return base_ticks * terrain.move_cost
    
    def get_resources_nearby(
        self,
        location: Location,
        resource_type: str,
        radius: float = 1000.0
    ) -> List[Location]:
        """Find resource nodes within radius."""
        if resource_type not in self.resource_nodes:
            return []
        
        nearby = []
        for node_loc in self.resource_nodes[resource_type]:
            if location.distance_to(node_loc) <= radius:
                nearby.append(node_loc)
        
        return nearby
    
    def get_statistics(self) -> dict:
        """World map statistics."""
        terrain_counts = {}
        for cell in self.cells.values():
            terrain = cell.terrain_type.name
            terrain_counts[terrain] = terrain_counts.get(terrain, 0) + 1
        
        return {
            "total_cells": len(self.cells),
            "terrain_distribution": terrain_counts,
            "agents_positioned": len(self.agent_locations),
            "resource_nodes": {
                k: len(v) for k, v in self.resource_nodes.items()
            }
        }