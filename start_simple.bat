@echo off
echo 🏥 Starting Simple Health AI Platform...
echo 📍 Backend will be available at: http://localhost:5000
echo 🌐 Frontend will be available at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo --------------------------------------------------

cd simple_backend
pip install -r requirements.txt
python app.py

pause
