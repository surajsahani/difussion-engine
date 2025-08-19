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
            "id": "car",
            "name": "car",
            "difficulty": "Hard",
            "description": "A bear driving car",
            "url": "https://images.unsplash.com/photo-1755593853479-10550d810c22?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "filename": "car.png",
            "hints": [
                "Cute bear driving a toy car illustration.",
                "Retro flat design cartoon vehicle with animal driver.",
                "Minimal playful vector art of bear in car."
            ]
        },
        {
            "id": "foxes",
            "name": "Foxes",
            "difficulty": "Medium",
            "description": "Two cute foxes sitting on tree",
            "url": "https://cdn.pixabay.com/photo/2022/12/04/00/42/foxes-7633559_1280.png",
            "filename": "foxes.png",
            "hints": [
                "Create Two Foxes setting on tree",
                "Two cute Foxes setting on tree"
                                        ]
        },
        {
            "id": "LLama",
            "name": "LLama",
            "difficulty": "Medium",
            "description": "A sheep in snow fall",
            "url": "https://images.unsplash.com/photo-1755590764677-68c742d97e8f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8MXx8fGVufDB8fHx8fA%3D%3D",
            "filename": "llama.jpg",
            "hints": [
                "Mention the atmospheric mist",
                "Describe the forest path",
                "Include the soft, diffused lighting"
            ]
        },
        {
            "id": "van",
            "name": "Van",
            "difficulty": "Easy",
            "description": "A van climbling mountain beside ocean",
            "url": "https://images.unsplash.com/photo-1755590764782-d55944ec0a61?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwcm9maWxlLXBhZ2V8Mnx8fGVufDB8fHx8fA%3D%3D",
            "filename": "van.jpg",
            "hints": [
                "Van climbing a mountain",
                "Create a illustration of blue van",
                "Can Climbing a mountain besides ocean"
            ]
        },
        {
            "id": "owl",
            "name": "owl",
            "difficulty": "Hard",
            "description": "owl illlustration",
            "url": "https://cdn.pixabay.com/photo/2022/12/04/00/01/owl-7633529_1280.png",
            "filename": "owl.png",
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