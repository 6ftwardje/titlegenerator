#!/bin/bash

echo "🚀 Cryptoriez Shorts Helper Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is niet geïnstalleerd. Installeer eerst Python 3.10+"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python versie $python_version is te oud. Je hebt minimaal Python $required_version nodig."
    exit 1
fi

echo "✅ Python $python_version gevonden"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is niet geïnstalleerd. Installeer het met: brew install ffmpeg"
    echo "   Of download van: https://ffmpeg.org/download.html"
    read -p "Doorgaan zonder FFmpeg? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg gevonden"
fi

# Create virtual environment
echo "📦 Virtual environment aanmaken..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Virtual environment activeren..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Pip upgraden..."
pip install --upgrade pip

# Install requirements
echo "📚 Dependencies installeren..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 .env bestand aanmaken..."
    cp env.example .env
    echo "⚠️  Bewerk .env en voeg je OpenAI API key toe!"
else
    echo "✅ .env bestand bestaat al"
fi

echo ""
echo "🎉 Setup voltooid!"
echo ""
echo "Volgende stappen:"
echo "1. Bewerk .env en voeg je OpenAI API key toe"
echo "2. Activeer de virtual environment: source venv/bin/activate"
echo "3. Start de app: streamlit run app.py"
echo ""
echo "📖 Bekijk README.md voor meer informatie"

