#!/usr/bin/env python3
"""
Test script to verify visual display functionality works
"""

import sys
import os

def test_visual_display():
    """Test if visual display works"""
    print("🧪 Testing Visual Display Functionality")
    print("=" * 50)
    
    # Test matplotlib import and backend
    try:
        import matplotlib
        print(f"✅ Matplotlib version: {matplotlib.__version__}")
        
        # Try different backends like the game does
        backends_to_try = ['MacOSX', 'TkAgg', 'Qt5Agg', 'Agg']
        
        backend_set = False
        for backend in backends_to_try:
            try:
                matplotlib.use(backend)
                print(f"✅ Using {backend} backend")
                backend_set = True
                break
            except Exception as e:
                print(f"⚠️  {backend} backend failed: {e}")
                continue
        
        if not backend_set:
            print("⚠️  Using default backend")
        
        import matplotlib.pyplot as plt
        print("✅ Matplotlib pyplot imported")
        
    except ImportError as e:
        print(f"❌ Matplotlib import failed: {e}")
        return False
    
    # Test image creation and display
    try:
        import numpy as np
        
        # Create test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        plt.figure(figsize=(6, 4))
        plt.imshow(test_image)
        plt.title("🧪 Test Image Display")
        plt.axis('off')
        
        print("🖼️  Attempting to display test image...")
        plt.show(block=False)
        plt.pause(1)  # Show for 1 second
        plt.close()
        
        print("✅ Matplotlib display test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Matplotlib display test failed: {e}")
        print("💡 Will try system viewer fallback in game")
        return False

def test_game_import():
    """Test if the game can be imported"""
    try:
        from ai_prompt_game.game_engine import PromptGame
        print("✅ Game engine import successful")
        
        # Test initialization
        game = PromptGame(visual_mode=True, verbose=True)
        print("✅ Game initialization successful")
        print(f"✅ Visual mode: {game.visual_mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Game import failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 AI Prompt Game - Visual Display Test")
    print("=" * 50)
    
    # Test visual display
    visual_ok = test_visual_display()
    
    print("\n" + "=" * 50)
    
    # Test game import
    game_ok = test_game_import()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   Visual Display: {'✅ PASS' if visual_ok else '❌ FAIL'}")
    print(f"   Game Import: {'✅ PASS' if game_ok else '❌ FAIL'}")
    
    if visual_ok and game_ok:
        print("\n🎉 All tests passed! Visual mode should work.")
        print("\n🚀 Try running: ai-prompt-game --setup")
    else:
        print("\n⚠️  Some tests failed. Visual mode may not work properly.")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install matplotlib pillow")