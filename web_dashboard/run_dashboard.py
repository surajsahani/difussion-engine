#!/usr/bin/env python3
"""
Easy startup script for AI Prompt Game Web Dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def check_setup():
    """Check if the game is set up"""
    game_dir = Path.home() / ".ai-prompt-game"
    targets_dir = game_dir / "targets"
    
    if not targets_dir.exists() or len(list(targets_dir.glob("*.jpg"))) == 0:
        print("🚨 Game not set up yet!")
        print("\n📋 Please run the setup first:")
        print("   pip install ai-prompt-game")
        print("   ai-prompt-game --setup")
        print("\n💡 Then run this dashboard again!")
        return False
    
    return True

def install_requirements():
    """Install dashboard requirements"""
    try:
        import flask
        import cv2
        import numpy
        import PIL
        print("✅ All requirements already installed!")
        return True
    except ImportError:
        print("📦 Installing dashboard requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements!")
            return False

def main():
    print("🚀 AI Prompt Game v2.0 - Web Dashboard")
    print("=" * 50)
    
    # Check if game is set up
    if not check_setup():
        return
    
    # Install requirements if needed
    if not install_requirements():
        return
    
    # Start the dashboard
    print("\n🌐 Starting web dashboard...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🎮 Enjoy the gamified experience!")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        print("\n💡 Make sure you have installed the ai-prompt-game package:")
        print("   pip install ai-prompt-game")

if __name__ == "__main__":
    main()