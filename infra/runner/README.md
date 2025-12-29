Self-hosted GitHub Actions runner — setup notes

This directory contains helper scripts and examples to register a self-hosted runner
either directly on a machine (systemd) or inside a container.

Two supported approaches:

1) Install runner on the machine (systemd)

- Pros: full machine resources, simple to integrate with local network, no extra container layer.
- Cons: less isolation; be careful about security and what jobs you accept.

Quick steps (systemd):

1. On GitHub: Repository → Settings → Actions → Runners → New self-hosted runner → follow instructions and obtain the registration token.
2. Copy the token and run the helper as root on the target machine:

```bash
sudo ./register-runner.sh https://github.com/<OWNER>/<REPO> <REGISTRATION_TOKEN> my-runner-01
```

3. The script downloads the runner, configures it (unattended), creates `actions-runner` user, and installs a systemd service. After this, the runner should appear in the repository runner list.

Security notes:
- Only register trusted machines for public repos. Self-hosted runners execute arbitrary workflow jobs.
- Use firewall rules and run the runner under a dedicated user.

2) Run runner inside Docker container

- Pros: isolation, easier rollback, reproducible environment.
- Cons: requires Docker and appropriate capabilities; may need bind mounts for workspace.

Example Docker run (replace token and repo):

```bash
docker run -d \
  --name actions-runner \
  --restart unless-stopped \
  -e RUNNER_NAME=my-runner-01 \
  -e RUNNER_REPOSITORY_URL=https://github.com/<OWNER>/<REPO> \
  -e RUNNER_TOKEN=<REGISTRATION_TOKEN> \
  ghcr.io/actions/runner:latest
```

If you prefer a VM/cloud-init or systemd+docker approach, I can generate a cloud-init snippet or Docker Compose file for you.
