# 🎯 AI Prompt Engineering Game

[![PyPI version](https://badge.fury.io/py/ai-prompt-game.svg)](https://badge.fury.io/py/ai-prompt-game)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cross-Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/yourusername/ai-prompt-game)

**Learn AI prompt engineering through reverse engineering!** 🎮

An educational CLI game where students see a target image and must craft prompts to recreate it using AI image generation. Perfect for learning prompt engineering, visual analysis, and AI communication skills.

**✅ Cross-Platform Compatible**: Works seamlessly on Windows, macOS, and Linux (Ubuntu/Debian)

## 🚀 Quick Start

### Install
```bash
pip install ai-prompt-game
```

### Play
```bash
ai-prompt-game
```

That's it! The game will guide you through setup and start your first challenge.

## 🎮 How It Works

1. **See a target image** (beautiful sunset, ocean waves, etc.)
2. **Write a prompt** describing what you see
3. **AI generates an image** based on your prompt
4. **Get scored** on how well it matches the target
5. **Improve and try again** until you master it!

### Example Game Flow
```
🎯 Target: Fox
[Shows cute fox image]

[Attempt #1] Your prompt: animal
📊 Score: 23.4% - "Too generic! Describe the specific animal and setting."

[Attempt #2] Your prompt: orange fox in forest  
📊 Score: 67.8% - "Better! Add more details about the fox's features."

[Attempt #3] Your prompt: cute orange fox with white fur sitting in natural forest setting
📊 Score: 89.1% - "Excellent! Almost perfect!"

🎉 You're learning prompt engineering!
```

## ✨ Features

- **🎯 Multiple Challenges**: Mountain sunsets, ocean waves, forests, beaches, aurora
- **🤖 Real AI Generation**: Uses Pollinations.ai (free) or your own models
- **📊 Smart Scoring**: 4-metric similarity analysis (structure, colors, edges, composition)
- **🎓 Educational Feedback**: Learn what makes prompts effective
- **📈 Progress Tracking**: See your improvement over time
- **🖼️ Visual Display**: See target and generated images side-by-side
- **🌍 Works Offline**: After setup, only AI generation needs internet
- **🖥️ Cross-Platform**: Native support for Windows, macOS, and Linux

## 🛠️ Installation Options

### Option 1: Simple Install (Recommended)
```bash
pip install ai-prompt-game
ai-prompt-game --setup  # Download challenge images
ai-prompt-game          # Start playing!
```

### Option 2: Development Install
```bash
git clone https://github.com/yourusername/ai-prompt-game.git
cd ai-prompt-game
pip install -e .
ai-prompt-game --setup
```

### Option 3: With Advanced AI Models
```bash
# For local Hugging Face models
pip install ai-prompt-game[huggingface]

# For Replicate API
pip install ai-prompt-game[replicate]
```

## 🖥️ Platform-Specific Setup

### Windows
```cmd
# Install via pip (works in Command Prompt or PowerShell)
pip install ai-prompt-game
ai-prompt-game

# If you encounter OpenCV issues:
pip install opencv-python-headless
```

### Ubuntu/Linux
```bash
# Standard installation
pip install ai-prompt-game

# If you need system OpenCV dependencies:
sudo apt-get update
sudo apt-get install python3-opencv libopencv-dev

# Then install the game
pip install ai-prompt-game
ai-prompt-game
```

### macOS
```bash
# Standard installation works out of the box
pip install ai-prompt-game
ai-prompt-game
```

**Note**: All platforms use the same commands once installed. The game automatically detects your operating system and adapts accordingly.

## 🖼️ Visual Features

The game includes **visual display mode** that shows images side-by-side:

- **Target Image**: The image you're trying to recreate
- **Generated Image**: Your AI-generated result  
- **Real-time Comparison**: See both images with similarity scores
- **Automatic Saving**: All images saved to `~/.ai-prompt-game/generated/`

### Visual Mode Commands
```bash
ai-prompt-game              # Full visual mode (default)
ai-prompt-game --no-visual  # Text-only mode
```

**Visual mode requires**: `matplotlib` (automatically installed with the package)

## 🎯 Game Commands

```bash
ai-prompt-game                    # Start interactive game with visual display
ai-prompt-game --setup           # Setup game files and targets
ai-prompt-game --list-targets    # Show available challenges
ai-prompt-game --target sunset   # Play specific challenge
ai-prompt-game --quick           # Quick 5-minute game
ai-prompt-game --stats           # Show your progress
ai-prompt-game --no-visual       # Text-only mode (no image display)
```

### In-Game Commands
- `progress` - Show current game progress
- `target` - Show target image info again  
- `help` - Show help and tips
- `quit` - Exit game

## 🎓 Educational Value

Perfect for learning:
- **Prompt Engineering**: How to communicate effectively with AI
- **Visual Analysis**: Breaking down images into describable components
- **Iterative Improvement**: Learning from feedback and refining
- **AI Understanding**: How image generation actually works

### For Educators
- **Measurable Learning**: Quantified skill improvement
- **Engaging Format**: Students love the game approach
- **Scalable**: Works for 1 or 1000 students
- **Progress Tracking**: Built-in analytics and statistics

## 🤖 AI Models Supported

| Model | Cost | Quality | Setup |
|-------|------|---------|-------|
| **Pollinations.ai** | Free | High | None (default) |
| **Hugging Face** | Free | Very High | Local GPU recommended |
| **Replicate** | Pay-per-use | Highest | API key required |

### Using Different Models
```bash
# Use Pollinations.ai (default, free)
ai-prompt-game --model pollinations

# Use local Hugging Face model
ai-prompt-game --model huggingface

# Use Replicate API
ai-prompt-game --model replicate
```

## 📊 Scoring System

The game uses an advanced multi-metric scoring system:

### **🤖 LLaVA AI-Enhanced Scoring (Optional)**
- **LLaVA Semantic (25%)**: AI-powered semantic understanding of image similarity
- **Structure (20%)**: Layout and composition matching
- **Colors (20%)**: Color distribution and palette
- **Edges (20%)**: Shape and boundary detection  
- **Dominant Colors (15%)**: Key color matching

### **🔧 Traditional Scoring (Fallback)**
- **Structure (30%)**: Layout and composition matching
- **Colors (25%)**: Color distribution and palette
- **Edges (25%)**: Shape and boundary detection  
- **Dominant Colors (20%)**: Key color matching

**Combined Score**: Weighted average of all metrics (0-100%)

### **🚀 Enable LLaVA Enhancement**
```bash
# Install LLaVA dependencies (large download ~13GB)
pip install transformers torch torchvision

# Use LLaVA-enhanced scoring (default)
ai-prompt-game

# Disable LLaVA (traditional metrics only)
ai-prompt-game --no-llava
```

**LLaVA Benefits:**
- 🧠 Semantic understanding (not just pixel comparison)
- 🎯 Better scoring for artistic and stylistic matches
- 💬 AI explanations of what matches/differs
- 🎨 Understands context, mood, and composition

## 🎯 Challenge Targets

- **🦊 Fox** (Medium) - A cute fox in a natural setting
- **🚗 Car** (Hard) - A bear driving a colorful toy car
- **🦙 Llama** (Medium) - A fluffy llama in a winter landscape
- **🚐 Van** (Easy) - A colorful van climbing a mountain road beside the ocean
- **🦉 Owl** (Hard) - A wise-looking owl with detailed feathers

## 📈 Example Learning Progression

```
Session 1: "animal" → 15.6% → "Be more specific!"
Session 2: "fox forest" → 42.3% → "Add color details!"  
Session 3: "orange fox in natural setting" → 68.7% → "Great progress!"
Session 4: "cute orange fox with white fur in forest" → 89.1% → "Almost perfect!"
Session 5: "adorable orange and white fox sitting peacefully in natural forest environment" → 96.7% → "MASTERY!"

🎓 Result: Student learned effective prompt engineering!
```

## 🔧 Advanced Usage

### Custom Targets
```python
from ai_prompt_game import PromptGame

game = PromptGame()
game.add_custom_target("my_image.jpg", "My Custom Challenge")
```

### API Integration
```python
from ai_prompt_game import ImageGenerator, ImageComparison

generator = ImageGenerator("pollinations")
comparator = ImageComparison()

# Generate image
image = generator.generate("sunset over mountains")

# Compare with target
scores = comparator.compare(image, target_image)
print(f"Similarity: {scores['combined']:.3f}")
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/yourusername/ai-prompt-game.git
cd ai-prompt-game
pip install -e .[dev]
pytest  # Run tests
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pollinations.ai** for free, high-quality image generation
- **Unsplash** for beautiful target images
- **OpenCV** for image processing capabilities
- **Education community** for inspiration and feedback

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-prompt-game/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-prompt-game/discussions)
- **Email**: your.email@example.com

---

**Made with ❤️ for AI education**

*"Making AI education engaging, measurable, and fun - one prompt at a time!"*