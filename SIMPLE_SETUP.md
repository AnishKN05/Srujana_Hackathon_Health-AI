# 🚀 Simple Health AI Platform - Setup Guide

## What You're Getting
- **Frontend**: HTML/CSS/JavaScript (no React, no Node.js needed)
- **Backend**: Python Flask (simple and lightweight)
- **Database**: MySQL (stores user data and chat history)
- **Features**: Symptom analysis, chat assistant, rule-based AI

## 📋 Prerequisites

### 1. Python 3.7+
```bash
python --version
```

### 2. MySQL Server
- Download from: https://dev.mysql.com/downloads/mysql/
- Or use XAMPP: https://www.apachefriends.org/
- Default settings:
  - Host: localhost
  - Port: 3306
  - Username: root
  - Password: (set your own)

### 3. Git (optional)
```bash
git --version
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install MySQL
1. Download and install MySQL
2. Set root password (remember this!)
3. Start MySQL service

### Step 2: Configure Database
Edit `simple_backend/app.py` and update the database password:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',  # Change this!
    'database': 'health_ai_db',
    'port': 3306
}
```

### Step 3: Start the Platform
**Option A: Python Script**
```bash
python start_simple_platform.py
```

**Option B: Windows Batch File**
```bash
start_simple.bat
```

**Option C: Manual**
```bash
cd simple_backend
pip install -r requirements.txt
python app.py
```

## 🌐 Access Your Application

Once started, open your browser and go to:
- **Main Application**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 🎯 Features

### 1. Symptom Analysis
- Add multiple symptoms
- Select duration and severity
- Get possible conditions with probabilities
- Receive first aid advice
- Emergency warning signs

### 2. Chat Assistant
- Conversational health assistant
- Ask follow-up questions
- Get personalized responses
- Suggested questions

### 3. Data Storage
- All interactions saved to MySQL
- Chat history preserved
- Symptom analysis logged

## 🔧 Troubleshooting

### "Module not found" Error
```bash
cd simple_backend
pip install -r requirements.txt
```

### "Can't connect to MySQL" Error
1. Make sure MySQL is running
2. Check password in `app.py`
3. Verify MySQL is on port 3306

### "Port 5000 already in use" Error
- Change port in `app.py`: `app.run(port=5001)`
- Or stop other applications using port 5000

### Database Connection Issues
1. Check MySQL service is running
2. Verify username/password
3. Make sure MySQL allows connections from localhost

## 📁 File Structure
```
simple_backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
└── templates/
    └── index.html        # Frontend HTML/CSS/JS

start_simple_platform.py  # Startup script
start_simple.bat          # Windows batch file
SIMPLE_SETUP.md          # This guide
```

## 🎨 Customization

### Change Port
Edit `simple_backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Add More Conditions
Edit the `analyze_symptoms()` function in `app.py` to add more medical conditions.

### Modify Frontend
Edit `simple_backend/templates/index.html` to change the appearance.

## 🚨 Important Notes

1. **Educational Use Only**: This is not a replacement for medical professionals
2. **No Real AI**: Uses rule-based analysis, not machine learning
3. **Local Only**: Runs on your computer, no external APIs
4. **Data Privacy**: All data stays on your local MySQL database

## 🆘 Need Help?

1. **Check MySQL**: Make sure it's running and accessible
2. **Check Python**: Make sure Python 3.7+ is installed
3. **Check Dependencies**: Run `pip install -r requirements.txt`
4. **Check Ports**: Make sure port 5000 is free

## 🎉 Success!

If everything works, you should see:
```
🚀 Starting Health AI Platform Backend...
📍 Backend will be available at: http://localhost:5000
✅ Database initialized successfully
 * Running on http://0.0.0.0:5000
```

Then open http://localhost:5000 in your browser!
