# 🎯 Difussion-Engine: How to Run This Codebase

## Overview
This is a comprehensive AI Prompt Engineering Game project with multiple ways to run it for different use cases:

- **Individual learners**: CLI package for personal learning
- **Developers**: Standalone Python scripts for testing and development  
- **Educators**: Student package for classroom deployment
- **Web developers**: REST API server for web frontends
- **Content creators**: Image comparison and generation tools

---

## 🚀 Method 1: CLI Package (Recommended for Individual Users)

The easiest way to use the game as an end user.

### Installation
```bash
# Install the package
pip install -e .

# Set up target images and test AI connection  
ai-prompt-game --setup

# Start playing!
ai-prompt-game
```

### Available CLI Commands
```bash
ai-prompt-game                    # Start interactive game
ai-prompt-game --setup           # Setup game files and targets  
ai-prompt-game --list-targets    # Show available challenges
ai-prompt-game --target sunset   # Play specific challenge
ai-prompt-game --quick           # Quick 5-minute game
ai-prompt-game --stats           # Show your progress
ai-prompt-game --help            # Show full help
```

### What It Does
- Downloads beautiful target images (sunsets, forests, beaches, etc.)
- Uses free Pollinations.ai API for image generation (no API key needed)
- Tracks your progress and improvement over time
- Provides educational feedback to improve your prompt engineering skills

---

## 🧪 Method 2: Standalone Python Scripts (For Developers & Testing)

Individual Python files for specific functionality and testing.

### Basic Testing (No Internet Required)
```bash
# Test core game logic with keyword matching
python basic_test.py
# Choose option 1 for automated test
```

### Natural Image Game (Requires Internet for AI)
```bash
# Interactive game with beautiful natural targets
python play_natural_game.py
# Select a difficulty level and start prompting!
```

### API Testing
```bash
# Test the free Pollinations.ai API
python test_pollinations.py

# Test image comparison algorithms  
python demo_comparison_algorithm.py
```

### Other Useful Scripts
```bash
# Create additional target images
python create_natural_targets.py

# Test specific game components
python example_usage.py
python visual_demo_comparison.py
```

---

## 🌐 Method 3: API Server (For Web Developers)

REST API server for building web frontends or integrating with other applications.

### Setup & Run
```bash
# Install API dependencies
pip install fastapi uvicorn python-multipart

# Start the server
python api_server.py
# Server runs on http://localhost:8000
```

### API Endpoints
- `GET /` - API information
- `GET /docs` - Interactive Swagger UI documentation
- `GET /health` - Health check
- `POST /game/create` - Create new game session
- `POST /game/{session_id}/attempt` - Submit prompt attempt
- `GET /game/{session_id}/status` - Get game progress
- `GET /game/sessions` - List all sessions

### Usage Example
```bash
# Test the API
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Open in browser for full API docs
```

---

## 🎓 Method 4: Student Package (For Educators)

One-click installer for classroom deployment to 500+ students.

### For Students
```bash
# Navigate to student_package directory
cd student_package

# Run one-click installer
python install.py
# Follow prompts to install game on student computer

# Play the game (after installation)
cd ~/ai_prompt_game
python play_natural_game.py
```

### What Student Package Includes
- `install.py` - One-click installer
- `requirements.txt` - Minimal dependencies
- `game_files/` - Complete game engine
- `natural_targets/` - Beautiful challenge images
- `README_STUDENTS.md` - Student instructions

### For Educators
- Distribute `AI_Prompt_Game_Student_Edition.zip` to students
- Each student runs `python install.py` once
- Students can play offline (except for AI image generation)
- Scales to unlimited students with no server costs

---

## 🔧 Dependencies & Requirements

### Core Requirements
- **Python 3.8+** (tested with 3.12)
- **opencv-python** - Image processing
- **matplotlib** - Image display and visualization
- **numpy** - Numerical computations
- **requests** - API communication
- **pillow** - Image handling

