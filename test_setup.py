#!/usr/bin/env python3
"""
Test script to verify the ML Health AI Platform setup
"""
import os
import sys
import subprocess
from pathlib import Path

def test_python_imports():
    """Test if all required Python packages are installed"""
    print("🔍 Testing Python imports...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'cv2', 'torch', 'sklearn', 
        'tensorflow', 'nltk', 'pandas', 'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'sklearn':
                import sklearn
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All Python packages are installed")
    return True

def test_node_setup():
    """Test if Node.js and npm are working"""
    print("\n🔍 Testing Node.js setup...")
    
    try:
        # Test Node.js
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Node.js: {result.stdout.strip()}")
        else:
            print("  ❌ Node.js not found")
            return False
        
        # Test npm
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ npm: {result.stdout.strip()}")
        else:
            print("  ❌ npm not found")
            return False
        
        return True
    except FileNotFoundError:
        print("  ❌ Node.js or npm not found")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'package.json',
        'requirements.txt',
        'backend/main.py',
        'src/main.jsx',
        'run_backend.py',
        'run_frontend.py'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def test_ml_models():
    """Test if ML models are available"""
    print("\n🔍 Testing ML models...")
    
    models_dir = Path("ml_models/trained_models")
    if not models_dir.exists():
        print("  ❌ ML models directory not found")
        print("  Run: python setup_ml_platform.py")
        return False
    
    required_models = [
        "symptom_model.pkl",
        "vectorizer.pkl",
        "label_encoder.pkl",
        "skin_classifier.h5"
    ]
    
    missing_models = []
    for model in required_models:
        if (models_dir / model).exists():
            print(f"  ✅ {model}")
        else:
            print(f"  ❌ {model}")
            missing_models.append(model)
    
    if missing_models:
        print(f"\n❌ Missing models: {', '.join(missing_models)}")
        print("  Run: python setup_ml_platform.py")
        return False
    
    print("✅ All ML models are available")
    return True

def test_backend_startup():
    """Test if backend can start (quick test)"""
    print("\n🔍 Testing backend startup...")
    
    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir("backend")
        
        # Try to import the main module
        sys.path.insert(0, '.')
        import main
        
        print("  ✅ Backend imports successfully")
        os.chdir(original_dir)
        return True
        
    except Exception as e:
        print(f"  ❌ Backend startup failed: {e}")
        os.chdir(original_dir)
        return False

def main():
    """Run all tests"""
    print("🏥 ML Health AI Platform - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Packages", test_python_imports),
        ("Node.js Setup", test_node_setup),
        ("File Structure", test_file_structure),
        ("ML Models", test_ml_models),
        ("Backend Startup", test_backend_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the platform:")
        print("  Terminal 1: python run_backend.py")
        print("  Terminal 2: python run_frontend.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Run: npm install")
        print("  - Run: python setup_ml_platform.py")

if __name__ == "__main__":
    main()
