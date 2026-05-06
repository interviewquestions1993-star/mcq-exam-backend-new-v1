@echo off
REM Quick Start Script for Online Hugging Face Backend

echo.
echo ============================================================
echo   HUGGING FACE ONLINE BACKEND - QUICK START
echo ============================================================
echo.

REM Check if in correct directory
if not exist "main_online.py" (
    echo ERROR: main_online.py not found!
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
python -c "import fastapi; import huggingface_hub" 2>nul
if errorlevel 1 (
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
echo   STARTING ONLINE BACKEND...
echo ============================================================
echo.
echo API Type: ONLINE (Requires internet)
echo Models: Hugging Face Serverless Inference
echo.
echo The API will be available at:
echo   http://localhost:8000
echo.
echo Documentation:
echo   http://localhost:8000/docs
echo.
echo All responses will use Hugging Face servers.
echo First request may take 5-10 seconds.
echo.
echo Free tier: ~1000 requests/day
echo Rate limits info: http://localhost:8000/limits
echo.
echo Press CTRL+C to stop the server
echo.
echo ============================================================
echo.

REM Start the backend
python main_online.py

pause
