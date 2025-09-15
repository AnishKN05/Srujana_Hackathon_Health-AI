#!/usr/bin/env python3
"""
Simple Health Platform Starter
Starts the platform without complex dependencies
"""
import os
import sys
import subprocess

def main():
    print("🏥 Starting Health AI Platform...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("simple_backend"):
        print("❌ Error: simple_backend directory not found")
        print("Please run this script from the project root directory")
        return
    
    # Change to simple_backend directory
    os.chdir("simple_backend")
    
    print("📁 Changed to simple_backend directory")
    print("🚀 Starting Flask server...")
    print("📍 Platform will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the Flask app directly
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the project root directory")
        print("2. Check if port 5000 is already in use")
        print("3. Verify Python and Flask are installed")

if __name__ == "__main__":
    main()
