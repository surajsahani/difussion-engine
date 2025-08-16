#!/usr/bin/env python3
"""
Setup script for Open LLM Game
Installs dependencies for different AI models
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def setup_pollinations():
    """Setup for Pollinations.ai (FREE, easiest)"""
    print("🌟 Setting up Pollinations.ai (FREE)")
    print("This requires no API keys and works immediately!")
    
    packages = ["requests", "pillow"]
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed")
        else:
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ Pollinations.ai setup complete!")
    return True

def setup_huggingface():
    """Setup for Hugging Face local models"""
    print("🤗 Setting up Hugging Face Diffusers")
    print("This will download models locally (several GB)")
    
    packages = [
        "diffusers",
        "transformers", 
        "torch",
        "torchvision",
        "accelerate"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed")
        else:
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ Hugging Face setup complete!")
    print("💡 First run will download ~4GB of models")
    return True

def setup_replicate():
    """Setup for Replicate API"""
    print("🔄 Setting up Replicate API")
    print("You'll need a free API key from https://replicate.com")
    
    if install_package("replicate"):
        print("✅ Replicate package installed")
        print("\n🔑 To use Replicate:")
        print("1. Sign up at https://replicate.com")
        print("2. Get your API token")
        print("3. Set environment variable:")
        print("   export REPLICATE_API_TOKEN=your_token_here")
        return True
    else:
        print("❌ Failed to install replicate")
        return False

def create_sample_target():
    """Create a sample target image for testing"""
    try:
        import cv2
        import numpy as np
        
        # Create a simple but interesting target image
        height, width = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sunset gradient
        for y in range(height // 2):
            intensity = 1.0 - (y / (height // 2))
            image[y, :, 0] = int(255 * intensity * 0.9)  # Red
            image[y, :, 1] = int(255 * intensity * 0.7)  # Green
            image[y, :, 2] = int(255 * intensity * 0.3)  # Blue
        
        # Water
        image[height//2:, :, 2] = 120
        image[height//2:, :, 1] = 80
        image[height//2:, :, 0] = 40
        
        # Sun
        cv2.circle(image, (400, 120), 45, (255, 255, 200), -1)
        
        # Mountain silhouette
        for x in range(width):
            mountain_height = int(height * 0.2 * (0.5 + 0.5 * np.sin(x * 0.008)))
            y_start = height//2 - mountain_height
            image[y_start:height//2, x] = [50, 50, 50]
        
        cv2.imwrite("sample_target.jpg", image)
        print("✅ Sample target image created: sample_target.jpg")
        return True
        
    except Exception as e:
        print(f"❌ Could not create sample target: {e}")
        return False

def main():
    print("🤖 Open LLM Game Setup")
    print("=" * 40)
    
    # Install basic dependencies first
    basic_packages = ["opencv-python", "matplotlib", "numpy"]
    
    print("📦 Installing basic dependencies...")
    for package in basic_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed")
        else:
            print(f"❌ Failed to install {package}")
            return
    
    print("\n🎯 Choose AI model to setup:")
    print("1. 🌟 Pollinations.ai (FREE, recommended for beginners)")
    print("2. 🤗 Hugging Face Diffusers (local, better quality)")
    print("3. 🔄 Replicate API (highest quality, needs API key)")
    print("4. All of the above")
    
    choice = input("Enter choice (1-4): ").strip()
    
    success = False
    
    if choice == "1":
        success = setup_pollinations()
    elif choice == "2":
        success = setup_huggingface()
    elif choice == "3":
        success = setup_replicate()
    elif choice == "4":
        success = (setup_pollinations() and 
                  setup_huggingface() and 
                  setup_replicate())
    else:
        print("Invalid choice, setting up Pollinations.ai by default...")
        success = setup_pollinations()
    
    if success:
        print("\n🎨 Creating sample target image...")
        create_sample_target()
        
        print("\n🎉 Setup complete!")
        print("\n🚀 To play the game:")
        print("python3 open_llm_game.py")
        print("\n💡 Or test with sample target:")
        print("python3 open_llm_game.py")
        print("Then enter: sample_target.jpg")
        
    else:
        print("\n❌ Setup failed. Try installing dependencies manually:")
        print("pip install opencv-python matplotlib numpy requests pillow")

if __name__ == "__main__":
    main()