PYTHON = python
PIP = pip
UVICORN = uvicorn
DOCKER_COMPOSE = docker compose

APP_FILE = app.main:app
ENV_FILE = .env

.PHONY: help install run clean docker-up docker-down docker-logs lint format


help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  install      Install dependencies"
	@echo "  run          Run the server locally (without Docker)"
	@echo "  up           Run the application in Docker (with rebuilding)"
	@echo "  down         Stop Docker containers"
	@echo "  logs         View Docker logs"
	@echo "  clean        Clean temporary files (__pycache__)"
	@echo "  lint         Check the code with linters (flake8)"
	@echo "  format       Format code (black)"

install:
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) $(APP_FILE) --reload --host 127.0.0.1 --port 8000 --env-file $(ENV_FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 app/

format:
	black app/

up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

test:
	$(PYTHON) -m pytest -v --cov=app --cov-report=term-missing

badge:
	$(PYTHON) -m pytest --cov=app
	coverage-badge -o coverage.svg -f	