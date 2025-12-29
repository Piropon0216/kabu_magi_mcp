#!/usr/bin/env bash
set -euo pipefail

# Entrypoint for containerized GitHub Actions Runner
# Expects environment variables:
#   RUNNER_REPO_URL (e.g. https://github.com/OWNER/REPO)
#   RUNNER_TOKEN (registration token from GitHub)
#   RUNNER_NAME (optional, defaults to container hostname)
#   RUNNER_LABELS (optional, comma separated)

RUNNER_REPO_URL=${RUNNER_REPO_URL:-}
RUNNER_TOKEN=${RUNNER_TOKEN:-}
RUNNER_NAME=${RUNNER_NAME:-$(hostname)}
RUNNER_LABELS=${RUNNER_LABELS:-self-hosted,docker,linux}

if [ -z "$RUNNER_REPO_URL" ] || [ -z "$RUNNER_TOKEN" ]; then
  echo "Missing RUNNER_REPO_URL or RUNNER_TOKEN environment variable"
  echo "Set RUNNER_REPO_URL and RUNNER_TOKEN when starting the container."
  exit 2
fi

cd /actions-runner

if [ ! -f ./config.sh ]; then
  echo "Downloading GitHub Actions runner..."
  LATEST_JSON=$(curl -s https://api.github.com/repos/actions/runner/releases/latest)
  DOWNLOAD_URL=$(echo "$LATEST_JSON" | jq -r '.assets[] | select(.name|test("linux.*x64|linux.*arm64|linux.*armv7")) | .browser_download_url' | head -n1)
  if [ -z "$DOWNLOAD_URL" ] || [ "$DOWNLOAD_URL" = "null" ]; then
    # fallback: pick first browser_download_url
    DOWNLOAD_URL=$(echo "$LATEST_JSON" | jq -r '.assets[0].browser_download_url')
  fi
  echo "Downloading: $DOWNLOAD_URL"
  curl -sL "$DOWNLOAD_URL" -o actions-runner.tar.gz
  tar xzf actions-runner.tar.gz
  rm -f actions-runner.tar.gz
fi

# Configure runner unattended (idempotent for clean containers)
./config.sh --unattended --url "$RUNNER_REPO_URL" --token "$RUNNER_TOKEN" --name "$RUNNER_NAME" --labels "$RUNNER_LABELS"

echo "Starting runner: $RUNNER_NAME"
exec ./run.sh
