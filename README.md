# Reverse Prompt Engineering Game 🎯

An educational game where students are given a target image and must craft prompts until their generated image matches the original. Perfect for teaching prompt engineering skills!

## Features

- **Target Image Matching**: Students try to recreate a given image through prompts
- **Multi-metric Scoring**: Uses structural similarity, histogram comparison, and feature matching
- **Progressive Hints**: Provides helpful hints as students make more attempts
- **Session Tracking**: Saves all attempts and progress
- **Real-time Feedback**: Immediate scoring and feedback on each attempt

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have a target image ready (JPG/PNG format)

## How to Play

Run the game with a target image:

```bash
python play_game.py path/to/target_image.jpg
```

### Optional Parameters:
- `--device CPU` or `--device GPU` (default: CPU)
- `--steps 20` (number of inference steps, default: 20)
- `--guidance 7.5` (guidance scale, default: 7.5)

### Example:
```bash
python play_game.py target_images/sunset_landscape.jpg --steps 25 --guidance 8.0
```

## Game Commands

While playing:
- Enter any text prompt to generate an image
- `progress` - Show current game statistics
- `quit` - Exit and save your session
- `help` - Show available commands

## Scoring System

The game uses a combined similarity score (0.0 to 1.0):
- **Structural Similarity (40%)**: Compares image structure and patterns
- **Histogram Comparison (40%)**: Compares color distributions
- **Feature Matching (20%)**: Compares key visual features

### Score Ranges:
- 🎉 **Excellent (0.85+)**: Very close match!
- 👍 **Good (0.70-0.84)**: Getting closer
- 🤔 **Fair (0.50-0.69)**: Decent attempt
- 💡 **Keep Trying (<0.50)**: Room for improvement

## Educational Benefits

- **Prompt Engineering Skills**: Learn how different words affect image generation
- **Visual Analysis**: Develop ability to describe images precisely
- **Iterative Improvement**: Practice refining prompts based on feedback
- **Technical Understanding**: Learn about AI image generation

## File Structure

- `stable_difussion_engine.py` - Core Stable Diffusion engine
- `prompt_guessing_game.py` - Main game logic and scoring
- `play_game.py` - CLI interface for playing
- `game_session.json` - Saved game progress (auto-generated)
- `attempt_XXX_score_X.XXX.jpg` - Generated images from attempts

## Tips for Students

1. **Start Simple**: Begin with basic descriptions of the main subject
2. **Add Details Gradually**: Include style, colors, lighting, composition
3. **Use Specific Terms**: "Oil painting" vs "painting", "Golden hour" vs "sunset"
4. **Learn from Feedback**: Pay attention to which aspects improve your score
5. **Experiment**: Try different artistic styles and descriptive approaches

## For Educators

This tool is perfect for:
- AI/ML courses covering generative models
- Digital art and design classes
- Creative writing workshops
- Computer vision education
- Prompt engineering training

Students will develop both technical and creative skills while having fun with the challenge!# difussion-engine
