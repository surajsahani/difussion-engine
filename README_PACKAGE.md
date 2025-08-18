# 🎯 AI Prompt Engineering Game

[![PyPI version](https://badge.fury.io/py/ai-prompt-game.svg)](https://badge.fury.io/py/ai-prompt-game)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Learn AI prompt engineering through reverse engineering!** 🎮

An educational CLI game where students see a target image and must craft prompts to recreate it using AI image generation. Perfect for learning prompt engineering, visual analysis, and AI communication skills.

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
🎯 Target: Mountain Sunset
[Shows beautiful sunset image]

[Attempt #1] Your prompt: landscape
📊 Score: 23.4% - "Too generic! Describe the colors and lighting."

[Attempt #2] Your prompt: sunset over mountains  
📊 Score: 67.8% - "Better! Add more details about the dramatic sky."

[Attempt #3] Your prompt: golden sunset over mountain peaks with dramatic clouds
📊 Score: 89.1% - "Excellent! Almost perfect!"

🎉 You're learning prompt engineering!
```

## ✨ Features

- **🎯 Multiple Challenges**: Mountain sunsets, ocean waves, forests, beaches, aurora
- **🤖 Real AI Generation**: Uses Pollinations.ai (free) or your own models
- **📊 Smart Scoring**: 4-metric similarity analysis (structure, colors, edges, composition)
- **🎓 Educational Feedback**: Learn what makes prompts effective
- **📈 Progress Tracking**: See your improvement over time
- **🌍 Works Offline**: After setup, only AI generation needs internet

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

## 🎯 Game Commands

```bash
ai-prompt-game                    # Start interactive game
ai-prompt-game --setup           # Setup game files and targets
ai-prompt-game --list-targets    # Show available challenges
ai-prompt-game --target sunset   # Play specific challenge
ai-prompt-game --quick           # Quick 5-minute game
ai-prompt-game --stats           # Show your progress
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

The game uses a sophisticated 4-metric scoring system:

- **Structure (30%)**: Layout and composition matching
- **Colors (25%)**: Color distribution and palette
- **Edges (25%)**: Shape and boundary detection  
- **Dominant Colors (20%)**: Key color matching

**Combined Score**: Weighted average of all metrics (0-100%)

## 🎯 Challenge Targets

- **🌅 Mountain Sunset** (Medium) - Golden hour over peaks
- **🌊 Ocean Waves** (Hard) - Powerful waves on rocky shore
- **🌲 Misty Forest** (Medium) - Peaceful forest path with mist
- **🏖️ Tropical Beach** (Easy) - Crystal clear water and white sand
- **🌌 Northern Lights** (Hard) - Aurora borealis over snow

## 📈 Example Learning Progression

```
Session 1: "landscape" → 15.6% → "Be more specific!"
Session 2: "sunset mountains" → 42.3% → "Add color details!"  
Session 3: "golden sunset over mountain peaks" → 68.7% → "Great progress!"
Session 4: "golden sunset over mountain peaks with dramatic clouds" → 89.1% → "Almost perfect!"
Session 5: "golden sunset over mountain peaks with dramatic orange clouds and lake reflection" → 96.7% → "MASTERY!"

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