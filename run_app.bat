@echo off
title RealityCheck AI Launcher
echo ===================================================
echo   Starting RealityCheck AI - Fake News Analyzer...
echo ===================================================
echo.

:: Change directory to the folder containing this script
cd /d "%~dp0"

:: Verify that the virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv/
    echo Please make sure you are running this inside your project folder.
    echo.
    pause
    exit /b
)

:: Launch browser in a background timer
echo [1/2] Launching browser timer...
start "" /b cmd /c "timeout /t 3 /nobreak > nul && start http://127.0.0.1:8000/"

:: Start the Python FastAPI backend directly in this window
echo [2/2] Starting backend service...
echo.
.venv\Scripts\python -m backend.app

echo.
echo ===================================================
echo   Server has stopped or failed to start.
echo ===================================================
echo.
pause
