#!/usr/bin/env python3
"""
Create Diverse Target Image Collection
Variety of styles, contrasts, and visual complexity for better learning
"""

import requests
import os
from PIL import Image
import io
import json

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

def create_diverse_targets():
    """Create a diverse collection of target images"""
    
    # Create targets directory
    os.makedirs("diverse_targets", exist_ok=True)
    
    print("🌈 Creating Diverse Target Image Collection")
    print("=" * 50)
    
    # Diverse collection with variety in style, contrast, and complexity
    targets = [
        # HIGH CONTRAST IMAGES
        {
            "name": "lightning_storm.jpg",
            "url": "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=1024&q=80",
            "difficulty": "Hard",
            "style": "High Contrast",
            "key_elements": ["lightning", "storm clouds", "dramatic sky", "electric bolts"],
            "description": "Dramatic lightning bolts against dark storm clouds"
        },
        {
            "name": "silhouette_sunset.jpg",
            "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1024&q=80",
            "difficulty": "Medium",
            "style": "High Contrast",
            "key_elements": ["silhouette", "person", "sunset", "dramatic lighting"],
            "description": "Person silhouetted against bright sunset sky"
        },
        
        # MINIMALIST/SIMPLE IMAGES
        {
            "name": "single_tree.jpg",
            "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1024&q=80",
            "difficulty": "Easy",
            "style": "Minimalist",
            "key_elements": ["lone tree", "field", "simple composition", "clear sky"],
            "description": "Single tree in open field with clear sky"
        },
        {
            "name": "geometric_architecture.jpg",
            "url": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=1024&q=80",
            "difficulty": "Medium",
            "style": "Minimalist",
            "key_elements": ["geometric", "architecture", "clean lines", "modern building"],
            "description": "Modern geometric building with clean architectural lines"
        },
        
        # COMPLEX/DETAILED IMAGES
        {
            "name": "busy_market.jpg",
            "url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1024&q=80",
            "difficulty": "Hard",
            "style": "Complex",
            "key_elements": ["market", "people", "colorful", "busy scene", "many objects"],
            "description": "Bustling colorful market with many people and objects"
        },
        {
            "name": "detailed_flower.jpg",
            "url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=1024&q=80",
            "difficulty": "Hard",
            "style": "Complex",
            "key_elements": ["macro", "flower", "detailed petals", "close-up", "intricate"],
            "description": "Macro close-up of flower with intricate petal details"
        },
        
        # ABSTRACT/ARTISTIC IMAGES
        {
            "name": "abstract_colors.jpg",
            "url": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=1024&q=80",
            "difficulty": "Hard",
            "style": "Abstract",
            "key_elements": ["abstract", "flowing colors", "paint", "artistic", "fluid"],
            "description": "Abstract flowing colors like paint in water"
        },
        {
            "name": "smoke_art.jpg",
            "url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=1024&q=80",
            "difficulty": "Hard",
            "style": "Abstract",
            "key_elements": ["smoke", "wispy", "ethereal", "flowing", "artistic"],
            "description": "Artistic smoke patterns against dark background"
        },
        
        # URBAN/MODERN IMAGES
        {
            "name": "neon_city.jpg",
            "url": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1024&q=80",
            "difficulty": "Medium",
            "style": "Urban",
            "key_elements": ["neon lights", "city", "night", "colorful signs", "urban"],
            "description": "Neon-lit city street at night with colorful signs"
        },
        {
            "name": "subway_motion.jpg",
            "url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=1024&q=80",
            "difficulty": "Hard",
            "style": "Urban",
            "key_elements": ["motion blur", "subway", "speed", "lights", "movement"],
            "description": "Motion-blurred subway train with streaking lights"
        },
        
        # VINTAGE/RETRO IMAGES
        {
            "name": "vintage_car.jpg",
            "url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1024&q=80",
            "difficulty": "Medium",
            "style": "Vintage",
            "key_elements": ["classic car", "vintage", "retro", "old-fashioned", "nostalgic"],
            "description": "Classic vintage car in retro setting"
        },
        {
            "name": "old_books.jpg",
            "url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1024&q=80",
            "difficulty": "Easy",
            "style": "Vintage",
            "key_elements": ["old books", "vintage", "library", "aged paper", "classic"],
            "description": "Stack of old vintage books with aged pages"
        },
        
        # NATURE WITH DIFFERENT MOODS
        {
            "name": "misty_forest.jpg",
            "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1024&q=80",
            "difficulty": "Medium",
            "style": "Atmospheric",
            "key_elements": ["mist", "fog", "forest", "mysterious", "atmospheric"],
            "description": "Mysterious misty forest with fog between trees"
        },
        {
            "name": "desert_cactus.jpg",
            "url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1024&q=80",
            "difficulty": "Easy",
            "style": "Natural",
            "key_elements": ["cactus", "desert", "arid", "spines", "southwestern"],
            "description": "Large desert cactus in arid southwestern landscape"
        },
        
        # FOOD/OBJECTS (Different category)
        {
            "name": "colorful_spices.jpg",
            "url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=1024&q=80",
            "difficulty": "Medium",
            "style": "Colorful",
            "key_elements": ["spices", "colorful", "market", "powders", "vibrant"],
            "description": "Colorful spice powders arranged in market display"
        }
    ]
    
    successful_downloads = 0
    
    for target in targets:
        filename = f"diverse_targets/{target['name']}"
        
        if download_image(target['url'], filename):
            successful_downloads += 1
            print(f"📝 Style: {target['style']} | Difficulty: {target['difficulty']}")
            print(f"🎯 Elements: {', '.join(target['key_elements'][:3])}...")
            print(f"📖 Description: {target['description']}")
        
        print()  # Empty line for readability
    
    print("=" * 50)
    print(f"🎯 Successfully created {successful_downloads}/{len(targets)} diverse target images")
    print("📁 Images saved in: diverse_targets/")
    
    return successful_downloads > 0, targets

