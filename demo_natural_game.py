#!/usr/bin/env python3
"""
Demo of the game using beautiful natural target images
"""

from open_llm_game import OpenLLMGame
import os
import json

def show_available_targets():
    """Show available natural target images"""
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
    
    # List available targets
    targets = []
    print("🌟 Available Natural Target Images:")
    print("=" * 50)
    
    for i, filename in enumerate(sorted(os.listdir(targets_dir)), 1):
        if filename.endswith('.jpg') and not filename.startswith('test_'):
            target_path = f"{targets_dir}/{filename}"
            targets.append(target_path)
            
            # Get description if available
            desc = descriptions.get(filename, {})
            difficulty = desc.get('difficulty', 'Unknown')
            elements = desc.get('key_elements', [])
            
            print(f"{i}. {filename}")
            print(f"   📊 Difficulty: {difficulty}")
            print(f"   🎯 Elements: {', '.join(elements[:3])}...")
            print()
    
    return targets

def demo_with_target(target_path):
    """Demo the game with a specific target"""
    print(f"🎯 Starting demo with: {os.path.basename(target_path)}")
    print("=" * 60)
    
    try:
        # Initialize game with Pollinations.ai
        game = OpenLLMGame(target_path, model_type="pollinations")
        
        # Show target
        print("🖼️  Target image loaded!")
        game.show_target_image()
        
        # Demo prompts based on the target
        demo_prompts = get_demo_prompts(target_path)
        
        print(f"\n🎮 Demo with {len(demo_prompts)} sample prompts:")
        print("=" * 60)
        
        for i, prompt in enumerate(demo_prompts, 1):
            print(f"\n--- Demo Attempt {i}/{len(demo_prompts)} ---")
            
            result = game.make_attempt(prompt)
            
            if result:
                print(f"🎯 Score: {result['score']:.3f}")
                print(f"💬 {result['feedback']}")
                
                if result['is_best']:
                    print("🏆 New best score!")
                
                # Check for victory
                if game.check_victory():
                    print("🎉 Victory achieved in demo!")
                    break
            
            # Show progress
            game.show_progress()
            
            # Pause between attempts
            input("\nPress Enter to continue to next demo prompt...")
        
        # Final summary
        print("\n" + "=" * 60)
        print("🏁 Demo Complete!")
        game.show_progress()
        game.save_session()
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def get_demo_prompts(target_path):
    """Get demo prompts based on target image"""
    filename = os.path.basename(target_path)
    
    prompt_sets = {
        "mountain_sunset.jpg": [
            "landscape photo",
            "sunset over mountains", 
            "golden hour mountain landscape",
            "dramatic sunset over mountain peaks with clouds",
            "golden sunset over mountain silhouette with dramatic sky"
        ],
        "ocean_waves.jpg": [
            "ocean scene",
            "waves crashing on shore",
            "powerful ocean waves on rocky coast",
            "dramatic seascape with white foam and spray",
            "powerful ocean waves crashing on rocky shore with spray"
        ],
        "tropical_beach.jpg": [
            "beach scene",
            "tropical paradise",
            "crystal clear tropical water",
            "pristine white sand beach with turquoise water",
            "tropical beach paradise with crystal clear water and white sand"
        ],
        "forest_path.jpg": [
            "forest scene",
            "woodland path",
            "misty forest trail",
            "peaceful forest path through tall trees",
            "atmospheric forest path with morning mist and soft lighting"
        ],
        "desert_dunes.jpg": [
            "desert landscape",
            "sand dunes",
            "rolling desert dunes",
            "golden sand dunes with dramatic shadows",
            "minimalist desert landscape with rolling sand dunes and blue sky"
        ]
    }
    
    return prompt_sets.get(filename, [
        "natural landscape",
        "beautiful scenery", 
        "nature photography",
        "scenic landscape view",
        "professional nature photograph"
    ])

def interactive_demo():
    """Interactive demo where user chooses target"""
    print("🌟 Natural Target Image Demo")
    print("=" * 40)
    
    # Show available targets
    targets = show_available_targets()
    
    if not targets:
        return
    
    # Let user choose
    try:
        choice = input(f"Choose target (1-{len(targets)}): ").strip()
        index = int(choice) - 1
        
        if 0 <= index < len(targets):
            target_path = targets[index]
            demo_with_target(target_path)
        else:
            print("❌ Invalid choice")
            
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Demo cancelled")

def quick_demo():
    """Quick demo with mountain sunset"""
    target_path = "natural_target/mountain_sunset.jpg"
    
    if os.path.exists(target_path):
        print("🚀 Quick Demo with Mountain Sunset")
        demo_with_target(target_path)
    else:
        print("❌ Mountain sunset target not found")
        print("💡 Run: python create_natural_targets.py")

def main():
    """Main demo function"""
    print("🎯 Natural Image Game Demo")
    print("Choose demo mode:")
    print("1. 🚀 Quick demo (Mountain Sunset)")
    print("2. 🎮 Interactive demo (Choose target)")
    print("3. 📋 Just show available targets")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        quick_demo()
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        show_available_targets()
    else:
        print("🚀 Running quick demo by default...")
        quick_demo()

if __name__ == "__main__":
    main()