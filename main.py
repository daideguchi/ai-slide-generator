#!/usr/bin/env python3
"""
AI Slide Generator - Main Entry Point

A command-line tool for generating high-quality presentations from text files
using Google Slides API and HTML/Reveal.js.

Usage:
    python slide_generator.py google input.txt --template modern
    python slide_generator.py html input.txt --theme black
    python slide_generator.py analyze input.txt
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from slide_generator.cli import main

if __name__ == "__main__":
    main()