def create_challenge_categories():
    """Create categorized challenges with different learning objectives"""
    
    categories = {
        "beginner_friendly": {
            "name": "🌱 Beginner Challenges",
            "description": "Simple, clear images perfect for learning basics",
            "targets": ["single_tree.jpg", "old_books.jpg", "desert_cactus.jpg"],
            "learning_focus": "Basic object and scene description"
        },
        "high_contrast": {
            "name": "⚡ High Contrast Challenges", 
            "description": "Dramatic lighting and strong visual contrasts",
            "targets": ["lightning_storm.jpg", "silhouette_sunset.jpg"],
            "learning_focus": "Describing dramatic lighting and contrast"
        },
        "complex_scenes": {
            "name": "🧩 Complex Scene Challenges",
            "description": "Busy, detailed images with many elements",
            "targets": ["busy_market.jpg", "detailed_flower.jpg"],
            "learning_focus": "Breaking down complex scenes into components"
        },
        "artistic_abstract": {
            "name": "🎨 Artistic & Abstract Challenges",
            "description": "Abstract and artistic images requiring creative description",
            "targets": ["abstract_colors.jpg", "smoke_art.jpg"],
            "learning_focus": "Creative and artistic vocabulary"
        },
        "urban_modern": {
            "name": "🏙️ Urban & Modern Challenges",
            "description": "City scenes and modern environments",
            "targets": ["neon_city.jpg", "subway_motion.jpg", "geometric_architecture.jpg"],
            "learning_focus": "Modern and urban vocabulary"
        },
        "atmospheric": {
            "name": "🌫️ Atmospheric Challenges",
            "description": "Moody images with special atmosphere",
            "targets": ["misty_forest.jpg", "vintage_car.jpg"],
            "learning_focus": "Describing mood and atmosphere"
        }
    }
    
    return categories

def create_diverse_descriptions(targets):
    """Create comprehensive description file"""
    
    descriptions = {}
    
    for target in targets:
        descriptions[target['name']] = {
            "difficulty": target['difficulty'],
            "style": target['style'],
            "key_elements": target['key_elements'],
            "description": target['description'],
            "sample_prompts": generate_sample_prompts(target),
            "learning_objectives": get_learning_objectives(target['style'], target['difficulty'])
        }
    
    # Save descriptions
    with open("diverse_targets/descriptions.json", "w") as f:
        json.dump(descriptions, f, indent=2)
    
    print("📋 Diverse challenge descriptions saved to: diverse_targets/descriptions.json")
    
    # Save categories
    categories = create_challenge_categories()
    with open("diverse_targets/categories.json", "w") as f:
        json.dump(categories, f, indent=2)
    
    print("📂 Challenge categories saved to: diverse_targets/categories.json")

