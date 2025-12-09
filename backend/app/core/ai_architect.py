"""
Professional AI Architect - Intelligent Floor Plan Generation
Uses architectural best practices, building codes, and optimization algorithms
"""
import math
import numpy as np
from typing import Dict, List, Tuple, Optional
from app.models.room import Room, FloorPlan, RoomType, Orientation
from config import Config

class ArchitecturalKnowledge:
    """
    Expert architectural knowledge base
    Based on architectural best practices and building science
    """

    # Room adjacency preferences (1-10 scale, 10 = highly preferred)
    ADJACENCY_MATRIX = {
        RoomType.LIVING: {
            RoomType.DINING: 10,
            RoomType.KITCHEN: 8,
            RoomType.OFFICE: 6,
            RoomType.BEDROOM: 2,
            RoomType.GARAGE: 3,
        },
        RoomType.KITCHEN: {
            RoomType.DINING: 10,
            RoomType.LIVING: 8,
            RoomType.PANTRY: 9,
            RoomType.GARAGE: 6,
            RoomType.BEDROOM: 1,
        },
        RoomType.MASTER_BEDROOM: {
            RoomType.MASTER_BATHROOM: 10,
            RoomType.LIVING: 2,
            RoomType.KITCHEN: 1,
        },
        RoomType.BEDROOM: {
            RoomType.BATHROOM: 8,
            RoomType.HALLWAY: 7,
            RoomType.LIVING: 2,
            RoomType.KITCHEN: 1,
        },
        RoomType.GARAGE: {
            RoomType.MUDROOM: 10,
            RoomType.LAUNDRY: 8,
            RoomType.KITCHEN: 6,
            RoomType.BEDROOM: 1,
        }
    }

    # Preferred orientations for natural light and energy efficiency
    ORIENTATION_PREFERENCES = {
        RoomType.LIVING: [Orientation.SOUTH, Orientation.SOUTHWEST],
        RoomType.KITCHEN: [Orientation.EAST, Orientation.SOUTHEAST],
        RoomType.MASTER_BEDROOM: [Orientation.EAST, Orientation.NORTHEAST],
        RoomType.BEDROOM: [Orientation.EAST, Orientation.NORTHEAST],
        RoomType.DINING: [Orientation.SOUTH, Orientation.EAST],
        RoomType.OFFICE: [Orientation.NORTH, Orientation.NORTHEAST],
        RoomType.BATHROOM: [Orientation.NORTH, Orientation.WEST],
        RoomType.GARAGE: [Orientation.NORTH, Orientation.NORTHWEST],
    }

    # Ideal aspect ratios (width:height) for different rooms
    ASPECT_RATIOS = {
        RoomType.LIVING: 1.5,       # Rectangular
        RoomType.KITCHEN: 1.3,
        RoomType.DINING: 1.4,
        RoomType.BEDROOM: 1.2,
        RoomType.MASTER_BEDROOM: 1.3,
        RoomType.BATHROOM: 1.1,
        RoomType.OFFICE: 1.2,
        RoomType.GARAGE: 2.0,       # Long and narrow
    }

    # Room priority for placement (higher = place first)
    PLACEMENT_PRIORITY = {
        RoomType.LIVING: 10,
        RoomType.KITCHEN: 9,
        RoomType.MASTER_BEDROOM: 8,
        RoomType.DINING: 7,
        RoomType.GARAGE: 6,
        RoomType.BEDROOM: 5,
        RoomType.BATHROOM: 4,
        RoomType.OFFICE: 5,
        RoomType.LAUNDRY: 3,
    }

    # Color palette for visualization
    ROOM_COLORS = {
        RoomType.LIVING: '#a8d5ff',
        RoomType.DINING: '#ffd9a8',
        RoomType.KITCHEN: '#ffb6a8',
        RoomType.BEDROOM: '#c8ffc8',
        RoomType.MASTER_BEDROOM: '#b3ffb3',
        RoomType.BATHROOM: '#e6d5ff',
        RoomType.MASTER_BATHROOM: '#d4bdff',
        RoomType.OFFICE: '#fff4a8',
        RoomType.GARAGE: '#d4d4d4',
        RoomType.LAUNDRY: '#c4e5f4',
        RoomType.HALLWAY: '#f5f5f5',
        RoomType.STORAGE: '#e0e0e0',
        RoomType.PANTRY: '#ffe4cc',
        RoomType.MUDROOM: '#e8dcc4',
        RoomType.TEMPLE: '#fff0e6',
    }