### Optional Requirements  
- **fastapi + uvicorn** - For API server
- **python-multipart** - For API file uploads
- **diffusers + transformers** - For local Hugging Face models
- **replicate** - For Replicate API integration

### Installation
```bash
# Install core dependencies
pip install opencv-python matplotlib numpy requests pillow

# For API server
pip install fastapi uvicorn python-multipart

# For advanced AI models (optional)
pip install diffusers transformers torch  # Hugging Face
pip install replicate                      # Replicate API
```

---

## 🎮 How to Play

### 1. Choose Your Challenge
- Mountain Sunset (Medium)
- Ocean Waves (Hard)  
- Forest Path (Medium)
- Tropical Beach (Easy)
- Northern Lights (Hard)

### 2. Write Effective Prompts
- Start simple: "sunset over mountains"
- Add details: "golden sunset over mountain peaks with dramatic clouds"
- Include style: "golden sunset over mountain peaks with dramatic orange clouds, landscape photography"

### 3. Learn from Feedback
- The game scores your images on 4 metrics:
  - **Structure (30%)**: Layout and composition
  - **Colors (25%)**: Color distribution and palette  
  - **Edges (25%)**: Shape and boundary detection
  - **Dominant Colors (20%)**: Key color matching

### 4. Improve Iteratively
- Use hints and feedback to refine your prompts
- Track your progress over time
- Master the art of AI communication!

---

## 🎯 Use Cases & Target Audiences

### For Students
- Learn prompt engineering fundamentals
- Understand AI image generation
- Develop visual analysis skills
- Practice iterative improvement

### For Educators  
- Scalable AI education tool
- Measurable learning outcomes
- Engaging game-based learning
- No server infrastructure needed

### For Developers
- Test AI model integrations
- Experiment with image comparison algorithms
- Build custom educational tools
- Prototype new features

### For Researchers
- Study prompt engineering effectiveness
- Analyze learning progression patterns
- Test different AI models
- Evaluate educational impact

---

## 🌟 Key Features

### ✅ **Completely Free**
- Uses Pollinations.ai free API
- No API keys required
- No server costs for scaling

### ✅ **Cross-Platform**  
- Works on Windows, macOS, Linux
- Same commands across all platforms
- Consistent experience everywhere

### ✅ **Educational**
- Progressive difficulty levels
- Detailed feedback and hints
- Learning analytics and progress tracking
- Skill development over time

### ✅ **Scalable**
- Individual installation for 1 user
- Classroom deployment for 500+ students
- Same code, same quality, zero marginal cost

### ✅ **Extensible**
- Multiple AI model integrations
- Custom target image support
- API for building web frontends
- Open source for contributions

---

## 🛠️ Troubleshooting

### Common Issues

**"No targets found"**
```bash
# Solution: Run setup to download target images
ai-prompt-game --setup
```

**"Network connection failed"**  
```bash
# The game works offline except for AI generation
# Target images and game logic work without internet
# Only AI image generation requires network connection
```

**"Dependencies missing"**
```bash
# Install missing packages
pip install opencv-python matplotlib numpy requests pillow
```

**"API server won't start"**
```bash
# Install FastAPI dependencies
pip install fastapi uvicorn python-multipart
```

### Performance Tips
- **For faster generation**: Use Pollinations.ai (default, fastest)
- **For highest quality**: Use Replicate API (requires payment)
- **For privacy**: Use local Hugging Face models (requires GPU)

---

## 📞 Support & Contribution

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/surajsahani/difussion-engine/issues)
- **Documentation**: This README and in-code comments
- **API Docs**: Run API server and visit `/docs` endpoint

### Contributing
- **Fork the repository**
- **Add new features or fix bugs**
- **Submit pull requests**
- **Share feedback and suggestions**

### Educational Impact
This tool has been designed to scale from 1 student to 1 million students with the same code quality and zero marginal cost per additional user. Perfect for:
- Individual learning
- Classroom instruction  
- Online courses
- AI literacy programs
- Research studies

---

**Made with ❤️ for AI education - Making prompt engineering fun, engaging, and accessible to everyone!**