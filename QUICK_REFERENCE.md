# Quick Reference - Trafikverket Data Extractor

## ⚡ Super Quick Start (One Command)

### macOS/Linux (Recommended)
```bash
./run.sh scraper.py
```

### Windows (Recommended)
```cmd
run.cmd scraper.py
```

**This automatically activates the virtual environment and runs the scraper!**

---

## ⚠️ IMPORTANT: Virtual Environment Activation

**If you get `ModuleNotFoundError: No module named 'pandas'`**, you forgot to activate the virtual environment!

### Activate Virtual Environment First:

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
.venv\Scripts\activate
```

**Or use the helper script (automatically activates for you):**
```bash
./run.sh scraper.py          # macOS/Linux
run.cmd scraper.py           # Windows
```

---

## 2-Minute Setup

### Prerequisites
- Python 3.9.6 or higher
- Chrome/Chromium browser
- Internet connection

### Installation Steps

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements-py39.txt

# 4. Verify setup
python verify_setup.py
```

---

## Usage Examples

### Using Helper Script (No venv activation needed!)

**macOS/Linux:**
```bash
./run.sh scraper.py          # Run scraper
./run.sh cli.py --help       # Show CLI help
./run.sh verify_setup.py     # Verify installation
```

**Windows:**
```cmd
run.cmd scraper.py           # Run scraper
run.cmd cli.py --help        # Show CLI help
run.cmd verify_setup.py      # Verify installation
```

### Manual Approach (Must activate venv first!)

```bash
# Activate virtual environment
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows

# Then run commands
python scraper.py
python cli.py --help
python cli.py -o myfile.xlsx
python cli.py --headless
python verify_setup.py
```

---

## CLI Options

```bash
./run.sh cli.py --help                      # Show all options
./run.sh cli.py -o myfile.xlsx              # Save as myfile.xlsx
./run.sh cli.py --headless                  # Run in background
./run.sh cli.py -u "https://..." -o out.xlsx # Use custom URL
```

---

## Verify Installation

```bash
./run.sh verify_setup.py     # macOS/Linux
run.cmd verify_setup.py      # Windows
```

All checks should show ✅ PASSED

---

## Output

The scraper generates an Excel file in your current directory:
- Default: `trafikverket_data_<timestamp>.xlsx`
- Custom: `myfile.xlsx` (if you specified `-o myfile.xlsx`)

---

## Helper Scripts

### run.sh (macOS/Linux)
```bash
./run.sh                     # Show help and verify setup
./run.sh scraper.py          # Run scraper (auto-activates)
./run.sh cli.py --help       # CLI help (auto-activates)
./run.sh verify_setup.py     # Verify (auto-activates)
```

### run.cmd (Windows)
```cmd
run.cmd                      # Show help and verify setup
run.cmd scraper.py           # Run scraper (auto-activates)
run.cmd cli.py --help        # CLI help (auto-activates)
run.cmd verify_setup.py      # Verify (auto-activates)
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
**Problem:** Forgot to activate virtual environment  
**Solution:** Use `./run.sh` or manually activate:
```bash
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
```

### "Permission denied" on run.sh
**Solution:**
```bash
chmod +x run.sh setup.sh
```

### "Python not found"
**Solution:** Install Python 3.9.6+
```bash
# macOS with Homebrew
brew install python@3.9
```

### Setup verification fails
**Solution:** Run setup again
```bash
./run.sh setup.sh            # macOS/Linux
python setup.py              # Windows
```

---

## 💡 Pro Tips

✅ **Always use `./run.sh` or `run.cmd`** - handles venv automatically  
✅ **Never run `python3 scraper.py` directly** - use helper script  
✅ **Remember to activate venv** if running manually  
✅ **Check current directory** for output Excel file  

---

## Quick Reference

| Task | Command |
|------|---------|
| Setup verification | `./run.sh verify_setup.py` |
| Run scraper | `./run.sh scraper.py` |
| Custom output | `./run.sh cli.py -o file.xlsx` |
| Show help | `./run.sh cli.py --help` |
| Background mode | `./run.sh cli.py --headless` |
| Make scripts executable | `chmod +x *.sh` |
| Activate manually | `source .venv/bin/activate` |

# See all CLI options
python cli.py --help

# Create Excel from custom URL
python cli.py -u "YOUR_URL" -o output.xlsx
```

---

## ✅ Requirements Met

| Requirement | Status |
|------------|--------|
| Python 3.9.6+ | ✅ |
| Selenium 4+ | ✅ |
| Pandas | ✅ |
| openpyxl | ✅ |
| WebDriver Manager | ✅ |

---

## 📁 File Locations

```
/Users/arif.ahsan/Documents/Code/RnD/dalarna/thesis/
├── scraper.py                    # Main script
├── requirements-py39.txt         # Python 3.9 dependencies
├── .venv/                        # Virtual environment
└── trafikverket_data_*.xlsx      # Generated output files
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.9.6: `brew install python@3.9` |
| "Module not found" | Install dependencies: `pip install -r requirements-py39.txt` |
| "Permission denied" on setup.sh | `chmod +x setup.sh` then `./setup.sh` |
| "WebDriver not found" | Run: `pip install --upgrade webdriver-manager` |
| Python version too old | Create new venv: `python3.9 -m venv .venv` |

---

## 📊 Version Compatibility

✅ Supports: Python 3.9.6, 3.10.x, 3.11.x, 3.12.x, 3.13.x+  
❌ Not supported: Python < 3.9

---

## 📖 Documentation Files

- **README.md** - Full usage guide
- **SETUP_COMPLETE.md** - Complete setup instructions
- **PYTHON39_COMPATIBILITY.md** - Detailed compatibility info
- **ADJUSTMENT_SUMMARY.md** - What was changed
- **config.py** - Configuration options

---

## 💡 Tips

1. Always use virtual environment for clean isolation
2. Use `verify_setup.py` to debug issues
3. Check `compatibility.py` output for system info
4. Excel files are saved with timestamp by default
5. Run in headless mode for automated/server use

---

## 🎯 Success Indicators

✅ You see "ALL CHECKS PASSED!" from `verify_setup.py`  
✅ Excel file is generated after running `python scraper.py`  
✅ No import errors when running scripts  
✅ Browser opens and navigates to Trafikverket (if not headless)  

---

**Ready to go!** Run `python scraper.py` to start extracting data.
