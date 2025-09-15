# 🚀 Quick Start Guide - Enhanced Health AI Platform

## ⚡ **Step-by-Step Setup (Windows)**

### **Step 1: Install Requirements**
```bash
pip install -r requirements.txt
```

### **Step 2: Train ML Models**
```bash
python train_models.py --all
```

### **Step 3: Test Models (Optional)**
```bash
python test_models_only.py
```

### **Step 4: Start the Platform**
```bash
# Option 1: Use the batch file
start_platform.bat

# Option 2: Use Python script
python start_platform.py
```

### **Step 5: Access the Platform**
- Open your browser
- Go to: http://localhost:5000
- Register with your details
- Choose from 4 services:
  - 🩺 General Health
  - 🥗 Nutrition
  - 🏃 Physiotherapy  
  - 🩸 Blood Bank

## 🔧 **Troubleshooting**

### **Problem: "No connection could be made"**
**Solution:** The server isn't running. Make sure you completed Step 4.

### **Problem: "Module not found" errors**
**Solution:** Run Step 1 again:
```bash
pip install -r requirements.txt
```

### **Problem: "Models not found" errors**
**Solution:** Run Step 2 again:
```bash
python train_models.py --all
```

### **Problem: MySQL connection errors**
**Solution:** 
1. Install MySQL 8.0+
2. Update credentials in `simple_backend/app.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_password',  # Change this
       'database': 'health_ai_db',
       'port': 3306
   }
   ```

## 📋 **What Each Service Does**

### 🩺 **General Health**
- Symptom analysis and diagnosis
- First aid guidance
- Emergency contacts
- Chat-based consultation

### 🥗 **Nutrition**
- Weight loss/gain advice
- Diabetes and heart health nutrition
- Muscle building diet plans
- Meal planning

### 🏃 **Physiotherapy**
- Back pain exercises
- Posture correction
- Strength training
- Injury rehabilitation

### 🩸 **Blood Bank**
- Check blood availability
- Find compatible donors
- Locate nearby hospitals
- Emergency blood requests

## 🧪 **Testing**

### **Test ML Models Only:**
```bash
python test_models_only.py
```

### **Test Full Platform (requires server running):**
```bash
python test_enhanced_platform.py
```

## 📱 **Usage Examples**

### **Nutrition Query:**
"I want to lose weight, what should I eat?"

### **Physiotherapy Query:**
"I have lower back pain, what exercises can help?"

### **Blood Bank Request:**
Select blood type (e.g., O+), urgency level, and city

## ⚠️ **Important Notes**

- This platform is for **educational purposes only**
- It is **NOT a substitute** for professional medical advice
- For medical emergencies, call **108** (India)
- All AI recommendations should be verified with healthcare professionals

## 🆘 **Need Help?**

1. Check the console output for error messages
2. Ensure all steps are completed in order
3. Verify Python and MySQL are installed
4. Check that port 5000 is not being used by another application

---

**🎉 Once everything is running, you'll have a complete health platform with AI-powered nutrition, physiotherapy, and blood bank services!**
