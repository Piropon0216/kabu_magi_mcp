# Stock MAGI System

MicrosoftFoundryを活用した株式取引支援システム - 複数のAIトレーダーエージェントによるアンサンブル合議意思決定プラットフォーム

## 概要

Stock MAGI Systemは、異なる投資戦略を持つ複数のAIエージェント（短期・中期・イベントトレーダー）が、Model Context Protocol (MCP)を通じて株式情報を収集し、アンサンブル合議により投資判断を提供する低コストな意思決定支援アプリケーションです。

## 主な特徴

- 🤖 **複数AIエージェント**: 短期・中期・イベントトレーダー人格による多角的分析
- 🔄 **アンサンブル合議**: 投票方式による意思決定の統合
- 🔌 **MCP統合**: プラグイン方式で拡張可能なデータソース接続
- ☁️ **Azure基盤**: サーバーレスアーキテクチャによる低コスト運用
- 🧪 **TDD**: テストカバレッジ80%以上を維持
- 📈 **段階的開発**: MVP戦略で小さく始めて価値を積み上げ

## 技術スタック

- **言語**: TypeScript 5.3+
- **ランタイム**: Node.js v20 LTS
- **クラウド**: Azure (Functions, OpenAI, Storage, Key Vault)
- **LLM**: Azure OpenAI Service (GPT-4 Turbo / GPT-4o)
- **テスト**: Vitest
- **アーキテクチャ**: ヘキサゴナル（Ports & Adapters）

## 開発フェーズ

### Phase 1: MVP (現在)
- ✅ 基本的なデータ収集
- ✅ 1-2エージェント実装
- ✅ シンプルな合議機能
- ✅ CLI/基本UI
- ✅ TDD環境構築

### Phase 2: 拡張
- 🔲 全3エージェント（短期・中期・イベント）
- 🔲 高度な合議アルゴリズム
- 🔲 Webダッシュボード
- 🔲 インテグレーションテスト

### Phase 3: 統合
- 🔲 DuckDB統合（Jquants APIデータ）
- 🔲 バックテスト機能
- 🔲 高度な分析機能
- 🔲 E2Eテスト

## セットアップ

### 前提条件

- Node.js v20 LTS以上
- npm または yarn
- Azure アカウント（Azure OpenAI利用のため）
- Git

### インストール

```bash
# リポジトリクローン
git clone <repository-url>
cd stock-magi-system

# 依存関係インストール
npm install

# 環境変数設定
cp .env.example .env
# .envファイルを編集してAzure認証情報を設定
```

### 環境変数設定

`.env`ファイルに以下を設定:

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-turbo

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=your-connection-string

# MCP設定
MCP_SERVER_ENDPOINT=http://localhost:3001

# アプリケーション
NODE_ENV=development
LOG_LEVEL=debug
```

## 使用方法

### CLI（Phase 1）

```bash
# 株式分析実行
npm run cli analyze -- --symbol 7203

# 設定確認
npm run cli config

# ヘルプ
npm run cli -- --help
```

### テスト実行

```bash
# すべてのテスト実行
npm test

# ユニットテストのみ
npm run test:unit

# カバレッジ確認
npm run test:coverage

# ウォッチモード
npm run test:watch
```

### 開発

```bash
# 開発サーバー起動
npm run dev

# ビルド
npm run build

# リント
npm run lint

# フォーマット
npm run format
```

## プロジェクト構造

```
src/
├── core/           # コアドメインロジック
│   ├── agents/     # AIエージェント実装
│   ├── ensemble/   # 合議システム
│   └── models/     # ドメインモデル
├── adapters/       # 外部システムアダプター
│   ├── data-sources/
│   ├── llm/
│   └── storage/
├── ports/          # インターフェース定義
├── functions/      # Azure Functions
└── cli/            # CLIインターフェース
```

詳細は[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)を参照してください。

## ドキュメント

- [アーキテクチャ設計](docs/ARCHITECTURE.md)
- [TypeScriptガイド（Python開発者向け）](docs/TYPESCRIPT_GUIDE.md)
- [API仕様](docs/API.md)
- [セットアップガイド](docs/SETUP.md)
- [変更履歴](CHANGELOG.md)

## 開発ワークフロー

1. **ブランチ作成**: `git checkout -b feature/your-feature`
2. **TDD開発**: テスト先行で実装
3. **コミット**: Conventional Commits形式
4. **プルリクエスト**: コードレビュー依頼
5. **マージ**: CI成功後にマージ

### コミットメッセージ例

```
feat(agents): 短期トレーダーエージェントを実装

- テクニカル分析ロジック追加
- 信頼度スコア計算実装
- ユニットテスト追加（カバレッジ85%）

Refs: #12
```

## コントリビューション

プルリクエストを歓迎します。大きな変更の場合は、まずissueで議論してください。

## Python開発者向け注意事項

このプロジェクトはTypeScriptで記述されています。Python開発者向けに以下のリソースを用意しています:

- [TypeScript入門ガイド](docs/TYPESCRIPT_GUIDE.md): Python → TypeScript対応表
- [詳細なChangelog](CHANGELOG.md): すべての変更を詳細に記録
- コード内コメント: TypeScript特有の構文を説明

## ライセンス

MIT License

## 謝辞

- Microsoft Foundry
- Model Context Protocol (MCP)
- Azure OpenAI Service

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。
