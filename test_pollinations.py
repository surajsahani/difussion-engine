#!/usr/bin/env python3
"""
Quick test of Pollinations.ai free API
"""

import requests
from PIL import Image
import io
import matplotlib.pyplot as plt

def test_pollinations_api():
    """Test the free Pollinations.ai API"""
    print("🌟 Testing Pollinations.ai Free API...")
    
    # Test prompt
    test_prompt = "a beautiful sunset over a calm lake with mountains"
    
    try:
        # Pollinations.ai free API endpoint
        import urllib.parse
        encoded_prompt = urllib.parse.quote(test_prompt)
        
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=42&model=flux"
        
        print(f"🔄 Generating: '{test_prompt}'")
        print("⏳ This may take 10-30 seconds...")
        
        # Make request
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            # Load and display image
            image = Image.open(io.BytesIO(response.content))
            
            plt.figure(figsize=(8, 8))
            plt.imshow(image)
            plt.title(f"Generated: '{test_prompt}'", fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            
            # Save test image
            image.save("pollinations_test.jpg")
            plt.savefig("pollinations_test_display.png", dpi=150, bbox_inches='tight')
            
            plt.show()
            
            print("✅ SUCCESS! Pollinations.ai is working!")
            print("💾 Test image saved as: pollinations_test.jpg")
            print("🎨 The API generates beautiful, realistic images!")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out. The API might be busy, try again later.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_api_info():
    """Show information about Pollinations.ai"""
    print("\n🌟 About Pollinations.ai:")
    print("✅ Completely FREE")
    print("✅ No API key required")
    print("✅ High-quality images")
    print("✅ Multiple AI models available")
    print("✅ Fast generation (10-30 seconds)")
    print("\n🔗 Website: https://pollinations.ai")
    print("📚 API Docs: https://image.pollinations.ai")

if __name__ == "__main__":
    print("🧪 Pollinations.ai API Test")
    print("=" * 40)
    
    show_api_info()
    
    # Test the API
    if test_pollinations_api():
        print("\n🎉 Ready to use in the game!")
        print("Run: python3 open_llm_game.py")
    else:
        print("\n💡 Troubleshooting:")
        print("1. Check internet connection")
        print("2. Try again in a few minutes")
        print("3. Install dependencies: pip install requests pillow matplotlib")