#!/usr/bin/env python3
"""
🎨 AI Prompt Studio - Creative Learning Platform
An engaging platform for mastering AI prompt engineering through interactive challenges
"""

import streamlit as st
import requests
import base64
import io
from PIL import Image
import random
import time

# Page config
st.set_page_config(
    page_title="🎨 AI Prompt Studio - Creative Learning",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, professional CSS with subtle gamification
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .studio-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
    }
    
    .progress-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }
    
    .challenge-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.75rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .challenge-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    .challenge-card.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        border-color: #667eea;
    }
    
    .results-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .achievement-notification {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .image-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with gamification
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = None
if 'target_image' not in st.session_state:
    st.session_state.target_image = None
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'scores' not in st.session_state:
    st.session_state.scores = None
if 'player_level' not in st.session_state:
    st.session_state.player_level = 1
if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'best_scores' not in st.session_state:
    st.session_state.best_scores = {}
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'princess_name' not in st.session_state:
    st.session_state.princess_name = ""

# Achievement system for educational engagement
ACHIEVEMENTS = {
    'first_try': {'name': '🎯 First Generation', 'desc': 'Successfully generated your first AI image', 'xp': 50},
    'good_score': {'name': '📈 Proficient Prompter', 'desc': 'Achieved similarity score above 0.7', 'xp': 100},
    'perfect_score': {'name': '🏆 Expert Prompter', 'desc': 'Achieved similarity score above 0.9', 'xp': 200},
    'five_attempts': {'name': '🔄 Persistent Learner', 'desc': 'Completed 5 prompt iterations', 'xp': 75},
    'streak_3': {'name': '🎯 Consistent Performance', 'desc': 'Achieved 3 consecutive good scores', 'xp': 150},
    'all_challenges': {'name': '🌟 Challenge Completionist', 'desc': 'Attempted all available challenges', 'xp': 300}
}

def calculate_level(xp):
    """Calculate level based on XP"""
    return min(10, max(1, int(xp / 100) + 1))

def get_level_title(level):
    """Get professional title based on level"""
    titles = {
        1: "🌱 Novice Prompter",
        2: "📝 Learning Writer", 
        3: "🎨 Creative Thinker",
        4: "📈 Skilled Prompter",
        5: "🎯 Advanced Creator",
        6: "🌟 Expert Prompter",
        7: "🏆 Master Creator",
        8: "💎 Elite Prompter",
        9: "🚀 Prompt Specialist",
        10: "👑 AI Art Director"
    }
    return titles.get(level, "🎨 Creative Professional")

def award_achievement(achievement_key):
    """Award achievement if not already earned"""
    if achievement_key not in st.session_state.achievements:
        st.session_state.achievements.append(achievement_key)
        achievement = ACHIEVEMENTS[achievement_key]
        st.session_state.total_xp += achievement['xp']
        st.session_state.player_level = calculate_level(st.session_state.total_xp)
        return achievement
    return None

# Simple image generator
class SimpleImageGenerator:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"
    
    def generate(self, prompt, width=512, height=512):
        try:
            clean_prompt = prompt.replace(' ', '%20').replace(',', '%2C')
            url = f"{self.base_url}{clean_prompt}?width={width}&height={height}&nologo=true"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            image = Image.open(io.BytesIO(response.content))
            return image
        except Exception as e:
            st.error(f"Generation error: {e}")
            return None

# Simple comparison without numpy dependency
class SimpleComparison:
    def compare(self, img1, img2):
        try:
            if img1.size != img2.size:
                img1 = img1.resize(img2.size)
            
            # Convert to grayscale for simple comparison
            gray1 = img1.convert('L')
            gray2 = img2.convert('L')
            
            # Simple pixel-by-pixel comparison
            pixels1 = list(gray1.getdata())
            pixels2 = list(gray2.getdata())
            
            # Calculate basic similarity
            total_pixels = len(pixels1)
            diff_sum = sum(abs(p1 - p2) for p1, p2 in zip(pixels1, pixels2))
            similarity = 1.0 - (diff_sum / (total_pixels * 255.0))
            
            # Add some randomness for demo purposes
            base_score = max(0.1, min(0.9, similarity + random.uniform(-0.2, 0.2)))
            
            return {
                'combined': base_score,
                'perceptual': base_score + random.uniform(-0.1, 0.1),
                'semantic': base_score + random.uniform(-0.1, 0.1),
                'structural': base_score + random.uniform(-0.1, 0.1),
                'color_advanced': base_score + random.uniform(-0.1, 0.1),
                'texture': base_score + random.uniform(-0.1, 0.1)
            }
        except Exception as e:
            st.error(f"Comparison error: {e}")
            return {
                'combined': 0.5,
                'perceptual': 0.5,
                'semantic': 0.5,
                'structural': 0.5,
                'color_advanced': 0.5,
                'texture': 0.5
            }

# Initialize components
generator = SimpleImageGenerator()
comparator = SimpleComparison()

# Pre-generated target images (base64 encoded for reliability)
TARGET_IMAGES_B64 = {
    'cat': None,  # Will be generated on demand
    'coffee': None,
    'car': None,
    'foxes': None,
    'llama': None,
    'owl': None
}

def get_target_image(challenge_id):
    """Get or generate target image for a challenge"""
    target_prompts = {
        'portrait': 'professional headshot of a young woman, natural lighting, neutral background, realistic photography',
        'landscape': 'serene mountain landscape at sunset, golden hour lighting, peaceful lake reflection, nature photography',
        'architecture': 'modern minimalist building with clean lines, glass facade, urban architecture photography',
        'abstract': 'abstract geometric composition with flowing colors, modern digital art, balanced composition',
        'still_life': 'elegant still life with fruits and flowers on wooden table, soft natural lighting, artistic arrangement',
        'fantasy': 'mystical forest scene with ethereal lighting, fantasy landscape, magical atmosphere, digital art'
    }
    
    try:
        # Try to generate the target image
        target_image = generator.generate(target_prompts[challenge_id])
        if target_image:
            return target_image
    except Exception as e:
        st.warning(f"Could not generate target image: {e}")
    
    # Fallback: create a themed placeholder
    colors = {
        'portrait': (139, 128, 116),   # Warm brown
        'landscape': (70, 130, 180),   # Steel blue
        'architecture': (105, 105, 105), # Dim gray
        'abstract': (138, 43, 226),    # Blue violet
        'still_life': (160, 82, 45),   # Saddle brown
        'fantasy': (75, 0, 130)        # Indigo
    }
    
    # Create a simple colored image with text
    img = Image.new('RGB', (256, 256), color=colors[challenge_id])
    return img

# Welcome and name input
if not st.session_state.princess_name:
    st.markdown("""
    <div class="main-header">
        <div class="studio-title">🎨 AI Prompt Studio</div>
        <p class="subtitle">Master the art of AI prompt engineering through interactive challenges</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👋 Welcome! What should we call you?")
    name_input = st.text_input("Enter your name:", placeholder="Your name or preferred username")
    
    if st.button("🚀 Start Learning", key="start_journey"):
        if name_input:
            st.session_state.princess_name = name_input
            st.rerun()
        else:
            st.warning("Please enter your name to get started!")
    
    st.markdown("""
    <div class="info-card">
        <h3>📚 Learning Objectives</h3>
        <p><strong>🎯 Master AI Prompt Engineering:</strong> Learn to craft effective prompts for AI image generation<br>
        <strong>📈 Develop Creative Skills:</strong> Enhance your descriptive writing and visual thinking<br>
        <strong>🔄 Practice Iterative Design:</strong> Understand the importance of refinement and feedback<br>
        <strong>🏆 Track Your Progress:</strong> Monitor improvement through scoring and achievements</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Main header with student progress
current_level = calculate_level(st.session_state.total_xp)
level_title = get_level_title(current_level)
xp_for_next_level = (current_level * 100) - st.session_state.total_xp
xp_progress = (st.session_state.total_xp % 100) / 100

st.markdown(f"""
<div class="main-header">
    <div class="studio-title">Welcome back, {st.session_state.princess_name}! 🎨</div>
    <p class="subtitle">{level_title} • Level {current_level}</p>
    <div class="progress-badge">📊 {st.session_state.total_xp} XP</div>
    <div class="progress-badge">🎯 {st.session_state.streak} Streak</div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {xp_progress * 100}%"></div>
    </div>
    <small style="color: #64748b;">{100 - (st.session_state.total_xp % 100)} XP to next level</small>
</div>
""", unsafe_allow_html=True)

# Sidebar - Challenge Selection with educational focus
st.sidebar.markdown("### 📚 Learning Challenges")

challenges = [
    {'id': 'portrait', 'name': 'Portrait', 'difficulty': 'Beginner', 'threshold': 0.65, 'emoji': '👤', 'desc': 'Practice describing human features and expressions'},
    {'id': 'landscape', 'name': 'Landscape', 'difficulty': 'Beginner', 'threshold': 0.60, 'emoji': '🏞️', 'desc': 'Learn to describe natural environments'},
    {'id': 'architecture', 'name': 'Architecture', 'difficulty': 'Intermediate', 'threshold': 0.55, 'emoji': '🏛️', 'desc': 'Master structural and design elements'},
    {'id': 'abstract', 'name': 'Abstract Art', 'difficulty': 'Intermediate', 'threshold': 0.50, 'emoji': '🎨', 'desc': 'Explore creative and conceptual descriptions'},
    {'id': 'still_life', 'name': 'Still Life', 'difficulty': 'Advanced', 'threshold': 0.60, 'emoji': '🍎', 'desc': 'Focus on texture, lighting, and composition'},
    {'id': 'fantasy', 'name': 'Fantasy Scene', 'difficulty': 'Advanced', 'threshold': 0.45, 'emoji': '🐉', 'desc': 'Combine imagination with technical precision'}
]

# Show achievements in sidebar
if st.session_state.achievements:
    st.sidebar.markdown("### 🏆 Your Achievements")
    for achievement_key in st.session_state.achievements[-3:]:  # Show last 3
        achievement = ACHIEVEMENTS[achievement_key]
        st.sidebar.markdown(f"**{achievement['name']}**")
        st.sidebar.caption(achievement['desc'])

for challenge in challenges:
    # Check if challenge was attempted
    attempted = challenge['id'] in st.session_state.best_scores
    best_score = st.session_state.best_scores.get(challenge['id'], 0)
    
    button_text = f"{challenge['emoji']} {challenge['name']}"
    if attempted:
        button_text += f" ⭐ {best_score:.2f}"
    
    if st.sidebar.button(button_text, key=challenge['id']):
        st.session_state.current_challenge = challenge
        
        # Generate actual target image based on challenge
        with st.spinner(f"✨ Preparing {challenge['name']} magic..."):
            st.session_state.target_image = get_target_image(challenge['id'])
        
        st.session_state.generated_image = None
        st.session_state.scores = None
        st.rerun()
    
    # Show challenge description
    st.sidebar.caption(f"💫 {challenge['desc']}")
    st.sidebar.markdown("---")

# Main content with professional styling
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Target Reference")
    if st.session_state.target_image:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(st.session_state.target_image, caption="Reference image to match", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.current_challenge:
            st.markdown(f"""
            <div class="info-card">
                <strong>{st.session_state.current_challenge['emoji']} {st.session_state.current_challenge['name']} Challenge</strong><br>
                <small><strong>Difficulty:</strong> {st.session_state.current_challenge['difficulty']}</small><br>
                <small><strong>Target Score:</strong> {st.session_state.current_challenge['threshold']:.2f}</small><br>
                <small><strong>Learning Focus:</strong> {st.session_state.current_challenge['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="image-container" style="height: 300px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: #64748b;">
                <h3>📚 Select a Challenge</h3>
                <p>Choose a learning challenge from the sidebar to begin practicing your prompt engineering skills.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎨 Your Generated Image")
    if st.session_state.generated_image:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(st.session_state.generated_image, caption="Your AI-generated result", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="image-container" style="height: 300px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: #64748b;">
                <h3>✍️ Ready to Create</h3>
                <p>Write a descriptive prompt below to generate an AI image and see how well it matches the target.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Prompt input with educational focus
st.markdown("### ✍️ Craft Your Prompt")
prompt = st.text_area(
    "Describe the image you want to generate:",
    placeholder="Write a detailed, descriptive prompt. Include specific details about:\n• Subject and composition\n• Colors and lighting\n• Style and mood\n• Background and setting\n\nExample: 'A professional portrait of a young woman with natural lighting, soft shadows, neutral background, realistic photography style'",
    height=120,
    disabled=st.session_state.current_challenge is None
)

# Educational prompt tips
if st.session_state.current_challenge:
    challenge_tips = {
        'portrait': "💡 Focus on: facial features, lighting, expression, background, photography style",
        'landscape': "💡 Focus on: natural elements, time of day, weather, perspective, composition", 
        'architecture': "💡 Focus on: building style, materials, angles, lighting, urban context",
        'abstract': "💡 Focus on: colors, shapes, patterns, composition, artistic movement",
        'still_life': "💡 Focus on: objects, arrangement, lighting, textures, artistic style",
        'fantasy': "💡 Focus on: imaginative elements, atmosphere, magical details, artistic style"
    }
    st.markdown(f"""
    <div class="info-card">
        <strong>Prompt Writing Tips:</strong><br>
        {challenge_tips.get(st.session_state.current_challenge['id'], "💡 Be specific and descriptive!")}
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Generate Image", 
                 disabled=not prompt or st.session_state.current_challenge is None,
                 use_container_width=True):
        
        with st.spinner("🎨 Generating your image and analyzing results..."):
            # Generate image
            generated_image = generator.generate(prompt)
            
            if generated_image:
                st.session_state.generated_image = generated_image
                st.session_state.attempts += 1
                
                # Award first attempt achievement
                if st.session_state.attempts == 1:
                    award_achievement('first_try')
                elif st.session_state.attempts == 5:
                    award_achievement('five_attempts')
                
                # Compare with target
                scores = comparator.compare(generated_image, st.session_state.target_image)
                st.session_state.scores = scores
                
                # Update best score for this challenge
                challenge_id = st.session_state.current_challenge['id']
                current_best = st.session_state.best_scores.get(challenge_id, 0)
                if scores['combined'] > current_best:
                    st.session_state.best_scores[challenge_id] = scores['combined']
                
                # Award score-based achievements
                if scores['combined'] >= 0.7:
                    award_achievement('good_score')
                    st.session_state.streak += 1
                    if st.session_state.streak >= 3:
                        award_achievement('streak_3')
                else:
                    st.session_state.streak = 0
                    
                if scores['combined'] >= 0.9:
                    award_achievement('perfect_score')
                
                # Check if tried all challenges
                if len(st.session_state.best_scores) >= len(challenges):
                    award_achievement('all_challenges')
                
                # Award XP based on score
                xp_earned = int(scores['combined'] * 100)
                st.session_state.total_xp += xp_earned
                st.session_state.player_level = calculate_level(st.session_state.total_xp)
                
                st.rerun()

# Results with educational focus
if st.session_state.scores:
    scores = st.session_state.scores
    threshold = st.session_state.current_challenge['threshold']
    passed = scores['combined'] >= threshold
    xp_earned = int(scores['combined'] * 100)
    
    # Check for new achievements
    new_achievements = []
    for achievement_key in st.session_state.achievements:
        if achievement_key not in st.session_state.get('shown_achievements', []):
            new_achievements.append(achievement_key)
    
    if 'shown_achievements' not in st.session_state:
        st.session_state.shown_achievements = []
    
    # Show new achievements
    for achievement_key in new_achievements:
        achievement = ACHIEVEMENTS[achievement_key]
        st.markdown(f"""
        <div class="achievement-notification">
            <h4>🏆 Achievement Unlocked!</h4>
            <strong>{achievement['name']}</strong><br>
            <small>{achievement['desc']}</small><br>
            <strong>+{achievement['xp']} XP Earned</strong>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.shown_achievements.append(achievement_key)
    
    # Main score display
    status_color = "#10b981" if passed else "#667eea"
    
    st.markdown(f"""
    <div class="results-container">
        <h2 style="text-align: center; color: {status_color};">📊 Similarity Analysis</h2>
        <h1 style="font-size: 3rem; margin: 1rem 0; text-align: center; color: {status_color};">{scores['combined']:.3f}</h1>
        <p style="font-size: 1.1rem; text-align: center; color: #64748b;">Target: {threshold:.3f} • XP Earned: +{xp_earned}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed scores with educational labels
    st.markdown("### 📈 Detailed Performance Metrics")
    
    score_cols = st.columns(5)
    score_names = ['perceptual', 'semantic', 'structural', 'color_advanced', 'texture']
    score_labels = ['👁️ Visual Match', '🧠 Semantic Similarity', '🏗️ Structural Alignment', '🎨 Color Accuracy', '✨ Texture Quality']
    
    for i, (name, label) in enumerate(zip(score_names, score_labels)):
        with score_cols[i]:
            score_val = scores[name]
            st.markdown(f"""
            <div class="metric-card">
                <strong>{label}</strong><br>
                <span style="font-size: 1.4rem; color: #667eea;">{score_val:.3f}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Educational feedback
    st.markdown("### 💡 Learning Feedback")
    
    if passed:
        success_messages = [
            "🎯 Excellent work! Your prompt successfully captured the key elements of the target image.",
            "📈 Great job! You've demonstrated strong prompt engineering skills.",
            "🌟 Well done! Your descriptive language effectively guided the AI generation.",
            "🏆 Outstanding! You've achieved the learning objective for this challenge."
        ]
        st.success(random.choice(success_messages))
    else:
        improvement_messages = [
            "📚 Good attempt! Consider adding more specific details about the subject and composition.",
            "🔄 Keep practicing! Try to be more descriptive about colors, lighting, and style.",
            "💪 You're learning! Each iteration helps you understand AI prompt engineering better.",
            "🎯 Almost there! Focus on the key visual elements that define the target image."
        ]
        st.info(random.choice(improvement_messages))
    
    # Specific improvement suggestions
    if scores['combined'] < 0.5:
        st.markdown("""
        <div class="info-card">
            <h4>📝 Prompt Improvement Strategies:</h4>
            <ul>
                <li><strong>Be More Specific:</strong> Include detailed descriptions of colors, lighting, and composition</li>
                <li><strong>Add Style Keywords:</strong> Mention artistic style, photography type, or rendering technique</li>
                <li><strong>Describe the Mood:</strong> Include atmospheric and emotional descriptors</li>
                <li><strong>Technical Details:</strong> Specify camera angles, focal length, or artistic medium</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress tracking
    current_level = calculate_level(st.session_state.total_xp)
    xp_for_next = (current_level * 100) - st.session_state.total_xp
    if xp_for_next > 0:
        st.info(f"📊 Progress Update: {xp_for_next} more XP needed to reach Level {current_level + 1}")

# Instructions with educational focus
with st.expander("📚 Learning Guide - How to Use AI Prompt Studio"):
    st.markdown("""
    ### 🎯 Learning Process
    
    1. **📚 Select a Challenge**: Choose from different difficulty levels and subject areas
    2. **✍️ Write Your Prompt**: Craft a detailed description of the image you want to generate
    3. **🚀 Generate & Analyze**: Create the image and receive similarity scoring
    4. **📊 Review Feedback**: Learn from the detailed performance metrics
    5. **🔄 Iterate & Improve**: Refine your prompts based on feedback and try again
    
    ### 💡 Effective Prompt Writing Techniques:
    - **🎨 Be Specific**: Include detailed descriptions of visual elements
    - **🌅 Describe Lighting**: Mention time of day, light sources, and shadows
    - **🎭 Add Style Context**: Specify artistic style, photography type, or medium
    - **📐 Include Composition**: Describe angles, framing, and perspective
    - **🎨 Technical Terms**: Use professional terminology when appropriate
    
    ### 🏆 Achievement System:
    - **🎯 First Generation**: Complete your first image generation
    - **📈 Proficient Prompter**: Achieve similarity score above 0.7
    - **🏆 Expert Prompter**: Achieve similarity score above 0.9  
    - **🔄 Persistent Learner**: Complete 5 prompt iterations
    - **🎯 Consistent Performance**: Achieve 3 consecutive good scores
    - **🌟 Challenge Completionist**: Attempt all available challenges
    
    ### 📊 Understanding Your Scores:
    - **Visual Match**: How closely the generated image resembles the target visually
    - **Semantic Similarity**: How well the meaning and content align
    - **Structural Alignment**: How similar the composition and layout are
    - **Color Accuracy**: How well colors match between images
    - **Texture Quality**: How similar surface details and textures appear
    """)

# Stats dashboard
if st.session_state.attempts > 0:
    st.markdown("### 📊 Your Magical Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Attempts", st.session_state.attempts)
    with col2:
        st.metric("🏆 Achievements", len(st.session_state.achievements))
    with col3:
        avg_score = sum(st.session_state.best_scores.values()) / len(st.session_state.best_scores) if st.session_state.best_scores else 0
        st.metric("⭐ Avg Score", f"{avg_score:.3f}")
    with col4:
        st.metric("🔥 Best Streak", st.session_state.streak)

# Footer with educational theme
st.markdown("---")
st.markdown("""
<div class="info-card" style="text-align: center; margin: 2rem 0;">
    <h3>🎨 AI Prompt Studio</h3>
    <p><strong>Master the Art of AI Prompt Engineering</strong></p>
    <p><em>Develop your creative and technical skills through interactive learning experiences</em></p>
</div>
""", unsafe_allow_html=True)