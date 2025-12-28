# Changelog

このファイルは、Stock MAGI Systemのすべての重要な変更を記録します。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [Unreleased]

### 追加（Added）
- プロジェクト初期セットアップ
- Kiro Spec-Driven Development環境構築
- Steering設定ファイル作成（product.md, tech.md, structure.md）
  - MVP戦略の定義
  - TypeScript技術スタック決定（Copilot+ PC ARM64互換性のため）
  - Azure + Azure OpenAI統合方針
  - Hexagonal Architectureパターン採用
  - TDD必須（カバレッジ80%以上）
- 要件定義書作成（stock-magi-system-ja）
  - 10個の主要要件定義
  - MVP Phase 1/2/3のフェーズ戦略
  - エージェント拡張性の確保（N個対応）
  - DuckDB統合をPhase 3 Pendingに設定
- Gitリポジトリ初期化
- プロジェクト基本ファイル作成
  - README.md: プロジェクト概要・セットアップ手順
  - CHANGELOG.md: 変更履歴管理
  - .gitignore: Git管理除外設定

### 技術的決定（Technical Decisions）
- **言語選択**: TypeScript 5.x
  - 理由: Copilot+ PC (ARM64)でのPythonライブラリ互換性問題を回避
  - 配慮: Python開発者向けに丁寧なコメント・ドキュメント
- **アーキテクチャ**: Hexagonal Architecture (Ports & Adapters)
  - 理由: エージェントプラグイン機構との親和性、テスト容易性
- **クラウド**: Microsoft Azure
  - 理由: MicrosoftFoundry活用、Azure OpenAI統合
- **LLM**: Azure OpenAI Service (Primary)
  - Future: ローカルLLM対応も視野（抽象レイヤー設計）
- **MCP統合**: Model Context Protocol採用
  - Phase 1: 基本MCPクライアント
  - Phase 2: Azure/AWSナレッジベース統合
  - Phase 3: DuckDB統合（Pending）

### 開発方針（Development Principles）
- **MVP第一**: 小さく始めて段階的に機能追加
- **TDD必須**: テストファーストアプローチ、カバレッジ80%以上
- **ドキュメント重視**: CHANGELOG、README、コメントの徹底
- **Git管理**: Conventional Commits、ブランチ戦略（main/develop/feature/*）

## [0.0.0] - 2025-12-28

### 追加
- プロジェクト開始
- 初期リポジトリ構成

---

## 凡例

- **追加（Added）**: 新機能の追加
- **変更（Changed）**: 既存機能の変更
- **非推奨（Deprecated）**: 近い将来削除予定の機能
- **削除（Removed）**: 削除された機能
- **修正（Fixed）**: バグ修正
- **セキュリティ（Security）**: セキュリティ関連の変更
- **技術的決定（Technical Decisions）**: 重要な技術選択の記録
- **開発方針（Development Principles）**: 開発プロセス・方針の決定
