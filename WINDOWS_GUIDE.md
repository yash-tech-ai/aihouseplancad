# 🪟 Windows Quick Start Guide
## AI Floor Plan Generator on Windows with VS Code

---

## Prerequisites Check

Before starting, make sure you have:

### 1. Python 3.8 or Higher

**Check if installed:**
```cmd
python --version
```

**If not installed:**
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart VS Code after installation

### 2. VS Code

**Download from:** https://code.visualstudio.com/

**Recommended Extensions:**
- Python (by Microsoft)
- Pylance (by Microsoft)
- REST Client (for testing API)

---

## Step-by-Step Setup

### Step 1: Open Project in VS Code

1. Open VS Code
2. File → Open Folder
3. Navigate to: `/home/user/aihouseplancad`
4. Click "Select Folder"

### Step 2: Open Integrated Terminal

In VS Code:
- Press `` Ctrl + ` `` (backtick) to open terminal
- OR: View → Terminal

### Step 3: Start Backend

**In VS Code Terminal:**

```cmd
cd backend
start-backend.bat
```

**What you'll see:**
```
╔════════════════════════════════════════════════════════╗
║   🏗️  AI FLOOR PLAN GENERATOR - WINDOWS SETUP  🏗️      ║
╚════════════════════════════════════════════════════════╝

[✓] Python found
[INFO] Creating Python virtual environment...
[✓] Virtual environment created
[INFO] Installing dependencies...
[✓] Dependencies installed
[✓] Directories created

🚀 STARTING BACKEND 🚀

Backend API starting on http://localhost:5000
```

**Leave this terminal running!**

### Step 4: Start Frontend (New Terminal)

**Open a second terminal in VS Code:**
1. Click the `+` icon in terminal panel
2. OR: Terminal → New Terminal

**Run:**
```cmd
start-frontend.bat
```

**You'll see:**
```
╔════════════════════════════════════════════════════════╗
║           🌐 STARTING FRONTEND SERVER 🌐               ║
╚════════════════════════════════════════════════════════╝

[✓] Starting frontend on http://localhost:8000
[✓] Open your browser to:

    http://localhost:8000/floor-plan-generator.html
```

### Step 5: Open in Browser

Open your browser (Chrome, Edge, Firefox) and go to:

```
http://localhost:8000/floor-plan-generator.html
```

**You're now running! 🎉**

---

## VS Code Workspace Setup

### Recommended Folder Structure

In VS Code Explorer, you'll see:

```
aihouseplancad/
├── backend/
│   ├── app/              # Backend code
│   ├── venv/             # Python virtual environment (auto-created)
│   ├── app.py            # Main Flask app
│   ├── start-backend.bat # Windows startup script
│   └── test_system.py    # Test suite
├── floor-plan-generator.html  # Frontend
├── start-frontend.bat    # Frontend startup
└── WINDOWS_GUIDE.md      # This file
```

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

---

## Testing the System

### Run Automated Tests

**In VS Code Terminal:**

```cmd
run-tests.bat
```

**Expected output:**
```
🧪 SYSTEM TEST SUITE 🧪

[INFO] Running comprehensive tests...

Testing: Health Check
✓ Health check passed
   Version: 1.0.0
   Features: 4 available

Testing: AI Floor Plan Generation
ℹ Generating floor plan...
✓ Generated floor plan with 8 rooms
   Total area: 2000 sq ft
   Efficiency: 85.5%
   Compliance: A (95/100)

Testing: Building Code Validation
✓ Validation completed
   Grade: A
   Critical violations: 0
   Warnings: 0

Testing: DXF Export
✓ DXF file generated (45,231 bytes)
   Saved to: test_output.dxf

Testing: SVG Export
✓ SVG generated (12,445 characters)
   Saved to: test_output.svg

Testing: Comprehensive Analysis
✓ Analysis completed
   Energy Grade: B (82.3/100)
   Recommendations: 3

════════════════════════════════════════════════════════
TEST SUMMARY
════════════════════════════════════════════════════════

  Health: PASSED
  Generation: PASSED
  Validation: PASSED
  Dxf Export: PASSED
  Svg Export: PASSED
  Analysis: PASSED

Results: 6/6 tests passed

