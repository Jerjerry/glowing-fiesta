@echo off
echo Starting Story Reader...

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not found. Please install Python 3.11 or newer.
    pause
    exit /b 1
)

:: Check if required packages are installed
python -c "import edge_tts" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

:: Run the application
python story_reader.py

if %ERRORLEVEL% neq 0 (
    echo An error occurred while running the application.
    pause
    exit /b 1
)
