#!/usr/bin/env python3
"""
One-Click Installer for AI Prompt Game
For students - installs everything automatically
"""

import subprocess
import sys
import os
import shutil

def install_dependencies():
    """Install required packages"""
    print("📦 Installing game dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--user"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("💡 Try: pip install opencv-python matplotlib numpy requests pillow")
        return False

def setup_game_files():
    """Set up game files in user directory"""
    print("📁 Setting up game files...")
    
    # Create game directory in user's home
    home_dir = os.path.expanduser("~")
    game_dir = os.path.join(home_dir, "ai_prompt_game")
    
    if os.path.exists(game_dir):
        print(f"🔄 Updating existing installation at {game_dir}")
        shutil.rmtree(game_dir)
    
    os.makedirs(game_dir)
    
    # Copy game files
    if os.path.exists("game_files"):
        for file in os.listdir("game_files"):
            src = os.path.join("game_files", file)
            dst = os.path.join(game_dir, file)
            shutil.copy2(src, dst)
    
    # Copy natural targets
    if os.path.exists("natural_target"):
        shutil.copytree("natural_target", os.path.join(game_dir, "natural_target"))
    
    print(f"✅ Game installed to: {game_dir}")
    return game_dir

def create_desktop_shortcut(game_dir):
    """Create desktop shortcut (Windows/Mac/Linux)"""
    try:
        import platform
        system = platform.system()
        
        if system == "Windows":
            # Create .bat file for Windows
            shortcut_content = f"""@echo off
cd /d "{game_dir}"
python play_natural_game.py
pause
"""
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "AI Prompt Game.bat")
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            print("✅ Desktop shortcut created (Windows)")
            
        elif system == "Darwin":  # Mac
            # Create .command file for Mac
            shortcut_content = f"""#!/bin/bash
cd "{game_dir}"
python3 play_natural_game.py
"""
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "AI Prompt Game.command")
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
            print("✅ Desktop shortcut created (Mac)")
            
        elif system == "Linux":
            # Create .desktop file for Linux
            shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=AI Prompt Game
Comment=Learn AI prompt engineering through games
Exec=python3 "{os.path.join(game_dir, 'play_natural_game.py')}"
Path={game_dir}
Icon=applications-games
Terminal=true
Categories=Education;Game;
"""
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "AI Prompt Game.desktop")
            with open(shortcut_path, "w") as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
            print("✅ Desktop shortcut created (Linux)")
            
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")

def main():
    """Main installer function"""
    print("🎯 AI Prompt Engineering Game - Student Installer")
    print("=" * 60)
    print("This will install the game on your computer.")
    print("You'll be able to play offline after installation!")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Please update Python.")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup game files
    game_dir = setup_game_files()
    if not game_dir:
        return
    
    # Create desktop shortcut
    create_desktop_shortcut(game_dir)
    
    # Success message
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETE!")
    print("=" * 60)
    print(f"📁 Game installed to: {game_dir}")
    print("🎮 To play: Double-click the desktop shortcut")
    print("📚 Or run: python play_natural_game.py")
    print("\n💡 The game uses free AI (Pollinations.ai) - no API keys needed!")
    print("🌐 Internet connection required for AI image generation")
    print("=" * 60)
    
    # Test installation
    test_choice = input("\n🧪 Test the installation now? (y/n): ").strip().lower()
    if test_choice == 'y':
        print("\n🚀 Starting game...")
        os.chdir(game_dir)
        try:
            subprocess.run([sys.executable, "play_natural_game.py"])
        except KeyboardInterrupt:
            print("\n👋 Game closed. Installation successful!")

if __name__ == "__main__":
    main()
