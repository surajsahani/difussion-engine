#!/usr/bin/env python3
"""
Easy AI Prompt Game with Beginner-Friendly Targets
Perfect for learning and getting high scores!
"""

from ai_prompt_game.game_engine import PromptGame
import json
import os

def load_easy_targets():
    """Load the easy targets we created"""
    if not os.path.exists("easy_targets/targets.json"):
        print("❌ Easy targets not found!")
        print("💡 Run: python create_easy_targets.py")
        return []
    
    with open("easy_targets/targets.json", "r") as f:
        return json.load(f)

def show_easy_targets(targets):
    """Show available easy targets"""
    print("🎯 BEGINNER-FRIENDLY CHALLENGES:")
    print("=" * 50)
    print("These targets are designed for HIGH SUCCESS RATES! 🎉")
    print()
    
    for i, target in enumerate(targets, 1):
        difficulty = target['difficulty']
        if difficulty == 'Beginner':
            emoji = "🟢"
        else:
            emoji = "🔵"
        
        print(f"{i}. {target['name']}")
        print(f"   {emoji} Difficulty: {difficulty}")
        print(f"   📝 {target['description']}")
        print(f"   ✨ Try: '{target['example_prompts'][0]}'")
        print()
    
    return targets

def play_easy_challenge():
    """Play with easy, beginner-friendly targets"""
    print("🎮 EASY AI PROMPT CHALLENGE")
    print("=" * 50)
    print("🎯 Mission: Get HIGH similarity scores with simple prompts!")
    print("🤖 AI Model: Pollinations.ai (Free)")
    print("💡 These targets are designed for SUCCESS!")
    print("=" * 50)
    
    # Load easy targets
    targets = load_easy_targets()
    if not targets:
        return
    
    # Show targets
    targets = show_easy_targets(targets)
    
    # Let user choose
    try:
        choice = input(f"Choose your challenge (1-{len(targets)}): ").strip()
        
        if choice.lower() == 'quit':
            print("👋 Maybe next time!")
            return
        
        index = int(choice) - 1
        
        if 0 <= index < len(targets):
            target = targets[index]
            
            print(f"\n🎯 Challenge: {target['name']}")
            print("=" * 60)
            
            # Initialize game with visual mode
            game = PromptGame(model_type="pollinations", visual_mode=True)
            
            # Start game session
            game.start_game_session(target)
            
            print("\n" + "=" * 60)
            print("🎮 YOUR TURN! Enter prompts to match this image")
            print("💡 Use the example prompts or create your own!")
            print("Commands: 'progress' = stats, 'target' = show target again, 'quit' = exit")
            print("=" * 60)
            
            # Game loop
            while True:
                try:
                    prompt = input(f"\n[Attempt #{len(game.attempts) + 1}] Your prompt: ").strip()
                    
                    if prompt.lower() == 'quit':
                        game.save_session_stats(False)
                        print("👋 Thanks for playing!")
                        break
                    elif prompt.lower() == 'progress':
                        game.show_progress()
                        continue
                    elif prompt.lower() == 'target':
                        game.show_target()
                        continue
                    elif prompt.lower() == 'help':
                        print("\n📖 Tips for this target:")
                        for hint in target.get('hints', []):
                            print(f"   • {hint}")
                        print("\n✨ Example prompts:")
                        for example in target.get('example_prompts', []):
                            print(f"   • '{example}'")
                        continue
                    elif not prompt:
                        print("⚠️  Please enter a prompt or command")
                        continue
                    
                    # Make attempt
                    print("🔄 Generating your image with AI...")
                    result = game.make_attempt(prompt)
                    
                    if result:
                        score = result['score']
                        print(f"\n📊 Your Score: {score:.3f}")
                        
                        # Encouraging feedback for easy targets
                        if score >= 0.8:
                            print("🎉 AMAZING! Excellent match!")
                        elif score >= 0.6:
                            print("🌟 Great work! Very good similarity!")
                        elif score >= 0.4:
                            print("👍 Good progress! Try being more specific!")
                        else:
                            print("💪 Keep trying! Look at the example prompts!")
                        
                        if result.get('is_best'):
                            print("🏆 NEW PERSONAL BEST!")
                        
                        # Check for victory (lower threshold for easy targets)
                        if game.check_victory(threshold=0.75):  # Easier victory condition
                            print("\n🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉")
                            print("You successfully matched the target!")
                            game.save_session_stats(True)
                            break
                        
                        # Show progress
                        game.show_progress()
                        
                        # Helpful suggestions
                        if score < 0.5 and len(game.attempts) <= 2:
                            print(f"\n💡 Hint: Try '{target['example_prompts'][0]}'")
                
                except KeyboardInterrupt:
                    print("\n\n⏸️  Game paused")
                    save_choice = input("Save progress? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        game.save_session_stats(False)
                    break
        else:
            print("❌ Invalid choice. Please run again.")
            
    except ValueError:
        print("❌ Please enter a number")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    play_easy_challenge()