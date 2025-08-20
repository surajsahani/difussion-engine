#!/usr/bin/env python3
"""
Test script to check if image generation works for Streamlit app
"""

import requests
import io
from PIL import Image

def test_image_generation():
    """Test if Pollinations.ai image generation works"""
    base_url = "https://image.pollinations.ai/prompt/"
    prompt = "a cute orange tabby cat sitting on a windowsill"
    
    try:
        clean_prompt = prompt.replace(' ', '%20').replace(',', '%2C')
        url = f"{base_url}{clean_prompt}?width=256&height=256&nologo=true"
        
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        print(f"✅ Image generated successfully: {image.size}")
        
        # Save test image
        image.save("test_generated_image.png")
        print("✅ Test image saved as 'test_generated_image.png'")
        
        return image
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return None

if __name__ == "__main__":
    print("Testing image generation for Streamlit app...")
    test_image_generation()