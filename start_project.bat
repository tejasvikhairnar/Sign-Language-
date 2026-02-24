@echo off
title SLR Project Launcher
echo ===================================================
echo       SLR Project - Sign Language Recognition
echo ===================================================

echo.
echo [1/3] Checking environment...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python is not found in PATH.
    pause
    exit /b
)
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: npm is not found in PATH.
    pause
    exit /b
)

echo.
echo [2/3] Starting Backend Server...
start "SLR Backend (Flask)" cmd /k "python final_backend.py"

echo.
echo [3/3] Starting Frontend Server...
cd frontend
start "SLR Frontend (Next.js)" cmd /k "npm run dev"

echo.
echo ===================================================
echo       Application Launched Successfully!
echo ===================================================
echo Backend: http://127.0.0.1:5000
echo Frontend: http://localhost:3000
echo.
echo Opening Dashboard in 5 seconds...
timeout /t 5 >nul
start http://localhost:3000/dashboard
