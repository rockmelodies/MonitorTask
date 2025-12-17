@echo off
REM MonitorTask Startup Script
REM Set UTF-8 encoding
chcp 65001 >nul 2>&1

echo ====================================
echo   MonitorTask Startup
echo ====================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python installed

REM Check virtual environment
echo.
echo [2/5] Checking virtual environment...
if not exist ".venv" (
    if not exist "venv" (
        echo Creating virtual environment...
        python -m venv .venv
        echo [OK] Virtual environment created
    ) else (
        echo [OK] Using existing venv folder
    )
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Cannot find activate script
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo [4/5] Installing dependencies...
echo This may take a few minutes...
pip install -q -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    echo Trying without mirror...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        pause
        exit /b 1
    )
)
echo [OK] Dependencies installed

REM Check config
echo.
echo [5/5] Checking configuration...
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env >nul
    echo [WARNING] Please edit .env file for configuration
)
echo [OK] Configuration ready

REM Start service
echo.
echo ====================================
echo   Starting MonitorTask Service
echo ====================================
echo.
echo Backend API: http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo ====================================
echo.

python run.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Service failed to start
    echo Check the error message above
    pause
)

pause
