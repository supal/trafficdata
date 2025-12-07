# Trafikverket Data Extractor

This application automatically extracts traffic data from the Trafikverket website and exports it to an Excel file.

## Requirements

- **Python 3.9.6 or higher** (tested on Python 3.9.6, 3.10, 3.11, 3.12, 3.13)
- Chrome/Chromium browser installed
- Internet connection

## Installation

### Step 1: Verify Python Version
```bash
python3 --version
```
Ensure you have Python 3.9.6 or higher.

### Step 2: Create a virtual environment (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### Step 3: Install required packages
For Python 3.9.6 specifically:
```bash
pip install -r requirements-py39.txt
```

Or for any Python 3.9+:
```bash
pip install -r requirements.txt
```

Alternatively, install packages directly:
```bash
pip install selenium>=4.0.0 pandas>=1.3.0 openpyxl>=3.0.0 webdriver-manager>=3.8.0
```

## Usage

### Basic Usage

Run the script with default settings:
```bash
python scraper.py
```

This will:
1. Open a Chrome browser window
2. Navigate to the Trafikverket website with the provided URL
3. Check all checkboxes on the page
4. Select "Table" as the presentation format
5. Click the "Starta" (Start) button
6. Extract all table data
7. Save the data to `trafikverket_data_<timestamp>.xlsx`

### Customizing the URL

Edit the `main()` function in `scraper.py` to change the URL:

```python
def main():
    url = "YOUR_NEW_URL_HERE"
    scraper = TrafikverketScraper(url)
    scraper.run(output_file="custom_output.xlsx")
```

### Using as a Module

```python
from scraper import TrafikverketScraper

url = "https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?..."
scraper = TrafikverketScraper(url)
scraper.run(output_file="my_data.xlsx")
```

## Features

- ✅ Automatic checkbox selection
- ✅ Table format selection
- ✅ Automatic data extraction
- ✅ Excel export with multiple sheet support
- ✅ Robust error handling
- ✅ Webdriver auto-management

## Headless Mode

To run the browser in the background (headless mode), uncomment this line in the `setup_driver()` method:

```python
options.add_argument('--headless')
```

## Output

The script generates an Excel file with the following naming convention:
- `trafikverket_data_<YYYYMMDD_HHMMSS>.xlsx`

If multiple tables are extracted, each will be saved as a separate sheet.

## Troubleshooting

### "Could not reach host" error
- Ensure you have an active internet connection
- Try running in headless mode: `options.add_argument('--headless')`

### Chrome/Chromium not found
- Install Google Chrome or Chromium browser
- Or specify the path to your browser in ChromeOptions

### Timeout errors
- Increase the wait times in the script (currently set to 3 seconds for page loads)
- Check if the website is responding correctly

### Elements not found
- The website structure might have changed
- Update the XPath selectors in the `check_all_checkboxes()`, `select_table_format()`, and `click_start_button()` methods

## Notes

- The script includes delays to allow pages to load and render properly
- All textual data is stripped of extra whitespace
- The browser window will close after extraction completes
