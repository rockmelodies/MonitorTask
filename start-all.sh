#!/bin/bash
# Complete Startup Script (Backend + Frontend)

echo "===================================="
echo "  MonitorTask Complete Setup"
echo "===================================="
echo ""

# Step 1: Build Frontend
echo "[Step 1/2] Building Frontend..."
echo ""
bash build-frontend.sh
if [ $? -ne 0 ]; then
    echo "[ERROR] Frontend build failed"
    exit 1
fi

echo ""
echo "===================================="
echo ""

# Step 2: Start Backend
echo "[Step 2/2] Starting Backend..."
echo ""
bash start.sh
