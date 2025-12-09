# PowerShell Script for Backend - AI Floor Plan Generator

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   AI FLOOR PLAN GENERATOR - BACKEND SETUP" -ForegroundColor Cyan
Write-Host "   World-Class Production System" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    Write-Host "[ERROR] Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green

# Check Python version and warn if 3.13
if ($pythonVersion -match "3\.13") {
    Write-Host "[WARNING] Python 3.13 detected - using minimal dependencies" -ForegroundColor Yellow
    Write-Host "[INFO] Some packages need C++ compiler on Windows" -ForegroundColor Yellow
}
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[OK] Virtual environment exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Cannot find activation script" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Try to install from minimal requirements first (works with Python 3.13)
Write-Host "[INFO] Installing core dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements-minimal.txt") {
    pip install -r requirements-minimal.txt

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Core dependencies installed successfully" -ForegroundColor Green
        Write-Host "[INFO] System ready with core features" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Failed to install core dependencies" -ForegroundColor Red
        Write-Host "Try: pip install flask flask-cors ezdxf python-dotenv" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[WARNING] requirements-minimal.txt not found, trying full install..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet

    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        Write-Host "" -ForegroundColor Yellow
        Write-Host "SOLUTION: Python 3.13 is too new for some packages." -ForegroundColor Yellow
        Write-Host "Option 1: Install Python 3.11 or 3.12 (Recommended)" -ForegroundColor Cyan
        Write-Host "Option 2: Install Microsoft C++ Build Tools" -ForegroundColor Cyan
        Write-Host "          https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
}

Write-Host ""

# Create necessary directories
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}
if (-not (Test-Path "temp")) {
    New-Item -ItemType Directory -Path "temp" | Out-Null
}
Write-Host "[OK] Directories created" -ForegroundColor Green
Write-Host ""

# Copy .env.example to .env if doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] Environment file created" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "   STARTING BACKEND SERVER" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "[INFO] Backend API starting on http://localhost:5000" -ForegroundColor Cyan
Write-Host "[INFO] Health check: http://localhost:5000/api/health" -ForegroundColor Cyan
Write-Host "[INFO] Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Start the Flask application
python app.py
