#!/usr/bin/env python3
"""
Core game engine for AI Prompt Engineering Game
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np
try:
    import matplotlib
    # Try different backends in order of preference for macOS
    backends_to_try = ['MacOSX', 'TkAgg', 'Qt5Agg', 'Agg']
    
    backend_set = False
    for backend in backends_to_try:
        try:
            matplotlib.use(backend)
            backend_set = True
            break
        except:
            continue
    
    if not backend_set:
        # Use default backend
        pass
    
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    DISPLAY_AVAILABLE = True
except ImportError:
    DISPLAY_AVAILABLE = False
from .image_generator import ImageGenerator
from .comparison import ImageComparison
from .utils import load_target_image, save_player_stats, get_game_directory

class PromptGame:
    """Main game engine"""
    
    def __init__(self, model_type="pollinations", verbose=False, visual_mode=True, use_llava=True):
        self.model_type = model_type
        self.verbose = verbose
        self.visual_mode = visual_mode and DISPLAY_AVAILABLE
        self.use_llava = use_llava
        self.game_dir = get_game_directory()
        
        # Initialize components
        self.generator = ImageGenerator(model_type)
        self.comparator = ImageComparison(use_llava=use_llava)
        
        # Game state
        self.current_target = None
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.session_start = datetime.now()
        
        # Create generated images directory
        self.generated_dir = self.game_dir / "generated"
        self.generated_dir.mkdir(exist_ok=True)
        
        if not DISPLAY_AVAILABLE and visual_mode:
            print("⚠️  Visual mode requested but matplotlib not available")
            print("💡 Install with: pip install matplotlib")
            self.visual_mode = False
    
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
        """Show target image information and display if visual mode"""
        if not self.current_target:
            return
        
        print(f"\n🖼️  TARGET: {self.current_target['name']}")
        
        # Show target image visually if in visual mode
        if self.visual_mode:
            self.display_target_image()
        
        # Show hints if available
        if 'hints' in self.current_target:
            print("💡 Hints:")
            for hint in self.current_target['hints'][:2]:  # Show first 2 hints
                print(f"   • {hint}")
    
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
        
        # Save generated image
        gen_filename = self.generated_dir / f"attempt_{attempt_num:03d}_generated.jpg"
        cv2.imwrite(str(gen_filename), generated_image)
        
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
        
        # Show LLaVA score if available
        if 'llava_semantic' in scores and scores['llava_semantic'] > 0:
            print(f"   - AI Semantic: {scores['llava_semantic']:.3f}")
            if 'llava_explanation' in scores:
                print(f"🤖 AI Insight: {scores['llava_explanation']}")
        
        # Display images if visual mode is enabled
        if self.visual_mode:
            self.display_images(generated_image, target_image, prompt, combined_score, attempt_num)
        else:
            print(f"💾 Generated image saved: {gen_filename}")
        
        # Generate feedback
        feedback = self.get_feedback(combined_score, attempt_num)
        print(f"\n💬 {feedback}")
        
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
    
    def display_target_image(self):
        """Display target image with multiple fallback methods"""
        if not self.current_target:
            return
            
        target_image = load_target_image(self.current_target['path'])
        if target_image is None:
            print("⚠️  Could not load target image")
            return
        
        # Method 1: Try matplotlib display
        if DISPLAY_AVAILABLE:
            try:
                plt.figure(figsize=(8, 6))
                target_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
                plt.imshow(target_rgb)
                plt.title(f"🎯 TARGET: {self.current_target['name']}", 
                         fontsize=16, fontweight='bold', pad=20)
                plt.axis('off')
                plt.figtext(0.5, 0.02, 
                           "Write prompts to generate images similar to this target",
                           ha='center', fontsize=12, style='italic')
                plt.tight_layout()
                plt.show()
                print("🖼️  Target image displayed in matplotlib window!")
                return
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Matplotlib display failed: {e}")
        
        # Method 2: Save and open with system viewer
        try:
            import subprocess
            import platform
            
            # Save target image to a temporary location
            temp_target = self.generated_dir / "current_target.jpg"
            cv2.imwrite(str(temp_target), target_image)
            
            # Open with system default viewer
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(temp_target)], check=True)
            elif system == "Windows":
                subprocess.run(["start", str(temp_target)], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(temp_target)], check=True)
            
            print(f"🖼️  Target image opened with system viewer: {temp_target}")
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  System viewer failed: {e}")
            print(f"💾 Target image saved to: {self.current_target['path']}")
            print("💡 You can manually open this file to see the target image")
    
    def display_images(self, generated_image, target_image, prompt, score, attempt_num):
        """Display target and generated images side by side"""
        if not DISPLAY_AVAILABLE:
            return
        
        # Save images first
        gen_filename = self.generated_dir / f"attempt_{attempt_num:03d}_generated.jpg"
        cv2.imwrite(str(gen_filename), generated_image)
        
        comparison_filename = self.generated_dir / f"attempt_{attempt_num:03d}_comparison.png"
        
        # Method 1: Try matplotlib display
        if DISPLAY_AVAILABLE:
            try:
                plt.figure(figsize=(12, 6))
                
                # Convert BGR to RGB for matplotlib
                target_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
                generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
                
                # Target image
                plt.subplot(1, 2, 1)
                plt.imshow(target_rgb)
                plt.title("🎯 Target Image", fontsize=14, fontweight='bold')
                plt.axis('off')
                
                # Generated image
                plt.subplot(1, 2, 2)
                plt.imshow(generated_rgb)
                plt.title(f"🎨 Generated Image\nScore: {score:.3f}", fontsize=14, fontweight='bold')
                plt.axis('off')
                
                # Add prompt as figure title
                plt.suptitle(f"Attempt #{attempt_num}: '{prompt}'", fontsize=16, fontweight='bold')
                plt.tight_layout()
                
                # Save the comparison
                plt.savefig(str(comparison_filename), dpi=150, bbox_inches='tight')
                
                # Show the plot (blocking like the working local script)
                plt.show()
                
                print(f"🖼️  Comparison displayed! Saved: {comparison_filename}")
                return
                
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Matplotlib display failed: {e}")
        
        # Method 2: Create comparison and open with system viewer
        try:
            import subprocess
            import platform
            
            # Create side-by-side comparison manually
            target_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
            generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
            
            # Resize images to same height
            height = 400
            target_resized = cv2.resize(target_rgb, (int(target_rgb.shape[1] * height / target_rgb.shape[0]), height))
            generated_resized = cv2.resize(generated_rgb, (int(generated_rgb.shape[1] * height / generated_rgb.shape[0]), height))
            
            # Create side-by-side image
            comparison = np.hstack([target_resized, generated_resized])
            comparison_bgr = cv2.cvtColor(comparison, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(comparison_filename), comparison_bgr)
            
            # Open with system viewer
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(comparison_filename)], check=True)
            elif system == "Windows":
                subprocess.run(["start", str(comparison_filename)], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(comparison_filename)], check=True)
            
            print(f"🖼️  Comparison opened with system viewer: {comparison_filename}")
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  System viewer failed: {e}")
            print(f"💾 Images saved to: {self.generated_dir}")
            print(f"💾 Generated: {gen_filename}")
            print(f"💾 Comparison: {comparison_filename}")
    
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