#!/usr/bin/env python3
"""
Setup script for AI Prompt Engineering Game
Makes it installable via pip
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-prompt-game",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Cross-platform AI-powered reverse prompt engineering educational game for Windows, macOS, and Linux",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-prompt-game",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "ai-prompt-game=ai_prompt_game.cli:main",
            "prompt-game=ai_prompt_game.cli:main",
            "ai-game=ai_prompt_game.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_prompt_game": [
            "targets/*.jpg",
            "targets/*.png",
            "data/*.json",
        ],
    },
    keywords="ai, education, prompt-engineering, machine-learning, game, cli",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-prompt-game/issues",
        "Source": "https://github.com/yourusername/ai-prompt-game",
        "Documentation": "https://github.com/yourusername/ai-prompt-game#readme",
    },
)