"""
Production-Grade Configuration Management
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    # Base Directory
    BASE_DIR = Path(__file__).parent

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # CORS Settings
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

    # File Upload Settings
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = {'dxf', 'dwg', 'pdf', 'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    TEMP_FOLDER = BASE_DIR / 'temp'

    # CAD Export Settings
    DXF_VERSION = os.getenv('DXF_VERSION', 'R2010')
    DEFAULT_UNITS = os.getenv('DEFAULT_UNITS', 'feet')

    # AI Layout Settings
    MIN_ROOM_SIZE = int(os.getenv('MIN_ROOM_SIZE', 50))
    MAX_ROOM_SIZE = int(os.getenv('MAX_ROOM_SIZE', 1000))
    OPTIMIZATION_ITERATIONS = int(os.getenv('OPTIMIZATION_ITERATIONS', 100))

    # Building Codes (International Residential Code - IRC)
    BUILDING_CODES = {
        'room_minimums': {
            'bedroom': 70,  # sq ft
            'bathroom': 35,
            'kitchen': 50,
            'living': 120,
            'hallway_width': 3,  # feet
        },
        'egress': {
            'bedroom_window_min_area': 5.7,  # sq ft
            'bedroom_window_min_width': 20,  # inches
            'bedroom_window_min_height': 24,
        },
        'ceiling_height': {
            'habitable_rooms': 7,  # feet
            'bathrooms': 6.67,
        }
    }

    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        cls.UPLOAD_FOLDER.mkdir(exist_ok=True)
        cls.TEMP_FOLDER.mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}
