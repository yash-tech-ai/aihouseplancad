# PowerShell Script for Testing
# AI Floor Plan Generator

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║            🧪 SYSTEM TEST SUITE 🧪                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Set-Location backend

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

Write-Host "[INFO] Running comprehensive tests..." -ForegroundColor Yellow
Write-Host ""

# Run tests
python test_system.py

Write-Host ""
Write-Host "[INFO] Test complete! Review results above." -ForegroundColor Cyan
Read-Host "Press Enter to exit"
