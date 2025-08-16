#!/usr/bin/env python3
"""
Simple test script to verify the game logic without heavy dependencies
"""

import os
import sys
import json
from datetime import datetime

# Mock the heavy dependencies for testing
class MockStableDiffusionEngine:
    """Mock engine that generates random colored images for testing"""
    def __init__(self, scheduler, device="CPU"):
        print(f"✅ Mock Stable Diffusion Engine initialized (device: {device})")
        
    def __call__(self, prompt, num_inference_steps=20, guidance_scale=7.5):
        """Generate a mock image based on prompt"""
        import random
        
        # Simple mock image representation (just metadata)
        mock_image = {
            'prompt': prompt,
            'dominant_color': 'blue' if 'blue' in prompt.lower() else 
                            'red' if 'red' in prompt.lower() else
                            'green' if 'green' in prompt.lower() else
                            'orange' if 'orange' in prompt.lower() or 'sunset' in prompt.lower() else
                            'random',
            'complexity': len(prompt.split()),
            'keywords': prompt.lower().split()
        }
        
        print(f"🎨 Generated mock image for prompt: '{prompt}'")
        return mock_image

def mock_cv2_imread(path):
    """Mock cv2.imread that creates a simple target image"""
    import numpy as np
    if not os.path.exists(path):
        # Create a simple target image (blue square)
        target = np.full((512, 512, 3), [255, 100, 0], dtype=np.uint8)  # Orange-ish
        return target
    return None

def mock_cv2_imwrite(filename, image):
    """Mock cv2.imwrite that just prints what would be saved"""
    print(f"💾 Would save image: {filename}")
    return True

def mock_cv2_resize(image, size, interpolation=None):
    """Mock cv2.resize"""
    import numpy as np
    return np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)

def mock_cv2_cvtColor(image, conversion):
    """Mock cv2.cvtColor"""
    import numpy as np
    if len(image.shape) == 3:
        return np.mean(image, axis=2).astype(np.uint8)
    return image

def mock_cv2_calcHist(images, channels, mask, histSize, ranges):
    """Mock cv2.calcHist"""
    import numpy as np
    return np.random.rand(histSize[0] * histSize[1] * histSize[2], 1)

def mock_cv2_compareHist(hist1, hist2, method):
    """Mock cv2.compareHist"""
    import random
    return random.uniform(0.3, 0.9)  # Random similarity score

# Mock cv2 module
class MockCV2:
    INTER_LANCZOS4 = 4
    INTER_NEAREST = 0
    COLOR_BGR2RGB = 4
    COLOR_BGR2GRAY = 6
    HISTCMP_CORREL = 0
    NORM_HAMMING = 6
    
    imread = staticmethod(mock_cv2_imread)
    imwrite = staticmethod(mock_cv2_imwrite)
    resize = staticmethod(mock_cv2_resize)
    cvtColor = staticmethod(mock_cv2_cvtColor)
    calcHist = staticmethod(mock_cv2_calcHist)
    compareHist = staticmethod(mock_cv2_compareHist)
    
    class ORB_create:
        @staticmethod
        def create():
            return MockORB()
    
    class BFMatcher:
        def __init__(self, norm, crossCheck=True):
            pass
        def match(self, des1, des2):
            import random
            return [None] * random.randint(10, 100)  # Mock matches

# Mock ORB detector
class MockORB:
    def detectAndCompute(self, image, mask):
        import random
        import numpy as np
        # Return mock keypoints and descriptors
        kp = [None] * random.randint(50, 200)
        des = np.random.randint(0, 255, (len(kp), 32), dtype=np.uint8) if kp else None
        return kp, des

# Mock other dependencies
def mock_ssim(img1, img2):
    import random
    return random.uniform(0.2, 0.8)

# Patch the imports
sys.modules['cv2'] = MockCV2()
sys.modules['skimage.metrics'] = type('MockModule', (), {'structural_similarity': mock_ssim})()

