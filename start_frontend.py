#!/usr/bin/env python3
"""
Health AI Platform Frontend Startup Script
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm version: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def check_package_json():
    """Check if package.json exists"""
    if not Path("package.json").exists():
        print("❌ package.json not found")
        return False
    print("✅ package.json found")
    return True

def install_dependencies():
    """Install npm dependencies"""
    print("📦 Installing frontend dependencies...")
    try:
        result = subprocess.run(["npm", "install"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_dev_server():
    """Start the Vite development server"""
    print("🚀 Starting Health AI Platform Frontend...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")

def main():
    """Main startup function"""
    print("🏥 Health AI Platform Frontend Startup")
    print("=" * 50)
    
    # Check Node.js
    if not check_node():
        sys.exit(1)
    
    # Check npm
    if not check_npm():
        sys.exit(1)
    
    # Check package.json
    if not check_package_json():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start dev server
    start_dev_server()

if __name__ == "__main__":
    main()
