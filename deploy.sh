#!/bin/bash

echo "🚀 Cryptoriez Shorts Helper - Production Deployment"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is niet geïnstalleerd. Installeer eerst Docker Desktop."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is niet geïnstalleerd. Installeer eerst Docker Compose."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env bestand niet gevonden!"
    echo "📝 Kopieer env.example naar .env en voeg je OpenAI API key toe:"
    echo "   cp env.example .env"
    echo "   # Bewerk .env en voeg je API key toe"
    exit 1
fi

# Build and start the application
echo "🐳 Docker image bouwen..."
docker-compose build

echo "🚀 Applicatie starten..."
docker-compose up -d

echo "✅ Applicatie gestart!"
echo "🌐 Beschikbaar op: http://localhost:8501"
echo ""
echo "📊 Status bekijken: docker-compose ps"
echo "🛑 Stoppen: docker-compose down"
echo "📝 Logs bekijken: docker-compose logs -f"
