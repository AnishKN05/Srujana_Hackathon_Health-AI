#!/usr/bin/env python3
"""
Simple frontend startup script that works from any directory
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the frontend server"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    print("🏥 Starting Health AI Platform Frontend...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Check if package.json exists
        package_json = script_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json not found. Make sure you're in the project root directory.")
            return
        
        # Install dependencies if node_modules doesn't exist
        node_modules = script_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start the development server
        subprocess.run(["npm", "run", "dev"])
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend server: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
