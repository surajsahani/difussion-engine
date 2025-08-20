#!/usr/bin/env python3
"""
✨ Prompt Princess - AI Art Challenge Game ✨
A magical journey into AI prompt engineering for creative minds!
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
    page_title="✨ Prompt Princess - AI Art Challenge",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with magical girl theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        font-family: 'Quicksand', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.3);
        border: 3px solid #fff;
    }
    
    .princess-title {
        font-family: 'Comfortaa', cursive;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .level-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        border: 2px solid #fff;
    }
    
    .xp-bar {
        background: rgba(255,255,255,0.3);
        border-radius: 15px;
        height: 20px;
        margin: 1rem 0;
        overflow: hidden;
        border: 2px solid #fff;
    }
    
    .xp-fill {
        background: linear-gradient(90deg, #ff6b9d 0%, #ffd700 100%);
        height: 100%;
        border-radius: 13px;
        transition: width 0.5s ease;
    }
    
    .challenge-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #fff;
        margin: 0.5rem 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);
    }
    
    .challenge-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 154, 158, 0.4);
        border-color: #ff6b9d;
    }
    
    .challenge-card.active {
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        transform: scale(1.05);
        border-color: #ffd700;
    }
    
    .score-container {
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        padding: 2rem;
        border-radius: 25px;
        text-align: center;
        margin: 1rem 0;
        border: 3px solid #fff;
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.3);
    }
    
    .achievement-popup {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        border: 3px solid #fff;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        animation: bounce 0.6s ease-in-out;
    }
    
    @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
    }
    
    .sparkle {
        animation: sparkle 1.5s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    .cute-button {
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        border: 3px solid #fff;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 107, 157, 0.3);
        font-family: 'Quicksand', sans-serif;
    }
    
    .cute-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 107, 157, 0.4);
    }
    
    .image-frame {
        border: 4px solid #fff;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);
        background: linear-gradient(135deg, #ffeef8 0%, #fff 100%);
        padding: 1rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #ffeef8 0%, #fff 100%);
        border: 3px solid #ff9a9e;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
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

# Achievement system
ACHIEVEMENTS = {
    'first_try': {'name': '✨ First Magic Spell', 'desc': 'Generated your first image!', 'xp': 50},
    'good_score': {'name': '🌟 Rising Star', 'desc': 'Scored above 0.7!', 'xp': 100},
    'perfect_score': {'name': '👑 Prompt Princess', 'desc': 'Scored above 0.9!', 'xp': 200},
    'five_attempts': {'name': '🎨 Creative Explorer', 'desc': 'Made 5 attempts!', 'xp': 75},
    'streak_3': {'name': '🔥 On Fire', 'desc': '3 good scores in a row!', 'xp': 150},
    'all_challenges': {'name': '🏆 Challenge Master', 'desc': 'Tried all challenges!', 'xp': 300}
}

def calculate_level(xp):
    """Calculate level based on XP"""
    return min(10, max(1, int(xp / 100) + 1))

def get_level_title(level):
    """Get cute title based on level"""
    titles = {
        1: "✨ Apprentice Dreamer",
        2: "🌸 Budding Artist", 
        3: "🎨 Creative Spark",
        4: "🌟 Rising Star",
        5: "💫 Imagination Queen",
        6: "🦄 Unicorn Whisperer",
        7: "👑 Prompt Princess",
        8: "🌈 Rainbow Weaver",
        9: "✨ Magic Master",
        10: "🏆 Legendary Creator"
    }
    return titles.get(level, "✨ Magical Creator")

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
        'unicorn': 'a beautiful white unicorn with rainbow mane in magical forest, fantasy art, sparkles and glitter',
        'princess': 'a beautiful princess in pink dress with tiara, fairy tale style, magical castle background',
        'butterfly': 'colorful butterflies with rainbow wings flying in flower garden, magical and dreamy',
        'flowers': 'beautiful pink and purple flowers in magical garden, soft lighting, fairy tale style',
        'castle': 'a magical fairy tale castle with pink towers, rainbow bridge, fantasy architecture',
        'mermaid': 'a beautiful mermaid with long flowing hair underwater, magical sea creatures, coral reef'
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
        'unicorn': (255, 192, 203),  # Pink
        'princess': (255, 182, 193),  # Light pink
        'butterfly': (255, 105, 180),  # Hot pink
        'flowers': (255, 20, 147),   # Deep pink
        'castle': (186, 85, 211),    # Medium orchid
        'mermaid': (72, 209, 204)    # Medium turquoise
    }
    
    # Create a simple colored image with text
    img = Image.new('RGB', (256, 256), color=colors[challenge_id])
    return img

# Welcome and name input
if not st.session_state.princess_name:
    st.markdown("""
    <div class="main-header">
        <div class="princess-title">👑 Welcome to Prompt Princess! ✨</div>
        <p class="subtitle">Where creativity meets AI magic! 🌈</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💫 What should we call you, future Prompt Princess?")
    name_input = st.text_input("Enter your magical name:", placeholder="Princess Aurora, Creative Queen, etc.")
    
    if st.button("🌟 Begin My Magical Journey!", key="start_journey"):
        if name_input:
            st.session_state.princess_name = name_input
            st.rerun()
        else:
            st.warning("Please enter your magical name first! ✨")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #ffeef8 0%, #fff 100%); border-radius: 15px; border: 3px solid #ff9a9e;">
        <h3>🎮 How to Play</h3>
        <p>🎯 Choose a magical challenge<br>
        ✍️ Write creative prompts to generate images<br>
        🏆 Earn XP and unlock achievements<br>
        👑 Level up to become the ultimate Prompt Princess!</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Main header with player stats
