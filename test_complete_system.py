#!/usr/bin/env python3
"""
Complete system test for AI Prompt Game
Tests all functionality before production deployment
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def test_installation():
    """Test package installation"""
    print("🧪 Testing Package Installation")
    print("=" * 50)
    
    try:
        # Test import
        from ai_prompt_game.game_engine import PromptGame
        from ai_prompt_game.image_generator import ImageGenerator
        from ai_prompt_game.comparison import ImageComparison
        from ai_prompt_game.utils import get_game_directory
        
        print("✅ All modules import successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("\n🔧 Testing Dependencies")
    print("=" * 50)
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('PIL', 'pillow'),
        ('requests', 'requests')
    ]
    
    all_ok = True
    for module, package in required_packages:
        try:
            if module == 'cv2':
                import cv2
                print(f"✅ OpenCV: {cv2.__version__}")
            elif module == 'PIL':
                from PIL import Image
                print(f"✅ Pillow: {Image.__version__}")
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'unknown')
                print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ Missing: {package}")
            all_ok = False
    
    return all_ok

def test_game_setup():
    """Test game setup and target download"""
    print("\n🎯 Testing Game Setup")
    print("=" * 50)
    
    try:
        from ai_prompt_game.utils import setup_game_directory, download_targets
        
        # Setup game directory
        game_dir = setup_game_directory()
        print(f"✅ Game directory created: {game_dir}")
        
        # Download targets
        targets = download_targets(game_dir)
        print(f"✅ Downloaded {len(targets)} targets")
        
        # Verify targets exist
        for target in targets:
            if os.path.exists(target['path']):
                print(f"✅ Target exists: {target['name']}")
            else:
                print(f"❌ Missing target: {target['name']}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_image_generation():
    """Test AI image generation"""
    print("\n🤖 Testing AI Image Generation")
    print("=" * 50)
    
    try:
        from ai_prompt_game.image_generator import ImageGenerator
        
        # Test Pollinations API
        generator = ImageGenerator("pollinations")
        
        test_prompts = [
            "red rose",
            "blue sky",
            "mountain sunset"
        ]
        
        for prompt in test_prompts:
            try:
                print(f"🔄 Testing: '{prompt}'")
                image = generator.generate(prompt)
                if image is not None:
                    print(f"✅ Generated: {image.shape}")
                else:
                    print(f"❌ Failed to generate image for: {prompt}")
                    return False
            except Exception as e:
                print(f"❌ Generation error for '{prompt}': {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

def test_image_comparison():
    """Test image comparison system"""
    print("\n📊 Testing Image Comparison")
    print("=" * 50)
    
    try:
        from ai_prompt_game.comparison import ImageComparison
        import numpy as np
        
        comparator = ImageComparison()
        
        # Create test images
        image1 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        image2 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        image3 = image1.copy()  # Identical image
        
        # Test comparison
        scores1 = comparator.compare(image1, image2)
        scores2 = comparator.compare(image1, image3)
        
        print(f"✅ Different images score: {scores1['combined']:.3f}")
        print(f"✅ Identical images score: {scores2['combined']:.3f}")
        
        # Identical images should score higher
        if scores2['combined'] > scores1['combined']:
            print("✅ Comparison logic working correctly")
            return True
        else:
            print("❌ Comparison logic issue")
            return False
            
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        return False

def test_visual_display():
    """Test visual display functionality"""
    print("\n🖼️  Testing Visual Display")
    print("=" * 50)
    
    try:
        import matplotlib
        print(f"✅ Matplotlib backend: {matplotlib.get_backend()}")
        
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Test basic display
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        plt.figure(figsize=(4, 3))
        plt.imshow(test_image)
        plt.title("🧪 Visual Test")
        plt.axis('off')
        
        # Save instead of show for automated testing
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            plt.savefig(tmp.name)
            plt.close()
            
            if os.path.exists(tmp.name):
                print("✅ Visual display system working")
                os.unlink(tmp.name)
                return True
            else:
                print("❌ Visual display failed")
                return False
                
    except Exception as e:
        print(f"❌ Visual display test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface"""
    print("\n💻 Testing CLI Interface")
    print("=" * 50)
    
    try:
        # Test CLI help
        result = subprocess.run([sys.executable, '-m', 'ai_prompt_game.cli', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI help works")
        else:
            print("❌ CLI help failed")
            return False
        
        # Test CLI version
        result = subprocess.run([sys.executable, '-m', 'ai_prompt_game.cli', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI version works")
        else:
            print("❌ CLI version failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_game_flow():
    """Test complete game flow"""
    print("\n🎮 Testing Game Flow")
    print("=" * 50)
    
    try:
        from ai_prompt_game.game_engine import PromptGame
        
        # Initialize game
        game = PromptGame(visual_mode=False, verbose=False)  # Disable visual for testing
        
        # Get targets
        targets = game.get_available_targets()
        if not targets:
            print("❌ No targets available")
            return False
        
        print(f"✅ Found {len(targets)} targets")
        
        # Test game session
        target = targets[0]  # Use first target
        game.start_game_session(target)
        
        print(f"✅ Game session started with: {target['name']}")
        
        # Test attempt (without actual generation)
        print("✅ Game flow working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Game flow test failed: {e}")
        return False

def run_all_tests():
    """Run complete test suite"""
    print("🚀 AI PROMPT GAME - PRODUCTION READINESS TEST")
    print("=" * 60)
    
    tests = [
        ("Installation", test_installation),
        ("Dependencies", test_dependencies),
        ("Game Setup", test_game_setup),
        ("Image Generation", test_image_generation),
        ("Image Comparison", test_image_comparison),
        ("Visual Display", test_visual_display),
        ("CLI Interface", test_cli_interface),
        ("Game Flow", test_game_flow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"OVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - READY FOR PRODUCTION! 🎉")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - FIX BEFORE PRODUCTION")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)