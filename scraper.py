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
        """Navigate to the target page"""
        print(f"Navigating to {self.url}...")
        self.driver.get(self.url)
        # Wait for the measurement occasion dropdown to be clickable (indicates page is loaded)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//select[@id] | //option"))
            )
            print("Page loaded successfully")
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
                
                # Extract table data from popup
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
        """Extract data from popup table"""
        try:
            print("Extracting data from popup...")
            
            # Find all tables in popup
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"  Found {len(tables)} table(s) in popup")
            
            if len(tables) == 0:
                print("  No tables found in popup, trying to find any data elements...")
                # Try to find any structured data
                return
            
            popup_data = []
            
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
                
                all_data = []
                
                for row in rows:
                    cells = row.find_elements(By.XPATH, "./td")
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        all_data.append(row_data)
                
                # If we have data, create DataFrame
                if all_data:
                    if headers:
                        df = pd.DataFrame(all_data, columns=headers)
                    else:
                        df = pd.DataFrame(all_data)
                    
                    self.data.append(df)
                    print(f"    Extracted {len(all_data)} data rows from popup table {table_idx + 1}")
                    
        except Exception as e:
            print(f"Error extracting popup table data: {e}")
    
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
                    df = pd.DataFrame(all_data)
                    self.data.append(df)
                    print(f"  Extracted {len(all_data)} data rows from table {table_idx + 1}")
            
            return True
        except TimeoutException:
            print("Error: Table did not appear within timeout period")
            return False
        except Exception as e:
            print(f"Error extracting table data: {e}")
            return False
    
    def save_to_excel(self, filename=None):
        """Save extracted data to Excel file - append all data to same sheet"""
        if not self.data:
            print("No data to save")
            return False
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trafikverket_data_{timestamp}.xlsx"
        
        try:
            # Concatenate all dataframes into one
            combined_df = pd.concat(self.data, ignore_index=True)
            
            # Save to single sheet
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                combined_df.to_excel(writer, sheet_name="Data", index=False)
            
            filepath = os.path.abspath(filename)
            print(f"Data successfully saved to: {filepath}")
            print(f"  Total rows: {len(combined_df)}")
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
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
                
                # Extract data from popup
                self.handle_popup_window()
            
            # Save all collected data to Excel
            if self.data:
                self.save_to_excel(output_file)
                print(f"\nScraping completed successfully! Extracted {len(self.data)} table(s)")
            else:
                print("\nNo data extracted")
                
        except Exception as e:
            print(f"Fatal error during scraping: {e}")
        finally:
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
                    urls = [line.strip() for line in f if line.strip()]
                    if urls:
                        urls_to_process = urls
                        print(f"Loaded {len(urls)} URL(s) from {input_file}")
                    else:
                        print(f"Error: {input_file} is empty")
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
