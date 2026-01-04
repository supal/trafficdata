"""
Enhanced CLI for Trafikverket Data Extraction
Provides a command-line interface with additional options
"""

import argparse
import sys
from scraper import TrafikverketScraper
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description='Extract data from Trafikverket website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python cli.py
  
  # Specify custom output file
  python cli.py -o custom_output.csv
  
  # Use custom URL
  python cli.py -u "https://vtf.trafikverket.se/..." -o data.csv
  
  # Run in headless mode (background)
  python cli.py --headless
        """
    )
    
    parser.add_argument(
        '-u', '--url',
        default='https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?punktnrlista=13520237%2c13520237%2c13520505&laenkrollista=2%2c3%2c1',
        help='URL of the Trafikverket page to scrape'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output file path (default: trafikverket_data_<timestamp>.csv)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (background)'
    )
    
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Timeout in seconds for waiting for elements (default: 10)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Trafikverket Data Extractor")
    print("=" * 60)
    print(f"URL: {args.url}")
    print(f"Output: {args.output or 'trafikverket_data_<timestamp>.csv'}")
    print(f"Headless mode: {'Yes' if args.headless else 'No'}")
    print("=" * 60)
    print()
    
    try:
        scraper = TrafikverketScraper(args.url)
        scraper.run(output_file=args.output)
        print()
        print("=" * 60)
        print("Extraction completed successfully!")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
