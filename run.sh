#!/bin/bash
# Celeste Map - Quick Start Script for macOS/Linux
# This script sets up and runs the application

echo "========================================"
echo "Celeste Map - Dark Web Awareness System"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Please ensure Python 3.8+ is installed"
        exit 1
    fi
    echo "Virtual environment created successfully!"
    echo ""
else
    echo "Virtual environment already exists."
    echo ""
fi

# Activate virtual environment
echo "[2/3] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Install/update dependencies
echo "[3/3] Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

# Check if config exists
if [ ! -f "config/config.yaml" ]; then
    echo "NOTE: Config file not found, using defaults."
    echo "To enable API features, copy config.example.yaml to config.yaml"
    echo ""
fi

# Start the application
echo "========================================"
echo "Starting Celeste Map..."
echo "========================================"
echo ""
echo "The application will open in your browser."
echo "Press Ctrl+C to stop the application."
echo ""

streamlit run app.py
