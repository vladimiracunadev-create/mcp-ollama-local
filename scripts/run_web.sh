#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

# Carga .env si existe (exporta variables para el proceso)
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

PY="$PWD/.venv/bin/python"

unset PYTHONPATH
unset PYTHONHOME

"$PY" -m uvicorn apps.web.app:app --port 8000

