@echo off
title RealityCheck AI Docker Stopper
echo ===================================================
echo   Stopping RealityCheck AI Docker Container...
echo ===================================================
echo.

cd /d "%~dp0"

:: Shut down compose container
docker-compose down

echo.
echo ===================================================
echo   SUCCESS: Docker container stopped successfully!
echo ===================================================
echo.
timeout /t 3
