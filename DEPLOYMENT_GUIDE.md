# 🚀 Production Deployment Guide
## AI Floor Plan CAD Generator - World-Class System

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start (5 Minutes)](#quick-start)
4. [Production Deployment](#production-deployment)
5. [Architecture](#architecture)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## System Overview

### What You Have Now

A **world-class, production-grade** floor plan generation system featuring:

✅ **Real AI Intelligence**
- Architectural knowledge base with adjacency preferences
- Building code compliance (International Residential Code)
- Energy efficiency optimization
- Space allocation algorithms

✅ **Professional CAD Integration**
- Real DXF export (opens in AutoCAD, LibreCAD, DraftSight)
- Real SVG export (vector graphics)
- Real DXF import with element detection
- Professional title blocks and dimensions

✅ **Building Code Validation**
- Automatic code compliance checking
- Detailed violation reports
- Compliance scoring and grading
- Egress requirements validation

✅ **Production-Grade Backend**
- RESTful API with comprehensive error handling
- Request validation and sanitization
- File upload security
- CORS configuration
- Environment-based configuration

✅ **Professional Architecture**
- Modular, maintainable code structure
- Comprehensive testing suite
- Production and development modes
- Scalable design

---

## Prerequisites

### Required Software

```bash
# Python 3.8 or higher
python3 --version

# pip (Python package manager)
pip3 --version

# Git (for version control)
git --version
```

### Optional (for advanced features)

- **ODA File Converter** - for DWG format support
- **Docker** - for containerized deployment
- **Nginx** - for reverse proxy in production

---

## Quick Start (5 Minutes)

### Step 1: Set Up Backend

```bash
# Navigate to project directory
cd /home/user/aihouseplancad

# Navigate to backend
cd backend

# Run the startup script
chmod +x run.sh
./run.sh
```

The script will:
- Create virtual environment
- Install all dependencies
- Create necessary directories
- Start the Flask server on `http://localhost:5000`

### Step 2: Start Frontend

Open a new terminal:

```bash
# Navigate to project root
cd /home/user/aihouseplancad

# Start simple HTTP server
python3 -m http.server 8000
```

Frontend will be available at: `http://localhost:8000/floor-plan-generator.html`

### Step 3: Test the System

Open a third terminal:

```bash
cd /home/user/aihouseplancad/backend
source venv/bin/activate
python test_system.py
```

You should see all tests passing! ✅

---

## Production Deployment

### Option 1: Traditional Server (Recommended)

#### 1. Set Up Production Environment

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and essentials
sudo apt-get install python3 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/aihouseplancad.git
cd aihouseplancad/backend
```

#### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit production settings
nano .env
```

Set these values:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-random-key-here-change-this
ALLOWED_ORIGINS=https://yourdomain.com
```

#### 3. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Set Up Systemd Service

Create `/etc/systemd/system/floorplan-api.service`:

```ini
[Unit]
Description=AI Floor Plan Generator API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/aihouseplancad/backend
Environment="PATH=/var/www/aihouseplancad/backend/venv/bin"
ExecStart=/var/www/aihouseplancad/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start floorplan-api
sudo systemctl enable floorplan-api
sudo systemctl status floorplan-api
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/floorplan`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/aihouseplancad;
        index floor-plan-generator.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Content-Type';
    }

    # File upload size
    client_max_body_size 50M;
}
```

Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/floorplan /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL with Let's Encrypt (Recommended)

```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile

`backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p uploads temp

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/temp:/app/temp
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./floor-plan-generator.html:/usr/share/nginx/html/index.html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
    restart: unless-stopped
```

#### 3. Deploy

```bash
docker-compose up -d
docker-compose logs -f
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                    │
│  (floor-plan-generator.html + JavaScript)           │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/HTTPS
                   │
┌──────────────────▼──────────────────────────────────┐
│                 NGINX (Reverse Proxy)                │
│  - Static file serving                               │
│  - SSL termination                                   │
│  - Request routing                                   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│            FLASK API (Python Backend)                │
│  ┌─────────────────────────────────────────────┐    │
│  │  API Layer (app/api/routes.py)             │    │
│  │  - Request validation                       │    │
│  │  - Error handling                           │    │
│  │  - Response formatting                      │    │
│  └─────────────────┬───────────────────────────┘    │
│                    │                                 │
│  ┌─────────────────▼───────────────────────────┐    │
│  │  Core Services                              │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │  AI Architect (ai_architect.py)      │  │    │
│  │  │  - Space allocation                  │  │    │
│  │  │  - Room placement                    │  │    │
│  │  │  - Optimization                      │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │  CAD Engine (cad_engine.py)          │  │    │
│  │  │  - DXF import/export                 │  │    │
│  │  │  - SVG generation                    │  │    │
│  │  │  - File parsing                      │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │  Code Validator (code_validator.py)  │  │    │
│  │  │  - Building code checks              │  │    │
│  │  │  - Compliance scoring                │  │    │
│  │  │  - Report generation                 │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### File Structure

```
aihouseplancad/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── ai_architect.py    # AI layout generation
│   │   │   ├── cad_engine.py      # CAD import/export
│   │   │   └── code_validator.py  # Building code validation
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── room.py            # Data models
│   │   └── utils/
│   │       └── __init__.py
│   ├── app.py                     # Flask application
│   ├── config.py                  # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   ├── run.sh                     # Startup script
│   └── test_system.py             # Test suite
├── floor-plan-generator.html      # Frontend
├── README.md
├── DEPLOYMENT_GUIDE.md           # This file
└── PROFESSIONAL_UPGRADE_PLAN.md
```

---

## Testing

### Manual Testing

1. **Test Backend Health**
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Floor Plan Generator",
  "version": "1.0.0"
}
```

2. **Test Floor Plan Generation**
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "totalSqFt": 2000,
    "bedrooms": 3,
    "bathrooms": 2,
    "style": "modern"
  }'
```

3. **Test DXF Export**
```bash
curl -X POST http://localhost:5000/api/export/dxf \
  -H "Content-Type: application/json" \
  -d @floor_plan.json \
  -o output.dxf
```

### Automated Testing

```bash
cd backend
source venv/bin/activate
python test_system.py
```

### Load Testing (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API performance
ab -n 1000 -c 10 http://localhost:5000/api/health
```

---

## Troubleshooting

### Backend won't start

**Problem**: Port 5000 already in use

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port in .env
PORT=5001
```

---

### CORS errors in browser

**Problem**: Cross-origin requests blocked

**Solution**: Update `ALLOWED_ORIGINS` in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,https://yourdomain.com
```

---

### DXF export fails

**Problem**: "DXF export failed" error

**Solution**: Check logs:
```bash
tail -f backend/logs/app.log
```

Common causes:
- Invalid room data
- Missing required fields
- File permissions

---

### High memory usage

**Problem**: Backend using too much memory

**Solution**: Reduce gunicorn workers in production:
```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

## Performance Optimization

### Backend

1. **Enable Caching** (for static responses)
2. **Use Redis** (for session management)
3. **Optimize Room Placement Algorithm** (reduce iterations)
4. **Enable Gzip Compression** (in Nginx)

### Frontend

1. **Minify JavaScript** and CSS
2. **Enable Browser Caching**
3. **Use CDN** for static assets
4. **Lazy Load** images and components

---

## Security Best Practices

### Production Checklist

- [ ] Change `SECRET_KEY` to random value
- [ ] Set `FLASK_DEBUG=False`
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set restrictive `ALLOWED_ORIGINS`
- [ ] Implement rate limiting
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Implement authentication (if needed)
- [ ] Regular backups

---

## Monitoring

### Health Checks

Set up monitoring with cron:

```bash
# Check every 5 minutes
*/5 * * * * curl -f http://localhost:5000/api/health || systemctl restart floorplan-api
```

### Log Management

```bash
# View logs
sudo journalctl -u floorplan-api -f

# Rotate logs
sudo logrotate /etc/logrotate.d/floorplan-api
```

---

## Scaling

### Horizontal Scaling

1. **Load Balancer** (Nginx, HAProxy)
2. **Multiple Backend Instances**
3. **Shared Storage** (for uploads)
4. **Database** (for persistence if needed)

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize Python code
3. Use faster algorithms
4. Implement caching

---

## Support

For issues or questions:

1. Check this guide
2. Review logs
3. Run test suite
4. Check GitHub issues
5. Contact support

---

## License

Professional Commercial License - All Rights Reserved

---

**Deployed successfully? Congratulations! 🎉**

You now have a world-class, production-grade floor plan generation system!
