#!/usr/bin/env python3
"""
Simple script to run the API server
"""

import os
import sys
import subprocess

def install_requirements():
    """Install API requirements"""
    print("📦 Installing API requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "api_requirements.txt"
        ])
        print("✅ API requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install API requirements")
        print("💡 Try: pip install fastapi uvicorn opencv-python pillow numpy requests")
        return False

def run_server():
    """Run the API server"""
    print("🚀 Starting API server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔴 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Create necessary directories
        os.makedirs("api_sessions", exist_ok=True)
        
        # Run the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    print("🎯 AI Prompt Game API Server")
    print("=" * 40)
    
    # Install requirements first
    if install_requirements():
        run_server()
    else:
        print("❌ Cannot start server without requirements")
        sys.exit(1)
