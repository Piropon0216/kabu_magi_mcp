# Project Structure - Stock MAGI System

## ディレクトリ構成

```
stock-magi-system/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── src/
│   ├── common/             # 汎用基盤（ドメイン非依存・再利用可能）
│   │   ├── consensus/      # マルチエージェント合議エンジン
│   │   │   ├── orchestrators/
│   │   │   │   └── group_chat_consensus.py  # GroupChat合議オーケストレーター
│   │   │   └── strategies/
│   │   │       ├── voting_strategy.py       # 多数決/重み付け投票
│   │   │       └── confidence_aggregation.py # 信頼度ベース集約
│   │   ├── mcp/            # MCP統合管理
│   │   │   ├── plugin_registry.py           # MCPプラグイン統一管理
│   │   │   └── data_source_adapter.py       # 汎用データソースアダプター
│   │   └── models/         # 共通データモデル
│   │       └── decision_models.py           # Action, AgentVote, FinalDecision
│   ├── stock_magi/         # 株式ドメイン固有実装
│   │   ├── agents/         # 株式分析エージェント
│   │   │   ├── melchior_agent.py            # ファンダメンタルズ分析
│   │   │   ├── balthasar_agent.py           # バランス分析
│   │   │   └── casper_agent.py              # テクニカル分析
│   │   ├── prompts/        # 株式分析プロンプト
│   │   │   └── stock_analysis_prompts.py    # プロンプトテンプレート
│   │   └── api/            # FastAPI エンドポイント
│   │       └── endpoints.py                 # /api/analyze 実装
│   └── main.py             # FastAPI アプリケーションエントリーポイント
├── tests/                  # テストファイル
│   ├── common/             # 共通基盤のテスト
│   │   ├── test_consensus.py                # 合議エンジンテスト
│   │   └── test_mcp_registry.py             # MCP レジストリテスト
│   └── stock_magi/         # ドメイン固有のテスト
│       ├── test_agents.py                   # エージェントテスト
│       └── test_api.py                      # API統合テスト
├── infra/                  # インフラ定義
│   └── main.bicep          # Azure Container Apps定義
├── config/                 # 設定ファイル
│   └── mcp_servers.json    # MCP サーバー設定
├── docs/                   # ドキュメント（教育重視）
│   ├── ARCHITECTURE.md     # アーキテクチャ詳細（図解付き）
│   ├── AGENT_FRAMEWORK_GUIDE.md  # Agent Framework 入門
│   ├── MCP_INTEGRATION.md  # MCP プロトコル解説
│   ├── FOUNDRY_GUIDE.md    # Microsoft Foundry 使い方
│   ├── REUSABILITY_GUIDE.md # 他ドメインへの流用方法
│   ├── PYTHON_GUIDE.md     # Python async/await, 型ヒント入門
│   ├── LEARNING_PATH.md    # 推奨学習順序と各段階の目標
│   ├── TROUBLESHOOTING.md  # よくある問題と解決方法
│   ├── RESOURCES.md        # 学習リソース集
│   ├── API.md              # API仕様
│   └── SETUP.md            # セットアップガイド（詳細手順）
├── scripts/                # ビルド・デプロイスクリプト
│   ├── setup.sh            # 初期セットアップ
│   └── deploy.sh           # デプロイスクリプト
├── .vscode/                # VSCode設定
│   ├── settings.json       # エディター設定
│   ├── launch.json         # デバッグ設定
│   └── extensions.json     # 推奨拡張機能
├── pyproject.toml          # Poetry 依存管理
├── ruff.toml               # Ruff 設定（Linter/Formatter）
├── pytest.ini              # pytest 設定
├── Dockerfile              # Docker イメージ定義
├── .env.example            # 環境変数テンプレート
├── .gitignore              # Git除外設定
├── CHANGELOG.md            # 変更履歴（詳細記録）
└── README.md               # プロジェクト概要
```

## モジュール境界

### 共通基盤層（ドメイン非依存・再利用可能）
- `src/common/consensus/`: マルチエージェント合議エンジン（汎用）
- `src/common/mcp/`: MCP プラグイン管理（汎用）
- `src/common/models/`: 共通データモデル（Action, Decision など）

