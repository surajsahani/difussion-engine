#!/usr/bin/env python3
"""
Proper Visual Prompt Guessing Game
Students see the target image FIRST, then try to create prompts to match it
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
import random

class MockStableDiffusionEngine:
    """Mock engine that creates images based on prompt keywords"""
    
    def __init__(self, scheduler=None, device="CPU"):
        print(f"🎨 Mock Stable Diffusion Engine initialized (device: {device})")
        
    def __call__(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate a mock image based on prompt keywords"""
        print(f"🔄 Generating image for: '{prompt}'")
        
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        prompt_lower = prompt.lower()
        
        # Sky/background based on keywords
        if "sunset" in prompt_lower or "golden" in prompt_lower or "orange" in prompt_lower:
            # Sunset gradient
            for y in range(height // 2):
                intensity = 1.0 - (y / (height // 2))
                image[y, :, 0] = int(255 * intensity * 0.9)  # Red
                image[y, :, 1] = int(255 * intensity * 0.7)  # Green
                image[y, :, 2] = int(255 * intensity * 0.3)  # Blue
        elif "blue" in prompt_lower and "sky" in prompt_lower:
            # Blue sky
            image[:height//2, :, 2] = 200
            image[:height//2, :, 1] = 150
            image[:height//2, :, 0] = 100
        else:
            # Default sky
            image[:height//2, :] = [180, 180, 200]
        
        # Ground/water
        if "water" in prompt_lower or "ocean" in prompt_lower or "lake" in prompt_lower:
            # Water
            image[height//2:, :, 2] = 150
            image[height//2:, :, 1] = 100
            image[height//2:, :, 0] = 50
        elif "desert" in prompt_lower or "sand" in prompt_lower:
            # Desert
            image[height//2:, :] = [139, 169, 255]  # Sandy color
        else:
            # Default ground
            image[height//2:, :] = [60, 120, 60]  # Green ground
        
        # Add objects
        if "mountain" in prompt_lower:
            # Mountain silhouette
            for x in range(width):
                mountain_height = int(height * 0.25 * (0.5 + 0.5 * np.sin(x * 0.01)))
                y_start = height//2 - mountain_height
                image[y_start:height//2, x] = [60, 60, 60]
        
        if "sun" in prompt_lower:
            # Add sun
            sun_x = random.randint(width//4, 3*width//4)
            sun_y = random.randint(50, height//3)
            cv2.circle(image, (sun_x, sun_y), 40, (255, 255, 200), -1)
        
        if "moon" in prompt_lower:
            # Add moon
            moon_x = random.randint(width//4, 3*width//4)
            moon_y = random.randint(50, height//3)
            cv2.circle(image, (moon_x, moon_y), 35, (240, 240, 240), -1)
        
        # Add variation
        noise = np.random.randint(-15, 15, image.shape)
        image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return image

class ProperVisualGame:
    """Proper visual game that shows target first"""
    
    def __init__(self, target_image_path=None):
        print("🎯 Initializing Visual Prompt Guessing Game...")
        
        # Initialize engine
        self.engine = MockStableDiffusionEngine()
        
        # Load or create target image
        if target_image_path and os.path.exists(target_image_path):
            self.target_image = cv2.imread(target_image_path)
            self.target_path = target_image_path
            print(f"📁 Loaded target image: {target_image_path}")
        else:
            # Create a challenging target image
            self.target_image = self.create_challenge_image()
            self.target_path = "challenge_target.jpg"
            cv2.imwrite(self.target_path, self.target_image)
            print(f"🎨 Created challenge target: {self.target_path}")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Create output directory
        os.makedirs("game_attempts", exist_ok=True)
        
        print("✅ Game initialized!")
    
    def create_challenge_image(self):
        """Create a challenging target image for students to match"""
        height, width = 512, 512
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create a sunset over water with mountains
        # Sunset sky gradient
        for y in range(height // 2):
            intensity = 1.0 - (y / (height // 2))
            target[y, :, 0] = int(255 * intensity * 0.9)  # Red
            target[y, :, 1] = int(255 * intensity * 0.7)  # Green
            target[y, :, 2] = int(255 * intensity * 0.3)  # Blue
        
        # Water reflection
        target[height//2:, :, 2] = 120
        target[height//2:, :, 1] = 80
        target[height//2:, :, 0] = 40
        
        # Add sun
        cv2.circle(target, (400, 120), 45, (255, 255, 200), -1)
        
        # Add mountain silhouette
        for x in range(width):
            mountain_height = int(height * 0.2 * (0.5 + 0.5 * np.sin(x * 0.008)))
            y_start = height//2 - mountain_height
            target[y_start:height//2, x] = [50, 50, 50]
        
        return target
    
    def show_target_image(self):
        """Display the target image that students need to match"""
        plt.figure(figsize=(8, 6))
        
        # Convert BGR to RGB for matplotlib
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        
        plt.imshow(target_rgb)
        plt.title("TARGET IMAGE - Try to create a prompt that generates this!", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        # Add instructions
        plt.figtext(0.5, 0.02, 
                   "Your goal: Write prompts that will generate an image similar to this target",
                   ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        
        # Save the target display
        target_display_file = "TARGET_IMAGE_TO_MATCH.png"
        plt.savefig(target_display_file, dpi=150, bbox_inches='tight')
        
        plt.show()
        
        print("🎯 TARGET IMAGE saved as: TARGET_IMAGE_TO_MATCH.png")
        print("👆 Check this file to see what you need to match!")
        print("🎯 Your mission: Create prompts that will generate a similar image")
        print("💡 Think about: colors, objects, style, lighting, composition")
    
    def calculate_similarity(self, generated_image, target_image):
        """Calculate similarity between images"""
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
        
        # Convert to grayscale for structural comparison
        gen_gray = cv2.cvtColor(generated_image, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        
        # Structural similarity
        mse = np.mean((gen_gray.astype(float) - target_gray.astype(float)) ** 2)
        structural_sim = 1 - (mse / (255 * 255))
        
        # Color histogram similarity
        gen_hist = cv2.calcHist([generated_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        target_hist = cv2.calcHist([target_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        hist_sim = cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CORREL)
        
        # Combined score
        combined = (structural_sim * 0.6 + max(0, hist_sim) * 0.4)
        
        return {
            'combined': max(0, min(1, combined)),
            'structural': max(0, structural_sim),
            'histogram': max(0, hist_sim)
        }
    
    def display_comparison(self, generated_image, prompt, score):
        """Show target vs generated image comparison"""
        plt.figure(figsize=(14, 7))
        
        # Convert BGR to RGB
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        
        # Target image
        plt.subplot(1, 2, 1)
        plt.imshow(target_rgb)
        plt.title("🎯 TARGET IMAGE", fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Generated image
        plt.subplot(1, 2, 2)
        plt.imshow(generated_rgb)
        plt.title(f"🎨 YOUR GENERATED IMAGE\nSimilarity Score: {score:.3f}", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Add prompt as figure title
        plt.suptitle(f"Attempt #{self.current_attempt}: '{prompt}'", 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Save comparison
        comparison_file = f"game_attempts/attempt_{self.current_attempt:03d}_comparison.png"
        plt.savefig(comparison_file, dpi=150, bbox_inches='tight')
        print(f"💾 Comparison saved: {comparison_file}")
        
        plt.show()
    
    def get_feedback_and_hints(self, score, prompt):
        """Provide feedback and hints based on score and prompt"""
        feedback = ""
        hints = []
        
        if score >= 0.85:
            feedback = "🎉 Excellent! You're very close to the target!"
        elif score >= 0.70:
            feedback = "👍 Good work! You're getting closer."
            hints.append("💡 Try being more specific about colors and lighting")
        elif score >= 0.50:
            feedback = "🤔 Fair attempt. You're on the right track."
            hints.append("💡 Look closely at the colors in the target image")
            hints.append("💡 Consider the time of day and lighting")
        else:
            feedback = "💪 Keep trying! Every attempt teaches you something."
            hints.append("💡 What's the main subject in the target image?")
            hints.append("💡 What colors dominate the scene?")
            hints.append("💡 What time of day does it look like?")
        
        # Specific hints based on target image content
        if score < 0.6:
            if "sunset" not in prompt.lower() and "orange" not in prompt.lower():
                hints.append("🌅 Hint: The lighting suggests a specific time of day")
            if "water" not in prompt.lower() and "lake" not in prompt.lower():
                hints.append("💧 Hint: There's a reflective surface in the image")
            if "mountain" not in prompt.lower():
                hints.append("⛰️ Hint: There are landscape features creating a silhouette")
        
        return feedback, hints
    
    def make_attempt(self, prompt):
        """Process a student's prompt attempt"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        
        # Generate image
        generated_image = self.engine(prompt)
        
        # Save generated image
        gen_file = f"game_attempts/attempt_{self.current_attempt:03d}_generated.jpg"
        cv2.imwrite(gen_file, generated_image)
        
        # Calculate similarity
        scores = self.calculate_similarity(generated_image, self.target_image)
        combined_score = scores['combined']
        
        # Update best score
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 NEW BEST SCORE!")
        
        # Display results
        print(f"📊 Similarity Score: {combined_score:.3f}")
        print(f"   - Structural: {scores['structural']:.3f}")
        print(f"   - Color Match: {scores['histogram']:.3f}")
        
        # Show comparison
        self.display_comparison(generated_image, prompt, combined_score)
        
        # Get feedback and hints
        feedback, hints = self.get_feedback_and_hints(combined_score, prompt)
        print(f"💬 {feedback}")
        
        for hint in hints:
            print(f"   {hint}")
        
        # Save attempt
        attempt_data = {
            'attempt': self.current_attempt,
            'prompt': prompt,
            'score': combined_score,
            'detailed_scores': scores,
            'generated_image_path': gen_file,
            'is_best': is_best,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        return {
            'score': combined_score,
            'feedback': feedback,
            'hints': hints,
            'is_best': is_best
        }
    
    def show_progress(self):
        """Show current game progress"""
        print(f"\n📈 GAME PROGRESS:")
        print(f"   Total Attempts: {self.current_attempt}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
        
        if len(self.attempts) > 1:
            recent_scores = [a['score'] for a in self.attempts[-5:]]
            print(f"   Recent Scores: {[f'{s:.3f}' for s in recent_scores]}")
            
            # Show improvement
            if len(self.attempts) >= 2:
                improvement = self.attempts[-1]['score'] - self.attempts[-2]['score']
                if improvement > 0:
                    print(f"   📈 Last attempt improved by: +{improvement:.3f}")
                elif improvement < 0:
                    print(f"   📉 Last attempt decreased by: {improvement:.3f}")
    
    def check_victory(self, threshold=0.85):
        """Check for victory condition"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY ACHIEVED! 🎉🎉🎉")
            print(f"🏆 You successfully matched the target image!")
            print(f"🎯 Final Score: {self.best_score:.3f}")
            print(f"✨ Winning Prompt: '{self.best_prompt}'")
            print(f"📊 Total Attempts: {self.current_attempt}")
            return True
        return False
    
    def save_session(self):
        """Save game session"""
        session_data = {
            'target_image_path': self.target_path,
            'attempts': self.attempts,
            'best_score': self.best_score,
            'best_prompt': self.best_prompt,
            'total_attempts': self.current_attempt,
            'session_end': datetime.now().isoformat()
        }
        
        session_file = f"game_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Game session saved: {session_file}")

def play_game():
    """Main game function"""
    print("🎯 REVERSE PROMPT ENGINEERING GAME")
    print("=" * 50)
    print("🎮 How to play:")
    print("1. You'll see a TARGET IMAGE")
    print("2. Your job is to write prompts that generate similar images")
    print("3. Each attempt shows you the result and gives you a score")
    print("4. Try to get as close as possible to the target!")
    print("=" * 50)
    
    # Initialize game
    game = ProperVisualGame()
    
    # Show the target image FIRST
    print("\n🎯 Here's your TARGET IMAGE:")
    game.show_target_image()
    
    print("\n" + "=" * 50)
    print("Now start entering prompts to try to match this image!")
    print("Commands: 'progress' = show stats, 'target' = show target again, 'quit' = exit")
    print("=" * 50)
    
    # Game loop
    while True:
        try:
            prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter your prompt: ").strip()
            
            if prompt.lower() == 'quit':
                game.save_session()
                print("👋 Thanks for playing! Your session has been saved.")
                break
            elif prompt.lower() == 'progress':
                game.show_progress()
                continue
            elif prompt.lower() == 'target':
                game.show_target_image()
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt or command")
                continue
            
            # Make attempt
            result = game.make_attempt(prompt)
            
            # Check for victory
            if game.check_victory():
                game.save_session()
                break
            
            # Show progress after each attempt
            game.show_progress()
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Game interrupted by user")
            game.save_session()
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    play_game()