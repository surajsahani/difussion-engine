#!/usr/bin/env python3
"""
Play Game with Diverse Target Images
Variety of styles, contrasts, and complexity levels
"""

from open_llm_game import OpenLLMGame
import os
import json

def show_diverse_categories():
    """Show categorized diverse targets"""
    targets_dir = "diverse_targets"
    
    if not os.path.exists(targets_dir):
        print("❌ Diverse targets not found. Run: python create_diverse_targets.py")
        return []
    
    # Load categories
    categories_file = f"{targets_dir}/categories.json"
    if os.path.exists(categories_file):
        with open(categories_file, 'r') as f:
            categories = json.load(f)
    else:
        categories = {}
    
    # Load descriptions
    desc_file = f"{targets_dir}/descriptions.json"
    descriptions = {}
    if os.path.exists(desc_file):
        with open(desc_file, 'r') as f:
            descriptions = json.load(f)
    
    print("🌈 DIVERSE CHALLENGE CATEGORIES")
    print("=" * 60)
    
    all_targets = []
    category_number = 1
    
    for cat_key, category in categories.items():
        print(f"\n{category_number}. {category['name']}")
        print(f"   📖 {category['description']}")
        print(f"   🎓 Focus: {category['learning_focus']}")
        print("   🎯 Challenges:")
        
        for i, target_file in enumerate(category['targets'], 1):
            target_path = f"{targets_dir}/{target_file}"
            if os.path.exists(target_path):
                all_targets.append(target_path)
                
                # Get target info
                desc = descriptions.get(target_file, {})
                difficulty = desc.get('difficulty', 'Medium')
                style = desc.get('style', 'Unknown')
                
                target_name = target_file.replace('.jpg', '').replace('_', ' ').title()
                print(f"      {len(all_targets)}. {target_name} ({style} - {difficulty})")
        
        category_number += 1
    
    print(f"\n📊 Total Challenges: {len(all_targets)}")
    return all_targets

def show_style_based_selection():
    """Show targets organized by style"""
    targets_dir = "diverse_targets"
    
    if not os.path.exists(targets_dir):
        return []
    
    # Load descriptions
    desc_file = f"{targets_dir}/descriptions.json"
    descriptions = {}
    if os.path.exists(desc_file):
        with open(desc_file, 'r') as f:
            descriptions = json.load(f)
    
    # Group by style
    styles = {}
    for filename, desc in descriptions.items():
        style = desc.get('style', 'Other')
        if style not in styles:
            styles[style] = []
        styles[style].append(filename)
    
    print("🎨 CHOOSE BY VISUAL STYLE")
    print("=" * 40)
    
    all_targets = []
    for i, (style, files) in enumerate(styles.items(), 1):
        print(f"\n{i}. {style} Style:")
        for filename in files:
            target_path = f"{targets_dir}/{filename}"
            if os.path.exists(target_path):
                all_targets.append(target_path)
                desc = descriptions[filename]
                difficulty = desc.get('difficulty', 'Medium')
                target_name = filename.replace('.jpg', '').replace('_', ' ').title()
                print(f"   {len(all_targets)}. {target_name} ({difficulty})")
    
    return all_targets

