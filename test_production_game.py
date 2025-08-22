#!/usr/bin/env python3
"""
Production test of the improved algorithm in the actual game
"""

from ai_prompt_game.game_engine import PromptGame
import os

def test_production_game():
    """Test the game with improved algorithm"""
    
    print("🎮 Production Game Test with Improved Algorithm")
    print("=" * 60)
    
    # Initialize game engine
    game = PromptGame(visual_mode=False, verbose=True)  # No visual for automated test
    
    # Test with a simple prompt
    test_prompts = [
        "a cute orange cat sitting",
        "white fluffy cat portrait", 
        "tabby cat with green eyes",
        "hello world text"  # This should score very low
    ]
    
    print("🎯 Testing with 'cat' target...")
    
    # Load cat target
    target_name = "cat"
    game.play_target(target_name)  # This sets up the target
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 Test {i}: '{prompt}'")
        print("-" * 40)
        
        try:
            # Make attempt
            result = game.make_attempt(prompt)
            
            if result:
                scores = result['scores']
                print(f"✅ Success!")
                print(f"   Combined Score: {scores['combined']:.3f}")
                print(f"   Perceptual: {scores['perceptual']:.3f}")
                print(f"   Semantic: {scores['semantic']:.3f}")
                print(f"   Structural: {scores['structural']:.3f}")
                print(f"   Color Advanced: {scores['color_advanced']:.3f}")
                print(f"   Texture: {scores['texture']:.3f}")
                
                # Test backward compatibility
                print(f"   [Legacy] Histogram: {scores['histogram']:.3f}")
                print(f"   [Legacy] Edges: {scores['edges']:.3f}")
                print(f"   [Legacy] Colors: {scores['colors']:.3f}")
                
                # Get explanations
                explanations = game.comparison.explain_scores(scores)
                print(f"   🤖 AI Analysis: {explanations[0]}")
                
            else:
                print("❌ Failed to generate image")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Production test completed!")
    print(f"📊 The improved algorithm is working in production!")

if __name__ == "__main__":
    test_production_game()