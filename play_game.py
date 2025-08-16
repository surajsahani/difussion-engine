#!/usr/bin/env python3
"""
Reverse Prompt Engineering Game
Students try to guess the prompt that would generate a given target image
"""

import argparse
import os
import sys
from prompt_guessing_game import PromptGuessingGame

def main():
    parser = argparse.ArgumentParser(description="Play the Reverse Prompt Engineering Game")
    parser.add_argument("target_image", help="Path to the target image")
    parser.add_argument("--device", default="CPU", help="Device to use (CPU/GPU)")
    parser.add_argument("--steps", type=int, default=20, help="Number of inference steps")
    parser.add_argument("--guidance", type=float, default=7.5, help="Guidance scale")
    
    args = parser.parse_args()
    
    # Check if target image exists
    if not os.path.exists(args.target_image):
        print(f"❌ Error: Target image '{args.target_image}' not found!")
        sys.exit(1)
    
    print("🎯 Welcome to the Reverse Prompt Engineering Game!")
    print("=" * 50)
    print("Your mission: Create prompts that generate images similar to the target image")
    print(f"Target image: {args.target_image}")
    print(f"Device: {args.device}")
    print("=" * 50)
    
    # Initialize game
    try:
        game = PromptGuessingGame(args.target_image, device=args.device)
        print("✅ Game initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing game: {e}")
        sys.exit(1)
    
    print("\n📋 Instructions:")
    print("- Enter prompts to generate images")
    print("- Type 'progress' to see your current progress")
    print("- Type 'quit' to exit and save your session")
    print("- Type 'help' for more commands")
    print("\n🎮 Let's start!")
    
    while True:
        try:
            # Get user input
            prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter your prompt: ").strip()
            
            # Handle special commands
            if prompt.lower() == 'quit':
                game.save_session()
                print("👋 Thanks for playing! Session saved.")
                break
            elif prompt.lower() == 'progress':
                game.show_progress()
                continue
            elif prompt.lower() == 'help':
                print("\n📖 Available commands:")
                print("  - Enter any text prompt to generate an image")
                print("  - 'progress' - Show current game progress")
                print("  - 'quit' - Exit and save session")
                print("  - 'help' - Show this help message")
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt or command")
                continue
            
            # Make attempt
            result = game.make_attempt(
                prompt, 
                num_inference_steps=args.steps,
                guidance_scale=args.guidance
            )
            
            if result is None:
                continue
            
            # Check for victory
            if game.check_victory():
                game.save_session()
                break
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Game interrupted by user")
            game.save_session()
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()