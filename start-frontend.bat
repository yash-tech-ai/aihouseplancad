@echo off
REM Frontend Server for Windows
REM Serves the HTML interface

echo ╔════════════════════════════════════════════════════════╗
echo ║           🌐 STARTING FRONTEND SERVER 🌐               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    pause
    exit /b 1
)

echo [✓] Starting frontend on http://localhost:8000
echo [✓] Open your browser to:
echo.
echo     http://localhost:8000/floor-plan-generator.html
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ══════════════════════════════════════════════════════════
echo.

REM Start Python HTTP server
python -m http.server 8000
