.PHONY: help install run dev test clean setup

help: ## Toon deze help
	@echo "Cryptoriez Shorts Helper - Beschikbare commando's:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Installeer alle dependencies en setup de omgeving
	@echo "🚀 Setup starten..."
	@./setup.sh

install: ## Installeer alleen Python dependencies
	@echo "📚 Dependencies installeren..."
	pip install -r requirements.txt

install-dev: ## Installeer development dependencies
	@echo "🔧 Development dependencies installeren..."
	pip install -r requirements-dev.txt

run: ## Start de Streamlit app
	@echo "🎬 App starten..."
	streamlit run app.py

dev: ## Start de app in development mode
	@echo "🔧 Development mode starten..."
	streamlit run app.py --server.port 8502

test: ## Voer tests uit
	@echo "🧪 Tests uitvoeren..."
	pytest

clean: ## Ruim tijdelijke bestanden op
	@echo "🧹 Opschonen..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.tmp" -delete
	find . -type f -name "*.temp" -delete

format: ## Format code met Black
	@echo "🎨 Code formatteren..."
	black .

lint: ## Controleer code kwaliteit
	@echo "🔍 Code linten..."
	flake8 .

check: format lint ## Format en lint code

venv: ## Maak virtual environment aan
	@echo "📦 Virtual environment aanmaken..."
	python3 -m venv venv
	@echo "✅ Virtual environment aangemaakt. Activeer met: source venv/bin/activate"

update: ## Update alle dependencies
	@echo "⬆️  Dependencies updaten..."
	pip install --upgrade -r requirements.txt

docker-build: ## Build Docker image
	@echo "🐳 Docker image bouwen..."
	docker build -t cryptoriez-shorts-helper .

docker-run: ## Run Docker container
	@echo "🚀 Docker container starten..."
	docker run -p 8501:8501 -e OPENAI_API_KEY=$(OPENAI_API_KEY) cryptoriez-shorts-helper

