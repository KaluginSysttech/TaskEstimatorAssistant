.PHONY: setup run clean format lint typecheck test test-cov quality run-stats-api test-stats-api open-stats-docs

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

# Statistics API commands
run-stats-api:
	@echo "Starting Statistics API on http://localhost:8001"
	@echo "Swagger UI: http://localhost:8001/docs"
	@echo "ReDoc: http://localhost:8001/redoc"
	uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload

test-stats-api:
	@echo "Testing Statistics API endpoints..."
	@echo "\n=== Testing /health endpoint ==="
	@curl -s "http://localhost:8001/health" | python -m json.tool
	@echo "\n=== Testing /api/v1/stats?period=day ==="
	@curl -s "http://localhost:8001/api/v1/stats?period=day" | python -m json.tool
	@echo "\n=== Testing /api/v1/stats?period=week ==="
	@curl -s "http://localhost:8001/api/v1/stats?period=week" | python -m json.tool
	@echo "\n=== Testing /api/v1/stats?period=month ==="
	@curl -s "http://localhost:8001/api/v1/stats?period=month" | python -m json.tool

open-stats-docs:
	@echo "Opening Statistics API documentation..."
	@start http://localhost:8001/docs

