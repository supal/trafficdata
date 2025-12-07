#!/usr/bin/env python3
"""
Test script to verify HTML response capture
"""
import os
from datetime import datetime

# Run scraper
print("Running scraper to capture HTML response...")
os.system('./run.sh scraper.py > /dev/null 2>&1')

# Check for HTML files
print("\nChecking for HTML response files...")
html_files = [f for f in os.listdir('.') if f.startswith('response_') and f.endswith('.html')]

if html_files:
    print(f"\n✅ Found {len(html_files)} HTML response file(s):")
    for html_file in sorted(html_files):
        size = os.path.getsize(html_file)
        print(f"   • {html_file} ({size:,} bytes)")
        
        # Show first 1000 characters
        print(f"\n   First 500 characters:")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"   {content[:500]}...")
            print(f"\n   Total file size: {len(content):,} characters")
else:
    print("❌ No HTML response files found")
    print("\nChecking for other output files...")
    files = [f for f in os.listdir('.') if f.endswith(('.html', '.xlsx'))]
    print(f"Found: {files}")
