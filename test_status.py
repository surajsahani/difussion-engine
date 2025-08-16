#!/usr/bin/env python3
"""
Test Status Checker - Verifies what's working and what needs setup
"""

import os
import sys
import json

def check_basic_functionality():
    """Test the basic game logic"""
    print("🔍 Testing Basic Game Logic...")
    
    try:
        # Import and run basic test
        from basic_test import BasicPromptGame
        
        game = BasicPromptGame()
        result = game.make_attempt("test prompt")
        
        if result and 'score' in result:
            print("✅ Basic game logic works!")
            return True
        else:
            print("❌ Basic game logic failed")
            return False
            
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking Files...")
    
    required_files = [
        'stable_difussion_engine.py',
        'prompt_guessing_game.py', 
        'play_game.py',
        'basic_test.py',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check which dependencies are available"""
    print("\n📦 Checking Dependencies...")
    
    dependencies = {
        'numpy': 'Core numerical operations',
        'cv2': 'Image processing (opencv-python)',
        'sklearn': 'Machine learning utilities (scikit-learn)',
        'skimage': 'Image processing (scikit-image)',
        'transformers': 'Hugging Face transformers',
        'diffusers': 'Diffusion models',
        'openvino': 'Intel OpenVINO runtime'
    }
    
    available = []
    missing = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep} - {description}")
            available.append(dep)
        except ImportError:
            print(f"❌ {dep} - {description} (Not installed)")
            missing.append(dep)
    
    return available, missing

def check_session_files():
    """Check if test sessions were created"""
    print("\n💾 Checking Session Files...")
    
    session_files = [
        'basic_test_session.json',
        'test_session.json',
        'game_session.json'
    ]
    
    found_sessions = []
    for file in session_files:
        if os.path.exists(file):
            print(f"✅ {file}")
            found_sessions.append(file)
        else:
            print(f"⚪ {file} - Not created yet")
    
    return found_sessions

def show_next_steps(available_deps, missing_deps):
    """Show what to do next based on current status"""
    print("\n🚀 Next Steps:")
    
    if len(missing_deps) == 0:
        print("🎉 All dependencies available! You can run the full game:")
        print("   python3 play_game.py target_image.jpg")
    elif 'numpy' not in available_deps:
        print("📦 Install basic dependencies first:")
        print("   pip3 install --user numpy opencv-python scikit-learn scikit-image")
        print("   (or use a virtual environment)")
    else:
        print("🔧 For full functionality, install remaining dependencies:")
        print("   pip3 install -r requirements.txt")
        print("   (or use a virtual environment)")
    
    print("\n🎯 Current Testing Options:")
    print("1. ✅ Basic Logic Test: python3 basic_test.py")
    print("2. 🔄 Simple Mock Test: python3 simple_test.py (needs numpy)")
    print("3. 🎮 Full Game: python3 play_game.py image.jpg (needs all deps)")
    
    print("\n💡 Recommended Testing Order:")
    print("1. Run basic_test.py to verify game logic")
    print("2. Install dependencies gradually")
    print("3. Test with real Stable Diffusion model")
    print("4. Add your own target images")

def main():
    """Main test status check"""
    print("🎯 Reverse Prompt Engineering Game - Status Check")
    print("=" * 60)
    
    # Check basic functionality
    basic_works = check_basic_functionality()
    
    # Check files
    files_ok = check_files()
    
    # Check dependencies
    available_deps, missing_deps = check_dependencies()
    
    # Check session files
    sessions = check_session_files()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"✅ Basic Logic: {'Working' if basic_works else 'Failed'}")
    print(f"📁 Required Files: {'All present' if files_ok else 'Some missing'}")
    print(f"📦 Dependencies: {len(available_deps)}/{len(available_deps) + len(missing_deps)} available")
    print(f"💾 Test Sessions: {len(sessions)} created")
    
    # Show next steps
    show_next_steps(available_deps, missing_deps)
    
    print("\n🎓 Educational Use:")
    print("- Students can start with basic_test.py to learn prompt engineering")
    print("- Gradually move to full image generation as dependencies are installed")
    print("- Game tracks progress and provides educational feedback")

if __name__ == "__main__":
    main()