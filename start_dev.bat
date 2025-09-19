@echo off
echo 🌾 Starting Kerala Farming Assistant Development Environment
echo ============================================================
echo.

echo 📦 Installing Frontend Dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo 🐍 Setting up Backend Environment...
cd Backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Backend Server...
start "Backend Server" cmd /k "cd Backend && call venv\Scripts\activate && python run_server.py"

echo.
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Starting Frontend Development Server...
cd ..
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ✅ Development environment started!
echo.
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/api/docs
echo.
echo Press any key to exit...
pause > nul