def generate_sample_prompts(target):
    """Generate sample prompts based on target characteristics"""
    
    style_prompts = {
        "High Contrast": [
            f"dramatic {target['key_elements'][0]} with strong lighting",
            f"high contrast {target['description'].split()[0]} scene",
            f"bold {target['key_elements'][0]} against dark background"
        ],
        "Minimalist": [
            f"simple {target['key_elements'][0]} composition",
            f"minimalist {target['description'].split()[0]} scene",
            f"clean {target['key_elements'][0]} with negative space"
        ],
        "Complex": [
            f"detailed {target['key_elements'][0]} with many elements",
            f"busy {target['description'].split()[0]} scene",
            f"intricate {target['key_elements'][0]} with fine details"
        ],
        "Abstract": [
            f"abstract {target['key_elements'][0]} composition",
            f"artistic {target['description'].split()[0]} pattern",
            f"flowing {target['key_elements'][0]} design"
        ],
        "Urban": [
            f"modern {target['key_elements'][0]} cityscape",
            f"urban {target['description'].split()[0]} scene",
            f"contemporary {target['key_elements'][0]} environment"
        ],
        "Vintage": [
            f"vintage {target['key_elements'][0]} style",
            f"retro {target['description'].split()[0]} aesthetic",
            f"classic {target['key_elements'][0]} design"
        ],
        "Atmospheric": [
            f"moody {target['key_elements'][0]} atmosphere",
            f"atmospheric {target['description'].split()[0]} scene",
            f"mysterious {target['key_elements'][0]} environment"
        ],
        "Natural": [
            f"natural {target['key_elements'][0]} landscape",
            f"organic {target['description'].split()[0]} scene",
            f"wild {target['key_elements'][0]} environment"
        ],
        "Colorful": [
            f"vibrant {target['key_elements'][0]} display",
            f"colorful {target['description'].split()[0]} arrangement",
            f"bright {target['key_elements'][0]} collection"
        ]
    }
    
    return style_prompts.get(target['style'], [
        f"{target['key_elements'][0]} scene",
        f"{target['description'].split()[0]} image",
        f"detailed {target['key_elements'][0]}"
    ])

def get_learning_objectives(style, difficulty):
    """Get learning objectives based on style and difficulty"""
    
    objectives = {
        "High Contrast": "Learn to describe dramatic lighting, shadows, and visual contrast",
        "Minimalist": "Practice concise, focused descriptions of simple compositions",
        "Complex": "Develop skills in breaking down busy scenes into key components",
        "Abstract": "Build creative vocabulary for non-representational imagery",
        "Urban": "Learn modern and architectural vocabulary",
        "Vintage": "Practice describing historical and nostalgic elements",
        "Atmospheric": "Develop ability to describe mood and environmental conditions",
        "Natural": "Build nature and landscape description vocabulary",
        "Colorful": "Practice specific color and visual description"
    }
    
    difficulty_modifiers = {
        "Easy": "Focus on basic identification and simple descriptions",
        "Medium": "Practice detailed descriptions with multiple elements",
        "Hard": "Master complex, nuanced descriptions with artistic vocabulary"
    }
    
    return {
        "style_objective": objectives.get(style, "General visual description skills"),
        "difficulty_objective": difficulty_modifiers.get(difficulty, "Standard description practice")
    }

def main():
    """Main function"""
    print("🌈 Diverse Target Image Creator")
    print("Creating varied, contrasting images for better learning")
    print("=" * 60)
    
    # Create diverse targets
    success, targets = create_diverse_targets()
    
    if success:
        print("✅ Diverse targets created successfully!")
        
        # Create descriptions and categories
        create_diverse_descriptions(targets)
        
        print("\n🎉 Setup complete!")
        print("\n📊 Image Variety Created:")
        print("• High Contrast: Lightning, silhouettes")
        print("• Minimalist: Simple compositions, clean lines")
        print("• Complex: Busy markets, detailed close-ups")
        print("• Abstract: Flowing colors, artistic patterns")
        print("• Urban: Neon cities, modern architecture")
        print("• Vintage: Classic cars, old books")
        print("• Atmospheric: Misty forests, moody scenes")
        
        print("\n🎮 To use these targets:")
        print("python play_natural_game.py")
        print("# Then choose from diverse_targets/ folder")
        
    else:
        print("❌ Failed to create diverse targets")
        print("💡 Check your internet connection and try again")

if __name__ == "__main__":
    main()