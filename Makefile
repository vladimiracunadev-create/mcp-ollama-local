.PHONY: help install run lint format format-check test audit semgrep sbom trust-check smoke ci-local clean

VENV_BIN := .venv/bin

help:  ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias del proyecto usando uv
	uv sync --frozen

run: ## Ejecuta el servidor de desarrollo
	$(VENV_BIN)/uvicorn apps.web.app:app --reload --host 127.0.0.1 --port 8000

lint: ## Ejecuta el análisis estático local (ruff)
	$(VENV_BIN)/ruff check .

format: ## Formatea el código con ruff
	$(VENV_BIN)/ruff format .

format-check: ## Verifica que el código ya esté formateado
	$(VENV_BIN)/ruff format --check .

test: ## Ejecuta la suite de pruebas con pytest
	$(VENV_BIN)/pytest

smoke: ## Ejecuta solo smoke tests del backend/API
	$(VENV_BIN)/pytest -k "health or history or chat or auth"

audit: ## Ejecuta checks de seguridad reproducibles
	bash ./scripts/audit.sh

semgrep: ## Ejecuta reglas Semgrep propias del repositorio
	bash ./scripts/semgrep.sh

sbom: ## Genera un SBOM CycloneDX desde la .venv del proyecto
	bash ./scripts/sbom.sh

trust-check: ## Ejecuta la validación ampliada de confianza del repositorio
	bash ./scripts/trust_check.sh

ci-local: ## Replica los checks principales de CI en local
	bash ./scripts/ci_local.sh

clean: ## Limpia archivos temporales y cachés
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
