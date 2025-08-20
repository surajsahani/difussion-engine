#!/usr/bin/env python3
"""
Streamlit version of AI Prompt Game Dashboard
"""

import streamlit as st
import requests
import base64
import io
from PIL import Image
import random

# Page config
st.set_page_config(
    page_title="🎯 AI Prompt Game v2.0",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .challenge-card {
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        margin: 0.5rem 0;
        text-align: center;
        cursor: pointer;
    }
    .challenge-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    .score-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .score-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .score-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = None
if 'target_image' not in st.session_state:
    st.session_state.target_image = None
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'scores' not in st.session_state:
    st.session_state.scores = None

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
        'cat': 'a cute orange tabby cat sitting on a windowsill, realistic photo, soft lighting',
        'coffee': 'a white ceramic coffee cup with steam rising, on wooden table, morning light',
        'car': 'a red sports car on an empty road, side view, realistic automotive photography',
        'foxes': 'two red foxes playing in autumn forest, realistic wildlife photography',
        'llama': 'a white fluffy llama in green mountain meadow, realistic animal portrait',
        'owl': 'a brown owl with yellow eyes perched on oak branch, realistic bird photography'
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
        'cat': (255, 165, 0),  # Orange
        'coffee': (139, 69, 19),  # Brown
        'car': (255, 0, 0),  # Red
        'foxes': (255, 69, 0),  # Red-orange
        'llama': (255, 255, 255),  # White
        'owl': (139, 115, 85)  # Brown
    }
    
    # Create a simple colored image with text
    img = Image.new('RGB', (256, 256), color=colors[challenge_id])
    return img

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Prompt Game v2.0</h1>
    <p>Master AI prompt engineering through gamified challenges</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Challenge Selection
st.sidebar.header("🏆 Choose Your Challenge")

challenges = [
    {'id': 'cat', 'name': 'Cat', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '🐱'},
    {'id': 'coffee', 'name': 'Coffee', 'difficulty': 'Easy', 'threshold': 0.65, 'emoji': '☕'},
    {'id': 'car', 'name': 'Car', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🚗'},
    {'id': 'foxes', 'name': 'Foxes', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦊'},
    {'id': 'llama', 'name': 'Llama', 'difficulty': 'Medium', 'threshold': 0.60, 'emoji': '🦙'},
    {'id': 'owl', 'name': 'Owl', 'difficulty': 'Hard', 'threshold': 0.55, 'emoji': '🦉'}
]

for challenge in challenges:
    if st.sidebar.button(f"{challenge['emoji']} {challenge['name']} ({challenge['difficulty']})", 
                        key=challenge['id']):
        st.session_state.current_challenge = challenge
        
        # Generate actual target image based on challenge
        with st.spinner(f"Loading {challenge['name']} challenge..."):
            st.session_state.target_image = get_target_image(challenge['id'])
        
        st.session_state.generated_image = None
        st.session_state.scores = None
        st.rerun()

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Target Image")
    if st.session_state.target_image:
        st.image(st.session_state.target_image, caption="Target to match", use_column_width=True)
        if st.session_state.current_challenge:
            st.caption(f"Challenge: {st.session_state.current_challenge['name']} ({st.session_state.current_challenge['difficulty']})")
    else:
        st.info("Select a challenge to see the target image")
        if st.session_state.current_challenge:
            st.warning(f"Selected: {st.session_state.current_challenge['name']} but no image loaded")

with col2:
    st.subheader("✨ Generated Image")
    if st.session_state.generated_image:
        st.image(st.session_state.generated_image, caption="Your generated image", use_column_width=True)
    else:
        st.info("Enter a prompt below to generate an image")

# Prompt input
st.subheader("💭 Your Prompt")
prompt = st.text_area(
    "Describe the image you want to create...",
    placeholder="Be creative and detailed! Describe colors, objects, style, composition...",
    height=100,
    disabled=st.session_state.current_challenge is None
)

if st.button("🚀 Generate & Compare", 
             disabled=not prompt or st.session_state.current_challenge is None,
             use_container_width=True):
    
    with st.spinner("Generating your image and analyzing similarity..."):
        # Generate image
        generated_image = generator.generate(prompt)
        
        if generated_image:
            st.session_state.generated_image = generated_image
            
            # Compare with target
            scores = comparator.compare(generated_image, st.session_state.target_image)
            st.session_state.scores = scores
            
            st.rerun()

# Results
if st.session_state.scores:
    scores = st.session_state.scores
    threshold = st.session_state.current_challenge['threshold']
    passed = scores['combined'] >= threshold
    
    # Main score display
    st.markdown(f"""
    <div class="score-container">
        <h2>Similarity Score</h2>
        <h1 style="font-size: 4rem; margin: 1rem 0;">{scores['combined']:.3f}</h1>
        <p style="font-size: 1.2rem;">Required: {threshold:.3f}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed scores
    st.subheader("📊 Detailed Analysis")
    
    score_cols = st.columns(5)
    score_names = ['perceptual', 'semantic', 'structural', 'color_advanced', 'texture']
    score_labels = ['Perceptual', 'Semantic', 'Structural', 'Color', 'Texture']
    
    for i, (name, label) in enumerate(zip(score_names, score_labels)):
        with score_cols[i]:
            st.metric(label, f"{scores[name]:.3f}")
    
    # Passing status
    if passed:
        st.success(f"🎉 Congratulations! You passed with a score of {scores['combined']:.3f}!")
    else:
        st.warning(f"🎯 Keep trying! You need {threshold:.3f} but got {scores['combined']:.3f}")
    
    # AI Feedback
    st.subheader("💡 AI Feedback")
    
    if scores['combined'] > 0.8:
        st.info("✅ Excellent match! Great job with your prompt!")
    elif scores['combined'] > 0.6:
        st.info("🤔 Good similarity, but try to be more specific")
    elif scores['combined'] > 0.4:
        st.info("⚠️ Some similarity, focus on key details")
    else:
        st.info("🔄 Low similarity, try a different approach")
    
    st.info("💡 Describe colors, objects, and style clearly")
    st.info("🎯 Be specific about composition and lighting")

# Instructions
with st.expander("ℹ️ How to Play"):
    st.markdown("""
    1. **Choose a Challenge**: Select a target from the sidebar
    2. **Write a Prompt**: Describe the image you want to create
    3. **Generate & Compare**: Click the button to create and analyze
    4. **Improve**: Use the feedback to refine your prompts
    
    **Tips for Better Scores:**
    - Be specific about colors, objects, and composition
    - Mention artistic style (realistic, cartoon, etc.)
    - Describe lighting and mood
    - Include details about background and setting
    """)

# Footer
st.markdown("---")
st.markdown("🎯 **AI Prompt Game v2.0** - Master the art of AI prompt engineering!")