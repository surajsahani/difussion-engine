#!/usr/bin/env python3
"""
Real Stable Diffusion Game using your actual engine
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# Import your actual Stable Diffusion engine
from stable_difussion_engine import StableDiffusionEngine
from diffusers import LMSDiscreteScheduler

class RealPromptGame:
    """Game using your actual Stable Diffusion engine"""
    
    def __init__(self, target_image_path=None, device="CPU"):
        print("🎯 Initializing REAL Stable Diffusion Game...")
        
        # Initialize YOUR actual Stable Diffusion engine
        print("🔄 Loading Stable Diffusion model...")
        scheduler = LMSDiscreteScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear"
        )
        
        try:
            self.engine = StableDiffusionEngine(scheduler=scheduler, device=device)
            print("✅ Real Stable Diffusion engine loaded!")
        except Exception as e:
            print(f"❌ Error loading Stable Diffusion: {e}")
            print("💡 Make sure you have all dependencies installed")
            raise
        
        # Load target image
        if target_image_path and os.path.exists(target_image_path):
            self.target_image = cv2.imread(target_image_path)
            self.target_path = target_image_path
            print(f"📁 Loaded target image: {target_image_path}")
        else:
            print("❌ Please provide a target image path!")
            print("💡 Usage: python real_sd_game.py path/to/your/target/image.jpg")
            raise ValueError("Target image required")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Create output directory
        os.makedirs("real_game_attempts", exist_ok=True)
        
        print("✅ Real game initialized!")
    
    def show_target_image(self):
        """Display the target image"""
        plt.figure(figsize=(8, 6))
        
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        
        plt.imshow(target_rgb)
        plt.title("TARGET IMAGE - Match this with your prompts!", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        plt.figtext(0.5, 0.02, 
                   "Create prompts that generate images similar to this target",
                   ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        
        # Save target display
        target_display = "REAL_TARGET_TO_MATCH.png"
        plt.savefig(target_display, dpi=150, bbox_inches='tight')
        plt.show()
        
        print(f"🎯 Target image saved as: {target_display}")
        print("👆 This is what you need to match with your prompts!")
    
    def calculate_similarity(self, generated_image, target_image):
        """Calculate similarity between images"""
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
        
        # Convert to grayscale
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
        """Show comparison between target and generated"""
        plt.figure(figsize=(14, 7))
        
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        
        # Target
        plt.subplot(1, 2, 1)
        plt.imshow(target_rgb)
        plt.title("TARGET IMAGE", fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Generated
        plt.subplot(1, 2, 2)
        plt.imshow(generated_rgb)
        plt.title(f"GENERATED IMAGE\nSimilarity: {score:.3f}", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        
        plt.suptitle(f"Attempt #{self.current_attempt}: '{prompt}'", 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Save comparison
        comparison_file = f"real_game_attempts/attempt_{self.current_attempt:03d}_comparison.png"
        plt.savefig(comparison_file, dpi=150, bbox_inches='tight')
        print(f"💾 Comparison saved: {comparison_file}")
        
        plt.show()
    
    def make_attempt(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate image using REAL Stable Diffusion"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        print("🔄 Generating with REAL Stable Diffusion...")
        
        try:
            # Use YOUR actual Stable Diffusion engine
            generated_image = self.engine(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            )
            
            print("✅ Image generated successfully!")
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
        
        # Save generated image
        gen_file = f"real_game_attempts/attempt_{self.current_attempt:03d}_generated.jpg"
        cv2.imwrite(gen_file, generated_image)
        print(f"💾 Generated image saved: {gen_file}")
        
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
        
        # Feedback
        if combined_score >= 0.85:
            feedback = "🎉 Excellent! Very close match!"
        elif combined_score >= 0.70:
            feedback = "👍 Good work! Getting closer."
        elif combined_score >= 0.50:
            feedback = "🤔 Fair attempt. Keep refining."
        else:
            feedback = "💪 Keep trying! Analyze the target more carefully."
        
        print(f"💬 {feedback}")
        
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
            'is_best': is_best
        }
    
    def show_progress(self):
        """Show game progress"""
        print(f"\n📈 PROGRESS:")
        print(f"   Attempts: {self.current_attempt}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
    
    def check_victory(self, threshold=0.85):
        """Check for victory"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"Score: {self.best_score:.3f}")
            print(f"Winning Prompt: '{self.best_prompt}'")
            return True
        return False
    
    def save_session(self):
        """Save session"""
        session_data = {
            'target_image_path': self.target_path,
            'attempts': self.attempts,
            'best_score': self.best_score,
            'best_prompt': self.best_prompt,
            'total_attempts': self.current_attempt,
            'session_end': datetime.now().isoformat()
        }
        
        session_file = f"real_game_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session saved: {session_file}")

def play_real_game(target_image_path, device="CPU"):
    """Play with real Stable Diffusion"""
    print("🎯 REAL STABLE DIFFUSION PROMPT GAME")
    print("=" * 50)
    
    try:
        # Initialize with real engine
        game = RealPromptGame(target_image_path, device)
        
        # Show target
        print("\n🎯 Here's your TARGET IMAGE:")
        game.show_target_image()
        
        print("\n" + "=" * 50)
        print("Now enter prompts to match this image using REAL AI!")
        print("Commands: 'progress', 'target', 'quit'")
        print("=" * 50)
        
        # Game loop
        while True:
            try:
                prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter prompt: ").strip()
                
                if prompt.lower() == 'quit':
                    game.save_session()
                    break
                elif prompt.lower() == 'progress':
                    game.show_progress()
                    continue
                elif prompt.lower() == 'target':
                    game.show_target_image()
                    continue
                elif not prompt:
                    print("⚠️  Please enter a prompt")
                    continue
                
                # Generate with real SD
                result = game.make_attempt(prompt)
                
                if result and game.check_victory():
                    game.save_session()
                    break
                
                game.show_progress()
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted")
                game.save_session()
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have:")
        print("   1. All dependencies installed")
        print("   2. A valid target image")
        print("   3. Stable Diffusion models downloaded")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python real_sd_game.py path/to/target/image.jpg")
        sys.exit(1)
    
    target_path = sys.argv[1]
    play_real_game(target_path)