#!/bin/bash

echo "🌾 Starting Kerala Farming Assistant Development Environment"
echo "============================================================"
echo

echo "📦 Installing Frontend Dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

echo
echo "🐍 Setting up Backend Environment..."
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

echo
echo "🚀 Starting Backend Server..."
gnome-terminal -- bash -c "cd Backend && source venv/bin/activate && python run_server.py; exec bash" &
BACKEND_PID=$!

echo
echo "⏳ Waiting for backend to start..."
sleep 5

echo
echo "🌐 Starting Frontend Development Server..."
cd ..
npm run dev &
FRONTEND_PID=$!

echo
echo "✅ Development environment started!"
echo
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
