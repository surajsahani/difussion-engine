# 🚀 How to Run AI Prompt Game v2.0

## 🎯 Three Easy Ways to Get Started

### 1. 🚀 **Super Easy - One Click** (Recommended)
```bash
python quick_start.py
```
**What it does:**
- ✅ Checks your Python version
- ✅ Installs the AI Prompt Game package
- ✅ Downloads challenge images
- ✅ Installs web dashboard requirements
- ✅ Starts the web dashboard
- ✅ Opens your browser automatically

**Perfect for:** First-time users, students, quick demos

---

### 2. 🌐 **Web Dashboard** (Visual & Interactive)
```bash
# Step 1: Install the game
pip install ai-prompt-game
ai-prompt-game --setup

# Step 2: Start web dashboard
cd web_dashboard
python run_dashboard.py

# Step 3: Open browser
# Go to: http://localhost:8080
```

**Features:**
- 🎮 Beautiful gamified interface
- 📊 Real-time scoring with detailed metrics
- 🎯 Progress tracking across challenges
- 🤖 AI-powered explanations
- 📱 Works on desktop, tablet, and mobile

**Perfect for:** Interactive learning, classrooms, visual learners

---

### 3. 💻 **Command Line Interface** (Classic)
```bash
# Install and setup
pip install ai-prompt-game
ai-prompt-game --setup

# Play specific challenges
ai-prompt-game --target cat
ai-prompt-game --target coffee
ai-prompt-game --target car

# Check your progress
ai-prompt-game --stats

# Quick 5-minute game
ai-prompt-game --quick
```

**Features:**
- ⚡ Fast and lightweight
- 🎯 Direct challenge access
- 📊 Built-in statistics
- 🔧 Advanced options and flags

**Perfect for:** Developers, terminal users, automation

---

## 🎮 **Challenge Progression**

| Challenge | Difficulty | Required Score | Description |
|-----------|------------|----------------|-------------|
| 🐱 Cat    | Easy       | 65%           | Cute cat portrait |
| ☕ Coffee | Easy       | 65%           | Steaming coffee cup |
| 🚗 Car    | Medium     | 60%           | Sports car scene |
| 🦊 Foxes  | Medium     | 60%           | Fox family |
| 🦙 Llama  | Medium     | 60%           | Llama portrait |
| 🦉 Owl    | Hard       | 55%           | Wise owl |

## 🎯 **Tips for Success**

### **Writing Great Prompts:**
```
❌ Bad: "cat"
⚠️  Okay: "orange cat sitting"  
✅ Good: "fluffy orange tabby cat sitting on wooden table"
🎯 Perfect: "fluffy orange tabby cat with green eyes sitting on rustic wooden table, soft natural lighting, realistic photograph"
```

### **Key Elements to Include:**
- **Colors**: "bright orange", "deep blue", "warm golden"
- **Objects**: "tabby cat", "ceramic mug", "sports car"
- **Setting**: "wooden table", "mountain road", "cozy kitchen"
- **Lighting**: "soft natural light", "dramatic sunset", "studio lighting"
- **Style**: "realistic photograph", "oil painting", "digital art"
- **Details**: "fluffy fur", "steam rising", "chrome details"

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **"Command not found" or "Module not found"**
```bash
# Make sure you're in the right directory
cd path/to/ai-prompt-game

# Check if Python is installed
python --version

# Try with python3 if python doesn't work
python3 quick_start.py
```

#### **"Port already in use"**
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Or use different port by editing web_dashboard/app.py
# Change: app.run(port=8080) to app.run(port=8081)
```

#### **"Images not loading"**
```bash
# Run setup again
ai-prompt-game --setup

# Check if images downloaded
ls ~/.ai-prompt-game/targets/
```

#### **"Generation fails"**
- Check your internet connection (uses Pollinations.ai)
- Try simpler prompts first
- Wait a bit longer for complex images

## 📚 **More Resources**

- **📖 [Web Dashboard Guide](WEB_DASHBOARD_GUIDE.md)** - Complete web interface guide
- **🚀 [Vercel Deployment Guide](VERCEL_DEPLOYMENT_GUIDE.md)** - Deploy to cloud
- **📋 [Final Release Summary](FINAL_RELEASE_SUMMARY.md)** - Complete feature overview
- **📝 [Release Notes](RELEASE_NOTES_v2.0.md)** - What's new in v2.0

## 🎉 **Ready to Play!**

Choose your preferred method above and start mastering AI prompt engineering! 

**Remember:**
- 🎯 Start with easy challenges (Cat, Coffee)
- 📝 Be specific and detailed in your prompts
- 🤖 Learn from the AI feedback
- 🎮 Have fun and experiment!

**Happy prompting!** ✨🚀🎮