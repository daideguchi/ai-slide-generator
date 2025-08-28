#!/bin/bash

# AI Slide Generator - Streamlit UI Startup Script

echo "🎯 Starting AI Slide Generator UI..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "   Installing required packages..."
    pip install -r requirements.txt
fi

echo "🚀 Launching Streamlit UI..."
echo "   URL: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

# Launch Streamlit
PYTHONPATH=src streamlit run streamlit_ui.py --server.port 8501 --server.address localhost