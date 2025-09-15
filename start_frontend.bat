@echo off
echo 🏥 Starting Health AI Platform Frontend...
echo 📍 Frontend will be available at: http://localhost:3000
echo 🛑 Press Ctrl+C to stop the server
echo --------------------------------------------------

if not exist node_modules (
    echo 📦 Installing frontend dependencies...
    npm install
)

npm run dev

pause
