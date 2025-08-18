"""
AI Prompt Engineering Game
Educational game for learning AI prompt engineering through reverse engineering
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "AI-powered reverse prompt engineering educational game"

from .game_engine import PromptGame
from .image_generator import ImageGenerator
from .comparison import ImageComparison

__all__ = ["PromptGame", "ImageGenerator", "ImageComparison"]