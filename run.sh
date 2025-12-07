#!/bin/zsh
# Helper script to run the scraper with the correct virtual environment
# Place in your project root and run: ./run.sh [command]

set -e

VENV_PATH=".venv/bin/activate"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
    echo "❌ Error: Virtual environment not found at $VENV_PATH"
    echo ""
    echo "To create it, run:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements-py39.txt"
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH"

# Run the command or default to help
if [ $# -eq 0 ]; then
    # No arguments - show scraper help and run verification
    echo "🔍 Verifying setup..."
    python verify_setup.py
    echo ""
    echo "✅ Setup verified! Ready to scrape."
    echo ""
    echo "Usage examples:"
    echo "  ./run.sh scraper.py"
    echo "  ./run.sh cli.py --help"
    echo "  ./run.sh cli.py -o output.xlsx"
    echo "  ./run.sh verify_setup.py"
else
    # Run with provided arguments
    python "$@"
fi
