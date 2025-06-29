# PetroCalc Web Deployment Guide

This guide covers deployment scenarios for the PetroCalc Web application. **This application requires petrocalc to be installed via pip.**

## 📦 Prerequisites

The petrocalc package must be installed via pip before running this web application:

```bash
pip install petrocalc
```

**Note**: This application does not support local development installations. You must install petrocalc from PyPI.

## 🚀 Installation and Setup

### Quick Start

```bash
# Clone and setup web app
git clone https://github.com/Farzad0514/petrocalc-web.git
cd petrocalc-web

# Install all dependencies (including petrocalc)
pip install -r requirements.txt

# Run the application
python run.py
```

### Using requirements.txt (Recommended)

```bash
# Install petrocalc (required)
pip install petrocalc

# Clone and setup web app
git clone https://github.com/Farzad0514/petrocalc-web.git
cd petrocalc-web

# Install web app dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Manual installation

## 🐳 Docker Deployment

### Option 1: Using the provided Dockerfile

```bash
# Build and run
docker build -t petrocalc-web .
docker run -p 8000:8000 petrocalc-web
```

### Option 2: Using docker-compose

```bash
docker-compose up
```

### Option 3: Custom Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install petrocalc from PyPI
RUN pip install petrocalc

# Copy web app
COPY . .
RUN pip install fastapi uvicorn[standard] jinja2 python-multipart aiofiles

EXPOSE 8000
CMD ["python", "run.py"]
```

## 🔧 Configuration

The application requires petrocalc to be available as a pip-installed package. If petrocalc is not found, the application will:

1. Display an error message
2. Exit with instructions to install petrocalc via pip
3. Not start any web services

## 📊 Status Monitoring

Check the application status:

```bash
curl http://localhost:8000/api/status
```

Response example:
```json
{
  "app_status": "running",
  "petrocalc_available": true,
  "config": {
    "petrocalc_location": "pip_installed",
    "petrocalc_version": "0.1.1",
    "is_development": false
  }
}
```

## 🚀 Production Deployment

### 1. Standalone Server

```bash
# Basic production server
python run.py

# With specific host/port using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Cloud Deployment (Heroku, AWS, etc.)

Create a `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Ensure your `requirements.txt` includes:
```
petrocalc
fastapi
uvicorn[standard]
jinja2
python-multipart
aiofiles
```

### 3. Container Orchestration

For Kubernetes, Docker Swarm, or similar:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: petrocalc-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: petrocalc-web
  template:
    metadata:
      labels:
        app: petrocalc-web
    spec:
      containers:
      - name: petrocalc-web
        image: petrocalc-web:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
```

## 🔍 Troubleshooting

### Issue: PetroCalc not found

**Error message**:
```
❌ Error: petrocalc package not found!
Please install petrocalc using: pip install petrocalc
```

**Solution**:
```bash
pip install petrocalc
```

### Issue: Import errors after installation

**Check installation**:
```python
python -c "import petrocalc; print(f'✅ petrocalc {petrocalc.__version__} found at {petrocalc.__file__}')"
```

**Verify pip installation**:
```bash
pip list | grep petrocalc
```

### Issue: Application won't start

1. Verify petrocalc is installed: `pip list | grep petrocalc`
2. Check Python version: `python --version` (requires 3.10+)
3. Verify all dependencies: `pip install -r requirements.txt`

## 📋 Environment Variables

- `ENVIRONMENT`: Set to "production" for production mode
- `PORT`: Override default port (8000)
- `HOST`: Override default host (127.0.0.1)

## 🧪 Testing the Deployment

### Test installation

```bash
# Test petrocalc availability
python -c "import petrocalc; print('✅ petrocalc available')"

# Test web app startup
python run.py &
sleep 5
curl http://localhost:8000/api/status
```

### Test API endpoints

```bash
# Test drilling calculations
curl -X POST "http://localhost:8000/api/drilling/mud_weight_to_pressure_gradient" \
  -H "Content-Type: application/json" \
  -d '{"mud_weight": 12.5}'

# Test status endpoint
curl http://localhost:8000/api/status
```

## 🏗️ CI/CD Pipeline Example

```yaml
# .github/workflows/deploy.yml
name: Deploy PetroCalc Web

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install petrocalc
      run: pip install petrocalc
        
    - name: Install web app dependencies
      run: pip install -r requirements.txt
        
    - name: Test application
      run: |
        python -c "from app.config import get_config; print(get_config().get_status_info())"
        python run.py &
        sleep 10
        curl http://localhost:8000/api/status
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Your deployment commands here
        echo "Deploying to production..."
```

This deployment approach ensures consistent behavior across all environments by requiring pip-installed petrocalc.
