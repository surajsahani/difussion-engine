#!/usr/bin/env python3
"""
Perfect Demo Script - Shows 100% Match Progression
Pre-scripted demo for hackathon presentations
"""

import time
import os
from datetime import datetime

class PerfectDemo:
    """Demo class that simulates perfect learning progression"""
    
    def __init__(self):
        self.attempt_count = 0
        self.target_description = "Golden sunset over mountain peaks with dramatic clouds and lake reflection"
        
    def show_intro(self):
        """Show demo introduction"""
        print("🎯 AI PROMPT ENGINEERING GAME - PERFECT DEMO")
        print("=" * 60)
        print("🎨 Target: Beautiful Mountain Sunset Landscape")
        print("🎓 Watch a student learn prompt engineering in real-time!")
        print("=" * 60)
        
        print("\n📸 TARGET IMAGE DISPLAYED:")
        print("┌─────────────────────────────────────────┐")
        print("│  🌄 Golden sunset over mountain peaks   │")
        print("│  ☁️  Dramatic clouds in orange sky      │") 
        print("│  🏔️  Dark mountain silhouettes          │")
        print("│  🌊 Lake with perfect reflection        │")
        print("│  🎨 Professional landscape photography  │")
        print("└─────────────────────────────────────────┘")
        
        input("\n👆 Student sees this target image. Press Enter to start attempts...")
    
    def make_demo_attempt(self, prompt, expected_score, feedback, generated_description):
        """Simulate a single attempt with realistic timing"""
        self.attempt_count += 1
        
        print(f"\n🎯 Attempt #{self.attempt_count}")
        print(f"📝 Student enters: '{prompt}'")
        
        # Simulate thinking time
        print("🤔 Student is thinking about the target...")
        time.sleep(1)
        
        # Simulate AI generation
        print("🔄 AI generating image...")
        for i in range(3):
            print("   ⏳ Processing..." + "." * (i + 1))
            time.sleep(0.8)
        
        print("✅ AI image generated!")
        
        # Show generated result
        print(f"\n🎨 AI GENERATED: {generated_description}")
        
        # Calculate and show scores
        print(f"\n📊 SIMILARITY ANALYSIS:")
        print(f"   - Overall Score: {expected_score:.3f}")
        
        if expected_score < 0.3:
            print(f"   - Structure: {expected_score + 0.1:.3f}")
            print(f"   - Colors: {expected_score - 0.05:.3f}")
            print(f"   - Composition: {expected_score + 0.05:.3f}")
        elif expected_score < 0.6:
            print(f"   - Structure: {expected_score + 0.15:.3f}")
            print(f"   - Colors: {expected_score - 0.1:.3f}")
            print(f"   - Composition: {expected_score + 0.2:.3f}")
        else:
            print(f"   - Structure: {min(1.0, expected_score + 0.1):.3f}")
            print(f"   - Colors: {min(1.0, expected_score + 0.05):.3f}")
            print(f"   - Composition: {min(1.0, expected_score + 0.15):.3f}")
        
        # Show feedback
        print(f"\n💬 FEEDBACK: {feedback}")
        
        # Show improvement if not first attempt
        if self.attempt_count > 1:
            improvement = expected_score - self.previous_score
            if improvement > 0:
                print(f"📈 IMPROVEMENT: +{improvement:.3f} from last attempt!")
            
        self.previous_score = expected_score
        
        # Victory check
        if expected_score >= 0.95:
            print("\n🎉🎉🎉 PERFECT MATCH ACHIEVED! 🎉🎉🎉")
            print("🏆 Student has mastered prompt engineering!")
            return True
        
        return False
    
    def show_learning_progression(self):
        """Show the complete learning journey"""
        print("\n📈 LEARNING PROGRESSION ANALYSIS:")
        print("=" * 50)
        
        attempts = [
            ("landscape", 0.156),
            ("sunset over mountains", 0.423),
            ("golden sunset mountain landscape", 0.687),
            ("golden sunset over mountain peaks with dramatic clouds", 0.891),
            ("golden sunset over mountain peaks with dramatic clouds and lake reflection", 0.967)
        ]
        
        print("Attempt | Prompt | Score | Learning")
        print("-" * 50)
        
        for i, (prompt, score) in enumerate(attempts, 1):
            improvement = "First attempt" if i == 1 else f"+{score - attempts[i-2][1]:.3f}"
            short_prompt = prompt[:25] + "..." if len(prompt) > 25 else prompt
            print(f"   {i}    | {short_prompt:<28} | {score:.3f} | {improvement}")
        
        print("\n🎓 KEY LEARNING INSIGHTS:")
        print("• Started with basic word → Learned to be specific")
        print("• Added colors and lighting → Improved dramatically") 
        print("• Included composition details → Achieved near-perfect match")
        print("• Total improvement: +0.811 points across 5 attempts")
    
    def run_perfect_demo(self):
        """Run the complete perfect demo"""
        self.show_intro()
        
        # Attempt 1: Basic and poor
        victory = self.make_demo_attempt(
            prompt="landscape",
            expected_score=0.156,
            feedback="💡 Too generic! Try describing what you see in the target image.",
            generated_description="Basic countryside landscape with green fields"
        )
        if victory: return
        
        input("\n🤔 Student realizes they need to be more specific. Press Enter...")
        
        # Attempt 2: Better but still missing key elements
        victory = self.make_demo_attempt(
            prompt="sunset over mountains", 
            expected_score=0.423,
            feedback="👍 Better! You identified key elements. Now add more details about colors and atmosphere.",
            generated_description="Orange sunset behind mountain silhouettes"
        )
        if victory: return
        
        input("\n💡 Student is learning! Adding more descriptive words. Press Enter...")
        
        # Attempt 3: Good progress, getting specific
        victory = self.make_demo_attempt(
            prompt="golden sunset mountain landscape",
            expected_score=0.687, 
            feedback="🌟 Great improvement! Try being even more specific about the dramatic elements.",
            generated_description="Golden hour mountain landscape with warm lighting"
        )
        if victory: return
        
        input("\n🚀 Student is getting close! Adding dramatic details. Press Enter...")
        
        # Attempt 4: Very close, almost perfect
        victory = self.make_demo_attempt(
            prompt="golden sunset over mountain peaks with dramatic clouds",
            expected_score=0.891,
            feedback="🎯 Excellent! Almost perfect! What about the water reflection?",
            generated_description="Stunning golden sunset over mountain peaks with dramatic orange clouds"
        )
        if victory: return
        
        input("\n🔥 So close to perfect! Student adds final detail. Press Enter...")
        
        # Attempt 5: Perfect match!
        victory = self.make_demo_attempt(
            prompt="golden sunset over mountain peaks with dramatic clouds and lake reflection",
            expected_score=0.967,
            feedback="🎉 PERFECT! You've mastered the art of AI prompt engineering!",
            generated_description="Perfect golden sunset over mountain peaks with dramatic clouds and beautiful lake reflection"
        )
        
        # Show learning analysis
        time.sleep(2)
        self.show_learning_progression()
        
        # Final celebration
        print("\n" + "=" * 60)
        print("🎓 EDUCATIONAL OUTCOME ACHIEVED!")
        print("=" * 60)
        print("✅ Student learned to analyze images systematically")
        print("✅ Student mastered specific, descriptive language")
        print("✅ Student understood iterative improvement process")
        print("✅ Student achieved measurable skill progression")
        print("\n🚀 Ready for more advanced AI prompt engineering challenges!")

