#!/usr/bin/env python3
"""
Test script for the advanced image comparison algorithm
Demonstrates improvements in discrimination and accuracy
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from ai_prompt_game.comparison import ImageComparison
import os

def create_test_images():
    """Create test images with known similarity levels"""
    
    # Create base image (512x512, colorful scene)
    base = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Add colorful geometric shapes
    cv2.rectangle(base, (100, 100), (200, 200), (255, 100, 50), -1)  # Orange rectangle
    cv2.circle(base, (350, 150), 80, (50, 255, 100), -1)  # Green circle
    cv2.ellipse(base, (250, 350), (120, 60), 45, 0, 360, (100, 50, 255), -1)  # Purple ellipse
    
    # Add some texture
    noise = np.random.randint(0, 50, (512, 512, 3), dtype=np.uint8)
    base = cv2.addWeighted(base, 0.8, noise, 0.2, 0)
    
    test_images = {
        'original': base.copy(),
        'very_similar': None,
        'somewhat_similar': None,
        'different_colors': None,
        'different_shapes': None,
        'completely_different': None
    }
    
    # Very similar (slight color shift)
    very_similar = base.copy()
    very_similar[:,:,0] = np.clip(very_similar[:,:,0] * 1.1, 0, 255)  # Slight blue shift
    test_images['very_similar'] = very_similar
    
    # Somewhat similar (same shapes, different colors)
    somewhat_similar = base.copy()
    # Shift all colors
    hsv = cv2.cvtColor(somewhat_similar, cv2.COLOR_BGR2HSV)
    hsv[:,:,0] = (hsv[:,:,0] + 30) % 180  # Hue shift
    test_images['somewhat_similar'] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Different colors (same shapes, completely different palette)
    different_colors = np.zeros((512, 512, 3), dtype=np.uint8)
    cv2.rectangle(different_colors, (100, 100), (200, 200), (0, 255, 255), -1)  # Cyan
    cv2.circle(different_colors, (350, 150), 80, (255, 0, 255), -1)  # Magenta
    cv2.ellipse(different_colors, (250, 350), (120, 60), 45, 0, 360, (255, 255, 0), -1)  # Yellow
    test_images['different_colors'] = different_colors
    
    # Different shapes (same colors, different geometry)
    different_shapes = base.copy()
    different_shapes.fill(0)
    pts = np.array([[150, 50], [250, 50], [200, 150]], np.int32)
    cv2.fillPoly(different_shapes, [pts], (255, 100, 50))
    cv2.rectangle(different_shapes, (300, 100), (400, 250), (50, 255, 100), -1)
    cv2.circle(different_shapes, (200, 400), 100, (100, 50, 255), -1)
    test_images['different_shapes'] = different_shapes
    
    # Completely different (text)
    completely_different = np.ones((512, 512, 3), dtype=np.uint8) * 255
    cv2.putText(completely_different, 'HELLO', (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 8)
    cv2.putText(completely_different, 'WORLD', (150, 350), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 8)
    test_images['completely_different'] = completely_different
    
    return test_images

def test_comparison_algorithm():
    """Test the advanced comparison algorithm"""
    
    print("🧪 Testing Advanced Image Comparison Algorithm")
    print("=" * 60)
    
    # Create test images
    test_images = create_test_images()
    
    # Initialize comparison (with verbose output)
    comparator = ImageComparison(verbose=True)
    
    # Test against original
    original = test_images['original']
    results = {}
    
    for name, image in test_images.items():
        if name == 'original':
            continue
            
        print(f"\n🔍 Comparing with {name.replace('_', ' ').title()}:")
        print("-" * 40)
        
        # Get similarity scores
        scores = comparator.compare(image, original)
        results[name] = scores
        
        # Print detailed scores
        print(f"Combined Score: {scores['combined']:.3f}")
        print(f"Perceptual:     {scores['perceptual']:.3f}")
        print(f"Semantic:       {scores['semantic']:.3f}")
        print(f"Structural:     {scores['structural']:.3f}")
        print(f"Color Advanced: {scores['color_advanced']:.3f}")
        print(f"Texture:        {scores['texture']:.3f}")
        
        # Get explanations
        explanations = comparator.explain_scores(scores)
        print("\n📝 Analysis:")
        for explanation in explanations:
            print(f"   {explanation}")
    
    # Summary comparison
    print("\n" + "=" * 60)
    print("📊 SUMMARY COMPARISON")
    print("=" * 60)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['combined'], reverse=True)
    
    print(f"{'Comparison':<20} {'Score':<8} {'Expected':<12} {'✓/✗'}")
    print("-" * 50)
    
    expected_order = ['very_similar', 'somewhat_similar', 'different_colors', 'different_shapes', 'completely_different']
    expected_ranges = {
        'very_similar': (0.8, 1.0),
        'somewhat_similar': (0.6, 0.8),
        'different_colors': (0.4, 0.7),
        'different_shapes': (0.3, 0.6),
        'completely_different': (0.0, 0.4)
    }
    
    for name, scores in sorted_results:
        score = scores['combined']
        expected_min, expected_max = expected_ranges[name]
        is_correct = expected_min <= score <= expected_max
        status = "✅" if is_correct else "❌"
        
        print(f"{name.replace('_', ' '):<20} {score:<8.3f} {expected_min:.1f}-{expected_max:.1f}      {status}")
    
    # Check if ordering is correct
    actual_order = [name for name, _ in sorted_results]
    order_correct = actual_order == expected_order
    
    print(f"\n🎯 Ranking Order: {'✅ Correct' if order_correct else '❌ Incorrect'}")
    print(f"Expected: {' > '.join(expected_order)}")
    print(f"Actual:   {' > '.join(actual_order)}")
    
    return results, test_images

def visualize_results(results, test_images):
    """Create visualization of test results"""
    
    print("\n🎨 Creating visualization...")
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Advanced Image Comparison Test Results', fontsize=16, fontweight='bold')
    
    # Plot images and scores
    images_to_plot = ['original', 'very_similar', 'somewhat_similar', 'different_colors', 'different_shapes', 'completely_different']
    
    for i, name in enumerate(images_to_plot):
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        
        # Convert BGR to RGB for matplotlib
        image_rgb = cv2.cvtColor(test_images[name], cv2.COLOR_BGR2RGB)
        ax.imshow(image_rgb)
        
        if name == 'original':
            title = 'Original (Reference)'
        else:
            score = results[name]['combined']
            title = f'{name.replace("_", " ").title()}\nScore: {score:.3f}'
        
        ax.set_title(title, fontweight='bold')
        ax.axis('off')
    
    plt.tight_layout()
    
    # Save visualization
    os.makedirs('test_results', exist_ok=True)
    plt.savefig('test_results/advanced_comparison_test.png', dpi=150, bbox_inches='tight')
    print("💾 Visualization saved to: test_results/advanced_comparison_test.png")
    
    # Show if possible
    try:
        plt.show()
    except:
        print("📱 Display not available, but image saved successfully")

def benchmark_performance():
    """Benchmark the performance of the new algorithm"""
    
    print("\n⚡ Performance Benchmark")
    print("=" * 40)
    
    import time
    
    # Create test images
    test_images = create_test_images()
    comparator = ImageComparison(verbose=False)
    
    original = test_images['original']
    test_image = test_images['somewhat_similar']
    
    # Warm up
    for _ in range(3):
        comparator.compare(test_image, original)
    
    # Benchmark
    num_runs = 10
    start_time = time.time()
    
    for _ in range(num_runs):
        scores = comparator.compare(test_image, original)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / num_runs
    
    print(f"Average comparison time: {avg_time:.3f} seconds")
    print(f"Comparisons per second: {1/avg_time:.1f}")
    
    # Memory usage estimate
    import sys
    image_size_mb = (original.nbytes + test_image.nbytes) / (1024 * 1024)
    print(f"Memory per comparison: ~{image_size_mb:.1f} MB")

if __name__ == "__main__":
    try:
        # Run comprehensive test
        results, test_images = test_comparison_algorithm()
        
        # Create visualization
        visualize_results(results, test_images)
        
        # Performance benchmark
        benchmark_performance()
        
        print("\n🎉 Advanced comparison algorithm test completed successfully!")
        print("🔍 Check the detailed scores above to see the improvements")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()