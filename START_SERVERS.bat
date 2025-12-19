@echo off
echo ===================================
echo Starting Physical AI Textbook
echo ===================================

echo.
echo [1/3] Starting Backend API Server...
start "Backend API" cmd /k "cd C:\Users\Admin\hackathon\physical-ai-textbook\api && python main.py"

echo.
echo [2/3] Waiting 5 seconds for backend to initialize...
timeout /t 5

echo.
echo [3/3] Starting Frontend (Docusaurus)...
start "Frontend" cmd /k "cd C:\Users\Admin\hackathon\physical-ai-textbook && npm run start"

echo.
echo ===================================
echo Servers Started!
echo ===================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo ===================================
echo.
echo Press any key to close this window...
pause