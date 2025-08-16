#!/usr/bin/env python3
"""
Visual Prompt Guessing Game with Image Generation and Display
This version generates actual images and shows them to the user
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime
import json
import os
import random

class MockStableDiffusionEngine:
    """
    Mock Stable Diffusion Engine that creates realistic-looking images
    based on prompt keywords for demonstration purposes
    """
    
    def __init__(self, scheduler=None, device="CPU"):
        print(f"🎨 Initializing Mock Stable Diffusion Engine (device: {device})")
        self.device = device
        
    def __call__(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate a mock image based on prompt keywords"""
        print(f"🔄 Generating image for: '{prompt}'")
        
        # Create base image
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        prompt_lower = prompt.lower()
        
        # Sky/background generation
        if "sunset" in prompt_lower or "golden" in prompt_lower:
            # Create sunset gradient
            for y in range(height // 2):
                intensity = 1.0 - (y / (height // 2))
                image[y, :, 0] = int(255 * intensity * 0.9)  # Red
                image[y, :, 1] = int(255 * intensity * 0.6)  # Green
                image[y, :, 2] = int(255 * intensity * 0.2)  # Blue
        elif "blue" in prompt_lower:
            # Blue sky
            image[:height//2, :, 2] = 200
            image[:height//2, :, 1] = 100
        elif "night" in prompt_lower or "dark" in prompt_lower:
            # Dark sky
            image[:height//2, :] = 30
        else:
            # Default light sky
            image[:height//2, :] = 180
        
        # Ground/water
        if "water" in prompt_lower or "ocean" in prompt_lower or "lake" in prompt_lower:
            # Water reflection
            image[height//2:, :, 2] = 150
            image[height//2:, :, 1] = 100
            image[height//2:, :, 0] = 50
        elif "mountain" in prompt_lower:
            # Mountain silhouette
            for x in range(width):
                mountain_height = int(height * 0.3 * (0.5 + 0.5 * np.sin(x * 0.02)))
                y_start = height//2 - mountain_height
                image[y_start:height//2, x] = [80, 80, 80]
        else:
            # Default ground
            image[height//2:, :, 1] = 120
            image[height//2:, :, 0] = 60
        
        # Add objects based on keywords
        if "tree" in prompt_lower or "forest" in prompt_lower:
            # Add some trees
            for _ in range(random.randint(3, 8)):
                x = random.randint(50, width-50)
                tree_height = random.randint(80, 150)
                y_start = height//2 - tree_height//2
                y_end = height//2 + tree_height//2
                # Tree trunk
                image[y_end-20:y_end, x-5:x+5] = [101, 67, 33]  # Brown
                # Tree foliage
                cv2.circle(image, (x, y_start+20), 25, (34, 139, 34), -1)  # Green
        
        if "sun" in prompt_lower:
            # Add sun
            sun_x, sun_y = random.randint(100, width-100), random.randint(50, 150)
            cv2.circle(image, (sun_x, sun_y), 40, (255, 255, 200), -1)
        
        if "cloud" in prompt_lower:
            # Add clouds
            for _ in range(random.randint(2, 5)):
                cloud_x = random.randint(50, width-100)
                cloud_y = random.randint(30, 120)
                cv2.ellipse(image, (cloud_x, cloud_y), (60, 30), 0, 0, 360, (255, 255, 255), -1)
        
        # Add artistic effects
        if "painting" in prompt_lower or "art" in prompt_lower:
            # Add some texture/noise for artistic effect
            noise = np.random.randint(-20, 20, image.shape)
            image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add some general variation
        variation = np.random.randint(-10, 10, image.shape)
        image = np.clip(image.astype(np.int16) + variation, 0, 255).astype(np.uint8)
        
        return image

class VisualPromptGame:
    """Visual version of the prompt guessing game with image display"""
    
    def __init__(self, target_image_path=None):
        print("🎯 Initializing Visual Prompt Game...")
        
        # Initialize mock engine (replace with real engine when ready)
        self.engine = MockStableDiffusionEngine()
        
        # Load or create target image
        if target_image_path and os.path.exists(target_image_path):
            self.target_image = cv2.imread(target_image_path)
            print(f"📁 Loaded target image: {target_image_path}")
        else:
            # Create a default target image
            self.target_image = self.create_target_image()
            cv2.imwrite("target_image.jpg", self.target_image)
            print("🎨 Created default target image: target_image.jpg")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Create output directory
        os.makedirs("generated_images", exist_ok=True)
        
        print("✅ Visual game initialized!")
    
    def create_target_image(self):
        """Create a default target image for demonstration"""
        height, width = 512, 512
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create a sunset scene
        for y in range(height // 2):
            intensity = 1.0 - (y / (height // 2))
            target[y, :, 0] = int(255 * intensity * 0.9)  # Red
            target[y, :, 1] = int(255 * intensity * 0.7)  # Green
            target[y, :, 2] = int(255 * intensity * 0.3)  # Blue
        
        # Add water
        target[height//2:, :, 2] = 120
        target[height//2:, :, 1] = 80
        target[height//2:, :, 0] = 40
        
        # Add sun
        cv2.circle(target, (400, 100), 50, (255, 255, 200), -1)
        
        # Add mountain silhouette
        for x in range(width):
            mountain_height = int(height * 0.2 * (0.5 + 0.5 * np.sin(x * 0.01)))
            y_start = height//2 - mountain_height
            target[y_start:height//2, x] = [60, 60, 60]
        
        return target
    
    def calculate_similarity(self, generated_image, target_image):
        """Calculate similarity between images using multiple metrics"""
        # Resize to same size if needed
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
        
        # Convert to different color spaces for comparison
        gen_gray = cv2.cvtColor(generated_image, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        
        # 1. Structural similarity (simplified)
        mse = np.mean((gen_gray.astype(float) - target_gray.astype(float)) ** 2)
        max_mse = 255 * 255
        structural_sim = 1 - (mse / max_mse)
        
        # 2. Color histogram similarity
        gen_hist = cv2.calcHist([generated_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        target_hist = cv2.calcHist([target_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        hist_sim = cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CORREL)
        
        # 3. Simple feature matching (edge detection)
        gen_edges = cv2.Canny(gen_gray, 50, 150)
        target_edges = cv2.Canny(target_gray, 50, 150)
        edge_sim = 1 - np.mean(np.abs(gen_edges.astype(float) - target_edges.astype(float))) / 255
        
        # Combined score
        combined = (structural_sim * 0.4 + max(0, hist_sim) * 0.4 + edge_sim * 0.2)
        
        return {
            'combined': max(0, min(1, combined)),
            'structural': max(0, structural_sim),
            'histogram': max(0, hist_sim),
            'features': max(0, edge_sim)
        }
    
    def display_images(self, generated_image, target_image, prompt, score):
        """Display target and generated images side by side"""
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
        plt.suptitle(f"Prompt: '{prompt}'", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save the comparison
        comparison_filename = f"generated_images/attempt_{self.current_attempt:03d}_comparison.png"
        plt.savefig(comparison_filename, dpi=150, bbox_inches='tight')
        print(f"💾 Comparison saved: {comparison_filename}")
        
        # Show the plot
        plt.show()
    
    def get_feedback(self, score):
        """Generate feedback based on similarity score"""
        if score >= 0.85:
            return "🎉 Excellent! You're very close to the target image!"
        elif score >= 0.70:
            return "👍 Good work! You're getting closer. Try refining your prompt."
        elif score >= 0.50:
            return "🤔 Fair attempt. Consider the style, colors, and composition."
        else:
            return "💡 Keep trying! Think about the main subject, style, and details."
    
    def make_attempt(self, prompt):
        """Process a student's prompt attempt with visual output"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        
        # Generate image
        generated_image = self.engine(prompt)
        
        # Save generated image
        gen_filename = f"generated_images/attempt_{self.current_attempt:03d}_generated.jpg"
        cv2.imwrite(gen_filename, generated_image)
        
        # Calculate similarity
        scores = self.calculate_similarity(generated_image, self.target_image)
        combined_score = scores['combined']
        
        # Update best score
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 New best score!")
        
        # Display results
        print(f"📊 Similarity Score: {combined_score:.3f}")
        print(f"   - Structural: {scores['structural']:.3f}")
        print(f"   - Color/Histogram: {scores['histogram']:.3f}")
        print(f"   - Features: {scores['features']:.3f}")
        
        # Show images
        self.display_images(generated_image, self.target_image, prompt, combined_score)
        
        # Provide feedback
        feedback = self.get_feedback(combined_score)
        print(f"💬 {feedback}")
        
        # Save attempt data
        attempt_data = {
            'attempt': self.current_attempt,
            'prompt': prompt,
            'score': combined_score,
            'detailed_scores': scores,
            'generated_image_path': gen_filename,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        return {
            'score': combined_score,
            'detailed_scores': scores,
            'feedback': feedback,
            'is_best': is_best,
            'generated_image': generated_image
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
            print(f"You've successfully matched the target image!")
            print(f"Final Score: {self.best_score:.3f}")
            print(f"Winning Prompt: '{self.best_prompt}'")
            print(f"Total Attempts: {self.current_attempt}")
            return True
        return False
    
    def save_session(self, filename="visual_game_session.json"):
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

def run_visual_demo():
    """Run a visual demonstration of the game"""
    print("🎨 Visual Prompt Game Demo")
    print("=" * 50)
    
    # Initialize game
    game = VisualPromptGame()
    
    # Demo prompts
    demo_prompts = [
        "a landscape",
        "sunset over water",
        "golden sunset with mountains",
        "beautiful sunset painting over water with mountains"
    ]
    
    print("\n🎮 Running visual demo...")
    print("Images will be displayed and saved to 'generated_images/' folder")
    
    for prompt in demo_prompts:
        result = game.make_attempt(prompt)
        
        if game.check_victory():
            break
        
        input("\nPress Enter to continue to next prompt...")
    
    game.show_progress()
    game.save_session()
    
    print(f"\n✅ Demo complete! Check the 'generated_images/' folder for all images.")

def run_interactive_visual():
    """Run interactive visual game"""
    print("🎨 Interactive Visual Prompt Game")
    print("=" * 50)
    
    game = VisualPromptGame()
    
    print("\n📋 Instructions:")
    print("- Enter prompts to generate images")
    print("- Images will be displayed and saved automatically")
    print("- Type 'progress' to see your stats")
    print("- Type 'quit' to exit")
    
    while True:
        try:
            prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter your prompt: ").strip()
            
            if prompt.lower() == 'quit':
                game.save_session()
                print("👋 Thanks for playing!")
                break
            elif prompt.lower() == 'progress':
                game.show_progress()
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt")
                continue
            
            result = game.make_attempt(prompt)
            
            if game.check_victory():
                game.save_session()
                break
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Game interrupted")
            game.save_session()
            break

if __name__ == "__main__":
    print("🎯 Visual Prompt Engineering Game")
    print("Choose mode:")
    print("1. Demo (automated with sample prompts)")
    print("2. Interactive (you enter prompts)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        run_visual_demo()
    elif choice == "2":
        run_interactive_visual()
    else:
        print("Running demo by default...")
        run_visual_demo()