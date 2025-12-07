# Troubleshooting Guide

## ❌ Error: ModuleNotFoundError: No module named 'pandas'

### Cause
You're running Python directly without activating the virtual environment.

### Solution

#### Option 1: Use Helper Script (Recommended)
**macOS/Linux:**
```bash
./run.sh scraper.py
```

**Windows:**
```cmd
run.cmd scraper.py
```

#### Option 2: Activate Virtual Environment Manually
**macOS/Linux:**
```bash
source .venv/bin/activate
python scraper.py
```

**Windows:**
```cmd
.venv\Scripts\activate
python scraper.py
```

#### Option 3: Use Full Path to Python
```bash
./.venv/bin/python scraper.py     # macOS/Linux
.\.venv\Scripts\python scraper.py # Windows
```

---

## ❌ Error: "python3: command not found" or "python not found"

### Cause
Python is not installed or not in your PATH.

### Solution

**macOS (with Homebrew):**
```bash
brew install python@3.9
python3.9 --version  # Verify
```

**macOS (with pyenv):**
```bash
brew install pyenv
pyenv install 3.9.6
pyenv global 3.9.6
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv
```

**Windows:**
- Download from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installation

---

## ❌ Error: "Permission denied" on run.sh or setup.sh

### Cause
Shell scripts don't have execute permission.

### Solution
```bash
chmod +x run.sh setup.sh
./run.sh scraper.py  # Now it works
```

---

## ❌ Error: "No such file or directory: .venv"

### Cause
Virtual environment was never created.

### Solution
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-py39.txt

# Verify
python verify_setup.py
```

---

## ❌ Error: "ModuleNotFoundError: No module named 'openpyxl'"

### Cause
Dependencies not installed in virtual environment.

### Solution
```bash
# Make sure venv is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --force-reinstall -r requirements-py39.txt

# Verify
python verify_setup.py
```

---

## ❌ Error: "could not find chromedriver"

### Cause
Chrome browser not installed or WebDriver can't find it.

### Solution

**Check if Chrome is installed:**
```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Linux
google-chrome --version

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

**If not installed:**

**macOS:**
```bash
brew install google-chrome
```

**Ubuntu:**
```bash
sudo apt install google-chrome-stable
```

**Windows:**
- Download from https://www.google.com/chrome/
- Install normally

**Then reinstall webdriver-manager:**
```bash
pip install --force-reinstall webdriver-manager
python scraper.py
```

---

## ❌ Error: "Could not reach host. Are you offline?"

### Cause
- No internet connection
- Trafikverket website is down
- Network/firewall blocking access

### Solution
1. Check internet connection: `ping google.com`
2. Try accessing website manually: https://vtf.trafikverket.se/
3. Check if using a proxy/VPN that might block the site
4. Try again in a few minutes (site might be down temporarily)

---

## ❌ Error: "Timeout waiting for table"

### Cause
Website is slow or structure has changed.

### Solution
```bash
# Try with longer timeout (default is 10 seconds)
./run.sh cli.py -t 30 scraper.py  # 30 second timeout
```

Or edit `config.py` and increase timeout values.

---

## ❌ Error: "verify_setup.py: No such file"

### Cause
You're in the wrong directory.

### Solution
```bash
# Navigate to project directory
cd /Users/arif.ahsan/Documents/Code/RnD/dalarna/thesis

# Then run
./run.sh verify_setup.py
```

---

## ❌ Error: "ImportError: cannot import name 'Select' from selenium"

### Cause
Selenium version mismatch.

### Solution
```bash
# Reinstall with correct version
pip install --force-reinstall -r requirements-py39.txt
```

---

## ❌ Error: setup.sh or run.sh not working on Windows

### Cause
Windows uses `.cmd` files, not `.sh` files.

### Solution
Use `run.cmd` instead:
```cmd
run.cmd scraper.py
run.cmd cli.py --help
run.cmd verify_setup.py
```

---

## ✅ Verification Steps

### Step 1: Check Python Version
```bash
python --version  # Should be 3.9.6 or higher
# If not, activate venv first:
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
python --version
```

### Step 2: Check Virtual Environment
```bash
which python  # macOS/Linux - should show .venv path
where python  # Windows - should show .venv path
```

### Step 3: Verify Dependencies
```bash
python -c "import selenium; import pandas; import openpyxl; print('✅ All imports work')"
```

### Step 4: Run Full Verification
```bash
./run.sh verify_setup.py  # macOS/Linux
run.cmd verify_setup.py   # Windows
```

---

## 🆘 Still Having Issues?

### Check Documentation Files
- `README.md` - Full usage guide
- `SETUP_COMPLETE.md` - Detailed setup
- `PYTHON39_COMPATIBILITY.md` - Compatibility info
- `FINAL_SUMMARY.txt` - Summary of setup

### Try Step-by-Step Setup
```bash
# Complete fresh start
rm -rf .venv              # macOS/Linux: remove old venv
rmdir /s .venv            # Windows: remove old venv

python3 -m venv .venv     # Create fresh venv
source .venv/bin/activate # Activate (macOS/Linux)
.venv\Scripts\activate    # Activate (Windows)

pip install --upgrade pip
pip install -r requirements-py39.txt
python verify_setup.py    # Verify
./run.sh scraper.py       # Run (macOS/Linux)
run.cmd scraper.py        # Run (Windows)
```

### Get System Information
```bash
./run.sh verify_setup.py  # Shows Python, OS, and all installed packages
```

---

## 📞 Quick Reference

| Error | Quick Fix |
|-------|-----------|
| ModuleNotFoundError | Use `./run.sh` or activate venv |
| Permission denied | `chmod +x run.sh` |
| Venv not found | `python3 -m venv .venv` |
| Python not found | Install Python 3.9.6+ |
| Wrong directory | `cd /path/to/thesis` |
| Timeout | Use `-t 30` for longer timeout |
| Chrome not found | Install Google Chrome |
| No internet | Check connection & firewall |

---

## 💡 Pro Tips

1. **Always use `./run.sh` or `run.cmd`** - avoids venv issues
2. **When in doubt, run `verify_setup.py`** - shows what's wrong
3. **Check you're in the correct directory** - use `pwd` (macOS/Linux) or `cd` (Windows)
4. **Never modify system Python** - always use virtual environment
5. **Reinstall if issues persist** - fresh start usually fixes things

---

**Still stuck? Read the error message carefully - it usually tells you exactly what's wrong!**
