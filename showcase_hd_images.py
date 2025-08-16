#!/usr/bin/env python3
"""
Showcase script for the improved diffusion engine with HD, child-friendly images
"""

import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from proper_visual_game import ProperVisualGame
import numpy as np

def create_showcase():
    """Create a showcase of the new HD, child-friendly images"""
    print("🎨 Creating HD Child-Friendly Image Showcase...")
    
    # Create multiple target images to show variety
    target_images = []
    descriptions = []
    
    for i in range(6):
        game = ProperVisualGame()
        target_images.append(game.target_image)
        # Determine what type of image was created
        descriptions.append(f"HD Target Image #{i+1}")
    
    # Create a grid display
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("High Definition Child-Friendly Learning Images\n(1024x1024 resolution, high contrast)", 
                 fontsize=16, fontweight='bold')
    
    for i, (ax, img, desc) in enumerate(zip(axes.flat, target_images, descriptions)):
        # Convert BGR to RGB for matplotlib
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(img_rgb)
        ax.set_title(desc, fontsize=12, fontweight='bold')
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('HD_ChildFriendly_Showcase.png', dpi=150, bbox_inches='tight')
    print("✅ Showcase saved as HD_ChildFriendly_Showcase.png")
    
    # Also test some prompt examples
    print("\n🔄 Testing child-friendly prompt generation...")
    
    game = ProperVisualGame()
    test_prompts = [
        "bright red house with blue roof and yellow door",
        "colorful rainbow with white clouds",
        "cute orange cat with green eyes",
        "simple flower with pink petals and yellow center",
        "red car with round black wheels",
        "blue circle and red square shapes"
    ]
    
    generated_images = []
    for prompt in test_prompts:
        result = game.engine(prompt)
        generated_images.append(result)
        print(f"  ✓ Generated image for: '{prompt}'")
    
    # Create another showcase for generated images
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("AI Generated HD Images from Child-Friendly Prompts\n(Educational prompt engineering examples)", 
                 fontsize=16, fontweight='bold')
    
    for i, (ax, img, prompt) in enumerate(zip(axes.flat, generated_images, test_prompts)):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(img_rgb)
        # Wrap long prompts
        wrapped_prompt = prompt if len(prompt) <= 40 else prompt[:37] + "..."
        ax.set_title(f'"{wrapped_prompt}"', fontsize=10, fontweight='bold')
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('HD_Generated_Examples.png', dpi=150, bbox_inches='tight')
    print("✅ Generated examples saved as HD_Generated_Examples.png")
    
    # Create a comparison image showing old vs new
    print("\n📊 Creating comparison with old system...")
    
    # Create old-style image (512x512, complex scene)
    old_image = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Old sunset scene
    for y in range(512 // 2):
        intensity = 1.0 - (y / (512 // 2))
        old_image[y, :, 0] = int(255 * intensity * 0.9)
        old_image[y, :, 1] = int(255 * intensity * 0.7)
        old_image[y, :, 2] = int(255 * intensity * 0.3)
    
    old_image[256:, :, 2] = 120
    old_image[256:, :, 1] = 80
    old_image[256:, :, 0] = 40
    
    cv2.circle(old_image, (400, 120), 45, (255, 255, 200), -1)
    
    for x in range(512):
        mountain_height = int(512 * 0.2 * (0.5 + 0.5 * np.sin(x * 0.008)))
        y_start = 256 - mountain_height
        old_image[y_start:256, x] = [50, 50, 50]
    
    # Get a new HD image
    new_game = ProperVisualGame()
    new_image = new_game.target_image
    
    # Resize old image to match new for comparison
    old_image_resized = cv2.resize(old_image, (1024, 1024))
    
    # Create comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    ax1.imshow(cv2.cvtColor(old_image_resized, cv2.COLOR_BGR2RGB))
    ax1.set_title("Old System:\nComplex, Low Contrast\n(Not suitable for young learners)", 
                  fontsize=14, fontweight='bold', color='red')
    ax1.axis('off')
    
    ax2.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
    ax2.set_title("New System:\nSimple, High Contrast, Child-Friendly\n(Perfect for 5-year-olds)", 
                  fontsize=14, fontweight='bold', color='green')
    ax2.axis('off')
    
    plt.suptitle("Educational Image Generation: Before vs After Improvement", 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('Before_After_Comparison.png', dpi=150, bbox_inches='tight')
    print("✅ Comparison saved as Before_After_Comparison.png")
    
    print("\n🎯 Showcase complete! Educational benefits:")
    print("   ✓ High Definition: 1024x1024 (vs 512x512)")
    print("   ✓ High Contrast: Clear, distinct colors")
    print("   ✓ Child-Friendly: Simple shapes and objects")
    print("   ✓ Educational: Perfect for learning prompt engineering")
    print("   ✓ Age-Appropriate: Suitable for 5-year-old students")

if __name__ == "__main__":
    create_showcase()