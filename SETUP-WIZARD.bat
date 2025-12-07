@echo off
REM Windows Setup Wizard for Trafikverket Data Extractor
REM Interactive installation with options

setlocal enabledelayedexpansion

cls
echo.
echo =========================================================================
echo   TRAFIKVERKET DATA EXTRACTOR - Windows Setup Wizard
echo =========================================================================
echo.
echo This wizard will guide you through setting up the scraper.
echo.
echo Requirements:
echo   - Python 3.9.6 or higher
echo   - Google Chrome browser
echo   - Internet connection
echo.
pause

REM Check Python
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo ERROR: Python not found!
    echo.
    echo Python is required but not installed or not in PATH.
    echo.
    echo Please install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box:
    echo   "Add Python to PATH"
    echo.
    echo After installing Python, restart this setup wizard.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found: %PYTHON_VERSION%
echo.

REM Check Chrome
echo Checking Chrome installation...
set CHROME_FOUND=0
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✓ Chrome found
    set CHROME_FOUND=1
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✓ Chrome found
    set CHROME_FOUND=1
)

if %CHROME_FOUND% equ 0 (
    cls
    echo.
    echo WARNING: Google Chrome not found!
    echo.
    echo Chrome is required for the scraper to work.
    echo.
    echo Install Chrome from: https://www.google.com/chrome/
    echo.
    set /p CHROME_PROMPT="Do you want to continue anyway? (Y/N): "
    if /i not "%CHROME_PROMPT%"=="Y" (
        exit /b 0
    )
) else (
    echo.
)

REM Check for existing installation
if exist ".venv" (
    cls
    echo.
    echo EXISTING INSTALLATION DETECTED
    echo.
    echo A virtual environment already exists.
    echo.
    set /p REINSTALL="Do you want to reinstall? (Y/N): "
    if /i not "%REINSTALL%"=="Y" (
        echo.
        echo Activating existing environment...
        call .venv\Scripts\activate.bat
        echo Ready to use!
        echo.
        echo Run: run.cmd scraper.py --headless
        echo.
        pause
        exit /b 0
    )
    echo Removing old installation...
    rmdir /s /q .venv >nul 2>&1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

REM Activate and upgrade pip
call .venv\Scripts\activate.bat
echo Upgrading pip...
python -m pip install --upgrade pip --quiet >nul 2>&1

REM Install dependencies
echo Installing dependencies (this may take a minute)...
echo.

python --version 2>&1 | find "3.9" >nul
if %errorlevel% equ 0 (
    echo Installing for Python 3.9...
    pip install -r requirements-py39.txt --quiet
) else (
    echo Installing standard requirements...
    pip install -r requirements.txt --quiet
)

if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies failed to install
    echo Trying alternative installation method...
    echo.
    pip install selenium pandas openpyxl webdriver-manager
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo ✓ Dependencies installed
echo.

REM Verification
echo Verifying installation...
python -c "import selenium, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some packages could not be verified
    echo But installation appears complete
) else (
    echo ✓ All packages verified
)

cls
echo.
echo =========================================================================
echo   INSTALLATION COMPLETE!
echo =========================================================================
echo.
echo Setup has completed successfully.
echo.
echo Next steps:
echo   1. Edit input_url.txt with URLs to process (one per line)
echo   2. Run: run.cmd scraper.py --headless
echo.
echo Example URLs:
echo   https://vtf.trafikverket.se/tmg101/AGS/tmg104bestaellinfouttag.aspx?...
echo.
echo For help and more options, see README.md
echo.
pause
endlocal
