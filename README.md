# Stock MAGI System

MicrosoftFoundryを活用した、複数のAIトレーダーエージェントによるアンサンブル合議システム

## 概要

Stock MAGI Systemは、異なる投資戦略を持つ複数のAIエージェント（短期・中期・イベント駆動）が、Model Context Protocol (MCP)を通じて株式情報を収集し、合議により投資判断を提供する意思決定支援プラットフォームです。

### 主な特徴

- 🤖 **複数エージェント**: 短期・中期・イベントトレーダーによる多角的分析
- 🔄 **アンサンブル合議**: 単一視点に偏らないバランスの取れた判断
- 🔌 **MCP統合**: プラグイン方式で拡張可能なデータソース
- ☁️ **Azure基盤**: サーバーレス + Azure OpenAI で低コスト運用
- 🧪 **TDD**: テストカバレッジ80%以上、品質重視の開発
- 📊 **透明性**: 各エージェントの判断根拠と合議プロセスの可視化

## 開発フェーズ

### Phase 1 (MVP) - 現在
- 基本的なデータ収集
- 1つのトレーダーエージェント
- シンプルな合議機能
- CLIインターフェース

### Phase 2
- 3つの完全なエージェント実装
- 高度な合議アルゴリズム
- Webダッシュボード

### Phase 3
- DuckDB統合（Jquants APIデータ）
- バックテスト機能
- 高度な分析機能

## 技術スタック

- **言語**: TypeScript 5.x
- **ランタイム**: Node.js 20.x LTS
- **クラウド**: Microsoft Azure
- **LLM**: Azure OpenAI Service
- **アーキテクチャ**: Hexagonal Architecture (Ports & Adapters)
- **テスト**: Jest / Vitest (TDD, カバレッジ80%+)

## セットアップ

### 前提条件

- Node.js 20.x以上
- npm または pnpm
- Azureアカウント（Azure OpenAI利用時）
- Git

### インストール手順

```bash
# リポジトリのクローン
git clone <repository-url>
cd stock-magi-system

# 依存関係のインストール
npm install

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してAzure認証情報を設定

# ビルド
npm run build

# テスト実行
npm test

# 開発モードで実行
npm run dev
```

### 環境変数設定

`.env`ファイルに以下の情報を設定してください:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# MCP設定
MCP_SERVER_ENDPOINT=http://localhost:3000

# ログレベル
LOG_LEVEL=info
```

## 使用方法

### CLI（Phase 1 MVP）

```bash
# 銘柄分析
npm run cli analyze -- --symbol 7203

# ステータス確認
npm run cli status

# ヘルプ
npm run cli -- --help
```

## 開発ガイド

### ディレクトリ構成

```
src/
├── domain/           # ドメインロジック（ビジネスルール）
├── application/      # アプリケーションロジック（ユースケース）
├── infrastructure/   # インフラストラクチャ層（外部統合）
├── presentation/     # プレゼンテーション層（UI）
└── shared/           # 共有ユーティリティ
```

詳細は `.kiro/steering/structure.md` を参照してください。

### テスト実行

```bash
# すべてのテスト実行
npm test

# ウォッチモード
npm run test:watch

# カバレッジ確認
npm run test:coverage
```

### コーディング規約

- TypeScript: `any`の使用禁止、明示的な型定義
- TDD: テストファーストアプローチ必須
- コミット: Conventional Commits形式

詳細は `.kiro/steering/tech.md` を参照してください。

## Python開発者向けの注意

このプロジェクトはTypeScriptで実装されていますが、Python開発者が理解しやすいよう、以下の配慮をしています:

- コード内に丁寧なコメント
- CHANGELOG.mdでの詳細な変更履歴
- READMEとドキュメントの充実
- 型定義の明示的な説明

TypeScript学習リソース:
- [TypeScript公式ドキュメント（日本語）](https://www.typescriptlang.org/ja/docs/)
- [TypeScript Deep Dive 日本語版](https://typescript-jp.gitbook.io/deep-dive/)

## ドキュメント

- [アーキテクチャ概要](docs/architecture/overview.md)
- [開発環境セットアップ](docs/development/setup.md)
- [テスト戦略](docs/development/testing.md)
- [API仕様](docs/api/)

## 変更履歴

詳細な変更履歴は [CHANGELOG.md](CHANGELOG.md) を参照してください。

## ライセンス

MIT License

## 貢献

このプロジェクトはKiro Spec-Driven Developmentを採用しています。機能追加・変更は以下の手順で行ってください:

1. 仕様初期化: `/kiro-spec-init <feature-description>`
2. 要件定義: `/kiro-spec-requirements <feature-name>`
3. 設計: `/kiro-spec-design <feature-name> -y`
4. タスク分解: `/kiro-spec-tasks <feature-name> -y`
5. 実装: `/kiro-spec-impl <feature-name> <task-id>`

## サポート

問題が発生した場合は、GitHubのIssuesにて報告してください。
