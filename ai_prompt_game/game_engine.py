#!/usr/bin/env python3
"""
Core game engine for AI Prompt Engineering Game
"""
import requests
import os
import json
import random
from pathlib import Path
from datetime import datetime
from .image_generator import ImageGenerator
from .comparison import ImageComparison
from .utils import load_target_image, save_player_stats, get_game_directory
from dotenv import load_dotenv
import pyttsx3


load_dotenv()
class PromptGame:
    """Main game engine"""
    
    def __init__(self, model_type="pollinations", verbose=False):
        self.model_type = model_type
        self.verbose = verbose
        self.game_dir = get_game_directory()
        
        # Initialize components
        self.generator = ImageGenerator(model_type)
        self.comparator = ImageComparison()
        
        # Game state
        self.current_target = None
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.session_start = datetime.now()
    
    def play_interactive(self):
        """Interactive game mode"""
        print("🎯 AI PROMPT ENGINEERING GAME")
        print("=" * 50)
        print("🎮 Learn AI prompt engineering through reverse engineering!")
        print("🎨 You'll see a target image and try to recreate it with prompts")
        print("=" * 50)
        
        # Choose target
        target = self.choose_target()
        if not target:
            return
        
        self.start_game_session(target)
        
        # Game loop
        while True:
            try:
                prompt = input(f"\n[Attempt #{len(self.attempts) + 1}] Your prompt: ").strip()
                
                if prompt.lower() == 'quit':
                    self.end_session()
                    break
                elif prompt.lower() == 'progress':
                    self.show_progress()
                    continue
                elif prompt.lower() == 'target':
                    self.show_target()
                    continue
                elif prompt.lower() == 'help':
                    self.show_help()
                    continue
                elif not prompt:
                    print("⚠️  Please enter a prompt or command")
                    continue
                
                # Make attempt
                result = self.make_attempt(prompt)
                
                if result and self.check_victory():
                    self.end_session(victory=True)
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⏸️  Game paused")
                self.end_session()
                break
    
    def play_target(self, target_id):
        """Play specific target"""
        target = self.get_target_by_id(target_id)
        if not target:
            print(f"❌ Target '{target_id}' not found!")
            print("💡 Use: ai-prompt-game --list-targets")
            return
        
        self.start_game_session(target)
        self.play_interactive()
    
    def play_quick_mode(self):
        """Quick 5-minute game mode"""
        print("⚡ QUICK MODE - 5 Minutes!")
        print("=" * 30)
        
        # Choose easy target
        easy_targets = [t for t in self.get_available_targets() 
                       if t.get('difficulty', 'Medium') == 'Easy']
        
        if not easy_targets:
            print("❌ No easy targets available!")
            return
        
        target = random.choice(easy_targets)
        self.start_game_session(target)
        
        print(f"🎯 Challenge: {target['name']}")
        print("⏰ You have 5 minutes to get the highest score!")
        
        # Quick game loop (simplified)
        attempts_limit = 10
        for i in range(attempts_limit):
            try:
                prompt = input(f"\n[{i+1}/{attempts_limit}] Quick prompt: ").strip()
                
                if not prompt or prompt.lower() == 'quit':
                    break
                
                result = self.make_attempt(prompt)
                
                if result and result['score'] >= 0.8:
                    print("🎉 Great score! Quick victory!")
                    break
                    
            except KeyboardInterrupt:
                break
        
        self.end_session()
    
    def choose_target(self):
        """Let player choose a target"""
        targets = self.get_available_targets()
        if not targets:
            print("❌ No targets available!")
            print("💡 Run: ai-prompt-game --setup")
            return None
        
        print("\n🎯 Choose Your Challenge:")
        print("-" * 30)
        
        for i, target in enumerate(targets, 1):
            name = target['name']
            difficulty = target.get('difficulty', 'Medium')
            print(f"{i}. {name} ({difficulty})")
        
        while True:
            try:
                choice = input(f"\nChoose target (1-{len(targets)}): ").strip()
                
                if choice.lower() == 'quit':
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(targets):
                    return targets[index]
                else:
                    print("❌ Invalid choice!")
                    
            except ValueError:
                print("❌ Please enter a number!")
            except KeyboardInterrupt:
                return None
    
    def start_game_session(self, target):
        """Start a new game session"""
        self.current_target = target
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.session_start = datetime.now()
        
        print(f"\n🎯 Challenge: {target['name']}")
        print(f"📊 Difficulty: {target.get('difficulty', 'Medium')}")
        
        if 'description' in target:
            print(f"📝 {target['description']}")
        
        self.show_target()
    
    def show_target(self):
        """Show target image information"""
        if not self.current_target:
            return
        
        print(f"\n🖼️  TARGET: {self.current_target['name']}")
        
        # Show hints if available
        if 'hints' in self.current_target:
            print("💡 Hints:")
            for hint in self.current_target['hints'][:2]:  # Show first 2 hints
                print(f"   • {hint}")
    def speak_feedback(self,feedback_text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)  # speed of speech
        engine.setProperty('volume', 1)  # volume (0.0 to 1.0)
        engine.say(feedback_text)
        engine.runAndWait()

    def make_attempt(self, prompt):
        """Process a prompt attempt"""
        attempt_num = len(self.attempts) + 1
        
        print(f"\n🎯 Attempt #{attempt_num}")
        print(f"📝 Prompt: '{prompt}'")
        print("🔄 Generating image with AI...")
        
        # Generate image
        try:
            generated_image = self.generator.generate(prompt)
            if generated_image is None:
                print("❌ Failed to generate image")
                return None
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return None
        
        # Load target image
        target_image = load_target_image(self.current_target['path'])
        if target_image is None:
            print("❌ Could not load target image")
            return None
        
        # Compare images
        scores = self.comparator.compare(generated_image, target_image)
        combined_score = scores['combined']
        
        # Update best score
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 NEW BEST SCORE!")
        
        # Show results
        print(f"\n📊 Similarity Score: {combined_score:.3f}")
        print(f"   - Structure: {scores['structural']:.3f}")
        print(f"   - Colors: {scores['histogram']:.3f}")
        print(f"   - Edges: {scores['edges']:.3f}")
        print(f"   - Dom Colors: {scores['colors']:.3f}")
        
        # Generate feedback
        feedback = self.get_feedback(combined_score, attempt_num)
        text_feedback = self.get_text_feedback(round(combined_score,1),attempt_num)
        print(f"\n💬 {feedback}")
        print(f"The text feedback is {text_feedback}")
        self.speak_feedback(text_feedback)
        # Save attempt
        attempt_data = {
            'attempt': attempt_num,
            'prompt': prompt,
            'score': combined_score,
            'detailed_scores': scores,
            'is_best': is_best,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        return attempt_data
    
    def get_text_feedback(self,score,attempt_num):
        API_URL = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        }

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        response = query({
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a Motivational Speaker. Based on the score {score} and number of attempts {attempt_num} Motivate the player in 3 short but powerful sentences"
                }
            ],
            "model": "google/gemma-2-2b-it:nebius"
        })

        return response["choices"][0]["message"]["content"]

    def get_feedback(self, score, attempt_num):
        """Generate educational feedback"""
        if score >= 0.9:
            return "🎉 Outstanding! Nearly perfect match!"
        elif score >= 0.8:
            return "🌟 Excellent! You're very close!"
        elif score >= 0.7:
            return "👍 Great work! Fine-tune your description."
        elif score >= 0.6:
            return "🤔 Good progress! Add more specific details."
        elif score >= 0.4:
            return "💡 Fair attempt! Focus on key visual elements."
        else:
            feedback = "💪 Keep trying! "
            if attempt_num <= 2:
                feedback += "Analyze the target image more carefully."
            elif attempt_num <= 4:
                feedback += "Think about colors, shapes, and composition."
            else:
                feedback += "Try a completely different approach."
            return feedback
    
    def show_progress(self):
        """Show current progress"""
        print(f"\n📈 PROGRESS:")
        print(f"   Target: {self.current_target['name']}")
        print(f"   Attempts: {len(self.attempts)}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
        
        if len(self.attempts) > 1:
            recent_scores = [a['score'] for a in self.attempts[-3:]]
            print(f"   Recent: {[f'{s:.3f}' for s in recent_scores]}")
    
    def show_help(self):
        """Show help information"""
        print("\n📖 HELP:")
        print("Commands:")
        print("  progress - Show your current progress")
        print("  target   - Show target image info again")
        print("  help     - Show this help")
        print("  quit     - Exit the game")
        print("\n💡 Tips for better prompts:")
        print("  • Be specific about colors and lighting")
        print("  • Describe the main objects and composition")
        print("  • Include style keywords (e.g., 'photography', 'painting')")
        print("  • Think about the mood and atmosphere")
    
    def check_victory(self, threshold=0.85):
        """Check if player achieved victory"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"🏆 You successfully matched the target!")
            print(f"🎯 Final Score: {self.best_score:.3f}")
            print(f"✨ Winning Prompt: '{self.best_prompt}'")
            print(f"📊 Total Attempts: {len(self.attempts)}")
            return True
        return False
    
    def end_session(self, victory=False):
        """End the current game session"""
        if not self.attempts:
            print("👋 Thanks for trying the game!")
            return
        
        # Calculate session stats
        session_time = (datetime.now() - self.session_start).total_seconds()
        
        print(f"\n📊 SESSION SUMMARY:")
        print(f"   Target: {self.current_target['name']}")
        print(f"   Duration: {session_time/60:.1f} minutes")
        print(f"   Attempts: {len(self.attempts)}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Victory: {'Yes! 🎉' if victory else 'Not yet 💪'}")
        
        # Save stats
        self.save_session_stats(victory)
        
        print("\n👋 Thanks for playing!")
        if not victory:
            print("💡 Try again anytime: ai-prompt-game")
    
    def save_session_stats(self, victory):
        """Save session statistics"""
        try:
            stats = {
                'target': self.current_target['name'],
                'attempts': len(self.attempts),
                'best_score': self.best_score,
                'best_prompt': self.best_prompt,
                'victory': victory,
                'session_time': (datetime.now() - self.session_start).total_seconds(),
                'timestamp': datetime.now().isoformat()
            }
            
            save_player_stats(stats)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Could not save stats: {e}")
    
    def get_available_targets(self):
        """Get list of available targets"""
        targets_file = self.game_dir / "targets.json"
        
        if not targets_file.exists():
            return []
        
        try:
            with open(targets_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_target_by_id(self, target_id):
        """Get target by ID"""
        targets = self.get_available_targets()
        
        for target in targets:
            if target.get('id', '').lower() == target_id.lower():
                return target
            if target.get('name', '').lower().replace(' ', '_') == target_id.lower():
                return target
        
        return None