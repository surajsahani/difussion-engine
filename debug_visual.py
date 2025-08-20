#!/usr/bin/env python3
"""
Debug visual display issues
"""

def test_matplotlib():
    """Test if matplotlib can display images"""
    print("🧪 Testing Matplotlib Display")
    print("=" * 40)
    
    try:
        import matplotlib
        print(f"✅ Matplotlib version: {matplotlib.__version__}")
        
        # Check backend
        print(f"✅ Backend: {matplotlib.get_backend()}")
        
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create simple test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        plt.figure(figsize=(6, 4))
        plt.imshow(test_image)
        plt.title("🧪 Test Image - Should Pop Up!")
        plt.axis('off')
        
        print("🖼️  Attempting to show test image...")
        plt.show()  # This should create a popup
        
        print("✅ If you saw a popup window, matplotlib is working!")
        return True
        
    except Exception as e:
        print(f"❌ Matplotlib test failed: {e}")
        return False

def test_game_visual_mode():
    """Test if the game's visual mode is enabled"""
    print("\n🎮 Testing Game Visual Mode")
    print("=" * 40)
    
    try:
        from ai_prompt_game.game_engine import PromptGame, DISPLAY_AVAILABLE
        
        print(f"DISPLAY_AVAILABLE: {DISPLAY_AVAILABLE}")
        
        # Create game instance
        game = PromptGame(visual_mode=True, verbose=True)
        print(f"Game visual_mode: {game.visual_mode}")
        
        # Test target loading
        targets = game.get_available_targets()
        if targets:
            target = targets[0]  # Mountain Sunset
            print(f"Testing with target: {target['name']}")
            
            # Try to load target image
            from ai_prompt_game.utils import load_target_image
            target_image = load_target_image(target['path'])
            
            if target_image is not None:
                print(f"✅ Target image loaded: {target_image.shape}")
                
                # Test display method directly
                game.current_target = target
                print("🖼️  Calling display_target_image()...")
                game.display_target_image()
                
            else:
                print("❌ Could not load target image")
        else:
            print("❌ No targets available")
            
        return True
        
    except Exception as e:
        print(f"❌ Game test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Visual Display Debug Tool")
    print("=" * 50)
    
    # Test matplotlib first
    matplotlib_ok = test_matplotlib()
    
    # Test game visual mode
    game_ok = test_game_visual_mode()
    
    print("\n" + "=" * 50)
    print("📊 DEBUG RESULTS:")
    print(f"   Matplotlib: {'✅ OK' if matplotlib_ok else '❌ FAIL'}")
    print(f"   Game Visual: {'✅ OK' if game_ok else '❌ FAIL'}")
    
    if not matplotlib_ok:
        print("\n💡 Matplotlib issues - try:")
        print("   pip install matplotlib")
        print("   # Or check if you're in a headless environment")
    
    if not game_ok:
        print("\n💡 Game visual issues - check target images exist")
        print("   ai-prompt-game --setup")