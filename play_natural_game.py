#!/usr/bin/env python3
"""
Interactive Natural Image Game
You enter prompts to match beautiful natural target images
"""

from open_llm_game import OpenLLMGame
import os
import json

def show_target_options():
    """Show available natural targets with descriptions"""
    targets_dir = "natural_target"
    
    if not os.path.exists(targets_dir):
        print("❌ Natural targets not found. Run: python create_natural_targets.py")
        return []
    
    # Load descriptions
    desc_file = f"{targets_dir}/descriptions.json"
    descriptions = {}
    if os.path.exists(desc_file):
        with open(desc_file, 'r') as f:
            descriptions = json.load(f)
    
    # List targets
    targets = []
    print("🌟 Choose Your Challenge Target:")
    print("=" * 50)
    
    target_files = [f for f in sorted(os.listdir(targets_dir)) 
                   if f.endswith('.jpg') and not f.startswith('test_')]
    
    for i, filename in enumerate(target_files, 1):
        target_path = f"{targets_dir}/{filename}"
        targets.append(target_path)
        
        # Get info
        desc = descriptions.get(filename, {})
        difficulty = desc.get('difficulty', 'Medium')
        elements = desc.get('key_elements', [])
        
        # Display option
        name = filename.replace('.jpg', '').replace('_', ' ').title()
        print(f"{i}. {name}")
        print(f"   📊 Difficulty: {difficulty}")
        if elements:
            print(f"   🎯 Key Elements: {', '.join(elements[:4])}")
        print()
    
    return targets

def play_interactive_game(target_path):
    """Play the interactive game with your prompts"""
    target_name = os.path.basename(target_path).replace('.jpg', '').replace('_', ' ').title()
    
    print(f"🎯 Challenge: {target_name}")
    print("=" * 60)
    
    try:
        # Initialize game
        game = OpenLLMGame(target_path, model_type="pollinations")
        
        # Show target image
        print("🖼️  Here's your target image to match:")
        game.show_target_image()
        
        print("\n" + "=" * 60)
        print("🎮 YOUR TURN! Enter prompts to match this image")
        print("💡 Think about: colors, lighting, composition, style, objects")
        print("Commands: 'progress' = stats, 'target' = show target again, 'quit' = exit")
        print("=" * 60)
        
        # Game loop - YOU enter the prompts!
        while True:
            try:
                # Get YOUR prompt
                prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Your prompt: ").strip()
                
                # Handle commands
                if prompt.lower() == 'quit':
                    game.save_session()
                    print("👋 Thanks for playing! Session saved.")
                    break
                elif prompt.lower() == 'progress':
                    game.show_progress()
                    continue
                elif prompt.lower() == 'target':
                    game.show_target_image()
                    continue
                elif prompt.lower() == 'help':
                    print("\n📖 Tips:")
                    print("- Describe what you see: colors, objects, lighting")
                    print("- Be specific: 'golden sunset' vs 'sunset'")
                    print("- Include style: 'landscape photography', 'natural'")
                    print("- Try different angles: 'aerial view', 'close-up'")
                    continue
                elif not prompt:
                    print("⚠️  Please enter a prompt or command")
                    continue
                
                # Make YOUR attempt
                print("🔄 Generating your image with AI...")
                result = game.make_attempt(prompt)
                
                if result:
                    print(f"\n📊 Your Score: {result['score']:.3f}")
                    print(f"💬 {result['feedback']}")
                    
                    if result['is_best']:
                        print("🏆 NEW PERSONAL BEST!")
                    
                    # Check for victory
                    if game.check_victory():
                        print("\n🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉")
                        print("You successfully matched the target image!")
                        game.save_session()
                        break
                    
                    # Show current progress
                    game.show_progress()
                    
                    # Encourage to continue
                    if result['score'] < 0.5:
                        print("\n💡 Tip: Look more closely at the target image details")
                    elif result['score'] < 0.7:
                        print("\n💡 Tip: You're getting closer! Try being more specific")
                    else:
                        print("\n💡 Tip: Almost there! Fine-tune your description")
                
            except KeyboardInterrupt:
                print("\n\n⏸️  Game paused")
                save_choice = input("Save progress? (y/n): ").strip().lower()
                if save_choice == 'y':
                    game.save_session()
                break
                
    except Exception as e:
        print(f"❌ Game error: {e}")

def main():
    """Main game function"""
    print("🌟 NATURAL IMAGE PROMPT CHALLENGE")
    print("=" * 50)
    print("🎯 Your mission: Write prompts that generate images matching natural targets")
    print("🤖 AI Model: Pollinations.ai (Free, High Quality)")
    print("=" * 50)
    
    # Show target options
    targets = show_target_options()
    
    if not targets:
        print("💡 First run: python create_natural_targets.py")
        return
    
    # Let you choose target
    try:
        choice = input(f"Choose your challenge (1-{len(targets)}): ").strip()
        
        if choice.lower() == 'quit':
            print("👋 Maybe next time!")
            return
        
        index = int(choice) - 1
        
        if 0 <= index < len(targets):
            target_path = targets[index]
            
            # Start the interactive game
            play_interactive_game(target_path)
            
        else:
            print("❌ Invalid choice. Please run again.")
            
    except ValueError:
        print("❌ Please enter a number")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()