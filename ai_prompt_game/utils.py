#!/usr/bin/env python3
"""
Utility functions for the AI Prompt Game
"""

import os
import json
import requests
import cv2
from pathlib import Path
from datetime import datetime

def get_game_directory():
    """Get or create the game directory in user's home"""
    game_dir = Path.home() / ".ai-prompt-game"
    game_dir.mkdir(exist_ok=True)
    return game_dir

def setup_game_directory():
    """Setup the complete game directory structure"""
    game_dir = get_game_directory()
    
    # Create subdirectories
    (game_dir / "targets").mkdir(exist_ok=True)
    (game_dir / "sessions").mkdir(exist_ok=True)
    (game_dir / "generated").mkdir(exist_ok=True)
    
    return game_dir

def download_targets(game_dir):
    """Download target images for challenges"""
    targets_dir = game_dir / "targets"
    
    # Define target images with their URLs and metadata
    targets = [
        {
            "id": "sunset",
            "name": "Mountain Sunset",
            "difficulty": "Medium",
            "description": "Golden sunset over mountain peaks with dramatic clouds",
            "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=512&q=80",
            "filename": "mountain_sunset.jpg",
            "hints": [
                "Focus on the golden/orange colors",
                "Mention the mountain silhouettes",
                "Describe the dramatic sky"
            ]
        },
        {
            "id": "ocean",
            "name": "Ocean Waves",
            "difficulty": "Hard",
            "description": "Powerful ocean waves crashing on rocky shore",
            "url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=512&q=80",
            "filename": "ocean_waves.jpg",
            "hints": [
                "Describe the wave motion and spray",
                "Mention the rocky coastline",
                "Include the power and energy"
            ]
        },
        {
            "id": "forest",
            "name": "Misty Forest",
            "difficulty": "Medium",
            "description": "Peaceful forest path with morning mist and soft lighting",
            "url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=512&q=80",
            "filename": "forest_path.jpg",
            "hints": [
                "Mention the atmospheric mist",
                "Describe the forest path",
                "Include the soft, diffused lighting"
            ]
        },
        {
            "id": "beach",
            "name": "Tropical Beach",
            "difficulty": "Easy",
            "description": "Crystal clear tropical water with white sand beach",
            "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=512&q=80",
            "filename": "tropical_beach.jpg",
            "hints": [
                "Focus on the crystal clear water",
                "Mention the white sand",
                "Describe the tropical paradise feel"
            ]
        },
        {
            "id": "aurora",
            "name": "Northern Lights",
            "difficulty": "Hard",
            "description": "Aurora borealis dancing over snowy landscape",
            "url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=512&q=80",
            "filename": "northern_lights.jpg",
            "hints": [
                "Describe the colorful aurora lights",
                "Mention the snowy landscape",
                "Include the dancing/flowing motion"
            ]
        }
    ]
    
    downloaded_targets = []
    
    for target in targets:
        target_path = targets_dir / target["filename"]
        
        # Skip if already exists
        if target_path.exists():
            print(f"✅ {target['name']} (already exists)")
            target["path"] = str(target_path)
            downloaded_targets.append(target)
            continue
        
        # Download image
        try:
            print(f"📥 Downloading {target['name']}...")
            response = requests.get(target["url"], timeout=30)
            response.raise_for_status()
            
            with open(target_path, 'wb') as f:
                f.write(response.content)
            
            target["path"] = str(target_path)
            downloaded_targets.append(target)
            print(f"✅ {target['name']}")
            
        except Exception as e:
            print(f"❌ Failed to download {target['name']}: {e}")
    
    # Save targets metadata
    targets_file = game_dir / "targets.json"
    with open(targets_file, 'w') as f:
        json.dump(downloaded_targets, f, indent=2)
    
    print(f"\n📁 Downloaded {len(downloaded_targets)} targets")
    return downloaded_targets

def load_target_image(image_path):
    """Load a target image"""
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        return image
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None

def save_player_stats(session_stats):
    """Save player statistics"""
    game_dir = get_game_directory()
    stats_file = game_dir / "stats.json"
    
    # Load existing stats
    if stats_file.exists():
        try:
            with open(stats_file, 'r') as f:
                all_stats = json.load(f)
        except:
            all_stats = {
                'games_played': 0,
                'total_attempts': 0,
                'best_score': 0,
                'victories': 0,
                'sessions': [],
                'favorite_targets': {},
                'recent_scores': []
            }
    else:
        all_stats = {
            'games_played': 0,
            'total_attempts': 0,
            'best_score': 0,
            'victories': 0,
            'sessions': [],
            'favorite_targets': {},
            'recent_scores': []
        }
    
    # Update stats
    all_stats['games_played'] += 1
    all_stats['total_attempts'] += session_stats['attempts']
    all_stats['best_score'] = max(all_stats['best_score'], session_stats['best_score'])
    
    if session_stats['victory']:
        all_stats['victories'] += 1
    
    # Update favorite targets
    target = session_stats['target']
    all_stats['favorite_targets'][target] = all_stats['favorite_targets'].get(target, 0) + 1
    
    # Update recent scores
    all_stats['recent_scores'].append(session_stats['best_score'])
    all_stats['recent_scores'] = all_stats['recent_scores'][-20:]  # Keep last 20
    
    # Calculate average score
    if all_stats['recent_scores']:
        all_stats['average_score'] = sum(all_stats['recent_scores']) / len(all_stats['recent_scores'])
    
    # Add session
    all_stats['sessions'].append(session_stats)
    all_stats['sessions'] = all_stats['sessions'][-50:]  # Keep last 50 sessions
    
    # Save updated stats
    try:
        with open(stats_file, 'w') as f:
            json.dump(all_stats, f, indent=2)
    except Exception as e:
        print(f"⚠️  Could not save stats: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['cv2', 'numpy', 'requests', 'PIL']
    missing = []
    
    for dep in required:
        try:
            if dep == 'cv2':
                import cv2
            elif dep == 'PIL':
                from PIL import Image
            else:
                __import__(dep)
        except ImportError:
            missing.append(dep)
    
    return len(missing) == 0

def get_package_info():
    """Get package information"""
    return {
        'name': 'ai-prompt-game',
        'version': '1.0.0',
        'description': 'AI-powered reverse prompt engineering educational game',
        'author': 'Your Name',
        'url': 'https://github.com/yourusername/ai-prompt-game'
    }