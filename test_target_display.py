#!/usr/bin/env python3
"""
Test target image display functionality
"""

from ai_prompt_game.game_engine import PromptGame
import json
from pathlib import Path

def test_target_display():
    """Test if target image displays correctly"""
    print("🧪 Testing Target Image Display")
    print("=" * 40)
    
    try:
        # Initialize game
        game = PromptGame(visual_mode=True, verbose=True)
        
        # Get available targets
        targets = game.get_available_targets()
        
        if not targets:
            print("❌ No targets available. Run: ai-prompt-game --setup")
            return False
        
        # Use the first target (should be easy)
        target = targets[0]
        print(f"🎯 Testing with target: {target['name']}")
        
        # Start game session (this should display the target)
        game.start_game_session(target)
        
        print("✅ Target display test completed!")
        print("💡 If you saw a popup window, the visual display is working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Target display test failed: {e}")
        return False

if __name__ == "__main__":
    test_target_display()