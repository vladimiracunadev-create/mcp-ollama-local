#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RULES_DIR="$ROOT/semgrep-rules"
UV_CACHE_DIR="${TMPDIR:-/tmp}/uv-cache"
FORMAT="${1:-text}"
OUTPUT_FILE="${2:-}"
RULE_FILES=()
while IFS= read -r rule; do
  RULE_FILES+=("$rule")
done < <(find "$RULES_DIR" -name '*.yml' ! -name '._*' -print | sort)

if [ ! -d "$RULES_DIR" ]; then
  echo "error: missing Semgrep rules directory: $RULES_DIR" >&2
  exit 1
fi
if [ "${#RULE_FILES[@]}" -eq 0 ]; then
  echo "error: no Semgrep rule files found in $RULES_DIR" >&2
  exit 1
fi

echo "==> Validating Semgrep rules"
VALIDATE_CMD=(uv tool run --from semgrep semgrep scan --validate)
for rule in "${RULE_FILES[@]}"; do
  VALIDATE_CMD+=(--config "$rule")
done
UV_CACHE_DIR="$UV_CACHE_DIR" "${VALIDATE_CMD[@]}"

SCAN_CMD=(
  uv tool run --from semgrep semgrep scan
  --error
  --metrics off
  --disable-version-check
  --exclude ".venv"
  --exclude "artifacts"
  --exclude "data"
  "$ROOT/apps"
  "$ROOT/host"
  "$ROOT/mcp_server"
  "$ROOT/main.py"
)
for rule in "${RULE_FILES[@]}"; do
  SCAN_CMD+=(--config "$rule")
done

echo
echo "==> Running Semgrep"
if [ "$FORMAT" = "sarif" ]; then
  if [ -z "$OUTPUT_FILE" ]; then
    echo "error: sarif output requires a destination file" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$OUTPUT_FILE")"
  UV_CACHE_DIR="$UV_CACHE_DIR" "${SCAN_CMD[@]}" --sarif --output "$OUTPUT_FILE"
else
  UV_CACHE_DIR="$UV_CACHE_DIR" "${SCAN_CMD[@]}"
fi
