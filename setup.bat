@echo off
setlocal enabledelayedexpansion

REM Color codes
set RED=[31m
set GREEN=[32m
set YELLOW=[33m
set BLUE=[34m
set NC=[0m

cls
echo.
echo ============================================================
echo     Username Sniper - Setup ^& Installation Script
echo ============================================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check if pip is installed
echo.
echo [2/5] Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed!
    echo Please install pip or upgrade Python
    pause
    exit /b 1
)

echo [OK] pip found

REM Install requirements
echo.
echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] All dependencies installed successfully

REM Setup environment file
echo.
echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env >nul
    if errorlevel 1 (
        echo Error: Failed to create .env file
        pause
        exit /b 1
    )
    echo [OK] .env file created from template
    echo WARNING: Edit .env and add your Discord bot token!
) else (
    echo [OK] .env file already exists
)

REM Verify files
echo.
echo [5/5] Verifying installation...

set FILES_OK=true

if exist main.py (
    echo [OK] main.py found
) else (
    echo Error: main.py not found
    set FILES_OK=false
)

if exist discord_bot.py (
    echo [OK] discord_bot.py found
) else (
    echo Error: discord_bot.py not found
    set FILES_OK=false
)

if exist .env (
    echo [OK] .env file found
) else (
    echo Error: .env file not found
    set FILES_OK=false
)

echo.
echo ============================================================

if "%FILES_OK%"=="true" (
    echo.
    echo [SUCCESS] Setup complete!
    echo.
    echo Next steps:
    echo 1. Edit .env and add your Discord bot token:
    echo    notepad .env
    echo.
    echo 2. Run the CLI version (Terminal):
    echo    python main.py
    echo.
    echo 3. Or run the Discord bot:
    echo    python discord_bot.py
    echo.
    echo For help, see: QUICK_START.md or DISCORD_BOT_SETUP.md
) else (
    echo.
    echo [ERROR] Setup incomplete. Check the errors above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo.
pause
