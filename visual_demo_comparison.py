#!/usr/bin/env python3
"""
Visual Demo Comparison - Shows Before/After Results
Perfect for hackathon presentations
"""

import matplotlib.pyplot as plt
import numpy as np

def create_demo_visualizations():
    """Create visual comparisons for the demo"""
    
    print("🎨 Creating Demo Visualizations...")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('AI Prompt Engineering Game - Learning Progression Demo', fontsize=16, fontweight='bold')
    
    # Demo data
    attempts = [
        {
            'attempt': 1,
            'prompt': 'landscape',
            'score': 0.156,
            'color': 'lightcoral'
        },
        {
            'attempt': 2, 
            'prompt': 'sunset over mountains',
            'score': 0.423,
            'color': 'orange'
        },
        {
            'attempt': 3,
            'prompt': 'golden sunset mountain landscape', 
            'score': 0.687,
            'color': 'gold'
        },
        {
            'attempt': 4,
            'prompt': 'golden sunset over mountain peaks with dramatic clouds',
            'score': 0.891,
            'color': 'lightgreen'
        },
        {
            'attempt': 5,
            'prompt': 'golden sunset over mountain peaks with dramatic clouds and lake reflection',
            'score': 0.967,
            'color': 'green'
        }
    ]
    
    # Top row: Target and final result
    axes[0, 0].text(0.5, 0.5, '🎯 TARGET IMAGE\n\n🌄 Golden sunset\n☁️ Dramatic clouds\n🏔️ Mountain peaks\n🌊 Lake reflection', 
                   ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    axes[0, 0].set_title('Target Image', fontweight='bold')
    axes[0, 0].axis('off')
    
    axes[0, 1].text(0.5, 0.5, '❌ ATTEMPT #1\nScore: 15.6%\n\n🌾 Basic countryside\n🟢 Green fields\n☁️ Plain sky\n\n"landscape"', 
                   ha='center', va='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
    axes[0, 1].set_title('First Attempt (Poor)', fontweight='bold')
    axes[0, 1].axis('off')
    
    axes[0, 2].text(0.5, 0.5, '✅ ATTEMPT #5\nScore: 96.7%\n\n🌄 Perfect sunset\n☁️ Dramatic clouds\n🏔️ Mountain peaks\n🌊 Lake reflection\n\n"golden sunset over mountain\npeaks with dramatic clouds\nand lake reflection"', 
                   ha='center', va='center', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    axes[0, 2].set_title('Final Attempt (Perfect!)', fontweight='bold')
    axes[0, 2].axis('off')
    
    # Bottom row: Progress charts
    
    # Score progression
    attempts_nums = [a['attempt'] for a in attempts]
    scores = [a['score'] for a in attempts]
    colors = [a['color'] for a in attempts]
    
    axes[1, 0].bar(attempts_nums, scores, color=colors, alpha=0.7)
    axes[1, 0].plot(attempts_nums, scores, 'ko-', linewidth=2, markersize=6)
    axes[1, 0].set_xlabel('Attempt Number')
    axes[1, 0].set_ylabel('Similarity Score')
    axes[1, 0].set_title('Learning Progression', fontweight='bold')
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Add score labels on bars
    for i, (attempt, score) in enumerate(zip(attempts_nums, scores)):
        axes[1, 0].text(attempt, score + 0.02, f'{score:.3f}', ha='center', fontweight='bold')
    
    # Improvement per attempt
    improvements = [0] + [scores[i] - scores[i-1] for i in range(1, len(scores))]
    axes[1, 1].bar(attempts_nums, improvements, color=['gray'] + ['green' if x > 0 else 'red' for x in improvements[1:]], alpha=0.7)
    axes[1, 1].set_xlabel('Attempt Number')
    axes[1, 1].set_ylabel('Score Improvement')
    axes[1, 1].set_title('Improvement Per Attempt', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add improvement labels
    for i, (attempt, improvement) in enumerate(zip(attempts_nums, improvements)):
        if improvement > 0:
            axes[1, 1].text(attempt, improvement + 0.01, f'+{improvement:.3f}', ha='center', fontweight='bold')
    
    # Prompt complexity (word count)
    word_counts = [len(a['prompt'].split()) for a in attempts]
    axes[1, 2].bar(attempts_nums, word_counts, color='skyblue', alpha=0.7)
    axes[1, 2].set_xlabel('Attempt Number')
    axes[1, 2].set_ylabel('Words in Prompt')
    axes[1, 2].set_title('Prompt Complexity Growth', fontweight='bold')
    axes[1, 2].grid(True, alpha=0.3)
    
    # Add word count labels
    for i, (attempt, count) in enumerate(zip(attempts_nums, word_counts)):
        axes[1, 2].text(attempt, count + 0.1, str(count), ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('demo_learning_progression.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: demo_learning_progression.png")
    
    # Create summary statistics
    create_summary_stats(attempts)
    
    plt.show()

def create_summary_stats(attempts):
    """Create summary statistics visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Demo Statistics - Educational Impact', fontsize=16, fontweight='bold')
    
    # Learning curve
    scores = [a['score'] for a in attempts]
    ax1.plot(range(1, len(scores) + 1), scores, 'bo-', linewidth=3, markersize=8)
    ax1.fill_between(range(1, len(scores) + 1), scores, alpha=0.3)
    ax1.set_xlabel('Attempt Number')
    ax1.set_ylabel('Similarity Score')
    ax1.set_title('Learning Curve')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add milestone markers
    ax1.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Fair (50%)')
    ax1.axhline(y=0.8, color='green', linestyle='--', alpha=0.7, label='Victory (80%)')
    ax1.legend()
    
    # Skill categories (simulated breakdown)
    categories = ['Specificity', 'Color Description', 'Composition', 'Style Awareness']
    initial_skills = [0.2, 0.1, 0.3, 0.1]
    final_skills = [0.95, 0.98, 0.96, 0.92]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax2.bar(x - width/2, initial_skills, width, label='Initial', color='lightcoral', alpha=0.7)
    ax2.bar(x + width/2, final_skills, width, label='Final', color='lightgreen', alpha=0.7)
    ax2.set_xlabel('Skill Categories')
    ax2.set_ylabel('Skill Level')
    ax2.set_title('Skill Development')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Time to mastery
    attempt_times = [30, 45, 60, 75, 90]  # Simulated seconds per attempt
    cumulative_time = np.cumsum(attempt_times)
    
    ax3.bar(range(1, len(cumulative_time) + 1), attempt_times, color='skyblue', alpha=0.7)
    ax3.plot(range(1, len(cumulative_time) + 1), cumulative_time, 'ro-', linewidth=2, label='Cumulative')
    ax3.set_xlabel('Attempt Number')
    ax3.set_ylabel('Time (seconds)')
    ax3.set_title('Time Investment')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Educational metrics
    metrics = ['Engagement', 'Skill Gain', 'Retention', 'Satisfaction']
    values = [95, 87, 92, 89]  # Simulated percentages
    colors = ['gold', 'lightgreen', 'skyblue', 'plum']
    
    ax4.pie(values, labels=metrics, colors=colors, autopct='%1.1f%%', startangle=90)
    ax4.set_title('Educational Impact Metrics')
    
    plt.tight_layout()
    plt.savefig('demo_statistics.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: demo_statistics.png")
    
    plt.show()

def create_comparison_table():
    """Create a comparison table for the demo"""
    
    print("\n📊 DEMO COMPARISON TABLE")
    print("=" * 80)
    print("| Attempt | Prompt | Score | Generated Image Description |")
    print("|---------|--------|-------|----------------------------|")
    print("| 1 | 'landscape' | 15.6% | Basic countryside with green fields |")
    print("| 2 | 'sunset over mountains' | 42.3% | Orange sunset behind mountain silhouettes |") 
    print("| 3 | 'golden sunset mountain landscape' | 68.7% | Golden hour mountain landscape with warm lighting |")
    print("| 4 | 'golden sunset over mountain peaks with dramatic clouds' | 89.1% | Stunning golden sunset with dramatic orange clouds |")
    print("| 5 | 'golden sunset over mountain peaks with dramatic clouds and lake reflection' | 96.7% | Perfect match with all target elements |")
    print("=" * 80)
    
    print("\n🎓 KEY LEARNING INSIGHTS:")
    print("• Total improvement: +81.1 percentage points")
    print("• Average improvement per attempt: +20.3 points")
    print("• Time to mastery: 5 attempts (5 minutes)")
    print("• Final skill level: Expert (96.7% accuracy)")

def main():
    """Main demo visualization function"""
    print("🎨 AI PROMPT GAME - VISUAL DEMO CREATOR")
    print("=" * 50)
    print("Creating perfect demo visualizations for hackathon presentation")
    print("=" * 50)
    
    # Create visualizations
    create_demo_visualizations()
    
    # Show comparison table
    create_comparison_table()
    
    print("\n🎉 DEMO VISUALIZATIONS COMPLETE!")
    print("📁 Files created:")
    print("   - demo_learning_progression.png")
    print("   - demo_statistics.png")
    print("\n💡 Use these in your hackathon presentation!")
    print("🎯 Shows perfect learning progression from 15.6% to 96.7%")

if __name__ == "__main__":
    main()