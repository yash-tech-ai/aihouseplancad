#!/bin/bash
# Quick Start Script for AI Floor Plan Generator
# One command to start everything!

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║   🏗️  AI FLOOR PLAN GENERATOR - QUICK START  🏗️        ║"
echo "║       World-Class Production System                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

print_success "Python $(python3 --version) found"

# Navigate to project directory
cd "$(dirname "$0")"
print_status "Working directory: $(pwd)"

# Setup backend
print_status "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies (this may take a moment)..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependencies installed"

# Create necessary directories
mkdir -p uploads temp
print_success "Directories created"

# Go back to root
cd ..

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                 🚀 STARTING SERVICES 🚀                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    print_warning "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    print_success "Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
print_status "Starting backend API server..."
cd backend
source venv/bin/activate
python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if kill -0 $BACKEND_PID 2>/dev/null; then
    print_success "Backend API running on http://localhost:5000"
    print_status "   Health check: http://localhost:5000/api/health"
else
    print_error "Backend failed to start! Check backend.log for errors"
    cat backend.log
    exit 1
fi

# Start frontend
print_status "Starting frontend server..."
python3 -m http.server 8000 > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

# Check if frontend is running
if kill -0 $FRONTEND_PID 2>/dev/null; then
    print_success "Frontend running on http://localhost:8000"
else
    print_error "Frontend failed to start!"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              ✨ SYSTEM READY! ✨                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Open your browser and visit:"
echo "   ${GREEN}http://localhost:8000/floor-plan-generator.html${NC}"
echo ""
echo "📊 API Documentation:"
echo "   ${BLUE}http://localhost:5000${NC}"
echo ""
echo "🏥 Health Check:"
echo "   ${BLUE}http://localhost:5000/api/health${NC}"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "⚡ Quick Test:"
echo "   cd backend && source venv/bin/activate && python test_system.py"
echo ""
echo "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""
print_status "Monitoring services... (logs being written to backend.log and frontend.log)"

# Monitor processes
while kill -0 $BACKEND_PID 2>/dev/null && kill -0 $FRONTEND_PID 2>/dev/null; do
    sleep 2
done

# If we get here, something crashed
print_error "One or more services stopped unexpectedly!"
echo "Check logs for details:"
echo "  tail backend.log"
echo "  tail frontend.log"
cleanup
