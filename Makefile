.PHONY: help install run lint format test clean

# Detectar si estamos en un entorno virtual activado o necesitamos usar 'uv run'
UV_RUN := uv run

help:  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias del proyecto usando uv
	uv sync

run: ## Ejecuta el servidor de desarrollo
	$(UV_RUN) uvicorn apps.web.app:app --reload --host 0.0.0.0 --port 8000

lint: ## Verifica el estilo de código con ruff
	$(UV_RUN) ruff check .

format: ## Formatea el código con ruff
	$(UV_RUN) ruff format .

test: ## Ejecuta las pruebas con pytest
	$(UV_RUN) pytest

clean: ## Limpia archivos temporales y cachés
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
