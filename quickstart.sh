#!/bin/bash

echo "🚀 Cryptoriez Shorts Helper - Quick Start"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env bestand niet gevonden!"
    echo "📝 Kopieer env.example naar .env en voeg je OpenAI API key toe:"
    echo "   cp env.example .env"
    echo "   # Bewerk .env en voeg je API key toe"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment niet gevonden. Maak het aan..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Virtual environment activeren..."
source venv/bin/activate

# Install/update requirements
echo "📚 Dependencies controleren..."
pip install -r requirements.txt

# Start the app
echo "🎬 App starten..."
echo "🌐 App opent op: http://localhost:8501"
echo "🛑 Stop met Ctrl+C"
echo ""

streamlit run app.py

