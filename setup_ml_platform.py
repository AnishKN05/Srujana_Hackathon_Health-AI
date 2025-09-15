#!/usr/bin/env python3
"""
Complete setup script for ML-based Health AI Platform
Handles model training, environment setup, and deployment preparation
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

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def install_requirements():
    """Install Python requirements"""
    logger.info("Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        logger.info("Python requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Python requirements: {e}")
        return False

def install_nltk_data():
    """Download required NLTK data"""
    logger.info("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        logger.info("NLTK data downloaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to download NLTK data: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    logger.info("Creating directories...")
    directories = [
        'ml_models/trained_models',
        'backend/logs',
        'data/synthetic',
        'models/cache'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    return True

def setup_environment():
    """Setup environment configuration"""
    logger.info("Setting up environment...")
    
    # Check if .env exists
    if not Path('.env').exists():
        if Path('env.example').exists():
            # Copy env.example to .env
            with open('env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            logger.info("Created .env file from env.example")
        else:
            logger.warning("No env.example found. Please create .env file manually.")
    
    return True

def train_models():
    """Train the ML models"""
    logger.info("Training ML models...")
    try:
        # Run the training script
        result = subprocess.run([sys.executable, "train_models.py", "--all"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Models trained successfully")
            logger.info("Training output:")
            print(result.stdout)
            return True
        else:
            logger.error("Model training failed")
            logger.error("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        logger.error(f"Error training models: {e}")
        return False

def test_models():
    """Test the trained models"""
    logger.info("Testing trained models...")
    try:
        result = subprocess.run([sys.executable, "train_models.py", "--test"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Model testing completed successfully")
            logger.info("Test output:")
            print(result.stdout)
            return True
        else:
            logger.error("Model testing failed")
            logger.error("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        logger.error(f"Error testing models: {e}")
        return False

def create_startup_scripts():
    """Create startup scripts for the ML platform"""
    logger.info("Creating startup scripts...")
    
    # Create ML backend startup script
    ml_backend_script = """#!/usr/bin/env python3
import os
import sys
import subprocess

def start_ml_backend():
    print("🏥 Starting ML-based Health AI Platform Backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🤖 Using ML models instead of OpenAI")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_ml_backend()
"""
    
    with open('start_ml_backend.py', 'w') as f:
        f.write(ml_backend_script)
    
    # Make it executable
    os.chmod('start_ml_backend.py', 0o755)
    
    logger.info("Created ML backend startup script")
    return True

def verify_setup():
    """Verify the setup is complete"""
    logger.info("Verifying setup...")
    
    checks = [
        ("Python requirements", Path("requirements.txt").exists()),
        ("ML models directory", Path("ml_models").exists()),
        ("Backend directory", Path("backend").exists()),
        ("Frontend directory", Path("src").exists()),
        ("Environment file", Path(".env").exists()),
        ("Trained models", Path("ml_models/trained_models").exists()),
    ]
    
    all_good = True
    for check_name, check_result in checks:
        if check_result:
            logger.info(f"✅ {check_name}: OK")
        else:
            logger.error(f"❌ {check_name}: Missing")
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    logger.info("🏥 Setting up ML-based Health AI Platform")
    logger.info("=" * 60)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Installing requirements", install_requirements),
        ("Installing NLTK data", install_nltk_data),
        ("Training ML models", train_models),
        ("Testing models", test_models),
        ("Creating startup scripts", create_startup_scripts),
        ("Verifying setup", verify_setup)
    ]
    
    for step_name, step_function in steps:
        logger.info(f"\n📋 {step_name}...")
        if not step_function():
            logger.error(f"❌ {step_name} failed!")
            sys.exit(1)
        logger.info(f"✅ {step_name} completed")
    
    logger.info("\n🎉 ML-based Health AI Platform setup completed successfully!")
    logger.info("\n📖 Next steps:")
    logger.info("1. Edit .env file with your configuration")
    logger.info("2. Start the ML backend: python start_ml_backend.py")
    logger.info("3. Start the frontend: python start_frontend.py")
    logger.info("4. Access the platform at: http://localhost:3000")
    logger.info("\n🤖 The platform now uses trained ML models instead of OpenAI!")
    logger.info("💡 Models are trained on synthetic data and can be improved with real data")

if __name__ == "__main__":
    main()
