
"""
Image comparison module for scoring similarity
Enhanced with LLaVA vision model for intelligent semantic comparison
"""

import cv2
import numpy as np
import pickle
import os
from pathlib import Path

class ImageComparison:
    """Handles image similarity comparison using multiple metrics including LLaVA"""
    
    def __init__(self, cache_dir="hog_cache"):
        self.weights = {
            'hog_features': 0.35,    
            'structural': 0.20,      
            'histogram': 0.15,       
            'edges': 0.15,           
            'colors': 0.10,          
            'hsv_similarity': 0.05   
        }
        
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.hog_cache = {}
        
        
        self.hog = cv2.HOGDescriptor()
        
    def get_hog_features(self, image):
        """Extract HOG features for semantic texture/shape analysis"""
        
        resized = cv2.resize(image, (128, 128))
        
        
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        
        features = self.hog.compute(gray)
        
        return features.flatten()
    
    def hog_similarity(self, img1, img2):
        """Calculate HOG feature similarity for semantic content matching"""
        
        hog1 = self.get_hog_features(img1)
        hog2 = self.get_hog_features(img2)
        
        
        dot_product = np.dot(hog1, hog2)
        norm1 = np.linalg.norm(hog1)
        norm2 = np.linalg.norm(hog2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = dot_product / (norm1 * norm2)
        return max(0, similarity)
    
    def get_cached_hog_features(self, image_path):
        """Get HOG features from cache or compute and cache them"""
        if isinstance(image_path, str):
            cache_key = str(Path(image_path).absolute())
        else:
            
            cache_key = str(hash(image_path.tobytes()))
        
        cache_file = self.cache_dir / f"{hash(cache_key)}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except:
                pass
        
        
        features = self.get_hog_features(image_path)
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(features, f)
        except:
            pass
            
        return features
    
    def hsv_similarity(self, img1, img2):
        """Calculate HSV color space similarity for better color perception"""
        
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        
        h_hist1 = cv2.calcHist([hsv1], [0], None, [180], [0, 180])
        s_hist1 = cv2.calcHist([hsv1], [1], None, [256], [0, 256])
        v_hist1 = cv2.calcHist([hsv1], [2], None, [256], [0, 256])
        
        h_hist2 = cv2.calcHist([hsv2], [0], None, [180], [0, 180])
        s_hist2 = cv2.calcHist([hsv2], [1], None, [256], [0, 256])
        v_hist2 = cv2.calcHist([hsv2], [2], None, [256], [0, 256])
        
        
        h_sim = cv2.compareHist(h_hist1, h_hist2, cv2.HISTCMP_CORREL)
        s_sim = cv2.compareHist(s_hist1, s_hist2, cv2.HISTCMP_CORREL)
        v_sim = cv2.compareHist(v_hist1, v_hist2, cv2.HISTCMP_CORREL)
        
        
        hsv_similarity = (h_sim * 0.5 + s_sim * 0.3 + v_sim * 0.2)
        return max(0, hsv_similarity)
    
    def lab_similarity(self, img1, img2):
        """Calculate LAB color space similarity for perceptual color matching"""
        
        lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
        lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
        
        
        l_hist1 = cv2.calcHist([lab1], [0], None, [256], [0, 256])
        a_hist1 = cv2.calcHist([lab1], [1], None, [256], [0, 256])
        b_hist1 = cv2.calcHist([lab1], [2], None, [256], [0, 256])
        
        l_hist2 = cv2.calcHist([lab2], [0], None, [256], [0, 256])
        a_hist2 = cv2.calcHist([lab2], [1], None, [256], [0, 256])
        b_hist2 = cv2.calcHist([lab2], [2], None, [256], [0, 256])
        
        
        l_sim = cv2.compareHist(l_hist1, l_hist2, cv2.HISTCMP_CORREL)
        a_sim = cv2.compareHist(a_hist1, a_hist2, cv2.HISTCMP_CORREL)
        b_sim = cv2.compareHist(b_hist1, b_hist2, cv2.HISTCMP_CORREL)
        
        
        lab_similarity = (l_sim * 0.4 + a_sim * 0.3 + b_sim * 0.3)
        return max(0, lab_similarity)

    def compare(self, generated_image, target_image):
        """
        Compare two images and return similarity scores
        
        Args:
            generated_image: Generated image (OpenCV format)
            target_image: Target image (OpenCV format)
            
        Returns:
            dict: Similarity scores for each metric plus combined score
        """
        
        if generated_image.shape != target_image.shape:
            generated_image = cv2.resize(
                generated_image, 
                (target_image.shape[1], target_image.shape[0])
            )
        
        
        hog_sim = self.hog_similarity(generated_image, target_image)
        structural_sim = self.structural_similarity(generated_image, target_image)
        histogram_sim = self.histogram_similarity(generated_image, target_image)
        edge_sim = self.edge_similarity(generated_image, target_image)
        color_sim = self.dominant_color_similarity(generated_image, target_image)
        hsv_sim = self.hsv_similarity(generated_image, target_image)
        
        
        combined = (
            hog_sim * self.weights['hog_features'] +
            structural_sim * self.weights['structural'] +
            histogram_sim * self.weights['histogram'] +
            edge_sim * self.weights['edges'] +
            color_sim * self.weights['colors'] +
            hsv_sim * self.weights['hsv_similarity']
        )
        
        return {
            'combined': max(0, min(1, combined)),
            'hog_features': max(0, hog_sim),
            'structural': max(0, structural_sim),
            'histogram': max(0, histogram_sim),
            'edges': max(0, edge_sim),
            'colors': max(0, color_sim),
            'hsv_similarity': max(0, hsv_sim)
        }
    
    def structural_similarity(self, img1, img2):
        """Calculate structural similarity using MSE"""
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        
        mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)
        
        
        max_mse = 255 * 255
        similarity = 1 - (mse / max_mse)
        
        return similarity
    
    def histogram_similarity(self, img1, img2):
        """Calculate color histogram similarity"""
        
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        
        
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        
        chi_square = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        intersection = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        
        
        chi_square_norm = max(0, 1 - (chi_square / 1000000))
        
        
        intersection_norm = intersection / max(np.sum(hist1), np.sum(hist2))
        
        
        combined = (
            max(0, correlation) * 0.5 +
            chi_square_norm * 0.3 +
            intersection_norm * 0.2
        )
        
        return combined
    
    def edge_similarity(self, img1, img2):
        """Calculate edge pattern similarity"""
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        
        edge_diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float))) / 255
        similarity = 1 - edge_diff
        
        return similarity
    
    def dominant_color_similarity(self, img1, img2):
        """Calculate dominant color similarity using k-means"""
        try:
            
            colors1 = self.get_dominant_colors(img1, k=3)
            colors2 = self.get_dominant_colors(img2, k=3)
            
            
            distances = []
            for color1 in colors1:
                min_dist = float('inf')
                for color2 in colors2:
                    dist = np.linalg.norm(color1 - color2)
                    min_dist = min(min_dist, dist)
                distances.append(min_dist)
            
            
            avg_distance = np.mean(distances)
            max_distance = 255 * np.sqrt(3)  
            similarity = 1 - (avg_distance / max_distance)
            
            return similarity
            
        except Exception:
            
            mean1 = np.mean(img1.reshape(-1, 3), axis=0)
            mean2 = np.mean(img2.reshape(-1, 3), axis=0)
            
            distance = np.linalg.norm(mean1 - mean2)
            similarity = 1 - (distance / (255 * np.sqrt(3)))
            
            return similarity
    
    def get_dominant_colors(self, image, k=3):
        """Extract dominant colors using k-means clustering"""
        
        data = image.reshape((-1, 3))
        data = np.float32(data)
        
        
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
        
        if scores['hog_features'] > 0.8:
            explanations.append("✅ Great semantic texture and shape match")
        elif scores['hog_features'] > 0.6:
            explanations.append("🤔 Good semantic texture, but some shape differences")
        else:
            explanations.append("❌ Very different semantic content - focus on overall texture")
        
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
        
        if scores['hsv_similarity'] > 0.8:
            explanations.append("✅ Excellent color perception match")
        elif scores['hsv_similarity'] > 0.6:
            explanations.append("🤔 Good color perception, but some differences")
        else:
            explanations.append("❌ Very different color perception - describe the color palette")
        
        return explanations