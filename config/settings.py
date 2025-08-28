"""
Configuration settings for AI Slide Generator
"""
import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CONFIG_DIR = PROJECT_ROOT / "config"

# Google Slides API configuration
GOOGLE_SLIDES_API_SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file'
]

# Default Google Slides templates
GOOGLE_SLIDES_TEMPLATES = {
    "simple": "Simple",
    "modern": "Modern Writer",
    "focus": "Focus",
    "geometric": "Geometric",
    "swiss": "Swiss",
    "paradigm": "Paradigm"
}

# HTML presentation themes
HTML_THEMES = {
    "black": "Black",
    "white": "White",
    "league": "League",
    "beige": "Beige",
    "sky": "Sky",
    "night": "Night",
    "serif": "Serif",
    "simple": "Simple",
    "solarized": "Solarized",
    "blood": "Blood",
    "moon": "Moon"
}

# Default settings
DEFAULT_SETTINGS = {
    "google_slides": {
        "template": "simple",
        "slide_size": "LARGE_16_9",
        "default_font": "Arial",
        "default_font_size": 14
    },
    "html_slides": {
        "theme": "black",
        "transition": "slide",
        "controls": True,
        "progress": True,
        "center": True,
        "touch": True,
        "loop": False,
        "rtl": False
    },
    "parsing": {
        "max_bullet_points": 7,
        "max_slide_title_length": 60,
        "max_bullet_point_length": 120
    }
}

# Environment variables
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

# Output settings
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_OUTPUT_DIR.mkdir(exist_ok=True)