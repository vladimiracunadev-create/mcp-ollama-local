#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_BIN="$ROOT/.venv/bin"

if [ ! -x "$VENV_BIN/bandit" ] || [ ! -x "$VENV_BIN/python" ]; then
  echo "error: missing audit tools in .venv. Run 'make install' first." >&2
  exit 1
fi

echo "==> Bandit"
PY_FILES="$(find "$ROOT/apps" "$ROOT/host" "$ROOT/mcp_server" -name '*.py' ! -name '._*' -print)"
"$VENV_BIN/bandit" $PY_FILES "$ROOT/main.py" -c "$ROOT/pyproject.toml"

echo
echo "==> pip check"
"$VENV_BIN/python" -m pip check
