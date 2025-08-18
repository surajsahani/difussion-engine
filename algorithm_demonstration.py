#!/usr/bin/env python3
"""
Comprehensive demonstration of how the 4 image comparison algorithms work internally.
This script provides detailed insights into the rating distribution system.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time

class AlgorithmDemonstrator:
    """Demonstrates how each of the 4 algorithms works internally"""
    
    def __init__(self):
        self.weights = {
            'structural': 0.30,
            'histogram': 0.25,
            'edges': 0.25,
            'colors': 0.20
        }
    
    def create_test_images(self):
        """Create test images to demonstrate each algorithm"""
        
        print("🎨 Creating Test Images for Algorithm Demonstration")
        print("=" * 60)
        
        # Original target image (sunset landscape)
        target = np.zeros((300, 400, 3), dtype=np.uint8)
        
        # Sunset sky gradient
        for y in range(150):
            intensity = 1.0 - (y / 150)
            target[y, :, 0] = int(255 * intensity * 0.9)  # Red
            target[y, :, 1] = int(255 * intensity * 0.7)  # Green
            target[y, :, 2] = int(255 * intensity * 0.3)  # Blue
        
        # Ground
        target[150:, :] = [60, 120, 60]  # Green ground
        
        # Mountain silhouette
        for x in range(400):
            mountain_height = int(50 * (0.5 + 0.5 * np.sin(x * 0.02)))
            y_start = 150 - mountain_height
            target[y_start:150, x] = [40, 40, 40]  # Dark mountain
        
        # Sun
        cv2.circle(target, (320, 80), 30, (255, 255, 200), -1)
        
        # Test cases for different aspects
        test_cases = {}
        
        # 1. Same structure, different colors
        same_structure = target.copy()
        same_structure[:, :, [0, 2]] = same_structure[:, :, [2, 0]]  # Swap red and blue
        test_cases['Same Structure, Different Colors'] = same_structure
        
        # 2. Different structure, similar colors
        different_structure = np.zeros((300, 400, 3), dtype=np.uint8)
        # Vertical composition instead of horizontal
        for x in range(200):
            intensity = 1.0 - (x / 200)
            different_structure[:, x, 0] = int(255 * intensity * 0.9)  # Red
            different_structure[:, x, 1] = int(255 * intensity * 0.7)  # Green
            different_structure[:, x, 2] = int(255 * intensity * 0.3)  # Blue
        different_structure[:, 200:] = [60, 120, 60]  # Green area
        test_cases['Different Structure, Similar Colors'] = different_structure
        
        # 3. Similar edges, different colors
        similar_edges = np.zeros((300, 400, 3), dtype=np.uint8)
        similar_edges[:150, :] = [100, 100, 200]  # Blue sky
        similar_edges[150:, :] = [200, 100, 100]  # Red ground
        # Same mountain silhouette
        for x in range(400):
            mountain_height = int(50 * (0.5 + 0.5 * np.sin(x * 0.02)))
            y_start = 150 - mountain_height
            similar_edges[y_start:150, x] = [40, 40, 40]
        test_cases['Similar Edges, Different Colors'] = similar_edges
        
        # 4. Completely different
        completely_different = np.zeros((300, 400, 3), dtype=np.uint8)
        # Create random colored circles
        for _ in range(20):
            center = (np.random.randint(50, 350), np.random.randint(50, 250))
            radius = np.random.randint(10, 30)
            color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
            cv2.circle(completely_different, center, radius, color, -1)
        test_cases['Completely Different'] = completely_different
        
        return target, test_cases
    
    def demonstrate_structural_similarity(self, target, generated, title):
        """Demonstrate how structural similarity works step by step"""
        
        print(f"\n🏗️  STRUCTURAL SIMILARITY DEMO: {title}")
        print("=" * 60)
        
        # Step 1: Convert to grayscale
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        generated_gray = cv2.cvtColor(generated, cv2.COLOR_BGR2GRAY)
        print("✓ Step 1: Converted images to grayscale")
        
        # Step 2: Calculate pixel differences
        pixel_diff = target_gray.astype(float) - generated_gray.astype(float)
        print(f"✓ Step 2: Calculated pixel differences (range: {pixel_diff.min():.1f} to {pixel_diff.max():.1f})")
        
        # Step 3: Square the differences
        squared_diff = pixel_diff ** 2
        print(f"✓ Step 3: Squared differences (range: 0 to {squared_diff.max():.1f})")
        
        # Step 4: Calculate MSE
        mse = np.mean(squared_diff)
        print(f"✓ Step 4: Mean Squared Error = {mse:.2f}")
        
        # Step 5: Convert to similarity
        max_mse = 255 * 255
        similarity = 1 - (mse / max_mse)
        print(f"✓ Step 5: Structural Similarity = 1 - ({mse:.2f} / {max_mse}) = {similarity:.3f}")
        
        return similarity, target_gray, generated_gray, pixel_diff
    
    def demonstrate_histogram_analysis(self, target, generated, title):
        """Demonstrate how color histogram analysis works"""
        
        print(f"\n🎨 HISTOGRAM ANALYSIS DEMO: {title}")
        print("=" * 60)
        
        # Step 1: Create histograms
        target_hist = cv2.calcHist([target], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        generated_hist = cv2.calcHist([generated], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
        print("✓ Step 1: Created 3D color histograms (50×50×50 = 125,000 bins)")
        
        # Step 2: Calculate statistics
        target_colors = np.sum(target_hist > 0)
        generated_colors = np.sum(generated_hist > 0)
        print(f"✓ Step 2: Target uses {target_colors} unique color bins")
        print(f"          Generated uses {generated_colors} unique color bins")
        
        # Step 3: Compare using correlation
        correlation = cv2.compareHist(target_hist, generated_hist, cv2.HISTCMP_CORREL)
        print(f"✓ Step 3: Histogram correlation = {correlation:.3f}")
        
        # Step 4: Additional comparison methods
        chi_square = cv2.compareHist(target_hist, generated_hist, cv2.HISTCMP_CHISQR)
        intersection = cv2.compareHist(target_hist, generated_hist, cv2.HISTCMP_INTERSECT)
        
        # Normalize additional methods
        chi_square_norm = max(0, 1 - (chi_square / 1000000))
        intersection_norm = intersection / max(np.sum(target_hist), np.sum(generated_hist))
        
        print(f"✓ Step 4: Chi-square (normalized) = {chi_square_norm:.3f}")
        print(f"          Intersection (normalized) = {intersection_norm:.3f}")
        
        # Step 5: Combined score
        combined = max(0, correlation * 0.5 + chi_square_norm * 0.3 + intersection_norm * 0.2)
        print(f"✓ Step 5: Combined histogram score = {combined:.3f}")
        
        return combined, target_hist, generated_hist
    
    def demonstrate_edge_detection(self, target, generated, title):
        """Demonstrate how edge detection similarity works"""
        
        print(f"\n🔲 EDGE DETECTION DEMO: {title}")
        print("=" * 60)
        
        # Step 1: Convert to grayscale
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        generated_gray = cv2.cvtColor(generated, cv2.COLOR_BGR2GRAY)
        print("✓ Step 1: Converted to grayscale for edge detection")
        
        # Step 2: Apply Canny edge detection
        target_edges = cv2.Canny(target_gray, 50, 150)
        generated_edges = cv2.Canny(generated_gray, 50, 150)
        
        target_edge_pixels = np.sum(target_edges > 0)
        generated_edge_pixels = np.sum(generated_edges > 0)
        print(f"✓ Step 2: Detected {target_edge_pixels} edge pixels in target")
        print(f"          Detected {generated_edge_pixels} edge pixels in generated")
        
        # Step 3: Compare edge patterns
        edge_diff = np.mean(np.abs(target_edges.astype(float) - generated_edges.astype(float))) / 255
        edge_similarity = 1 - edge_diff
        
        # Calculate overlap
        edge_overlap = np.sum((target_edges > 0) & (generated_edges > 0))
        total_edges = np.sum((target_edges > 0) | (generated_edges > 0))
        overlap_percentage = (edge_overlap / total_edges) if total_edges > 0 else 0
        
        print(f"✓ Step 3: Edge overlap = {edge_overlap} pixels ({overlap_percentage:.1%})")
        print(f"          Edge similarity = {edge_similarity:.3f}")
        
        return edge_similarity, target_edges, generated_edges
    
    def demonstrate_dominant_colors(self, target, generated, title):
        """Demonstrate how dominant color matching works"""
        
        print(f"\n🌈 DOMINANT COLOR DEMO: {title}")
        print("=" * 60)
        
        # Step 1: Extract dominant colors using K-means
        def get_dominant_colors_detailed(image, k=3):
            data = image.reshape((-1, 3)).astype(np.float32)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Calculate how many pixels belong to each cluster
            unique, counts = np.unique(labels, return_counts=True)
            percentages = counts / len(data) * 100
            
            return centers, percentages
        
        target_colors, target_percentages = get_dominant_colors_detailed(target)
        generated_colors, generated_percentages = get_dominant_colors_detailed(generated)
        
        print("✓ Step 1: Extracted dominant colors using K-means clustering")
        print("  Target dominant colors:")
        for i, (color, pct) in enumerate(zip(target_colors, target_percentages)):
            print(f"    Color {i+1}: RGB({color[0]:.0f}, {color[1]:.0f}, {color[2]:.0f}) - {pct:.1f}%")
        
        print("  Generated dominant colors:")
        for i, (color, pct) in enumerate(zip(generated_colors, generated_percentages)):
            print(f"    Color {i+1}: RGB({color[0]:.0f}, {color[1]:.0f}, {color[2]:.0f}) - {pct:.1f}%")
        
        # Step 2: Calculate color distances
        distances = []
        for i, gen_color in enumerate(generated_colors):
            min_dist = float('inf')
            closest_target = 0
            for j, target_color in enumerate(target_colors):
                dist = np.linalg.norm(gen_color - target_color)
                if dist < min_dist:
                    min_dist = dist
                    closest_target = j
            distances.append(min_dist)
            print(f"✓ Step 2: Generated color {i+1} closest to target color {closest_target+1} (distance: {min_dist:.1f})")
        
        # Step 3: Calculate similarity
        avg_distance = np.mean(distances)
        max_distance = 255 * np.sqrt(3)  # Maximum possible distance in RGB space
        similarity = 1 - (avg_distance / max_distance)
        
        print(f"✓ Step 3: Average distance = {avg_distance:.1f}")
        print(f"          Maximum possible distance = {max_distance:.1f}")
        print(f"          Color similarity = {similarity:.3f}")
        
        return similarity, target_colors, generated_colors
    
    def create_comprehensive_visualization(self, target, test_case, title, results):
        """Create a comprehensive visualization of all algorithms"""
        
        fig, axes = plt.subplots(3, 4, figsize=(20, 15))
        fig.suptitle(f'Algorithm Analysis: {title}', fontsize=16, fontweight='bold')
        
        # Row 1: Original images and algorithm visualizations
        axes[0, 0].imshow(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('🎯 Target Image', fontweight='bold')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(cv2.cvtColor(test_case, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('🤖 Generated Image', fontweight='bold')
        axes[0, 1].axis('off')
        
        # Structural analysis visualization
        if 'structural_data' in results:
            target_gray, generated_gray, pixel_diff = results['structural_data']
            diff_vis = np.abs(pixel_diff)
            axes[0, 2].imshow(diff_vis, cmap='hot')
            axes[0, 2].set_title(f'🏗️ Structural Diff\nScore: {results["structural"]:.3f}', fontweight='bold')
            axes[0, 2].axis('off')
        
        # Edge detection visualization
        if 'edge_data' in results:
            target_edges, generated_edges = results['edge_data']
            # Combine edges for visualization
            edge_combined = np.zeros((target_edges.shape[0], target_edges.shape[1], 3), dtype=np.uint8)
            edge_combined[:, :, 0] = target_edges  # Red for target edges
            edge_combined[:, :, 1] = generated_edges  # Green for generated edges
            edge_combined[:, :, 2] = target_edges & generated_edges  # Blue for overlap
            axes[0, 3].imshow(edge_combined)
            axes[0, 3].set_title(f'🔲 Edge Comparison\nScore: {results["edges"]:.3f}', fontweight='bold')
            axes[0, 3].axis('off')
        
        # Row 2: Algorithm scores and color analysis
        algorithms = ['Structural', 'Histogram', 'Edges', 'Colors']
        scores = [results['structural'], results['histogram'], results['edges'], results['colors']]
        weights = [0.30, 0.25, 0.25, 0.20]
        colors = ['lightcoral', 'gold', 'lightblue', 'lightgreen']
        
        bars = axes[1, 0].bar(algorithms, scores, color=colors, alpha=0.7)
        axes[1, 0].set_title('📊 Algorithm Scores', fontweight='bold')
        axes[1, 0].set_ylim(0, 1)
        axes[1, 0].tick_params(axis='x', rotation=45)
        for bar, score in zip(bars, scores):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                           f'{score:.3f}', ha='center', fontweight='bold')
        
        # Weighted contribution
        weighted_scores = [score * weight for score, weight in zip(scores, weights)]
        bars2 = axes[1, 1].bar(algorithms, weighted_scores, color=colors, alpha=0.7)
        axes[1, 1].set_title('⚖️ Weighted Contributions', fontweight='bold')
        axes[1, 1].set_ylim(0, 0.35)
        axes[1, 1].tick_params(axis='x', rotation=45)
        for bar, score in zip(bars2, weighted_scores):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{score:.3f}', ha='center', fontweight='bold')
        
        # Color palette comparison
        if 'color_data' in results:
            target_colors, generated_colors = results['color_data']
            
            # Target colors
            for i, color in enumerate(target_colors):
                rect = Rectangle((i, 0), 1, 1, facecolor=color/255, edgecolor='black')
                axes[1, 2].add_patch(rect)
            axes[1, 2].set_xlim(0, 3)
            axes[1, 2].set_ylim(0, 1)
            axes[1, 2].set_title('🎨 Target Colors', fontweight='bold')
            axes[1, 2].set_xticks([0.5, 1.5, 2.5])
            axes[1, 2].set_xticklabels(['Color 1', 'Color 2', 'Color 3'])
            axes[1, 2].set_yticks([])
            
            # Generated colors
            for i, color in enumerate(generated_colors):
                rect = Rectangle((i, 0), 1, 1, facecolor=color/255, edgecolor='black')
                axes[1, 3].add_patch(rect)
            axes[1, 3].set_xlim(0, 3)
            axes[1, 3].set_ylim(0, 1)
            axes[1, 3].set_title('🤖 Generated Colors', fontweight='bold')
            axes[1, 3].set_xticks([0.5, 1.5, 2.5])
            axes[1, 3].set_xticklabels(['Color 1', 'Color 2', 'Color 3'])
            axes[1, 3].set_yticks([])
        
        # Row 3: Final score calculation and analysis
        final_score = sum(weighted_scores)
        
        # Score breakdown pie chart
        sizes = weighted_scores
        explode = (0.1, 0.1, 0.1, 0.1)
        axes[2, 0].pie(sizes, explode=explode, labels=algorithms, colors=colors, autopct='%1.3f',
                       shadow=True, startangle=90)
        axes[2, 0].set_title(f'🥧 Score Breakdown\nTotal: {final_score:.3f}', fontweight='bold')
        
        # Score interpretation
        if final_score >= 0.85:
            interpretation = "🎉 Excellent Match!"
            color = 'green'
        elif final_score >= 0.70:
            interpretation = "👍 Good Match"
            color = 'orange'
        elif final_score >= 0.50:
            interpretation = "🤔 Fair Match"
            color = 'yellow'
        else:
            interpretation = "💪 Needs Improvement"
            color = 'red'
        
        axes[2, 1].text(0.5, 0.7, f'Final Score: {final_score:.3f}', ha='center', va='center',
                        fontsize=20, fontweight='bold', transform=axes[2, 1].transAxes)
        axes[2, 1].text(0.5, 0.5, f'{final_score*100:.1f}%', ha='center', va='center',
                        fontsize=24, fontweight='bold', color=color, transform=axes[2, 1].transAxes)
        axes[2, 1].text(0.5, 0.3, interpretation, ha='center', va='center',
                        fontsize=16, fontweight='bold', color=color, transform=axes[2, 1].transAxes)
        axes[2, 1].set_xlim(0, 1)
        axes[2, 1].set_ylim(0, 1)
        axes[2, 1].axis('off')
        
        # Algorithm insights
        insights = []
        if results['structural'] > 0.8:
            insights.append("✅ Great composition match")
        elif results['structural'] < 0.3:
            insights.append("❌ Very different layout")
        
        if results['histogram'] > 0.8:
            insights.append("✅ Excellent color distribution")
        elif results['histogram'] < 0.3:
            insights.append("❌ Very different colors")
        
        if results['edges'] > 0.8:
            insights.append("✅ Similar shapes and boundaries")
        elif results['edges'] < 0.3:
            insights.append("❌ Different edge patterns")
        
        if results['colors'] > 0.8:
            insights.append("✅ Matching dominant colors")
        elif results['colors'] < 0.3:
            insights.append("❌ Different color themes")
        
        axes[2, 2].text(0.05, 0.95, "🔍 Analysis Insights:", fontweight='bold', fontsize=12,
                        transform=axes[2, 2].transAxes, va='top')
        for i, insight in enumerate(insights):
            axes[2, 2].text(0.05, 0.85 - i*0.15, insight, fontsize=10,
                           transform=axes[2, 2].transAxes, va='top')
        axes[2, 2].set_xlim(0, 1)
        axes[2, 2].set_ylim(0, 1)
        axes[2, 2].axis('off')
        
        # Educational value
        educational_text = f"""
