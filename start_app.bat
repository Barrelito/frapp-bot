@echo off
echo Starting FRAPP Support Bot...

:: Start Backend in a new window
echo Starting Backend (Python)...
start "FRAPP Backend" cmd /k "cd backend && venv\Scripts\uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend in a new window
echo Starting Frontend (Next.js)...
start "FRAPP Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   Servers are starting!
echo   Wait approx 10-20 seconds.
echo   Then open browser at: http://localhost:3000
echo ===================================================
pause
