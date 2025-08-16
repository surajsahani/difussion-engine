#!/usr/bin/env python3
"""
Create Natural High-Quality Target Images
Downloads beautiful natural images to use as challenging targets
"""

import requests
import os
from PIL import Image
import io

def download_image(url, filename):
    """Download and save an image"""
    try:
        print(f"📥 Downloading: {filename}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Open and resize image
        image = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to standard size while maintaining aspect ratio
        image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        # Save as high quality JPEG
        image.save(filename, 'JPEG', quality=95)
        print(f"✅ Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def create_natural_targets():
    """Create a collection of natural target images"""
    
    # Create targets directory
    os.makedirs("natural_targets", exist_ok=True)
    
    print("🌟 Creating Natural Target Image Collection")
    print("=" * 50)
    
    # Collection of beautiful natural images from Unsplash (free to use)
    targets = [
        {
            "name": "mountain_sunset.jpg",
            "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1024&q=80",
            "description": "Golden sunset over mountain peaks with dramatic clouds"
        },
        {
            "name": "ocean_waves.jpg", 
            "url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=1024&q=80",
            "description": "Powerful ocean waves crashing on rocky shore"
        },
        {
            "name": "forest_path.jpg",
            "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1024&q=80",
            "description": "Misty forest path with tall trees and soft lighting"
        },
        {
            "name": "desert_dunes.jpg",
            "url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1024&q=80",
            "description": "Rolling sand dunes with dramatic shadows and blue sky"
        },
        {
            "name": "lake_reflection.jpg",
            "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1024&q=80",
            "description": "Perfect mountain reflection in calm lake water"
        },
        {
            "name": "cherry_blossoms.jpg",
            "url": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1024&q=80",
            "description": "Pink cherry blossoms in full bloom with soft focus"
        },
        {
            "name": "northern_lights.jpg",
            "url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1024&q=80",
            "description": "Aurora borealis dancing over snowy landscape"
        },
        {
            "name": "tropical_beach.jpg",
            "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1024&q=80",
            "description": "Crystal clear tropical water with white sand beach"
        },
        {
            "name": "autumn_forest.jpg",
            "url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97?w=1024&q=80",
            "description": "Vibrant autumn colors in deciduous forest"
        },
        {
            "name": "starry_night.jpg",
            "url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1024&q=80",
            "description": "Milky Way galaxy over silhouetted mountain range"
        }
    ]
    
    successful_downloads = 0
    
    for target in targets:
        filename = f"natural_targets/{target['name']}"
        
        if download_image(target['url'], filename):
            successful_downloads += 1
            print(f"📝 Description: {target['description']}")
        
        print()  # Empty line for readability
    
    print("=" * 50)
    print(f"🎯 Successfully created {successful_downloads}/{len(targets)} target images")
    print("📁 Images saved in: natural_targets/")
    
    return successful_downloads > 0

def create_challenge_descriptions():
    """Create description file for each target"""
    
    descriptions = {
        "mountain_sunset.jpg": {
            "difficulty": "Medium",
            "key_elements": ["mountains", "sunset", "golden light", "dramatic clouds", "silhouette"],
            "style_hints": ["landscape photography", "golden hour", "dramatic lighting"],
            "sample_prompts": [
                "golden sunset over mountain peaks",
                "dramatic mountain silhouette at sunset",
                "golden hour landscape with mountains and clouds"
            ]
        },
        "ocean_waves.jpg": {
            "difficulty": "Hard", 
            "key_elements": ["ocean", "waves", "rocks", "spray", "motion"],
            "style_hints": ["seascape", "dynamic water", "coastal photography"],
            "sample_prompts": [
                "powerful ocean waves crashing on rocks",
                "dramatic seascape with white foam",
                "coastal waves with spray and motion"
            ]
        },
        "forest_path.jpg": {
            "difficulty": "Medium",
            "key_elements": ["forest", "path", "trees", "mist", "green"],
            "style_hints": ["nature photography", "atmospheric", "peaceful"],
            "sample_prompts": [
                "misty forest path through tall trees",
                "peaceful woodland trail with soft light",
                "atmospheric forest scene with morning mist"
            ]
        },
        "desert_dunes.jpg": {
            "difficulty": "Easy",
            "key_elements": ["sand dunes", "desert", "shadows", "blue sky"],
            "style_hints": ["minimalist", "geometric", "warm colors"],
            "sample_prompts": [
                "rolling sand dunes with dramatic shadows",
                "desert landscape with golden sand",
                "minimalist dune photography"
            ]
        },
        "tropical_beach.jpg": {
            "difficulty": "Easy",
            "key_elements": ["beach", "tropical", "clear water", "white sand", "paradise"],
            "style_hints": ["tropical", "crystal clear", "pristine"],
            "sample_prompts": [
                "tropical beach with crystal clear water",
                "pristine white sand beach paradise",
                "turquoise water and white sand"
            ]
        }
    }
    
    # Save descriptions as JSON
    import json
    with open("natural_targets/descriptions.json", "w") as f:
        json.dump(descriptions, f, indent=2)
    
    print("📋 Challenge descriptions saved to: natural_targets/descriptions.json")

def test_with_pollinations():
    """Test generating images with Pollinations.ai using natural targets"""
    
    print("\n🧪 Testing with Pollinations.ai")
    print("=" * 30)
    
    # Test prompts for different targets
    test_cases = [
        {
            "target": "mountain_sunset.jpg",
            "prompt": "golden sunset over mountain peaks with dramatic clouds"
        },
        {
            "target": "ocean_waves.jpg", 
            "prompt": "powerful ocean waves crashing on rocky shore"
        },
        {
            "target": "tropical_beach.jpg",
            "prompt": "crystal clear tropical water with white sand beach"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎯 Test {i}: {test['target']}")
        print(f"📝 Prompt: '{test['prompt']}'")
        
        # Generate with Pollinations.ai
        try:
            import urllib.parse
            encoded_prompt = urllib.parse.quote(test['prompt'])
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
            
            print("🔄 Generating with Pollinations.ai...")
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                # Save generated image
                output_file = f"natural_targets/test_generated_{i}.jpg"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Generated image saved: {output_file}")
            else:
                print(f"❌ Generation failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🌟 Natural Target Image Creator")
    print("Creating beautiful, challenging target images for the game")
    print("=" * 60)
    
    # Create natural targets
    if create_natural_targets():
        print("✅ Natural targets created successfully!")
        
        # Create descriptions
        create_challenge_descriptions()
        
        # Test with Pollinations.ai
        test_choice = input("\n🧪 Test with Pollinations.ai? (y/n): ").strip().lower()
        if test_choice == 'y':
            test_with_pollinations()
        
        print("\n🎉 Setup complete!")
        print("\n🎮 To use these targets:")
        print("python open_llm_game.py")
        print("# Then enter: natural_targets/mountain_sunset.jpg")
        
        print("\n🌐 Or with the API:")
        print("python api_server.py")
        print("# Upload any image from natural_targets/ folder")
        
    else:
        print("❌ Failed to create natural targets")
        print("💡 Check your internet connection and try again")

if __name__ == "__main__":
    main()