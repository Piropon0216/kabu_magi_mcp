# Technical Architecture - Stock MAGI System

## 言語とランタイム
### 主要言語
- **TypeScript** (必須)
  - 理由: Copilot+ PC (ARM64)でのPythonライブラリ互換性問題を回避
  - バージョン: 5.3以上（最新安定版）
  - 厳格な型チェック有効化（`strict: true`）

### 実行環境
- **Node.js**: v20 LTS以上
- **開発環境**: Windows ARM64対応

## クラウドプラットフォーム
### 優先クラウド: Azure
- **理由**: Microsoft Foundry統合、Azure OpenAI利用
- **主要サービス**:
  - Azure Functions（サーバーレス実行環境）
  - Azure OpenAI Service（LLM推論）
  - Azure Storage（データ永続化）
  - Azure Key Vault（シークレット管理）

### ローカル実行サポート（将来対応）
- **オフラインモード**: ローカルLLM対応を設計に組み込む
  - Ollama、LM Studioなどの統合検討
  - LLMプロバイダーをインターフェース化（Azure OpenAI / ローカル切り替え可能）

## アーキテクチャパターン
### ヘキサゴナルアーキテクチャ（Ports & Adapters）
- **コアドメイン**: エージェント分析ロジック、合議アルゴリズム
- **ポート**: インターフェース定義（データソース、LLM、ストレージ）
- **アダプター**: 具体実装（MCP、Azure OpenAI、Azure Storage）

### プラグインアーキテクチャ
- **エージェントレジストリ**: 動的なエージェント登録・管理
- **MCPコネクタ**: プラグイン方式でデータソース追加
- **合議アルゴリズム**: 戦略パターンで切り替え可能

## 技術スタック
### フロントエンド/CLI (Phase 1: MVP)
- **CLI**: Commander.js（コマンドラインインターフェース）
- **出力**: テキストベース（chalk.jsでカラー表示）

### フロントエンド/Web (Phase 2)
- **フレームワーク**: Next.js 14+ (App Router)
- **UIライブラリ**: Tailwind CSS + shadcn/ui
- **状態管理**: Zustand または React Context

### バックエンド
- **ランタイム**: Azure Functions v4 (TypeScript)
- **フレームワーク**: なし（軽量化のため標準Azure Functions使用）
- **API仕様**: REST API（将来的にGraphQL検討）

### LLMサービス
- **プライマリ**: Azure OpenAI Service
  - モデル: GPT-4 Turbo / GPT-4o（コスト効率重視）
  - SDK: `@azure/openai`
- **抽象化層**: LLMProviderインターフェース
  - Azure OpenAI実装
  - ローカルLLM実装（将来用）

### MCPプロトコル
- **実装**: Model Context Protocol SDK
- **対応サーバー**:
  - 株式データ用MCPサーバー
  - Azure/AWSナレッジベース用MCPサーバー
  - DuckDB用MCPサーバー（Phase 3 - Pending）

### データストレージ
- **Phase 1 (MVP)**: Azure Blob Storage（JSON形式）
- **Phase 2**: Azure Table Storage または Cosmos DB（NoSQL）
- **Phase 3 (Pending)**: DuckDB統合（コネクタ仕様確定後）

### テスティング
- **ユニットテスト**: Vitest（高速、TypeScript親和性）
- **E2Eテスト**: Playwright（Phase 2以降）
- **モック**: MSW (Mock Service Worker)
- **カバレッジ**: c8 または Vitest内蔵

### CI/CD
- **CI**: GitHub Actions
  - テスト自動実行
  - リント（ESLint + Prettier）
  - ビルド検証
- **CD**: Azure Deployment（Azure Functions Deploy Action）

### コーディング規約
- **リンター**: ESLint with TypeScript plugin
- **フォーマッター**: Prettier
- **コミット規約**: Conventional Commits
- **ブランチ戦略**: Git Flow（main, develop, feature/*, hotfix/*）

## 型安全性
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

## パフォーマンス
- **キャッシング**: Azure Cache for Redis（Phase 2）
- **並列処理**: Promise.all()でエージェント分析並列実行
- **レスポンス目標**: <3秒（単一銘柄分析）

## モニタリング
- **ログ**: Azure Application Insights
- **メトリクス**: カスタムメトリクス（エージェント精度、レスポンス時間）
- **アラート**: エラー率閾値超過時通知

## ドキュメント方針
### Python開発者向け配慮
- **詳細なコメント**: TypeScript構文の説明
- **Changelog詳細記録**: 各変更の理由と影響
- **実装ガイド**: TypeScript特有パターンの解説
- **対応表**: Python概念 → TypeScript実装マッピング

### 必須ドキュメント
- `CHANGELOG.md`: すべての変更を詳細記録
- `README.md`: セットアップ、実行方法
- `docs/ARCHITECTURE.md`: アーキテクチャ詳細
- `docs/TYPESCRIPT_GUIDE.md`: Python開発者向けTypeScript入門