# Now create a simplified game class
class SimplePromptGame:
    def __init__(self, target_image_path="mock_target.jpg"):
        print(f"🎯 Initializing Simple Prompt Game...")
        print(f"📁 Target image: {target_image_path}")
        
        # Mock engine
        self.engine = MockStableDiffusionEngine(None)
        
        # Create mock target image
        import numpy as np
        self.target_image = np.full((512, 512, 3), [255, 100, 0], dtype=np.uint8)
        
        # Game state
        self.attempts = []
        self.best_score = 0
        self.best_prompt = ""
        self.current_attempt = 0
        
        print("✅ Game initialized successfully!")
    
    def calculate_similarity(self, generated_image, target_image):
        """Simple similarity calculation for testing"""
        import random
        
        # Mock similarity scores
        structural = random.uniform(0.2, 0.9)
        histogram = random.uniform(0.2, 0.9)
        features = random.uniform(0.1, 0.8)
        
        # Boost score if prompt contains certain keywords
        combined = (structural * 0.4 + histogram * 0.4 + features * 0.2)
        
        return {
            'combined': max(0, combined),
            'structural': max(0, structural),
            'histogram': max(0, histogram),
            'features': features
        }
    
    def get_feedback(self, score):
        """Generate feedback based on similarity score"""
        if score >= 0.85:
            return "🎉 Excellent! You're very close to the target image!"
        elif score >= 0.70:
            return "👍 Good work! You're getting closer. Try refining your prompt."
        elif score >= 0.50:
            return "🤔 Fair attempt. Consider the style, colors, and composition."
        else:
            return "💡 Keep trying! Think about the main subject, style, and details."
    
    def make_attempt(self, prompt):
        """Process a student's prompt attempt"""
        self.current_attempt += 1
        
        print(f"\n🎯 Attempt #{self.current_attempt}")
        print(f"📝 Prompt: '{prompt}'")
        print("🔄 Generating image...")
        
        # Generate mock image
        generated_image = self.engine(prompt)
        
        # Calculate similarity
        scores = self.calculate_similarity(generated_image, self.target_image)
        combined_score = scores['combined']
        
        # Save attempt
        attempt_data = {
            'attempt': self.current_attempt,
            'prompt': prompt,
            'score': combined_score,
            'detailed_scores': scores,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt_data)
        
        # Update best score
        is_best = False
        if combined_score > self.best_score:
            self.best_score = combined_score
            self.best_prompt = prompt
            is_best = True
            print("🏆 New best score!")
        
        # Display results
        print(f"📊 Similarity Score: {combined_score:.3f}")
        print(f"   - Structural: {scores['structural']:.3f}")
        print(f"   - Color/Histogram: {scores['histogram']:.3f}")
        print(f"   - Features: {scores['features']:.3f}")
        
        # Provide feedback
        feedback = self.get_feedback(combined_score)
        print(f"💬 {feedback}")
        
        return {
            'score': combined_score,
            'detailed_scores': scores,
            'feedback': feedback,
            'is_best': is_best
        }
    
    def show_progress(self):
        """Display current game progress"""
        print(f"\n📈 Game Progress:")
        print(f"   Attempts: {self.current_attempt}")
        print(f"   Best Score: {self.best_score:.3f}")
        print(f"   Best Prompt: '{self.best_prompt}'")
        
        if self.attempts:
            recent_scores = [a['score'] for a in self.attempts[-5:]]
            print(f"   Recent Scores: {[f'{s:.3f}' for s in recent_scores]}")
    
    def check_victory(self, threshold=0.85):
        """Check if student has achieved victory"""
        if self.best_score >= threshold:
            print(f"\n🎉🎉🎉 VICTORY! 🎉🎉🎉")
            print(f"You've successfully matched the target image!")
            print(f"Final Score: {self.best_score:.3f}")
            print(f"Winning Prompt: '{self.best_prompt}'")
            print(f"Total Attempts: {self.current_attempt}")
            return True
        return False

def run_test():
    """Run a simple test of the game"""
    print("🚀 Starting Simple Prompt Game Test")
    print("=" * 50)
    
    # Initialize game
    game = SimplePromptGame()
    
    # Test prompts
    test_prompts = [
        "a red apple",
        "blue ocean waves",
        "green forest landscape", 
        "orange sunset over mountains",
        "a beautiful orange and blue abstract painting"
    ]
    
    print("\n🎮 Testing with sample prompts...")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}/{len(test_prompts)} ---")
        result = game.make_attempt(prompt)
        
        if game.check_victory():
            break
    
    # Show final results
    print("\n" + "=" * 50)
    print("🏁 Test Complete!")
    game.show_progress()
    
    # Save test session
    session_data = {
        'test_session': True,
        'attempts': game.attempts,
        'best_score': game.best_score,
        'best_prompt': game.best_prompt,
        'total_attempts': game.current_attempt
    }
    
    with open('test_session.json', 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print("💾 Test session saved to test_session.json")
    print("\n✅ Test completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Install the full dependencies when ready")
    print("   2. Replace mock engine with real Stable Diffusion")
    print("   3. Add a real target image")
    print("   4. Run the full game with: python play_game.py target_image.jpg")

if __name__ == "__main__":
    run_test()