# 🏥 Enhanced Health AI Platform - India

A comprehensive AI-powered health platform with **Nutrition Consultation**, **Physiotherapy Guidance**, and **Blood Bank Services** integrated with the existing symptom analysis and diagnosis features.

## 🚀 New Features Added

### 🥗 Nutrition Consultation
- **AI-powered dietary recommendations** for various health goals
- **Meal planning** with sample meal plans
- **Weight management** guidance (loss/gain)
- **Medical condition-specific** nutrition (diabetes, heart health, etc.)
- **Muscle building** and sports nutrition
- **Age-specific** recommendations (teenagers, seniors)

### 🏃 Physiotherapy Guidance
- **Exercise recommendations** for various conditions
- **Injury assessment** and rehabilitation guidance
- **Posture correction** exercises
- **Strength training** programs
- **Flexibility and balance** training
- **Precautions and safety** guidelines

### 🩸 Blood Bank Services
- **Blood availability checking** in nearby hospitals
- **Donor matching** based on blood type compatibility
- **Nearby hospital search** with distance calculation
- **Emergency blood requests** with urgency levels
- **Blood type compatibility** matrix
- **Real-time inventory** tracking

## 🏗️ Architecture

### ML Models
1. **Nutrition Classifier** - Random Forest, Gradient Boosting, Logistic Regression
2. **Physiotherapy Classifier** - Random Forest, Gradient Boosting, Logistic Regression
3. **Blood Bank System** - Random Forest with geospatial matching
4. **Enhanced Symptom Classifier** - Rule-based with Indian healthcare context
5. **Image Classifier** - CNN with EfficientNet backbone

### Database Schema
- **Users** - User registration and profiles
- **Symptoms** - Symptom analysis history
- **Image Analysis** - Image-based diagnosis
- **Nutrition Consultations** - Nutrition advice history
- **Physio Consultations** - Physiotherapy guidance history
- **Blood Requests** - Blood requirement tracking
- **Blood Donors** - Donor database
- **Hospitals** - Hospital and blood bank information
- **Blood Inventory** - Real-time blood stock tracking

## 📋 Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- 4GB+ RAM (for ML models)
- Windows/Linux/Mac

### Quick Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd health-ai-platform
   pip install -r requirements.txt
   ```

2. **Run automated setup**
   ```bash
   python setup_enhanced_health_platform.py
   ```

3. **Start the platform**
   ```bash
   # Windows
   start_enhanced_platform.bat
   
   # Linux/Mac
   ./start_enhanced_platform.sh
   ```

4. **Access the platform**
   - Open http://localhost:5000 in your browser
   - Register with your details
   - Choose from 4 services: General Health, Nutrition, Physiotherapy, Blood Bank

### Manual Setup

1. **Train ML models**
   ```bash
   python train_models.py --all
   ```

2. **Update database credentials**
   - Edit `simple_backend/app.py`
   - Update MySQL connection details

3. **Start backend**
   ```bash
   cd simple_backend
   python app.py
   ```

4. **Test the platform**
   ```bash
   python test_enhanced_platform.py
   ```

## 🔌 API Endpoints

### General Health
- `POST /api/symptoms/analyze` - Analyze symptoms
- `POST /api/chat` - General health chat
- `POST /api/image/analyze` - Image-based diagnosis

### Nutrition Services
- `POST /api/nutrition/consult` - Get nutrition advice
- Categories: weight_loss, weight_gain, diabetes_management, heart_health, muscle_building, general_health

### Physiotherapy Services
- `POST /api/physio/consult` - Get physiotherapy guidance
- Categories: back_pain, neck_pain, knee_pain, shoulder_pain, posture_correction, strength_training, flexibility, balance_training

### Blood Bank Services
- `POST /api/blood-bank/request` - Request blood
- `POST /api/blood-bank/donor-register` - Register as donor
- `GET /api/blood-bank/hospitals` - Get nearby hospitals

### Multi-Service
- `POST /api/services/chat` - Multi-service chat with service type selection

## 🎯 Usage Examples

### Nutrition Consultation
```json
POST /api/nutrition/consult
{
  "user_id": "user123",
  "query": "I want to lose weight, what should I eat?",
  "user_context": {
    "age": 30,
    "gender": "male",
    "location": "delhi"
  }
}
```

### Physiotherapy Guidance
```json
POST /api/physio/consult
{
  "user_id": "user123",
  "query": "I have lower back pain, what exercises can help?",
  "user_context": {
    "age": 30,
    "gender": "male",
    "fitness_level": "beginner"
  }
}
```

### Blood Bank Request
```json
POST /api/blood-bank/request
{
  "user_id": "user123",
  "blood_type": "O+",
  "request_type": "urgent_blood_request",
  "urgency_level": "high",
  "city": "Delhi",
  "state": "Delhi",
  "contact_number": "+91-9876543210"
}
```

## 🧪 Testing

### Run All Tests
```bash
python test_enhanced_platform.py
```

### Test Individual Services
```bash
# Test nutrition service
curl -X POST http://localhost:5000/api/nutrition/consult \
  -H "Content-Type: application/json" \
  -d '{"query": "I want to lose weight"}'

