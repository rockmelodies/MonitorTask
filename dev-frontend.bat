@echo off
REM Frontend Development Server

echo ====================================
echo   Frontend Dev Server (Port 3000)
echo ====================================
echo.

cd frontend

echo Checking dependencies...
if not exist "node_modules\@vueuse" (
    echo Installing missing dependencies...
    npm install
)

echo.
echo Starting Vite dev server...
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo.
echo Features:
echo - Click collapse icon to fold/unfold sidebar
echo - Click sun/moon icon to switch theme
echo.

npm run dev

pause
