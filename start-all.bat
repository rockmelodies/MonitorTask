@echo off
REM Complete Startup Script (Backend + Frontend)

echo ====================================
echo   MonitorTask Complete Setup
echo ====================================
echo.

REM Step 1: Build Frontend
echo [Step 1/2] Building Frontend...
echo.
call build-frontend.bat
if %errorlevel% neq 0 (
    echo [ERROR] Frontend build failed
    pause
    exit /b 1
)

echo.
echo ====================================
echo.

REM Step 2: Start Backend
echo [Step 2/2] Starting Backend...
echo.
call start.bat

pause
