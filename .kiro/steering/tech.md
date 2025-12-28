# Technical Architecture - Stock MAGI System

## 言語とランタイム
### 主要言語
- **TypeScript** (必須)
  - 理由: Copilot+ PC (ARM64)でのPythonライブラリ互換性問題を回避
  - バージョン: 5.3以上（最新安定版）
  - 厳格な型チェック有効化（`strict: true`）
  - 学習リソース: [TypeScript公式ドキュメント](https://www.typescriptlang.org/docs/)

### 実行環境
- **Node.js**: v20 LTS以上
- **開発環境**: Windows ARM64対応
- 学習リソース: [Node.js公式ガイド](https://nodejs.org/en/docs/)

## クラウドプラットフォーム
### 優先クラウド: Azure
- **理由**: Microsoft Foundry統合、Azure OpenAI利用
- **主要サービス**:
  - Azure Functions（サーバーレス実行環境）
  - Azure OpenAI Service（LLM推論）
  - Azure Storage（データ永続化）
  - Azure Key Vault（シークレット管理）
- **学習リソース**:
  - [Azure Fundamentals](https://learn.microsoft.com/ja-jp/training/azure/)
  - [Azure Functions入門](https://learn.microsoft.com/ja-jp/azure/azure-functions/)
  - [Azure OpenAI Service](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/)
  - [Azure無料アカウント](https://azure.microsoft.com/ja-jp/free/)

## アーキテクチャパターン
### ヘキサゴナルアーキテクチャ（Ports & Adapters）
- **コアドメイン**: エージェント分析ロジック、合議アルゴリズム
- **ポート**: インターフェース定義（データソース、LLM、ストレージ）
- **アダプター**: 具体実装（MCP、Azure OpenAI、Azure Storage）
- **学習リソース**: 
  - [ヘキサゴナルアーキテクチャ解説](https://alistair.cockburn.us/hexagonal-architecture/)
  - [クリーンアーキテクチャ](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### プラグインアーキテクチャ
- **エージェントレジストリ**: 動的なエージェント登録・管理
- **MCPコネクタ**: プラグイン方式でデータソース追加
- **合議アルゴリズム**: 戦略パターンで切り替え可能
- **学習リソース**:
  - [デザインパターン解説](https://refactoring.guru/ja/design-patterns)penAI、Azure Storage）

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

## ドキュメント方針
### 教育的配慮（最重要）
このプロジェクトは実用的な学習教材としても機能することを重視します。

#### 初学者向けサポート
- **段階的学習パス**: 機能追加ごとに必要な知識を明示
- **実装前の概念説明**: コードを書く前に「なぜこうするのか」を説明
- **豊富な例とコメント**: すべてのコードに教育的コメント
- **トラブルシューティング**: よくあるエラーと解決方法を記録

#### Python開発者向け配慮
- **詳細なコメント**: TypeScript構文の説明
- **Changelog詳細記録**: 各変更の理由と影響
- **実装ガイド**: TypeScript特有パターンの解説
- **対応表**: Python概念 → TypeScript実装マッピング

#### Azure初学者向け配慮
- **サービス説明**: 使用する各Azureサービスの役割を明記
- **設定手順**: Azure Portal操作を画面キャプチャ付きで記録
- **コスト説明**: 各リソースのコスト影響を明示
- **代替方法**: ローカル開発環境での代替手段を提供

### 必須ドキュメント
- `CHANGELOG.md`: すべての変更を詳細記録（教育的説明付き）
- `README.md`: セットアップ、実行方法
- `docs/ARCHITECTURE.md`: アーキテクチャ詳細（図解付き）
- `docs/TYPESCRIPT_GUIDE.md`: Python開発者向けTypeScript入門
- `docs/AZURE_GUIDE.md`: Azure初学者向けガイド（新規追加）
- `docs/LEARNING_PATH.md`: 推奨学習順序と各段階の目標（新規追加）
- `docs/TROUBLESHOOTING.md`: よくある問題と解決方法（新規追加）
- `docs/RESOURCES.md`: 学習リソース集（新規追加）
### 必須ドキュメント
- `CHANGELOG.md`: すべての変更を詳細記録
- `README.md`: セットアップ、実行方法
- `docs/ARCHITECTURE.md`: アーキテクチャ詳細
- `docs/TYPESCRIPT_GUIDE.md`: Python開発者向けTypeScript入門
