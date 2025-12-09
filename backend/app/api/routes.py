"""
REST API Routes for Floor Plan Generator
Production-grade with comprehensive error handling and validation
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import traceback
from app.core.ai_architect import AIArchitect
from app.core.cad_engine import CADEngine
from app.core.code_validator import BuildingCodeValidator
from app.models.room import FloorPlan, Room, RoomType
from config import Config

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Initialize services
ai_architect = AIArchitect()
cad_engine = CADEngine()
code_validator = BuildingCodeValidator()
config = Config()

# Error handlers
class APIError(Exception):
    """Custom API error"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['success'] = False
        return rv

@api.errorhandler(APIError)
def handle_api_error(error):
    """Handle custom API errors"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@api.errorhandler(Exception)
def handle_generic_error(error):
    """Handle unexpected errors"""
    print(f"Unexpected error: {str(error)}")
    traceback.print_exc()
    return jsonify({
        'error': 'Internal server error',
        'success': False,
        'details': str(error) if config.DEBUG else None
    }), 500

# Utility functions
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def validate_floor_plan_params(data):
    """Validate floor plan generation parameters"""
    errors = []

    total_sqft = data.get('totalSqFt')
    if not total_sqft or not isinstance(total_sqft, (int, float)):
        errors.append('totalSqFt is required and must be a number')
    elif total_sqft < 500 or total_sqft > 20000:
        errors.append('totalSqFt must be between 500 and 20,000')

    bedrooms = data.get('bedrooms')
    if not bedrooms or not isinstance(bedrooms, int):
        errors.append('bedrooms is required and must be an integer')
    elif bedrooms < 1 or bedrooms > 10:
        errors.append('bedrooms must be between 1 and 10')

    bathrooms = data.get('bathrooms')
    if not bathrooms or not isinstance(bathrooms, (int, float)):
        errors.append('bathrooms is required and must be a number')
    elif bathrooms < 1 or bathrooms > 8:
        errors.append('bathrooms must be between 1 and 8')

    return errors

# API Routes

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Floor Plan Generator',
        'version': '1.0.0',
        'features': {
            'ai_generation': True,
            'cad_export': True,
            'cad_import': True,
            'code_validation': True
        }
    })

@api.route('/generate', methods=['POST'])
def generate_floor_plan():
    """
    Generate intelligent floor plan using AI architect

    Request body:
    {
        "totalSqFt": 2000,
        "bedrooms": 3,
        "bathrooms": 2,
        "style": "modern",
        "specialRooms": {
            "office": true,
            "garage": true,
            "garage_cars": 2,
            "temple": false
        }
    }
    """
    try:
        data = request.get_json()

        if not data:
            raise APIError('Request body is required', 400)

        # Validate parameters
        errors = validate_floor_plan_params(data)
        if errors:
            raise APIError('Validation failed', 400, {'errors': errors})

        # Extract parameters
        total_sqft = float(data['totalSqFt'])
        bedrooms = int(data['bedrooms'])
        bathrooms = float(data['bathrooms'])
        style = data.get('style', 'modern')
        special_rooms = data.get('specialRooms', {})

        # Generate floor plan using AI
        floor_plan = ai_architect.generate_floor_plan(
            total_sqft=total_sqft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            style=style,
            special_rooms=special_rooms
        )

        # Validate against building codes
        validation = code_validator.validate_floor_plan(floor_plan)

        return jsonify({
            'success': True,
            'floorPlan': floor_plan.to_dict(),
            'validation': validation,
            'message': 'Floor plan generated successfully'
        })

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'Floor plan generation failed: {str(e)}', 500)

@api.route('/validate', methods=['POST'])
def validate_plan():
    """
    Validate a floor plan against building codes

    Request body should contain floor plan data
    """
    try:
        data = request.get_json()

        if not data or 'rooms' not in data:
            raise APIError('Floor plan data is required', 400)

        # Reconstruct floor plan from data
        floor_plan = FloorPlan(
            total_sqft=data.get('total_sqft', 0),
            bedrooms=data.get('bedrooms', 0),
            bathrooms=data.get('bathrooms', 0),
            style=data.get('style', 'modern')
        )

        # Reconstruct rooms
        for room_data in data['rooms']:
            room = Room(
                name=room_data['name'],
                room_type=RoomType(room_data['type']),
                x=room_data['x'],
                y=room_data['y'],
                width=room_data['width'],
                height=room_data['height'],
                area=room_data['area'],
                color=room_data.get('color', '#ffffff'),
                doors=room_data.get('doors', []),
                windows=room_data.get('windows', [])
            )
            floor_plan.rooms.append(room)

        # Validate
        validation = code_validator.validate_floor_plan(floor_plan)

        # Generate report
        report = code_validator.generate_compliance_report(validation)

        return jsonify({
            'success': True,
            'validation': validation,
            'report': report
        })

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'Validation failed: {str(e)}', 500)

@api.route('/export/dxf', methods=['POST'])
def export_dxf():
    """
    Export floor plan to DXF format

    Request body should contain floor plan data
    """
    try:
        data = request.get_json()

        if not data or 'rooms' not in data:
            raise APIError('Floor plan data is required', 400)

        # Reconstruct floor plan
        floor_plan = FloorPlan(
            total_sqft=data.get('total_sqft', 0),
            bedrooms=data.get('bedrooms', 0),
            bathrooms=data.get('bathrooms', 0),
            style=data.get('style', 'modern')
        )

        for room_data in data['rooms']:
            room = Room(
                name=room_data['name'],
                room_type=RoomType(room_data.get('type', 'living')),
                x=room_data['x'],
                y=room_data['y'],
                width=room_data['width'],
                height=room_data['height'],
                area=room_data['area'],
                color=room_data.get('color', '#ffffff'),
                doors=room_data.get('doors', []),
                windows=room_data.get('windows', [])
            )
            floor_plan.rooms.append(room)

        # Export to DXF
        scale = data.get('scale', '1:50')
        dxf_file = cad_engine.export_to_dxf(floor_plan, scale)

        return send_file(
            dxf_file,
            mimetype='application/dxf',
            as_attachment=True,
            download_name='floor-plan.dxf'
        )

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'DXF export failed: {str(e)}', 500)

@api.route('/export/svg', methods=['POST'])
def export_svg():
    """Export floor plan to SVG format"""
    try:
        data = request.get_json()

        if not data or 'rooms' not in data:
            raise APIError('Floor plan data is required', 400)

        # Reconstruct floor plan
        floor_plan = FloorPlan(
            total_sqft=data.get('total_sqft', 0),
            bedrooms=data.get('bedrooms', 0),
            bathrooms=data.get('bathrooms', 0)
        )

        for room_data in data['rooms']:
            room = Room(
                name=room_data['name'],
                room_type=RoomType(room_data.get('type', 'living')),
                x=room_data['x'],
                y=room_data['y'],
                width=room_data['width'],
                height=room_data['height'],
                area=room_data['area'],
                color=room_data.get('color', '#ffffff'),
                doors=room_data.get('doors', []),
                windows=room_data.get('windows', [])
            )
            floor_plan.rooms.append(room)

        # Export to SVG
        svg_content = cad_engine.export_to_svg(floor_plan)

        return svg_content, 200, {
            'Content-Type': 'image/svg+xml',
            'Content-Disposition': 'attachment; filename=floor-plan.svg'
        }

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'SVG export failed: {str(e)}', 500)

@api.route('/import/dxf', methods=['POST'])
def import_dxf():
    """
    Import and analyze DXF file

    Expects multipart/form-data with 'file' field
    """
    try:
        if 'file' not in request.files:
            raise APIError('No file uploaded', 400)

        file = request.files['file']

        if file.filename == '':
            raise APIError('No file selected', 400)

        if not allowed_file(file.filename):
            raise APIError(
                f'Invalid file type. Allowed: {", ".join(config.ALLOWED_EXTENSIONS)}',
                400
            )

        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        if file_size > config.MAX_UPLOAD_SIZE:
            raise APIError(
                f'File too large. Maximum size: {config.MAX_UPLOAD_SIZE / 1024 / 1024:.0f}MB',
                400
            )

        # Save temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(config.TEMP_FOLDER, filename)
        file.save(temp_path)

        try:
            # Import and analyze
            with open(temp_path, 'rb') as dxf_file:
                analysis = cad_engine.import_from_dxf(dxf_file)

            return jsonify({
                'success': True,
                'analysis': analysis,
                'message': 'DXF file imported and analyzed successfully'
            })

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'DXF import failed: {str(e)}', 500)

@api.route('/analyze', methods=['POST'])
def analyze_plan():
    """
    Comprehensive analysis of floor plan

    Returns:
    - Building code validation
    - Space efficiency
    - Energy efficiency estimates
    - Recommendations
    """
    try:
        data = request.get_json()

        if not data or 'rooms' not in data:
            raise APIError('Floor plan data is required', 400)

        # Reconstruct floor plan
        floor_plan = FloorPlan(
            total_sqft=data.get('total_sqft', 0),
            bedrooms=data.get('bedrooms', 0),
            bathrooms=data.get('bathrooms', 0),
            style=data.get('style', 'modern')
        )

        for room_data in data['rooms']:
            room = Room(
                name=room_data['name'],
                room_type=RoomType(room_data.get('type', 'living')),
                x=room_data['x'],
                y=room_data['y'],
                width=room_data['width'],
                height=room_data['height'],
                area=room_data['area'],
                color=room_data.get('color', '#ffffff'),
                doors=room_data.get('doors', []),
                windows=room_data.get('windows', []),
                orientation=room_data.get('orientation')
            )
            floor_plan.rooms.append(room)

        # Validate
        validation = code_validator.validate_floor_plan(floor_plan)

        # Calculate energy efficiency score
        energy_score = calculate_energy_efficiency(floor_plan)

        # Generate recommendations
        recommendations = generate_recommendations(floor_plan, validation)

        return jsonify({
            'success': True,
            'validation': validation,
            'stats': floor_plan.to_dict()['stats'],
            'energyEfficiency': energy_score,
            'recommendations': recommendations
        })

    except APIError:
        raise
    except Exception as e:
        raise APIError(f'Analysis failed: {str(e)}', 500)

# Helper functions

def calculate_energy_efficiency(floor_plan: FloorPlan) -> Dict:
    """Calculate estimated energy efficiency"""
    # Simple estimation based on:
    # - Building shape (compactness)
    # - Room orientation
    # - Window placement

    if not floor_plan.rooms:
        return {'score': 0, 'grade': 'N/A'}

    # Calculate compactness (area to perimeter ratio)
    total_area = sum(room.area for room in floor_plan.rooms)
    total_perimeter = sum(room.perimeter for room in floor_plan.rooms)

    compactness = total_area / total_perimeter if total_perimeter > 0 else 0

    # Ideal compactness for energy efficiency (square shape ≈ 0.25)
    compactness_score = min(100, compactness / 0.25 * 100)

    # Check room orientations
    south_facing_rooms = sum(1 for room in floor_plan.rooms
                            if room.orientation and 'south' in room.orientation.value.lower())

    orientation_score = min(100, (south_facing_rooms / len(floor_plan.rooms)) * 200)

    # Overall score
    score = (compactness_score * 0.6 + orientation_score * 0.4)

    grade = 'A' if score >= 85 else 'B' if score >= 70 else 'C' if score >= 55 else 'D'

    return {
        'score': round(score, 1),
        'grade': grade,
        'compactness': round(compactness_score, 1),
        'orientation': round(orientation_score, 1),
        'details': {
            'building_compactness': round(compactness, 3),
            'south_facing_rooms': south_facing_rooms,
            'total_rooms': len(floor_plan.rooms)
        }
    }

def generate_recommendations(floor_plan: FloorPlan, validation: Dict) -> List[Dict]:
    """Generate actionable recommendations"""
    recommendations = []

    # Based on violations
    if validation['summary']['critical'] > 0:
        recommendations.append({
            'priority': 'high',
            'category': 'Building Code',
            'title': 'Critical Code Violations',
            'description': f"Address {validation['summary']['critical']} critical building code violations before construction",
            'action': 'Review validation report and make necessary changes'
        })

    # Based on efficiency
    efficiency = floor_plan.efficiency_ratio
    if efficiency < 80:
        recommendations.append({
            'priority': 'medium',
            'category': 'Space Efficiency',
            'title': 'Improve Space Utilization',
            'description': f'Current efficiency is {efficiency:.1f}%. Consider reducing circulation areas',
            'action': 'Optimize hallway and transition spaces'
        })

    # Based on room sizes
    for room in floor_plan.rooms:
        if room.aspect_ratio > 2.5:
            recommendations.append({
                'priority': 'low',
                'category': 'Room Design',
                'title': f'Balance {room.name} Proportions',
                'description': f'Room has unusual aspect ratio ({room.aspect_ratio:.1f}:1)',
                'action': 'Consider more balanced width-to-length ratio'
            })

    return recommendations[:10]  # Limit to top 10
