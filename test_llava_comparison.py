#!/usr/bin/env python3
"""
Test LLaVA-enhanced image comparison
"""

import cv2
import numpy as np
from ai_prompt_game.comparison import ImageComparison

def create_test_images():
    """Create simple test images for comparison"""
    # Create target image (blue sky with white cloud)
    target = np.ones((256, 256, 3), dtype=np.uint8)
    target[:, :] = [200, 150, 100]  # Blue sky
    cv2.circle(target, (128, 80), 40, (255, 255, 255), -1)  # White cloud
    
    # Create similar image (blue sky with white cloud, slightly different)
    similar = np.ones((256, 256, 3), dtype=np.uint8)
    similar[:, :] = [190, 140, 110]  # Slightly different blue
    cv2.circle(similar, (120, 85), 35, (250, 250, 250), -1)  # Slightly different cloud
    
    # Create different image (red sunset)
    different = np.ones((256, 256, 3), dtype=np.uint8)
    different[:, :] = [50, 100, 200]  # Red/orange
    cv2.circle(different, (200, 200), 30, (100, 200, 255), -1)  # Yellow sun
    
    return target, similar, different

def test_llava_comparison():
    """Test LLaVA-enhanced comparison"""
    print("🧪 Testing LLaVA-Enhanced Image Comparison")
    print("=" * 50)
    
    # Create test images
    target, similar, different = create_test_images()
    
    # Save test images for visual inspection
    cv2.imwrite("test_target.jpg", target)
    cv2.imwrite("test_similar.jpg", similar)
    cv2.imwrite("test_different.jpg", different)
    
    print("📁 Test images saved: test_target.jpg, test_similar.jpg, test_different.jpg")
    
    # Test with LLaVA enabled
    print("\n🤖 Testing with LLaVA enabled...")
    comparator_llava = ImageComparison(use_llava=True)
    
    if comparator_llava.llava_available:
        print("✅ LLaVA successfully loaded!")
        
        # Test similar images
        print("\n📊 Comparing SIMILAR images:")
        scores_similar = comparator_llava.compare(similar, target)
        print(f"   Combined Score: {scores_similar['combined']:.3f}")
        print(f"   LLaVA Semantic: {scores_similar.get('llava_semantic', 'N/A'):.3f}")
        print(f"   AI Explanation: {scores_similar.get('llava_explanation', 'N/A')}")
        
        # Test different images
        print("\n📊 Comparing DIFFERENT images:")
        scores_different = comparator_llava.compare(different, target)
        print(f"   Combined Score: {scores_different['combined']:.3f}")
        print(f"   LLaVA Semantic: {scores_different.get('llava_semantic', 'N/A'):.3f}")
        print(f"   AI Explanation: {scores_different.get('llava_explanation', 'N/A')}")
        
    else:
        print("⚠️  LLaVA not available, testing fallback...")
        
        # Test fallback mode
        scores_similar = comparator_llava.compare(similar, target)
        print(f"\n📊 Fallback comparison (similar): {scores_similar['combined']:.3f}")
        
        scores_different = comparator_llava.compare(different, target)
        print(f"📊 Fallback comparison (different): {scores_different['combined']:.3f}")
    
    # Test traditional comparison for baseline
    print("\n🔧 Testing traditional comparison (baseline):")
    comparator_traditional = ImageComparison(use_llava=False)
    
    scores_trad_similar = comparator_traditional.compare(similar, target)
    scores_trad_different = comparator_traditional.compare(different, target)
    
    print(f"   Traditional similar: {scores_trad_similar['combined']:.3f}")
    print(f"   Traditional different: {scores_trad_different['combined']:.3f}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 COMPARISON SUMMARY:")
    
    if comparator_llava.llava_available:
        print("✅ LLaVA Enhancement: ACTIVE")
        print(f"   Similar images: {scores_similar['combined']:.3f} (LLaVA) vs {scores_trad_similar['combined']:.3f} (Traditional)")
        print(f"   Different images: {scores_different['combined']:.3f} (LLaVA) vs {scores_trad_different['combined']:.3f} (Traditional)")
    else:
        print("⚠️  LLaVA Enhancement: NOT AVAILABLE")
        print("💡 To enable LLaVA:")
        print("   pip install transformers torch torchvision")
        print("   # Note: LLaVA models are large (~13GB)")

def test_installation():
    """Test if LLaVA dependencies are available"""
    print("🔍 Checking LLaVA Dependencies")
    print("=" * 40)
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not installed")
        return False
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    try:
        from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
        print("✅ LLaVA components available")
        return True
    except ImportError:
        print("❌ LLaVA components not available")
        return False

if __name__ == "__main__":
    print("🤖 LLaVA Image Comparison Test")
    print("=" * 50)
    
    # Test installation first
    deps_ok = test_installation()
    
    print("\n" + "=" * 50)
    
    if deps_ok:
        test_llava_comparison()
    else:
        print("⚠️  Dependencies missing. Install with:")
        print("pip install transformers torch torchvision")
        print("\n💡 Note: LLaVA models are large and will download ~13GB on first use")
        
        # Still test traditional comparison
        print("\n🔧 Testing traditional comparison only...")
        target, similar, different = create_test_images()
        comparator = ImageComparison(use_llava=False)
        
        scores_similar = comparator.compare(similar, target)
        scores_different = comparator.compare(different, target)
        
        print(f"Traditional similar: {scores_similar['combined']:.3f}")
        print(f"Traditional different: {scores_different['combined']:.3f}")