#!/usr/bin/env python3
"""
Indian Health AI Platform Startup Script
Enhanced with Indian healthcare details, authentication, and first aid
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python not found: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "simple_backend/requirements.txt"], 
                      check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_mysql():
    """Check if MySQL is available"""
    print("\n🔍 Checking MySQL...")
    print("⚠️  Make sure MySQL is installed and running")
    print("📝 Default connection settings:")
    print("   Host: localhost")
    print("   Port: 3306")
    print("   User: root")
    print("   Password: password (change in simple_backend/app.py)")
    print("   Database: health_ai_db (will be created automatically)")
    return True

def start_backend():
    """Start the Flask backend"""
    print("\n🚀 Starting Indian Health AI Platform...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🚑 First Aid Guide: http://localhost:5000/firstaid.html")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        os.chdir("simple_backend")
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🏥 Indian Health AI Platform Startup")
    print("🇮🇳 Enhanced with Indian Healthcare Details")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check MySQL
    check_mysql()
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
