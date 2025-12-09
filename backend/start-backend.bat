@echo off
REM Quick Start Script for Windows
REM AI Floor Plan Generator

echo ╔════════════════════════════════════════════════════════╗
echo ║   🏗️  AI FLOOR PLAN GENERATOR - WINDOWS SETUP  🏗️      ║
echo ║       World-Class Production System                    ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python found:
python --version
echo.

REM Navigate to backend directory
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and install dependencies
echo [INFO] Installing dependencies (this may take a moment)...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [✓] Dependencies installed
echo.

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "temp" mkdir temp
echo [✓] Directories created
echo.

REM Copy .env.example to .env if .env doesn't exist
if not exist ".env" (
    copy .env.example .env >nul
    echo [✓] Environment file created
)

echo ╔════════════════════════════════════════════════════════╗
echo ║                 🚀 STARTING BACKEND 🚀                  ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo [INFO] Backend API starting on http://localhost:5000
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ══════════════════════════════════════════════════════════
echo.

REM Start the Flask application
python app.py
