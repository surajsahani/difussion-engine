#!/usr/bin/env python3
"""
Startup script for Prompt Guessing Game API
Handles setup and server startup
"""

import subprocess
import sys
import os
import time
import requests

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing API dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "api_requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "opencv-python",
        "pillow",
        "numpy",
        "requests"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    
    print("✅ All required packages available")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "api_sessions",
        "uploads",
        "static"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI server"""
    print(f"🚀 Starting API server on {host}:{port}")
    print(f"📖 Swagger docs will be available at: http://localhost:{port}/docs")
    print(f"📚 ReDoc will be available at: http://localhost:{port}/redoc")
    
    try:
        import uvicorn
        uvicorn.run(
            "api_server:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n⏸️  Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def test_server(host="localhost", port=8000, timeout=30):
    """Test if server is running"""
    url = f"http://{host}:{port}/health"
    
    print(f"🧪 Testing server at {url}")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < timeout - 1:
            print(f"⏳ Waiting for server... ({i+1}/{timeout})")
            time.sleep(1)
    
    print("❌ Server health check failed")
    return False

def show_usage():
    """Show usage examples"""
    print("\n🎯 API Usage Examples:")
    print("=" * 50)
    
    print("\n📖 Swagger UI (Interactive docs):")
    print("   http://localhost:8000/docs")
    
    print("\n🔧 CLI Client:")
    print("   python cli_client.py                    # Interactive mode")
    print("   python cli_client.py --target image.jpg # Quick start")
    print("   python cli_client.py --list             # List sessions")
    
    print("\n🌐 API Endpoints:")
    print("   POST /game/create                       # Create session")
    print("   POST /game/attempt                      # Make attempt")
    print("   GET  /game/{session_id}/progress        # Get progress")
    print("   GET  /game/{session_id}/target          # Get target image")
    
    print("\n💡 Example cURL commands:")
    print("   # Health check")
    print("   curl http://localhost:8000/health")
    print()
    print("   # Create session")
    print("   curl -X POST -F 'target_image=@image.jpg' -F 'model_type=pollinations' \\")
    print("        http://localhost:8000/game/create")

def main():
    """Main startup function"""
    print("🎯 Prompt Guessing Game API Startup")
    print("=" * 50)
    
    # Check/install dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Setup failed. Please install dependencies manually:")
            print("pip install -r api_requirements.txt")
            return
    
    # Create directories
    create_directories()
    
    # Show usage info
    show_usage()
    
    print("\n" + "=" * 50)
    
    # Ask user what to do
    print("Choose an option:")
    print("1. 🚀 Start API server")
    print("2. 🧪 Test existing server")
    print("3. 📖 Show usage examples only")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting server...")
        start_server()
    elif choice == "2":
        test_server()
    elif choice == "3":
        show_usage()
    else:
        print("🚀 Starting server by default...")
        start_server()

if __name__ == "__main__":
    main()