#!/usr/bin/env python3
"""
Gamified Web Dashboard for AI Prompt Game v2.0
Beautiful interactive frontend with real-time scoring
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import numpy as np
import base64
import io
from PIL import Image
import json
from datetime import datetime
from pathlib import Path
import sys

# Add the parent directory to path to import our game modules
sys.path.append(str(Path(__file__).parent.parent))

from ai_prompt_game.comparison import ImageComparison
from ai_prompt_game.image_generator import ImageGenerator
from ai_prompt_game.game_engine import PromptGame

app = Flask(__name__)
app.secret_key = 'ai-prompt-game-dashboard-2024'

# Initialize game components
comparator = ImageComparison(verbose=False)
generator = ImageGenerator()
game = PromptGame(visual_mode=False, verbose=False)

# Game state
current_session = {
    'target': None,
    'attempts': [],
    'best_score': 0,
    'current_attempt': 0,
    'start_time': None
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/targets')
def get_targets():
    """Get available challenge targets"""
    targets = [
        {'id': 'cat', 'name': 'Cat', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '🐱'},
        {'id': 'coffee', 'name': 'Coffee', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '☕'},
        {'id': 'car', 'name': 'Car', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🚗'},
        {'id': 'foxes', 'name': 'Foxes', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦊'},
        {'id': 'llama', 'name': 'Llama', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦙'},
        {'id': 'owl', 'name': 'Owl', 'difficulty': 'Hard', 'threshold': 0.55, 'emoji': '🦉'}
    ]
    return jsonify(targets)

@app.route('/api/start_challenge', methods=['POST'])
def start_challenge():
    """Start a new challenge"""
    data = request.json
    target_id = data.get('target_id')
    
    # Load target image
    target_path = Path.home() / ".ai-prompt-game" / "targets" / f"{target_id}.jpg"
    
    if not target_path.exists():
        return jsonify({'error': 'Target image not found. Run setup first.'}), 404
    
    # Reset session
    current_session.update({
        'target': target_id,
        'attempts': [],
        'best_score': 0,
        'current_attempt': 0,
        'start_time': datetime.now().isoformat()
    })
    
    # Convert target image to base64
    target_image = cv2.imread(str(target_path))
    target_b64 = image_to_base64(target_image)
    
    return jsonify({
        'success': True,
        'target_image': target_b64,
        'target_id': target_id
    })

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """Generate image from prompt and compare"""
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    if not current_session['target']:
        return jsonify({'error': 'No active challenge'}), 400
    
    try:
        # Generate image
        generated_image = generator.generate(prompt)
        
        if generated_image is None:
            return jsonify({'error': 'Failed to generate image'}), 500
        
        # Load target image
        target_path = Path.home() / ".ai-prompt-game" / "targets" / f"{current_session['target']}.jpg"
        target_image = cv2.imread(str(target_path))
        
        # Compare images
        scores = comparator.compare(generated_image, target_image)
        
        # Get AI explanations
        explanations = comparator.explain_scores(scores)
        
        # Check passing criteria
        target_info = {'name': current_session['target'], 'difficulty': get_difficulty(current_session['target'])}
        passing_result = game.check_passing_criteria(scores['combined'], target_info)
        
        # Update session
        current_session['current_attempt'] += 1
        attempt_data = {
            'attempt': current_session['current_attempt'],
            'prompt': prompt,
            'score': scores['combined'],
            'detailed_scores': scores,
            'explanations': explanations,
            'passing_result': passing_result,
            'timestamp': datetime.now().isoformat(),
            'is_best': scores['combined'] > current_session['best_score']
        }
        
        if attempt_data['is_best']:
            current_session['best_score'] = scores['combined']
        
        current_session['attempts'].append(attempt_data)
        
        # Convert images to base64
        generated_b64 = image_to_base64(generated_image)
        target_b64 = image_to_base64(target_image)
        
        return jsonify({
            'success': True,
            'generated_image': generated_b64,
            'target_image': target_b64,
            'scores': scores,
            'explanations': explanations,
            'passing_result': passing_result,
            'attempt_number': current_session['current_attempt'],
            'is_best': attempt_data['is_best'],
            'best_score': current_session['best_score']
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/progress')
def get_progress():
    """Get user progress"""
    try:
        progress_file = Path.home() / ".ai-prompt-game" / "progress.json"
        
        if progress_file.exists():
            with open(progress_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {'overall': {'completed_challenges': 0, 'total_challenges': 6}}
        
        return jsonify(progress)
    except:
        return jsonify({'overall': {'completed_challenges': 0, 'total_challenges': 6}})

@app.route('/api/session_stats')
def get_session_stats():
    """Get current session statistics"""
    return jsonify({
        'target': current_session['target'],
        'attempts': len(current_session['attempts']),
        'best_score': current_session['best_score'],
        'current_attempt': current_session['current_attempt'],
        'start_time': current_session['start_time'],
        'recent_attempts': current_session['attempts'][-5:] if current_session['attempts'] else []
    })

def image_to_base64(image):
    """Convert OpenCV image to base64 string"""
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Convert to base64
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def get_difficulty(target_id):
    """Get difficulty for target"""
    difficulty_map = {
        'cat': 'Easy',
        'coffee': 'Easy', 
        'car': 'Medium',
        'foxes': 'Medium',
        'llama': 'Medium',
        'owl': 'Hard'
    }
    return difficulty_map.get(target_id, 'Medium')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting AI Prompt Game Dashboard...")
    print("🌐 Open your browser to: http://localhost:8080")
    print("🎮 Enjoy the gamified experience!")
    
    app.run(debug=True, host='0.0.0.0', port=8080)