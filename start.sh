#!/bin/bash
# MonitorTask Startup Script

echo "===================================="
echo "  MonitorTask Startup"
echo "===================================="
echo ""

# Check Python
echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found"
    echo "Please install Python 3.8+"
    exit 1
fi
echo "[OK] Python installed"

# Check virtual environment
echo ""
echo "[2/5] Checking virtual environment..."
if [ ! -d ".venv" ]; then
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
        echo "[OK] Virtual environment created"
    else
        echo "[OK] Using existing venv folder"
    fi
else
    echo "[OK] Virtual environment exists"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "[ERROR] Cannot find activate script"
    exit 1
fi
echo "[OK] Virtual environment activated"

# Install dependencies
echo ""
echo "[4/5] Installing dependencies..."
echo "This may take a few minutes..."
pip install -q -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    echo "Trying without mirror..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi
echo "[OK] Dependencies installed"

# Check config
echo ""
echo "[5/5] Checking configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "[WARNING] Please edit .env file for configuration"
fi
echo "[OK] Configuration ready"

# Start service
echo ""
echo "===================================="
echo "  Starting MonitorTask Service"
echo "===================================="
echo ""
echo "Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo "===================================="
echo ""

python run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Service failed to start"
    echo "Check the error message above"
fi
