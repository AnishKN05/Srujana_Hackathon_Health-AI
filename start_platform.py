#!/usr/bin/env python3
"""
Simple Health Platform Startup Script
Starts the enhanced health platform with all services
"""
import os
import sys
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import mysql.connector
        import numpy
        import pandas
        import sklearn
        import tensorflow
        import cv2
        import PIL
        import joblib
        logger.info("✅ All required packages are installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing package: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return False

def train_models():
    """Train ML models if they don't exist"""
    model_path = "ml_models/trained_models"
    if not os.path.exists(model_path):
        logger.info("📚 Training ML models...")
        try:
            result = subprocess.run([sys.executable, "train_models.py", "--all"], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logger.info("✅ Models trained successfully")
                return True
            else:
                logger.error(f"❌ Model training failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("❌ Model training timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Model training error: {e}")
            return False
    else:
        logger.info("✅ ML models already exist")
        return True

def start_server():
    """Start the Flask server"""
    logger.info("🚀 Starting Health AI Platform...")
    
    # Change to simple_backend directory
    os.chdir("simple_backend")
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    logger.info("🏥 Health AI Platform Startup")
    logger.info("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Train models if needed
    if not train_models():
        logger.warning("⚠️  Continuing without trained models...")
    
    # Start server
    logger.info("🌐 Starting web server...")
    logger.info("📍 Platform will be available at: http://localhost:5000")
    logger.info("🛑 Press Ctrl+C to stop the server")
    logger.info("=" * 50)
    
    start_server()

if __name__ == "__main__":
    main()
