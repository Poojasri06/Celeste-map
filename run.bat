@echo off
REM Celeste Map - Quick Start Script for Windows
REM This script sets up and runs the application

echo ========================================
echo Celeste Map - Dark Web Awareness System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

REM Activate virtual environment
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Install/update dependencies
echo [3/3] Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Check if config exists
if not exist "config\config.yaml" (
    echo NOTE: Config file not found, using defaults.
    echo To enable API features, copy config.example.yaml to config.yaml
    echo.
)

REM Start the application
echo ========================================
echo Starting Celeste Map...
echo ========================================
echo.
echo The application will open in your browser.
echo Press Ctrl+C to stop the application.
echo.

streamlit run app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo An error occurred
    echo ========================================
    pause
)
