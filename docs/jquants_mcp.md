% JQuants MCP PoC — 拡張ガイド (MVP)

このドキュメントは `src/mcp_providers/jquants_mcp.py` の PoC 実装を拡張・運用するための手順をまとめます。

## 概要
- 現在のエンドポイント: `GET /tools/jquants/price/{ticker}` — 指定銘柄の直近株価を返します。
- 認証: 環境変数またはプロジェクトルートの `.env` から `JQUANTS_MAIL_ADDRESS` / `JQUANTS_PASSWORD` または `JQUANTS_REFRESH_TOKEN` を読み込みます。

## 使い方（ローカル）
1. プロジェクトルートに `.env` を置き、必要な変数を設定します（既に設定済みの場合は修正不要）。
2. 仮想環境を有効化して uvicorn で起動:

```bash
source .venv/bin/activate
JQUANTS_API_BASE=https://api.jquants.com .venv/bin/uvicorn src.mcp_providers.jquants_mcp:app --host 127.0.0.1 --port 8081
```

3. 動作確認:

```bash
curl http://127.0.0.1:8081/tools/jquants/price/7203.T
```

## 環境変数
- `JQUANTS_API_BASE` (例: https://api.jquants.com)
- `JQUANTS_MAIL_ADDRESS` / `JQUANTS_EMAIL`
- `JQUANTS_PASSWORD`
- `JQUANTS_REFRESH_TOKEN` / `JQUANTS_API_REFRESH_TOKEN`

注: 実装は複数の名前の揺れを吸収します。空文字は無視されます。

## 拡張ポイント
1. 追加エンドポイント
   - `/tools/jquants/statements/{ticker}` のように新しい FastAPI ハンドラを追加し、`client.get_fins_statements` など公式クライアント API を呼ぶ。
   - 返却は JSON シリアライズ可能に（DataFrame → `to_dict(orient="records")`）。

2. キャッシュ
   - 頻度が低くコストが気になる API はローカルの LRU キャッシュや Redis を利用してレスポンスを短時間保存する。

3. エラーハンドリング
   - upstream (jquants) の `HTTPError` は 502 で返すが、クライアントが期待するエラー形に整形する。

4. ロギングとメトリクス
   - `structlog` や `prometheus_client` を導入して呼び出し成功/失敗・レイテンシを収集する。

5. 認証の改善
   - 現在はメール/パスワードまたは refresh token を使用。プロダクションではシークレットストア（Azure Key Vault）に保管し、ランタイムで読み込むことを推奨。

## テスト
- ユニットテスト: `pytest` で `src/mcp_providers/jquants_mcp.py` のハンドラを `TestClient`（fastapi.testclient）で呼び、モック化した `jquantsapi.Client` を注入して動作を確認する。
- E2E: ローカルで `uvicorn` を起動して `/tools/jquants/price/{ticker}` を叩く。

## コンテナ化 & Azure Container Apps Jobs への準備
1. 最小 Dockerfile を用意（下記テンプレート参照）。
2. コンテナイメージを ACR に push し、Container Apps Jobs でスケジュール実行（cron）を設定。
3. 1日1回の実行であれば Job を短時間実行する形が最もコスト効率が良い。

簡易 Dockerfile テンプレート:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-root
COPY . /app
ENV PORT=8081
CMD ["uvicorn", "src.mcp_providers.jquants_mcp:app", "--host", "0.0.0.0", "--port", "8081"]
```

## リリース/運用時のチェックリスト
- シークレットは環境変数ではなく Key Vault に保管
- レート制限/課金プランに応じたリトライ/バックオフを実装
- ログとメトリクスを監視対象に追加

---
更新や追加のテンプレートが必要なら教えてください。
