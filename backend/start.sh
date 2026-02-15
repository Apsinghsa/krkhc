#!/bin/bash

# AEGIS Backend Startup Script
# Uses uv for Python package management

cd "$(dirname "$0")"

echo "🚀 Starting AEGIS Backend..."
echo ""

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with uv..."
    uv sync
fi

echo "🔧 Checking dependencies..."
uv sync

echo ""
echo "🌐 Starting FastAPI server..."
echo "📚 API Docs: http://localhost:8000/docs"
echo "📖 ReDoc:    http://localhost:8000/redoc"
echo ""

# Run with uv
uv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000