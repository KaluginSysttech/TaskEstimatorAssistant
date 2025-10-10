.PHONY: setup run clean

setup:
	uv sync

run:
	uv run python src/main.py

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

