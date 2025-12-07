@echo off
REM Helper script to run the scraper with the correct virtual environment (Windows)
REM Place in your project root and run: run.cmd [command]

setlocal enabledelayedexpansion

set VENV_PATH=.venv\Scripts\activate.bat
set PROJECT_DIR=%~dp0

REM Check if virtual environment exists
if not exist "%VENV_PATH%" (
    echo ❌ Error: Virtual environment not found at %VENV_PATH%
    echo.
    echo To create it, run:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate.bat
    echo   pip install -r requirements-py39.txt
    exit /b 1
)

REM Activate virtual environment
call "%VENV_PATH%"

REM Run the command or default to help
if "%1"=="" (
    echo 🔍 Verifying setup...
    python verify_setup.py
    echo.
    echo ✅ Setup verified! Ready to scrape.
    echo.
    echo Usage examples:
    echo   run.cmd scraper.py
    echo   run.cmd cli.py --help
    echo   run.cmd cli.py -o output.xlsx
    echo   run.cmd verify_setup.py
) else (
    REM Run with provided arguments
    python %*
)

endlocal
