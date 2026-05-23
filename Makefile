.PHONY: install run lint format clean test help

.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	python3 -m pip install -e .

install-dev:  ## Install with dev dependencies
	python3 -m pip install -e ".[dev]"

run:  ## Run the book fetcher (must be installed)
	book-fetcher

lint:  ## Lint with ruff
	ruff check src tests

lint-fix:  ## Lint and auto-fix with ruff
	ruff check --fix src tests

format:  ## Format code with black and isort (or ruff format)
	ruff format src tests
	black src tests
	isort src tests

typecheck:  ## Type check with mypy
	mypy src

test:  ## Run tests with pytest
	pytest

clear:  ## Clean generated files
	rm -rf data/* __pycache__ .mypy_cache .pytest_cache