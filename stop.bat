@echo off
echo Stopping and removing services...
docker-compose down -v
if %errorlevel% neq 0 (
    echo Failed to stop services.
    exit /b %errorlevel%
)
echo Services stopped and volumes removed.