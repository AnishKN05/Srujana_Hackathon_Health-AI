#!/usr/bin/env python3
"""
Enhanced Health Platform Setup Script
Sets up the complete health platform with nutrition, physio, and blood bank services
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and log the result"""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'mysql-connector-python', 'numpy', 'pandas',
        'scikit-learn', 'tensorflow', 'opencv-python', 'pillow', 'joblib'
    ]
    
    logger.info("Checking Python packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"❌ {package} is not installed")
    
    if missing_packages:
        logger.info("Installing missing packages...")
        install_command = f"pip install {' '.join(missing_packages)}"
        return run_command(install_command, "Installing missing Python packages")
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        'ml_models/trained_models',
        'simple_backend/templates',
        'simple_backend/services'
    ]
    
    logger.info("Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")
    
    return True

def train_ml_models():
    """Train all ML models"""
    logger.info("Training ML models...")
    
    # Train all models
    train_command = "python train_models.py --all"
    return run_command(train_command, "Training all ML models")

def test_models():
    """Test the trained models"""
    logger.info("Testing ML models...")
    
    test_command = "python train_models.py --test"
    return run_command(test_command, "Testing ML models")

def setup_database():
    """Setup MySQL database"""
    logger.info("Setting up database...")
    
    # Check if MySQL is running
    mysql_check = subprocess.run("mysql --version", shell=True, capture_output=True, text=True)
    if mysql_check.returncode != 0:
        logger.error("❌ MySQL is not installed or not running")
        logger.info("Please install MySQL and start the service")
        return False
    
    logger.info("✅ MySQL is available")
    
    # Create database and user (this will be handled by the app when it starts)
    logger.info("Database will be initialized when the application starts")
    return True

def create_startup_scripts():
    """Create startup scripts for easy deployment"""
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Enhanced Health AI Platform...
echo.

echo Training ML models...
python train_models.py --all
if %errorlevel% neq 0 (
    echo Error training models
    pause
    exit /b 1
)

echo.
echo Starting backend server...
cd simple_backend
python app.py
pause
"""
    
    with open('start_enhanced_platform.bat', 'w') as f:
        f.write(windows_script)
    
    # Linux/Mac shell script
    linux_script = """#!/bin/bash
echo "Starting Enhanced Health AI Platform..."
echo

echo "Training ML models..."
python train_models.py --all
if [ $? -ne 0 ]; then
    echo "Error training models"
    exit 1
fi

echo
echo "Starting backend server..."
cd simple_backend
python app.py
"""
    
    with open('start_enhanced_platform.sh', 'w') as f:
        f.write(linux_script)
    
    # Make shell script executable
    os.chmod('start_enhanced_platform.sh', 0o755)
    
    logger.info("✅ Created startup scripts")
    return True

def create_documentation():
    """Create comprehensive documentation"""
    
    readme_content = """# Enhanced Health AI Platform - India

A comprehensive health platform with AI-powered nutrition consultation, physiotherapy guidance, and blood bank services.

## Features

### 🩺 General Health
- Symptom analysis and diagnosis
- First aid guidance
- Emergency contacts
- Chat-based health consultation

### 🥗 Nutrition Consultation
- AI-powered dietary recommendations
- Meal planning
- Weight management guidance
- Diabetes and heart health nutrition
- Muscle building nutrition

### 🏃 Physiotherapy
- Exercise recommendations
- Injury assessment
- Posture correction
- Strength training guidance
- Flexibility and balance training

### 🩸 Blood Bank Services
- Blood availability checking
- Donor matching
- Nearby hospital search
- Emergency blood requests
- Blood type compatibility

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- 4GB+ RAM (for ML models)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd health-ai-platform
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL**
   - Install MySQL 8.0+
   - Create a database user with appropriate permissions
   - Update database credentials in `simple_backend/app.py`

4. **Train ML models**
   ```bash
   python train_models.py --all
   ```

5. **Start the platform**
   ```bash
   # Windows
   start_enhanced_platform.bat
   
   # Linux/Mac
   ./start_enhanced_platform.sh
   ```

### Manual Setup

