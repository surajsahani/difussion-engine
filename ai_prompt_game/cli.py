#!/usr/bin/env python3
"""
CLI interface for AI Prompt Engineering Game
Students can install and play directly from command line
"""

import argparse
import sys
import os
import json
from pathlib import Path
from .game_engine import PromptGame
from .utils import setup_game_directory, download_targets, check_dependencies

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Prompt Engineering Game - Learn AI through reverse prompt engineering!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-prompt-game                    # Start interactive game with visual display
  ai-prompt-game --setup           # Setup game files and targets
  ai-prompt-game --list-targets    # Show available challenge targets
  ai-prompt-game --target fox      # Play specific target
  ai-prompt-game --quick           # Quick 5-minute game
  ai-prompt-game --stats           # Show your progress stats
  ai-prompt-game --no-visual       # Text-only mode (no image windows)

Visual Features:
  • Target and generated images displayed side-by-side
  • Real-time similarity scoring with visual feedback
  • LLaVA AI-powered semantic image comparison (if available)
  • All images automatically saved to ~/.ai-prompt-game/generated/

For more help: https://github.com/yourusername/ai-prompt-game
        """
    )
    
    # Game options
    parser.add_argument("--setup", action="store_true", 
                       help="Setup game files and download targets")
    parser.add_argument("--target", type=str, 
                       help="Play specific target (e.g., 'fox', 'car', 'llama')")
    parser.add_argument("--list-targets", action="store_true",
                       help="List all available challenge targets")
    parser.add_argument("--quick", action="store_true",
                       help="Quick 5-minute game mode")
    parser.add_argument("--stats", action="store_true",
                       help="Show your progress statistics")
    
    # Technical options
    parser.add_argument("--model", default="pollinations",
                       choices=["pollinations", "huggingface", "replicate"],
                       help="AI model to use (default: pollinations)")
    parser.add_argument("--steps", type=int, default=20,
                       help="Number of inference steps (default: 20)")
    parser.add_argument("--guidance", type=float, default=7.5,
                       help="Guidance scale (default: 7.5)")
    parser.add_argument("--no-visual", action="store_true",
                       help="Disable visual image display (text-only mode)")
    parser.add_argument("--no-llava", action="store_true",
                       help="Disable LLaVA AI comparison (use traditional metrics only)")
    
    # Utility options
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Handle setup
    if args.setup:
        setup_game()
        return
    
    # Handle list targets
    if args.list_targets:
        list_targets()
        return
    
    # Handle stats
    if args.stats:
        show_stats()
        return
    
    # Check if game is set up
    if not check_game_setup():
        print("🎯 AI Prompt Engineering Game")
        print("=" * 40)
        print("⚠️  Game not set up yet!")
        print("\n🚀 Quick setup:")
        print("   ai-prompt-game --setup")
        print("\n💡 This will:")
        print("   • Download beautiful challenge images")
        print("   • Set up your game directory")
        print("   • Test AI connection")
        return
    
    # Start the game
    try:
        game = PromptGame(
            model_type=args.model,
            verbose=args.verbose,
            visual_mode=not getattr(args, 'no_visual', False),
            use_llava=not getattr(args, 'no_llava', False)
        )
        
        if args.target:
            game.play_target(args.target)
        elif args.quick:
            game.play_quick_mode()
        else:
            game.play_interactive()
            
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing!")
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"❌ Error: {e}")
            print("💡 Try: ai-prompt-game --verbose for more details")

def setup_game():
    """Setup game files and targets"""
    print("🎯 AI Prompt Engineering Game - Setup")
    print("=" * 50)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        print("❌ Missing dependencies. Installing...")
        install_dependencies()
    
    # Setup game directory
    print("📁 Setting up game directory...")
    game_dir = setup_game_directory()
    
    # Download targets
    print("🖼️  Downloading challenge targets...")
    download_targets(game_dir)
    
    # Test AI connection
    print("🤖 Testing AI connection...")
    test_ai_connection()
    
    print("\n🎉 Setup complete!")
    print(f"📁 Game directory: {game_dir}")
    print("\n🎮 To play:")
    print("   ai-prompt-game")
    print("\n📚 To see targets:")
    print("   ai-prompt-game --list-targets")

def list_targets():
    """List available challenge targets"""
    print("🎯 Available Challenge Targets:")
    print("=" * 40)
    
    targets = get_available_targets()
    
    if not targets:
        print("❌ No targets found!")
        print("💡 Run: ai-prompt-game --setup")
        return
    
    for i, target in enumerate(targets, 1):
        name = target['name']
        difficulty = target.get('difficulty', 'Medium')
        description = target.get('description', 'No description')
        
        print(f"{i}. {name}")
        print(f"   📊 Difficulty: {difficulty}")
        print(f"   📝 {description}")
        print()
    
    print(f"💡 To play specific target:")
    print(f"   ai-prompt-game --target {targets[0]['id']}")

def show_stats():
    """Show player statistics"""
    print("📊 Your Progress Statistics")
    print("=" * 40)
    
    stats = load_player_stats()
    
    if not stats:
        print("📈 No games played yet!")
        print("💡 Start playing: ai-prompt-game")
        return
    
    print(f"🎮 Games Played: {stats.get('games_played', 0)}")
    print(f"🎯 Total Attempts: {stats.get('total_attempts', 0)}")
    print(f"🏆 Best Score: {stats.get('best_score', 0):.3f}")
    print(f"📈 Average Score: {stats.get('average_score', 0):.3f}")
    print(f"🎉 Victories: {stats.get('victories', 0)}")
    
    if 'favorite_targets' in stats:
        print(f"\n🌟 Favorite Targets:")
        for target, count in stats['favorite_targets'].items():
            print(f"   {target}: {count} times")
    
    if 'recent_scores' in stats:
        print(f"\n📊 Recent Scores:")
        recent = stats['recent_scores'][-5:]
        print(f"   {[f'{s:.3f}' for s in recent]}")

def check_game_setup():
    """Check if game is properly set up"""
    game_dir = Path.home() / ".ai-prompt-game"
    targets_dir = game_dir / "targets"
    
    return (
        game_dir.exists() and 
        targets_dir.exists() and 
        len(list(targets_dir.glob("*.jpg"))) > 0
    )

def get_available_targets():
    """Get list of available targets"""
    game_dir = Path.home() / ".ai-prompt-game"
    targets_file = game_dir / "targets.json"
    
    if not targets_file.exists():
        return []
    
    try:
        with open(targets_file, 'r') as f:
            return json.load(f)
    except:
        return []

def load_player_stats():
    """Load player statistics"""
    game_dir = Path.home() / ".ai-prompt-game"
    stats_file = game_dir / "stats.json"
    
    if not stats_file.exists():
        return {}
    
    try:
        with open(stats_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def install_dependencies():
    """Install required dependencies"""
    import subprocess
    
    dependencies = [
        "opencv-python>=4.5.0",
        "matplotlib>=3.5.0", 
        "numpy>=1.21.0",
        "requests>=2.28.0",
        "pillow>=9.0.0"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep, "--user"
            ])
            print(f"✅ Installed: {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {dep}")

def test_ai_connection():
    """Test AI connection"""
    try:
        import requests
        
        # Test Pollinations.ai
        test_url = "https://image.pollinations.ai/prompt/test?width=64&height=64"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ AI connection working!")
        else:
            print("⚠️  AI connection may be slow")
            
    except Exception as e:
        print(f"⚠️  AI connection test failed: {e}")
        print("💡 Game will still work, but generation may be slower")

if __name__ == "__main__":
    main()