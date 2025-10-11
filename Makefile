.PHONY: setup run clean format lint quality

setup:
	uv sync --all-extras

run:
	uv run python src/main.py

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	uv run ruff format src/
	uv run ruff check --fix src/

lint:
	uv run ruff check src/

quality: format lint
	@echo "✅ Code quality checks passed!"

