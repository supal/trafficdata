# Python 3.9.6 Compatibility Guide

This document outlines the adjustments made to support Python 3.9.6 and explains compatibility across Python versions.

## Version Support

The Trafikverket Data Extractor supports:
- ✅ Python 3.9.6 (minimum required version)
- ✅ Python 3.10.x
- ✅ Python 3.11.x
- ✅ Python 3.12.x
- ✅ Python 3.13.x

## What Was Changed for Python 3.9.6 Compatibility

### 1. **Dependency Versions**

All dependencies have been pinned to versions compatible with Python 3.9.6:

```
selenium>=4.0.0,<4.15.0      # Latest stable version compatible with Python 3.9
pandas>=1.3.0,<2.0.0         # pandas 1.x supports Python 3.9+
openpyxl>=3.0.0,<3.1.0       # openpyxl 3.0+ is Python 3.9 compatible
webdriver-manager>=3.8.0     # Fully compatible with Python 3.9
```

### 2. **Code Compatibility**

The code uses only Python 3.9+ compatible features:
- ✅ Type hints (available since Python 3.5)
- ✅ f-strings (available since Python 3.6)
- ✅ Context managers (available since Python 3.1)
- ✅ pathlib for file operations (available since Python 3.4)

No Python 3.10+ only features are used (e.g., match/case statements, union types with |).

### 3. **New Files Added**

- **`compatibility.py`** - Validates Python version and dependencies at runtime
- **`setup.py`** - Standard Python setup script for installation
- **`requirements-py39.txt`** - Python 3.9.6 specific dependency versions
- **`.python-version`** - Specifies minimum Python version (for version managers)
- **`setup.sh`** - Automated setup script for Unix-like systems

## Installation for Python 3.9.6

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3.9 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip to latest
pip install --upgrade pip

# Install dependencies
pip install -r requirements-py39.txt
```

### Using setup.sh (Unix/macOS)

```bash
chmod +x setup.sh
./setup.sh
```

## Verifying Installation

Check your setup with:

```bash
python3 compatibility.py
```

Or run directly:

```bash
python3 scraper.py
```

## Testing Compatibility

To test with a specific Python version:

```bash
# Create venv with specific Python version
python3.9 -m venv venv39
source venv39/bin/activate
pip install -r requirements-py39.txt
python scraper.py
```

## Common Issues

### Issue: "Python 3.9 or higher is required"
**Solution:** Update your Python version or create a virtual environment with Python 3.9+

```bash
python3 --version  # Check current version
python3.9 -m venv .venv  # Or specify your version
```

### Issue: "No module named 'openpyxl'"
**Solution:** Install dependencies

```bash
pip install -r requirements-py39.txt
```

### Issue: Selenium version conflicts
**Solution:** Use the pinned versions in requirements-py39.txt

```bash
pip install --force-reinstall -r requirements-py39.txt
```

## Version-Specific Notes

### Python 3.9
- Requires explicit type hint imports for some types
- No match/case statements
- Dict union syntax (`|`) not available
- Use `Union` from `typing` module

### Python 3.10+
- All Python 3.9 code is compatible
- Additional modern features available but not required

## Future Compatibility

The code is designed to remain compatible through Python 3.15+ with no changes required, as long as the current Selenium/pandas APIs don't break.

To maintain forward compatibility, avoid:
- Using syntax introduced in Python 3.10+ exclusively
- Relying on deprecated features
- Hard-coding version requirements

## Additional Resources

- [Python 3.9 Documentation](https://docs.python.org/3.9/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)