**再利用パターン**:
- 不動産分析: `src/real_estate/` を追加、`src/common/` はそのまま流用
- 医療診断: `src/medical/` を追加、合議エンジンを再利用

### ドメイン固有層
- `src/stock_magi/agents/`: 株式分析エージェント（ペルソナ定義）
- `src/stock_magi/prompts/`: 株式分析プロンプトテンプレート
- `src/stock_magi/api/`: FastAPI エンドポイント

### インフラ層
- `infra/`: Azure Container Apps 定義（Bicep）
- `config/`: MCP サーバー設定（JSON）

## 命名規則

### ファイル命名
- **Python**: snake_case（例: `group_chat_consensus.py`）
- **設定ファイル**: kebab-case（例: `mcp-servers.json`）
- **テスト**: `test_*.py`（pytest 規約）

### 変数・関数命名
- **変数**: snake_case（例: `stock_data`）
- **定数**: UPPER_SNAKE_CASE（例: `MAX_RETRY_COUNT`）
- **クラス**: PascalCase（例: `ReusableConsensusOrchestrator`）
- **関数**: snake_case（例: `reach_consensus()`）
- **ファクトリー関数**: `create_*`（例: `create_melchior_agent()`）

### 型定義命名
- **Pydantic モデル**: PascalCase（例: `FinalDecision`）
- **Enum**: PascalCase（例: `Action`）
- **型ヒント**: snake_case（例: `decision: FinalDecision`）

## Git管理
### ブランチ戦略
- `main`: 本番環境（安定版）
- `develop`: 開発統合ブランチ
- `feature/*`: 機能開発ブランチ
- `hotfix/*`: 緊急修正ブランチ

### コミットメッセージ
Conventional Commits形式:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント変更
- `style`: コードフォーマット
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `chore`: ビルド、設定変更

**例**:
```
feat(agents): 短期トレーダーエージェントを実装

- テクニカル分析ロジック追加
- 信頼度スコア計算実装
- ユニットテスト追加

Refs: #12
## 依存関係管理

### パッケージマネージャー
- **Poetry**: Python 依存関係管理（`pyproject.toml` 使用）

### 主要依存関係（予定）
- `agent-framework-azure-ai`: Agent Framework コア（⚠️ `--pre` プレリリース版）
- `fastapi`: Web API フレームワーク
- `uvicorn`: ASGI サーバー
- `pydantic`: データバリデーション
- `pytest`: テストフレームワーク
- `pytest-asyncio`: 非同期テストサポート
- `ruff`: Linter + Formatter（超高速）
- `mypy`: 型チェック（オプション）

### バージョン固定（プレリリース版対策）
## 環境変数管理

### 必須環境変数
```
# Microsoft Foundry (旧 Azure AI Foundry)
FOUNDRY_ENDPOINT=https://your-project.azure.ai.foundry.microsoft.com
FOUNDRY_API_KEY=
FOUNDRY_DEPLOYMENT=gpt-4o

# MCP サーバー設定（ローカル開発用）
MCP_YAHOO_FINANCE_COMMAND=npx @modelcontextprotocol/server-yahoo-finance
MCP_AZURE_DOCS_COMMAND=npx @modelcontextprotocol/server-azure-docs

# アプリケーション
PYTHON_ENV=development|production
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```zure Storage
AZURE_STORAGE_CONNECTION_STRING=

# MCP設定
MCP_SERVER_ENDPOINT=

# アプリケーション
NODE_ENV=development|production
LOG_LEVEL=debug|info|warn|error
```

## 開発ワークフロー
## 開発ワークフロー

1. `feature/*` ブランチ作成
2. TDD でテスト先行実装（pytest）
3. コミット（Conventional Commits）
4. プルリクエスト作成
5. CI 自動テスト実行（pytest, ruff check）
6. コードレビュー
7. `develop` へマージ
8. 定期的に `main` へリリース

## ドキュメント更新

### 必須更新タイミング
- **CHANGELOG.md**: すべてのコミット後
- **README.md**: セットアップ手順変更時
- **API.md**: API インターフェース変更時
- **ARCHITECTURE.md**: アーキテクチャ変更時
- **AGENT_FRAMEWORK_GUIDE.md**: Agent Framework 使用パターン追加時