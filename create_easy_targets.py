#!/usr/bin/env python3
"""
Create very simple target images for easy prompt generation
These are designed to be super easy to guess and generate
"""

import cv2
import numpy as np
import os

def create_simple_targets():
    """Create simple, easy-to-generate target images"""
    
    os.makedirs("easy_targets", exist_ok=True)
    
    targets = []
    
    # 1. Simple Red Rose (very easy)
    print("🌹 Creating Red Rose target...")
    rose_img = np.ones((512, 512, 3), dtype=np.uint8) * 255  # White background
    
    # Draw simple rose shape
    center = (256, 256)
    # Rose petals (red circles)
    cv2.circle(rose_img, center, 80, (50, 50, 200), -1)  # Red in BGR
    cv2.circle(rose_img, (center[0]-20, center[1]-20), 60, (40, 40, 180), -1)
    cv2.circle(rose_img, (center[0]+20, center[1]-20), 60, (40, 40, 180), -1)
    cv2.circle(rose_img, (center[0], center[1]+30), 50, (60, 60, 220), -1)
    
    # Simple stem
    cv2.rectangle(rose_img, (250, 336), (262, 450), (50, 150, 50), -1)  # Green stem
    
    cv2.imwrite("easy_targets/red_rose.jpg", rose_img)
    
    targets.append({
        "name": "Red Rose",
        "difficulty": "Beginner",
        "description": "A simple red rose on white background",
        "path": "easy_targets/red_rose.jpg",
        "example_prompts": ["red rose", "red rose on white background", "single red rose flower"],
        "hints": ["Just say 'red rose'", "Add 'white background'", "Keep it simple"]
    })
    
    # 2. Blue Sky with Clouds (very easy)
    print("☁️ Creating Blue Sky target...")
    sky_img = np.ones((512, 512, 3), dtype=np.uint8)
    
    # Blue sky gradient
    for y in range(512):
        intensity = 1.0 - (y / 512) * 0.3
        sky_img[y, :] = [200 * intensity, 150 * intensity, 100]  # Blue gradient
    
    # Simple white clouds
    cv2.ellipse(sky_img, (150, 100), (80, 40), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(sky_img, (350, 80), (60, 30), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(sky_img, (400, 150), (70, 35), 0, 0, 360, (255, 255, 255), -1)
    
    cv2.imwrite("easy_targets/blue_sky.jpg", sky_img)
    
    targets.append({
        "name": "Blue Sky with Clouds",
        "difficulty": "Beginner",
        "description": "Clear blue sky with white fluffy clouds",
        "path": "easy_targets/blue_sky.jpg",
        "example_prompts": ["blue sky with white clouds", "clear blue sky", "sunny day with clouds"],
        "hints": ["Say 'blue sky with clouds'", "Add 'clear day'", "Keep it simple"]
    })
    
    # 3. Green Grass Field (very easy)
    print("🌱 Creating Green Grass target...")
    grass_img = np.ones((512, 512, 3), dtype=np.uint8)
    
    # Blue sky top half
    grass_img[:256, :] = [200, 150, 100]  # Blue sky
    
    # Green grass bottom half
    grass_img[256:, :] = [50, 150, 50]  # Green grass
    
    # Add some texture to grass
    for _ in range(1000):
        x = np.random.randint(0, 512)
        y = np.random.randint(256, 512)
        grass_img[y, x] = [40 + np.random.randint(0, 30), 
                          140 + np.random.randint(0, 30), 
                          40 + np.random.randint(0, 30)]
    
    cv2.imwrite("easy_targets/green_grass.jpg", grass_img)
    
    targets.append({
        "name": "Green Grass Field",
        "difficulty": "Beginner", 
        "description": "Simple green grass field under blue sky",
        "path": "easy_targets/green_grass.jpg",
        "example_prompts": ["green grass field", "green meadow under blue sky", "grassy field"],
        "hints": ["Say 'green grass field'", "Add 'blue sky'", "Very straightforward"]
    })
    
    # 4. Simple Orange Cat (easy)
    print("🐱 Creating Orange Cat target...")
    cat_img = np.ones((512, 512, 3), dtype=np.uint8) * 240  # Light background
    
    # Cat body (orange oval)
    cv2.ellipse(cat_img, (256, 350), (100, 80), 0, 0, 360, (50, 100, 200), -1)  # Orange body
    
    # Cat head (orange circle)
    cv2.circle(cat_img, (256, 220), 70, (50, 100, 200), -1)  # Orange head
    
    # Cat ears (triangles)
    pts1 = np.array([[220, 180], [240, 140], [260, 180]], np.int32)
    pts2 = np.array([[252, 180], [272, 140], [292, 180]], np.int32)
    cv2.fillPoly(cat_img, [pts1], (40, 90, 180))
    cv2.fillPoly(cat_img, [pts2], (40, 90, 180))
    
    # Cat eyes (black dots)
    cv2.circle(cat_img, (235, 210), 8, (0, 0, 0), -1)
    cv2.circle(cat_img, (277, 210), 8, (0, 0, 0), -1)
    
    # Cat nose (pink triangle)
    nose_pts = np.array([[256, 225], [250, 235], [262, 235]], np.int32)
    cv2.fillPoly(cat_img, [nose_pts], (150, 100, 200))
    
    # Cat stripes (darker orange)
    for i in range(5):
        y = 180 + i * 30
        cv2.ellipse(cat_img, (256, y), (80, 8), 0, 0, 360, (30, 70, 150), -1)
    
    cv2.imwrite("easy_targets/orange_cat.jpg", cat_img)
    
    targets.append({
        "name": "Orange Cat",
        "difficulty": "Easy",
        "description": "Cute orange tabby cat sitting",
        "path": "easy_targets/orange_cat.jpg", 
        "example_prompts": ["orange tabby cat sitting", "cute ginger cat", "fluffy orange cat"],
        "hints": ["Say 'orange cat' or 'ginger cat'", "Add 'sitting'", "Mention 'cute' or 'fluffy'"]
    })
    
    print(f"\n✅ Created {len(targets)} easy target images!")
    print("📁 Saved to: easy_targets/")
    
    # Save metadata
    import json
    with open("easy_targets/targets.json", "w") as f:
        json.dump(targets, f, indent=2)
    
    print("💾 Target metadata saved to: easy_targets/targets.json")
    
    return targets

def show_targets_info(targets):
    """Show information about created targets"""
    print("\n🎯 EASY TARGETS CREATED:")
    print("=" * 50)
    
    for i, target in enumerate(targets, 1):
        print(f"{i}. {target['name']} ({target['difficulty']})")
        print(f"   📝 {target['description']}")
        print(f"   💡 Try: '{target['example_prompts'][0]}'")
        print()

if __name__ == "__main__":
    print("🎨 Creating Easy Target Images for AI Prompt Game")
    print("=" * 60)
    print("These targets are designed to be super easy to guess and generate!")
    print()
    
    targets = create_simple_targets()
    show_targets_info(targets)
    
    print("🚀 Now you can test with these easy targets!")
    print("💡 These should give much higher similarity scores!")