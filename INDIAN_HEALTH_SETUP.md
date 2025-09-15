# 🇮🇳 Indian Health AI Platform - Complete Setup Guide

## 🎯 What You're Getting
- **Frontend**: HTML/CSS/JavaScript with Indian healthcare focus
- **Backend**: Python Flask with Indian medical conditions
- **Database**: MySQL for user data and chat history
- **Features**: 
  - User authentication with consent form
  - Indian healthcare-specific symptom analysis
  - First Aid guide with YouTube videos
  - Emergency contacts for India
  - Chat assistant with Indian context

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
python start_indian_health_platform.py
```

**Option B: Manual**
```bash
cd simple_backend
pip install -r requirements.txt
python app.py
```

## 🌐 Access Your Application

Once started, open your browser and go to:
- **Main Application**: http://localhost:5000
- **First Aid Guide**: http://localhost:5000/firstaid.html
- **API Health Check**: http://localhost:5000/api/health

## 🎯 Features

### 1. User Authentication & Consent
- Full name, age, gender, and state selection
- Comprehensive consent form with Indian healthcare context
- User data stored securely in MySQL
- Session management

### 2. Indian Healthcare Symptom Analysis
- **Dengue Fever**: Common in India, with specific symptoms
- **Malaria**: Prevalent in many Indian states
- **Typhoid**: Common due to contaminated food/water
- **Heat Stroke**: Common during Indian summers
- **Common Cold**: With monsoon season context
- **Food Poisoning**: Common in India

### 3. First Aid Guide
- **CPR**: Cardiopulmonary Resuscitation
- **Choking**: Heimlich Maneuver
- **Bleeding**: Severe bleeding control
- **Burns**: Burn treatment
- **Fractures**: Fracture and sprain care
- **Heat Stroke**: Heat-related illness treatment
- **YouTube Videos**: Embedded training videos
- **Indian Emergency Contacts**: All emergency numbers

### 4. Chat Assistant
- Indian healthcare-focused responses
- Context-aware suggestions
- Emergency guidance
- Follow-up questions

### 5. Emergency Contacts - India
- **Emergency Services**: 108
- **Police**: 100
- **Fire Service**: 101
- **Ambulance**: 102
- **Women Helpline**: 1091
- **Child Helpline**: 1098
- **Mental Health**: 1800-599-0019
- **Poison Control**: 1800-116-117

## 🔧 Troubleshooting

### "Module not found" Error
```bash
cd simple_backend
pip install -r requirements.txt
```

### "Can't connect to MySQL" Error
1. Make sure MySQL is running
2. Check password in `simple_backend/app.py`
3. Verify MySQL is on port 3306

### "Port 5000 already in use" Error
- Change port in `simple_backend/app.py`: `app.run(port=5001)`
- Or stop other applications using port 5000

### Database Connection Issues
1. Check MySQL service is running
2. Verify username/password
3. Make sure MySQL allows connections from localhost

## 📁 File Structure
```
simple_backend/
├── app.py                 # Main Flask application with Indian healthcare
├── requirements.txt       # Python dependencies
└── templates/
    ├── index.html        # Main frontend with authentication
    └── firstaid.html     # First aid guide with videos

start_indian_health_platform.py  # Startup script
INDIAN_HEALTH_SETUP.md          # This guide
```

## 🎨 Customization

### Change Port
Edit `simple_backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Add More Indian Conditions
Edit the `analyze_symptoms()` function in `app.py` to add more Indian medical conditions.

### Modify First Aid Content
Edit `simple_backend/templates/firstaid.html` to add more procedures or videos.

### Update Emergency Contacts
Edit the emergency contacts section in both HTML files.

## 🚨 Important Notes

1. **Educational Use Only**: This is not a replacement for medical professionals
2. **Indian Context**: Specifically designed for Indian healthcare scenarios
3. **Emergency Numbers**: Uses Indian emergency numbers (108, 100, 101, etc.)
4. **Local Only**: Runs on your computer, no external APIs
5. **Data Privacy**: All data stays on your local MySQL database

## 🇮🇳 Indian Healthcare Context

### Common Conditions in India
- **Dengue**: Endemic in many parts of India
- **Malaria**: Prevalent in many Indian states
- **Typhoid**: Common due to contaminated food/water
- **Heat Stroke**: Common during Indian summers (April-June)
- **Food Poisoning**: Common due to unhygienic food

### Seasonal Considerations
- **Summer (April-June)**: Heat-related illnesses
- **Monsoon (July-September)**: Water-borne diseases
- **Winter (December-February)**: Respiratory infections

### Healthcare Access
- **Government Hospitals**: Free treatment available
- **Emergency Services**: 108 for medical emergencies
- **Local Clinics**: Available in most areas
- **Telemedicine**: Growing availability

## 🆘 Need Help?

1. **Check MySQL**: Make sure it's running and accessible
2. **Check Python**: Make sure Python 3.7+ is installed
3. **Check Dependencies**: Run `pip install -r requirements.txt`
4. **Check Ports**: Make sure port 5000 is free
5. **Check Logs**: Look at the console output for error messages

## 🎉 Success!

If everything works, you should see:
```
🚀 Starting Indian Health AI Platform...
📍 Backend will be available at: http://localhost:5000
✅ Database initialized successfully
 * Running on http://0.0.0.0:5000
```

Then open http://localhost:5000 in your browser!

## 📞 Emergency Contacts Reminder

**In case of medical emergency in India:**
- **Emergency Services**: 108
- **Police**: 100
- **Fire Service**: 101
- **Ambulance**: 102
- **Women Helpline**: 1091
- **Child Helpline**: 1098

**Remember**: This platform is for educational purposes only. Always consult qualified healthcare professionals for proper medical advice.