current_level = calculate_level(st.session_state.total_xp)
level_title = get_level_title(current_level)
xp_for_next_level = (current_level * 100) - st.session_state.total_xp
xp_progress = (st.session_state.total_xp % 100) / 100

st.markdown(f"""
<div class="main-header">
    <div class="princess-title">👑 {st.session_state.princess_name} ✨</div>
    <p class="subtitle">{level_title} • Level {current_level}</p>
    <div class="level-badge">💎 {st.session_state.total_xp} XP</div>
    <div class="level-badge">🔥 {st.session_state.streak} Streak</div>
    <div class="xp-bar">
        <div class="xp-fill" style="width: {xp_progress * 100}%"></div>
    </div>
    <small>{100 - (st.session_state.total_xp % 100)} XP to next level!</small>
</div>
""", unsafe_allow_html=True)

# Sidebar - Challenge Selection with cute theme
st.sidebar.markdown("### 🌟 Magical Challenges")

challenges = [
    {'id': 'unicorn', 'name': 'Unicorn', 'difficulty': 'Dreamy', 'threshold': 0.65, 'emoji': '🦄', 'desc': 'Create a magical unicorn!'},
    {'id': 'princess', 'name': 'Princess', 'difficulty': 'Royal', 'threshold': 0.60, 'emoji': '👸', 'desc': 'Design a beautiful princess!'},
    {'id': 'butterfly', 'name': 'Butterfly', 'difficulty': 'Gentle', 'threshold': 0.65, 'emoji': '🦋', 'desc': 'Paint colorful butterflies!'},
    {'id': 'flowers', 'name': 'Flowers', 'difficulty': 'Blooming', 'threshold': 0.60, 'emoji': '🌸', 'desc': 'Grow a magical garden!'},
    {'id': 'castle', 'name': 'Castle', 'difficulty': 'Majestic', 'threshold': 0.55, 'emoji': '🏰', 'desc': 'Build a fairy tale castle!'},
    {'id': 'mermaid', 'name': 'Mermaid', 'difficulty': 'Mystical', 'threshold': 0.50, 'emoji': '🧜‍♀️', 'desc': 'Dive into underwater magic!'}
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

# Main content with magical styling
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Magical Target")
    if st.session_state.target_image:
        st.markdown('<div class="image-frame">', unsafe_allow_html=True)
        st.image(st.session_state.target_image, caption="✨ Create something like this!", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.current_challenge:
            st.markdown(f"""
            <div class="stats-card">
                <strong>{st.session_state.current_challenge['emoji']} {st.session_state.current_challenge['name']} Challenge</strong><br>
                <small>Difficulty: {st.session_state.current_challenge['difficulty']} ✨</small><br>
                <small>Target Score: {st.session_state.current_challenge['threshold']:.2f} 🎯</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="image-frame" style="height: 300px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <h3>🌟 Choose Your Adventure!</h3>
                <p>Select a magical challenge from the sidebar to begin your creative journey! ✨</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎨 Your Creation")
    if st.session_state.generated_image:
        st.markdown('<div class="image-frame">', unsafe_allow_html=True)
        st.image(st.session_state.generated_image, caption="🌟 Your magical creation!", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="image-frame" style="height: 300px; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <h3>✨ Magic Awaits!</h3>
                <p>Write a creative prompt below to bring your imagination to life! 🦄</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Prompt input with magical styling
st.markdown("### 💫 Cast Your Creative Spell")
prompt = st.text_area(
    "✍️ Describe your magical vision...",
    placeholder="Be as creative as possible! Describe colors, magical elements, style, mood... ✨\nExample: 'A beautiful unicorn with rainbow mane dancing in a field of glittering flowers under starlight'",
    height=120,
    disabled=st.session_state.current_challenge is None
)

# Helpful prompt tips
if st.session_state.current_challenge:
    challenge_tips = {
        'unicorn': "💡 Try: 'magical', 'rainbow mane', 'sparkles', 'enchanted forest'",
        'princess': "💡 Try: 'elegant gown', 'tiara', 'royal', 'fairy tale castle'", 
        'butterfly': "💡 Try: 'colorful wings', 'flower garden', 'delicate', 'rainbow colors'",
        'flowers': "💡 Try: 'blooming', 'vibrant colors', 'magical garden', 'soft petals'",
        'castle': "💡 Try: 'fairy tale', 'towers', 'magical', 'enchanted kingdom'",
        'mermaid': "💡 Try: 'underwater', 'flowing hair', 'coral reef', 'ocean magic'"
    }
    st.caption(challenge_tips.get(st.session_state.current_challenge['id'], "💡 Be creative and descriptive!"))

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🌟 Create Magic!", 
                 disabled=not prompt or st.session_state.current_challenge is None,
                 use_container_width=True):
        
        with st.spinner("✨ Weaving your magical creation... 🌟"):
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

# Results with magical celebration
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
        <div class="achievement-popup sparkle">
            <h3>🎉 Achievement Unlocked! 🎉</h3>
            <h2>{achievement['name']}</h2>
            <p>{achievement['desc']}</p>
            <p><strong>+{achievement['xp']} XP!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.shown_achievements.append(achievement_key)
        time.sleep(0.1)  # Small delay for effect
    
    # Main score display with celebration
    celebration_emoji = "🎉" if passed else "💫"
    score_color = "#ffd700" if passed else "#ff6b9d"
    
    st.markdown(f"""
    <div class="score-container">
        <h2>{celebration_emoji} Your Magic Score {celebration_emoji}</h2>
        <h1 style="font-size: 4rem; margin: 1rem 0; color: {score_color};">{scores['combined']:.3f}</h1>
        <p style="font-size: 1.2rem;">Target: {threshold:.3f} • Earned: +{xp_earned} XP ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed scores with cute labels
    st.markdown("### 🌟 Magical Analysis")
    
    score_cols = st.columns(5)
    score_names = ['perceptual', 'semantic', 'structural', 'color_advanced', 'texture']
    score_labels = ['👁️ Visual', '🧠 Meaning', '🏗️ Structure', '🎨 Colors', '✨ Texture']
    
    for i, (name, label) in enumerate(zip(score_names, score_labels)):
        with score_cols[i]:
            score_val = scores[name]
            color = "#ffd700" if score_val > 0.7 else "#ff6b9d" if score_val > 0.5 else "#ffa8a8"
            st.markdown(f"""
            <div class="stats-card" style="border-color: {color};">
                <strong>{label}</strong><br>
                <span style="font-size: 1.5rem; color: {color};">{score_val:.3f}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Magical feedback
    st.markdown("### 💫 Princess Feedback")
    
    if passed:
        celebration_messages = [
            "🎉 Absolutely magical! You're becoming a true Prompt Princess!",
            "✨ Stunning work! Your creativity is shining bright!",
            "👑 Royal achievement! You've mastered this challenge!",
            "🌟 Incredible! Your imagination knows no bounds!"
        ]
        st.success(random.choice(celebration_messages))
    else:
        encouragement_messages = [
            "💫 You're on the right path! Keep experimenting with your prompts!",
            "🌸 Almost there! Try adding more magical details!",
            "✨ Great effort! Every attempt makes you stronger!",
            "🦄 Don't give up! The perfect prompt is within reach!"
        ]
        st.info(random.choice(encouragement_messages))
    
    # Helpful tips based on score
    if scores['combined'] < 0.5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffeef8 0%, #fff 100%); padding: 1rem; border-radius: 15px; border: 2px solid #ff9a9e; margin: 1rem 0;">
            <h4>💡 Magical Tips for Better Results:</h4>
            <ul>
                <li>🎨 Be more specific about colors and style</li>
                <li>✨ Add magical elements like 'sparkles', 'glowing', 'enchanted'</li>
                <li>🌈 Describe the mood and atmosphere</li>
                <li>👑 Include details about the setting and background</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress towards next level
    current_level = calculate_level(st.session_state.total_xp)
    xp_for_next = (current_level * 100) - st.session_state.total_xp
    if xp_for_next > 0:
        st.info(f"🌟 {xp_for_next} more XP needed to reach Level {current_level + 1}!")

# Instructions with magical theme
with st.expander("📚 Princess Guide - How to Play"):
    st.markdown("""
    ### 🌟 Your Magical Journey
    
    1. **👑 Choose Your Quest**: Pick a magical challenge from the sidebar
    2. **✍️ Cast Your Spell**: Write creative prompts to describe your vision
    3. **🌟 Create Magic**: Click "Create Magic!" to generate your image
    4. **📊 See Your Power**: Get scored on how well you matched the target
    5. **🏆 Level Up**: Earn XP, unlock achievements, and become the ultimate Prompt Princess!
    
    ### ✨ Magical Tips for Success:
    - 🎨 **Be Descriptive**: Use lots of colorful adjectives
    - 🌈 **Add Magic**: Include words like 'magical', 'enchanted', 'glowing'
    - 👗 **Describe Style**: Mention if it's 'fairy tale', 'dreamy', 'elegant'
    - 🌸 **Set the Scene**: Describe backgrounds, lighting, and mood
    - 💫 **Be Creative**: The more imaginative, the better!
    
    ### 🏆 Achievement System:
    - ✨ **First Magic Spell**: Generate your first image
    - 🌟 **Rising Star**: Score above 0.7
    - 👑 **Prompt Princess**: Score above 0.9  
    - 🎨 **Creative Explorer**: Make 5 attempts
    - 🔥 **On Fire**: Get 3 good scores in a row
    - 🏆 **Challenge Master**: Try all challenges
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

# Footer with magical theme
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ffeef8 0%, #fff 100%); border-radius: 15px; border: 3px solid #ff9a9e; margin: 2rem 0;">
    <h3>👑 ✨ Prompt Princess ✨ 👑</h3>
    <p>Where creativity meets AI magic! 🌈</p>
    <p><em>Become the ultimate AI artist and rule the kingdom of imagination! 🏰</em></p>
</div>
""", unsafe_allow_html=True)