🎓 Educational Value:

Students learn that:
• Structure: {results['structural']:.3f} (composition)
• Colors: {results['histogram']:.3f} (distribution)  
• Edges: {results['edges']:.3f} (shapes)
• Themes: {results['colors']:.3f} (main colors)

Final weighted score: {final_score:.3f}
        """
        axes[2, 3].text(0.05, 0.95, educational_text.strip(), fontsize=10,
                        transform=axes[2, 3].transAxes, va='top', ha='left')
        axes[2, 3].set_xlim(0, 1)
        axes[2, 3].set_ylim(0, 1)
        axes[2, 3].axis('off')
        
        plt.tight_layout()
        filename = f'algorithm_analysis_{title.lower().replace(" ", "_").replace(",", "")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Saved detailed analysis: {filename}")
        plt.close()
        
        return final_score
    
    def run_comprehensive_demonstration(self):
        """Run the complete algorithm demonstration"""
        
        print("🧠 COMPREHENSIVE ALGORITHM DEMONSTRATION")
        print("=" * 80)
        print("This demo shows exactly how each algorithm works internally")
        print("for the 4-part image comparison system.")
        print()
        
        # Create test images
        target, test_cases = self.create_test_images()
        
        all_results = {}
        
        for title, test_image in test_cases.items():
            print(f"\n🔍 ANALYZING TEST CASE: {title}")
            print("=" * 80)
            
            results = {}
            
            # Demonstrate each algorithm
            structural_score, target_gray, generated_gray, pixel_diff = \
                self.demonstrate_structural_similarity(target, test_image, title)
            results['structural'] = structural_score
            results['structural_data'] = (target_gray, generated_gray, pixel_diff)
            
            histogram_score, target_hist, generated_hist = \
                self.demonstrate_histogram_analysis(target, test_image, title)
            results['histogram'] = histogram_score
            results['histogram_data'] = (target_hist, generated_hist)
            
            edge_score, target_edges, generated_edges = \
                self.demonstrate_edge_detection(target, test_image, title)
            results['edges'] = edge_score
            results['edge_data'] = (target_edges, generated_edges)
            
            color_score, target_colors, generated_colors = \
                self.demonstrate_dominant_colors(target, test_image, title)
            results['colors'] = color_score
            results['color_data'] = (target_colors, generated_colors)
            
            # Calculate final score
            final_score = (
                structural_score * self.weights['structural'] +
                histogram_score * self.weights['histogram'] +
                edge_score * self.weights['edges'] +
                color_score * self.weights['colors']
            )
            results['final'] = final_score
            
            print(f"\n🎯 FINAL SCORE CALCULATION:")
            print(f"   {structural_score:.3f} × 0.30 = {structural_score * 0.30:.3f}")
            print(f"   {histogram_score:.3f} × 0.25 = {histogram_score * 0.25:.3f}")
            print(f"   {edge_score:.3f} × 0.25 = {edge_score * 0.25:.3f}")
            print(f"   {color_score:.3f} × 0.20 = {color_score * 0.20:.3f}")
            print(f"   ────────────────────────────")
            print(f"   TOTAL: {final_score:.3f} ({final_score*100:.1f}%)")
            
            # Create comprehensive visualization
            self.create_comprehensive_visualization(target, test_image, title, results)
            
            all_results[title] = results
            
            time.sleep(0.5)  # Brief pause for readability
        
        # Summary analysis
        print("\n" + "=" * 80)
        print("📊 SUMMARY: Algorithm Performance Across Test Cases")
        print("=" * 80)
        
        for title, results in all_results.items():
            print(f"\n{title}:")
            print(f"  Structural: {results['structural']:.3f} | Histogram: {results['histogram']:.3f} | "
                  f"Edges: {results['edges']:.3f} | Colors: {results['colors']:.3f} | "
                  f"Final: {results['final']:.3f}")
        
        print("\n🎓 EDUCATIONAL INSIGHTS:")
        print("• Students can see exactly how each algorithm contributes")
        print("• Clear feedback on which visual aspects matter most")
        print("• Understanding of weighted scoring helps improve prompts")
        print("• Objective measurement builds visual analysis skills")
        
        return all_results

if __name__ == "__main__":
    demonstrator = AlgorithmDemonstrator()
    results = demonstrator.run_comprehensive_demonstration()
    print("\n🎉 Comprehensive algorithm demonstration complete!")
    print("Check the generated PNG files for detailed visual analysis.")