def play_diverse_challenge(target_path):
    """Play with a diverse target image"""
    target_name = os.path.basename(target_path).replace('.jpg', '').replace('_', ' ').title()
    
    # Load target info
    targets_dir = os.path.dirname(target_path)
    desc_file = f"{targets_dir}/descriptions.json"
    target_info = {}
    
    if os.path.exists(desc_file):
        with open(desc_file, 'r') as f:
            descriptions = json.load(f)
            target_filename = os.path.basename(target_path)
            target_info = descriptions.get(target_filename, {})
    
    print(f"🎯 Challenge: {target_name}")
    print("=" * 60)
    
    # Show challenge info
    if target_info:
        print(f"🎨 Style: {target_info.get('style', 'Unknown')}")
        print(f"📊 Difficulty: {target_info.get('difficulty', 'Medium')}")
        print(f"🎓 Learning Focus: {target_info.get('learning_objectives', {}).get('style_objective', 'Visual description')}")
        print(f"🎯 Key Elements: {', '.join(target_info.get('key_elements', [])[:4])}")
        print("=" * 60)
    
    try:
        # Initialize game
        game = OpenLLMGame(target_path, model_type="pollinations")
        
        # Show target image
        print("🖼️  Here's your challenge image:")
        game.show_target_image()
        
        # Show sample prompts if available
        if target_info and 'sample_prompts' in target_info:
            print(f"\n💡 Sample prompt ideas (don't copy exactly!):")
            for i, prompt in enumerate(target_info['sample_prompts'][:3], 1):
                print(f"   {i}. \"{prompt}\"")
        
        print("\n" + "=" * 60)
        print("🎮 YOUR TURN! Enter prompts to match this image")
        print("💡 Think about the style, mood, and specific elements you see")
        print("Commands: 'progress', 'target', 'hint', 'quit'")
        print("=" * 60)
        
        # Game loop
        while True:
            try:
                prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Your prompt: ").strip()
                
                if prompt.lower() == 'quit':
                    game.save_session()
                    print("👋 Thanks for playing!")
                    break
                elif prompt.lower() == 'progress':
                    game.show_progress()
                    continue
                elif prompt.lower() == 'target':
                    game.show_target_image()
                    continue
                elif prompt.lower() == 'hint':
                    if target_info:
                        print(f"\n💡 HINT: This is a {target_info.get('style', 'unknown')} style image.")
                        print(f"🎯 Focus on: {', '.join(target_info.get('key_elements', [])[:2])}")
                        if 'sample_prompts' in target_info:
                            print(f"💭 Try something like: \"{target_info['sample_prompts'][0]}\"")
                    else:
                        print("💡 HINT: Look closely at the style, colors, and main elements!")
                    continue
                elif not prompt:
                    print("⚠️  Please enter a prompt or command")
                    continue
                
                # Make attempt
                result = game.make_attempt(prompt)
                
                if result:
                    # Check for victory
                    if game.check_victory():
                        print(f"\n🎉 Congratulations! You mastered this {target_info.get('style', '')} challenge!")
                        game.save_session()
                        break
                    
                    # Show progress
                    game.show_progress()
                    
                    # Style-specific encouragement
                    if target_info and result['score'] < 0.5:
                        style = target_info.get('style', '')
                        if style == 'High Contrast':
                            print("💡 Tip: Focus on the dramatic lighting and strong contrasts")
                        elif style == 'Minimalist':
                            print("💡 Tip: Keep it simple - describe the key elements clearly")
                        elif style == 'Complex':
                            print("💡 Tip: Break down the scene - what are the main components?")
                        elif style == 'Abstract':
                            print("💡 Tip: Use creative, artistic language to describe the patterns")
                        elif style == 'Urban':
                            print("💡 Tip: Think about modern, city-related vocabulary")
                        elif style == 'Vintage':
                            print("💡 Tip: Consider the nostalgic, classic elements")
                
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
    print("🌈 DIVERSE IMAGE PROMPT CHALLENGE")
    print("=" * 50)
    print("🎯 Mission: Master prompt engineering across different visual styles!")
    print("🤖 AI Model: Pollinations.ai (Free, High Quality)")
    print("=" * 50)
    
    print("Choose selection method:")
    print("1. 📂 Browse by Category (Recommended)")
    print("2. 🎨 Browse by Style")
    print("3. 🎲 Random Challenge")
    
    selection_choice = input("Enter choice (1-3): ").strip()
    
    if selection_choice == "1":
        # Category-based selection
        targets = show_diverse_categories()
    elif selection_choice == "2":
        # Style-based selection
        targets = show_style_based_selection()
    elif selection_choice == "3":
        # Random selection
        targets_dir = "diverse_targets"
        if os.path.exists(targets_dir):
            import random
            all_files = [f for f in os.listdir(targets_dir) if f.endswith('.jpg')]
            if all_files:
                random_file = random.choice(all_files)
                targets = [f"{targets_dir}/{random_file}"]
                print(f"🎲 Random challenge selected: {random_file}")
            else:
                targets = []
        else:
            targets = []
    else:
        print("Invalid choice, using category view...")
        targets = show_diverse_categories()
    
    if not targets:
        print("💡 First run: python create_diverse_targets.py")
        return
    
    # Let user choose target
    try:
        choice = input(f"\nChoose your challenge (1-{len(targets)}): ").strip()
        
        if choice.lower() == 'quit':
            print("👋 Maybe next time!")
            return
        
        index = int(choice) - 1
        
        if 0 <= index < len(targets):
            target_path = targets[index]
            
            # Start the game
            play_diverse_challenge(target_path)
            
        else:
            print("❌ Invalid choice. Please run again.")
            
    except ValueError:
        print("❌ Please enter a number")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()