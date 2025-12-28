# Multi-stage Dockerfile for Stock MAGI System
# Python 3.11 + Poetry + FastAPI

# ============================================
# Stage 1: Builder (依存関係インストール)
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Poetry インストール
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="$POETRY_HOME/bin:$PATH"

# pyproject.toml と poetry.lock をコピー
COPY pyproject.toml poetry.lock ./

# 依存関係インストール (virtualenv に)
RUN poetry install --no-root --only main


# ============================================
# Stage 2: Runtime (実行環境)
# ============================================
FROM python:3.11-slim as runtime

WORKDIR /app

# ビルドステージから virtualenv をコピー
COPY --from=builder /app/.venv /app/.venv

# アプリケーションコードをコピー
COPY src/ ./src/
COPY config/ ./config/

# 環境変数設定
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/health')" || exit 1

# 非 root ユーザーで実行
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# ポート公開
EXPOSE 8000

# uvicorn でアプリケーション起動
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
