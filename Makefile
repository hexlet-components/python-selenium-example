install:
	uv sync

run-basic-selenium-demo:
	uv run examples/basic_selenium_demo.py

run-corner-cases-demo:
	uv run examples/selenium_corner_cases_demo.py

test:
	uv run pytest

lint:
	uv run ruff check

check: test lint

build:
	uv build

.PHONY: install test lint selfcheck check build
