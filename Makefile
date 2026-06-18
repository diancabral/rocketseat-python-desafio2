.PHONY: help install run flask-shell db-up db-down db-logs clean

.DEFAULT_GOAL := help

VENV := .venv
PY := $(VENV)/bin/python
ACTIVATE := $(VENV)/bin/activate

help:
	@echo "Available commands:"
	@echo "  make install      - install dependencies (uv sync into $(VENV))"
	@echo "  make run          - activate $(VENV) and run the API (creates $(VENV) and installs deps if needed)"
	@echo "  make flask-shell  - activate $(VENV) and run Flask shell (same bootstrap as run)"
	@echo "  make db-up        - start MySQL"
	@echo "  make db-down      - stop MySQL"
	@echo "  make db-logs      - follow MySQL logs"
	@echo "  make clean        - remove __pycache__ directories and .pyc files"

install:
	uv sync

run:
	@if [ -x "$(PY)" ]; then \
		echo "Using virtual environment $(VENV)"; \
		. "$(ACTIVATE)" && PYTHONPATH=src python src/app.py; \
	else \
		echo "Creating $(VENV) and installing dependencies..."; \
		uv venv "$(VENV)" && uv sync && . "$(ACTIVATE)" && PYTHONPATH=src python src/app.py; \
	fi

flask-shell:
	@if [ -x "$(PY)" ]; then \
		echo "Using virtual environment $(VENV)"; \
		. "$(ACTIVATE)" && export PYTHONPATH=src FLASK_APP=app && flask shell; \
	else \
		echo "Creating $(VENV) and installing dependencies..."; \
		uv venv "$(VENV)" && uv sync && . "$(ACTIVATE)" && export PYTHONPATH=src FLASK_APP=app && flask shell; \
	fi

db-up:
	docker-compose up -d

db-down:
	docker-compose down

db-logs:
	docker-compose logs -f db

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
