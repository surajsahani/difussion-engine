#!/usr/bin/env python3
"""
Quick Demo Script for Teachers
Shows the improved HD, child-friendly image generation
"""

from proper_visual_game import ProperVisualGame
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def run_teacher_demo():
    """Run a quick demo for teachers to see the improvements"""
    print("🏫 TEACHER DEMO: HD Child-Friendly Image Generation")
    print("=" * 55)
    
    print("\n📚 Educational Benefits:")
    print("  ✓ High Definition: 1024x1024 (vs old 512x512)")
    print("  ✓ High Contrast: Clear colors for better visibility") 
    print("  ✓ Child-Friendly: Simple objects kids can understand")
    print("  ✓ Age-Appropriate: Perfect for 5+ year old students")
    print("  ✓ Educational: Great for learning prompt engineering")
    
    print("\n🎯 Creating sample target images...")
    
    # Create several examples to show variety
    for i in range(5):
        game = ProperVisualGame()
        print(f"  ✓ Generated HD target image #{i+1}")
        
    print("\n🔤 Testing child-friendly prompts...")
    
    # Test different types of prompts that kids might use
    kid_friendly_prompts = [
        "red house",
        "pretty rainbow", 
        "cute cat",
        "big tree",
        "my car",
        "yellow flower",
        "blue circle",
        "happy butterfly"
    ]
    
    game = ProperVisualGame()
    
    for prompt in kid_friendly_prompts:
        result = game.engine(prompt)
        print(f"  ✓ '{prompt}' → Generated {result.shape[0]}x{result.shape[1]} HD image")
    
    print("\n👨‍🏫 TEACHER NOTES:")
    print("─" * 50)
    print("• Images are now 4x larger (1024x1024 vs 512x512)")
    print("• High contrast makes details easier to see") 
    print("• Simple subjects help kids focus on prompt writing")
    print("• Bright colors keep young students engaged")
    print("• Clear shapes teach basic visual concepts")
    print("• Perfect for teaching descriptive language")
    
    print("\n🎮 How to use in classroom:")
    print("1. Show target image to students")
    print("2. Students write prompts to recreate it")
    print("3. Compare results and discuss what worked")
    print("4. Encourage descriptive, specific language")
    print("5. Celebrate creativity and learning!")
    
    print("\n🌟 Ready to revolutionize prompt engineering education!")
    print("   Students will love these bright, fun, HD images! 🎨")

if __name__ == "__main__":
    run_teacher_demo()