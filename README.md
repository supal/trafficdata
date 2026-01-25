# Trafikverket Data Extractor

A Python-based web scraper that extracts traffic measurement data from the Trafikverket website and stores it in a PostgreSQL database.

## Features

- 🚀 **Automated web scraping** - Automatically navigates the Trafikverket website
- 📊 **Multi-URL support** - Process multiple URLs from a configuration file
- 🗄️ **PostgreSQL integration** - Stores traffic data in a relational database with automatic schema creation
- ⚡ **Headless mode** - Fast, background execution without UI
- 🔄 **Intelligent waits** - Executes as soon as elements load, not fixed delays
- 🔁 **Duplicate detection** - Prevents duplicate records based on composite keys
- 📝 **Python 3.9+ compatible** - Works with Python 3.9.6 and newer versions

## Prerequisites

- **Python 3.9.6 or higher**
- **Google Chrome** (must be installed on your system)
- **PostgreSQL 12+** (local or remote database server)
- **pip** (Python package manager)
- **git** (for version control, optional)

## Installation for Fresh Environment

### Step 1: Clone or Download the Project

```bash
# If using git
git clone https://github.com/supal/trafficdata.git
cd trafficdata

# Or download and extract the ZIP file manually
```

### Step 2: Set Up PostgreSQL Database

**Create the database and user (use default credentials for local development):**

```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE traffic_data;
CREATE USER trafficdata WITH PASSWORD 'trafficdata';
ALTER ROLE trafficdata SET client_encoding TO 'utf8';
ALTER ROLE trafficdata SET default_transaction_isolation TO 'read committed';
ALTER ROLE trafficdata SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE traffic_data TO trafficdata;

# Exit psql
\q
```

**Or edit `scraper.py` to customize database credentials:**
```python
self.db_config = {
    'host': 'your-host',
    'user': 'your-username',
    'password': 'your-password',
    'database': 'traffic_data',
    'port': 5432
}
```

### Step 3: Set Up Virtual Environment and Dependencies

**On macOS/Linux:**
```bash
# Make scripts executable
chmod +x run.sh setup.sh

# Run setup script (creates venv and installs dependencies)
./setup.sh
```

**On Windows:**
```bash
# Option 1: Use provided batch script
setup.bat

# Option 2: Manual setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# On macOS/Linux
./run.sh scraper.py --help

# On Windows  
run.cmd scraper.py --help
```

You should see the help menu with available options.

## Quick Start

### 1. Ensure PostgreSQL is Running

Make sure your PostgreSQL server is running and the `traffic_data` database is created.

```bash
# On macOS with Homebrew
brew services start postgresql

# On Linux with systemd
sudo systemctl start postgresql

# On Windows
# PostgreSQL service should start automatically, or start it from Services
```

### 2. Add URLs to Process

Edit `input_url.txt` and add one URL per line:

```
https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520522,13520522&laenkrollista=2,3
https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520474,13520475&laenkrollista=1,1
```

### 3: Run the Scraper

**Recommended (fastest):**
```bash
./run.sh scraper.py --headless  # macOS/Linux
run.cmd scraper.py --headless   # Windows
```

**With browser window visible (for debugging):**
```bash
./run.sh scraper.py    # macOS/Linux
run.cmd scraper.py     # Windows
```

### 4: Check Output

Data will be automatically stored in the PostgreSQL `traffic_data` database. Query the data using:

```bash
# Connect to the database
psql -U postgres -d traffic_data

# Query all records
SELECT * FROM public.traffic_data;

# Query by date range
SELECT * FROM public.traffic_data 
WHERE measurement_time >= '2026-01-01' AND measurement_time < '2026-02-01';

# Query by road number
SELECT * FROM public.traffic_data WHERE road_number = '25';
```

## Command-Line Options

```bash
Usage: scraper.py [-h] [-u URL] [--headless]

Options:
  -h, --help              Show help message and exit
  -u, --url URL           Single URL to process (overrides input file)
  --headless              Run browser in headless mode (faster, no UI)
```

## Usage Examples

**Process all URLs from input_url.txt in headless mode (fastest):**
```bash
./run.sh scraper.py --headless
```

