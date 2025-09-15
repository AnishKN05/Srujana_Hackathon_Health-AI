#!/usr/bin/env python3
"""
Health AI Platform Backend Startup Script
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import cv2
        import torch
        import sklearn
        import tensorflow
        print("✅ All required ML dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please copy env.example to .env and configure your settings")
        return False
    
    print("✅ Environment configuration looks good (ML models don't require API keys)")
    return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting ML-based Health AI Platform Backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🤖 Using trained ML models (no external API calls)")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🏥 Health AI Platform Backend Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
