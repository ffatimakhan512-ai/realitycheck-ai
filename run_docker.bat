@echo off
title RealityCheck AI Docker Launcher
echo ===================================================
echo   Starting RealityCheck AI via Docker...
echo ===================================================
echo.

:: Change directory to the folder containing this script
cd /d "%~dp0"

:: Verify Docker is installed and running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in your system PATH.
    echo Please make sure Docker Desktop is installed and running.
    echo.
    pause
    exit /b
)

:: Launch browser in a background timer
echo [1/2] Launching browser timer...
start "" /b cmd /c "timeout /t 5 /nobreak > nul && start http://127.0.0.1:8000/"

:: Build and start the container in the foreground
echo [2/2] Starting Docker container...
echo.
docker-compose up --build

echo.
echo ===================================================
echo   Docker container stopped or failed to build/start.
echo ===================================================
echo.
pause
