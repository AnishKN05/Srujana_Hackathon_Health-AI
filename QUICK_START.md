# 🚀 Quick Start Guide - ML Health AI Platform

## The Problem You're Facing
You're trying to run the startup scripts from the wrong directory. The scripts are in the **root directory**, but you're running them from the `backend` directory.

## ✅ Solution - Multiple Ways to Start the Platform

### Method 1: Use the Simple Scripts (Recommended)
From the **root directory** (where you see `package.json` and `requirements.txt`):

```bash
# Terminal 1: Start Backend
python run_backend.py

# Terminal 2: Start Frontend  
python run_frontend.py
```

### Method 2: Use Batch Files (Windows)
From the **root directory**:

```bash
# Terminal 1: Start Backend
start_backend.bat

# Terminal 2: Start Frontend
start_frontend.bat
```

### Method 3: Manual Commands
From the **root directory**:

```bash
# Terminal 1: Start Backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend
npm install  # Only needed first time
npm run dev
```

## 🔧 First-Time Setup

If you haven't set up the ML models yet:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node.js dependencies
npm install

# 3. Set up environment
copy env.example .env

# 4. Train ML models (this will take a few minutes)
python setup_ml_platform.py
```

## 🌐 Access the Application

Once both servers are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🐛 Troubleshooting

### "File not found" Error
- Make sure you're in the **root directory** (where `package.json` is located)
- Don't run scripts from the `backend` directory

### "Module not found" Error
- Run: `pip install -r requirements.txt`
- Run: `npm install`

### "Models not found" Error
- Run: `python setup_ml_platform.py` to train the ML models

### Port Already in Use
- Backend uses port 8000, Frontend uses port 3000
- Make sure no other applications are using these ports

## 📁 Directory Structure
```
health-ai-platform/
├── run_backend.py          ← Use this to start backend
├── run_frontend.py         ← Use this to start frontend
├── start_backend.bat       ← Windows batch file
├── start_frontend.bat      ← Windows batch file
├── backend/
│   └── main.py
├── src/
│   └── (React frontend)
├── ml_models/
│   └── (ML models)
└── package.json
```

## 🎯 What You Should See

**Backend Terminal:**
```
🚀 Starting ML-based Health AI Platform Backend...
📍 Backend will be available at: http://localhost:8000
🤖 Using trained ML models
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Frontend Terminal:**
```
🏥 Starting Health AI Platform Frontend...
📍 Frontend will be available at: http://localhost:3000
  VITE v4.5.0  ready in 500 ms
  ➜  Local:   http://localhost:3000/
```

## 🆘 Still Having Issues?

1. **Check your current directory**: Run `dir` (Windows) or `ls` (Mac/Linux) - you should see `package.json`
2. **Make sure Python is installed**: Run `python --version`
3. **Make sure Node.js is installed**: Run `node --version`
4. **Check if ports are free**: Make sure nothing is running on ports 3000 and 8000
