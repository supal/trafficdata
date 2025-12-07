# Windows Installation Guide

## Quick Start (Recommended)

### Option 1: Automated Setup (Easiest)

1. **Download the project** - Extract the ZIP file to your desired location

2. **Run the Setup Wizard:**
   - Double-click `SETUP-WIZARD.bat`
   - Follow the on-screen prompts
   - The wizard will check prerequisites and install everything

3. **Start using the scraper:**
   - Edit `input_url.txt` with URLs to process
   - Double-click `RUN.bat` to execute

**That's it!** ✅

### Option 2: Manual Setup

If the automated installer doesn't work:

1. **Install Python 3.9.6+**
   - Download from: https://www.python.org/downloads/
   - **Important:** Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and run `python --version`

2. **Install Google Chrome**
   - Download from: https://www.google.com/chrome/

3. **Create virtual environment:**
   ```batch
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

4. **Install dependencies:**
   ```batch
   pip install -r requirements.txt
   ```
   
   Or for Python 3.9:
   ```batch
   pip install -r requirements-py39.txt
   ```

5. **Run the scraper:**
   ```batch
   python scraper.py --headless
   ```

## Running the Scraper

### Method 1: Double-Click (Easiest)
Simply double-click `RUN.bat` to run with default settings (headless mode)

### Method 2: Command Prompt

**Open Command Prompt** in the project folder:
- Hold Shift + Right-click in folder
- Select "Open PowerShell window here" or "Open Command Prompt here"

**Then run:**
```batch
run.cmd scraper.py --headless
```

### Method 3: Add URLs and Run

1. Open `input_url.txt` with a text editor (Notepad, VS Code, etc.)
2. Add one URL per line:
   ```
   https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520522,13520522&laenkrollista=2,3
   https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520474,13520475&laenkrollista=1,1
   ```

3. Save the file

4. Double-click `RUN.bat` or run in Command Prompt:
   ```batch
   run.cmd scraper.py --headless
   ```

## Command-Line Options

Open Command Prompt in the project folder and run:

```batch
run.cmd scraper.py [options]
```

### Available Options:

| Option | Description | Example |
|--------|-------------|---------|
| `--headless` | Run without browser window (faster) | `run.cmd scraper.py --headless` |
| `-u URL` | Process single URL | `run.cmd scraper.py -u "https://..."` |
| `-i FILE` | Use custom input file | `run.cmd scraper.py -i my_urls.txt` |
| `-o FILE` | Specify output file | `run.cmd scraper.py -o results.xlsx` |
| `-h` | Show help | `run.cmd scraper.py -h` |

### Examples:

```batch
REM Process all URLs from input_url.txt (headless - fastest)
run.cmd scraper.py --headless

REM Process single URL
run.cmd scraper.py -u "https://vtf.trafikverket.se/..." --headless

REM Use custom input file
run.cmd scraper.py -i my_urls.txt --headless

REM Show help menu
run.cmd scraper.py -h
```

## Output Files

After running, you'll find Excel files in the project folder:

- `trafikverket_data_1522be33.xlsx` - First URL results
- `trafikverket_data_5fdf80ae.xlsx` - Second URL results
- (One file per URL, named with a hash of the URL)

Each file contains:
- All measurement occasions for that URL combined
- Single sheet named "Data"
- Headers on first row only
- All rows after that are data records

## Troubleshooting

### Problem: "Python is not recognized"

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. **Important:** Check the box "Add Python to PATH"
3. Restart Command Prompt after installation
4. Verify: Type `python --version`

### Problem: "Chrome not found"

**Solution:**
1. Install Google Chrome: https://www.google.com/chrome/
2. Restart the script

### Problem: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
Always use `run.cmd` (or `RUN.bat`), which automatically activates the virtual environment:
```batch
run.cmd scraper.py --headless
```

Do NOT run `python scraper.py` directly.

### Problem: "input_url.txt not found"

**Solution:**
1. Create a new file named `input_url.txt` in the project folder
2. Add URLs (one per line)
3. Save the file

### Problem: Scraper runs but finds no data

**Possible causes:**
- URLs are incorrect or website structure changed
- Network connection issue
- Website temporarily down

**Try:**
- Verify URL is correct by opening in browser
- Check internet connection
- Run again later

### Problem: Installation keeps failing

**Try manual installation:**

1. Open Command Prompt
2. Navigate to project folder:
   ```batch
   cd C:\path\to\trafficdata
   ```

3. Create virtual environment:
   ```batch
   python -m venv .venv
   ```

4. Activate it:
   ```batch
   .venv\Scripts\activate.bat
   ```

5. Install packages manually:
   ```batch
   pip install --upgrade pip
   pip install selenium pandas openpyxl webdriver-manager
   ```

6. Run scraper:
   ```batch
   python scraper.py --headless
   ```

## Project Files

```
trafficdata/
├── INSTALL.bat              # Auto-installer
├── SETUP-WIZARD.bat         # Interactive setup wizard
├── RUN.bat                  # Quick launcher (double-click)
├── WINDOWS-INSTALL.md       # This file
├── scraper.py              # Main scraper application
├── input_url.txt           # URLs to process (edit this)
├── run.cmd                 # Command-line runner
├── requirements.txt        # Dependencies for most Python versions
├── requirements-py39.txt   # Dependencies for Python 3.9
└── README.md              # Full documentation
```

## Getting Help

1. **Check README.md** - Comprehensive documentation
2. **Verify prerequisites** - Python 3.9.6+, Chrome installed
3. **Check input_url.txt** - Make sure URLs are valid
4. **Try headless mode** - `run.cmd scraper.py --headless`
5. **Review the FAQ** in README.md

## System Requirements

- **Windows 7, 8, 10, 11** (64-bit recommended)
- **Python 3.9.6 or higher**
- **Google Chrome** (any recent version)
- **1GB+ RAM** (for Chrome and Python)
- **50MB+ disk space** (for venv and dependencies)
- **Internet connection** (required for web scraping)

## Performance Tips

- Use `--headless` flag for 50% faster execution
- Process multiple URLs in one batch instead of separately
- Check your internet connection speed
- Close unnecessary programs to free up RAM

## Next Steps

1. ✅ Install using SETUP-WIZARD.bat
2. ✅ Edit input_url.txt with your URLs
3. ✅ Double-click RUN.bat to execute
4. ✅ Check output Excel files

Enjoy! 🚀
