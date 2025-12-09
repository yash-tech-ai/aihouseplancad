@echo off
REM Complete System Test for Windows

echo ╔════════════════════════════════════════════════════════╗
echo ║            🧪 SYSTEM TEST SUITE 🧪                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd backend

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [INFO] Running comprehensive tests...
echo.

REM Run tests
python test_system.py

echo.
echo [INFO] Test complete! Review results above.
pause