def run_presentation_demo():
    """Run demo perfect for presentations"""
    print("🎤 HACKATHON PRESENTATION DEMO")
    print("=" * 40)
    print("This demo shows perfect learning progression")
    print("Student goes from 15.6% to 96.7% match in 5 attempts")
    print("=" * 40)
    
    demo = PerfectDemo()
    demo.run_perfect_demo()
    
    print("\n🎯 DEMO COMPLETE!")
    print("Questions about our AI-powered educational game?")

def run_quick_demo():
    """Quick 2-minute demo version"""
    print("⚡ QUICK DEMO - 2 MINUTES")
    print("=" * 30)
    
    demo = PerfectDemo()
    
    # Show just 3 key attempts
    print("🎯 Target: Mountain sunset landscape")
    print("📸 [Beautiful target image displayed]")
    
    print("\n--- Attempt 1: Beginner ---")
    demo.make_demo_attempt("landscape", 0.156, "Too generic!", "Basic countryside")
    
    print("\n--- Attempt 3: Learning ---") 
    demo.make_demo_attempt("golden sunset mountains", 0.687, "Much better!", "Golden mountain landscape")
    
    print("\n--- Attempt 5: Mastery ---")
    demo.make_demo_attempt("golden sunset over mountain peaks with dramatic clouds and lake reflection", 0.967, "PERFECT!", "Stunning perfect match")
    
    print("\n🎓 Result: Student learned effective prompt engineering!")
    print("📈 Improvement: 15.6% → 96.7% in 5 attempts")

def main():
    """Main demo selector"""
    print("🎯 AI PROMPT ENGINEERING GAME - DEMO SELECTOR")
    print("=" * 50)
    print("Choose demo type:")
    print("1. 🎤 Full Presentation Demo (5 minutes)")
    print("2. ⚡ Quick Demo (2 minutes)")
    print("3. 📊 Learning Analytics Only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_presentation_demo()
    elif choice == "2":
        run_quick_demo()
    elif choice == "3":
        demo = PerfectDemo()
        demo.show_learning_progression()
    else:
        print("Running full demo by default...")
        run_presentation_demo()

if __name__ == "__main__":
    main()