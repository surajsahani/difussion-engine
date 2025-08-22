# 🎮 AI Prompt Game v2.0 - Web Dashboard Guide

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
```bash
# Navigate to the web dashboard directory
cd web_dashboard

# Run the easy startup script
python run_dashboard.py

# Open your browser to: http://localhost:8080
```

### Option 2: Auto-Launch with Browser
```bash
# This will automatically open your browser
python web_dashboard/start_game.py
```

### Option 3: Manual Flask Run
```bash
# Navigate to web dashboard
cd web_dashboard

# Run Flask app directly
python app.py
```

## 📋 Prerequisites

### 1. Install AI Prompt Game Package
```bash
# Install the core game package first
pip install ai-prompt-game

# Set up the game (downloads target images)
ai-prompt-game --setup
```

### 2. Install Web Dashboard Dependencies
```bash
# Navigate to web dashboard directory
cd web_dashboard

# Install requirements
pip install -r requirements.txt
```

**Required Dependencies:**
- Flask >= 2.3.0
- opencv-python >= 4.5.0
- numpy >= 1.21.0
- Pillow >= 9.0.0
- scikit-image >= 0.19.0
- scipy >= 1.8.0
- requests >= 2.28.0

## 🎯 How to Play

### Step 1: Start the Dashboard
```bash
cd web_dashboard
python run_dashboard.py
```

You should see:
```
🚀 AI Prompt Game v2.0 - Web Dashboard
==================================================
✅ All requirements already installed!

🌐 Starting web dashboard...
📱 Open your browser to: http://localhost:8080
🎮 Enjoy the gamified experience!

💡 Press Ctrl+C to stop the server
--------------------------------------------------
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:8080**

### Step 3: Select a Challenge
Click on any challenge card:
- 🐱 **Cat (Easy)** - 65% similarity required
- ☕ **Coffee (Easy)** - 65% similarity required  
- 🚗 **Car (Medium)** - 60% similarity required
- 🦊 **Foxes (Medium)** - 60% similarity required
- 🦙 **Llama (Medium)** - 60% similarity required
- 🦉 **Owl (Hard)** - 55% similarity required

### Step 4: Enter Your Prompt
In the text area, describe the image you want to create:

**Good Examples:**
```
"A fluffy orange tabby cat sitting on a wooden table, soft lighting, realistic photo"

"A steaming cup of coffee with latte art, white ceramic mug, wooden background"

"A red sports car on a mountain road, sunset lighting, professional photography"
```

**Tips for Better Results:**
- Be specific about colors, objects, and style
- Mention lighting and background details
- Include composition and camera angle
- Describe textures and materials

### Step 5: Generate & Compare
- Click **"Generate & Compare"** button
- Wait for AI to create your image (~5-10 seconds)
- See your generated image appear on the right
- Get detailed similarity scores and AI feedback

### Step 6: Learn & Improve
- Read the AI explanations to understand your score
- Check if you passed the challenge threshold
- Try different prompts to improve your score
- Progress through increasingly difficult challenges

## 🎨 Interface Overview

### Main Dashboard Features:

#### **Challenge Selection Grid**
- Visual cards with emojis and difficulty levels
- Click to select and load target image
- Progressive unlock system (complete easier first)

#### **Image Comparison Panel**
- **Left**: Target image you're trying to recreate
- **Right**: Your AI-generated result
- Side-by-side comparison for easy analysis

#### **Prompt Input Area**
- Large text area for creative descriptions
- Keyboard shortcut: Ctrl+Enter to generate
- Placeholder text with helpful hints

#### **Scoring Display**
- **Main Score**: Overall similarity percentage
- **Detailed Breakdown**: 5 advanced metrics
  - Perceptual (30%): Human vision similarity
  - Semantic (25%): Object and shape matching
  - Structural (20%): Layout and composition
  - Color Advanced (15%): Perceptual color matching
  - Texture (10%): Surface detail analysis

#### **AI Feedback Section**
- Intelligent explanations of your score
- Specific suggestions for improvement
- Educational insights about image similarity

#### **Progress Tracking**
- Visual progress ring showing completion
- Session statistics (attempts, best score)
- Recent attempts history with scores

## 🔧 Troubleshooting

### Common Issues:

#### **Dashboard Won't Start**
```bash
# Check if ai-prompt-game is installed
pip list | grep ai-prompt-game

# If not installed:
pip install ai-prompt-game
ai-prompt-game --setup
```

#### **Port 8080 Already in Use**
```bash
# Kill process using port 8080
lsof -ti:8080 | xargs kill -9

