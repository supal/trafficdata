#!/usr/bin/env python3
"""
Verification script for Python 3.9.6 compatibility
Tests all components and verifies the setup is correct
"""

import sys
import os

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("PYTHON VERSION CHECK")
    
    version_info = sys.version_info
    version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    print(f"Current Python: {version_string}")
    print(f"Version Info: {sys.version}")
    print(f"Executable: {sys.executable}")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 9):
        print("\n❌ FAILED: Python 3.9 or higher required!")
        return False
    
    print("\n✅ PASSED: Python version is compatible")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("DEPENDENCY CHECK")
    
    required_packages = {
        'selenium': (4, 0, 0),
        'pandas': (1, 3, 0),
        'openpyxl': (3, 0, 0),
        'webdriver_manager': (3, 8, 0),
    }
    
    all_passed = True
    
    for package, min_version in required_packages.items():
        try:
            mod = __import__(package)
            version_string = getattr(mod, '__version__', 'unknown')
            
            # Try to parse version
            if version_string != 'unknown':
                parts = version_string.split('.')
                version_tuple = tuple(int(p) for p in parts[:3] if p.isdigit())
                
                if version_tuple >= min_version:
                    status = "✅ OK"
                else:
                    status = "⚠️  WARN"
                    all_passed = False
            else:
                status = "✅ OK"
            
            print(f"{package:20s} - {version_string:10s} {status}")
        except ImportError:
            print(f"{package:20s} - NOT INSTALLED ❌")
            all_passed = False
    
    if all_passed:
        print("\n✅ PASSED: All dependencies are installed")
    else:
        print("\n⚠️  WARNING: Some dependencies may have version issues")
        print("Run: pip install -r requirements-py39.txt")
    
    return all_passed

def check_files():
    """Check if all required files exist"""
    print_header("FILE STRUCTURE CHECK")
    
    required_files = [
        'scraper.py',
        'cli.py',
        'config.py',
        'compatibility.py',
        'requirements.txt',
        'requirements-py39.txt',
        'README.md',
    ]
    
    all_exist = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - MISSING")
            all_exist = False
    
    if all_exist:
        print("\n✅ PASSED: All required files present")
    else:
        print("\n❌ FAILED: Some files are missing")
    
    return all_exist

def check_imports():
    """Check if modules can be imported"""
    print_header("IMPORT CHECK")
    
    modules = ['scraper', 'cli', 'config', 'compatibility']
    all_imported = True
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name} - {str(e)}")
            all_imported = False
    
    if all_imported:
        print("\n✅ PASSED: All modules can be imported")
    else:
        print("\n❌ FAILED: Some modules failed to import")
    
    return all_imported

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  TRAFIKVERKET DATA EXTRACTOR - SETUP VERIFICATION")
    print("  Python 3.9.6+ Compatibility Check")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_files),
        ("Module Imports", check_imports),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {str(e)}")
            results[name] = False
    
    # Final summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:30s} {status}")
    
    print()
    
    if all_passed:
        print("✅ ALL CHECKS PASSED! Setup is ready to use.")
        print("\nYou can now run:")
        print("  python scraper.py")
        print("  python cli.py --help")
        return 0
    else:
        print("❌ SETUP ISSUES DETECTED")
        print("\nTo fix:")
        print("  1. Install Python 3.9+: brew install python@3.9")
        print("  2. Create venv: python3.9 -m venv .venv")
        print("  3. Activate: source .venv/bin/activate")
        print("  4. Install deps: pip install -r requirements-py39.txt")
        print("  5. Verify: python verify_setup.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