class AIArchitect:
    """
    Professional AI Architect for intelligent floor plan generation
    """

    def __init__(self):
        self.knowledge = ArchitecturalKnowledge()
        self.config = Config()

    def generate_floor_plan(
        self,
        total_sqft: float,
        bedrooms: int,
        bathrooms: int,
        style: str = "modern",
        special_rooms: Optional[Dict] = None,
        lot_dimensions: Optional[Tuple[float, float]] = None
    ) -> FloorPlan:
        """
        Generate an intelligent, code-compliant floor plan

        Args:
            total_sqft: Total square footage
            bedrooms: Number of bedrooms
            bathrooms: Number of bathrooms
            style: Architectural style (modern, traditional, ranch, etc.)
            special_rooms: Dict of special rooms to include
            lot_dimensions: (width, depth) of building lot

        Returns:
            FloorPlan object with optimized room layout
        """
        # Initialize floor plan
        floor_plan = FloorPlan(
            total_sqft=total_sqft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            style=style
        )

        if lot_dimensions:
            floor_plan.lot_width, floor_plan.lot_depth = lot_dimensions

        # Calculate space allocation
        allocation = self._calculate_space_allocation(
            total_sqft, bedrooms, bathrooms, style
        )

        # Generate room list
        rooms_to_create = self._generate_room_list(
            allocation, bedrooms, bathrooms, special_rooms
        )

        # Calculate optimal building dimensions
        building_width, building_depth = self._calculate_building_envelope(
            total_sqft, lot_dimensions
        )

        # Place rooms using intelligent algorithm
        placed_rooms = self._intelligent_room_placement(
            rooms_to_create, building_width, building_depth
        )

        floor_plan.rooms = placed_rooms
        floor_plan.lot_width = building_width
        floor_plan.lot_depth = building_depth

        # Optimize layout
        floor_plan = self._optimize_layout(floor_plan)

        # Add doors and windows
        floor_plan = self._add_openings(floor_plan)

        return floor_plan

    def _calculate_space_allocation(
        self,
        total_sqft: float,
        bedrooms: int,
        bathrooms: int,
        style: str
    ) -> Dict[str, float]:
        """
        Calculate optimal space allocation based on architectural style
        and building science principles
        """
        # Base allocations by style
        style_allocations = {
            'modern': {
                'living': 0.25,
                'kitchen': 0.15,
                'dining': 0.10,
                'bedrooms': 0.30,
                'bathrooms': 0.10,
                'circulation': 0.08,
                'storage': 0.02
            },
            'traditional': {
                'living': 0.22,
                'kitchen': 0.12,
                'dining': 0.12,
                'bedrooms': 0.32,
                'bathrooms': 0.12,
                'circulation': 0.08,
                'storage': 0.02
            },
            'ranch': {
                'living': 0.28,
                'kitchen': 0.16,
                'dining': 0.08,
                'bedrooms': 0.28,
                'bathrooms': 0.10,
                'circulation': 0.08,
                'storage': 0.02
            },
            'luxury': {
                'living': 0.30,
                'kitchen': 0.18,
                'dining': 0.10,
                'bedrooms': 0.25,
                'bathrooms': 0.12,
                'circulation': 0.03,
                'storage': 0.02
            }
        }

        allocation = style_allocations.get(style.lower(), style_allocations['modern'])

        # Adjust for number of bedrooms and bathrooms
        if bedrooms > 3:
            allocation['bedrooms'] += 0.05
            allocation['living'] -= 0.03
            allocation['circulation'] -= 0.02

        if bathrooms > 2:
            allocation['bathrooms'] += 0.03
            allocation['storage'] -= 0.03

        # Convert to square footage
        sqft_allocation = {
            key: total_sqft * value for key, value in allocation.items()
        }

        return sqft_allocation

    def _generate_room_list(
        self,
        allocation: Dict[str, float],
        bedrooms: int,
        bathrooms: int,
        special_rooms: Optional[Dict]
    ) -> List[Dict]:
        """Generate list of rooms to create"""
        rooms = []

        # Living areas
        rooms.append({
            'name': 'Living Room',
            'type': RoomType.LIVING,
            'area': allocation['living'],
            'priority': 10
        })

        rooms.append({
            'name': 'Kitchen',
            'type': RoomType.KITCHEN,
            'area': allocation['kitchen'],
            'priority': 9
        })

        if allocation.get('dining', 0) > 80:
            rooms.append({
                'name': 'Dining Room',
                'type': RoomType.DINING,
                'area': allocation['dining'],
                'priority': 7
            })

        # Bedrooms
        bedroom_area = allocation['bedrooms'] / bedrooms
        for i in range(bedrooms):
            if i == 0:  # Master bedroom
                master_area = bedroom_area * 1.4  # 40% larger
                rooms.append({
                    'name': 'Master Bedroom',
                    'type': RoomType.MASTER_BEDROOM,
                    'area': master_area,
                    'priority': 8
                })
            else:
                rooms.append({
                    'name': f'Bedroom {i + 1}',
                    'type': RoomType.BEDROOM,
                    'area': bedroom_area * 0.9,
                    'priority': 5
                })

        # Bathrooms
        bathroom_area = allocation['bathrooms'] / bathrooms
        for i in range(bathrooms):
            if i == 0:  # Master bathroom
                rooms.append({
                    'name': 'Master Bathroom',
                    'type': RoomType.MASTER_BATHROOM,
                    'area': bathroom_area * 1.3,
                    'priority': 7
                })
            else:
                rooms.append({
                    'name': f'Bathroom {i + 1}',
                    'type': RoomType.BATHROOM,
                    'area': bathroom_area,
                    'priority': 4
                })

        # Special rooms
        if special_rooms:
            if special_rooms.get('office'):
                rooms.append({
                    'name': 'Home Office',
                    'type': RoomType.OFFICE,
                    'area': 120,
                    'priority': 6
                })
            if special_rooms.get('laundry'):
                rooms.append({
                    'name': 'Laundry Room',
                    'type': RoomType.LAUNDRY,
                    'area': 60,
                    'priority': 3
                })
            if special_rooms.get('garage'):
                garage_size = special_rooms.get('garage_cars', 2)
                rooms.append({
                    'name': f'{garage_size}-Car Garage',
                    'type': RoomType.GARAGE,
                    'area': garage_size * 200,  # 200 sqft per car
                    'priority': 6
                })
            if special_rooms.get('temple'):
                rooms.append({
                    'name': 'Prayer Room',
                    'type': RoomType.TEMPLE,
                    'area': 80,
                    'priority': 5
                })

        return rooms

    def _calculate_building_envelope(
        self,
        total_sqft: float,
        lot_dimensions: Optional[Tuple[float, float]]
    ) -> Tuple[float, float]:
        """
        Calculate optimal building dimensions for minimum perimeter
        (reduces energy costs and construction costs)
        """
        if lot_dimensions:
            max_width, max_depth = lot_dimensions
            # Use 80% of lot to allow setbacks
            max_width *= 0.8
            max_depth *= 0.8
        else:
            max_width = max_depth = float('inf')

        # Ideal ratio for energy efficiency is close to square (1:1 to 1.5:1)
        ideal_ratio = 1.3

        # Calculate dimensions
        width = min(math.sqrt(total_sqft * ideal_ratio), max_width)
        depth = min(total_sqft / width, max_depth)

        # Adjust if needed
        while width * depth < total_sqft:
            if width < max_width:
                width += 5
            else:
                depth += 5

        return round(width, 2), round(depth, 2)

    def _intelligent_room_placement(
        self,
        rooms_to_create: List[Dict],
        building_width: float,
        building_depth: float
    ) -> List[Room]:
        """
        Intelligently place rooms using architectural principles
        """
        # Sort by priority
        rooms_to_create.sort(key=lambda x: x['priority'], reverse=True)

        placed_rooms = []
        grid_size = 10  # 10 ft grid for alignment

        # Track occupied space
        occupied = []

        for room_data in rooms_to_create:
            # Calculate room dimensions
            area = max(room_data['area'], self.config.MIN_ROOM_SIZE)
            room_type = room_data['type']

            # Get ideal aspect ratio
            aspect_ratio = self.knowledge.ASPECT_RATIOS.get(room_type, 1.2)

            # Calculate width and height
            height = math.sqrt(area / aspect_ratio)
            width = area / height

            # Snap to grid
            width = round(width / grid_size) * grid_size
            height = round(height / grid_size) * grid_size

            # Recalculate actual area
            actual_area = width * height

            # Find best position
            x, y, orientation = self._find_best_position(
                room_type, width, height, building_width, building_depth,
                occupied, placed_rooms
            )

            # Create room
            room = Room(
                name=room_data['name'],
                room_type=room_type,
                x=x,
                y=y,
                width=width,
                height=height,
                area=actual_area,
                color=self.knowledge.ROOM_COLORS.get(room_type, '#ffffff'),
                orientation=orientation,
                priority=room_data['priority']
            )

            placed_rooms.append(room)
            occupied.append((x, y, width, height))

        return placed_rooms

    def _find_best_position(
        self,
        room_type: RoomType,
        width: float,
        height: float,
        building_width: float,
        building_depth: float,
        occupied: List[Tuple],
        placed_rooms: List[Room]
    ) -> Tuple[float, float, Orientation]:
        """
        Find the best position for a room based on:
        - Orientation preferences
        - Adjacency to other rooms
        - Available space
        """
        best_x, best_y = 50, 50  # Default starting position
        best_score = -1
        best_orientation = Orientation.SOUTH

        # Preferred orientations
        preferred_orientations = self.knowledge.ORIENTATION_PREFERENCES.get(
            room_type, [Orientation.SOUTH]
        )

        # Try different positions
        grid_step = 50  # Try positions every 50 feet
        for orientation in preferred_orientations:
            # Determine search area based on orientation
            if orientation in [Orientation.SOUTH, Orientation.SOUTHEAST, Orientation.SOUTHWEST]:
                y_positions = [50]  # South side
                x_positions = range(50, int(building_width - width), grid_step)
            elif orientation in [Orientation.NORTH, Orientation.NORTHEAST, Orientation.NORTHWEST]:
                y_positions = [building_depth - height - 50]  # North side
                x_positions = range(50, int(building_width - width), grid_step)
            elif orientation == Orientation.EAST:
                x_positions = [50]  # East side
                y_positions = range(50, int(building_depth - height), grid_step)
            else:  # WEST
                x_positions = [building_width - width - 50]  # West side
                y_positions = range(50, int(building_depth - height), grid_step)

            for x in x_positions:
                for y in y_positions:
                    # Check if position is available
                    if self._is_position_available(x, y, width, height, occupied):
                        # Calculate score based on adjacency
                        score = self._calculate_position_score(
                            room_type, x, y, width, height, placed_rooms
                        )

                        if score > best_score:
                            best_score = score
                            best_x, best_y = x, y
                            best_orientation = orientation

        # If no ideal position found, use first available
        if best_score == -1:
            best_x, best_y = self._find_first_available(
                width, height, building_width, building_depth, occupied
            )

        return best_x, best_y, best_orientation

    def _is_position_available(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        occupied: List[Tuple]
    ) -> bool:
        """Check if a position doesn't overlap with occupied spaces"""
        margin = 5  # 5 ft margin between rooms

        for ox, oy, ow, oh in occupied:
            if not (x + width + margin < ox or
                   x - margin > ox + ow or
                   y + height + margin < oy or
                   y - margin > oy + oh):
                return False
        return True

    def _find_first_available(
        self,
        width: float,
        height: float,
        building_width: float,
        building_depth: float,
        occupied: List[Tuple]
    ) -> Tuple[float, float]:
        """Find first available position (fallback)"""
        grid_step = 25
        for y in range(50, int(building_depth - height), grid_step):
            for x in range(50, int(building_width - width), grid_step):
                if self._is_position_available(x, y, width, height, occupied):
                    return x, y
        return 50, 50  # Last resort

    def _calculate_position_score(
        self,
        room_type: RoomType,
        x: float,
        y: float,
        width: float,
        height: float,
        placed_rooms: List[Room]
    ) -> float:
        """
        Calculate score for a room position based on adjacency preferences
        """
        score = 0
        room_center = (x + width / 2, y + height / 2)

        adjacency_prefs = self.knowledge.ADJACENCY_MATRIX.get(room_type, {})

        for placed_room in placed_rooms:
            # Calculate distance between centers
            distance = math.sqrt(
                (room_center[0] - placed_room.center[0]) ** 2 +
                (room_center[1] - placed_room.center[1]) ** 2
            )

            # Get adjacency preference
            preference = adjacency_prefs.get(placed_room.room_type, 5)

            # Higher score for preferred adjacency, lower for non-preferred
            # Closer distance = higher influence
            if distance < 100:  # Within 100 ft
                score += preference * (100 - distance) / 100

        return score

    def _optimize_layout(self, floor_plan: FloorPlan) -> FloorPlan:
        """
        Optimize layout using iterative improvement
        """
        # For now, just update adjacent rooms
        for i, room in enumerate(floor_plan.rooms):
            for j, other_room in enumerate(floor_plan.rooms):
                if i != j:
                    # Check if rooms are adjacent (within 10 ft)
                    distance = math.sqrt(
                        (room.center[0] - other_room.center[0]) ** 2 +
                        (room.center[1] - other_room.center[1]) ** 2
                    )
                    if distance < 50:  # Adjacent threshold
                        if other_room.name not in room.adjacent_rooms:
                            room.adjacent_rooms.append(other_room.name)

        return floor_plan

    def _add_openings(self, floor_plan: FloorPlan) -> FloorPlan:
        """
        Add doors and windows based on room type and adjacency
        """
        for room in floor_plan.rooms:
            # Add doors based on room type
            if room.room_type in [RoomType.BEDROOM, RoomType.MASTER_BEDROOM]:
                # Bedroom needs at least one door
                room.doors.append({
                    'x': room.x + room.width / 2,
                    'y': room.y,
                    'width': 3,  # 3 ft door
                    'type': 'entry'
                })

                # Add egress window (building code requirement)
                room.windows.append({
                    'x': room.x + room.width * 0.7,
                    'y': room.y + room.height,
                    'width': 4,
                    'height': 4.5,
                    'type': 'egress'
                })

            if room.room_type == RoomType.LIVING:
                # Living room - multiple windows for light
                room.windows.append({
                    'x': room.x + room.width / 3,
                    'y': room.y + room.height,
                    'width': 6,
                    'height': 5,
                    'type': 'picture'
                })
                room.windows.append({
                    'x': room.x + room.width * 2/3,
                    'y': room.y + room.height,
                    'width': 4,
                    'height': 5,
                    'type': 'casement'
                })

        return floor_plan
