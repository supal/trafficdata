"""
Traffic Data Extractor from Trafikverket
Extracts data from the Trafikverket website and exports to Excel
Compatible with Python 3.9.6+
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import re
import psycopg2
from psycopg2 import sql

# Import config
try:
    from config import OUTPUT_DIRECTORY, rowCount
except ImportError:
    OUTPUT_DIRECTORY = "./output"
    rowCount = 0

# Import compatibility module
try:
    from compatibility import check_dependencies, print_system_info
except ImportError:
    # Fallback if compatibility module not available
    def check_dependencies():
        return True
    def print_system_info():
        pass


class TrafikverketScraper:
    def __init__(self, url, headless=False):
        """Initialize the scraper with the given URL"""
        self.url = url
        self.driver = None
        self.data = []
        self.headless = headless
        self.coordinate_cache = {}  # Cache for punkt_id -> (lat, lon)
        self.page_metadata = {}  # Metadata extracted from page (Punktnummer, Vägnr, Län)
        self.total_rows_extracted = 0  # Track total rows extracted
        self.db_connection = None
        self.db_cursor = None
        self.db_config = {
            'host': 'localhost',
            'user': 'postgres',
            'password': '',
            'database': 'traffic_data',
            'port': 5432
        }
        self.load_coordinate_cache()  # Load cache from file
        self.connect_to_database()  # Connect to PostgreSQL
        
    def load_coordinate_cache(self):
        """Load coordinate cache from file if it exists"""
        cache_file = "coordinate_cache.txt"
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        parts = line.split('|')
                        if len(parts) == 3:
                            punkt_id = parts[0].strip()
                            lat = parts[1].strip()
                            lon = parts[2].strip()
                            self.coordinate_cache[punkt_id] = (lat, lon)
                print(f"Loaded {len(self.coordinate_cache)} cached coordinates")
            except Exception as e:
                print(f"Warning: Could not load coordinate cache: {e}")
    
    def save_coordinate_cache(self):
        """Save coordinate cache to file"""
        cache_file = "coordinate_cache.txt"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write("# Coordinate Cache (punkt_id|latitude|longitude)\n")
                f.write("# Auto-generated - do not edit manually\n\n")
                for punkt_id, (lat, lon) in self.coordinate_cache.items():
                    f.write(f"{punkt_id}|{lat}|{lon}\n")
            print(f"Saved {len(self.coordinate_cache)} coordinates to cache")
        except Exception as e:
            print(f"Warning: Could not save coordinate cache: {e}")
    
    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        try:
            print("Connecting to PostgreSQL database...")
            self.db_connection = psycopg2.connect(**self.db_config)
            self.db_cursor = self.db_connection.cursor()
            
            # Create public schema if it doesn't exist
            self.db_cursor.execute("CREATE SCHEMA IF NOT EXISTS public")
            self.db_connection.commit()
            
            print("✓ Connected to PostgreSQL")
            
            # Check if table exists and create if needed
            self.create_table_if_not_exists()
        except Exception as e:
            print(f"✗ Error connecting to database: {e}")
            self.db_connection = None
            self.db_cursor = None
    
    def create_table_if_not_exists(self):
        """Create the traffic_data table if it doesn't exist"""
        try:
            # Check if table exists
            self.db_cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name = 'traffic_data'
                )
            """)
            table_exists = self.db_cursor.fetchone()[0]
            
            if not table_exists:
                print("Creating traffic_data table...")
                create_table_sql = """
                CREATE TABLE public.traffic_data (
                    id SERIAL PRIMARY KEY,
                    measurement_time TIMESTAMP NOT NULL,
                    county VARCHAR(100),
                    road_number VARCHAR(10),
                    punkt_nummer VARCHAR(20),
                    
                    all_vehicles_count INTEGER,
                    all_vehicles_avg_speed DECIMAL(5, 2),
                    
                    passenger_car_count INTEGER,
                    passenger_car_avg_speed DECIMAL(5, 2),
                    
                    heavy_vehicles_count INTEGER,
                    heavy_vehicles_avg_speed DECIMAL(5, 2),
                    
                    heavy_vehicles_trailer_count INTEGER,
                    heavy_vehicles_trailer_avg_speed DECIMAL(5, 2),
                    
                    heavy_vehicles_no_trailer_count INTEGER,
                    heavy_vehicles_no_trailer_avg_speed DECIMAL(5, 2),
                    
                    three_axle_tractor_trailer_count INTEGER,
                    three_axle_tractor_trailer_avg_speed DECIMAL(5, 2),
                    
                    two_axle_tractor_trailer_count INTEGER,
                    two_axle_tractor_trailer_avg_speed DECIMAL(5, 2),
                    
                    three_axle_tractor_no_trailer_count INTEGER,
                    three_axle_tractor_no_trailer_avg_speed DECIMAL(5, 2),
                    
                    two_axle_tractor_no_trailer_count INTEGER,
                    two_axle_tractor_no_trailer_avg_speed DECIMAL(5, 2),
                    
                    passenger_car_trailer_count INTEGER,
                    passenger_car_trailer_avg_speed DECIMAL(5, 2),
                    
                    passenger_car_no_trailer_count INTEGER,
                    passenger_car_no_trailer_avg_speed DECIMAL(5, 2),
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                self.db_cursor.execute(create_table_sql)
                
                # Create indexes
                self.db_cursor.execute("CREATE INDEX idx_measurement_time ON public.traffic_data(measurement_time)")
                self.db_cursor.execute("CREATE INDEX idx_punkt_nummer ON public.traffic_data(punkt_nummer)")
                self.db_cursor.execute("CREATE INDEX idx_road_county ON public.traffic_data(road_number, county)")
                
                self.db_connection.commit()
                print("✓ Table created successfully with indexes")
            else:
                print("✓ Table 'traffic_data' already exists")
        except Exception as e:
            print(f"Error creating table: {e}")
            self.db_connection.rollback()
    
    def parse_speed_value(self, value):
        """Convert Swedish decimal format (comma) to float"""
        if pd.isna(value) or value == '':
            return None
        try:
            value_str = str(value).strip()
            if value_str == '0,0' or value_str == '0.0':
                return 0.0
            return float(value_str.replace(',', '.'))
        except (ValueError, AttributeError):
            return None
    
    def parse_count_value(self, value):
        """Convert count to integer"""
        if pd.isna(value) or value == '':
            return 0
        try:
            return int(float(str(value).strip()))
        except (ValueError, AttributeError):
            return 0
    
    def insert_row_to_database(self, row_data):
        """Insert a single row into the traffic_data table, skip if duplicate exists"""
        try:
            if not self.db_connection or not self.db_cursor:
                return False
            
            # Extract key fields for duplicate check
            measurement_time = row_data[0]
            county = row_data[1]
            road_number = row_data[2]
            punkt_nummer = row_data[3]
            
            # Check if row with same measurement_time, county, road_number, punkt_nummer already exists
            check_sql = """
            SELECT COUNT(*) FROM public.traffic_data
            WHERE measurement_time = %s 
              AND county = %s 
              AND road_number = %s 
              AND punkt_nummer = %s
            """
            
            self.db_cursor.execute(check_sql, (measurement_time, county, road_number, punkt_nummer))
            existing_count = self.db_cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"    Row already exists: {measurement_time} | {county} | {road_number} | {punkt_nummer}")
                return False
            
            insert_sql = """
            INSERT INTO public.traffic_data (
                measurement_time, county, road_number, punkt_nummer,
                all_vehicles_count, all_vehicles_avg_speed,
                passenger_car_count, passenger_car_avg_speed,
                heavy_vehicles_count, heavy_vehicles_avg_speed,
                heavy_vehicles_trailer_count, heavy_vehicles_trailer_avg_speed,
                heavy_vehicles_no_trailer_count, heavy_vehicles_no_trailer_avg_speed,
                three_axle_tractor_trailer_count, three_axle_tractor_trailer_avg_speed,
                two_axle_tractor_trailer_count, two_axle_tractor_trailer_avg_speed,
                three_axle_tractor_no_trailer_count, three_axle_tractor_no_trailer_avg_speed,
                two_axle_tractor_no_trailer_count, two_axle_tractor_no_trailer_avg_speed,
                passenger_car_trailer_count, passenger_car_trailer_avg_speed,
                passenger_car_no_trailer_count, passenger_car_no_trailer_avg_speed
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.db_cursor.execute(insert_sql, row_data)
            self.db_connection.commit()
            return True
        except Exception as e:
            print(f"Error inserting row: {e}")
            return False
    
    
    def extract_punkt_ids_from_url(self):
        """Extract punkt IDs from the URL parameter"""
        try:
            parsed = urlparse(self.url)
            params = parse_qs(parsed.query)
            punkt_nrlista = params.get('punktnrlista', [''])[0]
            if punkt_nrlista:
                punkt_ids = punkt_nrlista.split(',')
                return [pid.strip() for pid in punkt_ids]
        except Exception as e:
            print(f"Warning: Could not extract punkt IDs from URL: {e}")
        return []
    
    def fetch_coordinate_from_trafikverket(self, punkt_id):
        """Fetch coordinates for a punkt ID from Trafikverket (if available)"""
        # Try to find coordinates from the page
        try:
            # Search for punkt ID in page and extract nearby coordinate info
            scripts = self.driver.find_elements(By.TAG_NAME, "script")
            for script in scripts:
                script_text = script.get_attribute("innerHTML")
                if punkt_id in script_text:
                    # Try to extract lat/lon if present in script
                    # Look for patterns like "lat": 59.xxx or latitude: 59.xxx
                    lat_match = re.search(r'["\']?(?:lat|latitude)["\']?\s*:\s*([0-9.]+)', script_text)
                    lon_match = re.search(r'["\']?(?:lon|longitude)["\']?\s*:\s*([0-9.]+)', script_text)
                    if lat_match and lon_match:
                        return lat_match.group(1), lon_match.group(1)
        except:
            pass
        return None, None
    
    def get_coordinates(self, punkt_id):
        """Get coordinates for a punkt ID (from cache or fetch)"""
        if punkt_id in self.coordinate_cache:
            return self.coordinate_cache[punkt_id]
        
        # Try to fetch from website
        lat, lon = self.fetch_coordinate_from_trafikverket(punkt_id)
        if lat and lon:
            self.coordinate_cache[punkt_id] = (lat, lon)
            return lat, lon
        
        return None, None
    
    def extract_metadata_from_page(self):
        """Extract metadata from the rendered page (county, road number, punkt nummer, riktning)"""
        metadata = {}
        try:
            # Extract county from span with id lblDLaen
            try:
                county_element = self.driver.find_element(By.ID, "lblDLaen")
                county_value = county_element.text.strip()
                if county_value:
                    metadata['county'] = county_value
                    print(f"  Found county: {metadata['county']}")
            except NoSuchElementException:
                print("  Warning: Could not find county element (lblDLaen)")
            
            # Extract road number from span with id lblDVaegnr
            try:
                road_element = self.driver.find_element(By.ID, "lblDVaegnr")
                road_value = road_element.text.strip()
                if road_value:
                    metadata['road number'] = road_value
                    print(f"  Found road number: {metadata['road number']}")
            except NoSuchElementException:
                print("  Warning: Could not find road number element (lblDVaegnr)")
            
            # Extract punkt nummer from span with id lblDPunktnummer
            try:
                punkt_element = self.driver.find_element(By.ID, "lblDPunktnummer")
                punkt_value = punkt_element.text.strip()
                if punkt_value:
                    metadata['punkt nummer'] = punkt_value
                    print(f"  Found punkt nummer: {metadata['punkt nummer']}")
            except NoSuchElementException:
                print("  Warning: Could not find punkt nummer element (lblDPunktnummer)")
            
            # Extract riktning from span with id lblDRiktning
            try:
                riktning_element = self.driver.find_element(By.ID, "lblDRiktning")
                riktning_value = riktning_element.text.strip()
                if riktning_value:
                    metadata['riktning'] = riktning_value
                    print(f"  Found riktning: {metadata['riktning']}")
            except NoSuchElementException:
                print("  Warning: Could not find riktning element (lblDRiktning)")
            
            return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}

        
    def setup_driver(self):
        """Set up the Chrome WebDriver"""
        print("Setting up Chrome WebDriver...")
        options = webdriver.ChromeOptions()
        
        # Enable headless mode if requested
        if self.headless:
            options.add_argument('--headless')
            print("Running in headless mode (faster)")
        
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            print("Attempting to set up ChromeDriver with webdriver-manager...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("WebDriver setup successful!")
        except Exception as e:
            print(f"Error with webdriver-manager: {e}")
            print("Trying to use system ChromeDriver...")
            try:
                self.driver = webdriver.Chrome(options=options)
                print("WebDriver setup successful with system ChromeDriver!")
            except Exception as e2:
                print(f"Error starting WebDriver: {e2}")
                raise
    
    def get_measurement_occasions(self):
        """Get all available measurement occasions"""
        try:
            print("Getting all measurement occasions...")
            # Find the measurement occasion dropdown/select element
            # Common selectors for select elements
            select_selectors = [
                "//select[@id*='Matt']",
                "//select[contains(@name, 'Matt')]",
                "//select[@name*='Mattle']",
                "//select",  # Generic select as fallback
            ]
            
            occasions = []
            select_element = None
            
            for selector in select_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        select_element = elements[0]
                        break
                except:
                    continue
            
            if select_element:
                # Get all option elements
                options = select_element.find_elements(By.XPATH, ".//option")
                occasions = [(opt.get_attribute("value"), opt.text) for opt in options if opt.get_attribute("value")]
                print(f"Found {len(occasions)} measurement occasion(s):")
                for value, text in occasions:
                    print(f"  - {text}")
                return occasions
            else:
                print("Warning: Could not find measurement occasions dropdown")
                return []
        except Exception as e:
            print(f"Error getting measurement occasions: {e}")
            return []
    
    def select_measurement_occasion(self, value):
        """Select a specific measurement occasion"""
        try:
            print(f"Selecting measurement occasion: {value}...")
            
            # Find and select the option
            select_selectors = [
                "//select[@id*='Matt']",
                "//select[contains(@name, 'Matt')]",
                "//select[@name*='Mattle']",
                "//select",
            ]
            
            select_element = None
            for selector in select_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        select_element = elements[0]
                        break
                except:
                    continue
            
            if select_element:
                # Use Select class to select the option
                from selenium.webdriver.support.ui import Select
                select = Select(select_element)
                select.select_by_value(value)
                time.sleep(1)
                print(f"Selected: {value}")
                return True
            else:
                print("Error: Could not find measurement occasions dropdown")
                return False
        except Exception as e:
            print(f"Error selecting measurement occasion {value}: {e}")
            return False
    
    def navigate_to_page(self):
        """Navigate to the target page and extract metadata"""
        print(f"Navigating to {self.url}...")
        self.driver.get(self.url)
        # Wait for the measurement occasion dropdown to be clickable (indicates page is loaded)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//select[@id] | //option"))
            )
            print("Page loaded successfully")
            
            # Extract and cache metadata once at the beginning
            print("Extracting page metadata...")
            self.page_metadata = self.extract_metadata_from_page()
            if self.page_metadata:
                print(f"  Cached metadata: {self.page_metadata}")
        except TimeoutException:
            print("Warning: Page load timeout, continuing anyway...")
    
    def check_all_checkboxes(self):
        """Check all checkboxes on the page"""
        print("Checking all checkboxes...")
        try:
            # Find all checkboxes
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            print(f"Found {len(checkboxes)} checkboxes")
            
            for i, checkbox in enumerate(checkboxes):
                # Scroll to checkbox if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.3)
                
                # Click if not already checked
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"  Checked checkbox {i+1}/{len(checkboxes)}")
                time.sleep(0.2)
        except Exception as e:
            print(f"Error checking checkboxes: {e}")
    
    def select_table_format(self):
        """Select table as the presentation format"""
        print("Selecting table format...")
        try:
            # Look for the presentation format dropdown/radio button
            # Common selectors for "table" option
            table_options = self.driver.find_elements(By.XPATH, "//input[@value='Tabell' or @value='Table' or contains(., 'Tabell')]")
            
            if table_options:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", table_options[0])
                table_options[0].click()
                print("Table format selected")
                time.sleep(1)
            else:
                print("Warning: Could not find table format option, trying alternative selectors...")
                # Try finding by label
                labels = self.driver.find_elements(By.XPATH, "//label[contains(text(), 'Tabell')]")
                if labels:
                    labels[0].click()
                    print("Table format selected via label")
                    time.sleep(1)
        except Exception as e:
            print(f"Warning: Could not select table format: {e}")
    
    def click_start_button(self):
        """Click the start button to generate the table"""
        print("Clicking the start button...")
        try:
            # Look for start button - common identifiers
            start_button = None
            
            # Try different selectors
            selectors = [
                "//input[@id='cmdStarta']",  # Direct ID selector (most reliable)
                "//input[@type='submit'][@value='Starta']",  # Type and value
                "//button[contains(text(), 'Starta')]",
                "//button[contains(text(), 'Start')]",
                "//input[@type='button'][contains(@value, 'Starta')]",
                "//input[@type='button'][contains(@value, 'Start')]",
                "//button[@id='startButton']",
                "//input[@name='cmdStarta']"  # Name attribute
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        start_button = elements[0]
                        print(f"  Found button using selector: {selector}")
                        break
                except:
                    continue
            
            if start_button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", start_button)
                time.sleep(0.5)
                start_button.click()
                print("Start button clicked successfully")
                # Wait for popup to open (handle_popup_window will wait for it)
                self.handle_popup_window()
            else:
                print("Warning: Could not find start button - trying JavaScript click")
                # Try clicking via JavaScript as fallback
                try:
                    self.driver.execute_script("document.getElementById('cmdStarta').click();")
                    print("Started via JavaScript")
                    self.handle_popup_window()
                except:
                    print("Error: Could not click start button")
        except Exception as e:
            print(f"Error clicking start button: {e}")
    
    def handle_popup_window(self):
        """Handle popup window and extract data"""
        try:
            print("Checking for popup window...")
            
            # Get all window handles
            main_window = self.driver.current_window_handle
            time.sleep(2)
            
            # Get all open windows
            all_windows = self.driver.window_handles
            print(f"  Found {len(all_windows)} window(s)")
            
            # Switch to popup if exists
            if len(all_windows) > 1:
                popup_window = all_windows[-1]  # Usually the last opened window
                self.driver.switch_to.window(popup_window)
                print(f"  Switched to popup window")
                # Wait for tables to appear in popup
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
                    )
                except TimeoutException:
                    print("  Warning: Tables did not appear quickly, continuing...")
                
                # Extract table data from popup using cached metadata
                self.extract_popup_table_data()
                
                # Close popup and switch back
                self.driver.close()
                self.driver.switch_to.window(main_window)
                print("  Popup closed, switched back to main window")
            else:
                print("  No popup window found, data might be in main window")
        except Exception as e:
            print(f"Error handling popup: {e}")
    
    def extract_popup_table_data(self):
        """Extract data from popup table and insert into database"""
        try:
            print("Extracting data from popup...")
            
            # Find all tables in popup
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"  Found {len(tables)} table(s) in popup")
            
            if len(tables) == 0:
                print("  No tables found in popup, trying to find any data elements...")
                return
            
            for table_idx, table in enumerate(tables):
                # Only process table 3 (index 2)
                if table_idx != 2:
                    print(f"  Skipping popup table {table_idx + 1}...")
                    continue
                
                print(f"  Processing popup table {table_idx + 1}...")
                
                # Extract headers
                headers = []
                header_cells = table.find_elements(By.XPATH, ".//th")
                for cell in header_cells:
                    headers.append(cell.text.strip())
                
                if headers:
                    print(f"    Headers: {headers}")
                
                # Extract rows
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"    Found {len(rows)} rows")
                
                rows_inserted = 0
                
                for i, row in enumerate(rows):
                    cells = row.find_elements(By.XPATH, "./td")
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        
                        # Skip header row (contains "Tidpunkt" or similar)
                        if row_data and row_data[0].lower() in ['tidpunkt', 'time', 'tid']:
                            print(f"    Row {i}: Skipping header row: {row_data[0]}")
                            continue
                        
                        # Check if row limit is set
                        if rowCount > 0 and self.total_rows_extracted >= rowCount:
                            print(f"    Row {i}: Row limit of {rowCount} reached (current total: {self.total_rows_extracted}).")
                            return
                        
                        # Parse and insert the row
                        print(f"    Row {i}: Attempting to insert data from {row_data[0]}")
                        if self.parse_and_insert_row(row_data):
                            rows_inserted += 1
                            self.total_rows_extracted += 1
                            print(f"    Row {i}: Successfully inserted (total: {self.total_rows_extracted})")
                        else:
                            print(f"    Row {i}: Failed to insert row starting with: {row_data[0] if row_data else 'empty'}")
                
                if rows_inserted > 0:
                    print(f"    Inserted {rows_inserted} data rows from popup table {table_idx + 1}")
                    print(f"    Total rows inserted so far: {self.total_rows_extracted}")
                
        except Exception as e:
            print(f"Error extracting popup table data: {e}")
    
    def parse_and_insert_row(self, row_data):
        """Parse row data and insert into database"""
        try:
            if not self.db_connection or not self.db_cursor:
                print(f"    Debug: Database connection issue")
                return False
            
            # Need at least 23 columns (0-22 for the actual data)
            if len(row_data) < 23:
                print(f"    Debug: Row has {len(row_data)} columns, expected at least 23")
                return False
            
            # Parse the measurement time
            measurement_time = pd.to_datetime(row_data[0])
            
            # Extract metadata from page
            county = self.page_metadata.get('county', None)
            road_number = self.page_metadata.get('road number', None)
            punkt_nummer = self.page_metadata.get('punkt nummer', None)
            
            # Parse vehicle counts and speeds (skipping every other column)
            all_vehicles_count = self.parse_count_value(row_data[1])
            all_vehicles_avg_speed = self.parse_speed_value(row_data[2])
            
            heavy_vehicles_count = self.parse_count_value(row_data[3])
            heavy_vehicles_avg_speed = self.parse_speed_value(row_data[4])
            
            passenger_car_count = self.parse_count_value(row_data[5])
            passenger_car_avg_speed = self.parse_speed_value(row_data[6])
            
            heavy_vehicles_trailer_count = self.parse_count_value(row_data[7])
            heavy_vehicles_trailer_avg_speed = self.parse_speed_value(row_data[8])
            
            heavy_vehicles_no_trailer_count = self.parse_count_value(row_data[9])
            heavy_vehicles_no_trailer_avg_speed = self.parse_speed_value(row_data[10])
            
            three_axle_tractor_trailer_count = self.parse_count_value(row_data[11])
            three_axle_tractor_trailer_avg_speed = self.parse_speed_value(row_data[12])
            
            two_axle_tractor_trailer_count = self.parse_count_value(row_data[13])
            two_axle_tractor_trailer_avg_speed = self.parse_speed_value(row_data[14])
            
            three_axle_tractor_no_trailer_count = self.parse_count_value(row_data[15])
            three_axle_tractor_no_trailer_avg_speed = self.parse_speed_value(row_data[16])
            
            two_axle_tractor_no_trailer_count = self.parse_count_value(row_data[17])
            two_axle_tractor_no_trailer_avg_speed = self.parse_speed_value(row_data[18])
            
            passenger_car_trailer_count = self.parse_count_value(row_data[19])
            passenger_car_trailer_avg_speed = self.parse_speed_value(row_data[20])
            
            passenger_car_no_trailer_count = self.parse_count_value(row_data[21])
            passenger_car_no_trailer_avg_speed = self.parse_speed_value(row_data[22])
            
            # Prepare row data for insertion
            insert_data = (
                measurement_time, county, road_number, punkt_nummer,
                all_vehicles_count, all_vehicles_avg_speed,
                passenger_car_count, passenger_car_avg_speed,
                heavy_vehicles_count, heavy_vehicles_avg_speed,
                heavy_vehicles_trailer_count, heavy_vehicles_trailer_avg_speed,
                heavy_vehicles_no_trailer_count, heavy_vehicles_no_trailer_avg_speed,
                three_axle_tractor_trailer_count, three_axle_tractor_trailer_avg_speed,
                two_axle_tractor_trailer_count, two_axle_tractor_trailer_avg_speed,
                three_axle_tractor_no_trailer_count, three_axle_tractor_no_trailer_avg_speed,
                two_axle_tractor_no_trailer_count, two_axle_tractor_no_trailer_avg_speed,
                passenger_car_trailer_count, passenger_car_trailer_avg_speed,
                passenger_car_no_trailer_count, passenger_car_no_trailer_avg_speed
            )
            
            return self.insert_row_to_database(insert_data)
        except Exception as e:
            print(f"    Error parsing row: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    
    def extract_table_data(self):
        """Extract data from the generated table"""
        print("Extracting table data...")
        try:
            # Wait for table to appear
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "table"))
            )
            
            # Find all tables
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"Found {len(tables)} table(s)")
            
            for table_idx, table in enumerate(tables):
                # Only process table 3 (index 2)
                if table_idx != 2:
                    print(f"Skipping table {table_idx + 1}...")
                    continue
                
                print(f"Processing table {table_idx + 1}...")
                
                # Extract rows (skip headers)
                rows = table.find_elements(By.XPATH, ".//tr")
                print(f"  Found {len(rows)} rows")
                
                all_data = []
                
                for row_idx, row in enumerate(rows):
                    cells = row.find_elements(By.XPATH, "./td")
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        all_data.append(row_data)
                
                # Only create DataFrame if we have data rows
                if all_data:
                    # Check if row limit is set and if we would exceed it
                    if rowCount > 0 and (self.total_rows_extracted + len(all_data)) > rowCount:
                        # Trim data to not exceed row limit
                        rows_to_take = rowCount - self.total_rows_extracted
                        if rows_to_take > 0:
                            all_data = all_data[:rows_to_take]
                            print(f"  Row limit reached. Trimmed to {rows_to_take} rows")
                        else:
                            print(f"  Row limit already reached, skipping this table")
                            continue
                    
                    self.total_rows_extracted += len(all_data)
                    df = pd.DataFrame(all_data)
                    self.data.append(df)
                    print(f"  Extracted {len(all_data)} data rows from table {table_idx + 1}")
                    print(f"  Total rows so far: {self.total_rows_extracted}")
                    
                    # Stop extraction if row limit reached
                    if rowCount > 0 and self.total_rows_extracted >= rowCount:
                        print(f"Row limit of {rowCount} reached. Stopping extraction.")
                        return True
            
            return True
        except TimeoutException:
            print("Error: Table did not appear within timeout period")
            return False
        except Exception as e:
            print(f"Error extracting table data: {e}")
            return False
    
    def load_translations(self):
        """Load translations from translation.txt file"""
        translations = {}
        translation_file = "translation.txt"
        
        if not os.path.exists(translation_file):
            print(f"Warning: {translation_file} not found, skipping translations")
            return translations
        
        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by comma to get individual key=value pairs
            pairs = content.split(',')
            
            for pair in pairs:
                pair = pair.strip()
                # Skip empty lines and comments
                if not pair or pair.startswith('#'):
                    continue
                
                # Split by = to separate key and value
                if '=' in pair:
                    parts = pair.split('=', 1)  # Use maxsplit=1 in case value contains =
                    if len(parts) == 2:
                        swedish = parts[0].strip()
                        english = parts[1].strip()
                        if swedish and english:  # Only add if both parts are non-empty
                            translations[swedish] = english
            
            print(f"Loaded {len(translations)} translation(s)")
            return translations
        except Exception as e:
            print(f"Error loading translations: {e}")
            return {}
    
    def apply_translations(self, df, translations):
        """Apply translations to dataframe columns and values"""
        if not translations:
            return df
        
        # Normalize translation keys (remove extra whitespace, tabs, etc.)
        normalized_translations = {}
        for swedish, english in translations.items():
            normalized_key = ' '.join(swedish.split())  # Normalize whitespace
            normalized_translations[normalized_key] = english
        
        # Translate column headers
        normalized_columns = {}
        for col in df.columns:
            normalized_col = ' '.join(str(col).split())
            if normalized_col in normalized_translations:
                normalized_columns[col] = normalized_translations[normalized_col]
            else:
                normalized_columns[col] = col
        df.columns = [normalized_columns.get(col, col) for col in df.columns]
        
        # Sort translation keys by length (longest first) to avoid partial replacements
        sorted_translations = sorted(normalized_translations.items(), key=lambda x: len(x[0]), reverse=True)
        
        # Translate cell values (all columns) - use substring matching
        for col in df.columns:
            if df[col].dtype == 'object':  # Only for string columns
                def translate_value(x):
                    if pd.isna(x):
                        return x
                    text = str(x)
                    # Normalize whitespace in the text
                    normalized_text = ' '.join(text.split())
                    # Replace translation keys in order (longest first)
                    for swedish, english in sorted_translations:
                        if swedish in normalized_text:
                            normalized_text = normalized_text.replace(swedish, english)
                    return normalized_text
                
                df[col] = df[col].apply(translate_value)
        
        return df
    
    def save_to_excel(self, filename=None):
        """Save extracted data to CSV file (comma-separated values) for easier ETL processing"""
        if not self.data:
            print("No data to save")
            return False
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trafikverket_data_{timestamp}.csv"
        else:
            # Replace .xlsx with .csv if needed
            filename = filename.replace('.xlsx', '.csv')
        
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(OUTPUT_DIRECTORY):
                os.makedirs(OUTPUT_DIRECTORY)
                print(f"Created output directory: {OUTPUT_DIRECTORY}")
            
            # Construct full filepath
            filepath = os.path.join(OUTPUT_DIRECTORY, os.path.basename(filename))
            
            # Extract punkt IDs first
            punkt_ids = self.extract_punkt_ids_from_url()
            print(f"Extracted punkt IDs from URL: {punkt_ids}")
            
            # Get coordinates for all punkt IDs and try to fetch if missing
            coordinates_data = {}
            for punkt_id in punkt_ids:
                lat, lon = self.get_coordinates(punkt_id)
                if not lat or not lon:
                    # Try to fetch from website
                    lat, lon = self.fetch_coordinate_from_trafikverket(punkt_id)
                    if lat and lon:
                        self.coordinate_cache[punkt_id] = (lat, lon)
                        print(f"  Found coordinates for {punkt_id}: {lat}, {lon}")
                
                coordinates_data[punkt_id] = (lat, lon)
            
            # Concatenate all dataframes into one
            combined_df = pd.concat(self.data, ignore_index=True)
            
            # Remove numeric column names and convert to proper column headers
            # If columns are integers (0, 1, 2, etc.), replace with generic Column_N
            if all(isinstance(col, int) for col in combined_df.columns):
                combined_df.columns = [f"Column_{i+1}" for i in range(len(combined_df.columns))]
            
            # Save the updated cache
            self.save_coordinate_cache()
            
            # Load and apply translations
            translations = self.load_translations()
            if translations:
                print("Applying translations...")
                combined_df = self.apply_translations(combined_df, translations)
            
            # Save to CSV file with comma separator and no header
            combined_df.to_csv(filepath, sep=',', index=False, header=False, encoding='utf-8')
            
            full_filepath = os.path.abspath(filepath)
            print(f"Data successfully saved to: {full_filepath}")
            print(f"  Total rows: {len(combined_df)}")
            print(f"  Format: CSV (comma-separated values)")
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self, output_file=None):
        """Run the complete scraping workflow"""
        try:
            self.setup_driver()
            self.navigate_to_page()
            
            # Get all measurement occasions
            occasions = self.get_measurement_occasions()
            
            if not occasions:
                print("No measurement occasions found")
                return
            
            # Iterate through each measurement occasion
            for idx, (value, text) in enumerate(occasions):
                # Check if row limit has been reached
                if rowCount > 0 and self.total_rows_extracted >= rowCount:
                    print(f"\nRow limit of {rowCount} reached. Stopping processing of measurement occasions.")
                    break
                
                print(f"\n{'='*60}")
                print(f"Processing {idx + 1}/{len(occasions)}: {text}")
                print(f"{'='*60}")
                
                # Select the measurement occasion
                if not self.select_measurement_occasion(value):
                    print(f"Skipping {text} - could not select")
                    continue
                
                # Check all checkboxes
                self.check_all_checkboxes()
                
                # Select table format
                self.select_table_format()
                
                # Click start button
                self.click_start_button()
                
                # Extract data from popup and insert into database
                self.handle_popup_window()
            
            # Print summary
            print(f"\n{'='*60}")
            print(f"Scraping completed successfully!")
            print(f"Total rows inserted into database: {self.total_rows_extracted}")
            print(f"{'='*60}")
                
        except Exception as e:
            print(f"Fatal error during scraping: {e}")
        finally:
            # Close database connection
            if self.db_cursor:
                self.db_cursor.close()
            if self.db_connection:
                self.db_connection.close()
            
            # Close browser
            if self.driver:
                print("Closing browser...")
                time.sleep(2)
                self.driver.quit()



def main():
    """Main entry point"""
    import sys
    import argparse
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print_system_info()
    print()
    
    parser = argparse.ArgumentParser(
        description='Extract data from Trafikverket website and save to Excel'
    )
    
    parser.add_argument(
        '-i', '--input',
        default='input_url.txt',
        help='Input file containing URLs (one per line). Default: input_url.txt'
    )
    
    parser.add_argument(
        '-u', '--url',
        default=None,
        help='Single URL to scrape (overrides input file if provided)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output Excel file path (default: trafikverket_data_<url_hash>.xlsx)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (faster, no UI)'
    )
    
    args = parser.parse_args()
    
    urls_to_process = []
    
    # If URL is provided as argument, use only that
    if args.url:
        urls_to_process = [args.url]
    else:
        # Try to read from input file
        input_file = args.input
        if os.path.exists(input_file):
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                    if urls:
                        urls_to_process = urls
                        print(f"Loaded {len(urls)} URL(s) from {input_file}")
                    else:
                        print(f"Error: {input_file} is empty or contains only comments")
                        sys.exit(1)
            except Exception as e:
                print(f"Error reading {input_file}: {e}")
                sys.exit(1)
        else:
            print(f"Error: {input_file} not found")
            print("Please create input_url.txt with one URL per line, or use -u to specify a URL")
            sys.exit(1)
    
    if not urls_to_process:
        print("Error: No URLs to process")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"Processing {len(urls_to_process)} URL(s)")
    print(f"{'='*70}\n")
    
    # Process each URL
    for url_idx, url in enumerate(urls_to_process, 1):
        print(f"\n{'='*70}")
        print(f"URL {url_idx}/{len(urls_to_process)}")
        print(f"{'='*70}")
        print(f"URL: {url}")
        
        # Generate output filename based on URL hash if not specified
        if args.output:
            output_file = args.output if len(urls_to_process) == 1 else f"{args.output.replace('.xlsx', '')}_{url_idx}.xlsx"
        else:
            # Create a hash-based filename for each URL
            import hashlib
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            output_file = f"trafikverket_data_{url_hash}.xlsx"
        
        print(f"Output file: {output_file}\n")
        
        try:
            scraper = TrafikverketScraper(url, headless=args.headless)
            scraper.run(output_file=output_file)
        except Exception as e:
            print(f"Error processing URL {url_idx}: {e}")
            continue
    
    print(f"\n{'='*70}")
    print("All URLs processed successfully!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
