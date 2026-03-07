#!/bin/bash

echo "Starting Weberdy stack..."

cd ~/Weberdy

echo "Activating environment..."
source weberdy-env/bin/activate

echo "Killing old uvicorn processes..."
pkill -f uvicorn

sleep 1

echo "Starting Weberdy Agent..."
uvicorn agent:app --host 0.0.0.0 --port 8001 --reload &

sleep 3

echo "Starting Frontend Server..."
python3 -m http.server 8090 &

sleep 2

echo "Testing agent status..."
curl http://127.0.0.1:8001/status

echo ""
echo "Weberdy UI:"
echo "http://127.0.0.1:8090/weberdy_interface/index.html"
