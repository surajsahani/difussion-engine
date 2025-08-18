#!/usr/bin/env python3
"""
Image comparison module for scoring similarity
"""

import cv2
import numpy as np

class ImageComparison:
    """Handles image similarity comparison using multiple metrics"""
    
    def __init__(self):
        self.weights = {
            'structural': 0.30,
            'histogram': 0.25,
            'edges': 0.25,
            'colors': 0.20
        }
    
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
        
        # Calculate individual metrics
        structural_sim = self.structural_similarity(generated_image, target_image)
        histogram_sim = self.histogram_similarity(generated_image, target_image)
        edge_sim = self.edge_similarity(generated_image, target_image)
        color_sim = self.dominant_color_similarity(generated_image, target_image)
        
        # Calculate combined score
        combined = (
            structural_sim * self.weights['structural'] +
            histogram_sim * self.weights['histogram'] +
            edge_sim * self.weights['edges'] +
            color_sim * self.weights['colors']
        )
        
        return {
            'combined': max(0, min(1, combined)),
            'structural': max(0, structural_sim),
            'histogram': max(0, histogram_sim),
            'edges': max(0, edge_sim),
            'colors': max(0, color_sim)
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
    
    def explain_scores(self, scores):
        """Generate human-readable explanation of scores"""
        explanations = []
        
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