1. **Train individual models**
   ```bash
   python train_models.py --nutrition  # Nutrition model only
   python train_models.py --physio     # Physiotherapy model only
   python train_models.py --blood      # Blood bank system only
   ```

2. **Test models**
   ```bash
   python train_models.py --test
   ```

3. **Start backend**
   ```bash
   cd simple_backend
   python app.py
   ```

## API Endpoints

### General Health
- `POST /api/symptoms/analyze` - Analyze symptoms
- `POST /api/chat` - General health chat

### Nutrition
- `POST /api/nutrition/consult` - Get nutrition advice

### Physiotherapy
- `POST /api/physio/consult` - Get physiotherapy guidance

### Blood Bank
- `POST /api/blood-bank/request` - Request blood
- `POST /api/blood-bank/donor-register` - Register as donor
- `GET /api/blood-bank/hospitals` - Get nearby hospitals

### Multi-Service
- `POST /api/services/chat` - Multi-service chat

## Usage

1. **Access the platform**: Open http://localhost:5000 in your browser
2. **Register**: Fill in your details and accept terms
3. **Choose service**: Select from General Health, Nutrition, Physiotherapy, or Blood Bank
4. **Get advice**: Ask questions or fill forms to get AI-powered recommendations

## Important Notes

- This platform is for **educational purposes only**
- It is **NOT a substitute** for professional medical advice
- For medical emergencies, call **108** (India)
- All AI recommendations should be verified with healthcare professionals

## Technical Details

### ML Models
- **Nutrition Classifier**: Random Forest, Gradient Boosting, Logistic Regression
- **Physiotherapy Classifier**: Random Forest, Gradient Boosting, Logistic Regression  
- **Blood Bank System**: Random Forest with geospatial matching
- **Symptom Classifier**: Rule-based with Indian healthcare context
- **Image Classifier**: CNN with EfficientNet backbone

### Database Schema
- Users, symptoms, image analysis
- Nutrition consultations
- Physiotherapy consultations
- Blood requests and donors
- Hospital and blood inventory data

### Technologies Used
- **Backend**: Flask, MySQL
- **ML**: scikit-learn, TensorFlow, OpenCV
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Python, Batch/Shell scripts

## Support

For issues or questions:
1. Check the logs in the console
2. Verify MySQL connection
3. Ensure all models are trained
4. Check API endpoints are responding

## License

This project is for educational use only.
"""
    
    with open('README_ENHANCED.md', 'w') as f:
        f.write(readme_content)
    
    logger.info("✅ Created comprehensive documentation")
    return True

def main():
    """Main setup function"""
    logger.info("🚀 Starting Enhanced Health AI Platform Setup")
    logger.info("=" * 60)
    
    steps = [
        ("Checking Python packages", check_python_packages),
        ("Setting up directories", setup_directories),
        ("Training ML models", train_ml_models),
        ("Testing models", test_models),
        ("Setting up database", setup_database),
        ("Creating startup scripts", create_startup_scripts),
        ("Creating documentation", create_documentation)
    ]
    
    success = True
    for step_name, step_function in steps:
        logger.info(f"\n📋 {step_name}...")
        if not step_function():
            logger.error(f"❌ {step_name} failed")
            success = False
            break
        logger.info(f"✅ {step_name} completed")
    
    if success:
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Enhanced Health AI Platform setup completed successfully!")
        logger.info("\n📋 Next steps:")
        logger.info("1. Update MySQL credentials in simple_backend/app.py")
        logger.info("2. Start the platform:")
        logger.info("   - Windows: start_enhanced_platform.bat")
        logger.info("   - Linux/Mac: ./start_enhanced_platform.sh")
        logger.info("3. Open http://localhost:5000 in your browser")
        logger.info("\n🔬 Available services:")
        logger.info("   • General Health Chat")
        logger.info("   • Nutrition Consultation")
        logger.info("   • Physiotherapy Guidance")
        logger.info("   • Blood Bank Services")
        logger.info("\n⚠️  Remember: This is for educational purposes only!")
        logger.info("   For medical emergencies, call 108 (India)")
    else:
        logger.error("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
