# Smart PowerShell Script - Detects Best Python Version
# AI Floor Plan Generator

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   AI FLOOR PLAN GENERATOR - SMART SETUP" -ForegroundColor Cyan
Write-Host "   Detects Best Python Version Automatically" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check Python version
function Get-PythonCommand {
    $pythonCommands = @("python3.11", "python3.12", "py -3.11", "py -3.12", "python")

    foreach ($cmd in $pythonCommands) {
        try {
            $version = if ($cmd -like "py *") {
                & py -3.11 --version 2>&1
            } else {
                & $cmd --version 2>&1
            }

            if ($version -match "Python 3\.1[12]") {
                return @{
                    Command = $cmd
                    Version = $version
                    IsGood = $true
                }
            } elseif ($version -match "Python 3\.13") {
                return @{
                    Command = $cmd
                    Version = $version
                    IsGood = $false
                }
            }
        } catch {
            continue
        }
    }

    return $null
}

# Check for Python
$pythonInfo = Get-PythonCommand

if (-not $pythonInfo) {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11 from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/release/python-3118/" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Found: $($pythonInfo.Version)" -ForegroundColor Green

if (-not $pythonInfo.IsGood) {
    Write-Host ""
    Write-Host "[WARNING] Python 3.13 detected - some packages won't install!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "RECOMMENDATION: Install Python 3.11 for 100% features" -ForegroundColor Cyan
    Write-Host "Download: https://www.python.org/downloads/release/python-3118/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Current limitations with Python 3.13:" -ForegroundColor Yellow
    Write-Host "  - No PDF generation (ReportLab)" -ForegroundColor Red
    Write-Host "  - No image processing (Pillow)" -ForegroundColor Red
    Write-Host "  - No advanced math (NumPy/SciPy)" -ForegroundColor Red
    Write-Host "  - DXF export still works!" -ForegroundColor Green
    Write-Host "  - AI generation still works!" -ForegroundColor Green
    Write-Host ""

    $response = Read-Host "Continue with limited features? (y/n)"
    if ($response -ne "y") {
        Write-Host "Exiting. Please install Python 3.11 and run again." -ForegroundColor Yellow
        exit 0
    }

    $requirementsFile = "requirements-minimal.txt"
} else {
    Write-Host "[OK] Perfect Python version for all features!" -ForegroundColor Green
    $requirementsFile = "requirements.txt"
}

Write-Host ""

# Determine Python command to use
$pythonCmd = $pythonInfo.Command

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating Python virtual environment..." -ForegroundColor Yellow

    if ($pythonCmd -like "py *") {
        & py -3.11 -m venv venv
    } else {
        & $pythonCmd -m venv venv
    }

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

# Install dependencies
Write-Host "[INFO] Installing dependencies from $requirementsFile..." -ForegroundColor Yellow
pip install -r $requirementsFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] All dependencies installed successfully!" -ForegroundColor Green
    if ($requirementsFile -eq "requirements.txt") {
        Write-Host "[OK] 100% FEATURES AVAILABLE!" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Core features available (60%)" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTION: Install Python 3.11" -ForegroundColor Cyan
    Write-Host "https://www.python.org/downloads/release/python-3118/" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
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

# Copy .env
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
Write-Host "[INFO] Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "[INFO] Health check: http://localhost:5000/api/health" -ForegroundColor Cyan
Write-Host "[INFO] Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Start Flask
python app.py
