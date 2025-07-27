@echo off
echo Starting services...
docker-compose up --build -d
if %errorlevel% neq 0 (
    echo Failed to start services.
    exit /b %errorlevel%
)
echo Services are running.