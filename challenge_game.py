#!/usr/bin/env python3
"""
Improved Challenge Game with Real Images and Better Scoring
Uses HuggingFace images and improved similarity metrics
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
import random
# import requests  # Not needed for mock version
# from urllib.parse import urlparse  # Not needed for mock version

class MockStableDiffusionEngine:
    """Mock engine with better image generation based on prompts"""
    
    def __init__(self, scheduler=None, device="CPU"):
        print(f"🎨 Mock Stable Diffusion Engine initialized (device: {device})")
        
    def __call__(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate better mock images based on detailed prompt analysis"""
        print(f"🔄 Generating image for: '{prompt}'")
        
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        prompt_lower = prompt.lower()
        
        # Analyze prompt for better generation
        has_sunset = any(word in prompt_lower for word in ['sunset', 'golden hour', 'dusk', 'orange sky'])
        has_water = any(word in prompt_lower for word in ['water', 'ocean', 'lake', 'sea', 'river'])
        has_mountains = any(word in prompt_lower for word in ['mountain', 'hills', 'peaks'])
        has_forest = any(word in prompt_lower for word in ['forest', 'trees', 'woods'])
        has_city = any(word in prompt_lower for word in ['city', 'urban', 'buildings', 'skyline'])
        has_desert = any(word in prompt_lower for word in ['desert', 'sand', 'dunes'])
        
        # Sky generation based on prompt
        if has_sunset:
            # Realistic sunset gradient
            for y in range(height // 2):
                intensity = 1.0 - (y / (height // 2))
                # More realistic sunset colors
                image[y, :, 0] = int(255 * intensity * 0.95)  # Strong red
                image[y, :, 1] = int(255 * intensity * 0.75)  # Orange
                image[y, :, 2] = int(255 * intensity * 0.25)  # Minimal blue
        elif 'blue sky' in prompt_lower or 'clear sky' in prompt_lower:
            # Clear blue sky
            image[:height//2, :] = [100, 150, 255]
        elif 'cloudy' in prompt_lower or 'overcast' in prompt_lower:
            # Cloudy sky
            image[:height//2, :] = [180, 180, 180]
        else:
            # Default sky based on other keywords
            if has_city:
                image[:height//2, :] = [120, 140, 200]  # Urban sky
            else:
                image[:height//2, :] = [135, 206, 235]  # Sky blue
        
        # Ground/surface generation
        if has_water:
            # Water with realistic colors
            if has_sunset:
                # Sunset reflection in water
                image[height//2:, :, 0] = 180  # Red reflection
                image[height//2:, :, 1] = 120  # Orange reflection
                image[height//2:, :, 2] = 60   # Blue water
            else:
                # Regular water
                image[height//2:, :] = [60, 100, 180]
        elif has_desert:
            # Desert sand
            image[height//2:, :] = [194, 178, 128]
        elif has_city:
            # Urban ground
            image[height//2:, :] = [80, 80, 80]
        else:
            # Default ground (grass/earth)
            image[height//2:, :] = [34, 139, 34]
        
        # Add landscape features
        if has_mountains:
            # Mountain silhouettes
            for x in range(width):
                mountain_height = int(height * 0.3 * (0.6 + 0.4 * np.sin(x * 0.008 + np.pi/4)))
                y_start = height//2 - mountain_height
                if y_start < height//2:
                    image[y_start:height//2, x] = [40, 40, 40]  # Dark mountain silhouette
        
        if has_forest:
            # Add forest silhouette
            for x in range(0, width, 20):
                tree_height = random.randint(60, 120)
                tree_width = random.randint(15, 25)
                y_start = height//2 - tree_height
                x_start = max(0, x - tree_width//2)
                x_end = min(width, x + tree_width//2)
                if y_start >= 0:
                    image[y_start:height//2, x_start:x_end] = [20, 60, 20]
        
        if has_city:
            # Add city skyline
            for x in range(0, width, 30):
                building_height = random.randint(80, 200)
                building_width = random.randint(20, 40)
                y_start = height//2 - building_height
                x_start = max(0, x)
                x_end = min(width, x + building_width)
                if y_start >= 0:
                    image[y_start:height//2, x_start:x_end] = [60, 60, 60]
                    # Add some lit windows
                    if random.random() > 0.7:
                        window_y = random.randint(y_start + 10, height//2 - 10)
                        window_x = random.randint(x_start + 2, x_end - 2)
                        image[window_y:window_y+3, window_x:window_x+3] = [255, 255, 200]
        
        # Add sun/moon
        if 'sun' in prompt_lower and has_sunset:
            sun_x = random.randint(width//3, 2*width//3)
            sun_y = random.randint(80, height//3)
            cv2.circle(image, (sun_x, sun_y), 35, (255, 255, 220), -1)
        elif 'moon' in prompt_lower:
            moon_x = random.randint(width//4, 3*width//4)
            moon_y = random.randint(50, height//4)
            cv2.circle(image, (moon_x, moon_y), 30, (240, 240, 240), -1)
        
        # Add clouds if mentioned
        if 'cloud' in prompt_lower:
            for _ in range(random.randint(2, 4)):
                cloud_x = random.randint(60, width-60)
                cloud_y = random.randint(30, height//3)
                cv2.ellipse(image, (cloud_x, cloud_y), (50, 25), 0, 0, 360, (255, 255, 255), -1)
        
        # Add artistic style effects
        if any(style in prompt_lower for style in ['painting', 'artistic', 'impressionist']):
            # Add texture for artistic effect
            noise = np.random.randint(-25, 25, image.shape)
            image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add final variation
        variation = np.random.randint(-8, 8, image.shape)
        image = np.clip(image.astype(np.int16) + variation, 0, 255).astype(np.uint8)
        
        return image

class ImprovedSimilarityCalculator:
    """Better similarity calculation that matches human perception"""
    
    @staticmethod
    def calculate_color_similarity(img1, img2):
        """Calculate color distribution similarity"""
        # Convert to HSV for better color comparison
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        # Calculate histograms for each channel
        h1 = cv2.calcHist([hsv1], [0], None, [180], [0, 180])
        s1 = cv2.calcHist([hsv1], [1], None, [256], [0, 256])
        v1 = cv2.calcHist([hsv1], [2], None, [256], [0, 256])
        
        h2 = cv2.calcHist([hsv2], [0], None, [180], [0, 180])
        s2 = cv2.calcHist([hsv2], [1], None, [256], [0, 256])
        v2 = cv2.calcHist([hsv2], [2], None, [256], [0, 256])
        
        # Compare histograms
        h_sim = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
        s_sim = cv2.compareHist(s1, s2, cv2.HISTCMP_CORREL)
        v_sim = cv2.compareHist(v1, v2, cv2.HISTCMP_CORREL)
        
        # Weighted average (hue is most important for color matching)
        color_sim = (h_sim * 0.5 + s_sim * 0.3 + v_sim * 0.2)
        return max(0, color_sim)
    
    @staticmethod
    def calculate_layout_similarity(img1, img2):
        """Calculate layout/composition similarity"""
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Divide image into regions and compare brightness
        h, w = gray1.shape
        regions_sim = []
        
        # Compare top, middle, bottom regions
        for i in range(3):
            y_start = i * h // 3
            y_end = (i + 1) * h // 3
            
            region1 = gray1[y_start:y_end, :]
            region2 = gray2[y_start:y_end, :]
            
            mean1 = np.mean(region1)
            mean2 = np.mean(region2)
            
            # Similarity based on brightness difference
            diff = abs(mean1 - mean2) / 255.0
            regions_sim.append(1 - diff)
        
        return np.mean(regions_sim)
    
    @staticmethod
    def calculate_edge_similarity(img1, img2):
        """Calculate edge/structure similarity"""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Detect edges
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # Compare edge patterns
        edge_diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float))) / 255.0
        return 1 - edge_diff
    
    @classmethod
    def calculate_similarity(cls, generated_image, target_image):
        """Calculate comprehensive similarity score"""
        # Resize if needed
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
        
        # Calculate different aspects
        color_sim = cls.calculate_color_similarity(generated_image, target_image)
        layout_sim = cls.calculate_layout_similarity(generated_image, target_image)
        edge_sim = cls.calculate_edge_similarity(generated_image, target_image)
        
        # Weighted combination (color is most important for visual similarity)
        combined = (color_sim * 0.5 + layout_sim * 0.3 + edge_sim * 0.2)
        
        return {
            'combined': max(0, min(1, combined)),
            'color': max(0, color_sim),
            'layout': max(0, layout_sim),
            'structure': max(0, edge_sim)
        }

class ChallengeImageManager:
    """Manages challenge images from various sources"""
    
    def __init__(self):
        self.challenges = self.create_challenge_set()
    
    def create_challenge_set(self):
        """Create a set of 7 diverse challenge images"""
        challenges = []
        
        # Challenge 1: Sunset Landscape
        challenge1 = self.create_sunset_landscape()
        challenges.append({
            'id': 1,
            'name': 'Golden Sunset',
            'image': challenge1,
            'description': 'A warm sunset scene with golden/orange colors',
            'keywords': ['sunset', 'golden', 'warm', 'orange', 'landscape'],
            'difficulty': 'Easy'
        })
        
        # Challenge 2: Mountain Lake
        challenge2 = self.create_mountain_lake()
        challenges.append({
            'id': 2,
            'name': 'Mountain Lake',
            'image': challenge2,
            'description': 'A serene lake surrounded by mountains',
            'keywords': ['lake', 'mountains', 'reflection', 'nature', 'peaceful'],
            'difficulty': 'Medium'
        })
        
        # Challenge 3: City Skyline
        challenge3 = self.create_city_skyline()
        challenges.append({
            'id': 3,
            'name': 'Urban Skyline',
            'image': challenge3,
            'description': 'A modern city skyline at dusk',
            'keywords': ['city', 'skyline', 'urban', 'buildings', 'dusk'],
            'difficulty': 'Medium'
        })
        
        # Challenge 4: Forest Path
        challenge4 = self.create_forest_scene()
        challenges.append({
            'id': 4,
            'name': 'Forest Path',
            'image': challenge4,
            'description': 'A path through a dense forest',
            'keywords': ['forest', 'trees', 'path', 'green', 'nature'],
            'difficulty': 'Hard'
        })
        
        # Challenge 5: Desert Dunes
        challenge5 = self.create_desert_scene()
        challenges.append({
            'id': 5,
            'name': 'Desert Dunes',
            'image': challenge5,
            'description': 'Rolling sand dunes in a desert',
            'keywords': ['desert', 'sand', 'dunes', 'arid', 'golden'],
            'difficulty': 'Medium'
        })
        
        # Challenge 6: Ocean Waves
        challenge6 = self.create_ocean_scene()
        challenges.append({
            'id': 6,
            'name': 'Ocean Waves',
            'image': challenge6,
            'description': 'Ocean waves under a blue sky',
            'keywords': ['ocean', 'waves', 'blue', 'water', 'seascape'],
            'difficulty': 'Easy'
        })
        
        # Challenge 7: Night Sky
        challenge7 = self.create_night_scene()
        challenges.append({
            'id': 7,
            'name': 'Starry Night',
            'image': challenge7,
            'description': 'A starry night sky over a landscape',
            'keywords': ['night', 'stars', 'moon', 'dark', 'celestial'],
            'difficulty': 'Hard'
        })
        
        return challenges
    
    def create_sunset_landscape(self):
        """Create a sunset landscape challenge"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sunset gradient
        for y in range(height // 2):
            intensity = 1.0 - (y / (height // 2))
            image[y, :, 0] = int(255 * intensity * 0.95)
            image[y, :, 1] = int(255 * intensity * 0.8)
            image[y, :, 2] = int(255 * intensity * 0.3)
        
        # Ground
        image[height//2:, :] = [60, 80, 40]
        
        # Sun
        cv2.circle(image, (400, 120), 40, (255, 255, 220), -1)
        
        # Mountain silhouette
        for x in range(width):
            mountain_height = int(height * 0.25 * (0.6 + 0.4 * np.sin(x * 0.01)))
            y_start = height//2 - mountain_height
            image[y_start:height//2, x] = [30, 30, 30]
        
        return image
    
    def create_mountain_lake(self):
        """Create a mountain lake scene"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky
        image[:height//2, :] = [135, 206, 235]
        
        # Lake (reflection)
        image[height//2:, :] = [70, 130, 180]
        
        # Mountains
        for x in range(width):
            mountain_height = int(height * 0.4 * (0.7 + 0.3 * np.sin(x * 0.005)))
            y_start = height//2 - mountain_height
            if y_start >= 0:
                image[y_start:height//2, x] = [100, 100, 100]
        
        # Add some clouds
        cv2.ellipse(image, (150, 80), (60, 30), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(image, (350, 60), (50, 25), 0, 0, 360, (255, 255, 255), -1)
        
        return image
    
    def create_city_skyline(self):
        """Create a city skyline"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Dusk sky
        for y in range(height // 2):
            intensity = 1.0 - (y / (height // 2))
            image[y, :, 0] = int(100 + 155 * intensity * 0.3)
            image[y, :, 1] = int(100 + 155 * intensity * 0.5)
            image[y, :, 2] = int(150 + 105 * intensity * 0.8)
        
        # Ground
        image[height//2:, :] = [40, 40, 40]
        
        # Buildings
        building_positions = [50, 120, 180, 250, 320, 380, 450]
        for x in building_positions:
            building_height = random.randint(100, 250)
            building_width = random.randint(30, 50)
            y_start = height//2 - building_height
            x_end = min(width, x + building_width)
            
            if y_start >= 0:
                image[y_start:height//2, x:x_end] = [60, 60, 60]
                
                # Add lit windows
                for window_y in range(y_start + 20, height//2 - 10, 25):
                    for window_x in range(x + 5, x_end - 5, 15):
                        if random.random() > 0.6:
                            image[window_y:window_y+8, window_x:window_x+8] = [255, 255, 200]
        
        return image
    
    def create_forest_scene(self):
        """Create a forest scene"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky through trees
        image[:height//3, :] = [100, 150, 100]
        
        # Forest floor
        image[2*height//3:, :] = [34, 80, 34]
        
        # Trees
        for x in range(0, width, 25):
            tree_height = random.randint(200, 350)
            tree_width = random.randint(20, 35)
            y_start = height - tree_height
            x_start = max(0, x - tree_width//2)
            x_end = min(width, x + tree_width//2)
            
            if y_start >= 0:
                # Tree trunk
                trunk_width = tree_width // 4
                trunk_x_start = x - trunk_width//2
                trunk_x_end = x + trunk_width//2
                image[height-50:height, trunk_x_start:trunk_x_end] = [101, 67, 33]
                
                # Tree foliage
                image[y_start:height-50, x_start:x_end] = [34, 139, 34]
        
        # Path
        path_y_start = 2*height//3
        for y in range(path_y_start, height):
            path_width = int(80 * (1 - (y - path_y_start) / (height - path_y_start)))
            path_x_start = width//2 - path_width//2
            path_x_end = width//2 + path_width//2
            image[y, path_x_start:path_x_end] = [139, 119, 101]
        
        return image
    
    def create_desert_scene(self):
        """Create a desert scene"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Desert sky
        image[:height//2, :] = [255, 218, 185]
        
        # Sand dunes
        for x in range(width):
            dune_height = int(height * 0.3 * (0.5 + 0.5 * np.sin(x * 0.02)))
            y_start = height//2 + dune_height
            image[y_start:height, x] = [194, 178, 128]
        
        # Sun
        cv2.circle(image, (100, 100), 50, (255, 255, 200), -1)
        
        return image
    
    def create_ocean_scene(self):
        """Create an ocean scene"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Blue sky
        image[:height//2, :] = [135, 206, 235]
        
        # Ocean
        image[height//2:, :] = [25, 25, 112]
        
        # Waves (lighter blue stripes)
        for y in range(height//2, height, 20):
            wave_intensity = random.uniform(0.3, 0.7)
            image[y:y+5, :] = [int(25 + 100*wave_intensity), int(25 + 150*wave_intensity), int(112 + 100*wave_intensity)]
        
        # Clouds
        for _ in range(3):
            cloud_x = random.randint(50, width-100)
            cloud_y = random.randint(30, height//3)
            cv2.ellipse(image, (cloud_x, cloud_y), (70, 35), 0, 0, 360, (255, 255, 255), -1)
        
        return image
    
    def create_night_scene(self):
        """Create a night scene"""
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Night sky
        image[:2*height//3, :] = [25, 25, 112]
        
        # Ground
        image[2*height//3:, :] = [34, 34, 34]
        
        # Moon
        cv2.circle(image, (400, 100), 40, (240, 240, 240), -1)
        
        # Stars
        for _ in range(50):
            star_x = random.randint(0, width)
            star_y = random.randint(0, 2*height//3)
            image[star_y:star_y+2, star_x:star_x+2] = [255, 255, 255]
        
        # Hill silhouette
        for x in range(width):
            hill_height = int(height * 0.2 * (0.5 + 0.5 * np.sin(x * 0.015)))
            y_start = 2*height//3 - hill_height
            image[y_start:2*height//3, x] = [20, 20, 20]
        
        return image
    
    def get_challenge(self, challenge_id):
        """Get a specific challenge by ID"""
        for challenge in self.challenges:
            if challenge['id'] == challenge_id:
                return challenge
        return None
    
    def get_random_challenge(self):
        """Get a random challenge"""
        return random.choice(self.challenges)
    
    def list_challenges(self):
        """List all available challenges"""
        return self.challenges

class ChallengeGame:
    """Main challenge game with improved scoring and real challenges"""
    
    def __init__(self):
        print("🎯 Initializing Challenge Game...")
        
        # Initialize components
        self.engine = MockStableDiffusionEngine()
        self.similarity_calc = ImprovedSimilarityCalculator()
        self.challenge_manager = ChallengeImageManager()
        
        # Game state
        self.current_challenge = None
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        # Create output directory
        os.makedirs("challenge_attempts", exist_ok=True)
        
        print("✅ Challenge Game initialized!")
    
    def select_challenge(self, challenge_id=None):
        """Select a challenge to play"""
        if challenge_id:
            self.current_challenge = self.challenge_manager.get_challenge(challenge_id)
        else:
            self.current_challenge = self.challenge_manager.get_random_challenge()
        
        if self.current_challenge:
            # Save challenge image
            challenge_file = f"challenge_{self.current_challenge['id']}_{self.current_challenge['name'].replace(' ', '_')}.jpg"
            cv2.imwrite(challenge_file, self.current_challenge['image'])
            
            print(f"🎯 Selected Challenge #{self.current_challenge['id']}: {self.current_challenge['name']}")
            print(f"📝 Description: {self.current_challenge['description']}")
            print(f"🎚️ Difficulty: {self.current_challenge['difficulty']}")
            print(f"💾 Challenge image saved as: {challenge_file}")
            
            return True
        return False
    
    def show_target_image(self):
        """Display the current challenge image"""
        if not self.current_challenge:
            print("❌ No challenge selected!")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Convert BGR to RGB
        target_rgb = cv2.cvtColor(self.current_challenge['image'], cv2.COLOR_BGR2RGB)
        
        plt.imshow(target_rgb)
        plt.title(f"Challenge #{self.current_challenge['id']}: {self.current_challenge['name']}\n{self.current_challenge['description']}", 
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        
        # Add difficulty and keywords
        plt.figtext(0.5, 0.02, 
                   f"Difficulty: {self.current_challenge['difficulty']} | "
                   f"Keywords: {', '.join(self.current_challenge['keywords'][:3])}...",
                   ha='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        
        # Save display
        display_file = f"TARGET_Challenge_{self.current_challenge['id']}.png"
        plt.savefig(display_file, dpi=150, bbox_inches='tight')
        
        plt.show()
        
        print(f"🎯 Target saved as: {display_file}")
        print("💡 Your goal: Create a prompt that generates a similar image!")
    
    def make_attempt(self, prompt):
        """Process an attempt with improved scoring"""
        if not self.current_challenge:
            print("❌ No challenge selected!")
            return None
        
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        
        # Generate image
        generated_image = self.engine(prompt)
        
        # Save generated image
        gen_file = f"challenge_attempts/challenge_{self.current_challenge['id']}_attempt_{self.current_attempt:03d}.jpg"
        cv2.imwrite(gen_file, generated_image)
        
        # Calculate improved similarity
        scores = self.similarity_calc.calculate_similarity(generated_image, self.current_challenge['image'])
        combined_score = scores['combined']
        
        # Update best score
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 NEW BEST SCORE!")
        
        # Display detailed results
        print(f"📊 SIMILARITY ANALYSIS:")
        print(f"   🎨 Overall Score: {combined_score:.3f}")
        print(f"   🌈 Color Match: {scores['color']:.3f}")
        print(f"   📐 Layout Match: {scores['layout']:.3f}")
        print(f"   🔍 Structure Match: {scores['structure']:.3f}")
        
        # Show comparison
        self.display_comparison(generated_image, prompt, scores)
        
        # Provide intelligent feedback
        feedback = self.get_intelligent_feedback(scores, prompt)
        print(f"💬 {feedback}")
        
        # Save attempt
        attempt_data = {
            'challenge_id': self.current_challenge['id'],
            'attempt': self.current_attempt,
            'prompt': prompt,
            'scores': scores,
            'combined_score': combined_score,
            'is_best': is_best,
            'generated_image_path': gen_file,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        return {
            'scores': scores,
            'feedback': feedback,
            'is_best': is_best
        }
    
    def display_comparison(self, generated_image, prompt, scores):
        """Display target vs generated comparison"""
        plt.figure(figsize=(16, 8))
        
        # Convert images
        target_rgb = cv2.cvtColor(self.current_challenge['image'], cv2.COLOR_BGR2RGB)
        generated_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
        
        # Target image
        plt.subplot(1, 2, 1)
        plt.imshow(target_rgb)
        plt.title(f"TARGET: {self.current_challenge['name']}", fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Generated image
        plt.subplot(1, 2, 2)
        plt.imshow(generated_rgb)
        plt.title(f"GENERATED (Score: {scores['combined']:.3f})\nColor: {scores['color']:.3f} | Layout: {scores['layout']:.3f} | Structure: {scores['structure']:.3f}", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        
        # Add prompt as figure title
        plt.suptitle(f"Attempt #{self.current_attempt}: '{prompt}'", fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        # Save comparison
        comparison_file = f"challenge_attempts/challenge_{self.current_challenge['id']}_attempt_{self.current_attempt:03d}_comparison.png"
        plt.savefig(comparison_file, dpi=150, bbox_inches='tight')
        
        plt.show()
        
        print(f"💾 Comparison saved: {comparison_file}")
    
    def get_intelligent_feedback(self, scores, prompt):
        """Provide intelligent feedback based on scores and challenge"""
        combined = scores['combined']
        color = scores['color']
        layout = scores['layout']
        structure = scores['structure']
        
        if combined >= 0.85:
            return "🎉 Outstanding! You've mastered this challenge!"
        elif combined >= 0.70:
            return "👍 Excellent work! You're very close to the target."
        elif combined >= 0.50:
            feedback = "🤔 Good progress! "
            if color < 0.5:
                feedback += "Focus on matching the colors better. "
            if layout < 0.5:
                feedback += "Consider the overall composition. "
            if structure < 0.5:
                feedback += "Think about the main elements and their arrangement."
            return feedback
        else:
            feedback = "💪 Keep experimenting! "
            
            # Specific hints based on challenge type
            challenge_keywords = self.current_challenge['keywords']
            prompt_lower = prompt.lower()
            
            missing_keywords = [kw for kw in challenge_keywords[:3] if kw not in prompt_lower]
            if missing_keywords:
                feedback += f"Try including: {', '.join(missing_keywords)}. "
            
            if color < 0.3:
                feedback += "Pay attention to the dominant colors in the target. "
            
            return feedback
    
    def show_progress(self):
        """Show current progress"""
        if not self.current_challenge:
            print("❌ No challenge selected!")
            return
        
        print(f"\n📈 CHALLENGE PROGRESS:")
        print(f"   Challenge: #{self.current_challenge['id']} - {self.current_challenge['name']}")
        print(f"   Attempts: {self.current_attempt}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
        
        if len(self.attempts) > 1:
            recent_scores = [a['combined_score'] for a in self.attempts[-5:]]
            print(f"   Recent Scores: {[f'{s:.3f}' for s in recent_scores]}")
    
    def check_victory(self, threshold=0.80):
        """Check for victory"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 CHALLENGE COMPLETED! 🎉🎉🎉")
            print(f"🏆 Challenge: {self.current_challenge['name']}")
            print(f"🎯 Final Score: {self.best_score:.3f}")
            print(f"✨ Winning Prompt: '{self.best_prompt}'")
            print(f"📊 Total Attempts: {self.current_attempt}")
            return True
        return False
    
    def list_all_challenges(self):
        """List all available challenges"""
        print("\n🎯 AVAILABLE CHALLENGES:")
        print("=" * 50)
        
        for challenge in self.challenge_manager.list_challenges():
            print(f"{challenge['id']}. {challenge['name']} ({challenge['difficulty']})")
            print(f"   📝 {challenge['description']}")
            print(f"   🏷️ Keywords: {', '.join(challenge['keywords'])}")
            print()

def main():
    """Main game function"""
    print("🎯 REVERSE PROMPT ENGINEERING CHALLENGE GAME")
    print("=" * 60)
    print("🎮 Features:")
    print("• 7 diverse challenge images")
    print("• Improved similarity scoring")
    print("• Detailed feedback and hints")
    print("• Progress tracking")
    print("=" * 60)
    
    game = ChallengeGame()
    
    # Show available challenges
    game.list_all_challenges()
    
    # Let user select challenge
    while True:
        try:
            choice = input("Select challenge (1-7) or 'random': ").strip().lower()
            
            if choice == 'random':
                if game.select_challenge():
                    break
            elif choice.isdigit() and 1 <= int(choice) <= 7:
                if game.select_challenge(int(choice)):
                    break
            else:
                print("❌ Please enter 1-7 or 'random'")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
    
    # Show target image
    game.show_target_image()
    
    print("\n" + "=" * 60)
    print("🎮 START PLAYING!")
    print("Commands: 'progress' = stats, 'target' = show target, 'challenges' = list all, 'quit' = exit")
    print("=" * 60)
    
    # Game loop
    while True:
        try:
            prompt = input(f"\n[Attempt #{game.current_attempt + 1}] Enter your prompt: ").strip()
            
            if prompt.lower() == 'quit':
                print("👋 Thanks for playing!")
                break
            elif prompt.lower() == 'progress':
                game.show_progress()
                continue
            elif prompt.lower() == 'target':
                game.show_target_image()
                continue
            elif prompt.lower() == 'challenges':
                game.list_all_challenges()
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt or command")
                continue
            
            # Make attempt
            result = game.make_attempt(prompt)
            
            if result and game.check_victory():
                break
            
            # Show progress
            game.show_progress()
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Game interrupted")
            break

if __name__ == "__main__":
    main()