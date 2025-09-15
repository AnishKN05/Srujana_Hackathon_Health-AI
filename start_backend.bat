@echo off
echo 🏥 Starting ML-based Health AI Platform Backend...
echo 📍 Backend will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🤖 Using trained ML models
echo 🛑 Press Ctrl+C to stop the server
echo --------------------------------------------------

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
