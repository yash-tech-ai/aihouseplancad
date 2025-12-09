"""
Production-Grade Flask Application for AI Floor Plan Generator
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import config, Config
import os

def create_app(config_name='production'):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['ALLOWED_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize directories
    Config.init_app()

    # Register blueprints
    from app.api.routes import api
    app.register_blueprint(api)

    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'service': 'AI Floor Plan Generator API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'generate': '/api/generate (POST)',
                'validate': '/api/validate (POST)',
                'analyze': '/api/analyze (POST)',
                'export_dxf': '/api/export/dxf (POST)',
                'export_svg': '/api/export/svg (POST)',
                'import_dxf': '/api/import/dxf (POST)'
            },
            'documentation': 'https://github.com/yourusername/ai-floor-plan-cad'
        })

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint not found',
            'status': 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'status': 500
        }), 500

    return app

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # For development only - use gunicorn in production
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