**Process a single URL:**
```bash
./run.sh scraper.py -u "https://vtf.trafikverket.se/..." --headless
```

**Run with browser window visible (for debugging):**
```bash
./run.sh scraper.py
```

## Output Format

Data is stored directly in the PostgreSQL `traffic_data` database with the following schema:

**Table: `public.traffic_data`**

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique record identifier |
| measurement_time | TIMESTAMP | Date and time of measurement |
| county | VARCHAR(100) | County/Region (Län) |
| road_number | VARCHAR(10) | Road number (Vägnr) |
| punkt_nummer | VARCHAR(20) | Measurement point ID |
| all_vehicles_count | INTEGER | Total vehicle count |
| all_vehicles_avg_speed | DECIMAL(5, 2) | Average speed for all vehicles |
| passenger_car_count | INTEGER | Passenger car count |
| passenger_car_avg_speed | DECIMAL(5, 2) | Average passenger car speed |
| heavy_vehicles_count | INTEGER | Heavy vehicle count |
| heavy_vehicles_avg_speed | DECIMAL(5, 2) | Average heavy vehicle speed |
| *_trailer_count / *_no_trailer_count | INTEGER | Breakdown by trailer type |
| *_trailer_avg_speed / *_no_trailer_avg_speed | DECIMAL(5, 2) | Speed data by trailer type |
| created_at | TIMESTAMP | Record insertion timestamp |

**Key Features:**
- Automatic schema creation on first run
- Composite key duplicate detection (measurement_time, county, road_number, punkt_nummer)
- Indexed for fast queries on measurement_time, punkt_nummer, and road/county combinations

## Project Structure

```
trafficdata/
├── scraper.py              # Main scraper application
├── cli.py                  # Command-line interface (alternative entry point)
├── compatibility.py        # Python version validation
├── input_url.txt          # URLs to process (one per line)
├── run.sh                 # Helper script for macOS/Linux
├── run.cmd                # Helper script for Windows
├── setup.sh               # Setup script for macOS/Linux
├── setup.bat              # Setup script for Windows
├── requirements.txt       # Python dependencies
├── requirements-py39.txt  # Python 3.9 specific dependencies
├── .python-version        # Python version hint
└── README.md             # This file
```

## How It Works

For each URL:

1. **Navigate** - Opens the Trafikverket webpage
2. **Detect** - Finds all measurement occasions available
3. **Loop** - For each measurement occasion:
   - Select the occasion from dropdown
   - Check all data checkboxes
   - Select table format
   - Click start button
   - Wait for popup window
   - Extract data from table
4. **Insert** - Stores each record in PostgreSQL with duplicate detection
5. **Commit** - Data is persisted to database

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:** Always use the `run.sh` or `run.cmd` helper scripts, which automatically activate the virtual environment:

```bash
./run.sh scraper.py --headless  # macOS/Linux
run.cmd scraper.py --headless   # Windows
```

### Issue: "could not translate host name \"localhost\" to address"

**Solution:** PostgreSQL is not running or not accessible. Check:

```bash
# On macOS
brew services list | grep postgres

# On Linux
sudo systemctl status postgresql

# Try connecting directly
psql -U postgres -d traffic_data
```

If you get "connection refused", start PostgreSQL:
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Issue: "FATAL: database 'traffic_data' does not exist"

**Solution:** Create the database following Step 2 of the installation:

```bash
psql -U postgres
CREATE DATABASE traffic_data;
CREATE USER trafficdata WITH PASSWORD 'trafficdata';
GRANT ALL PRIVILEGES ON DATABASE traffic_data TO trafficdata;
\q
```

### Issue: Browser window not opening in headless mode

**This is expected!** Headless mode runs in the background without UI. To see the browser:

```bash
./run.sh scraper.py  # Remove --headless flag
```

### Issue: "Could not reach host" error

This is a ChromeDriver download issue, not fatal. The scraper automatically falls back to system ChromeDriver.

### Issue: Timeouts or missed data

Check your internet connection. If on very slow connection, increase timeouts in `scraper.py`:

