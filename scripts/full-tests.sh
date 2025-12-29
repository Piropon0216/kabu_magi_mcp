#!/usr/bin/env bash
set -euo pipefail

# Full test runner with timing output
echo "Running full test suite (poetry run pytest)"
START=$(date +%s)
poetry run pytest -q
END=$(date +%s)
ELAPSED=$((END-START))
echo "Full test suite completed in ${ELAPSED}s"
