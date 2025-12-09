# 🚀 QUICK FIX - PowerShell in VS Code

## The Issue

PowerShell requires `.\` prefix to run scripts in the current directory for security.

---

## ✅ SOLUTION - Use These Commands:

### Start Backend

```powershell
cd backend
.\start-backend.ps1
```

### Start Frontend (New Terminal)

```powershell
.\start-frontend.ps1
```

### Run Tests

```powershell
.\run-tests.ps1
```

---

## 🔧 Alternative: Use .bat Files with .\

If you prefer .bat files:

```powershell
cd backend
.\start-backend.bat
```

```powershell
.\start-frontend.bat
```

---

## ⚡ Even Better: Enable Script Execution

If you see "script execution is disabled" error:

### One-Time Setup (Run as Administrator)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then you can run:
```powershell
.\start-backend.ps1
```

---

## 📋 Complete Steps for PowerShell

### Terminal 1 (Backend):
```powershell
cd backend
.\start-backend.ps1
```

**Wait for:** `Backend API starting on http://localhost:5000`

### Terminal 2 (Frontend):
```powershell
.\start-frontend.ps1
```

### Browser:
```
http://localhost:8000/floor-plan-generator.html
```

---

## 🎯 What I Created for You

✅ `backend/start-backend.ps1` - PowerShell script (colored output!)
✅ `start-frontend.ps1` - PowerShell script
✅ `run-tests.ps1` - PowerShell script

All scripts have:
- ✅ Colored output (Green ✓, Red ✗, Yellow info)
- ✅ Better error messages
- ✅ Auto-setup
- ✅ Works perfectly in PowerShell

---

## 💡 Pro Tip: VS Code Terminal Default

Make PowerShell your default in VS Code:

1. Press `Ctrl+Shift+P`
2. Type: "Terminal: Select Default Profile"
3. Choose: "PowerShell"

---

## 🆘 Still Having Issues?

### If script won't run:

**Check execution policy:**
```powershell
Get-ExecutionPolicy
```

**If it says "Restricted", run:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Then retry:**
```powershell
.\start-backend.ps1
```

---

## ✨ You're Ready!

```powershell
# Terminal 1
cd backend
.\start-backend.ps1

# Terminal 2 (click + button)
.\start-frontend.ps1

# Browser
http://localhost:8000/floor-plan-generator.html
```

**That's it!** 🎉
