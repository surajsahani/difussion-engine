#!/usr/bin/env python3
"""
Quick test of the API server
"""

import subprocess
import time
import requests
import sys
import os
from threading import Thread

def start_server_background():
    """Start server in background"""
    try:
        subprocess.run([
            sys.executable, "-c",
            "import uvicorn; uvicorn.run('api_server:app', host='127.0.0.1', port=8000, log_level='error')"
        ], check=True, capture_output=True)
    except:
        pass

def test_api():
    """Test the API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Prompt Guessing Game API")
    print("=" * 40)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is running!")
                break
        except:
            time.sleep(1)
    else:
        print("❌ Server failed to start")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data['message']}")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test session creation (would need actual image file)
    print("💡 API server is working!")
    print("🌐 Swagger docs available at: http://127.0.0.1:8000/docs")
    print("📚 ReDoc available at: http://127.0.0.1:8000/redoc")
    
    return True

if __name__ == "__main__":
    # Start server in background thread
    server_thread = Thread(target=start_server_background, daemon=True)
    server_thread.start()
    
    # Give server time to start
    time.sleep(3)
    
    # Test the API
    success = test_api()
    
    if success:
        print("\n🎉 API test successful!")
        print("\n🚀 To start the full server:")
        print("python api_server.py")
        print("\n🎮 To use the CLI client:")
        print("python cli_client.py")
    else:
        print("\n❌ API test failed")
        print("💡 Try running manually: python api_server.py")