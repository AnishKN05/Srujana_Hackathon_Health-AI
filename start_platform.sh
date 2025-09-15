#!/bin/bash
echo "Starting Enhanced Health AI Platform..."
echo

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python3 is not installed"
    exit 1
fi

echo
echo "Installing/updating requirements..."
pip3 install -r requirements.txt

echo
echo "Training ML models (if needed)..."
python3 train_models.py --all

echo
echo "Starting the platform..."
python3 start_platform.py
