"""
Professional CAD Engine - Real DXF/DWG Import/Export
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import io
import math
from typing import Dict, List, Tuple, BinaryIO, Optional
from app.models.room import FloorPlan, Room, RoomType
from config import Config

class CADEngine:
    """Professional CAD file generation and parsing engine"""

    def __init__(self):
        self.config = Config()

    def export_to_dxf(self, floor_plan: FloorPlan, scale: str = "1:50") -> BinaryIO:
        """
        Export floor plan to professional DXF format

        Args:
            floor_plan: FloorPlan object to export
            scale: Drawing scale (1:50, 1:100, 1:200)

        Returns:
            BytesIO object containing DXF file
        """
        # Create new DXF document
        doc = ezdxf.new(self.config.DXF_VERSION)
        doc.units = units.FT if self.config.DEFAULT_UNITS == 'feet' else units.M

        msp = doc.modelspace()

        # Create layers with proper colors and linetypes
        self._create_layers(doc)

        # Add title block
        self._add_title_block(msp, floor_plan, scale)

        # Draw rooms
        for room in floor_plan.rooms:
            self._draw_room(msp, room)

        # Add dimensions
        self._add_dimensions(msp, floor_plan)

        # Add room schedule/legend
        self._add_room_schedule(msp, floor_plan)

        # Save to BytesIO
        buffer = io.BytesIO()
        doc.write(buffer)
        buffer.seek(0)

        return buffer

    def _create_layers(self, doc: ezdxf.document.Drawing):
        """Create standard architectural layers"""
        layers = [
            ('WALLS', 1, 'CONTINUOUS', 0.5),      # Red, thick lines
            ('DOORS', 3, 'CONTINUOUS', 0.25),      # Green
            ('WINDOWS', 5, 'CONTINUOUS', 0.25),    # Blue
            ('DIMENSIONS', 2, 'CONTINUOUS', 0.13), # Yellow
            ('TEXT', 7, 'CONTINUOUS', 0.13),       # White/Black
            ('FURNITURE', 8, 'CONTINUOUS', 0.18),  # Gray
            ('GRID', 9, 'DASHED', 0.09),          # Light gray
            ('TITLE', 6, 'CONTINUOUS', 0.35),      # Magenta
        ]

        for name, color, linetype, lineweight in layers:
            layer = doc.layers.add(name)
            layer.color = color
            layer.dxf.lineweight = int(lineweight * 100)  # Convert to DXF units

    def _add_title_block(self, msp, floor_plan: FloorPlan, scale: str):
        """Add professional title block"""
        # Title block position
        tb_x, tb_y = 50, -100
        tb_width, tb_height = 400, 80

        # Border
        msp.add_lwpolyline(
            [
                (tb_x, tb_y),
                (tb_x + tb_width, tb_y),
                (tb_x + tb_width, tb_y + tb_height),
                (tb_x, tb_y + tb_height),
                (tb_x, tb_y)
            ],
            dxfattribs={'layer': 'TITLE', 'lineweight': 50}
        )

        # Title
        msp.add_text(
            'FLOOR PLAN',
            dxfattribs={
                'layer': 'TITLE',
                'height': 12,
                'style': 'Standard'
            }
        ).set_placement((tb_x + 20, tb_y + tb_height - 20))

        # Details
        details = [
            f'Total Area: {floor_plan.total_sqft:.0f} sq ft',
            f'Bedrooms: {floor_plan.bedrooms}',
            f'Bathrooms: {floor_plan.bathrooms}',
            f'Style: {floor_plan.style.title()}',
            f'Scale: {scale}',
        ]

        y_offset = tb_y + tb_height - 40
        for detail in details:
            msp.add_text(
                detail,
                dxfattribs={'layer': 'TEXT', 'height': 6}
            ).set_placement((tb_x + 20, y_offset))
            y_offset -= 10

    def _draw_room(self, msp, room: Room):
        """Draw a room with walls, doors, windows, and labels"""
        x, y, width, height = room.x, room.y, room.width, room.height

        # Draw room boundary (walls)
        wall_thickness = 0.5  # 6 inches

        # Outer boundary
        msp.add_lwpolyline(
            [
                (x, y),
                (x + width, y),
                (x + width, y + height),
                (x, y + height),
                (x, y)
            ],
            dxfattribs={'layer': 'WALLS', 'lineweight': 70}
        )

        # Inner boundary (for wall thickness)
        msp.add_lwpolyline(
            [
                (x + wall_thickness, y + wall_thickness),
                (x + width - wall_thickness, y + wall_thickness),
                (x + width - wall_thickness, y + height - wall_thickness),
                (x + wall_thickness, y + height - wall_thickness),
                (x + wall_thickness, y + wall_thickness)
            ],
            dxfattribs={'layer': 'WALLS', 'lineweight': 50}
        )

        # Add room label
        center_x, center_y = room.center
        msp.add_text(
            room.name,
            dxfattribs={
                'layer': 'TEXT',
                'height': 8,
                'style': 'Standard'
            }
        ).set_placement(
            (center_x, center_y + 5),
            align=TextEntityAlignment.MIDDLE_CENTER
        )

        # Add area label
        msp.add_text(
            f'{room.area:.0f} SF',
            dxfattribs={'layer': 'TEXT', 'height': 5}
        ).set_placement(
            (center_x, center_y - 5),
            align=TextEntityAlignment.MIDDLE_CENTER
        )

        # Draw doors
        for door in room.doors:
            self._draw_door(msp, door)

        # Draw windows
        for window in room.windows:
            self._draw_window(msp, window)

    def _draw_door(self, msp, door: Dict):
        """Draw door symbol"""
        x, y = door['x'], door['y']
        width = door.get('width', 3)

        # Door opening
        msp.add_line(
            (x - width/2, y),
            (x + width/2, y),
            dxfattribs={'layer': 'DOORS', 'lineweight': 35}
        )

        # Door arc (showing swing)
        msp.add_arc(
            center=(x - width/2, y),
            radius=width,
            start_angle=0,
            end_angle=90,
            dxfattribs={'layer': 'DOORS', 'lineweight': 25}
        )

    def _draw_window(self, msp, window: Dict):
        """Draw window symbol"""
        x, y = window['x'], window['y']
        width = window.get('width', 4)

        # Window frame
        msp.add_line(
            (x - width/2, y),
            (x + width/2, y),
            dxfattribs={'layer': 'WINDOWS', 'lineweight': 35}
        )

        # Window panes (parallel lines)
        offset = 0.3
        msp.add_line(
            (x - width/2, y + offset),
            (x + width/2, y + offset),
            dxfattribs={'layer': 'WINDOWS', 'lineweight': 15}
        )
        msp.add_line(
            (x - width/2, y - offset),
            (x + width/2, y - offset),
            dxfattribs={'layer': 'WINDOWS', 'lineweight': 15}
        )

    def _add_dimensions(self, msp, floor_plan: FloorPlan):
        """Add dimensions to floor plan"""
        if not floor_plan.rooms:
            return

        # Find overall dimensions
        min_x = min(room.x for room in floor_plan.rooms)
        max_x = max(room.x + room.width for room in floor_plan.rooms)
        min_y = min(room.y for room in floor_plan.rooms)
        max_y = max(room.y + room.height for room in floor_plan.rooms)

        # Overall width dimension
        dim_y = min_y - 20
        msp.add_linear_dim(
            base=(min_x + (max_x - min_x)/2, dim_y),
            p1=(min_x, dim_y),
            p2=(max_x, dim_y),
            dimstyle='EZDXF',
            dxfattribs={'layer': 'DIMENSIONS'}
        )

        # Overall depth dimension
        dim_x = max_x + 20
        msp.add_linear_dim(
            base=(dim_x, min_y + (max_y - min_y)/2),
            p1=(dim_x, min_y),
            p2=(dim_x, max_y),
            angle=90,  # Vertical dimension
            dimstyle='EZDXF',
            dxfattribs={'layer': 'DIMENSIONS'}
        )

    def _add_room_schedule(self, msp, floor_plan: FloorPlan):
        """Add room schedule/legend"""
        # Position schedule to the right of the plan
        max_x = max(room.x + room.width for room in floor_plan.rooms) if floor_plan.rooms else 0
        schedule_x = max_x + 50
        schedule_y = max(room.y + room.height for room in floor_plan.rooms) if floor_plan.rooms else 100

        # Title
        msp.add_text(
            'ROOM SCHEDULE',
            dxfattribs={'layer': 'TEXT', 'height': 10}
        ).set_placement((schedule_x, schedule_y))

        # Headers
        y_offset = schedule_y - 20
        msp.add_text(
            'ROOM NAME',
            dxfattribs={'layer': 'TEXT', 'height': 6}
        ).set_placement((schedule_x, y_offset))

        msp.add_text(
            'AREA (SF)',
            dxfattribs={'layer': 'TEXT', 'height': 6}
        ).set_placement((schedule_x + 150, y_offset))

        # Room list
        y_offset -= 15
        total_area = 0

        for room in sorted(floor_plan.rooms, key=lambda r: r.name):
            msp.add_text(
                room.name,
                dxfattribs={'layer': 'TEXT', 'height': 5}
            ).set_placement((schedule_x, y_offset))

            msp.add_text(
                f'{room.area:.0f}',
                dxfattribs={'layer': 'TEXT', 'height': 5}
            ).set_placement((schedule_x + 150, y_offset))

            total_area += room.area
            y_offset -= 10

        # Total
        y_offset -= 5
        msp.add_line(
            (schedule_x, y_offset + 5),
            (schedule_x + 200, y_offset + 5),
            dxfattribs={'layer': 'TEXT'}
        )

        y_offset -= 10
        msp.add_text(
            'TOTAL',
            dxfattribs={'layer': 'TEXT', 'height': 6}
        ).set_placement((schedule_x, y_offset))

        msp.add_text(
            f'{total_area:.0f}',
            dxfattribs={'layer': 'TEXT', 'height': 6}
        ).set_placement((schedule_x + 150, y_offset))

    def import_from_dxf(self, dxf_file: BinaryIO) -> Dict:
        """
        Import and analyze DXF file

        Args:
            dxf_file: DXF file as BytesIO or file object

        Returns:
            Dictionary containing extracted elements
        """
        try:
            # Read DXF
            doc = ezdxf.readfile(dxf_file)
            msp = doc.modelspace()

            # Extract elements
            walls = []
            rooms = []
            doors = []
            windows = []
            texts = []

            for entity in msp:
                entity_type = entity.dxftype()

                if entity_type == 'LINE':
                    # Lines are typically walls
                    start = entity.dxf.start
                    end = entity.dxf.end
                    length = math.sqrt(
                        (end.x - start.x)**2 + (end.y - start.y)**2
                    )

                    # Filter out short lines (likely not walls)
                    if length > 5:
                        walls.append({
                            'start': {'x': float(start.x), 'y': float(start.y)},
                            'end': {'x': float(end.x), 'y': float(end.y)},
                            'length': round(length, 2),
                            'layer': entity.dxf.layer
                        })

                elif entity_type == 'LWPOLYLINE' or entity_type == 'POLYLINE':
                    # Polylines are typically room boundaries
                    points = []
                    try:
                        for point in entity.get_points():
                            points.append({'x': float(point[0]), 'y': float(point[1])})
                    except:
                        continue

                    if len(points) >= 3:  # Valid room boundary
                        # Calculate approximate area
                        area = self._calculate_polygon_area(points)

                        rooms.append({
                            'points': points,
                            'area': round(area, 2),
                            'layer': entity.dxf.layer
                        })

                elif entity_type in ['TEXT', 'MTEXT']:
                    # Text labels (room names, dimensions)
                    try:
                        text_content = entity.dxf.text
                        insert_point = entity.dxf.insert

                        texts.append({
                            'text': text_content,
                            'x': float(insert_point.x),
                            'y': float(insert_point.y),
                            'height': float(entity.dxf.height) if hasattr(entity.dxf, 'height') else 10,
                            'layer': entity.dxf.layer
                        })
                    except:
                        continue

                elif entity_type == 'ARC':
                    # Arcs are often door swings
                    center = entity.dxf.center
                    radius = entity.dxf.radius

                    doors.append({
                        'x': float(center.x),
                        'y': float(center.y),
                        'radius': round(radius, 2),
                        'layer': entity.dxf.layer
                    })

                elif entity_type == 'INSERT':
                    # Blocks (often used for doors, windows, furniture)
                    block_name = entity.dxf.name.lower()
                    insert_point = entity.dxf.insert

                    if 'door' in block_name:
                        doors.append({
                            'x': float(insert_point.x),
                            'y': float(insert_point.y),
                            'type': 'block',
                            'name': entity.dxf.name
                        })
                    elif 'window' in block_name or 'win' in block_name:
                        windows.append({
                            'x': float(insert_point.x),
                            'y': float(insert_point.y),
                            'type': 'block',
                            'name': entity.dxf.name
                        })

            # Analyze and return results
            return {
                'walls': walls,
                'rooms': rooms,
                'doors': doors,
                'windows': windows,
                'texts': texts,
                'stats': {
                    'wall_count': len(walls),
                    'room_count': len(rooms),
                    'door_count': len(doors),
                    'window_count': len(windows),
                    'text_count': len(texts),
                    'total_wall_length': sum(w['length'] for w in walls),
                    'total_area': sum(r['area'] for r in rooms)
                },
                'metadata': {
                    'units': doc.units.name if hasattr(doc, 'units') else 'UNKNOWN',
                    'version': doc.dxfversion,
                    'layers': [layer.dxf.name for layer in doc.layers]
                }
            }

        except Exception as e:
            raise Exception(f'DXF import failed: {str(e)}')

    def _calculate_polygon_area(self, points: List[Dict]) -> float:
        """Calculate area of polygon using shoelace formula"""
        n = len(points)
        if n < 3:
            return 0

        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += points[i]['x'] * points[j]['y']
            area -= points[j]['x'] * points[i]['y']

        return abs(area) / 2

    def export_to_svg(self, floor_plan: FloorPlan, width: int = 1000, height: int = 800) -> str:
        """
        Export floor plan to SVG format

        Args:
            floor_plan: FloorPlan to export
            width: SVG canvas width
            height: SVG canvas height

        Returns:
            SVG string
        """
        if not floor_plan.rooms:
            return '<svg></svg>'

        # Calculate bounds
        min_x = min(room.x for room in floor_plan.rooms)
        min_y = min(room.y for room in floor_plan.rooms)
        max_x = max(room.x + room.width for room in floor_plan.rooms)
        max_y = max(room.y + room.height for room in floor_plan.rooms)

        # Calculate scale to fit in canvas
        plan_width = max_x - min_x
        plan_height = max_y - min_y
        scale_x = (width - 100) / plan_width if plan_width > 0 else 1
        scale_y = (height - 100) / plan_height if plan_height > 0 else 1
        scale = min(scale_x, scale_y)

        # Build SVG
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .wall {{ fill: none; stroke: #000; stroke-width: 3; }}
            .room-fill {{ stroke: #333; stroke-width: 2; opacity: 0.7; }}
            .room-label {{ font-family: Arial; font-size: 14px; font-weight: bold; text-anchor: middle; }}
            .room-area {{ font-family: Arial; font-size: 11px; text-anchor: middle; fill: #666; }}
            .door {{ stroke: #4CAF50; stroke-width: 2; fill: none; }}
            .window {{ stroke: #2196F3; stroke-width: 2; fill: none; }}
        </style>
    </defs>

    <rect width="100%" height="100%" fill="#f5f5f5"/>

    <g transform="translate(50, 50)">
'''

        # Draw rooms
        for room in floor_plan.rooms:
            x = (room.x - min_x) * scale
            y = (room.y - min_y) * scale
            w = room.width * scale
            h = room.height * scale
            cx, cy = x + w/2, y + h/2

            # Room rectangle
            svg += f'''        <rect x="{x}" y="{y}" width="{w}" height="{h}"
                  class="room-fill" fill="{room.color}"/>
'''

            # Room label
            svg += f'''        <text x="{cx}" y="{cy - 5}" class="room-label">{room.name}</text>
        <text x="{cx}" y="{cy + 15}" class="room-area">{room.area:.0f} sq ft</text>
'''

            # Doors
            for door in room.doors:
                dx = (door['x'] - min_x) * scale
                dy = (door['y'] - min_y) * scale
                dw = door.get('width', 3) * scale
                svg += f'        <line x1="{dx - dw/2}" y1="{dy}" x2="{dx + dw/2}" y2="{dy}" class="door"/>\n'

            # Windows
            for window in room.windows:
                wx = (window['x'] - min_x) * scale
                wy = (window['y'] - min_y) * scale
                ww = window.get('width', 4) * scale
                svg += f'        <line x1="{wx - ww/2}" y1="{wy}" x2="{wx + ww/2}" y2="{wy}" class="window"/>\n'

        svg += '''    </g>
</svg>'''

        return svg
