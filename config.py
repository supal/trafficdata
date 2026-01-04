"""
Configuration file for Trafikverket Scraper
Edit these settings to customize the scraper behavior
"""

# Default URL to scrape
DEFAULT_URL = "https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520237%2c13520237%2c13520505&laenkrollista=2%2c3%2c1"

# Output file settings
DEFAULT_OUTPUT_FILE = None  # None = auto-generate with timestamp
OUTPUT_DIRECTORY = "./output"  # Directory to save output files

# Browser settings
HEADLESS_MODE = False  # Set to True to run browser in background
BROWSER_WINDOW_SIZE = (1920, 1080)  # Width, Height
MAXIMIZE_WINDOW = True  # Maximize window on start
DISABLE_IMAGES = False  # Set to True to speed up loading (no images)

# Timing settings (in seconds)
PAGE_LOAD_TIMEOUT = 10
ELEMENT_WAIT_TIMEOUT = 10
BETWEEN_ACTIONS_DELAY = 0.3
AFTER_START_BUTTON_DELAY = 3

# Element selectors (XPath patterns)
# These may need to be updated if the website structure changes
CHECKBOX_SELECTOR = "//input[@type='checkbox']"
TABLE_FORMAT_SELECTORS = [
    "//input[@value='Tabell' or @value='Table']",
    "//label[contains(text(), 'Tabell')]",
]
START_BUTTON_SELECTORS = [
    "//button[contains(text(), 'Starta')]",
    "//button[contains(text(), 'Start')]",
    "//input[@type='button'][contains(@value, 'Starta')]",
    "//input[@type='button'][contains(@value, 'Start')]",
    "//button[@id='startButton']",
    "//input[@name='startButton']"
]

# Data export settings
# CSV export is the default format

# Logging
VERBOSE_OUTPUT = True
LOG_FILE = None  # Set to filename to log to file, None to disable

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # Seconds between retries

# Row limit settings
# If rowCount is set to a positive value, the program will exit after that many rows
# Set to 0 or None to disable row limit
rowCount = 0  # 0 = unlimited, >0 = max rows to process
