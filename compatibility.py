"""
Python 3.9 Compatibility Module
Ensures code works across Python 3.9.6+
"""

import sys
from typing import Any

# Verify Python version
PYTHON_VERSION = sys.version_info
if PYTHON_VERSION.major < 3 or (PYTHON_VERSION.major == 3 and PYTHON_VERSION.minor < 9):
    raise RuntimeError(
        "Python 3.9 or higher is required. "
        "You are running Python {}.{}".format(PYTHON_VERSION.major, PYTHON_VERSION.minor)
    )

# Python 3.9+ compatibility
try:
    from typing import Literal  # Available in 3.8+
except ImportError:
    from typing_extensions import Literal  # Fallback for older versions

# Ensure all required modules are available
def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    required_packages = [
        'selenium',
        'pandas',
        'webdriver_manager'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Error: Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall them using:")
        print("  pip install -r requirements.txt")
        return False
    
    return True

def print_system_info() -> None:
    """Print system and Python information."""
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
