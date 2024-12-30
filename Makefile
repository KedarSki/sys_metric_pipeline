#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

.PHONY: poetry-install-deps
poetry-install-deps:
	poetry install --with dev

# Run Virtual Environment
.PHONY: fastapi-run
fastapi-run:
	uvicorn src.api.fast_api:app --host=0.0.0.0 --port=8000 --reload

# .PHONY: venv-run
# venv-run:
# 	source .venv/Scripts/activate

#* Linting
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=src tests/

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: black_check
black_check:
	poetry run black --diff --check .

.PHONY: pylint
pylint:
	poetry run pylint -j 4 src/

.PHONY: check-all
check-all: black_check pylint mypy test

# Docker container
.PHONY: docker-build
docker-build:
	docker build -t sys-metric-pipeline .

.PHONY: docker-run
docker-run:
	docker-compose up
