"""
Room and Floor Plan Data Models
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class RoomType(Enum):
    """Standard room types"""
    LIVING = "living"
    DINING = "dining"
    KITCHEN = "kitchen"
    BEDROOM = "bedroom"
    MASTER_BEDROOM = "master_bedroom"
    BATHROOM = "bathroom"
    MASTER_BATHROOM = "master_bathroom"
    OFFICE = "office"
    LAUNDRY = "laundry"
    GARAGE = "garage"
    HALLWAY = "hallway"
    STORAGE = "storage"
    PANTRY = "pantry"
    MUDROOM = "mudroom"
    TEMPLE = "temple"
    GYM = "gym"
    LIBRARY = "library"

class Orientation(Enum):
    """Cardinal directions for room orientation"""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    NORTHEAST = "northeast"
    NORTHWEST = "northwest"
    SOUTHEAST = "southeast"
    SOUTHWEST = "southwest"

@dataclass
class Room:
    """Represents a single room in the floor plan"""
    name: str
    room_type: RoomType
    x: float
    y: float
    width: float
    height: float
    area: float
    color: str = "#ffffff"
    orientation: Optional[Orientation] = None
    floor_level: int = 1
    doors: List[Dict] = field(default_factory=list)
    windows: List[Dict] = field(default_factory=list)
    adjacent_rooms: List[str] = field(default_factory=list)
    priority: int = 5  # 1-10, higher = more important

    @property
    def perimeter(self) -> float:
        """Calculate room perimeter"""
        return 2 * (self.width + self.height)

    @property
    def aspect_ratio(self) -> float:
        """Calculate width to height ratio"""
        return self.width / self.height if self.height > 0 else 1.0

    @property
    def center(self) -> Tuple[float, float]:
        """Get room center coordinates"""
        return (self.x + self.width / 2, self.y + self.height / 2)

    def to_dict(self) -> Dict:
        """Convert room to dictionary"""
        return {
            'name': self.name,
            'type': self.room_type.value if isinstance(self.room_type, RoomType) else self.room_type,
            'x': round(self.x, 2),
            'y': round(self.y, 2),
            'width': round(self.width, 2),
            'height': round(self.height, 2),
            'area': round(self.area, 2),
            'color': self.color,
            'orientation': self.orientation.value if self.orientation else None,
            'floor_level': self.floor_level,
            'doors': self.doors,
            'windows': self.windows,
            'adjacent_rooms': self.adjacent_rooms,
            'perimeter': round(self.perimeter, 2),
            'aspect_ratio': round(self.aspect_ratio, 2)
        }

@dataclass
class FloorPlan:
    """Represents a complete floor plan"""
    total_sqft: float
    rooms: List[Room] = field(default_factory=list)
    bedrooms: int = 0
    bathrooms: int = 0
    floors: int = 1
    style: str = "modern"
    lot_width: float = 0
    lot_depth: float = 0

    @property
    def total_living_area(self) -> float:
        """Calculate total living area (excluding garage, storage)"""
        excluded_types = {RoomType.GARAGE, RoomType.STORAGE}
        return sum(room.area for room in self.rooms
                  if room.room_type not in excluded_types)

    @property
    def efficiency_ratio(self) -> float:
        """Calculate space efficiency (living area / total area)"""
        total = sum(room.area for room in self.rooms)
        return (self.total_living_area / total * 100) if total > 0 else 0

    @property
    def room_count(self) -> int:
        """Get total number of rooms"""
        return len(self.rooms)

    def get_rooms_by_type(self, room_type: RoomType) -> List[Room]:
        """Get all rooms of a specific type"""
        return [room for room in self.rooms if room.room_type == room_type]

    def to_dict(self) -> Dict:
        """Convert floor plan to dictionary"""
        return {
            'total_sqft': round(self.total_sqft, 2),
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'floors': self.floors,
            'style': self.style,
            'lot_width': round(self.lot_width, 2) if self.lot_width else None,
            'lot_depth': round(self.lot_depth, 2) if self.lot_depth else None,
            'rooms': [room.to_dict() for room in self.rooms],
            'stats': {
                'total_living_area': round(self.total_living_area, 2),
                'efficiency_ratio': round(self.efficiency_ratio, 2),
                'room_count': self.room_count,
                'total_area': round(sum(room.area for room in self.rooms), 2)
            }
        }
