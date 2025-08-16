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
        """Generate a mock image based on prompt keywords - High definition output"""
        print(f"🔄 Generating HD image for: '{prompt}'")
        
        # Use high definition resolution to match target images
        height, width = 1024, 1024
        image = np.zeros((height, width, 3), dtype=np.uint8)
        prompt_lower = prompt.lower()
        
        # Child-friendly image generation based on keywords
        
        # House-related keywords
        if "house" in prompt_lower or "home" in prompt_lower:
            return self._generate_house_image(height, width, prompt_lower)
        
        # Cat-related keywords
        elif "cat" in prompt_lower or "kitten" in prompt_lower:
            return self._generate_cat_image(height, width, prompt_lower)
        
        # Rainbow-related keywords
        elif "rainbow" in prompt_lower or "colorful" in prompt_lower:
            return self._generate_rainbow_image(height, width, prompt_lower)
        
        # Tree-related keywords
        elif "tree" in prompt_lower or "forest" in prompt_lower:
            return self._generate_tree_image(height, width, prompt_lower)
        
        # Car-related keywords
        elif "car" in prompt_lower or "vehicle" in prompt_lower:
            return self._generate_car_image(height, width, prompt_lower)
        
        # Flower-related keywords
        elif "flower" in prompt_lower or "garden" in prompt_lower:
            return self._generate_flower_image(height, width, prompt_lower)
        
        # Butterfly-related keywords
        elif "butterfly" in prompt_lower or "insect" in prompt_lower:
            return self._generate_butterfly_image(height, width, prompt_lower)
        
        # Geometric shapes
        elif any(shape in prompt_lower for shape in ["circle", "square", "triangle", "shape", "geometry"]):
            return self._generate_shapes_image(height, width, prompt_lower)
        
        # Fallback - simple colorful background
        else:
            return self._generate_simple_image(height, width, prompt_lower)
    
    def _generate_house_image(self, height, width, prompt_lower):
        """Generate a simple house based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky
        sky_color = [255, 200, 100] if "blue" in prompt_lower else [255, 200, 100]
        image[:height//2, :] = sky_color
        
        # Ground
        ground_color = [50, 200, 50] if "green" in prompt_lower else [50, 200, 50]
        image[height//2:, :] = ground_color
        
        # House body
        house_color = [0, 0, 255] if "red" in prompt_lower else [0, 0, 255]
        house_top, house_bottom = int(height * 0.4), int(height * 0.7)
        house_left, house_right = int(width * 0.3), int(width * 0.7)
        image[house_top:house_bottom, house_left:house_right] = house_color
        
        # Roof
        roof_peak = int(height * 0.25)
        roof_points = np.array([
            [house_left - 50, house_top],
            [house_right + 50, house_top],
            [width//2, roof_peak]
        ], np.int32)
        cv2.fillPoly(image, [roof_points], (150, 75, 0))
        
        # Door
        door_width, door_height = int(width * 0.08), int(height * 0.15)
        door_left = width//2 - door_width//2
        door_top = house_bottom - door_height
        image[door_top:house_bottom, door_left:door_left+door_width] = [0, 255, 255]
        
        # Windows
        window_size = int(width * 0.06)
        win_y = house_top + int(height * 0.08)
        image[win_y:win_y+window_size, house_left+50:house_left+50+window_size] = [255, 255, 255]
        image[win_y:win_y+window_size, house_right-50-window_size:house_right-50] = [255, 255, 255]
        
        if "sun" in prompt_lower:
            cv2.circle(image, (int(width * 0.8), int(height * 0.2)), 80, (0, 255, 255), -1)
        
        return image
    
    def _generate_cat_image(self, height, width, prompt_lower):
        """Generate a simple cat based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background
        bg_color = [200, 150, 255] if "purple" in prompt_lower else [200, 150, 255]
        image[:, :] = bg_color
        
        # Cat face
        face_color = [0, 150, 255] if "orange" in prompt_lower else [0, 150, 255]
        cv2.circle(image, (width//2, height//2), 200, face_color, -1)
        
        # Ears
        ear_left = np.array([
            [width//2 - 120, height//2 - 150],
            [width//2 - 180, height//2 - 250],
            [width//2 - 60, height//2 - 200]
        ], np.int32)
        cv2.fillPoly(image, [ear_left], face_color)
        
        ear_right = np.array([
            [width//2 + 120, height//2 - 150],
            [width//2 + 180, height//2 - 250],
            [width//2 + 60, height//2 - 200]
        ], np.int32)
        cv2.fillPoly(image, [ear_right], face_color)
        
        # Eyes
        cv2.circle(image, (width//2 - 60, height//2 - 40), 25, (0, 0, 0), -1)
        cv2.circle(image, (width//2 + 60, height//2 - 40), 25, (0, 0, 0), -1)
        
        # Nose
        nose = np.array([
            [width//2, height//2 + 10],
            [width//2 - 15, height//2 + 30],
            [width//2 + 15, height//2 + 30]
        ], np.int32)
        cv2.fillPoly(image, [nose], (255, 0, 255))
        
        return image
    
    def _generate_rainbow_image(self, height, width, prompt_lower):
        """Generate a rainbow based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky background
        image[:, :] = [255, 200, 150]
        
        # Rainbow
        rainbow_colors = [
            [0, 0, 255], [0, 165, 255], [0, 255, 255], [0, 255, 0],
            [255, 0, 0], [255, 0, 127], [255, 0, 255]
        ]
        
        center_x, center_y = width//2, int(height * 0.8)
        for i, color in enumerate(rainbow_colors):
            radius = 300 - i * 35
            cv2.ellipse(image, (center_x, center_y), (radius, radius), 0, 0, 180, color, 30)
        
        # Clouds
        cv2.circle(image, (100, int(height * 0.6)), 60, (255, 255, 255), -1)
        cv2.circle(image, (width-100, int(height * 0.6)), 60, (255, 255, 255), -1)
        
        return image
    
    def _generate_tree_image(self, height, width, prompt_lower):
        """Generate a tree based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky and ground
        image[:height//2, :] = [255, 255, 0]  # Cyan sky
        image[height//2:, :] = [0, 200, 0]    # Green ground
        
        # Tree trunk
        trunk_width = 80
        trunk_height = 300
        trunk_left = width//2 - trunk_width//2
        trunk_bottom = int(height * 0.8)
        trunk_top = trunk_bottom - trunk_height
        image[trunk_top:trunk_bottom, trunk_left:trunk_left+trunk_width] = [0, 100, 139]
        
        # Tree crown
        cv2.circle(image, (width//2, trunk_top - 100), 200, (0, 200, 0), -1)
        
        return image
    
    def _generate_car_image(self, height, width, prompt_lower):
        """Generate a car based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky and road
        image[:height//2, :] = [255, 200, 100]
        image[height//2:, :] = [100, 100, 100]
        
        # Car body
        car_width, car_height = 400, 150
        car_left = width//2 - car_width//2
        car_bottom = int(height * 0.7)
        car_top = car_bottom - car_height
        image[car_top:car_bottom, car_left:car_left+car_width] = [0, 0, 255]
        
        # Wheels
        wheel_y = car_bottom + 30
        cv2.circle(image, (car_left + 80, wheel_y), 50, (0, 0, 0), -1)
        cv2.circle(image, (car_left + car_width - 80, wheel_y), 50, (0, 0, 0), -1)
        
        return image
    
    def _generate_flower_image(self, height, width, prompt_lower):
        """Generate a flower based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background
        image[:, :] = [150, 255, 150]
        
        # Flower center
        cv2.circle(image, (width//2, height//2), 50, (0, 255, 255), -1)
        
        # Petals
        petal_positions = [
            (width//2, height//2 - 120), (width//2 + 85, height//2 - 85),
            (width//2 + 120, height//2), (width//2 + 85, height//2 + 85),
            (width//2, height//2 + 120), (width//2 - 85, height//2 + 85),
            (width//2 - 120, height//2), (width//2 - 85, height//2 - 85)
        ]
        
        for pos in petal_positions:
            cv2.circle(image, pos, 60, (255, 0, 255), -1)
        
        return image
    
    def _generate_butterfly_image(self, height, width, prompt_lower):
        """Generate a butterfly based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background
        image[:, :] = [150, 255, 255]
        
        # Body
        body_width = 15
        body_height = 250
        body_left = width//2 - body_width//2
        body_top = height//2 - body_height//2
        image[body_top:body_top+body_height, body_left:body_left+body_width] = [0, 0, 0]
        
        # Wings
        cv2.circle(image, (width//2 - 80, height//2 - 60), 80, (255, 0, 255), -1)
        cv2.circle(image, (width//2 + 80, height//2 - 60), 80, (0, 255, 255), -1)
        cv2.circle(image, (width//2 - 60, height//2 + 40), 60, (255, 150, 0), -1)
        cv2.circle(image, (width//2 + 60, height//2 + 40), 60, (0, 150, 255), -1)
        
        return image
    
    def _generate_shapes_image(self, height, width, prompt_lower):
        """Generate geometric shapes based on keywords"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background
        image[:, :] = [200, 200, 200]
        
        # Circle
        cv2.circle(image, (width//4, height//4), 100, (0, 0, 255), -1)
        
        # Square
        square_size = 200
        square_left = 3*width//4 - square_size//2
        square_top = height//4 - square_size//2
        image[square_top:square_top+square_size, square_left:square_left+square_size] = [255, 0, 0]
        
        # Triangle
        triangle = np.array([
            [width//4, 3*height//4 + 100],
            [width//4 - 100, 3*height//4 - 100],
            [width//4 + 100, 3*height//4 - 100]
        ], np.int32)
        cv2.fillPoly(image, [triangle], (0, 255, 0))
        
        return image
    
    def _generate_simple_image(self, height, width, prompt_lower):
        """Generate a simple colorful image as fallback"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Simple gradient background
        for y in range(height):
            intensity = y / height
            image[y, :, 0] = int(100 + 155 * intensity)
            image[y, :, 1] = int(150 + 105 * intensity)
            image[y, :, 2] = int(200 + 55 * intensity)
        
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
        """Create a challenging target image for students to match - High definition, high contrast, child-friendly"""
        # Upgrade to high definition resolution
        height, width = 1024, 1024
        
        # Choose a random child-friendly image type
        image_types = [
            'simple_house', 'rainbow', 'simple_cat', 'colorful_tree', 
            'geometric_shapes', 'simple_car', 'flower', 'butterfly'
        ]
        image_type = random.choice(image_types)
        
        if image_type == 'simple_house':
            return self._create_simple_house(height, width)
        elif image_type == 'rainbow':
            return self._create_rainbow(height, width)
        elif image_type == 'simple_cat':
            return self._create_simple_cat(height, width)
        elif image_type == 'colorful_tree':
            return self._create_colorful_tree(height, width)
        elif image_type == 'geometric_shapes':
            return self._create_geometric_shapes(height, width)
        elif image_type == 'simple_car':
            return self._create_simple_car(height, width)
        elif image_type == 'flower':
            return self._create_flower(height, width)
        else:  # butterfly
            return self._create_butterfly(height, width)
    
    def _create_simple_house(self, height, width):
        """Create a simple, high-contrast house perfect for children"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky - bright blue
        target[:height//2, :] = [255, 200, 100]  # Light blue sky
        
        # Ground - bright green
        target[height//2:, :] = [50, 200, 50]  # Bright green grass
        
        # House base - bright red
        house_bottom = int(height * 0.7)
        house_top = int(height * 0.4)
        house_left = int(width * 0.3)
        house_right = int(width * 0.7)
        target[house_top:house_bottom, house_left:house_right] = [0, 0, 255]  # Red house
        
        # Roof - dark blue triangle
        roof_peak = int(height * 0.25)
        roof_points = np.array([
            [house_left - 50, house_top],
            [house_right + 50, house_top],
            [width//2, roof_peak]
        ], np.int32)
        cv2.fillPoly(target, [roof_points], (150, 75, 0))  # Dark blue roof
        
        # Door - yellow rectangle
        door_width = int(width * 0.08)
        door_height = int(height * 0.15)
        door_left = width//2 - door_width//2
        door_right = width//2 + door_width//2
        door_top = house_bottom - door_height
        target[door_top:house_bottom, door_left:door_right] = [0, 255, 255]  # Yellow door
        
        # Windows - white squares
        window_size = int(width * 0.06)
        # Left window
        win_left_x = house_left + int(width * 0.05)
        win_left_y = house_top + int(height * 0.08)
        target[win_left_y:win_left_y+window_size, win_left_x:win_left_x+window_size] = [255, 255, 255]
        
        # Right window
        win_right_x = house_right - int(width * 0.05) - window_size
        target[win_left_y:win_left_y+window_size, win_right_x:win_right_x+window_size] = [255, 255, 255]
        
        # Sun - bright yellow circle
        cv2.circle(target, (int(width * 0.8), int(height * 0.2)), 80, (0, 255, 255), -1)
        
        return target
    
    def _create_rainbow(self, height, width):
        """Create a bright, colorful rainbow"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky - light blue
        target[:, :] = [255, 200, 150]  # Light blue background
        
        # Rainbow colors (BGR format)
        rainbow_colors = [
            [0, 0, 255],      # Red
            [0, 165, 255],    # Orange  
            [0, 255, 255],    # Yellow
            [0, 255, 0],      # Green
            [255, 0, 0],      # Blue
            [255, 0, 127],    # Indigo
            [255, 0, 255]     # Violet
        ]
        
        center_x, center_y = width//2, int(height * 0.8)
        
        # Draw rainbow arcs
        for i, color in enumerate(rainbow_colors):
            radius = 300 - i * 35
            thickness = 30
            cv2.ellipse(target, (center_x, center_y), (radius, radius), 
                       0, 0, 180, color, thickness)
        
        # Clouds at the ends
        cv2.circle(target, (100, int(height * 0.6)), 60, (255, 255, 255), -1)
        cv2.circle(target, (120, int(height * 0.6)), 50, (255, 255, 255), -1)
        cv2.circle(target, (80, int(height * 0.6)), 50, (255, 255, 255), -1)
        
        cv2.circle(target, (width-100, int(height * 0.6)), 60, (255, 255, 255), -1)
        cv2.circle(target, (width-120, int(height * 0.6)), 50, (255, 255, 255), -1)
        cv2.circle(target, (width-80, int(height * 0.6)), 50, (255, 255, 255), -1)
        
        return target
    
    def _create_simple_cat(self, height, width):
        """Create a simple, cute cat face"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background - light purple
        target[:, :] = [200, 150, 255]
        
        # Cat face - orange circle
        face_center = (width//2, height//2)
        face_radius = 200
        cv2.circle(target, face_center, face_radius, (0, 150, 255), -1)  # Orange face
        
        # Ears - orange triangles
        ear_left = np.array([
            [width//2 - 120, height//2 - 150],
            [width//2 - 180, height//2 - 250],
            [width//2 - 60, height//2 - 200]
        ], np.int32)
        cv2.fillPoly(target, [ear_left], (0, 150, 255))
        
        ear_right = np.array([
            [width//2 + 120, height//2 - 150],
            [width//2 + 180, height//2 - 250],
            [width//2 + 60, height//2 - 200]
        ], np.int32)
        cv2.fillPoly(target, [ear_right], (0, 150, 255))
        
        # Eyes - black circles
        cv2.circle(target, (width//2 - 60, height//2 - 40), 25, (0, 0, 0), -1)
        cv2.circle(target, (width//2 + 60, height//2 - 40), 25, (0, 0, 0), -1)
        
        # Nose - pink triangle
        nose = np.array([
            [width//2, height//2 + 10],
            [width//2 - 15, height//2 + 30],
            [width//2 + 15, height//2 + 30]
        ], np.int32)
        cv2.fillPoly(target, [nose], (255, 0, 255))
        
        # Mouth - black curve
        cv2.ellipse(target, (width//2, height//2 + 50), (40, 20), 0, 0, 180, (0, 0, 0), 3)
        
        return target
    
    def _create_colorful_tree(self, height, width):
        """Create a bright, colorful tree"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky - bright cyan
        target[:height//2, :] = [255, 255, 0]  # Cyan sky
        
        # Ground - green
        target[height//2:, :] = [0, 200, 0]
        
        # Tree trunk - brown rectangle
        trunk_width = 80
        trunk_height = 300
        trunk_left = width//2 - trunk_width//2
        trunk_right = width//2 + trunk_width//2
        trunk_bottom = int(height * 0.8)
        trunk_top = trunk_bottom - trunk_height
        target[trunk_top:trunk_bottom, trunk_left:trunk_right] = [0, 100, 139]  # Brown
        
        # Tree crown - large green circle
        crown_center = (width//2, trunk_top - 100)
        crown_radius = 200
        cv2.circle(target, crown_center, crown_radius, (0, 200, 0), -1)  # Green crown
        
        # Colorful fruits/decorations on tree
        fruit_positions = [
            (width//2 - 80, trunk_top - 50),
            (width//2 + 80, trunk_top - 50),
            (width//2, trunk_top - 150),
            (width//2 - 120, trunk_top - 120),
            (width//2 + 120, trunk_top - 120)
        ]
        
        fruit_colors = [(0, 0, 255), (0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0)]
        
        for pos, color in zip(fruit_positions, fruit_colors):
            cv2.circle(target, pos, 25, color, -1)
        
        return target
    
    def _create_geometric_shapes(self, height, width):
        """Create simple geometric shapes for learning"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background - light gray
        target[:, :] = [200, 200, 200]
        
        # Circle - red
        cv2.circle(target, (width//4, height//4), 100, (0, 0, 255), -1)
        
        # Square - blue
        square_size = 200
        square_left = 3*width//4 - square_size//2
        square_top = height//4 - square_size//2
        target[square_top:square_top+square_size, square_left:square_left+square_size] = [255, 0, 0]
        
        # Triangle - green
        triangle = np.array([
            [width//4, 3*height//4 + 100],
            [width//4 - 100, 3*height//4 - 100],
            [width//4 + 100, 3*height//4 - 100]
        ], np.int32)
        cv2.fillPoly(target, [triangle], (0, 255, 0))
        
        # Star - yellow
        star_center = (3*width//4, 3*height//4)
        star_points = []
        for i in range(10):
            angle = i * np.pi / 5
            if i % 2 == 0:
                radius = 100
            else:
                radius = 50
            x = int(star_center[0] + radius * np.cos(angle - np.pi/2))
            y = int(star_center[1] + radius * np.sin(angle - np.pi/2))
            star_points.append([x, y])
        
        star_points = np.array(star_points, np.int32)
        cv2.fillPoly(target, [star_points], (0, 255, 255))
        
        return target
    
    def _create_simple_car(self, height, width):
        """Create a simple, colorful car"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background - light blue sky
        target[:height//2, :] = [255, 200, 100]
        
        # Ground - gray road
        target[height//2:, :] = [100, 100, 100]
        
        # Car body - bright red rectangle
        car_width = 400
        car_height = 150
        car_left = width//2 - car_width//2
        car_right = width//2 + car_width//2
        car_bottom = int(height * 0.7)
        car_top = car_bottom - car_height
        target[car_top:car_bottom, car_left:car_right] = [0, 0, 255]  # Red car
        
        # Car roof - smaller rectangle
        roof_width = 250
        roof_height = 100
        roof_left = width//2 - roof_width//2
        roof_right = width//2 + roof_width//2
        roof_top = car_top - roof_height
        target[roof_top:car_top, roof_left:roof_right] = [0, 0, 200]  # Darker red roof
        
        # Wheels - black circles
        wheel_radius = 50
        wheel_y = car_bottom + 30
        cv2.circle(target, (car_left + 80, wheel_y), wheel_radius, (0, 0, 0), -1)
        cv2.circle(target, (car_right - 80, wheel_y), wheel_radius, (0, 0, 0), -1)
        
        # Windows - light blue
        window_margin = 20
        target[roof_top + window_margin:car_top - window_margin, 
               roof_left + window_margin:roof_right - window_margin] = [255, 255, 200]
        
        # Headlights - yellow circles
        cv2.circle(target, (car_right - 20, car_top + car_height//2), 20, (0, 255, 255), -1)
        
        return target
    
    def _create_flower(self, height, width):
        """Create a simple, colorful flower"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background - light green
        target[:, :] = [150, 255, 150]
        
        # Flower center - yellow circle
        center = (width//2, height//2)
        cv2.circle(target, center, 50, (0, 255, 255), -1)
        
        # Petals - pink/red circles around center
        petal_positions = [
            (width//2, height//2 - 120),      # top
            (width//2 + 85, height//2 - 85),  # top-right
            (width//2 + 120, height//2),      # right
            (width//2 + 85, height//2 + 85),  # bottom-right
            (width//2, height//2 + 120),      # bottom
            (width//2 - 85, height//2 + 85),  # bottom-left
            (width//2 - 120, height//2),      # left
            (width//2 - 85, height//2 - 85)   # top-left
        ]
        
        for pos in petal_positions:
            cv2.circle(target, pos, 60, (255, 0, 255), -1)  # Pink petals
        
        # Stem - green rectangle
        stem_width = 20
        stem_left = width//2 - stem_width//2
        stem_right = width//2 + stem_width//2
        stem_top = height//2 + 120
        stem_bottom = int(height * 0.9)
        target[stem_top:stem_bottom, stem_left:stem_right] = [0, 150, 0]
        
        # Leaves - green ovals
        cv2.ellipse(target, (width//2 - 50, height//2 + 200), (30, 60), -30, 0, 360, (0, 200, 0), -1)
        cv2.ellipse(target, (width//2 + 50, height//2 + 200), (30, 60), 30, 0, 360, (0, 200, 0), -1)
        
        return target
    
    def _create_butterfly(self, height, width):
        """Create a colorful butterfly"""
        target = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background - light yellow
        target[:, :] = [150, 255, 255]
        
        # Body - black rectangle
        body_width = 15
        body_height = 250
        body_left = width//2 - body_width//2
        body_right = width//2 + body_width//2
        body_top = height//2 - body_height//2
        body_bottom = height//2 + body_height//2
        target[body_top:body_bottom, body_left:body_right] = [0, 0, 0]
        
        # Upper wings - large colorful circles
        cv2.circle(target, (width//2 - 80, height//2 - 60), 80, (255, 0, 255), -1)  # Left upper wing - magenta
        cv2.circle(target, (width//2 + 80, height//2 - 60), 80, (0, 255, 255), -1)  # Right upper wing - yellow
        
        # Lower wings - smaller colorful circles  
        cv2.circle(target, (width//2 - 60, height//2 + 40), 60, (255, 150, 0), -1)  # Left lower wing - orange
        cv2.circle(target, (width//2 + 60, height//2 + 40), 60, (0, 150, 255), -1)  # Right lower wing - light blue
        
        # Wing patterns - small colored dots
        # Left upper wing dots
        cv2.circle(target, (width//2 - 100, height//2 - 80), 15, (0, 0, 255), -1)  # Red dot
        cv2.circle(target, (width//2 - 60, height//2 - 40), 15, (0, 255, 0), -1)   # Green dot
        
        # Right upper wing dots
        cv2.circle(target, (width//2 + 100, height//2 - 80), 15, (255, 0, 0), -1)  # Blue dot
        cv2.circle(target, (width//2 + 60, height//2 - 40), 15, (0, 255, 0), -1)   # Green dot
        
        # Antennae - black lines with small circles at ends
        cv2.line(target, (width//2 - 5, body_top), (width//2 - 30, body_top - 40), (0, 0, 0), 3)
        cv2.line(target, (width//2 + 5, body_top), (width//2 + 30, body_top - 40), (0, 0, 0), 3)
        cv2.circle(target, (width//2 - 30, body_top - 40), 8, (0, 0, 0), -1)
        cv2.circle(target, (width//2 + 30, body_top - 40), 8, (0, 0, 0), -1)
        
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