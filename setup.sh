#!/bin/bash
# Quick Start Script for Python 3.9.6
# This script sets up and runs the Trafikverket scraper

set -e  # Exit on error

echo "=================================================="
echo "Trafikverket Data Extractor - Python 3.9 Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python: $PYTHON_VERSION"

# Parse version
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "ERROR: Python 3.9 or higher is required!"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version OK: $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Installing dependencies..."
if [ -f "requirements-py39.txt" ]; then
    pip install -r requirements-py39.txt
else
    pip install -r requirements.txt
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "To run the scraper, use:"
echo "  python scraper.py"
echo ""
echo "Or use the CLI with custom options:"
echo "  python cli.py -h"
echo ""
echo "To deactivate the virtual environment later, run:"
echo "  deactivate"
echo ""
