# AI Knowledge YouTube Video Generator - Makefile

.PHONY: help install dev test lint format clean run setup docker

# Default target
help:
	@echo "AI Knowledge YouTube Video Generator"
	@echo "====================================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies"
	@echo "  dev        Install with dev dependencies"
	@echo "  setup      Run initial setup"
	@echo "  test       Run tests"
	@echo "  lint       Run linters"
	@echo "  format     Format code"
	@echo "  clean      Clean generated files"
	@echo "  run        Run sample generation"
	@echo "  docker     Build Docker image"

# Install dependencies
install:
	pip install -r requirements.txt

# Install with dev dependencies
dev:
	pip install -e ".[dev]"
	pre-commit install

# Run initial setup
setup:
	python scripts/setup.py

# Run tests
test:
	pytest tests/ -v --cov=src --cov-report=html

# Run tests (fast)
test-fast:
	pytest tests/ -v -x --tb=short

# Run linters
lint:
	flake8 src/ tests/
	mypy src/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Clean generated files
clean:
	python scripts/cleanup.py
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .mypy_cache

# Clean all including output
clean-all:
	python scripts/cleanup.py --clean-output --clean-backups

# Run sample generation
run:
	python scripts/generate_sample.py

# Generate video with topic
generate:
	python run.py generate "$(TOPIC)"

# Generate series
series:
	python run.py series "$(TOPIC)" --episodes $(EPISODES)

# Suggest topics
suggest:
	python run.py suggest --category $(CATEGORY) --count 10

# Validate configuration
validate:
	python scripts/validate_config.py

# Export analytics
analytics:
	python scripts/export_analytics.py --format html

# Build Docker image
docker:
	docker build -t ai-video-generator .

# Run with Docker
docker-run:
	docker-compose up -d

# Stop Docker
docker-stop:
	docker-compose down

# View logs
logs:
	tail -f logs/*.log

# Documentation
docs:
	mkdocs serve

# Build documentation
docs-build:
	mkdocs build
