
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
    
    def __init__(self, cache_dir="hog_cache", use_llava=True):
        self.weights = {
            'hog_features': 0.40,    # Enhanced semantic content
            'structural': 0.30,      # Better layout matching
            'edges': 0.30,           # Improved shape understanding
        }
        
        self.use_llava = use_llava
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
        edge_sim = self.edge_similarity(generated_image, target_image)
        
        
        combined = (
            hog_sim * self.weights['hog_features'] +
            structural_sim * self.weights['structural'] +
            edge_sim * self.weights['edges']
        )
        
        return {
            'combined': max(0, min(1, combined)),
            'hog_features': max(0, hog_sim),
            'structural': max(0, structural_sim),
            'edges': max(0, edge_sim)
        }
    
    def structural_similarity(self, img1, img2):
        """Calculate enhanced structural similarity with multiple metrics"""
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Method 1: MSE-based similarity (original)
        mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)
        max_mse = 255 * 255
        mse_similarity = 1 - (mse / max_mse)
        
        # Method 2: Texture similarity using local binary patterns
        texture_sim = self.texture_similarity(gray1, gray2)
        
        # Method 3: Composition similarity (rule of thirds, center of mass)
        composition_sim = self.composition_similarity(gray1, gray2)
        
        # Combine all structural metrics
        combined = (mse_similarity * 0.4 + texture_sim * 0.4 + composition_sim * 0.2)
        
        return max(0, min(1, combined))
    
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
        """Calculate context-aware edge similarity"""
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Standard edge detection
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # Method 1: Edge pattern similarity
        edge_diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float))) / 255
        pattern_similarity = 1 - edge_diff
        
        # Method 2: Edge density analysis (context-aware)
        edge_density1 = np.sum(edges1 > 0) / edges1.size
        edge_density2 = np.sum(edges2 > 0) / edges2.size
        density_similarity = 1 - abs(edge_density1 - edge_density2)
        
        # Method 3: Edge orientation analysis
        orientation_sim = self.edge_orientation_similarity(edges1, edges2)
        
        # Combine edge metrics with emphasis on pattern and density
        combined = (pattern_similarity * 0.6 + density_similarity * 0.3 + orientation_sim * 0.1)
        
        return max(0, min(1, combined))
    
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
    
    def texture_similarity(self, gray1, gray2):
        """Calculate texture similarity using local binary patterns"""
        try:
            # Simple texture analysis using gradient magnitude
            # Calculate gradients
            grad_x1 = cv2.Sobel(gray1, cv2.CV_64F, 1, 0, ksize=3)
            grad_y1 = cv2.Sobel(gray1, cv2.CV_64F, 0, 1, ksize=3)
            grad_mag1 = np.sqrt(grad_x1**2 + grad_y1**2)
            
            grad_x2 = cv2.Sobel(gray2, cv2.CV_64F, 1, 0, ksize=3)
            grad_y2 = cv2.Sobel(gray2, cv2.CV_64F, 0, 1, ksize=3)
            grad_mag2 = np.sqrt(grad_x2**2 + grad_y2**2)
            
            # Normalize and compare
            grad_mag1_norm = grad_mag1 / (np.max(grad_mag1) + 1e-8)
            grad_mag2_norm = grad_mag2 / (np.max(grad_mag2) + 1e-8)
            
            # Calculate correlation
            correlation = np.corrcoef(grad_mag1_norm.flatten(), grad_mag2_norm.flatten())[0, 1]
            return max(0, correlation) if not np.isnan(correlation) else 0.0
            
        except Exception:
            return 0.5  # Fallback to neutral score
    
    def composition_similarity(self, gray1, gray2):
        """Calculate composition similarity using rule of thirds and center of mass"""
        try:
            # Rule of thirds analysis
            thirds1 = self.rule_of_thirds_score(gray1)
            thirds2 = self.rule_of_thirds_score(gray2)
            thirds_sim = 1 - abs(thirds1 - thirds2)
            
            # Center of mass analysis
            com1 = self.center_of_mass(gray1)
            com2 = self.center_of_mass(gray2)
            com_sim = 1 - min(1, np.linalg.norm(com1 - com2) / 100)
            
            # Combine composition metrics
            return (thirds_sim * 0.6 + com_sim * 0.4)
            
        except Exception:
            return 0.5  # Fallback to neutral score
    
    def rule_of_thirds_score(self, gray_img):
        """Calculate how well image follows rule of thirds"""
        try:
            h, w = gray_img.shape
            
            # Define rule of thirds lines
            third_h = h // 3
            third_w = w // 3
            
            # Calculate interest at intersection points
            intersections = [
                gray_img[third_h, third_w],
                gray_img[third_h, 2*third_w],
                gray_img[2*third_h, third_w],
                gray_img[2*third_h, 2*third_w]
            ]
            
            # Normalize and return average interest
            return np.mean(intersections) / 255.0
            
        except Exception:
            return 0.5
    
    def center_of_mass(self, gray_img):
        """Calculate center of mass of the image"""
        try:
            h, w = gray_img.shape
            y_coords, x_coords = np.mgrid[0:h, 0:w]
            
            # Calculate weighted center
            total_mass = np.sum(gray_img)
            if total_mass == 0:
                return np.array([h/2, w/2])
            
            center_y = np.sum(y_coords * gray_img) / total_mass
            center_x = np.sum(x_coords * gray_img) / total_mass
            
            return np.array([center_y, center_x])
            
        except Exception:
            return np.array([gray_img.shape[0]/2, gray_img.shape[1]/2])
    
    def edge_orientation_similarity(self, edges1, edges2):
        """Calculate edge orientation similarity"""
        try:
            # Calculate gradient orientation
            grad_x1 = cv2.Sobel(edges1.astype(np.float64), cv2.CV_64F, 1, 0, ksize=3)
            grad_y1 = cv2.Sobel(edges1.astype(np.float64), cv2.CV_64F, 0, 1, ksize=3)
            orientation1 = np.arctan2(grad_y1, grad_x1)
            
            grad_x2 = cv2.Sobel(edges2.astype(np.float64), cv2.CV_64F, 1, 0, ksize=3)
            grad_y2 = cv2.Sobel(edges2.astype(np.float64), cv2.CV_64F, 0, 1, ksize=3)
            orientation2 = np.arctan2(grad_y2, grad_x2)
            
            # Calculate orientation histogram similarity
            hist1, _ = np.histogram(orientation1.flatten(), bins=18, range=(-np.pi, np.pi))
            hist2, _ = np.histogram(orientation2.flatten(), bins=18, range=(-np.pi, np.pi))
            
            # Normalize histograms
            hist1 = hist1 / (np.sum(hist1) + 1e-8)
            hist2 = hist2 / (np.sum(hist2) + 1e-8)
            
            # Calculate correlation
            correlation = np.corrcoef(hist1, hist2)[0, 1]
            return max(0, correlation) if not np.isnan(correlation) else 0.0
            
        except Exception:
            return 0.5  # Fallback to neutral score
    
    def perceptual_hash_similarity(self, img1, img2):
        """Calculate perceptual hash similarity - more reliable than histogram"""
        try:
            # Convert to grayscale and resize to 8x8
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
            # Resize to 8x8 for hash calculation
            small1 = cv2.resize(gray1, (8, 8))
            small2 = cv2.resize(gray2, (8, 8))
            
            # Calculate mean
            mean1 = np.mean(small1)
            mean2 = np.mean(small2)
            
            # Create hash (1 if pixel > mean, 0 otherwise)
            hash1 = small1 > mean1
            hash2 = small2 > mean2
            
            # Calculate hamming distance
            hamming_distance = np.sum(hash1 != hash2)
            
            # Convert to similarity (64 is max distance for 8x8)
            similarity = 1 - (hamming_distance / 64)
            
            return max(0, similarity)
            
        except Exception:
            return 0.5  # Fallback to neutral score
    
    def sift_similarity(self, img1, img2):
        """Calculate SIFT feature similarity for better semantic matching"""
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
            # Initialize SIFT detector
            sift = cv2.SIFT_create()
            
            # Detect keypoints and descriptors
            kp1, des1 = sift.detectAndCompute(gray1, None)
            kp2, des2 = sift.detectAndCompute(gray2, None)
            
            # If no descriptors found, return neutral score
            if des1 is None or des2 is None:
                return 0.5
            
            # Use FLANN matcher
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            
            # Find matches
            matches = flann.knnMatch(des1, des2, k=2)
            
            # Apply ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            # Calculate similarity based on number of good matches
            max_matches = min(len(kp1), len(kp2))
            if max_matches == 0:
                return 0.5
            
            similarity = len(good_matches) / max_matches
            
            return min(1.0, similarity)
            
        except Exception:
            return 0.5  # Fallback to neutral score
    
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