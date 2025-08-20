#!/usr/bin/env python3
"""
🚀 AI Prompt Game v2.0 - Quick Start Script
One-click setup and launch for the web dashboard
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🎯" + "=" * 60 + "🎯")
    print("🚀 AI PROMPT GAME v2.0 - QUICK START")
    print("🎮 Gamified AI Prompt Engineering Learning")
    print("🎯" + "=" * 60 + "🎯")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. You have:", sys.version)
        print("💡 Please upgrade Python and try again.")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def check_and_install_package():
    """Check if ai-prompt-game is installed, install if needed"""
    try:
        import ai_prompt_game
        print("✅ AI Prompt Game package - Already installed")
        return True
    except ImportError:
        print("📦 Installing AI Prompt Game package...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ai-prompt-game"])
            print("✅ AI Prompt Game package - Installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install AI Prompt Game package")
            print("💡 Try manually: pip install ai-prompt-game")
            return False

def setup_game():
    """Set up the game (download targets)"""
    game_dir = Path.home() / ".ai-prompt-game"
    targets_dir = game_dir / "targets"
    
    if targets_dir.exists() and len(list(targets_dir.glob("*.jpg"))) > 0:
        print("✅ Game targets - Already set up")
        return True
    
    print("🎯 Setting up game targets...")
    try:
        subprocess.check_call([sys.executable, "-m", "ai_prompt_game.cli", "--setup"])
        print("✅ Game targets - Set up successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to set up game targets")
        print("💡 Try manually: ai-prompt-game --setup")
        return False

def install_web_requirements():
    """Install web dashboard requirements"""
    web_dir = Path(__file__).parent / "web_dashboard"
    requirements_file = web_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("⚠️  Web requirements file not found")
        return False
    
    print("🌐 Installing web dashboard requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Web requirements - Installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install web requirements")
        return False

def open_browser_delayed():
    """Open browser after a delay"""
    time.sleep(3)  # Wait for server to start
    webbrowser.open('http://localhost:8080')
    print("🌐 Browser opened to: http://localhost:8080")

def start_dashboard():
    """Start the web dashboard"""
    web_dir = Path(__file__).parent / "web_dashboard"
    app_file = web_dir / "app.py"
    
    if not app_file.exists():
        print("❌ Web dashboard app not found")
        return False
    
    print("🚀 Starting web dashboard...")
    print("📱 URL: http://localhost:8080")
    print("💡 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Change to web directory and start app
    original_dir = os.getcwd()
    try:
        os.chdir(web_dir)
        sys.path.insert(0, str(web_dir))
        
        # Import and run the app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
    finally:
        os.chdir(original_dir)

def main():
    """Main setup and launch function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install/check AI Prompt Game package
    if not check_and_install_package():
        return
    
    # Step 3: Set up game targets
    if not setup_game():
        return
    
    # Step 4: Install web requirements
    if not install_web_requirements():
        return
    
    print("\n🎉 Setup complete! Starting dashboard...")
    print("🎮 Get ready for gamified AI prompt engineering!")
    print()
    
    # Step 5: Start the dashboard
    start_dashboard()

if __name__ == "__main__":
    main()