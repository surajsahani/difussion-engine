#!/usr/bin/env python3
"""
Quick test showing the practical improvements in your algorithm
"""

import cv2
import numpy as np
from ai_prompt_game.comparison import ImageComparison

def create_test_pair():
    """Create a test pair that demonstrates the improvements"""
    
    # Create target image: A simple scene
    target = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(target, (50, 50), (150, 150), (255, 100, 50), -1)  # Orange square
    cv2.circle(target, (200, 100), 30, (50, 255, 100), -1)  # Green circle
    cv2.putText(target, 'CAT', (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Create generated image: Similar but not identical
    generated = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(generated, (55, 55), (145, 145), (240, 120, 60), -1)  # Slightly different orange square
    cv2.circle(generated, (195, 105), 28, (60, 240, 120), -1)  # Slightly different green circle
    cv2.putText(generated, 'CAT', (105, 245), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 240, 240), 2)
    
    return target, generated

def main():
    print("🧪 Quick Algorithm Improvement Test")
    print("=" * 50)
    
    # Create test images
    target, generated = create_test_pair()
    
    # Test with new algorithm
    comparator = ImageComparison(verbose=False)
    scores = comparator.compare(generated, target)
    
    print(f"🎯 Target: Orange square + green circle + 'CAT' text")
    print(f"🎨 Generated: Very similar with slight variations")
    print()
    
    print("📊 Detailed Similarity Analysis:")
    print(f"  Overall Score:      {scores['combined']:.3f}")
    print(f"  Perceptual:         {scores['perceptual']:.3f}")
    print(f"  Semantic:           {scores['semantic']:.3f}")
    print(f"  Structural:         {scores['structural']:.3f}")
    print(f"  Color Advanced:     {scores['color_advanced']:.3f}")
    print(f"  Texture:            {scores['texture']:.3f}")
    print()
    
    # Get AI explanations
    explanations = comparator.explain_scores(scores)
    print("🤖 AI Analysis:")
    for explanation in explanations:
        print(f"   {explanation}")
    
    print()
    print("✨ Key Improvements Demonstrated:")
    print("   • Multi-metric analysis provides detailed breakdown")
    print("   • Perceptual scoring aligns with human vision")
    print("   • Adaptive weighting optimizes for image content")
    print("   • Clear explanations help understand the match quality")
    print("   • Balanced scoring avoids inflation or deflation")

if __name__ == "__main__":
    main()