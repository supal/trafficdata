# ✅ Virtual Environment Issue - FIXED

## The Problem

When you ran `python3 cli.py --help`, you got:
```
ModuleNotFoundError: No module named 'pandas'
```

This happens because you were using the **system Python** instead of the **virtual environment Python**.

---

## The Solution

### ✅ Use the Helper Script (Easiest!)

**macOS/Linux:**
```bash
./run.sh cli.py --help
./run.sh scraper.py
./run.sh verify_setup.py
```

**Windows:**
```cmd
run.cmd cli.py --help
run.cmd scraper.py
run.cmd verify_setup.py
```

The helper script **automatically activates the virtual environment** before running!

---

### Alternative: Activate Manually

If you prefer to activate the virtual environment manually:

**macOS/Linux:**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then run commands normally
python cli.py --help
python scraper.py
python verify_setup.py
```

**Windows:**
```cmd
REM Activate virtual environment first
.venv\Scripts\activate

REM Then run commands normally
python cli.py --help
python scraper.py
python verify_setup.py
```

---

## What Was Added to Fix This

### 1. Helper Scripts (Automatic Venv Activation)
- **`run.sh`** - For macOS/Linux
- **`run.cmd`** - For Windows

These scripts automatically:
- Check if virtual environment exists
- Activate the virtual environment
- Run your command
- Exit with proper error codes

### 2. Updated Documentation
- **`QUICK_REFERENCE.md`** - Updated with helper script usage
- **`TROUBLESHOOTING.md`** - NEW! Complete troubleshooting guide

---

## How to Use

### Quick Start (3 commands)

**macOS/Linux:**
```bash
chmod +x run.sh      # Make script executable (one time)
./run.sh scraper.py  # Run anytime, no venv activation needed!
```

**Windows:**
```cmd
run.cmd scraper.py   # Run anytime, no venv activation needed!
```

### Example Usage

```bash
# Show help
./run.sh cli.py --help

# Run scraper with default settings
./run.sh scraper.py

# Save to custom file
./run.sh cli.py -o mydata.xlsx

# Run in background (headless)
./run.sh cli.py --headless

# Verify setup
./run.sh verify_setup.py
```

---

## Why This Happens

When you run `python3 cli.py`, your shell runs:
- ❌ System Python (doesn't have pandas, selenium, etc.)
- ✅ Should use: Virtual Environment Python (has all packages)

The helper script ensures you use the correct Python.

---

## Files Added/Modified

### Added
- ✅ `run.sh` - Helper script for macOS/Linux
- ✅ `run.cmd` - Helper script for Windows
- ✅ `TROUBLESHOOTING.md` - Comprehensive troubleshooting guide

### Modified
- 📝 `QUICK_REFERENCE.md` - Updated with helper script usage

---

## Now It Works! ✅

Test it immediately:

```bash
./run.sh cli.py --help  # Should work now!
./run.sh scraper.py     # Ready to scrape!
```

---

## Summary

| Before (Failed) | After (Works) |
|---|---|
| `python3 cli.py --help` ❌ | `./run.sh cli.py --help` ✅ |
| `python3 scraper.py` ❌ | `./run.sh scraper.py` ✅ |
| Manual venv activation needed | Automatic venv activation |

No more `ModuleNotFoundError`! 🎉
