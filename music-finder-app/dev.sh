#!/bin/bash

# Start the Next.js frontend
echo "Starting Next.js frontend..."
npm run dev &
FRONTEND_PID=$!

# Activate Python virtual environment and start the backend
echo "Starting Python backend..."
source venv/bin/activate
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Function to handle script termination
function cleanup {
  echo "Shutting down services..."
  kill $FRONTEND_PID
  kill $BACKEND_PID
  exit
}

# Set up trap to catch termination signal
trap cleanup SIGINT

# Keep script running
echo "Development environment is running. Press Ctrl+C to stop."
wait 