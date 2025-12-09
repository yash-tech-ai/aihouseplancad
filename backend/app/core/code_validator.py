"""
Building Code Validation System
Based on International Residential Code (IRC) and universal best practices
"""
from typing import List, Dict, Tuple
from app.models.room import FloorPlan, Room, RoomType
from config import Config

class CodeViolation:
    """Represents a building code violation"""
    def __init__(self, severity: str, room: str, code: str, message: str, recommendation: str = ""):
        self.severity = severity  # 'critical', 'warning', 'info'
        self.room = room
        self.code = code
        self.message = message
        self.recommendation = recommendation

    def to_dict(self) -> Dict:
        return {
            'severity': self.severity,
            'room': self.room,
            'code': self.code,
            'message': self.message,
            'recommendation': self.recommendation
        }

class BuildingCodeValidator:
    """
    Validates floor plans against building codes and best practices
    """

    def __init__(self):
        self.config = Config()
        self.codes = self.config.BUILDING_CODES

    def validate_floor_plan(self, floor_plan: FloorPlan) -> Dict:
        """
        Comprehensive validation of floor plan

        Returns:
            Dictionary with validation results and violations
        """
        violations = []

        # Validate each room
        for room in floor_plan.rooms:
            violations.extend(self._validate_room(room))

        # Validate overall plan
        violations.extend(self._validate_overall_plan(floor_plan))

        # Validate egress requirements
        violations.extend(self._validate_egress(floor_plan))

        # Validate circulation
        violations.extend(self._validate_circulation(floor_plan))

        # Calculate compliance score
        critical_count = sum(1 for v in violations if v.severity == 'critical')
        warning_count = sum(1 for v in violations if v.severity == 'warning')
        info_count = sum(1 for v in violations if v.severity == 'info')

        # Score: 100 - (critical * 20) - (warning * 5) - (info * 1)
        compliance_score = max(0, 100 - (critical_count * 20) - (warning_count * 5) - (info_count * 1))

        return {
            'compliant': critical_count == 0,
            'compliance_score': compliance_score,
            'violations': [v.to_dict() for v in violations],
            'summary': {
                'critical': critical_count,
                'warnings': warning_count,
                'info': info_count,
                'total': len(violations)
            },
            'grade': self._calculate_grade(compliance_score)
        }

    def _validate_room(self, room: Room) -> List[CodeViolation]:
        """Validate individual room against codes"""
        violations = []

        # Check minimum room sizes
        min_sizes = self.codes['room_minimums']

        if room.room_type == RoomType.BEDROOM or room.room_type == RoomType.MASTER_BEDROOM:
            min_size = min_sizes['bedroom']
            if room.area < min_size:
                violations.append(CodeViolation(
                    severity='critical',
                    room=room.name,
                    code='IRC R304.1',
                    message=f'Bedroom area {room.area:.0f} sq ft is below minimum {min_size} sq ft',
                    recommendation=f'Increase room area by {min_size - room.area:.0f} sq ft'
                ))

        elif room.room_type == RoomType.BATHROOM or room.room_type == RoomType.MASTER_BATHROOM:
            min_size = min_sizes['bathroom']
            if room.area < min_size:
                violations.append(CodeViolation(
                    severity='critical',
                    room=room.name,
                    code='IRC R307',
                    message=f'Bathroom area {room.area:.0f} sq ft is below minimum {min_size} sq ft',
                    recommendation=f'Increase room area by {min_size - room.area:.0f} sq ft'
                ))

        elif room.room_type == RoomType.KITCHEN:
            min_size = min_sizes['kitchen']
            if room.area < min_size:
                violations.append(CodeViolation(
                    severity='warning',
                    room=room.name,
                    code='IRC R305',
                    message=f'Kitchen area {room.area:.0f} sq ft is below recommended {min_size} sq ft',
                    recommendation='Consider increasing kitchen size for better functionality'
                ))

        elif room.room_type == RoomType.LIVING:
            min_size = min_sizes['living']
            if room.area < min_size:
                violations.append(CodeViolation(
                    severity='warning',
                    room=room.name,
                    code='Best Practice',
                    message=f'Living room area {room.area:.0f} sq ft is below recommended {min_size} sq ft',
                    recommendation='Consider larger living space for comfort'
                ))

        # Check aspect ratio (shouldn't be too narrow)
        if room.aspect_ratio > 3.0:
            violations.append(CodeViolation(
                severity='info',
                room=room.name,
                code='Design Guideline',
                message=f'Room aspect ratio {room.aspect_ratio:.1f}:1 is unusually narrow',
                recommendation='Consider more balanced proportions for better space utilization'
            ))

        # Check for egress windows in bedrooms
        if room.room_type in [RoomType.BEDROOM, RoomType.MASTER_BEDROOM]:
            egress_windows = [w for w in room.windows if w.get('type') == 'egress']
            if not egress_windows:
                violations.append(CodeViolation(
                    severity='critical',
                    room=room.name,
                    code='IRC R310.1',
                    message='Bedroom requires egress window for emergency escape',
                    recommendation='Add egress window with min 5.7 sq ft opening'
                ))
            else:
                # Validate egress window size
                for window in egress_windows:
                    window_area = window.get('width', 0) * window.get('height', 0)
                    min_egress_area = self.codes['egress']['bedroom_window_min_area']
                    if window_area < min_egress_area:
                        violations.append(CodeViolation(
                            severity='critical',
                            room=room.name,
                            code='IRC R310.2.1',
                            message=f'Egress window {window_area:.1f} sq ft is below minimum {min_egress_area} sq ft',
                            recommendation=f'Increase window size by {min_egress_area - window_area:.1f} sq ft'
                        ))

        return violations

    def _validate_overall_plan(self, floor_plan: FloorPlan) -> List[CodeViolation]:
        """Validate overall floor plan"""
        violations = []

        # Check total living area vs claimed square footage
        actual_total = sum(room.area for room in floor_plan.rooms)
        claimed_total = floor_plan.total_sqft

        variance = abs(actual_total - claimed_total) / claimed_total * 100

        if variance > 10:  # More than 10% variance
            violations.append(CodeViolation(
                severity='warning',
                room='Overall Plan',
                code='Design Consistency',
                message=f'Total room area {actual_total:.0f} sq ft differs from target {claimed_total:.0f} sq ft by {variance:.1f}%',
                recommendation='Adjust room sizes to match target square footage'
            ))

        # Check efficiency ratio
        efficiency = floor_plan.efficiency_ratio

        if efficiency < 75:
            violations.append(CodeViolation(
                severity='info',
                room='Overall Plan',
                code='Space Efficiency',
                message=f'Space efficiency {efficiency:.1f}% is below recommended 75%',
                recommendation='Review circulation and storage areas to improve efficiency'
            ))

        # Validate required rooms
        bedrooms = floor_plan.get_rooms_by_type(RoomType.BEDROOM)
        master_bedrooms = floor_plan.get_rooms_by_type(RoomType.MASTER_BEDROOM)
        total_bedrooms = len(bedrooms) + len(master_bedrooms)

        if total_bedrooms < floor_plan.bedrooms:
            violations.append(CodeViolation(
                severity='critical',
                room='Overall Plan',
                code='Design Requirement',
                message=f'Plan has {total_bedrooms} bedrooms but requires {floor_plan.bedrooms}',
                recommendation=f'Add {floor_plan.bedrooms - total_bedrooms} more bedroom(s)'
            ))

        bathrooms = floor_plan.get_rooms_by_type(RoomType.BATHROOM)
        master_bathrooms = floor_plan.get_rooms_by_type(RoomType.MASTER_BATHROOM)
        total_bathrooms = len(bathrooms) + len(master_bathrooms)

        if total_bathrooms < floor_plan.bathrooms:
            violations.append(CodeViolation(
                severity='critical',
                room='Overall Plan',
                code='Design Requirement',
                message=f'Plan has {total_bathrooms} bathrooms but requires {floor_plan.bathrooms}',
                recommendation=f'Add {floor_plan.bathrooms - total_bathrooms} more bathroom(s)'
            ))

        return violations

    def _validate_egress(self, floor_plan: FloorPlan) -> List[CodeViolation]:
        """Validate egress (emergency exit) requirements"""
        violations = []

        # Every floor must have at least one egress door
        # Every bedroom must have egress window (checked in _validate_room)

        # Check if plan has accessible exit
        has_door_to_exterior = False

        # Check for rooms with exterior access
        for room in floor_plan.rooms:
            if room.room_type in [RoomType.LIVING, RoomType.KITCHEN, RoomType.GARAGE]:
                if room.doors:
                    has_door_to_exterior = True
                    break

        if not has_door_to_exterior:
            violations.append(CodeViolation(
                severity='critical',
                room='Overall Plan',
                code='IRC R311.2',
                message='No clear egress door to exterior identified',
                recommendation='Ensure at least one exterior door for building exit'
            ))

        return violations

    def _validate_circulation(self, floor_plan: FloorPlan) -> List[CodeViolation]:
        """Validate circulation and accessibility"""
        violations = []

        # Check for hallways if needed (bedrooms not adjacent to living areas)
        bedrooms = [r for r in floor_plan.rooms
                   if r.room_type in [RoomType.BEDROOM, RoomType.MASTER_BEDROOM]]

        if len(bedrooms) > 2:
            # Check if there's a hallway or circulation space
            hallways = floor_plan.get_rooms_by_type(RoomType.HALLWAY)

            if not hallways:
                violations.append(CodeViolation(
                    severity='info',
                    room='Overall Plan',
                    code='Design Guideline',
                    message='Multiple bedrooms without dedicated hallway circulation',
                    recommendation='Consider adding hallway for better privacy and access'
                ))

        # Check minimum hallway width if hallways exist
        min_hallway_width = self.codes['room_minimums']['hallway_width']

        for room in floor_plan.rooms:
            if room.room_type == RoomType.HALLWAY:
                min_dimension = min(room.width, room.height)
                if min_dimension < min_hallway_width:
                    violations.append(CodeViolation(
                        severity='critical',
                        room=room.name,
                        code='IRC R311.6',
                        message=f'Hallway width {min_dimension:.1f} ft is below minimum {min_hallway_width} ft',
                        recommendation=f'Increase hallway width to at least {min_hallway_width} ft'
                    ))

        return violations

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from compliance score"""
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'B+'
        elif score >= 80:
            return 'B'
        elif score >= 75:
            return 'C+'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def generate_compliance_report(self, validation_result: Dict) -> str:
        """Generate human-readable compliance report"""
        report = f"""
BUILDING CODE COMPLIANCE REPORT
================================

Overall Grade: {validation_result['grade']}
Compliance Score: {validation_result['compliance_score']}/100
Status: {'COMPLIANT' if validation_result['compliant'] else 'NON-COMPLIANT'}

Summary:
--------
Critical Violations: {validation_result['summary']['critical']}
Warnings: {validation_result['summary']['warnings']}
Informational: {validation_result['summary']['info']}
Total Issues: {validation_result['summary']['total']}

"""

        if validation_result['violations']:
            report += "\nDetailed Violations:\n"
            report += "-------------------\n\n"

            # Group by severity
            for severity in ['critical', 'warning', 'info']:
                violations = [v for v in validation_result['violations']
                            if v['severity'] == severity]

                if violations:
                    report += f"\n{severity.upper()}:\n"
                    for v in violations:
                        report += f"  [{v['code']}] {v['room']}\n"
                        report += f"    Issue: {v['message']}\n"
                        if v['recommendation']:
                            report += f"    Fix: {v['recommendation']}\n"
                        report += "\n"
        else:
            report += "\n✓ No violations found. Plan is fully compliant!\n"

        return report
