@echo off
REM Build Frontend Script

echo ====================================
echo   Building Frontend
echo ====================================
echo.

REM Check Node.js
echo [1/3] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js 16.0+ from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js installed

REM Enter frontend directory
echo.
echo [2/3] Installing dependencies...
cd frontend
if %errorlevel% neq 0 (
    echo [ERROR] Frontend directory not found!
    pause
    exit /b 1
)

REM Install dependencies
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Build
echo.
echo [3/3] Building frontend...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)
echo [OK] Build completed

echo.
echo ====================================
echo   Build Success!
echo ====================================
echo.
echo Output directory: ../static
echo You can now start the backend server
echo.

cd ..
pause
