@echo off
REM Windows Installer for Trafikverket Data Extractor
REM This script sets up the virtual environment and installs all dependencies

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  Trafikverket Data Extractor - Windows Installer
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9.6 or higher from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo [1/4] Checking Python version...
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %PYTHON_VERSION%
echo.

REM Check if Chrome is installed
echo [2/4] Checking for Google Chrome...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo Chrome found: C:\Program Files\Google\Chrome\Application\chrome.exe
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo Chrome found: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else (
    echo WARNING: Google Chrome not found
    echo Please install Chrome from: https://www.google.com/chrome/
    echo You can continue, but the scraper will not work without Chrome
    echo.
)
echo.

REM Create virtual environment
echo [3/4] Creating virtual environment...
if exist ".venv" (
    echo Virtual environment already exists at: .venv
    echo Skipping creation...
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment and install dependencies
echo [4/4] Installing Python dependencies...
echo.

REM Activate venv
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

REM Install dependencies
echo Installing required packages...
echo   - selenium
echo   - pandas
echo   - openpyxl
echo   - webdriver-manager
echo.

REM Try Python 3.9 specific requirements first
python --version 2>&1 | find "3.9" >nul
if %errorlevel% equ 0 (
    echo Detected Python 3.9 - installing from requirements-py39.txt
    pip install -r requirements-py39.txt --quiet
) else (
    pip install -r requirements.txt --quiet
)

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Trying manual installation...
    pip install selenium pandas openpyxl webdriver-manager
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

echo.
echo ========================================================================
echo  Installation Complete!
echo ========================================================================
echo.
echo You can now run the scraper using:
echo.
echo   run.cmd scraper.py --headless
echo.
echo To add URLs to process, edit input_url.txt
echo.
echo For more information, see README.md
echo.
pause
endlocal
