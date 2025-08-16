#!/usr/bin/env python3
"""
Create Student Installation Package
Bundles everything students need for local installation
"""

import os
import shutil
import zipfile
import json
from datetime import datetime

def create_student_package():
    """Create complete student installation package"""
    
    print("📦 Creating Student Installation Package")
    print("=" * 50)
    
    # Create package directory
    package_dir = "student_package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy essential game files
    game_files = [
        "open_llm_game.py",
        "play_natural_game.py", 
        "create_natural_targets.py",
        "test_pollinations.py"
    ]
    
    game_dir = f"{package_dir}/game_files"
    os.makedirs(game_dir)
    
    for file in game_files:
        if os.path.exists(file):
            shutil.copy2(file, game_dir)
            print(f"✅ Copied: {file}")
    
    # Copy natural targets if they exist
    if os.path.exists("natural_targets"):
        shutil.copytree("natural_targets", f"{package_dir}/natural_targets")
        print("✅ Copied: natural_targets/")
    
    # Create minimal requirements.txt for students
    student_requirements = """# Minimal requirements for students
opencv-python>=4.5.0
matplotlib>=3.5.0
numpy>=1.21.0
requests>=2.28.0
pillow>=9.0.0
"""
    
    with open(f"{package_dir}/requirements.txt", "w") as f:
        f.write(student_requirements)
    print("✅ Created: requirements.txt")
    
    # Create one-click installer
    installer_code = '''#!/usr/bin/env python3
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
    if os.path.exists("natural_targets"):
        shutil.copytree("natural_targets", os.path.join(game_dir, "natural_targets"))
    
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
    print("\\n" + "=" * 60)
    print("🎉 INSTALLATION COMPLETE!")
    print("=" * 60)
    print(f"📁 Game installed to: {game_dir}")
    print("🎮 To play: Double-click the desktop shortcut")
    print("📚 Or run: python play_natural_game.py")
    print("\\n💡 The game uses free AI (Pollinations.ai) - no API keys needed!")
    print("🌐 Internet connection required for AI image generation")
    print("=" * 60)
    
    # Test installation
    test_choice = input("\\n🧪 Test the installation now? (y/n): ").strip().lower()
    if test_choice == 'y':
        print("\\n🚀 Starting game...")
        os.chdir(game_dir)
        try:
            subprocess.run([sys.executable, "play_natural_game.py"])
        except KeyboardInterrupt:
            print("\\n👋 Game closed. Installation successful!")

if __name__ == "__main__":
    main()
'''
    
    with open(f"{package_dir}/install.py", "w") as f:
        f.write(installer_code)
    print("✅ Created: install.py")
    
    # Create student README
    readme_content = """# 🎯 AI Prompt Engineering Game - Student Edition

## 🚀 Quick Start (2 minutes!)

### Step 1: Install
```bash
python install.py
```

### Step 2: Play!
- Double-click the desktop shortcut, OR
- Run: `python play_natural_game.py`

## 🎮 How to Play

1. **Choose a challenge** (mountain sunset, ocean waves, etc.)
2. **See the target image** you need to match
3. **Write prompts** describing what you see
4. **AI generates images** based on your prompts
5. **Get scores and feedback** to improve
6. **Keep trying** until you match the target!

## 💡 Tips for Better Prompts

- **Be specific**: "golden sunset" vs "sunset"
- **Include style**: "landscape photography", "natural"
- **Describe colors**: "orange sky", "blue water"
- **Add details**: "dramatic clouds", "mountain peaks"

## 🆘 Need Help?

### Game Won't Start?
- Make sure Python 3.8+ is installed
- Run: `pip install opencv-python matplotlib numpy requests pillow`

### AI Generation Fails?
- Check internet connection
- Try again in a few minutes (API might be busy)

### Questions?
- Ask your teacher or classmates
- Check the game's help command: type 'help' during play

## 🎓 Learning Goals

By playing this game, you'll learn:
- How to write effective AI prompts
- How to analyze and describe images
- How AI image generation works
- Iterative improvement and problem-solving

## 🌟 Have Fun!

This game makes learning AI fun and interactive. Don't worry about getting perfect scores immediately - the learning happens through trying and improving!

**Good luck and enjoy the challenge!** 🚀
"""
    
    with open(f"{package_dir}/README_STUDENTS.md", "w") as f:
        f.write(readme_content)
    print("✅ Created: README_STUDENTS.md")
    
    # Create package info
    package_info = {
        "name": "AI Prompt Engineering Game - Student Edition",
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "description": "Educational game for learning AI prompt engineering",
        "requirements": "Python 3.8+, Internet connection",
        "students_supported": "Unlimited (uses free Pollinations.ai API)"
    }
    
    with open(f"{package_dir}/package_info.json", "w") as f:
        json.dump(package_info, f, indent=2)
    print("✅ Created: package_info.json")
    
    # Create ZIP distribution
    zip_filename = "AI_Prompt_Game_Student_Edition.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Created: {zip_filename}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📦 STUDENT PACKAGE CREATED!")
    print("=" * 50)
    print(f"📁 Package directory: {package_dir}/")
    print(f"📦 ZIP file: {zip_filename}")
    print("\n🎓 Distribution Instructions:")
    print("1. Share the ZIP file with students")
    print("2. Students extract and run: python install.py")
    print("3. Students can play immediately!")
    print("\n💡 Each student gets their own local installation")
    print("🌐 Uses free Pollinations.ai API (no server costs)")
    print("📈 Scales to unlimited students!")

if __name__ == "__main__":
    create_student_package()