#!/usr/bin/env python3
"""
Vercel-compatible entry point for AI Prompt Game Dashboard
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the simplified Vercel app
from web_dashboard.vercel_app import app

# Vercel expects the app to be available as 'app'
# This will be the WSGI application
if __name__ == "__main__":
    app.run()