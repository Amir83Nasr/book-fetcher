.PHONY: help up down seed run test lint format clean

.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Start PostgreSQL and Redis
	docker compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 3
	@echo "Services are ready!"

down: ## Stop PostgreSQL and Redis
	docker compose down

seed: ## Create Tables
	python3 scripts/db.py seed

reset: ## Reset Database
	python3 scripts/db.py reset

small: ## Small adding data
	python3 scripts/db.py addsmall

large: ## Large adding data
	python3 scripts/db.py addlarge

status: ## Database status
	python3 scripts/db.py status

run: ## Start FastAPI server
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run tests
	pytest tests/ -v

locust-redis: ## Run load test redis (open http://localhost:8089)
	locust -f tests/locustfile_redis.py --host=http://localhost:8000

locust-memory: ## Run load test nocache (open http://localhost:8089)
	locust -f tests/locustfile_memory.py --host=http://localhost:8000

locust-nocache: ## Run load test nocache (open http://localhost:8089)
	locust -f tests/locustfile_nocache.py --host=http://localhost:8000

lint: ## Lint code
	ruff check --fix app/ tests/

format: ## Format code
	ruff format app/ tests/
	isort app/ tests/

clean: ## Clean up
	docker compose down -v
	rm -rf __pycache__ .pytest_cache .mypy_cache