✓ ALL TESTS PASSED! System is working correctly.
```

---

## Using the System

### 1. Generate Your First Floor Plan

1. Open http://localhost:8000/floor-plan-generator.html
2. Fill in parameters:
   - Square Footage: `2000`
   - Bedrooms: `3`
   - Bathrooms: `2`
   - Style: `modern`
3. Click **"Generate Floor Plan"**

### 2. View Building Code Compliance

After generation, you'll automatically see:
- Compliance Grade (A+ to F)
- Any code violations
- Recommendations

### 3. Export to CAD

1. Go to "Export & CAD" tab
2. Click **"Export DXF"**
3. File downloads as `floor-plan.dxf`
4. Open in:
   - **AutoCAD** (if you have it)
   - **LibreCAD** (free: https://librecad.org/)
   - **DraftSight** (free version available)

---

## Windows-Specific Tips

### PowerShell Alternative

If you prefer PowerShell over Command Prompt:

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Frontend:**
```powershell
python -m http.server 8000
```

### Firewall Warning

Windows may show a firewall dialog when starting servers:
- Click **"Allow access"** for both Private and Public networks
- This allows your browser to connect to the local servers

### Port Already in Use

If you see "Address already in use":

**For Backend (port 5000):**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**For Frontend (port 8000):**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

---

## VS Code Debugging

### Debug Backend

1. Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

2. Press `F5` to start debugging
3. Set breakpoints by clicking left of line numbers

### View Logs in VS Code

**Terminal output shows logs in real-time!**

To save logs to file:
```cmd
cd backend
start-backend.bat > logs.txt 2>&1
```

---

## Common Issues & Solutions

### Issue 1: "Python not found"

**Solution:**
1. Install Python from python.org
2. During installation, check "Add Python to PATH"
3. Restart VS Code
4. Verify: `python --version`

### Issue 2: "pip install fails"

**Solution:**
```cmd
python -m pip install --upgrade pip
cd backend
pip install -r requirements.txt --verbose
```

### Issue 3: "Virtual environment activation fails"

**Solution:**
```cmd
cd backend
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
```

### Issue 4: "Import errors in Python"

**Solution:**
Make sure VS Code is using the correct Python interpreter:
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose: `.\backend\venv\Scripts\python.exe`

### Issue 5: "CORS errors in browser"

**Solution:**
1. Make sure backend is running (check Terminal 1)
2. Verify URL: http://localhost:5000/api/health
3. Check `backend/.env` has:
   ```
   ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

---

## Development Workflow

### Recommended VS Code Layout

1. **Left Sidebar:** File Explorer
2. **Main Area:** Code editor
3. **Bottom Panel:**
   - Terminal 1: Backend (running)
   - Terminal 2: Frontend (running)
   - Terminal 3: For commands/tests

### Making Changes

**To modify backend code:**
1. Edit files in `backend/app/`
2. Stop backend (Ctrl+C in Terminal 1)
3. Restart: `start-backend.bat`

**To modify frontend:**
1. Edit `floor-plan-generator.html`
2. Refresh browser (F5)
3. No need to restart frontend server

### Running Tests While Developing

Open new terminal:
```cmd
run-tests.bat
```

---

## Stopping the System

### Option 1: Clean Stop

In each terminal with running server:
1. Press `Ctrl+C`
2. Wait for "Shutting down..."
3. Close terminal

### Option 2: Close VS Code

Simply close VS Code - processes will terminate automatically.

### Option 3: Kill All Python

If servers won't stop:
```cmd
taskkill /F /IM python.exe
```

---

## Next Steps

### Today
1. ✅ Get system running (you're doing this now!)
2. ✅ Generate your first floor plan
3. ✅ Export a DXF file
4. ✅ Open in CAD software

### This Week
1. Read `START_HERE_NEW_USER.md`
2. Explore all features
3. Try different architectural styles
4. Run the test suite

### Going Forward
1. Customize AI algorithms
2. Add new features
3. Deploy to a server
4. Use professionally

---

## Getting Help

### In VS Code

1. **Hover over code:** See documentation
2. **Right-click:** Go to definition
3. **Ctrl+Space:** Auto-complete
4. **F12:** Jump to definition

### Documentation Files

- `WINDOWS_GUIDE.md` - This file
- `START_HERE_NEW_USER.md` - User guide
- `DEPLOYMENT_GUIDE.md` - Production deployment
- `SYSTEM_COMPLETE_SUMMARY.md` - Complete overview

### Check Logs

In backend terminal, you'll see all requests:
```
[INFO] Generating floor plan...
[INFO] Validating against building codes...
[SUCCESS] Floor plan generated (8 rooms, 2000 sqft)
```

---

## Quick Reference

### Start Everything
```cmd
Terminal 1: cd backend && start-backend.bat
Terminal 2: start-frontend.bat
Browser: http://localhost:8000/floor-plan-generator.html
```

### Run Tests
```cmd
run-tests.bat
```

### Check Backend Health
```cmd
curl http://localhost:5000/api/health
```

Or open in browser: http://localhost:5000/api/health

### Stop Everything
```cmd
Ctrl+C in each terminal
```

---

## You're Ready! 🚀

**Current Status:**
- ✅ Windows scripts created
- ✅ VS Code setup documented
- ✅ Troubleshooting guide included
- ✅ Development workflow explained

**To Start:**
```cmd
1. Open VS Code
2. Open terminal (Ctrl + `)
3. Run: cd backend && start-backend.bat
4. Open new terminal: start-frontend.bat
5. Open browser: http://localhost:8000/floor-plan-generator.html
```

**Welcome to professional floor plan generation!** 🏗️✨
