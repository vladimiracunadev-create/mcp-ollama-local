#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

bash "$ROOT/scripts/ci_local.sh"
bash "$ROOT/scripts/semgrep.sh"
bash "$ROOT/scripts/sbom.sh"