# Test physio service
curl -X POST http://localhost:5000/api/physio/consult \
  -H "Content-Type: application/json" \
  -d '{"query": "I have back pain"}'

# Test blood bank
curl -X POST http://localhost:5000/api/blood-bank/request \
  -H "Content-Type: application/json" \
  -d '{"blood_type": "O+", "city": "Delhi"}'
```

## 📊 Features Comparison

| Feature | Original Platform | Enhanced Platform |
|---------|------------------|-------------------|
| Symptom Analysis | ✅ | ✅ Enhanced |
| Image Analysis | ✅ | ✅ Enhanced |
| General Chat | ✅ | ✅ Enhanced |
| Nutrition Advice | ❌ | ✅ **NEW** |
| Physiotherapy | ❌ | ✅ **NEW** |
| Blood Bank | ❌ | ✅ **NEW** |
| Donor Matching | ❌ | ✅ **NEW** |
| Hospital Search | ❌ | ✅ **NEW** |
| ML Models | 2 | 5 |
| API Endpoints | 4 | 10+ |
| Database Tables | 4 | 8 |

## 🔧 Configuration

### Environment Variables
```bash
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=health_ai_db

# ML Models
MODEL_PATH=ml_models/trained_models/
```

### Model Training Options
```bash
# Train specific models
python train_models.py --nutrition    # Nutrition only
python train_models.py --physio       # Physiotherapy only
python train_models.py --blood        # Blood bank only
python train_models.py --all          # All models

# Test models
python train_models.py --test
```

## 🚨 Important Notes

### Medical Disclaimer
- This platform is for **educational purposes only**
- It is **NOT a substitute** for professional medical advice
- For medical emergencies, call **108** (India)
- All AI recommendations should be verified with healthcare professionals

### Data Privacy
- User data is stored securely in MySQL database
- No personal information is shared with third parties
- All consultations are logged for educational purposes

### Performance
- ML models are trained on synthetic data
- Real-world accuracy may vary
- Models should be retrained with real data for production use

## 🐛 Troubleshooting

### Common Issues

1. **Models not loading**
   ```bash
   # Retrain models
   python train_models.py --all
   ```

2. **Database connection error**
   - Check MySQL is running
   - Verify credentials in `simple_backend/app.py`
   - Ensure database exists

3. **Import errors**
   ```bash
   # Install missing packages
   pip install -r requirements.txt
   ```

4. **Port already in use**
   - Change port in `simple_backend/app.py`
   - Kill existing processes on port 5000

### Logs and Debugging
- Check console output for error messages
- Enable debug mode in Flask app
- Check MySQL logs for database issues

## 📈 Future Enhancements

### Planned Features
- [ ] Real-time chat with healthcare professionals
- [ ] Integration with wearable devices
- [ ] Telemedicine video consultations
- [ ] Prescription management
- [ ] Appointment booking
- [ ] Health records management
- [ ] Multi-language support
- [ ] Mobile app development

### Technical Improvements
- [ ] Model performance optimization
- [ ] Real-time data integration
- [ ] Advanced analytics dashboard
- [ ] API rate limiting
- [ ] Caching implementation
- [ ] Load balancing
- [ ] Microservices architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is for educational use only. Please ensure compliance with local healthcare regulations before using in production.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs
3. Test individual components
4. Create an issue with detailed information

---

**🎉 The Enhanced Health AI Platform is now ready with comprehensive nutrition, physiotherapy, and blood bank services!**
