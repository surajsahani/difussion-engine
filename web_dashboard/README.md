# 🎯 AI Prompt Game v2.0 - Web Dashboard

A beautiful, gamified web interface for the AI Prompt Engineering Game with real-time scoring and progress tracking.

## ✨ Features

### 🎮 **Gamified Interface**
- **Beautiful modern UI** with smooth animations
- **Interactive challenge selection** with emoji indicators
- **Real-time image comparison** side-by-side
- **Live scoring** with detailed metric breakdown
- **Progress tracking** with visual indicators

### 📊 **Advanced Analytics**
- **Detailed similarity scores** (Perceptual, Semantic, Structural, Color, Texture)
- **AI-powered explanations** for each comparison
- **Passing criteria indicators** with auto-progression
- **Session statistics** and attempt history
- **Overall progress tracking** across all challenges

### 🎯 **Challenge System**
- **6 Progressive challenges**: Cat → Coffee → Car → Foxes → Llama → Owl
- **Difficulty levels**: Easy (65%), Medium (60%), Hard (55%)
- **Auto-unlock system** when challenges are completed
- **Visual progress ring** showing overall completion

### 🤖 **AI Integration**
- **Advanced v2.0 algorithm** with state-of-the-art computer vision
- **Real-time image generation** using Pollinations.ai
- **Intelligent feedback** explaining similarity scores
- **Adaptive scoring** based on image characteristics

## 🚀 Quick Start

### Prerequisites
```bash
# Install the AI Prompt Game first
pip install ai-prompt-game

# Set up the game (downloads challenge images)
ai-prompt-game --setup
```

### Run the Dashboard
```bash
# Navigate to dashboard directory
cd web_dashboard

# Run the dashboard (auto-installs requirements)
python run_dashboard.py
```

### Open in Browser
```
http://localhost:8080
```

## 📱 How to Use

### 1. **Select a Challenge**
- Click on any challenge card (Cat, Coffee, Car, etc.)
- See the target image appear on the left
- Note the difficulty level and required score

### 2. **Enter Your Prompt**
- Type a detailed description in the prompt box
- Be creative and specific about colors, objects, style
- Press Ctrl+Enter or click "Generate & Compare"

### 3. **View Results**
- See your generated image on the right
- Get detailed similarity scores for each metric
- Read AI explanations about what to improve
- Check if you passed the challenge threshold

### 4. **Track Progress**
- Monitor your overall completion percentage
- View session statistics and attempt history
- See your best scores and recent attempts
- Unlock new challenges as you progress

## 🎨 Interface Overview

### Main Game Area
- **Target Image**: The challenge image you're trying to recreate
- **Generated Image**: Your AI-generated result
- **Prompt Input**: Where you enter your creative descriptions
- **Score Display**: Detailed breakdown of similarity metrics
- **AI Feedback**: Intelligent suggestions for improvement

### Sidebar Panels
- **Progress Ring**: Visual completion percentage
- **Session Stats**: Current attempts and best score
- **Recent Attempts**: History of your recent tries with scores

### Challenge Selection
- **Visual Grid**: All 6 challenges with emojis and difficulty
- **Progressive Unlock**: Complete easier challenges to unlock harder ones
- **Difficulty Indicators**: Easy, Medium, Hard with required scores

## 🔧 Technical Details

### Backend (Flask)
- **RESTful API** for all game operations
- **Real-time image processing** with OpenCV
- **Advanced comparison algorithm** v2.0
- **Progress persistence** with JSON storage
- **Error handling** and validation

### Frontend (HTML/CSS/JS)
- **Responsive design** works on desktop and mobile
- **Modern CSS Grid** and Flexbox layouts
- **Smooth animations** and transitions
- **Real-time updates** with fetch API
- **Progressive enhancement** for better UX

### Image Processing
- **Multi-scale perceptual analysis**
- **Advanced semantic features** (HOG + LBP + SIFT + ORB)
- **Perceptual color matching** (LAB + Earth Mover's Distance)
- **Texture analysis** with Gabor filters
- **Adaptive weighting** based on image content

## 🎯 Scoring System

### Similarity Metrics
- **Perceptual (30%)**: How similar images look to human vision
- **Semantic (25%)**: Object and shape matching
- **Structural (20%)**: Layout and composition similarity
- **Color Advanced (15%)**: Perceptual color matching
- **Texture (10%)**: Surface detail analysis

### Passing Thresholds
- **Easy Challenges**: 65% similarity required
- **Medium Challenges**: 60% similarity required
- **Hard Challenges**: 55% similarity required

### Progress Tracking
- **Persistent storage** of completed challenges
- **Best score tracking** for each challenge
- **Attempt counting** and time tracking
- **Overall completion percentage**

## 🚀 Deployment Options

### Local Development
```bash
python run_dashboard.py
# Runs on http://localhost:8080
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app

# Using Docker (create Dockerfile)
docker build -t ai-prompt-game-dashboard .
docker run -p 8080:8080 ai-prompt-game-dashboard
```

### Cloud Deployment
- **Heroku**: Ready for deployment with Procfile
- **AWS/GCP**: Compatible with standard Python hosting
- **Vercel/Netlify**: Can be adapted for serverless

## 🎨 Customization

### Themes
- Modify CSS variables in `templates/dashboard.html`
- Change color schemes and gradients
- Adjust animations and transitions

### Challenges
- Add new target images to the game setup
- Modify difficulty thresholds in `app.py`
- Customize challenge progression order

### UI Components
- Add new metrics to the scoring display
- Customize feedback messages
- Modify progress visualization

## 🐛 Troubleshooting

### Common Issues

**Dashboard won't start**
```bash
# Make sure ai-prompt-game is installed
pip install ai-prompt-game
ai-prompt-game --setup
```

**Images not loading**
```bash
# Check if target images exist
ls ~/.ai-prompt-game/targets/
# Should show: cat.jpg, coffee.jpg, car.jpg, etc.
```

**Generation fails**
```bash
# Check internet connection (uses Pollinations.ai)
# Try with a simple prompt first
```

**Scores seem wrong**
```bash
# This is normal - the v2.0 algorithm is much stricter
# Focus on detailed, accurate descriptions
```

## 📈 Performance Tips

### For Better Scores
- **Be specific** about colors, lighting, and composition
- **Describe the style** (realistic, cartoon, artistic, etc.)
- **Mention the background** and setting details
- **Include object positions** and relationships
- **Iterate based on AI feedback**

### For Better Performance
- **Use shorter prompts** for faster generation
- **Close other browser tabs** for smoother experience
- **Refresh page** if images stop loading
- **Check network connection** for generation issues

## 🎉 Have Fun!

The AI Prompt Game v2.0 Web Dashboard makes learning prompt engineering engaging and visual. Experiment with different descriptions, learn from the AI feedback, and master the art of communicating with AI systems!

**Happy prompting!** 🚀✨