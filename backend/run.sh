#!/bin/bash
# Production startup script for AI Floor Plan Generator Backend

set -e

echo "🏗️  AI Floor Plan Generator - Starting Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads temp

# Run application
echo "🚀 Starting Flask application..."
echo "   API will be available at: http://localhost:5000"
echo "   Health check: http://localhost:5000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Use gunicorn for production, flask for development
if [ "$FLASK_ENV" = "production" ]; then
    echo "Running in PRODUCTION mode with Gunicorn..."
    gunicorn -w 4 -b 0.0.0.0:5000 app:app --access-logfile - --error-logfile -
else
    echo "Running in DEVELOPMENT mode..."
    python app.py
fi
