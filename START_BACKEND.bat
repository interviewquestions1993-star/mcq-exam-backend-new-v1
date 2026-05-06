@echo off
REM Quick Start Script for Hugging Face Backend on Windows

echo.
echo ============================================================
echo   HUGGING FACE INFERENCE BACKEND - QUICK START
echo ============================================================
echo.

REM Check if in correct directory
if not exist "main_local.py" (
    echo ERROR: main_local.py not found!
    echo Please run this script from: d:\AI-Exam-Preparer
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo Step 1: Checking Python version...
python --version
echo.

echo Step 2: Checking dependencies...
python -c "import fastapi; import transformers; import torch" 2>nul
if errorlevel 1 (
    echo WARNING: Some dependencies may be missing
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo ✓ Dependencies OK
echo.

echo ============================================================
echo   STARTING BACKEND...
echo ============================================================
echo.
echo The API will be available at:
echo   http://localhost:8000
echo.
echo Documentation:
echo   http://localhost:8000/docs
echo.
echo First request will load the model (1-2 minutes)...
echo.
echo Press CTRL+C to stop the server
echo.
echo ============================================================
echo.

REM Start the backend
python main_local.py

pause
