#!/usr/bin/env python3
"""
Basic test script with no external dependencies
Tests the core game logic using pure Python
"""

import json
import random
from datetime import datetime

class BasicPromptGame:
    """Ultra-simple version using only built-in Python"""
    
    def __init__(self):
        print("🎯 Initializing Basic Prompt Game...")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Target characteristics (what we're trying to match)
        self.target_keywords = ["sunset", "orange", "warm", "sky", "golden"]
        
        print("✅ Game initialized successfully!")
        print("🎨 Target: A warm sunset scene with orange/golden colors")
    
    def calculate_similarity(self, prompt):
        """Calculate similarity based on keyword matching"""
        prompt_lower = prompt.lower()
        
        # Base score
        score = 0.1
        
        # Keyword matching
        keyword_matches = 0
        for keyword in self.target_keywords:
            if keyword in prompt_lower:
                keyword_matches += 1
                score += 0.15
        
        # Length bonus (more descriptive prompts get slight bonus)
        if len(prompt.split()) > 3:
            score += 0.05
        
        # Style keywords
        style_keywords = ["painting", "art", "beautiful", "scenic", "landscape"]
        for keyword in style_keywords:
            if keyword in prompt_lower:
                score += 0.1
                break
        
        # Color keywords
        color_keywords = ["red", "yellow", "gold", "amber"]
        for keyword in color_keywords:
            if keyword in prompt_lower:
                score += 0.1
                break
        
        # Add some randomness to simulate image generation variance
        score += random.uniform(-0.1, 0.1)
        
        # Ensure score is between 0 and 1
        score = max(0, min(1, score))
        
        return {
            'combined': score,
            'keyword_matches': keyword_matches,
            'total_keywords': len(self.target_keywords)
        }
    
    def get_feedback(self, score, keyword_matches):
        """Generate feedback based on similarity score"""
        if score >= 0.85:
            return "🎉 Excellent! You're very close to the target image!"
        elif score >= 0.70:
            return "👍 Good work! You're getting closer. Try refining your prompt."
        elif score >= 0.50:
            return "🤔 Fair attempt. Consider the style, colors, and composition."
        else:
            feedback = "💡 Keep trying! "
            if keyword_matches == 0:
                feedback += "Try including words like 'sunset', 'orange', or 'golden'."
            elif keyword_matches < 2:
                feedback += "You're on the right track, add more descriptive words."
            else:
                feedback += "Good keywords, try being more specific about the scene."
            return feedback
    
    def get_hints(self, attempt_number, score):
        """Provide progressive hints"""
        hints = []
        
        if attempt_number >= 3 and score < 0.4:
            hints.append("💡 Hint: The target image has warm, sunset colors")
        
        if attempt_number >= 5 and score < 0.6:
            hints.append("🌅 Hint: Think about the time of day - golden hour")
        
        if attempt_number >= 7 and score < 0.7:
            hints.append("🎨 Hint: Try adding artistic style words like 'painting' or 'beautiful'")
        
        return hints
    
    def make_attempt(self, prompt):
        """Process a student's prompt attempt"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        print("🔄 Analyzing prompt...")
        
        # Calculate similarity
        result = self.calculate_similarity(prompt)
        score = result['combined']
        keyword_matches = result['keyword_matches']
        
        # Save attempt
        attempt_data = {
            'attempt': self.current_attempt,
            'prompt': prompt,
            'score': score,
            'keyword_matches': keyword_matches,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        # Update best score
        is_best = False
        if score > self.best_score:
            self.best_score = score
            self.best_prompt = prompt
            is_best = True
            print("🏆 New best score!")
        
        # Display results
        print(f"📊 Similarity Score: {score:.3f}")
        print(f"🔍 Keyword Matches: {keyword_matches}/{result['total_keywords']}")
        
        # Provide feedback
        feedback = self.get_feedback(score, keyword_matches)
        print(f"💬 {feedback}")
        
        # Show hints if needed
        hints = self.get_hints(self.current_attempt, score)
        for hint in hints:
            print(f"   {hint}")
        
        return {
            'score': score,
            'keyword_matches': keyword_matches,
            'feedback': feedback,
            'hints': hints,
            'is_best': is_best
        }
    
    def show_progress(self):
        """Display current game progress"""
        print(f"\n📈 Game Progress:")
        print(f"   Attempts: {self.current_attempt}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
        
        if self.attempts:
            recent_scores = [a['score'] for a in self.attempts[-5:]]
            print(f"   Recent Scores: {[f'{s:.3f}' for s in recent_scores]}")
    
    def check_victory(self, threshold=0.85):
        """Check if student has achieved victory"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"You've successfully matched the target characteristics!")
            print(f"Final Score: {self.best_score:.3f}")
            print(f"Winning Prompt: '{self.best_prompt}'")
            print(f"Total Attempts: {self.current_attempt}")
            return True
        return False
    
    def save_session(self, filename="basic_test_session.json"):
        """Save the current game session"""
        session_data = {
            'attempts': self.attempts,
            'best_score': self.best_score,
            'best_prompt': self.best_prompt,
            'current_attempt': self.current_attempt,
            'session_end': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session saved to {filename}")

def run_automated_test():
    """Run automated test with sample prompts"""
    print("🚀 Starting Automated Basic Test")
    print("=" * 50)
    
    game = BasicPromptGame()
    
    # Test prompts (from worst to best)
    test_prompts = [
        "a picture",
        "blue ocean",
        "red car",
        "sunset",
        "orange sunset",
        "beautiful sunset painting",
        "golden sunset over mountains",
        "warm orange sunset with golden sky",
        "beautiful golden hour sunset painting with warm orange colors"
    ]
    
    print("\n🎮 Testing with sample prompts...")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}/{len(test_prompts)} ---")
        result = game.make_attempt(prompt)
        
        if game.check_victory():
            break
    
    # Show final results
    print("\n" + "=" * 50)
    print("🏁 Automated Test Complete!")
    game.show_progress()
    game.save_session()
    
    return game

def run_interactive_test():
    """Run interactive test where user enters prompts"""
    print("🚀 Starting Interactive Basic Test")
    print("=" * 50)
    
    game = BasicPromptGame()
    
    print("\n📋 Instructions:")
    print("- Enter prompts to try to match the target")
    print("- Type 'progress' to see your current progress")
    print("- Type 'quit' to exit")
    print("- Type 'help' for more commands")
    
    while True:
        try:
            prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter your prompt: ").strip()
            
            if prompt.lower() == 'quit':
                game.save_session()
                print("👋 Thanks for testing!")
                break
            elif prompt.lower() == 'progress':
                game.show_progress()
                continue
            elif prompt.lower() == 'help':
                print("\n📖 Available commands:")
                print("  - Enter any text prompt to test")
                print("  - 'progress' - Show current game progress")
                print("  - 'quit' - Exit and save session")
                print("  - 'help' - Show this help message")
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt or command")
                continue
            
            result = game.make_attempt(prompt)
            
            if game.check_victory():
                game.save_session()
                break
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Test interrupted")
            game.save_session()
            break
    
    return game

def main():
    """Main function to choose test mode"""
    print("🎯 Basic Prompt Game Tester")
    print("Choose test mode:")
    print("1. Automated test (runs sample prompts)")
    print("2. Interactive test (you enter prompts)")
    print("3. Both tests")
    
    try:
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            run_automated_test()
        elif choice == "2":
            run_interactive_test()
        elif choice == "3":
            print("\n" + "="*50)
            print("Running automated test first...")
            run_automated_test()
            
            print("\n" + "="*50)
            print("Now running interactive test...")
            run_interactive_test()
        else:
            print("Invalid choice. Running automated test by default...")
            run_automated_test()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")

if __name__ == "__main__":
    main()