# Technical Architecture - Stock MAGI System

## 言語とランタイム
### 主要言語
- **Python 3.11+** (必須)
  - 理由: Microsoft Agent Framework の最新機能サポート、AI/MLエコシステム親和性
  - バージョン: 3.11以上（Agent Framework 要件）
  - 型ヒント必須（mypy または Pyright でチェック）
  - パッケージ管理: Poetry（依存関係管理）
  - 学習リソース: [Python公式ドキュメント](https://docs.python.org/ja/3/)

### 実行環境
- **Python Runtime**: 3.11+
- **非同期処理**: asyncio + async/await パターン
- **開発環境**: Windows ARM64対応（Python標準サポート）
- 学習リソース: [Python Async/Await ガイド](https://docs.python.org/ja/3/library/asyncio.html)

## クラウドプラットフォーム
### 優先クラウド: Azure
- **理由**: Microsoft Foundry統合、Agent Framework ネイティブサポート
- **主要サービス**:
  - Azure Container Apps（コンテナベース実行環境、Python対応、自動スケーリング）
  - Microsoft Foundry（LLMモデル管理、プロンプト実験、コスト追跡）
  - Azure Storage（データ永続化）
  - Azure Key Vault（シークレット管理）
  - Application Insights（ログ、トレーシング）
- **学習リソース**:
  - [Azure Fundamentals](https://learn.microsoft.com/ja-jp/training/azure/)
  - [Azure Container Apps入門](https://learn.microsoft.com/ja-jp/azure/container-apps/)
  - [Microsoft Foundry (旧 Azure AI Foundry)](https://learn.microsoft.com/ja-jp/azure/ai-studio/)
  - [Azure無料アカウント](https://azure.microsoft.com/ja-jp/free/)
## アーキテクチャパターン
### Agent Framework + 再利用可能モジュール設計
- **共通基盤層** (`src/common/`):
  - `ReusableConsensusOrchestrator`: ドメイン非依存な汎用マルチエージェント合議エンジン
  - `MCPPluginRegistry`: 複数MCPサーバーの統一管理
  - `VotingStrategy`: 多数決/重み付け投票の戦略パターン実装
  - **目的**: 株式以外のドメイン（不動産、医療など）でも再利用可能
  
- **ドメイン固有層** (`src/stock_magi/`):
  - エージェント定義（Melchior, Balthasar, Casper）
  - 株式分析プロンプトテンプレート
  - FastAPI エンドポイント
  
- **学習リソース**: 
  - [Microsoft Agent Framework 公式](https://github.com/microsoft/agent-framework)
  - [Agent Framework ドキュメント](https://microsoft.github.io/agent-framework/)
  - [マルチエージェントシステム設計](https://learn.microsoft.com/ja-jp/azure/ai-studio/concepts/agents)

### フレームワーク活用方針
- **カスタム実装を最小化**: Agent Framework の組み込み機能（GroupChat, MCP Plugin）を最大限活用
- **70%コード削減**: フルスクラッチ実装(1,500行) → Agent Framework活用(300-500行)
## 技術スタック
### Core Framework
- **Agent Framework**: `agent-framework-azure-ai --pre` (⚠️ プレリリース版)
  - GroupChatOrchestrator（マルチエージェント合議）
  - MCPServerPlugin（Model Context Protocol ネイティブサポート）
  - Agent, AssistantAgent, UserProxyAgent
- **学習リソース**: [Agent Framework GitHub](https://github.com/microsoft/agent-framework)

### バックエンド
- **APIフレームワーク**: FastAPI 0.100+
  - 高速、非同期対応、自動OpenAPI生成
  - Pydantic による型安全なリクエスト/レスポンス検証
- **ランタイム**: Uvicorn（ASGI サーバー）
- **API仕様**: REST API（OpenAPI 3.1 自動生成）

### LLMサービス
- **プライマリ**: Microsoft Foundry (旧 Azure AI Foundry)
  - モデル: GPT-4o（コスト効率重視）
  - SDK: `azure-ai-agent` (Agent Framework 統合)
  - 機能: モデル管理、プロンプト実験、コスト追跡、トレーシング
- **学習リソース**: [Microsoft Foundry ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-studio/)

### MCP Protocol
- **実装**: Agent Framework の MCPServerPlugin（ネイティブ統合）
- **対応サーバー**:
  - Yahoo Finance MCP Server (`@modelcontextprotocol/server-yahoo-finance`)
  - Azure Docs MCP Server (`@modelcontextprotocol/server-azure-docs`)
  - DuckDB MCP Server（Phase 3 - Pending）
- **管理**: `MCPPluginRegistry` による統一管理
- **学習リソース**: [MCP Specification](https://modelcontextprotocol.io/)

### データストレージ
- **Phase 1 (MVP)**: なし（ステートレス）
- **Phase 2**: Azure Table Storage または Cosmos DB（分析履歴保存）
- **Phase 3 (Pending)**: DuckDB統合（時系列株式データ管理）

### テスティング
- **ユニットテスト**: pytest + pytest-asyncio
- **モック**: unittest.mock（Agent Framework モック）
- **統合テスト**: TestClient (FastAPI) + ローカル MCP サーバー
- **カバレッジ**: pytest-cov

### CI/CD
- **CI**: GitHub Actions
  - テスト自動実行 (`pytest`)
  - リント/フォーマット (`ruff check`, `ruff format`)
  - Dockerビルド検証
- **CD**: Azure Container Apps Deployment（GitHub Actions）

### コーディング規約
- **リンター/フォーマッター**: Ruff（超高速 Linter + Formatter）
- **型チェック**: mypy または Pyright
- **コミット規約**: Conventional Commits
- **ブランチ戦略**: Git Flow（main, develop, feature/*, hotfix/*）

## 型安全性
### 必須ルール
- **型ヒント必須**: すべての関数引数と戻り値に型アノテーション
- **Pydantic モデル**: 外部API境界でのデータ検証
- **mypy strict mode**: 型チェック厳格化（`strict = true`）
- **Any型禁止**: 不明な型は `object` または Protocol 使用
### 必須ルール
- `any`型の使用禁止（unknown使用を推奨）
- すべての関数に明示的な戻り値型
- インターフェース/型エイリアスでデータ構造定義
- Zodによるランタイムバリデーション（外部API境界）

## 外部API統合
### 株式データAPI
- **モーニングスター**: REST API（Phase 2）
- **Jquants API**: REST API（Phase 2）
- **Phase 1**: モックデータまたはシンプルなサンプルAPI

### 認証管理
- **Azure Key Vault**: APIキー、シークレット管理
- **環境変数**: ローカル開発用（`.env`ファイル）

## セキュリティ
- **HTTPS/TLS**: すべての通信で必須
- **APIキー暗号化**: Azure Key Vault使用
- **ログマスキング**: 機密情報の自動マスキング
- **依存関係スキャン**: Dependabot有効化
## ドキュメント方針
### 教育的配慮（最重要）
このプロジェクトは実用的な学習教材としても機能することを重視します。

#### 初学者向けサポート
- **段階的学習パス**: 機能追加ごとに必要な知識を明示
- **実装前の概念説明**: コードを書く前に「なぜこうするのか」を説明
- **豊富な例とコメント**: すべてのコードに教育的コメント
- **トラブルシューティング**: よくあるエラーと解決方法を記録

#### Agent Framework 学習支援
- **詳細なコメント**: Agent Framework APIの使用方法を説明
- **Changelog詳細記録**: 各変更の理由と影響
- **実装ガイド**: マルチエージェント設計パターンの解説
- **再利用方法**: `src/common/` モジュールを他ドメインに適用する方法

#### Azure/Foundry初学者向け配慮
- **サービス説明**: 使用する各Azureサービスの役割を明記
- **設定手順**: Azure Portal操作を画面キャプチャ付きで記録
- **コスト説明**: 各リソースのコスト影響を明示
- **代替方法**: ローカル開発環境での代替手段を提供

### 必須ドキュメント
- `CHANGELOG.md`: すべての変更を詳細記録（教育的説明付き）
- `README.md`: セットアップ、実行方法
- `docs/ARCHITECTURE.md`: アーキテクチャ詳細（図解付き）
- `docs/AGENT_FRAMEWORK_GUIDE.md`: Agent Framework 入門（新規）
- `docs/MCP_INTEGRATION.md`: MCP Protocol 解説（新規）
- `docs/FOUNDRY_GUIDE.md`: Microsoft Foundry 使い方（新規）
- `docs/REUSABILITY_GUIDE.md`: 他ドメインへの流用方法（新規）
- `docs/PYTHON_GUIDE.md`: Python async/await, 型ヒント入門（新規）
- `docs/LEARNING_PATH.md`: 推奨学習順序と各段階の目標
- `docs/TROUBLESHOOTING.md`: よくある問題と解決方法
- `docs/RESOURCES.md`: 学習リソース集
- `docs/RESOURCES.md`: 学習リソース集（新規追加）
### 必須ドキュメント
- `CHANGELOG.md`: すべての変更を詳細記録
- `README.md`: セットアップ、実行方法
- `docs/ARCHITECTURE.md`: アーキテクチャ詳細
- `docs/TYPESCRIPT_GUIDE.md`: Python開発者向けTypeScript入門
