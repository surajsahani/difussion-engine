"""
Image comparison module for scoring similarity
Advanced multi-metric comparison with perceptual and semantic analysis
"""

import cv2
import numpy as np
import pickle
import os
from pathlib import Path
from skimage.feature import hog, local_binary_pattern
from skimage.color import rgb2gray
from scipy.spatial.distance import cosine
from scipy.stats import wasserstein_distance

class ImageComparison:
    """Advanced image comparison using multiple metrics"""
    
    def __init__(self, use_llava=False, verbose=False):
        """Initialize comparison with optional LLaVA support"""
        self.use_llava = use_llava
        self.verbose = verbose
        self.llava_available = False
        
        # Initialize HOG descriptor for OpenCV
        self.hog_descriptor = cv2.HOGDescriptor()
        
        # Import scikit-image HOG for backup
        try:
            from skimage.feature import hog
            self.skimage_hog = hog
            self.has_skimage = True
        except ImportError:
            self.skimage_hog = None
            self.has_skimage = False
            print("⚠️  scikit-image not available, using OpenCV HOG only")
        
        # Define weights for different similarity metrics (optimized for better discrimination)
        self.weights = {
            'perceptual': 0.30,        # Advanced perceptual similarity (LPIPS-style)
            'semantic': 0.25,          # Semantic content (HOG + LBP + SIFT)
            'structural': 0.20,        # SSIM structural similarity  
            'color_advanced': 0.15,    # Advanced color matching (LAB + Earth Mover's Distance)
            'texture': 0.10           # Texture analysis (Gabor filters + LBP)
        }
        
        # Create cache directory for HOG features
        from pathlib import Path
        self.cache_dir = Path.home() / ".ai-prompt-game" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # For now, we'll disable LLaVA since you're not using it
        if self.use_llava:
            if self.verbose:
                print("⚠️  LLaVA not implemented, using traditional metrics")
        
        if self.verbose:
            print("📊 Using traditional image comparison metrics")
            print(f"📊 Weights: {self.weights}")
    
    def compare(self, generated_image, target_image):
        """
        Compare two images using advanced multi-metric analysis
        
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
        
        # Advanced similarity metrics
        perceptual_sim = self.perceptual_similarity(generated_image, target_image)
        semantic_sim = self.semantic_similarity(generated_image, target_image)
        structural_sim = self.structural_similarity(generated_image, target_image)
        color_advanced_sim = self.advanced_color_similarity(generated_image, target_image)
        texture_sim = self.texture_similarity(generated_image, target_image)
        
        # Apply non-linear combination with adaptive weighting
        scores = {
            'perceptual': perceptual_sim,
            'semantic': semantic_sim,
            'structural': structural_sim,
            'color_advanced': color_advanced_sim,
            'texture': texture_sim
        }
        
        # Adaptive weighting based on image characteristics
        adaptive_weights = self.calculate_adaptive_weights(generated_image, target_image)
        
        combined = sum(scores[metric] * adaptive_weights[metric] for metric in scores)
        
        # Apply final non-linear transformation for better discrimination
        combined = self.apply_discrimination_curve(combined, scores)
        
        # Backward compatibility - map new metrics to old names for game engine
        result = {
            'combined': max(0, min(1, combined)),
            'perceptual': max(0, perceptual_sim),
            'semantic': max(0, semantic_sim),
            'structural': max(0, structural_sim),
            'color_advanced': max(0, color_advanced_sim),
            'texture': max(0, texture_sim),
            'adaptive_weights': adaptive_weights,
            # Backward compatibility mappings
            'histogram': max(0, color_advanced_sim),  # Map color_advanced to histogram
            'edges': max(0, structural_sim * 0.8 + texture_sim * 0.2),  # Combine structural + texture
            'colors': max(0, color_advanced_sim),  # Map color_advanced to colors
            'hog_features': max(0, semantic_sim),  # Map semantic to hog_features
            'hsv_similarity': max(0, color_advanced_sim * 0.9)  # Map color_advanced to hsv
        }
        
        return result
    
    def _calculate_traditional_metrics(self, img1, img2):
        """Calculate traditional image similarity metrics"""
        import cv2
        import numpy as np
        
        # Convert to grayscale for structural similarity
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
        
        # Structural similarity using correlation
        try:
            result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)
            structural = float(result[0][0]) if result.size > 0 else 0.0
            structural = max(0, min(1, structural))  # Clamp to [0,1]
        except:
            structural = 0.0
        
        # Histogram similarity
        try:
            if len(img1.shape) == 3:
                hist1 = cv2.calcHist([img1], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
                hist2 = cv2.calcHist([img2], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
            else:
                hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
            
            histogram = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            histogram = max(0, min(1, histogram))
        except:
            histogram = 0.0
        
        # Edge similarity
        try:
            edges1 = cv2.Canny(gray1, 50, 150)
            edges2 = cv2.Canny(gray2, 50, 150)
            
            # Simple edge correlation
            edges1_norm = edges1.astype(np.float32) / 255.0
            edges2_norm = edges2.astype(np.float32) / 255.0
            
            correlation = np.corrcoef(edges1_norm.flatten(), edges2_norm.flatten())[0, 1]
            edges = max(0, min(1, correlation)) if not np.isnan(correlation) else 0.0
        except:
            edges = 0.0
        
        # Color similarity (use histogram)
        colors = histogram
        
        return {
            'structural': float(structural),
            'histogram': float(histogram),
            'edges': float(edges),
            'colors': float(colors)
        }

    def get_hog_features(self, image):
        """Extract HOG features from image"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Use scikit-image HOG if available (more reliable)
            if self.has_skimage:
                features = self.skimage_hog(
                    gray,
                    orientations=9,
                    pixels_per_cell=(8, 8),
                    cells_per_block=(2, 2),
                    visualize=False,
                    feature_vector=True
                )
                return features
            else:
                # Fallback to OpenCV HOG
                features = self.hog_descriptor.compute(gray)
                return features.flatten() if features is not None else np.array([])
                
        except Exception as e:
            print(f"⚠️  HOG feature extraction failed: {e}")
            # Return empty features array as fallback
            return np.array([])

    def hog_similarity(self, img1, img2):
        """Calculate HOG-based structural similarity"""
        try:
            features1 = self.get_hog_features(img1)
            features2 = self.get_hog_features(img2)
            
            # Check if features were extracted successfully
            if len(features1) == 0 or len(features2) == 0:
                return 0.5  # Neutral score if features extraction fails
            
            # Ensure same feature length
            min_len = min(len(features1), len(features2))
            if min_len == 0:
                return 0.5
                
            features1 = features1[:min_len]
            features2 = features2[:min_len]
            
            # Calculate cosine similarity
            dot_product = np.dot(features1, features2)
            norm1 = np.linalg.norm(features1)
            norm2 = np.linalg.norm(features2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.5
                
            similarity = dot_product / (norm1 * norm2)
            return max(0, similarity)  # Ensure non-negative
            
        except Exception as e:
            print(f"⚠️  HOG similarity calculation failed: {e}")
            return 0.5  # Fallback score
    
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
    
    def structural_similarity(self, img1, img2):
        """Calculate structural similarity using SSIM with stricter scoring"""
        from skimage.metrics import structural_similarity as ssim
        
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Resize to same size if needed
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
        
        # Calculate SSIM (ranges from -1 to 1, where 1 is identical)
        similarity_score = ssim(gray1, gray2)
        
        # Apply stricter scoring - square the positive score to penalize differences more
        if similarity_score > 0:
            similarity_score = similarity_score ** 1.8  # Much stricter
        
        # Additional penalty for very different content
        # Check if images have very different brightness distributions
        mean1 = np.mean(gray1)
        mean2 = np.mean(gray2)
        brightness_diff = abs(mean1 - mean2) / 255
        
        if brightness_diff > 0.3:  # Very different brightness
            similarity_score *= 0.5  # Heavy penalty
        
        return max(0, similarity_score)
    
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
        """Calculate edge pattern similarity with much stricter scoring"""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # Calculate edge density difference
        density1 = np.sum(edges1 > 0) / edges1.size
        density2 = np.sum(edges2 > 0) / edges2.size
        density_diff = abs(density1 - density2)
        
        # Much stricter penalty for edge density differences
        if density_diff > 0.15:  # Reduced threshold
            return max(0, 0.1 - density_diff)  # Harsher penalty
        
        # Calculate pixel-wise edge difference
        edge_diff = np.mean(np.abs(edges1.astype(float) - edges2.astype(float))) / 255
        similarity = 1 - edge_diff
        
        # Apply much stricter scoring
        similarity = similarity ** 2.5  # Very strict
        
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
    
    def perceptual_similarity(self, img1, img2):
        """
        Advanced perceptual similarity using multi-scale analysis
        Inspired by LPIPS (Learned Perceptual Image Patch Similarity)
        """
        try:
            # Convert to LAB color space for perceptual uniformity
            lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
            lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
            
            # Multi-scale analysis
            scales = [1.0, 0.5, 0.25]
            scale_similarities = []
            
            for scale in scales:
                if scale != 1.0:
                    h, w = int(img1.shape[0] * scale), int(img1.shape[1] * scale)
                    lab1_scaled = cv2.resize(lab1, (w, h))
                    lab2_scaled = cv2.resize(lab2, (w, h))
                else:
                    lab1_scaled, lab2_scaled = lab1, lab2
                
                # Calculate patch-based similarity
                patch_sim = self.calculate_patch_similarity(lab1_scaled, lab2_scaled)
                scale_similarities.append(patch_sim)
            
            # Weighted combination of scales (higher weight for original scale)
            weights = [0.6, 0.3, 0.1]
            perceptual_score = sum(sim * weight for sim, weight in zip(scale_similarities, weights))
            
            # Apply perceptual curve (human vision is non-linear)
            perceptual_score = 1 - (1 - perceptual_score) ** 0.8
            
            return perceptual_score
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Perceptual similarity error: {e}")
            return 0.5
    
    def calculate_patch_similarity(self, img1, img2, patch_size=16):
        """Calculate similarity using overlapping patches"""
        h, w = img1.shape[:2]
        similarities = []
        
        step = patch_size // 2  # 50% overlap
        
        for y in range(0, h - patch_size + 1, step):
            for x in range(0, w - patch_size + 1, step):
                patch1 = img1[y:y+patch_size, x:x+patch_size]
                patch2 = img2[y:y+patch_size, x:x+patch_size]
                
                # Calculate patch similarity using normalized cross-correlation
                patch1_norm = (patch1 - np.mean(patch1)) / (np.std(patch1) + 1e-8)
                patch2_norm = (patch2 - np.mean(patch2)) / (np.std(patch2) + 1e-8)
                
                correlation = np.mean(patch1_norm * patch2_norm)
                similarities.append(max(0, correlation))
        
        return np.mean(similarities) if similarities else 0.5
    
    def semantic_similarity(self, img1, img2):
        """
        Advanced semantic similarity combining multiple feature descriptors
        """
        try:
            # HOG features for shape/structure
            hog_sim = self.hog_similarity(img1, img2)
            
            # Local Binary Pattern for texture
            lbp_sim = self.lbp_similarity(img1, img2)
            
            # SIFT keypoints for distinctive features
            sift_sim = self.sift_similarity(img1, img2)
            
            # ORB features as backup
            orb_sim = self.orb_similarity(img1, img2)
            
            # Weighted combination
            semantic_score = (
                hog_sim * 0.4 +
                lbp_sim * 0.3 +
                sift_sim * 0.2 +
                orb_sim * 0.1
            )
            
            # Apply semantic discrimination curve
            semantic_score = semantic_score ** 1.5
            
            return semantic_score
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Semantic similarity error: {e}")
            return 0.5
    
    def lbp_similarity(self, img1, img2):
        """Local Binary Pattern similarity for texture analysis"""
        try:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Calculate LBP
            radius = 3
            n_points = 8 * radius
            
            lbp1 = local_binary_pattern(gray1, n_points, radius, method='uniform')
            lbp2 = local_binary_pattern(gray2, n_points, radius, method='uniform')
            
            # Calculate histograms
            hist1, _ = np.histogram(lbp1.ravel(), bins=n_points + 2, range=(0, n_points + 2))
            hist2, _ = np.histogram(lbp2.ravel(), bins=n_points + 2, range=(0, n_points + 2))
            
            # Normalize histograms
            hist1 = hist1.astype(float) / (hist1.sum() + 1e-8)
            hist2 = hist2.astype(float) / (hist2.sum() + 1e-8)
            
            # Calculate similarity using chi-square distance
            chi_square = np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + 1e-8))
            similarity = np.exp(-chi_square / 2)
            
            return similarity
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  LBP similarity error: {e}")
            return 0.5
    
    def sift_similarity(self, img1, img2):
        """SIFT keypoint similarity for distinctive features"""
        try:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Create SIFT detector
            sift = cv2.SIFT_create(nfeatures=100)  # Limit features for performance
            
            # Detect keypoints and descriptors
            kp1, desc1 = sift.detectAndCompute(gray1, None)
            kp2, desc2 = sift.detectAndCompute(gray2, None)
            
            if desc1 is None or desc2 is None or len(desc1) < 5 or len(desc2) < 5:
                return 0.3  # Low similarity if insufficient features
            
            # Match features using FLANN
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            
            matches = flann.knnMatch(desc1, desc2, k=2)
            
            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            # Calculate similarity based on good matches
            max_features = max(len(desc1), len(desc2))
            similarity = len(good_matches) / max_features if max_features > 0 else 0
            
            return min(1.0, similarity * 2)  # Scale up good matches
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  SIFT similarity error: {e}")
            return 0.3
    
    def orb_similarity(self, img1, img2):
        """ORB feature similarity as backup to SIFT"""
        try:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Create ORB detector
            orb = cv2.ORB_create(nfeatures=100)
            
            # Detect keypoints and descriptors
            kp1, desc1 = orb.detectAndCompute(gray1, None)
            kp2, desc2 = orb.detectAndCompute(gray2, None)
            
            if desc1 is None or desc2 is None:
                return 0.3
            
            # Match features using BFMatcher
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(desc1, desc2)
            
            # Sort matches by distance
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Calculate similarity
            good_matches = [m for m in matches if m.distance < 50]  # Threshold for good matches
            max_features = max(len(desc1), len(desc2))
            similarity = len(good_matches) / max_features if max_features > 0 else 0
            
            return min(1.0, similarity * 1.5)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  ORB similarity error: {e}")
            return 0.3
    
    def advanced_color_similarity(self, img1, img2):
        """
        Advanced color similarity using LAB color space and Earth Mover's Distance
        """
        try:
            # Convert to LAB for perceptual color matching
            lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
            lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
            
            # Calculate color distribution similarity
            lab_sim = self.lab_similarity(lab1, lab2)
            
            # Earth Mover's Distance for color distributions
            emd_sim = self.earth_movers_distance_similarity(img1, img2)
            
            # Color moment similarity
            moment_sim = self.color_moment_similarity(img1, img2)
            
            # Weighted combination
            color_score = (
                lab_sim * 0.5 +
                emd_sim * 0.3 +
                moment_sim * 0.2
            )
            
            return color_score
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Advanced color similarity error: {e}")
            return 0.5
    
    def earth_movers_distance_similarity(self, img1, img2):
        """Calculate color similarity using Earth Mover's Distance (Wasserstein)"""
        try:
            # Convert to LAB and flatten
            lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
            lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
            
            # Calculate EMD for each channel
            emd_scores = []
            for channel in range(3):
                hist1, bins = np.histogram(lab1[:,:,channel].flatten(), bins=50, density=True)
                hist2, _ = np.histogram(lab2[:,:,channel].flatten(), bins=bins, density=True)
                
                # Calculate Wasserstein distance
                emd = wasserstein_distance(bins[:-1], bins[:-1], hist1, hist2)
                
                # Convert to similarity (lower EMD = higher similarity)
                max_emd = np.max(bins) - np.min(bins)
                similarity = 1 - (emd / max_emd)
                emd_scores.append(max(0, similarity))
            
            return np.mean(emd_scores)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  EMD similarity error: {e}")
            return 0.5
    
    def color_moment_similarity(self, img1, img2):
        """Calculate similarity using color moments (mean, variance, skewness)"""
        try:
            # Convert to LAB
            lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB).astype(np.float32)
            lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB).astype(np.float32)
            
            similarities = []
            
            for channel in range(3):
                c1 = lab1[:,:,channel].flatten()
                c2 = lab2[:,:,channel].flatten()
                
                # First moment (mean)
                mean1, mean2 = np.mean(c1), np.mean(c2)
                mean_sim = 1 - abs(mean1 - mean2) / 255
                
                # Second moment (variance)
                var1, var2 = np.var(c1), np.var(c2)
                var_sim = 1 - abs(var1 - var2) / (255**2)
                
                # Third moment (skewness)
                from scipy.stats import skew
                skew1, skew2 = skew(c1), skew(c2)
                skew_sim = 1 - abs(skew1 - skew2) / 10  # Normalize skewness
                
                channel_sim = (mean_sim * 0.5 + var_sim * 0.3 + skew_sim * 0.2)
                similarities.append(max(0, channel_sim))
            
            return np.mean(similarities)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Color moment similarity error: {e}")
            return 0.5
    
    def texture_similarity(self, img1, img2):
        """
        Advanced texture analysis using Gabor filters and LBP
        """
        try:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Gabor filter responses
            gabor_sim = self.gabor_similarity(gray1, gray2)
            
            # LBP texture
            lbp_sim = self.lbp_similarity(img1, img2)
            
            # Texture energy
            energy_sim = self.texture_energy_similarity(gray1, gray2)
            
            # Weighted combination
            texture_score = (
                gabor_sim * 0.5 +
                lbp_sim * 0.3 +
                energy_sim * 0.2
            )
            
            return texture_score
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Texture similarity error: {e}")
            return 0.5
    
    def gabor_similarity(self, gray1, gray2):
        """Calculate texture similarity using Gabor filters"""
        try:
            # Define Gabor filter parameters
            orientations = [0, 45, 90, 135]  # degrees
            frequencies = [0.1, 0.3, 0.5]
            
            responses1 = []
            responses2 = []
            
            for freq in frequencies:
                for angle in orientations:
                    # Create Gabor kernel
                    kernel = cv2.getGaborKernel((21, 21), 5, np.radians(angle), 
                                              2*np.pi*freq, 0.5, 0, ktype=cv2.CV_32F)
                    
                    # Apply filter
                    resp1 = cv2.filter2D(gray1, cv2.CV_8UC3, kernel)
                    resp2 = cv2.filter2D(gray2, cv2.CV_8UC3, kernel)
                    
                    # Calculate energy (mean of squared responses)
                    energy1 = np.mean(resp1**2)
                    energy2 = np.mean(resp2**2)
                    
                    responses1.append(energy1)
                    responses2.append(energy2)
            
            # Calculate similarity between response vectors
            responses1 = np.array(responses1)
            responses2 = np.array(responses2)
            
            # Normalize
            responses1 = responses1 / (np.linalg.norm(responses1) + 1e-8)
            responses2 = responses2 / (np.linalg.norm(responses2) + 1e-8)
            
            # Cosine similarity
            similarity = np.dot(responses1, responses2)
            
            return max(0, similarity)
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Gabor similarity error: {e}")
            return 0.5
    
    def texture_energy_similarity(self, gray1, gray2):
        """Calculate texture energy similarity"""
        try:
            # Calculate texture energy using local variance
            kernel = np.ones((5,5), np.float32) / 25
            
            # Local mean
            mean1 = cv2.filter2D(gray1.astype(np.float32), -1, kernel)
            mean2 = cv2.filter2D(gray2.astype(np.float32), -1, kernel)
            
            # Local variance (texture energy)
            sqr1 = cv2.filter2D((gray1.astype(np.float32))**2, -1, kernel)
            sqr2 = cv2.filter2D((gray2.astype(np.float32))**2, -1, kernel)
            
            var1 = sqr1 - mean1**2
            var2 = sqr2 - mean2**2
            
            # Calculate similarity of variance maps
            correlation = np.corrcoef(var1.flatten(), var2.flatten())[0,1]
            
            return max(0, correlation) if not np.isnan(correlation) else 0.5
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Texture energy similarity error: {e}")
            return 0.5
    
    def calculate_adaptive_weights(self, img1, img2):
        """Calculate adaptive weights based on image characteristics"""
        try:
            # Analyze image characteristics
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Edge density (high = structural content, low = smooth/color content)
            edges1 = cv2.Canny(gray1, 50, 150)
            edges2 = cv2.Canny(gray2, 50, 150)
            edge_density = (np.sum(edges1 > 0) + np.sum(edges2 > 0)) / (2 * edges1.size)
            
            # Color variance (high = colorful, low = monochrome)
            color_var = np.mean([np.var(img1[:,:,i]) + np.var(img2[:,:,i]) for i in range(3)]) / (255**2)
            
            # Texture complexity
            lbp1 = local_binary_pattern(gray1, 8, 1, method='uniform')
            lbp2 = local_binary_pattern(gray2, 8, 1, method='uniform')
            texture_complexity = (np.std(lbp1) + np.std(lbp2)) / (2 * 10)  # Normalize
            
            # Adaptive weight calculation (more balanced)
            base_weights = self.weights.copy()
            
            # High edge density -> slightly increase structural weight
            if edge_density > 0.1:
                base_weights['structural'] *= 1.15
                base_weights['perceptual'] *= 0.95
            
            # High color variance -> slightly increase color weight
            if color_var > 0.3:
                base_weights['color_advanced'] *= 1.2
                base_weights['semantic'] *= 0.95
            
            # High texture complexity -> slightly increase texture weight
            if texture_complexity > 0.5:
                base_weights['texture'] *= 1.25
                base_weights['perceptual'] *= 0.9
            
            # Normalize weights
            total_weight = sum(base_weights.values())
            adaptive_weights = {k: v/total_weight for k, v in base_weights.items()}
            
            return adaptive_weights
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Adaptive weights error: {e}")
            return self.weights
    
    def apply_discrimination_curve(self, combined_score, individual_scores):
        """Apply balanced non-linear transformation for better score discrimination"""
        try:
            # Check for very low individual scores (indicates poor match)
            min_score = min(individual_scores.values())
            if min_score < 0.15:
                # Moderate penalty for very poor matches in any metric
                combined_score *= (min_score / 0.15) ** 1.5
            
            # Apply balanced sigmoid-like curve
            if combined_score > 0.7:
                # Slightly enhance excellent matches
                combined_score = 0.7 + (combined_score - 0.7) ** 0.8
            elif combined_score > 0.4:
                # Keep moderate matches relatively unchanged
                combined_score = combined_score ** 1.1
            else:
                # Moderate penalty for poor matches
                combined_score = combined_score ** 1.4
            
            # Consistency check with lighter penalty
            score_variance = np.var(list(individual_scores.values()))
            if score_variance > 0.15:  # High variance indicates inconsistent match
                combined_score *= 0.9  # Light penalty for inconsistency
            
            return combined_score
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Discrimination curve error: {e}")
            return combined_score
    
    def lab_similarity(self, lab1, lab2):
        """Enhanced LAB color space similarity"""
        try:
            # Calculate histograms for each LAB channel
            l_hist1 = cv2.calcHist([lab1], [0], None, [100], [0, 100])
            a_hist1 = cv2.calcHist([lab1], [1], None, [256], [0, 256])
            b_hist1 = cv2.calcHist([lab1], [2], None, [256], [0, 256])
            
            l_hist2 = cv2.calcHist([lab2], [0], None, [100], [0, 100])
            a_hist2 = cv2.calcHist([lab2], [1], None, [256], [0, 256])
            b_hist2 = cv2.calcHist([lab2], [2], None, [256], [0, 256])
            
            # Calculate similarities using multiple methods
            l_corr = cv2.compareHist(l_hist1, l_hist2, cv2.HISTCMP_CORREL)
            a_corr = cv2.compareHist(a_hist1, a_hist2, cv2.HISTCMP_CORREL)
            b_corr = cv2.compareHist(b_hist1, b_hist2, cv2.HISTCMP_CORREL)
            
            l_chi = cv2.compareHist(l_hist1, l_hist2, cv2.HISTCMP_CHISQR)
            a_chi = cv2.compareHist(a_hist1, a_hist2, cv2.HISTCMP_CHISQR)
            b_chi = cv2.compareHist(b_hist1, b_hist2, cv2.HISTCMP_CHISQR)
            
            # Normalize chi-square (lower is better)
            l_chi_norm = max(0, 1 - l_chi / 100000)
            a_chi_norm = max(0, 1 - a_chi / 100000)
            b_chi_norm = max(0, 1 - b_chi / 100000)
            
            # Weighted combination (L channel is most important for perception)
            lab_similarity = (
                (max(0, l_corr) * 0.3 + l_chi_norm * 0.2) * 0.5 +  # L channel: 50%
                (max(0, a_corr) * 0.3 + a_chi_norm * 0.2) * 0.25 + # A channel: 25%
                (max(0, b_corr) * 0.3 + b_chi_norm * 0.2) * 0.25   # B channel: 25%
            )
            
            return lab_similarity
            
        except Exception as e:
            if self.verbose:
                print(f"⚠️  LAB similarity error: {e}")
            return 0.5
    
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
        """Generate human-readable explanation of scores with advanced metrics"""
        explanations = []
        
        # Perceptual similarity
        if scores.get('perceptual', 0) > 0.8:
            explanations.append("✅ Excellent perceptual match - images look very similar to human vision")
        elif scores.get('perceptual', 0) > 0.6:
            explanations.append("🤔 Good perceptual similarity, but some visual differences")
        else:
            explanations.append("❌ Poor perceptual match - focus on overall visual appearance")
        
        # Semantic similarity
        if scores.get('semantic', 0) > 0.8:
            explanations.append("✅ Great semantic content match - objects and shapes align well")
        elif scores.get('semantic', 0) > 0.6:
            explanations.append("🤔 Good semantic content, but some object/shape differences")
        else:
            explanations.append("❌ Very different content - focus on main objects and their shapes")
        
        # Structural similarity
        if scores.get('structural', 0) > 0.8:
            explanations.append("✅ Excellent composition and layout match")
        elif scores.get('structural', 0) > 0.6:
            explanations.append("🤔 Good structure, but some layout differences")
        else:
            explanations.append("❌ Very different composition - focus on overall layout and positioning")
        
        # Advanced color similarity
        if scores.get('color_advanced', 0) > 0.8:
            explanations.append("✅ Outstanding color matching across all metrics")
        elif scores.get('color_advanced', 0) > 0.6:
            explanations.append("🤔 Good color similarity, but some palette differences")
        else:
            explanations.append("❌ Poor color match - describe the specific colors and lighting")
        
        # Texture similarity
        if scores.get('texture', 0) > 0.8:
            explanations.append("✅ Excellent texture and surface detail match")
        elif scores.get('texture', 0) > 0.6:
            explanations.append("🤔 Good texture similarity, but some surface differences")
        else:
            explanations.append("❌ Different textures - focus on surface details and patterns")
        
        # Overall assessment
        combined = scores.get('combined', 0)
        if combined > 0.85:
            explanations.append("🎯 Outstanding overall match!")
        elif combined > 0.7:
            explanations.append("👍 Good overall similarity")
        elif combined > 0.5:
            explanations.append("⚠️ Moderate similarity - room for improvement")
        else:
            explanations.append("🔄 Low similarity - try a different approach")
        
        # Adaptive weights info
        if 'adaptive_weights' in scores:
            weights = scores['adaptive_weights']
            max_weight_metric = max(weights, key=weights.get)
            explanations.append(f"🎛️ Focus area: {max_weight_metric.replace('_', ' ').title()}")
        
        return explanations