# Project Structure - Stock MAGI System

## ディレクトリ構成

```
stock-magi-system/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── src/
│   ├── core/               # コアドメインロジック
│   │   ├── agents/         # トレーダーエージェント実装
│   │   │   ├── registry.ts         # エージェントレジストリ
│   │   │   ├── base-agent.ts       # エージェント基底インターフェース
│   │   │   ├── short-term-agent.ts # 短期トレーダー
│   │   │   ├── mid-term-agent.ts   # 中期トレーダー
│   │   │   └── event-agent.ts      # イベントトレーダー
│   │   ├── ensemble/       # 合議システム
│   │   │   ├── consensus-engine.ts # 合議エンジン
│   │   │   ├── voting-strategies.ts # 投票戦略
│   │   │   └── decision.ts         # 意思決定モデル
│   │   └── models/         # ドメインモデル
│   │       ├── stock-data.ts       # 株式データモデル
│   │       ├── analysis-result.ts  # 分析結果モデル
│   │       └── decision.ts         # 判断モデル
│   ├── adapters/           # 外部システムアダプター
│   │   ├── data-sources/   # データソースアダプター
│   │   │   ├── mcp-connector.ts    # MCPコネクタ基底
│   │   │   ├── stock-api-adapter.ts # 株式APIアダプター
│   │   │   └── mock-data-adapter.ts # モックデータ（Phase 1）
│   │   ├── llm/            # LLMプロバイダー
│   │   │   ├── llm-provider.ts     # LLMプロバイダーインターフェース
│   │   │   ├── azure-openai.ts     # Azure OpenAI実装
│   │   │   └── local-llm.ts        # ローカルLLM実装（将来）
│   │   └── storage/        # ストレージアダプター
│   │       ├── storage-provider.ts # ストレージインターフェース
│   │       ├── azure-blob.ts       # Azure Blob実装
│   │       └── local-file.ts       # ローカルファイル実装
│   ├── ports/              # ポート定義（インターフェース）
│   │   ├── data-source.port.ts     # データソースポート
│   │   ├── llm-provider.port.ts    # LLMプロバイダーポート
│   │   └── storage.port.ts         # ストレージポート
│   ├── functions/          # Azure Functions（Phase 1: MVP）
│   │   ├── analyze-stock/  # 株式分析Function
│   │   │   ├── index.ts
│   │   │   └── function.json
│   │   └── health-check/   # ヘルスチェックFunction
│   │       ├── index.ts
│   │       └── function.json
│   ├── cli/                # CLIインターフェース（Phase 1）
│   │   ├── index.ts        # CLIエントリーポイント
│   │   ├── commands/       # コマンド実装
│   │   │   ├── analyze.ts  # 分析コマンド
│   │   │   └── config.ts   # 設定コマンド
│   │   └── ui/             # CLI出力フォーマット
│   │       └── formatter.ts
│   ├── web/                # Webアプリ（Phase 2）
│   │   ├── app/            # Next.js App Router
│   │   ├── components/     # Reactコンポーネント
│   │   └── lib/            # ユーティリティ
│   ├── config/             # 設定管理
│   │   ├── app-config.ts   # アプリケーション設定
│   │   └── env.ts          # 環境変数型定義
│   └── utils/              # ユーティリティ
│       ├── logger.ts       # ロギング
│       ├── error-handler.ts # エラーハンドリング
│       └── validator.ts    # バリデーション
├── tests/                  # テストファイル
│   ├── unit/               # ユニットテスト
│   │   ├── agents/
│   │   ├── ensemble/
│   │   └── adapters/
│   ├── integration/        # インテグレーションテスト
│   └── e2e/                # E2Eテスト（Phase 2）
├── docs/                   # ドキュメント
│   ├── ARCHITECTURE.md     # アーキテクチャ詳細
│   ├── TYPESCRIPT_GUIDE.md # Python開発者向けTS入門
│   ├── API.md              # API仕様
│   └── SETUP.md            # セットアップガイド
├── scripts/                # ビルド・デプロイスクリプト
│   ├── setup.sh            # 初期セットアップ
│   └── deploy.sh           # デプロイスクリプト
├── .vscode/                # VSCode設定
│   ├── settings.json       # エディター設定
│   ├── launch.json         # デバッグ設定
│   └── extensions.json     # 推奨拡張機能
├── package.json            # npm依存関係
├── tsconfig.json           # TypeScript設定
├── vitest.config.ts        # Vitestテスト設定
├── .eslintrc.js            # ESLint設定
├── .prettierrc             # Prettier設定
├── .env.example            # 環境変数テンプレート
├── .gitignore              # Git除外設定
├── CHANGELOG.md            # 変更履歴（詳細記録）
└── README.md               # プロジェクト概要
```

## モジュール境界
### コアドメイン（ビジネスロジック）
- `src/core/agents/`: エージェント実装（プラグイン可能）
- `src/core/ensemble/`: 合議アルゴリズム
- `src/core/models/`: ドメインモデル（型定義）

### アダプター層（外部システム統合）
- `src/adapters/data-sources/`: データ取得
- `src/adapters/llm/`: LLM統合
- `src/adapters/storage/`: データ永続化

### ポート層（インターフェース定義）
- `src/ports/`: コアドメインとアダプター間の契約

### アプリケーション層
- `src/functions/`: Azure Functions（サーバーレス）
- `src/cli/`: CLIインターフェース
- `src/web/`: Webアプリケーション（Phase 2）

## 命名規則
### ファイル命名
- **TypeScript**: kebab-case（例: `agent-registry.ts`）
- **コンポーネント**: PascalCase（例: `AgentCard.tsx`）
- **テスト**: `*.test.ts` または `*.spec.ts`

### 変数・関数命名
- **変数**: camelCase（例: `stockData`）
- **定数**: UPPER_SNAKE_CASE（例: `MAX_RETRY_COUNT`）
- **型/インターフェース**: PascalCase（例: `StockData`）
- **関数**: camelCase（例: `analyzeStock()`）
- **クラス**: PascalCase（例: `ShortTermAgent`）

### 型定義命名
- **インターフェース**: `I`プレフィックスなし（例: `Agent`）
- **型エイリアス**: PascalCase（例: `AnalysisResult`）
- **Enum**: PascalCase（例: `DecisionType`）

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
```

## 依存関係管理
### パッケージマネージャー
- **npm**: デフォルト（package-lock.json使用）

### 主要依存関係（予定）
- `typescript`: ^5.3.0
- `@azure/functions`: ^4.0.0
- `@azure/openai`: 最新
- `commander`: CLI
- `zod`: バリデーション
- `vitest`: テスト
- `eslint`: リント
- `prettier`: フォーマット

## 環境変数管理
### 必須環境変数
```
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_NAME=

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=

# MCP設定
MCP_SERVER_ENDPOINT=

# アプリケーション
NODE_ENV=development|production
LOG_LEVEL=debug|info|warn|error
```

## 開発ワークフロー
1. `feature/*`ブランチ作成
2. TDDでテスト先行実装
3. コミット（Conventional Commits）
4. プルリクエスト作成
5. CI自動テスト実行
6. コードレビュー
7. `develop`へマージ
8. 定期的に`main`へリリース

## ドキュメント更新
### 必須更新タイミング
- **CHANGELOG.md**: すべてのコミット後
- **README.md**: セットアップ手順変更時
- **API.md**: APIインターフェース変更時
- **ARCHITECTURE.md**: アーキテクチャ変更時
