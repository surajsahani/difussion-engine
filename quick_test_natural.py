#!/usr/bin/env python3
"""
Quick test of natural image game
"""

from open_llm_game import OpenLLMGame
import os

def quick_test():
    """Quick test with mountain sunset"""
    target_path = "natural_target/car.png"
    
    if not os.path.exists(target_path):
        print("❌ Target not found. Run: python create_natural_targets.py")
        return
    
    print("🌟 Quick Test: Mountain Sunset Challenge")
    print("=" * 50)
    
    # Initialize game
    game = OpenLLMGame(target_path, model_type="pollinations")
    
    # Show target
    print("🖼️  Target: Beautiful mountain sunset landscape")
    game.show_target_image()
    
    # Test with your prompt
    test_prompt = "golden sunset over mountain peaks with dramatic clouds"
    
    print(f"\n🧪 Testing with prompt: '{test_prompt}'")
    print("🔄 This will generate a real AI image...")
    
    result = game.make_attempt(test_prompt)
    
    if result:
        print(f"\n📊 Score: {result['score']:.3f}")
        print(f"💬 {result['feedback']}")
        
        print("\n✅ Test successful!")
        print("🎮 Now you can enter YOUR OWN prompts!")
        print("\n🚀 To play interactively:")
        print("python play_natural_game.py")
    else:
        print("❌ Test failed")

if __name__ == "__main__":
    quick_test()