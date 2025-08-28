@echo off
echo 🎯 Starting AI Slide Generator UI...
echo ==================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo    Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit not installed!
    echo    Installing required packages...
    pip install -r requirements.txt
)

echo 🚀 Launching Streamlit UI...
echo    URL: http://localhost:8501
echo    Press Ctrl+C to stop
echo.

REM Launch Streamlit
set PYTHONPATH=src
streamlit run streamlit_ui.py --server.port 8501 --server.address localhost