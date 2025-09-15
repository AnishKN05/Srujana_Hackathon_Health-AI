#!/usr/bin/env python3
"""
Simple backend startup script that works from any directory
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the backend server"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    print("🏥 Starting ML-based Health AI Platform Backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🤖 Using trained ML models")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory
        backend_dir = script_dir / "backend"
        os.chdir(backend_dir)
        
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

if __name__ == "__main__":
    main()
