# Stock MAGI System - MVP セットアップガイド

このガイドでは、Stock MAGI System (Phase 1 MVP) のセットアップから動作確認までの手順を説明します。

## 📋 前提条件

- **OS**: Windows 11 (ARM64 Copilot+ PC 推奨) / macOS / Linux
- **必須ツール**:
  - Docker Desktop または Podman
  - VS Code (DevContainer 使用時)
  - Git
- **Azure アカウント**: Microsoft Foundry へのアクセス権限

## ⏱️ 所要時間

- **手動作業**: 合計 **25-30 分**
  - Foundry Portal セットアップ: 20 分
  - Morningstar Tool Catalog セットアップ: 2 分
  - `.env` ファイル設定: 5 分
- **自動作業**: DevContainer ビルド (5-10 分)

---

## 🚀 セットアップ手順

### Step 1: リポジトリクローン

```bash
git clone <repository-url>
cd <repository-name>
```

### Step 2: Foundry Portal セットアップ ⏰ 20分

#### 2.1 Azure AI Foundry Portal へアクセス

1. ブラウザで [https://ai.azure.com/](https://ai.azure.com/) を開く
2. Azure アカウントでサインイン

#### 2.2 新しいプロジェクトを作成

1. **左サイドバー** → **「+ New Project」** をクリック
2. プロジェクト情報を入力:
   - **Project name**: `stock-magi-system` (任意)
   - **Subscription**: 使用する Azure サブスクリプション
   - **Resource group**: 既存または新規作成
   - **Region**: `East US` (推奨) または最寄りのリージョン
3. **「Create」** をクリック → プロジェクト作成完了 (1-2 分)

#### 2.3 GPT-4o モデルをデプロイ

1. プロジェクトダッシュボード → **「Deployments」** タブ
2. **「+ Create Deployment」** をクリック
3. モデル選択:
   - **Model**: `gpt-4o` (最新バージョン)
   - **Deployment name**: `gpt-4o-magi` (任意、`.env` で使用)
   - **Version**: 最新バージョンを選択
   - **Capacity**: `10K TPM` (開発環境用)
4. **「Deploy」** をクリック → デプロイ完了 (2-3 分)

#### 2.4 API 接続情報を取得

1. デプロイ完了後、**「Deployments」** リストで `gpt-4o-magi` をクリック
2. **「API Settings」** または **「Endpoint」** タブを開く
3. 以下の情報をメモ (`.env` ファイルで使用):
   ```
   FOUNDRY_ENDPOINT=https://<your-endpoint>.openai.azure.com/
   FOUNDRY_API_KEY=<your-api-key>
   FOUNDRY_DEPLOYMENT=gpt-4o-magi
   FOUNDRY_API_VERSION=2024-12-01
   ```

### Step 3: Morningstar Tool Catalog セットアップ ⏰ 2分

#### 3.1 Foundry Tool Catalog へアクセス

1. Foundry Portal 左サイドバー → **「Tools」** または **「Tool Catalog」**
2. 検索バーで `Morningstar` を検索

#### 3.2 Morningstar MCP Server を有効化

1. **「Morningstar MCP Server」** をクリック
2. **「Enable」** または **「Add to Project」** をクリック
3. 権限確認ダイアログが表示される場合は **「Allow」** をクリック
4. ステータスが **「Enabled」** になったことを確認

**注意**: Phase 1 では Foundry Portal の GUI 設定のみで完了。ローカル MCP サーバーのインストールは不要。

### Step 4: `.env` ファイル作成 ⏰ 5分

1. リポジトリルートで `.env.example` をコピー:
   ```bash
   cp .env.example .env
   ```

2. `.env` ファイルを開き、Step 2.4 で取得した情報を入力:
   ```env
   # Microsoft Foundry 設定
   FOUNDRY_ENDPOINT=https://<your-endpoint>.openai.azure.com/
   FOUNDRY_API_KEY=<your-api-key>
   FOUNDRY_DEPLOYMENT=gpt-4o-magi
   FOUNDRY_API_VERSION=2024-12-01

   # アプリケーション設定
   APP_ENV=development
   LOG_LEVEL=info
   ```

3. 保存して閉じる

---

## 🛠️ 開発環境の選択

### 方法 A: DevContainer (推奨)

**メリット**: 完全な開発環境が自動構築される

1. VS Code でリポジトリを開く
2. 右下の通知 **「Reopen in Container」** をクリック
   - または `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`
3. DevContainer ビルド完了まで待機 (初回 5-10 分)
4. ターミナルで依存関係インストール:
   ```bash
   poetry install
   ```

### 方法 B: Docker Compose

**メリット**: シンプルな起動、ローカル開発不要

1. `.env` ファイルが作成されていることを確認
2. Docker Compose でビルド・起動:
   ```bash
   docker compose up --build
   ```
3. API が起動したら [http://localhost:8000/docs](http://localhost:8000/docs) にアクセス

### 方法 C: ローカル Python 環境

**メリット**: 最速のホットリロード

1. Python 3.11+ がインストールされていることを確認
2. Poetry をインストール:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. 依存関係インストール:
   ```bash
   poetry install
   ```
4. アプリケーション起動:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

---

## ✅ 動作確認

### 1. API が起動していることを確認

```bash
curl http://localhost:8000/api/health
# 期待される出力: {"status":"ok"}
```

### 2. ルートエンドポイントにアクセス

```bash
curl http://localhost:8000/
# API 情報が JSON で返される
```

### 3. Swagger UI で API を確認

ブラウザで [http://localhost:8000/docs](http://localhost:8000/docs) を開く

### 4. 株式分析エンドポイントをテスト

Swagger UI または curl で POST /api/analyze を実行:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "7203.T",
    "include_reasoning": true
  }'
```

**期待される出力** (Phase 1 MVP):
```json
{
  "ticker": "7203.T",
  "final_action": "HOLD",
  "confidence": 0.5,
  "summary": "Phase 1 MVP - 1エージェントによる合議結果。最終アクション: HOLD",
  "reasoning": [
    {
      "agent": "Melchior",
      "action": "HOLD",
      "confidence": 0.5,
      "reasoning": "Phase 1 MVP - 7203.T のモック分析。Phase 2 で Agent Framework + Morningstar 統合予定。"
    }
  ],
  "has_conflict": false
}
```

**注意**: Phase 1 はモック実装のため、すべて `HOLD` + `confidence 0.5` を返します。Phase 2 で実際の Agent Framework + Morningstar データ統合が完了します。

---

## 🧪 テスト実行

### Unit Tests + Integration Tests

```bash
# DevContainer または ローカル環境
poetry run pytest tests/ -v

# カバレッジ付き
poetry run pytest tests/ --cov=src --cov-report=html
```

### E2E Tests (API エンドポイント)

```bash
poetry run pytest tests/test_api_endpoints.py -v
```

---

## 🐛 トラブルシューティング

### 問題 1: `FOUNDRY_API_KEY` not found エラー

**原因**: `.env` ファイルが読み込まれていない

**解決策**:
1. `.env` ファイルがリポジトリルートに存在することを確認
2. DevContainer の場合: コンテナを再ビルド (`Dev Containers: Rebuild Container`)
3. Docker Compose の場合: `docker compose down` → `docker compose up --build`

### 問題 2: Morningstar tool not found

**原因**: Foundry Tool Catalog で Morningstar が有効化されていない

**解決策**:
1. Foundry Portal ([https://ai.azure.com/](https://ai.azure.com/)) にアクセス
2. **「Tools」** → **「Morningstar MCP Server」** → **「Enable」**

### 問題 3: API が起動しない (Port 8000 already in use)

**原因**: ポート 8000 が既に使用されている

**解決策**:
```bash
# 使用中のプロセスを確認 (Linux/macOS)
lsof -i :8000

# 使用中のプロセスを確認 (Windows)
netstat -ano | findstr :8000

# プロセスを終了するか、別のポートを使用
uvicorn src.main:app --port 8001
```

### 問題 4: pytest で import エラー

**原因**: PYTHONPATH が設定されていない

**解決策**:
```bash
# リポジトリルートから実行
PYTHONPATH=. poetry run pytest tests/
```

### 問題 5: ARM64 Mac で Docker ビルドが遅い

**原因**: Rosetta 2 エミュレーション

**解決策**:
1. Docker Desktop の設定 → **「Use Rosetta for x86_64/amd64 emulation」** を有効化
2. または ARM64 ネイティブイメージを使用 (Dockerfile 既に対応済み)

---

## 📊 Phase 2 以降の拡張予定

### Phase 2: Yahoo Finance 統合 (1-2 週間)

- **データソース**: Yahoo Finance MCP Server (npm)
- **新エージェント**: Balthasar (テクニカル分析), Casper (センチメント分析)
- **機能拡張**: 加重投票、対立検出、リアルタイムチャート

### Phase 3: DuckDB + Jquants API (2-3 週間)

- **データソース**: DuckDB (時系列データ), Jquants API (日本株専用)
- **機能拡張**: バックテスト、ポートフォリオ最適化、履歴分析

---

## 📚 関連ドキュメント

- [docs/CONTEXT.md](./CONTEXT.md) - アーキテクチャと設計判断の詳細
- [README.md](../README.md) - プロジェクト概要
- [pyproject.toml](../pyproject.toml) - 依存関係とツール設定
- [.kiro/specs/stock-magi-system-ja/](../.kiro/specs/stock-magi-system-ja/) - 要件・設計・タスク

---

## 💬 サポート

問題が解決しない場合:
1. [docs/CONTEXT.md](./CONTEXT.md) の「Manual Setup Requirements」セクションを確認
2. GitHub Issues を作成 (エラーログと `.env` の設定内容を含める)
3. Agent Framework の公式ドキュメント: [https://learn.microsoft.com/azure/ai-services/agents/](https://learn.microsoft.com/azure/ai-services/agents/)

---

**Phase 1 MVP セットアップ完了!** 🎉

次のステップ: Phase 2 実装開始 (Agent Framework 統合 + Yahoo Finance)
