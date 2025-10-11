.PHONY: setup run clean format lint typecheck test test-cov quality

setup:
	uv sync --all-extras

run:
	uv run python src/main.py

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

lint:
	uv run ruff check src/ tests/

typecheck:
	cd src && uv run mypy .

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=src --cov-report=term-missing

quality: format lint typecheck test
	@echo "✅ All code quality checks passed!"

