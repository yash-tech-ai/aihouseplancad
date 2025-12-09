# 🚀 Claude Code Integration Guide

## How to Use This Floor Plan Generator in Claude Code

### Option 1: Open Directly in Browser

1. **Navigate to the file:**
   ```bash
   cd /home/claude/cad-floor-plan-generator
   ```

2. **Open in browser:**
   - Simply open `floor-plan-generator.html` in any web browser
   - Or use a local server:
   ```bash
   python3 -m http.server 8000
   ```
   Then visit: http://localhost:8000/floor-plan-generator.html

### Option 2: Enhance with Backend Integration

If you want to add real CAD file processing, create a Python backend:

```python
# backend.py - Example CAD processing server
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/analyze-cad', methods=['POST'])
def analyze_cad():
    file = request.files['cadFile']
    # Process CAD file here using libraries like:
    # - ezdxf (for DXF files)
    # - ODA File Converter (for DWG files)
    # - PyMuPDF (for PDF files)
    
    return jsonify({
        'walls': 12,
        'doors': 8,
        'windows': 10,
        'rooms': 6,
        'confidence': 95
    })

@app.route('/api/export-dwg', methods=['POST'])
def export_dwg():
    floor_plan_data = request.json
    # Generate DWG file using ezdxf or similar
    return jsonify({'status': 'success', 'file': 'output.dwg'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Option 3: Add Python CAD Libraries

Install CAD processing capabilities:

```bash
# Install DXF processing
pip install ezdxf --break-system-packages

# Install PDF processing
pip install PyMuPDF --break-system-packages

# Install image processing
pip install Pillow opencv-python --break-system-packages
```

### Option 4: Create NPM Package (Advanced)

For production use:

```bash
mkdir cad-floor-plan-npm
cd cad-floor-plan-npm
npm init -y

# Install dependencies
npm install express multer ezdxf-node sharp

# Create server.js
# (Server code for handling CAD files)

# Run
npm start
```

## 📁 Project Structure for Claude Code

```
cad-floor-plan-generator/
├── frontend/
│   └── floor-plan-generator.html
├── backend/ (optional)
│   ├── server.py
│   ├── cad_processor.py
│   └── requirements.txt
├── exports/ (generated files)
│   ├── PNG/
│   ├── PDF/
│   ├── DWG/
│   └── DXF/
└── uploads/ (user uploads)
    └── cad_files/
```

## 🔧 Enhancement Ideas

### 1. Real CAD File Processing

```python
# cad_processor.py
import ezdxf

def process_dxf(file_path):
    """Process DXF file and extract elements"""
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    
    walls = []
    doors = []
    windows = []
    
    for entity in msp:
        if entity.dxftype() == 'LINE':
            walls.append({
                'start': entity.dxf.start,
                'end': entity.dxf.end
            })
        elif entity.dxftype() == 'INSERT':
            # Door or window block
            pass
    
    return {
        'walls': walls,
        'doors': doors,
        'windows': windows
    }
```

### 2. AI Model Integration

```python
# ai_analyzer.py
import cv2
import numpy as np

def analyze_floor_plan_image(image_path):
    """Use computer vision to detect floor plan elements"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours (rooms)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return {
        'rooms': len(contours),
        'confidence': 0.85
    }
```

### 3. Database Integration

```python
# database.py
import sqlite3

def save_floor_plan(user_id, floor_plan_data):
    """Save floor plan to database"""
    conn = sqlite3.connect('floor_plans.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO floor_plans (user_id, data, created_at)
        VALUES (?, ?, datetime('now'))
    ''', (user_id, json.dumps(floor_plan_data)))
    
    conn.commit()
    conn.close()
```

## 🎯 Quick Commands for Claude Code

### Run the application:
```bash
cd /home/claude/cad-floor-plan-generator
python3 -m http.server 8000
```

### Process a CAD file:
```bash
python3 -c "
import ezdxf
doc = ezdxf.readfile('sample.dxf')
print(f'Layers: {len(doc.layers)}')
"
```

### Convert DWG to DXF (requires ODA File Converter):
```bash
ODAFileConverter input.dwg output.dxf ACAD2018 DXF 0 1
```

## 📦 Required Libraries (Optional)

For full CAD functionality:

```bash
# Python CAD libraries
pip install ezdxf PyMuPDF Pillow opencv-python --break-system-packages

# Image processing
pip install scikit-image matplotlib --break-system-packages

# Web framework (if using backend)
pip install flask flask-cors --break-system-packages
```

## 🔗 Connecting to CAD Software

### AutoCAD Script:
```lisp
; autocad_import.scr
(command "OPEN" "floor-plan.dwg")
(command "ZOOM" "E")
(command "LAYER" "ON" "*")
```

### LibreCAD Integration:
```bash
# Open file in LibreCAD
librecad floor-plan.dxf
```

## 💡 Tips for Claude Code

1. **Use relative paths** - Files should reference ./uploads, ./exports
2. **Add error handling** - Wrap file operations in try-catch
3. **Validate inputs** - Check file types and sizes before processing
4. **Provide feedback** - Show loading states during CAD analysis
5. **Cache results** - Store processed CAD data to avoid re-analysis

## 🎨 Customization

### Add new export format:
```javascript
function exportCustomFormat() {
    const canvas = document.getElementById('floorPlanCanvas');
    const data = extractFloorPlanData();
    
    // Convert to your custom format
    const customFormat = convertToCustomFormat(data);
    
    // Download
    downloadFile(customFormat, 'floor-plan.custom');
}
```

### Add new room type:
```javascript
const roomTypes = {
    'library': { color: '#d4a5a5', defaultSize: 150 },
    'gym': { color: '#a5d4a5', defaultSize: 200 },
    'theater': { color: '#a5a5d4', defaultSize: 300 }
};
```

## 🚀 Ready to Build!

You now have:
✅ Complete merged floor plan generator
✅ All features from remixes combined
✅ CAD integration capabilities
✅ Export to multiple formats
✅ AI analysis framework
✅ 3D visualization

**Next Steps:**
1. Open the HTML file in browser
2. Test all features
3. Add backend if needed
4. Deploy or distribute

Happy building! 🏗️
