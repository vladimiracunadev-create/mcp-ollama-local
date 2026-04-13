#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT/.venv/bin/python"
OUTPUT_FILE="${1:-$ROOT/artifacts/sbom.cdx.json}"
UV_CACHE_DIR="${TMPDIR:-/tmp}/uv-cache"
REQ_FILE="$(mktemp "${TMPDIR:-/tmp}/mcp-ollama-local-sbom.XXXXXX.txt")"

cleanup() {
  rm -f "$REQ_FILE"
}
trap cleanup EXIT

if [ ! -x "$PYTHON_BIN" ]; then
  echo "error: missing project virtualenv. Run 'make install' first." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

UV_CACHE_DIR="$UV_CACHE_DIR" uv export --frozen --format requirements-txt --all-groups > "$REQ_FILE"

UV_CACHE_DIR="$UV_CACHE_DIR" uv tool run --from cyclonedx-bom cyclonedx-py requirements \
  --pyproject "$ROOT/pyproject.toml" \
  --output-reproducible \
  --of JSON \
  -o "$OUTPUT_FILE" \
  "$REQ_FILE"

echo "SBOM written to $OUTPUT_FILE"
