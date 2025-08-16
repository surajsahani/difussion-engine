#!/usr/bin/env python3
"""
Open LLM Image Generation Game
Integrates with popular open-source image generation models
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
import requests
from PIL import Image
import io

class OpenImageGenerator:
    """
    Wrapper for various open-source image generation APIs and models
    """
    
    def __init__(self, model_type="huggingface", device="CPU"):
        self.model_type = model_type
        self.device = device
        print(f"🎨 Initializing {model_type} image generator...")
        
        if model_type == "huggingface":
            self.setup_huggingface()
        elif model_type == "replicate":
            self.setup_replicate()
        elif model_type == "local_diffusers":
            self.setup_local_diffusers()
        elif model_type == "pollinations":
            self.setup_pollinations()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def setup_huggingface(self):
        """Setup Hugging Face Inference API (Free tier available)"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            print("🔄 Loading Stable Diffusion from Hugging Face...")
            
            # Use a lightweight model for faster generation
            model_id = "runwayml/stable-diffusion-v1-5"
            
            if torch.cuda.is_available() and self.device.upper() == "GPU":
                self.pipe = StableDiffusionPipeline.from_pretrained(
                    model_id, 
                    torch_dtype=torch.float16
                ).to("cuda")
                print("✅ GPU acceleration enabled")
            else:
                self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
                print("✅ CPU mode (slower but works)")
            
            print("✅ Hugging Face Stable Diffusion loaded!")
            
        except ImportError:
            print("❌ Missing dependencies. Install with:")
            print("pip install diffusers transformers torch torchvision")
            raise
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def setup_replicate(self):
        """Setup Replicate API (requires API key but very good quality)"""
        try:
            import replicate
            
            # You'll need to set REPLICATE_API_TOKEN environment variable
            # Get free API key from https://replicate.com
            self.replicate_client = replicate
            print("✅ Replicate API ready!")
            print("💡 Make sure to set REPLICATE_API_TOKEN environment variable")
            
        except ImportError:
            print("❌ Install replicate: pip install replicate")
            raise
    
    def setup_local_diffusers(self):
        """Setup local diffusers with optimizations"""
        try:
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
            import torch
            
            print("🔄 Loading optimized local model...")
            
            # Use a fast, lightweight model
            model_id = "stabilityai/stable-diffusion-2-1-base"
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Use faster scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            if torch.cuda.is_available() and self.device.upper() == "GPU":
                self.pipe = self.pipe.to("cuda")
                # Enable memory efficient attention
                self.pipe.enable_attention_slicing()
                print("✅ GPU optimizations enabled")
            
            print("✅ Local diffusers model loaded!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    def setup_pollinations(self):
        """Setup Pollinations.ai (Free API, no key required!)"""
        print("✅ Pollinations.ai API ready!")
        print("🌟 This is completely free and requires no API key!")
    
    def generate_image(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate image based on the selected model"""
        print(f"🎨 Generating: '{prompt}'")
        
        if self.model_type == "huggingface" or self.model_type == "local_diffusers":
            return self.generate_with_diffusers(prompt, num_inference_steps, guidance_scale)
        elif self.model_type == "replicate":
            return self.generate_with_replicate(prompt)
        elif self.model_type == "pollinations":
            return self.generate_with_pollinations(prompt)
    
    def generate_with_diffusers(self, prompt, num_inference_steps, guidance_scale):
        """Generate with local diffusers"""
        try:
            with torch.no_grad():
                image = self.pipe(
                    prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=512,
                    width=512
                ).images[0]
            
            # Convert PIL to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return image_cv
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return None
    
    def generate_with_replicate(self, prompt):
        """Generate with Replicate API"""
        try:
            output = self.replicate_client.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={"prompt": prompt}
            )
            
            # Download image from URL
            response = requests.get(output[0])
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return image_cv
            
        except Exception as e:
            print(f"❌ Replicate error: {e}")
            return None
    
    def generate_with_pollinations(self, prompt):
        """Generate with Pollinations.ai (Free!)"""
        try:
            # Pollinations.ai free API
            url = "https://image.pollinations.ai/prompt/"
            
            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Add parameters for better quality
            full_url = f"{url}{encoded_prompt}?width=512&height=512&seed=-1&model=flux"
            
            print(f"🔄 Requesting from Pollinations.ai...")
            
            # Download image
            response = requests.get(full_url, timeout=30)
            
            if response.status_code == 200:
                # Convert to PIL then OpenCV
                image = Image.open(io.BytesIO(response.content))
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                return image_cv
            else:
                print(f"❌ API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Pollinations error: {e}")
            return None

class OpenLLMGame:
    """Game using open-source image generation models"""
    
    def __init__(self, target_image_path, model_type="pollinations", device="CPU"):
        print("🎯 Initializing Open LLM Image Game...")
        
        # Initialize image generator
        self.generator = OpenImageGenerator(model_type, device)
        
        # Load target image
        if not os.path.exists(target_image_path):
            raise ValueError(f"Target image not found: {target_image_path}")
        
        self.target_image = cv2.imread(target_image_path)
        self.target_path = target_image_path
        print(f"📁 Target image loaded: {target_image_path}")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Create output directory
        os.makedirs("open_llm_attempts", exist_ok=True)
        
        print("✅ Open LLM game ready!")
    
    def show_target_image(self):
        """Display target image"""
        plt.figure(figsize=(8, 6))
        
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        
        plt.imshow(target_rgb)
        plt.title("🎯 TARGET IMAGE - Match this with AI!", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        plt.figtext(0.5, 0.02, 
                   "Use AI image generation to create something similar to this target",
                   ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        
        # Save target
        target_display = "OPEN_LLM_TARGET.png"
        plt.savefig(target_display, dpi=150, bbox_inches='tight')
        plt.show()
        
        print(f"🎯 Target saved as: {target_display}")
    
    def calculate_similarity(self, generated_image, target_image):
        """Calculate image similarity with improved scoring"""
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
        
        # Multiple similarity metrics
        gen_gray = cv2.cvtColor(generated_image, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        
        # Structural similarity (improved)
        mse = np.mean((gen_gray.astype(float) - target_gray.astype(float)) ** 2)
        structural_sim = max(0, 1 - (mse / (255 * 255)))
        
        # Color histogram (improved with multiple methods)
        gen_hist = cv2.calcHist([generated_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        target_hist = cv2.calcHist([target_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        
        # Try multiple histogram comparison methods and take the best
        hist_correl = cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CORREL)
        hist_chi_sq = cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CHISQR)
        hist_intersect = cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_INTERSECT)
        
        # Normalize and combine histogram scores
        hist_correl = max(0, hist_correl)
        hist_chi_sq = max(0, 1 - (hist_chi_sq / 1000000))  # Normalize chi-square
        hist_intersect = hist_intersect / max(np.sum(gen_hist), np.sum(target_hist))
        
        hist_sim = (hist_correl * 0.5 + hist_chi_sq * 0.3 + hist_intersect * 0.2)
        
        # Edge similarity (improved)
        gen_edges = cv2.Canny(gen_gray, 50, 150)
        target_edges = cv2.Canny(target_gray, 50, 150)
        edge_diff = np.mean(np.abs(gen_edges.astype(float) - target_edges.astype(float))) / 255
        edge_sim = max(0, 1 - edge_diff)
        
        # Dominant color similarity (new metric)
        def get_dominant_colors(image, k=3):
            """Get dominant colors using k-means"""
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            return centers
        
        try:
            gen_colors = get_dominant_colors(generated_image)
            target_colors = get_dominant_colors(target_image)
            
            # Calculate color distance
            color_distances = []
            for gen_color in gen_colors:
                min_dist = float('inf')
                for target_color in target_colors:
                    dist = np.linalg.norm(gen_color - target_color)
                    min_dist = min(min_dist, dist)
                color_distances.append(min_dist)
            
            avg_color_dist = np.mean(color_distances)
            color_sim = max(0, 1 - (avg_color_dist / (255 * np.sqrt(3))))
            
        except:
            color_sim = hist_sim  # Fallback to histogram similarity
        
        # Improved combined score with better weighting
        combined = (
            structural_sim * 0.3 +    # Structure is important
            hist_sim * 0.25 +         # Overall color distribution
            edge_sim * 0.25 +         # Edge/shape matching
            color_sim * 0.2           # Dominant color matching
        )
        
        return {
            'combined': max(0, min(1, combined)),
            'structural': max(0, structural_sim),
            'histogram': max(0, hist_sim),
            'edges': max(0, edge_sim),
            'colors': max(0, color_sim)
        }
    
    def display_comparison(self, generated_image, prompt, score):
        """Show side-by-side comparison"""
        plt.figure(figsize=(15, 7))
        
        target_rgb = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2RGB)
        generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        
        # Target
        plt.subplot(1, 2, 1)
        plt.imshow(target_rgb)
        plt.title("🎯 TARGET", fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Generated
        plt.subplot(1, 2, 2)
        plt.imshow(generated_rgb)
        plt.title(f"🤖 AI GENERATED\nSimilarity: {score:.3f}", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        
        plt.suptitle(f"Attempt #{self.current_attempt}: '{prompt}'", 
                    fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Save comparison
        comparison_file = f"open_llm_attempts/attempt_{self.current_attempt:03d}_comparison.png"
        plt.savefig(comparison_file, dpi=150, bbox_inches='tight')
        print(f"💾 Saved: {comparison_file}")
        
        plt.show()
    
    def make_attempt(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate and evaluate attempt"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        
        # Generate with AI
        generated_image = self.generator.generate_image(
            prompt, num_inference_steps, guidance_scale
        )
        
        if generated_image is None:
            print("❌ Failed to generate image")
            return None
        
        print("✅ AI image generated!")
        
        # Save generated image
        gen_file = f"open_llm_attempts/attempt_{self.current_attempt:03d}_generated.jpg"
        cv2.imwrite(gen_file, generated_image)
        
        # Calculate similarity
        scores = self.calculate_similarity(generated_image, self.target_image)
        combined_score = scores['combined']
        
        # Update best
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 NEW BEST SCORE!")
        
        # Results
        print(f"📊 Similarity: {combined_score:.3f}")
        print(f"   - Structure: {scores['structural']:.3f}")
        print(f"   - Color Dist: {scores['histogram']:.3f}")
        print(f"   - Edges: {scores['edges']:.3f}")
        print(f"   - Dom Colors: {scores['colors']:.3f}")
        
        # Show comparison
        self.display_comparison(generated_image, prompt, combined_score)
        
        # Feedback
        if combined_score >= 0.85:
            feedback = "🎉 Amazing! Nearly perfect match!"
        elif combined_score >= 0.70:
            feedback = "🌟 Excellent work! Very close!"
        elif combined_score >= 0.50:
            feedback = "👍 Good progress! Keep refining!"
        else:
            feedback = "💪 Keep experimenting with different descriptions!"
        
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
        
        if len(self.attempts) > 1:
            recent = [a['score'] for a in self.attempts[-3:]]
            print(f"   Recent: {[f'{s:.3f}' for s in recent]}")
    
    def check_victory(self, threshold=0.80):
        """Check victory condition"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"🏆 Score: {self.best_score:.3f}")
            print(f"✨ Winning Prompt: '{self.best_prompt}'")
            print(f"🎯 Total Attempts: {self.current_attempt}")
            return True
        return False
    
    def save_session(self):
        """Save game session"""
        session_data = {
            'model_type': self.generator.model_type,
            'target_image_path': self.target_path,
            'attempts': self.attempts,
            'best_score': self.best_score,
            'best_prompt': self.best_prompt,
            'total_attempts': self.current_attempt,
            'session_end': datetime.now().isoformat()
        }
        
        session_file = f"open_llm_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session saved: {session_file}")

def play_open_llm_game():
    """Main game function with model selection"""
    print("🤖 OPEN LLM IMAGE GENERATION GAME")
    print("=" * 50)
    
    print("Choose your AI model:")
    print("1. 🌟 Pollinations.ai (FREE, no setup required!)")
    print("2. 🤗 Hugging Face Diffusers (local, needs GPU for speed)")
    print("3. 🔄 Replicate API (high quality, needs API key)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    model_map = {
        "1": "pollinations",
        "2": "local_diffusers", 
        "3": "replicate"
    }
    
    model_type = model_map.get(choice, "pollinations")
    
    # Get target image
    target_path = input("Enter path to target image: ").strip()
    
    if not target_path:
        print("Using default target...")
        # You could create a default target here
        target_path = "challenge_target.jpg"
    
    try:
        # Initialize game
        game = OpenLLMGame(target_path, model_type)
        
        # Show target
        print("\n🎯 Here's your TARGET:")
        game.show_target_image()
        
        print(f"\n🤖 Using {model_type} for AI generation")
        print("=" * 50)
        print("Enter prompts to generate images that match the target!")
        print("Commands: 'progress', 'target', 'quit'")
        print("=" * 50)
        
        # Game loop
        while True:
            try:
                prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Prompt: ").strip()
                
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
                    print("⚠️  Enter a prompt")
                    continue
                
                # Generate with AI
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
        print("\n💡 Quick setup for Pollinations.ai (easiest):")
        print("pip install requests pillow")

if __name__ == "__main__":
    play_open_llm_game()