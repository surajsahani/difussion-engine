#!/usr/bin/env python3
"""
Example usage of the Prompt Guessing Game
This shows how to use the game programmatically
"""

from prompt_guessing_game import PromptGuessingGame
import cv2

def run_example():
    # You'll need to provide a target image path
    target_image_path = "target_image.jpg"  # Replace with your image path
    
    try:
        # Initialize the game
        print("🎯 Initializing Reverse Prompt Engineering Game...")
        game = PromptGuessingGame(target_image_path, device="CPU")
        
        # Example prompts to try (you can modify these)
        example_prompts = [
            "a beautiful landscape",
            "a sunset over mountains",
            "a peaceful lake with trees",
            "golden hour photography of nature",
            "serene mountain landscape at sunset"
        ]
        
        print(f"🎮 Starting game with target image: {target_image_path}")
        print("=" * 60)
        
        # Try each prompt
        for prompt in example_prompts:
            print(f"\n🔄 Trying prompt: '{prompt}'")
            result = game.make_attempt(prompt)
            
            if result:
                print(f"✅ Score: {result['score']:.3f}")
                if result['is_best']:
                    print("🏆 This is your best attempt so far!")
                
                # Check if we've won
                if game.check_victory():
                    break
            
            # Show progress after each attempt
            game.show_progress()
        
        # Final summary
        print("\n" + "=" * 60)
        print("🎯 Game Summary:")
        print(f"   Total Attempts: {game.current_attempt}")
        print(f"   Best Score: {game.best_score:.3f}")
        print(f"   Best Prompt: '{game.best_prompt}'")
        
        # Save the session
        game.save_session("example_session.json")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find target image at '{target_image_path}'")
        print("💡 Please make sure you have a target image file and update the path in this script")
    except Exception as e:
        print(f"❌ Error running example: {e}")

if __name__ == "__main__":
    run_example()