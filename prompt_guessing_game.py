import cv2
import numpy as np
from stable_difussion_engine import StableDiffusionEngine
from diffusers import LMSDiscreteScheduler
from sklearn.metrics.pairwise import cosine_similarity
from skimage.metrics import structural_similarity as ssim
import os
import json
from datetime import datetime

class PromptGuessingGame:
    def __init__(self, target_image_path, device="CPU"):
        """
        Initialize the prompt guessing game
        
        Args:
            target_image_path: Path to the target image students need to match
            device: Device to run inference on (CPU/GPU)
        """
        # Initialize the Stable Diffusion engine
        scheduler = LMSDiscreteScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear"
        )
        self.engine = StableDiffusionEngine(scheduler=scheduler, device=device)
        
        # Load target image
        self.target_image = cv2.imread(target_image_path)
        if self.target_image is None:
            raise ValueError(f"Could not load target image from {target_image_path}")
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Scoring thresholds
        self.excellent_threshold = 0.85
        self.good_threshold = 0.70
        self.fair_threshold = 0.50
        
    def calculate_similarity(self, generated_image, target_image):
        """
        Calculate similarity between generated and target images
        Uses multiple metrics for comprehensive comparison
        """
        # Resize images to same size for comparison
        h, w = target_image.shape[:2]
        generated_resized = cv2.resize(generated_image, (w, h))
        
        # Convert to grayscale for SSIM
        target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        generated_gray = cv2.cvtColor(generated_resized, cv2.COLOR_BGR2GRAY)
        
        # Structural similarity
        ssim_score = ssim(target_gray, generated_gray)
        
        # Histogram comparison
        target_hist = cv2.calcHist([target_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        generated_hist = cv2.calcHist([generated_resized], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        hist_score = cv2.compareHist(target_hist, generated_hist, cv2.HISTCMP_CORREL)
        
        # Feature-based comparison (using ORB features)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(target_gray, None)
        kp2, des2 = orb.detectAndCompute(generated_gray, None)
        
        feature_score = 0
        if des1 is not None and des2 is not None:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            if len(matches) > 0:
                feature_score = min(len(matches) / max(len(kp1), len(kp2)), 1.0)
        
        # Combined score (weighted average)
        combined_score = (ssim_score * 0.4 + hist_score * 0.4 + feature_score * 0.2)
        
        return {
            'combined': max(0, combined_score),
            'structural': max(0, ssim_score),
            'histogram': max(0, hist_score),
            'features': feature_score
        }
    
    def get_feedback(self, score):
        """Generate feedback based on similarity score"""
        if score >= self.excellent_threshold:
            return "🎉 Excellent! You're very close to the target image!"
        elif score >= self.good_threshold:
            return "👍 Good work! You're getting closer. Try refining your prompt."
        elif score >= self.fair_threshold:
            return "🤔 Fair attempt. Consider the style, colors, and composition."
        else:
            return "💡 Keep trying! Think about the main subject, style, and details."
    
    def get_hints(self, score, attempt_number):
        """Provide progressive hints based on attempt number and score"""
        hints = []
        
        if attempt_number >= 3 and score < 0.3:
            hints.append("💡 Hint: Focus on the main subject in the image")
        
        if attempt_number >= 5 and score < 0.5:
            hints.append("🎨 Hint: Pay attention to the art style and colors")
        
        if attempt_number >= 7 and score < 0.6:
            hints.append("📐 Hint: Consider the composition and background elements")
        
        if attempt_number >= 10:
            hints.append("🔍 Hint: Look closely at lighting, textures, and fine details")
        
        return hints
    
    def make_attempt(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """
        Process a student's prompt attempt
        
        Args:
            prompt: The prompt entered by the student
            num_inference_steps: Number of diffusion steps
            guidance_scale: Guidance scale for generation
        """
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        print("🔄 Generating image...")
        
        # Generate image from prompt
        try:
            generated_image = self.engine(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            )
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
        
        # Calculate similarity
        scores = self.calculate_similarity(generated_image, self.target_image)
        combined_score = scores['combined']
        
        # Save attempt
        attempt_data = {
            'attempt': self.current_attempt,
            'prompt': prompt,
            'score': combined_score,
            'detailed_scores': scores,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        # Update best score
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            print("🏆 New best score!")
        
        # Display results
        print(f"📊 Similarity Score: {combined_score:.3f}")
        print(f"   - Structural: {scores['structural']:.3f}")
        print(f"   - Color/Histogram: {scores['histogram']:.3f}")
        print(f"   - Features: {scores['features']:.3f}")
        
        # Provide feedback
        feedback = self.get_feedback(combined_score)
        print(f"💬 {feedback}")
        
        # Show hints if needed
        hints = self.get_hints(combined_score, self.current_attempt)
        for hint in hints:
            print(f"   {hint}")
        
        # Save generated image
        output_filename = f"attempt_{self.current_attempt:03d}_score_{combined_score:.3f}.jpg"
        cv2.imwrite(output_filename, generated_image)
        print(f"💾 Generated image saved as: {output_filename}")
        
        return {
            'generated_image': generated_image,
            'score': combined_score,
            'detailed_scores': scores,
            'feedback': feedback,
            'hints': hints,
            'is_best': combined_score == self.best_score
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
    
    def save_session(self, filename="game_session.json"):
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