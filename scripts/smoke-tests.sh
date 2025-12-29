#!/usr/bin/env bash
set -euo pipefail

# Quick smoke test script: run a small set of fast unit tests.
# Edit the TEST_FILES array to adjust which tests are considered 'smoke'.

TEST_FILES=(
  "tests/test_decision_models.py"
  "tests/test_foundry_tool_registry.py"
  "tests/test_melchior_agent.py"
)

echo "Running smoke tests: ${TEST_FILES[*]}"

for f in "${TEST_FILES[@]}"; do
  if [ -f "$f" ]; then
    poetry run pytest -q "$f"
  else
    echo "Warning: test file $f not found, skipping"
  fi
done

echo "Smoke tests passed."
