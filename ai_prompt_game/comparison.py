#!/usr/bin/env python3
"""
Image comparison module for scoring similarity
Enhanced with LLaVA vision model for intelligent semantic comparison
"""

import cv2
import numpy as np
import base64
import io
from PIL import Image
import requests
import json

class ImageComparison:
    """Handles image similarity comparison using multiple metrics including LLaVA"""
    
    def __init__(self, use_llava=True, llava_model="llava-v1.6-mistral-7b"):
        self.use_llava = use_llava
        self.llava_model = llava_model
        self.weights = {
            'structural': 0.20,
            'histogram': 0.20,
            'edges': 0.20,
            'colors': 0.15,
            'llava_semantic': 0.25  # LLaVA gets highest weight for semantic understanding
        }
        
        # Try to initialize LLaVA
        self.llava_available = False
        if use_llava:
            self.llava_available = self.init_llava()
    
    def init_llava(self):
        """Initialize LLaVA model for semantic comparison"""
        try:
            # Try to import transformers and load LLaVA
            from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
            import torch
            
            print("🔄 Loading LLaVA model for intelligent image comparison...")
            
            # Use a smaller, faster LLaVA model
            model_id = "llava-hf/llava-v1.6-mistral-7b-hf"
            
            self.llava_processor = LlavaNextProcessor.from_pretrained(model_id)
            
            # Load model with appropriate device
            if torch.cuda.is_available():
                self.llava_model = LlavaNextForConditionalGeneration.from_pretrained(
                    model_id, 
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True
                ).to("cuda")
                print("✅ LLaVA loaded on GPU")
            else:
                self.llava_model = LlavaNextForConditionalGeneration.from_pretrained(
                    model_id,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True
                )
                print("✅ LLaVA loaded on CPU (slower)")
            
            return True
            
        except ImportError:
            print("⚠️  LLaVA not available. Install with: pip install transformers torch")
            return False
        except Exception as e:
            print(f"⚠️  LLaVA initialization failed: {e}")
            return False
    
    def compare(self, generated_image, target_image):
        """
        Compare two images and return similarity scores
        
        Args:
            generated_image: Generated image (OpenCV format)
            target_image: Target image (OpenCV format)
            
        Returns:
            dict: Similarity scores for each metric plus combined score
        """
        # Ensure same size
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(
                generated_image, 
                (target_image.shape[1], target_image.shape[0])
            )
        
        # Calculate traditional metrics
        structural_sim = self.structural_similarity(generated_image, target_image)
        histogram_sim = self.histogram_similarity(generated_image, target_image)
        edge_sim = self.edge_similarity(generated_image, target_image)
        color_sim = self.dominant_color_similarity(generated_image, target_image)
        
        # Calculate LLaVA semantic similarity if available
        llava_sim = 0.5  # Default fallback score
        llava_explanation = "LLaVA not available"
        
        if self.llava_available:
            try:
                llava_sim, llava_explanation = self.llava_similarity(generated_image, target_image)
            except Exception as e:
                print(f"⚠️  LLaVA comparison failed: {e}")
                llava_sim = 0.5
                llava_explanation = "LLaVA comparison failed"
        
        # Calculate combined score
        if self.llava_available:
            combined = (
                structural_sim * self.weights['structural'] +
                histogram_sim * self.weights['histogram'] +
                edge_sim * self.weights['edges'] +
                color_sim * self.weights['colors'] +
                llava_sim * self.weights['llava_semantic']
            )
        else:
            # Fallback to traditional metrics only
            traditional_weights = {
                'structural': 0.30,
                'histogram': 0.25,
                'edges': 0.25,
                'colors': 0.20
            }
            combined = (
                structural_sim * traditional_weights['structural'] +
                histogram_sim * traditional_weights['histogram'] +
                edge_sim * traditional_weights['edges'] +
                color_sim * traditional_weights['colors']
            )
        
        return {
            'combined': max(0, min(1, combined)),
            'structural': max(0, structural_sim),
            'histogram': max(0, histogram_sim),
            'edges': max(0, edge_sim),
            'colors': max(0, color_sim),
            'llava_semantic': max(0, llava_sim),
            'llava_explanation': llava_explanation
        }
    
    def structural_similarity(self, img1, img2):
        """Calculate structural similarity using MSE"""
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate MSE
        mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)
        
        # Convert to similarity score
        max_mse = 255 * 255
        similarity = 1 - (mse / max_mse)
        
        return similarity
    
    def histogram_similarity(self, img1, img2):
        """Calculate color histogram similarity"""
        # Calculate 3D histograms
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        
        # Compare using correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        # Also try chi-square and intersection for robustness
        chi_square = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        intersection = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        
        # Normalize chi-square (lower is better, so invert)
        chi_square_norm = max(0, 1 - (chi_square / 1000000))
        
        # Normalize intersection
        intersection_norm = intersection / max(np.sum(hist1), np.sum(hist2))
        
        # Combine methods
        combined = (
            max(0, correlation) * 0.5 +
            chi_square_norm * 0.3 +
            intersection_norm * 0.2
        )
        
        return combined
    
    def edge_similarity(self, img1, img2):
        """Calculate edge pattern similarity"""
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Detect edges
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # Compare edge patterns
        edge_diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float))) / 255
        similarity = 1 - edge_diff
        
        return similarity
    
    def dominant_color_similarity(self, img1, img2):
        """Calculate dominant color similarity using k-means"""
        try:
            # Get dominant colors for both images
            colors1 = self.get_dominant_colors(img1, k=3)
            colors2 = self.get_dominant_colors(img2, k=3)
            
            # Calculate minimum distances between color sets
            distances = []
            for color1 in colors1:
                min_dist = float('inf')
                for color2 in colors2:
                    dist = np.linalg.norm(color1 - color2)
                    min_dist = min(min_dist, dist)
                distances.append(min_dist)
            
            # Convert to similarity score
            avg_distance = np.mean(distances)
            max_distance = 255 * np.sqrt(3)  # Maximum possible distance in RGB space
            similarity = 1 - (avg_distance / max_distance)
            
            return similarity
            
        except Exception:
            # Fallback to simple mean color comparison
            mean1 = np.mean(img1.reshape(-1, 3), axis=0)
            mean2 = np.mean(img2.reshape(-1, 3), axis=0)
            
            distance = np.linalg.norm(mean1 - mean2)
            similarity = 1 - (distance / (255 * np.sqrt(3)))
            
            return similarity
    
    def get_dominant_colors(self, image, k=3):
        """Extract dominant colors using k-means clustering"""
        # Reshape image to list of pixels
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        # Define criteria and apply k-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        return centers
    
    def llava_similarity(self, generated_image, target_image):
        """
        Use LLaVA to perform semantic image comparison
        
        Returns:
            tuple: (similarity_score, explanation)
        """
        try:
            # Convert OpenCV images to PIL
            target_pil = Image.fromarray(cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB))
            generated_pil = Image.fromarray(cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB))
            
            # Create comparison prompt
            prompt = """<image>

Look at these two images. The first image is the TARGET that we want to match. The second image is the GENERATED image that was created to match the target.

<image>

Please analyze how similar these images are and provide:
1. A similarity score from 0.0 to 1.0 (where 1.0 is perfect match)
2. A brief explanation of what matches and what doesn't

Focus on:
- Overall composition and subject matter
- Colors and lighting
- Style and mood
- Key visual elements

Respond in this exact format:
SCORE: [0.0-1.0]
EXPLANATION: [brief explanation]"""

            # Process images and prompt
            inputs = self.llava_processor(prompt, images=[target_pil, generated_pil], return_tensors="pt")
            
            # Move to same device as model
            if hasattr(self.llava_model, 'device'):
                inputs = {k: v.to(self.llava_model.device) for k, v in inputs.items()}
            
            # Generate response
            import torch
            with torch.no_grad():
                output = self.llava_model.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,
                    temperature=0.1
                )
            
            # Decode response
            response = self.llava_processor.decode(output[0], skip_special_tokens=True)
            
            # Extract score and explanation
            score, explanation = self.parse_llava_response(response)
            
            return score, explanation
            
        except Exception as e:
            print(f"⚠️  LLaVA comparison error: {e}")
            return 0.5, f"LLaVA error: {str(e)}"
    
    def parse_llava_response(self, response):
        """Parse LLaVA response to extract score and explanation"""
        try:
            # Look for SCORE: and EXPLANATION: patterns
            lines = response.split('\n')
            score = 0.5
            explanation = "Could not parse LLaVA response"
            
            for line in lines:
                line = line.strip()
                if line.startswith('SCORE:'):
                    score_text = line.replace('SCORE:', '').strip()
                    try:
                        score = float(score_text)
                        score = max(0.0, min(1.0, score))  # Clamp to valid range
                    except ValueError:
                        score = 0.5
                elif line.startswith('EXPLANATION:'):
                    explanation = line.replace('EXPLANATION:', '').strip()
            
            # If no structured response, try to extract from free text
            if score == 0.5 and explanation == "Could not parse LLaVA response":
                # Look for numbers that might be scores
                import re
                score_matches = re.findall(r'(\d+\.?\d*)', response)
                if score_matches:
                    try:
                        potential_score = float(score_matches[0])
                        if 0 <= potential_score <= 1:
                            score = potential_score
                        elif 0 <= potential_score <= 10:
                            score = potential_score / 10.0
                        elif 0 <= potential_score <= 100:
                            score = potential_score / 100.0
                    except ValueError:
                        pass
                
                # Use the response as explanation
                explanation = response[:200] + "..." if len(response) > 200 else response
            
            return score, explanation
            
        except Exception as e:
            return 0.5, f"Parse error: {str(e)}"
    
    def explain_scores(self, scores):
        """Generate human-readable explanation of scores"""
        explanations = []
        
        # LLaVA explanation gets priority if available
        if 'llava_explanation' in scores and scores.get('llava_semantic', 0) > 0:
            explanations.append(f"🤖 AI Analysis: {scores['llava_explanation']}")
        
        if scores['structural'] > 0.8:
            explanations.append("✅ Great composition and layout match")
        elif scores['structural'] > 0.6:
            explanations.append("🤔 Good structure, but some layout differences")
        else:
            explanations.append("❌ Very different composition - focus on overall layout")
        
        if scores['histogram'] > 0.8:
            explanations.append("✅ Excellent color distribution match")
        elif scores['histogram'] > 0.6:
            explanations.append("🤔 Good color balance, but some differences")
        else:
            explanations.append("❌ Very different colors - describe the color palette")
        
        if scores['edges'] > 0.8:
            explanations.append("✅ Great shape and edge matching")
        elif scores['edges'] > 0.6:
            explanations.append("🤔 Good shapes, but some edge differences")
        else:
            explanations.append("❌ Different shapes - focus on object boundaries")
        
        if scores['colors'] > 0.8:
            explanations.append("✅ Dominant colors match well")
        elif scores['colors'] > 0.6:
            explanations.append("🤔 Some dominant colors match")
        else:
            explanations.append("❌ Different main colors - what are the key colors?")
        
        return explanations