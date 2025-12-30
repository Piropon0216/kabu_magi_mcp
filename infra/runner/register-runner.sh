#!/usr/bin/env bash
set -euo pipefail

# Usage: sudo ./register-runner.sh <GITHUB_URL> <RUNNER_TOKEN> <RUNNER_NAME>
# Example: sudo ./register-runner.sh https://github.com/Piropon0216/kabu_magi_mcp <token> my-runner-01

GITHUB_URL=${1:-}
TOKEN=${2:-}
RUNNER_NAME=${3:-$(hostname)}
RUNNER_WORKDIR=/opt/actions-runner

if [ -z "$GITHUB_URL" ] || [ -z "$TOKEN" ]; then
  echo "Usage: sudo $0 <GITHUB_URL> <RUNNER_TOKEN> [RUNNER_NAME]"
  exit 2
fi

if [ $(id -u) -ne 0 ]; then
  echo "This script must be run as root (it installs the runner under $RUNNER_WORKDIR)." >&2
  exit 1
fi

mkdir -p "$RUNNER_WORKDIR"
cd "$RUNNER_WORKDIR"

ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
  PLATFORM=linux-x64
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
  PLATFORM=linux-arm64
else
  PLATFORM=linux-x64
fi

echo "Downloading GitHub Actions runner for $PLATFORM..."
LATEST=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | grep -m1 "browser_download_url" | cut -d '"' -f4)
TARBALL_URL=${LATEST}
echo "Using: $TARBALL_URL"
curl -sL "$TARBALL_URL" -o actions-runner.tar.gz
tar xzf actions-runner.tar.gz
rm -f actions-runner.tar.gz

useradd -m -s /bin/bash actions-runner || true
chown -R actions-runner:actions-runner "$RUNNER_WORKDIR"

sudo -u actions-runner bash -c "cd $RUNNER_WORKDIR && ./config.sh --unattended --url \"$GITHUB_URL\" --token \"$TOKEN\" --name \"$RUNNER_NAME\""

cat > /etc/systemd/system/actions-runner.service <<'EOF'
[Unit]
Description=GitHub Actions Runner
After=network.target

[Service]
Type=simple
User=actions-runner
WorkingDirectory=/opt/actions-runner
ExecStart=/opt/actions-runner/run.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now actions-runner.service

echo "Runner installed and service started. Check status: systemctl status actions-runner.service"