```python
# Increase these values (currently 5-10 seconds):
WebDriverWait(self.driver, 10).until(...)
```

### Issue: Input file not found

Create `input_url.txt` in the project directory:

**macOS/Linux:**
```bash
echo "https://your-url-here" > input_url.txt
```

**Windows:**
```bash
echo https://your-url-here > input_url.txt
```

### Issue: Chrome not installed

Install Google Chrome from: https://www.google.com/chrome/

Or install Chromium:
```bash
# macOS
brew install chromium

# Ubuntu/Debian
sudo apt-get install chromium

# Fedora
sudo dnf install chromium
```

### Issue: Duplicate rows in database

The scraper includes duplicate detection based on composite key (measurement_time, county, road_number, punkt_nummer). If you see duplicates, this may indicate:
- Data was inserted twice with slightly different timestamps
- The composite key detection needs adjustment

Check the database:
```bash
SELECT COUNT(*) FROM public.traffic_data;
SELECT DISTINCT measurement_time, county, road_number, punkt_nummer FROM public.traffic_data;
```

## Python Version Support

- ✅ Tested: Python 3.9.6, 3.13.8
- ✅ Compatible: Python 3.9+
- ⚠️ Not tested: Python < 3.9

Check your Python version:

```bash
python --version
# or
python3 --version
```

## Dependencies

### Python Packages

- **selenium** (4.38.0) - Web browser automation
- **pandas** (2.3.3) - Data manipulation
- **psycopg2** (2.9.0+) - PostgreSQL database adapter
- **webdriver-manager** (4.0.2) - Automatic Chrome driver management

All dependencies are automatically installed during setup.

## Performance Optimization

### Tips for Fastest Execution

1. **Use headless mode:**
   ```bash
   ./run.sh scraper.py --headless  # ~50% faster
   ```

2. **Batch multiple URLs:**
   - Process all URLs in one run instead of separately
   - Saves startup time

3. **Check internet connection:**
   - Most execution time is network waiting
   - Faster internet = faster extraction

### Performance Metrics

With optimized intelligent waits (execute immediately when ready):
- Single URL, 5 measurement occasions: ~2-3 minutes
- Headless mode: 50% faster than with UI

## Advanced Configuration

### Custom Chrome Options

Edit `setup_driver()` method in `scraper.py`:

```python
options.add_argument('--disable-notifications')  # No notifications
options.add_argument('--no-sandbox')             # Sandbox disabled
options.add_argument('--disable-dev-shm-usage')  # Lower memory
options.add_argument('--window-size=1920,1080')  # Custom window size
```

### Adjust Timeout Values

In `scraper.py`, modify WebDriverWait timeouts:

```python
# Default is 5-10 seconds, increase if needed:
WebDriverWait(self.driver, 15).until(...)  # 15 seconds
```

### Custom Delays

Most delays have been optimized to execute immediately when elements load. Fixed delays are minimal (~1-2 seconds for complex page loads).

## Frequently Asked Questions

**Q: How long does extraction take?**
A: ~2-5 minutes per URL depending on internet speed. Headless mode is faster.

**Q: Can I run multiple scrapes simultaneously?**
A: Not recommended - would require separate Chrome instances. Process URLs sequentially.

**Q: What if the website changes?**
A: Update the XPath selectors in `scraper.py` if elements are renamed/repositioned.

**Q: Can I use this on a server/VPS?**
A: Yes, especially useful there. Headless mode is perfect for servers.

**Q: Do I need to be online the entire time?**
A: Yes, the scraper connects to Trafikverket continuously throughout extraction.

## Support & Issues

1. Check the **Troubleshooting** section above
2. Review code comments in `scraper.py`
3. Verify Chrome is installed: `which google-chrome` (macOS/Linux)
4. Ensure `input_url.txt` exists and has valid URLs

## License

This project is part of Dalarna University thesis research.

## Notes

- **Headless mode recommended** for production and batch processing
- **Browser window mode useful** for debugging extraction issues
- **Network speed** is the primary factor affecting total execution time
- **Intelligent waits** mean execution is as fast as network allows
- Data extraction respects website rate limiting

