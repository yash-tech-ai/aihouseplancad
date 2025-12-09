# PowerShell Script for Frontend
# AI Floor Plan Generator

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           🌐 STARTING FRONTEND SERVER 🌐               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[✓] Starting frontend on http://localhost:8000" -ForegroundColor Green
Write-Host "[✓] Open your browser to:" -ForegroundColor Green
Write-Host ""
Write-Host "    http://localhost:8000/floor-plan-generator.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "[INFO] Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Start Python HTTP server
python -m http.server 8000
