# Health AI Platform (ML-Based)

A comprehensive multi-modal ML platform that provides accessible, preliminary health assessment by combining symptom analysis and image recognition. This application uses trained machine learning models instead of external AI services for better control and privacy.

## 🚨 Important Medical Disclaimer

**This platform is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health professionals with any questions about medical conditions.**

## Features

### 🔍 ML-Powered Symptom Checker
- Trained machine learning model for symptom classification
- Analyzes symptoms and health history using NLP techniques
- Provides list of possible conditions with probability scores
- Offers actionable first-aid advice based on condition database
- Includes emergency guidance and when to seek professional help

### 📸 ML-Based Image Analysis
- Trained computer vision model for skin condition classification
- Detects visual features like redness, swelling, lesions using OpenCV
- Provides ML-driven preliminary diagnosis with confidence scores
- Supports 15+ skin conditions including wounds, rashes, and infections
- Image quality assessment and feature detection

### 🛡️ Safety-First Approach
- Comprehensive medical disclaimers throughout the application
- Clear guidance on when to seek professional medical help
- Emergency contact information and warning signs
- Privacy-focused with local ML processing (no external API calls)

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Scikit-learn** - Machine learning library for symptom classification
- **TensorFlow/Keras** - Deep learning for image classification
- **OpenCV** - Computer vision and image processing
- **NLTK** - Natural language processing for text analysis
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Machine Learning Models
- **Symptom Classifier** - Random Forest/Gradient Boosting for symptom analysis
- **Image Classifier** - EfficientNet-based CNN for skin condition classification
- **Feature Detection** - OpenCV-based visual feature extraction
- **NLP Processing** - TF-IDF vectorization and text preprocessing

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- 4GB+ RAM (for ML model training and inference)
- No external API keys required (uses local ML models)

### Quick Start (Recommended)

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd health-ai-platform
   ```

2. **Run the complete setup script**
   ```bash
   python setup_ml_platform.py
   ```
   This will:
   - Install all dependencies
   - Train the ML models
   - Set up the environment
   - Create startup scripts

3. **Start ML Backend (Terminal 1)**
   ```bash
   python start_ml_backend.py
   ```

4. **Start Frontend (Terminal 2)**
   ```bash
   python start_frontend.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the backend server**
   ```bash
   cd backend
   python main.py
   ```

#### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

### Troubleshooting

#### Common Issues

**1. OpenAI API Key Issues**
- Make sure you have a valid OpenAI API key
- Check that the key is correctly set in your `.env` file
- Ensure you have credits in your OpenAI account

**2. Backend Not Starting**
- Check if port 8000 is available
- Verify all Python dependencies are installed
- Check the console for error messages

**3. Frontend Not Loading**
- Ensure Node.js 16+ is installed
- Run `npm install` to install dependencies
- Check if port 3000 is available

**4. API Connection Issues**
- Verify backend is running on http://localhost:8000
- Check CORS settings in backend
- Ensure VITE_API_BASE_URL is set correctly

**5. Image Upload Issues**
- Check file size (max 5MB)
- Ensure file is a valid image format (JPG, PNG, WebP)
- Verify backend image processing is working

#### Getting Help

If you encounter issues:
1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Ensure your OpenAI API key is valid and has credits
4. Check that both frontend and backend are running

## Usage

### Symptom Checker
1. Navigate to the Symptom Checker page
2. Describe your symptoms in the chat interface
3. Answer follow-up questions from the AI
4. Receive preliminary analysis and first-aid guidance
5. Review recommendations and when to seek professional help

### Image Analysis
1. Go to the Image Analysis page
2. Upload a clear image of the condition
3. Add optional description for context
4. Receive AI analysis with confidence scores
5. Review detected features and recommendations

## API Endpoints

### Health & Status
- `GET /` - API information
- `GET /health` - Health check

### Symptom Analysis
- `POST /api/symptoms/analyze` - Analyze symptoms
- `POST /api/chat` - Chat with health AI

### Image Analysis
- `POST /api/image/analyze` - Analyze uploaded image

### Information
- `GET /api/disclaimers` - Get medical disclaimers

## Configuration

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000

# Model Configuration
MODEL_CACHE_DIR=./models
MAX_IMAGE_SIZE=5242880  # 5MB
ALLOWED_IMAGE_TYPES=jpg,jpeg,png,webp
```

## Development

### Project Structure
```
health-ai-platform/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   └── services/
│       ├── symptom_checker.py  # LLM symptom analysis
│       └── image_analyzer.py   # Computer vision analysis
├── src/
│   ├── components/             # React components
│   ├── pages/                  # Application pages
│   ├── services/               # API services
│   └── context/                # React context
├── requirements.txt            # Python dependencies
├── package.json               # Node.js dependencies
└── README.md
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
npm test
```

### Building for Production
```bash
# Build frontend
npm run build

# Run backend in production
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Security & Privacy

- Images are processed securely and not stored permanently
- All API communications use HTTPS in production
- User data is not shared with third parties
- Medical disclaimers are prominently displayed
- Emergency contact information is readily available

## Limitations

- AI analysis accuracy depends on input quality
- Cannot perform physical examinations
- Cannot access complete medical history
- Cannot provide definitive medical diagnoses
- Should not replace professional medical consultation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Emergency Resources

- **Emergency Services**: 100
- **Poison Control**: 1800-425-1213
- **National Suicide Prevention**: 9152987821
- **National Domestic Violence**: 8793088814

## Support

For technical support or questions about the platform, please open an issue in the repository.

**Remember: This platform is for educational purposes only. For medical emergencies, call 108 immediately.**
#   S r u j a n a _ H a c k a t h o n _ H e a l t h - A I  
 