# Or edit app.py to use different port:
# Change port=8080 to port=8081
```

#### **Images Not Loading**
```bash
# Check if target images exist
ls ~/.ai-prompt-game/targets/

# Should show: cat.jpg, coffee.jpg, car.jpg, etc.
# If missing, run setup again:
ai-prompt-game --setup
```

#### **Generation Fails**
- **Check internet connection** (uses Pollinations.ai)
- **Try simpler prompts** first
- **Wait longer** for complex images
- **Refresh page** if stuck

#### **Scores Seem Wrong**
- This is normal! The v2.0 algorithm is much stricter
- Focus on detailed, accurate descriptions
- Use the AI feedback to improve your prompts

### **Flask Debug Mode**
```bash
# Run in debug mode for development
export FLASK_DEBUG=1
python app.py
```

### **Check Logs**
```bash
# View detailed logs
python run_dashboard.py --verbose
```

## 🎯 Tips for Success

### **Writing Better Prompts:**

#### **Be Specific About:**
- **Colors**: "bright orange tabby cat" vs "cat"
- **Lighting**: "soft morning light" vs generic
- **Style**: "realistic photograph" vs "cartoon drawing"
- **Background**: "wooden table" vs "plain background"
- **Composition**: "close-up portrait" vs "full body shot"

#### **Example Progression:**
```
❌ Bad: "cat"
⚠️  Okay: "orange cat sitting"
✅ Good: "fluffy orange tabby cat sitting on wooden table"
🎯 Excellent: "fluffy orange tabby cat with green eyes sitting on rustic wooden table, soft natural lighting, realistic photograph"
```

### **Understanding Scores:**

#### **Score Ranges:**
- **0.85-1.00**: Excellent match! 🎯
- **0.70-0.84**: Very good similarity 👍
- **0.55-0.69**: Good attempt, room for improvement 🤔
- **0.40-0.54**: Some similarity, try different approach ⚠️
- **0.00-0.39**: Very different, start over 🔄

#### **Metric Meanings:**
- **High Perceptual**: Looks similar to human eyes
- **High Semantic**: Objects and shapes match well
- **High Structural**: Good composition and layout
- **High Color**: Colors match the target
- **High Texture**: Surface details are similar

## 🚀 Advanced Usage

### **Custom Configuration:**
```python
# Edit web_dashboard/app.py
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'custom_uploads'
```

### **Different AI Models:**
```python
# In image_generator.py, change model:
generator = ImageGenerator(model_type="huggingface")  # or "replicate"
```

### **Custom Challenges:**
```python
# Add new targets in app.py:
targets.append({
    'id': 'custom', 
    'name': 'Custom', 
    'difficulty': 'Medium', 
    'threshold': 0.60, 
    'emoji': '🎨'
})
```

## 📱 Mobile Usage

The dashboard is **fully responsive** and works great on:
- **Desktop**: Full feature experience
- **Tablet**: Touch-friendly interface
- **Mobile**: Optimized layout for small screens

### **Mobile Tips:**
- Use landscape mode for better image comparison
- Tap and hold images to zoom
- Swipe between challenges easily

## 🎓 Educational Use

### **For Teachers:**
- **Classroom Demo**: Project on screen for group learning
- **Individual Practice**: Students work at their own pace
- **Progress Tracking**: Monitor student advancement
- **Skill Building**: Progressive difficulty builds expertise

### **For Students:**
- **Learn by Doing**: Hands-on prompt engineering practice
- **Immediate Feedback**: Understand what works and why
- **Gamified Learning**: Engaging and motivational
- **Skill Transfer**: Apply to other AI tools and platforms

## 🎉 Have Fun!

The AI Prompt Game v2.0 Web Dashboard makes learning prompt engineering **visual, interactive, and fun**! 

### **Remember:**
- **Experiment freely** - there's no penalty for trying
- **Learn from feedback** - the AI explanations are educational
- **Progress gradually** - start with easy challenges
- **Be creative** - unique prompts often work best
- **Practice regularly** - prompt engineering is a skill that improves with use

**Happy prompting!** 🚀✨🎯

---

## 📞 Support

### **Need Help?**
- **Check the troubleshooting section** above
- **Review the AI feedback** for specific guidance
- **Try simpler prompts** if having issues
- **Restart the dashboard** if it becomes unresponsive

### **Found a Bug?**
- **Note the exact error message**
- **Check browser console** for JavaScript errors
- **Try in a different browser**
- **Restart with fresh session**

**Enjoy mastering AI prompt engineering!** 🎮🧠