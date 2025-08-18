#!/usr/bin/env python3
"""
Voice Feedback Demo Script
Demonstrates the new voice feedback functionality in the AI Prompt Game
"""

import time
from simple_test import SimplePromptGame

def demo_voice_feedback():
    """Demonstrate voice feedback functionality"""
    
    print("🎤 Voice Feedback Demo for AI Prompt Game")
    print("=" * 50)
    print()
    
    # Test with voice feedback enabled
    print("📢 Testing with voice feedback ENABLED:")
    game_with_voice = SimplePromptGame(voice_feedback_enabled=True)
    
    print("\n🎯 Making a few test attempts...")
    
    # Simulate some attempts
    test_prompts = [
        "a beautiful sunset over mountains",
        "orange and blue abstract art", 
        "golden hour landscape photography"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Voice Demo {i}/3 ---")
        result = game_with_voice.make_attempt(prompt)
        time.sleep(2)  # Give time for voice feedback
    
    print("\n" + "="*50)
    print("📢 Testing with voice feedback DISABLED:")
    game_without_voice = SimplePromptGame(voice_feedback_enabled=False)
    
    print("\n🎯 Making a test attempt...")
    result = game_without_voice.make_attempt("silent test prompt")
    
    print("\n" + "="*50)
    print("🔧 Testing voice feedback control:")
    
    # Test dynamic control
    game_with_voice.set_voice_feedback(False)
    print("Making attempt with voice disabled...")
    game_with_voice.make_attempt("quiet test")
    
    game_with_voice.set_voice_feedback(True)
    print("Making attempt with voice re-enabled...")
    game_with_voice.make_attempt("voice test again")
    
    print("\n✅ Voice feedback demo completed!")
    print("\n💡 Key Features:")
    print("   • Voice feedback can be enabled/disabled at initialization")
    print("   • Voice feedback can be toggled during gameplay")
    print("   • Speaks similarity scores and feedback messages")
    print("   • Falls back gracefully when TTS is not available")
    print("   • Cleans emoji and formatting for better speech")
    print("   • Uses separate thread to avoid blocking game flow")

if __name__ == "__main__":
    demo_voice_feedback()