FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl wget tar gzip git python3.11 python3.11-venv python3-pip build-essential \
    libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev jq sudo gnupg2 \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry || true

WORKDIR /actions-runner

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME ["/actions-runner/_work"]

ENTRYPOINT ["/entrypoint.sh"]
