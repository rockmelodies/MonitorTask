@echo off
REM Frontend Development Server

echo ====================================
echo   Frontend Dev Server (Port 3000)
echo ====================================
echo.

cd frontend

echo Starting Vite dev server...
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo.

npm run dev

pause
