#!/bin/bash
# Build Frontend Script

echo "===================================="
echo "  Building Frontend"
echo "===================================="
echo ""

# Check Node.js
echo "[1/3] Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found!"
    echo "Please install Node.js 16.0+ from https://nodejs.org/"
    exit 1
fi
echo "[OK] Node.js installed"

# Enter frontend directory
echo ""
echo "[2/3] Installing dependencies..."
cd frontend
if [ $? -ne 0 ]; then
    echo "[ERROR] Frontend directory not found!"
    exit 1
fi

# Install dependencies
npm install
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[OK] Dependencies installed"

# Build
echo ""
echo "[3/3] Building frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo "[ERROR] Build failed"
    exit 1
fi
echo "[OK] Build completed"

echo ""
echo "===================================="
echo "  Build Success!"
echo "===================================="
echo ""
echo "Output directory: ../static"
echo "You can now start the backend server"
echo ""

cd ..
