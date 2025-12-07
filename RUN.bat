@echo off
REM Quick Launcher for Trafikverket Data Extractor
REM Double-click this file to run the scraper with default settings

setlocal enabledelayedexpansion

REM Check if venv exists
if not exist ".venv" (
    echo.
    echo Virtual environment not found!
    echo.
    echo Please run INSTALL.bat or SETUP-WIZARD.bat first
    echo.
    pause
    exit /b 1
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Run scraper with headless mode
cls
echo.
echo Starting Trafikverket Data Extractor (Headless Mode)
echo.
echo Reading URLs from input_url.txt...
echo.

python scraper.py --headless

if errorlevel 1 (
    echo.
    echo An error occurred. Check input_url.txt and try again.
    echo.
)

pause
