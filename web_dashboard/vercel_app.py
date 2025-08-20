#!/usr/bin/env python3
"""
Vercel-optimized version of AI Prompt Game Dashboard
Ultra-simplified for serverless deployment
"""

from flask import Flask, render_template, request, jsonify
import base64
import io
from PIL import Image
import json
from datetime import datetime
import requests
import numpy as np

app = Flask(__name__)
app.secret_key = 'ai-prompt-game-vercel-2024'

# Ultra-simplified image generator for Vercel
class SimpleImageGenerator:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"
    
    def generate(self, prompt, width=512, height=512):
        """Generate image using Pollinations.ai"""
        try:
            # Clean and encode prompt
            clean_prompt = prompt.replace(' ', '%20').replace(',', '%2C')
            url = f"{self.base_url}{clean_prompt}?width={width}&height={height}&nologo=true"
            
            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Return PIL image directly
            image = Image.open(io.BytesIO(response.content))
            return image
            
        except Exception as e:
            print(f"Generation error: {e}")
            return None

# Ultra-simplified comparison for Vercel
class SimpleComparison:
    def compare(self, img1, img2):
        """Ultra-simplified comparison for serverless"""
        try:
            # Convert to grayscale and compare basic similarity
            if img1.size != img2.size:
                img1 = img1.resize(img2.size)
            
            # Convert to arrays
            arr1 = np.array(img1.convert('L'))
            arr2 = np.array(img2.convert('L'))
            
            # Simple pixel difference
            diff = np.abs(arr1.astype(float) - arr2.astype(float))
            similarity = 1.0 - (np.mean(diff) / 255.0)
            
            # Add some randomness for demo purposes
            import random
            base_score = max(0.1, min(0.9, similarity + random.uniform(-0.2, 0.2)))
            
            return {
                'combined': base_score,
                'perceptual': base_score + random.uniform(-0.1, 0.1),
                'semantic': base_score + random.uniform(-0.1, 0.1),
                'structural': base_score + random.uniform(-0.1, 0.1),
                'color_advanced': base_score + random.uniform(-0.1, 0.1),
                'texture': base_score + random.uniform(-0.1, 0.1)
            }
            
        except Exception as e:
            print(f"Comparison error: {e}")
            return {
                'combined': 0.5,
                'perceptual': 0.5,
                'semantic': 0.5,
                'structural': 0.5,
                'color_advanced': 0.5,
                'texture': 0.5
            }
    
    def explain_scores(self, scores):
        """Generate explanations"""
        explanations = []
        combined = scores.get('combined', 0)
        
        if combined > 0.8:
            explanations.append("✅ Excellent match! Great job with your prompt!")
        elif combined > 0.6:
            explanations.append("🤔 Good similarity, but try to be more specific")
        elif combined > 0.4:
            explanations.append("⚠️ Some similarity, focus on key details")
        else:
            explanations.append("🔄 Low similarity, try a different approach")
        
        explanations.append("💡 Describe colors, objects, and style clearly")
        explanations.append("🎯 Be specific about composition and lighting")
        
        return explanations

# Initialize components
generator = SimpleImageGenerator()
comparator = SimpleComparison()

# Embedded target images (base64 encoded small versions for demo)
TARGET_IMAGES = {
    'cat': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=',
    'coffee': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k='
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('vercel_dashboard.html')

@app.route('/api/targets')
def get_targets():
    """Get available challenge targets"""
    targets = [
        {'id': 'cat', 'name': 'Cat', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '🐱'},
        {'id': 'coffee', 'name': 'Coffee', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '☕'},
        {'id': 'car', 'name': 'Car', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🚗'},
        {'id': 'foxes', 'name': 'Foxes', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦊'},
        {'id': 'llama', 'name': 'Llama', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦙'},
        {'id': 'owl', 'name': 'Owl', 'difficulty': 'Hard', 'threshold': 0.55, 'emoji': '🦉'}
    ]
    return jsonify(targets)

@app.route('/api/start_challenge', methods=['POST'])
def start_challenge():
    """Start a new challenge"""
    data = request.json
    target_id = data.get('target_id')
    
    # For demo, return a placeholder image
    target_image = TARGET_IMAGES.get(target_id, TARGET_IMAGES['cat'])
    
    return jsonify({
        'success': True,
        'target_image': target_image,
        'target_id': target_id
    })

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """Generate image from prompt and compare"""
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        # Generate image
        generated_image = generator.generate(prompt)
        
        if generated_image is None:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        # Create a simple target for comparison (placeholder)
        target_image = np.ones((256, 256, 3), dtype=np.uint8) * 128
        
        # Create a simple target for comparison (placeholder)
        target_image = Image.new('RGB', (256, 256), color='lightgray')
        
        # Compare images
        scores = comparator.compare(generated_image, target_image)
        
        # Get explanations
        explanations = comparator.explain_scores(scores)
        
        # Check passing criteria
        threshold = 0.65  # Default threshold
        passed = scores['combined'] >= threshold
        
        passing_result = {
            'passed': passed,
            'message': f"Score: {scores['combined']:.3f} (Required: {threshold:.3f})",
            'threshold': threshold
        }
        
        # Convert images to base64
        generated_b64 = pil_to_base64(generated_image)
        
        return jsonify({
            'success': True,
            'generated_image': generated_b64,
            'scores': scores,
            'explanations': explanations,
            'passing_result': passing_result,
            'attempt_number': 1,
            'is_best': True,
            'best_score': scores['combined']
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

def pil_to_base64(image):
    """Convert PIL image to base64 string"""
    try:
        # Convert to base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Image conversion error: {e}")
        return ""

# For Vercel
if __name__ == "__main__":
    app.run(debug=False)