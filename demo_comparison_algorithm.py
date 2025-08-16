#!/usr/bin/env python3
"""
Demo of Image Comparison Algorithm
Shows how the 4-metric system works
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2

def create_demo_images():
    """Create demo images to show algorithm in action"""
    
    # Create target image (sunset scene)
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
    
    return target

def create_comparison_images(target):
    """Create different generated images for comparison"""
    
    images = {}
    
    # 1. Very similar (good prompt)
    similar = target.copy()
    # Add slight variation
    noise = np.random.randint(-20, 20, similar.shape)
    similar = np.clip(similar.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    images['Similar (Good Prompt)'] = similar
    
    # 2. Same structure, different colors (partial match)
    partial = target.copy()
    # Change colors but keep structure
    partial[:, :, [0, 2]] = partial[:, :, [2, 0]]  # Swap red and blue
    images['Different Colors'] = partial
    
    # 3. Different scene entirely (bad prompt)
    different = np.zeros((300, 400, 3), dtype=np.uint8)
    # Create city scene
    different[:150, :] = [135, 206, 235]  # Sky blue
    different[150:, :] = [128, 128, 128]  # Gray ground
    # Add buildings
    for i in range(0, 400, 80):
        height = np.random.randint(50, 120)
        different[150-height:150, i:i+60] = [64, 64, 64]  # Building
    images['Completely Different'] = different
    
    return images

def analyze_similarity(target, generated, title):
    """Analyze similarity using our 4-metric system"""
    
    print(f"\n🔍 ANALYZING: {title}")
    print("=" * 40)
    
    # Ensure same size
    if generated.shape != target.shape:
        generated = cv2.resize(generated, (target.shape[1], target.shape[0]))
    
    # 1. Structural Similarity
    gen_gray = cv2.cvtColor(generated, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gen_gray.astype(float) - target_gray.astype(float)) ** 2)
    structural_sim = max(0, 1 - (mse / (255 * 255)))
    
    # 2. Color Histogram
    gen_hist = cv2.calcHist([generated], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
    target_hist = cv2.calcHist([target], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
    hist_sim = max(0, cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CORREL))
    
    # 3. Edge Similarity
    gen_edges = cv2.Canny(gen_gray, 50, 150)
    target_edges = cv2.Canny(target_gray, 50, 150)
    edge_diff = np.mean(np.abs(gen_edges.astype(float) - target_edges.astype(float))) / 255
    edge_sim = max(0, 1 - edge_diff)
    
    # 4. Dominant Colors (simplified)
    gen_mean_color = np.mean(generated.reshape(-1, 3), axis=0)
    target_mean_color = np.mean(target.reshape(-1, 3), axis=0)
    color_dist = np.linalg.norm(gen_mean_color - target_mean_color)
    color_sim = max(0, 1 - (color_dist / (255 * np.sqrt(3))))
    
    # Combined score
    combined = (structural_sim * 0.3 + hist_sim * 0.25 + edge_sim * 0.25 + color_sim * 0.2)
    
    # Display results
    print(f"📊 Structural Similarity: {structural_sim:.3f}")
    print(f"🎨 Color Histogram:      {hist_sim:.3f}")
    print(f"🔲 Edge Detection:       {edge_sim:.3f}")
    print(f"🌈 Dominant Colors:      {color_sim:.3f}")
    print(f"🎯 COMBINED SCORE:       {combined:.3f}")
    
    return {
        'structural': structural_sim,
        'histogram': hist_sim,
        'edges': edge_sim,
        'colors': color_sim,
        'combined': combined
    }

def visualize_comparison():
    """Create visual comparison demonstration"""
    
    print("🎨 Creating Image Comparison Algorithm Demo")
    print("=" * 50)
    
    # Create images
    target = create_demo_images()
    comparisons = create_comparison_images(target)
    
    # Analyze each comparison
    results = {}
    for title, image in comparisons.items():
        results[title] = analyze_similarity(target, image, title)
    
    # Create visualization
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle('Image Comparison Algorithm Demo', fontsize=16, fontweight='bold')
    
    # Top row: Images
    # Target
    axes[0, 0].imshow(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('🎯 TARGET\n(Sunset Scene)', fontweight='bold')
    axes[0, 0].axis('off')
    
    # Comparisons
    for i, (title, image) in enumerate(comparisons.items(), 1):
        axes[0, i].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        score = results[title]['combined']
        axes[0, i].set_title(f'{title}\nScore: {score:.3f}', fontweight='bold')
        axes[0, i].axis('off')
    
    # Bottom row: Metric breakdowns
    metrics = ['structural', 'histogram', 'edges', 'colors']
    metric_names = ['Structure', 'Colors', 'Edges', 'Dom. Colors']
    
    for i, (title, result) in enumerate(results.items()):
        values = [result[metric] for metric in metrics]
        colors = ['lightcoral', 'gold', 'lightblue', 'lightgreen']
        
        bars = axes[1, i+1].bar(metric_names, values, color=colors, alpha=0.7)
        axes[1, i+1].set_title(f'{title}\nBreakdown', fontweight='bold')
        axes[1, i+1].set_ylim(0, 1)
        axes[1, i+1].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            axes[1, i+1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                             f'{value:.2f}', ha='center', fontweight='bold')
    
    # Algorithm explanation
    axes[1, 0].text(0.1, 0.8, '🧠 ALGORITHM:', fontweight='bold', fontsize=12)
    axes[1, 0].text(0.1, 0.65, '• Structure (30%)', fontsize=10)
    axes[1, 0].text(0.1, 0.55, '• Colors (25%)', fontsize=10)
    axes[1, 0].text(0.1, 0.45, '• Edges (25%)', fontsize=10)
    axes[1, 0].text(0.1, 0.35, '• Dom. Colors (20%)', fontsize=10)
    axes[1, 0].text(0.1, 0.2, '🎯 Combined Score', fontweight='bold', fontsize=11)
    axes[1, 0].set_xlim(0, 1)
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].axis('off')
    
    plt.tight_layout()
    plt.savefig('comparison_algorithm_demo.png', dpi=300, bbox_inches='tight')
    print("\n✅ Saved: comparison_algorithm_demo.png")
    plt.show()
    
    # Summary
    print("\n📊 ALGORITHM DEMO SUMMARY:")
    print("=" * 50)
    for title, result in results.items():
        print(f"{title:20} → Score: {result['combined']:.3f}")
    
    print("\n🎓 EDUCATIONAL INSIGHT:")
    print("Students learn that effective prompts need to match:")
    print("• Overall composition and structure")
    print("• Color palette and distribution") 
    print("• Important shapes and boundaries")
    print("• Dominant visual elements")

if __name__ == "__main__":
    visualize_comparison()