### 試行錯誤・運用履歴
- Pydantic v2系移行時、`ConfigDict`/`BaseSettings`の環境変数prefixやenv_fileの適用順序でバリデーションエラー多発 → `model_config`構文で安定化。
- MelchiorAgentのファクトリ関数がPhase 1/1.5の混在で重複・破損 → `git checkout HEAD`で正常状態に復元、段階的リファクタリングへ方針転換。
- APIシグネチャ変更で既存エンドポイントが動作不能化 → 互換性維持のため、既存APIは維持し新機能は別ブランチで開発。
- Spec-Driven Development用サブモジュール（cc-sdd/）が本体に混入 → `.gitignore`と`git rm --cached`で除外。
- 変更履歴の信頼性担保のため、「過去分は編集せず、追記のみ」運用を徹底。

---
# Changelog

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

形式は[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、
このプロジェクトは[セマンティック バージョニング](https://semver.org/lang/ja/)に準拠しています。

## Python開発者向け注意
各エントリには詳細な説明と、TypeScript特有の実装について補足説明を含めています。

---




## [0.1.0] - 2025-12-28

### Added
- プロジェクト初期化とSteering設定（54b1100, 182df49）
- cc-sddリポジトリをVS Code Git管理から除外（3c95275）
- プロジェクト基盤・開発環境セットアップ（331bee0）
- 汎用マルチエージェント基盤モジュール実装（ca77c4c）
- 株式ドメイン実装 - Melchiorエージェント + FastAPI（c0582cd）
- 包括的テストスイート実装（ffe3f23）
- 包括的ドキュメント整備（b684187）
- `src/common/consensus/orchestrators/group_chat_consensus.py`（絶対パスインポート対応）
- `src/common/mcp/foundry_tool_registry.py`（Pydantic v2 `ConfigDict`構文）
- `.gitignore`に`cc-sdd/`サブモジュール除外、Pythonキャッシュ/テスト生成物除外
- `feature/agent-framework-integration`ブランチ作成（Phase 1.5開発用）

### Changed
- セマンティックバージョニングとKeep a Changelog形式の厳格運用を明文化（772d4a6）
- コードフォーマット適用（278060c）

### Fixed
- Pydantic v2対応と環境変数読み込み修正（dc06b65）
- Pydantic v2バリデーションエラーに対応したテスト修正（7adbf27）
- `src/stock_magi/agents/melchior_agent.py` の重複関数定義を修正し、Phase 1実装に復元
- `src/common/mcp/foundry_tool_registry.py` の型アノテーション警告（Optional→| None）を修正予定

### Chore
- Agent Framework準備: `azure-ai-projects`/`azure-identity`依存追加、`pyproject.toml`修正（980e756）
- Phase 1 MVP完了マーク
- プロジェクト整理・不要サブモジュール除外

### Docs
- 教育用途の方針を追加（1a02f30）
- v0.1.0 CHANGELOG + プロジェクトメタデータ更新（772d4a6）

### Test
- Phase 1 MVP: 全37テスト合格、カバレッジ95%

## [Unreleased] - 2025-12-29

### Fixed
- リポジトリ全体に対して `ruff check . --fix` を実行し、自動修正可能なスタイル問題を適用（約100件修正）。

### Known issues / To Do
- 自動修正で残った `ruff` の警告（29件）は手動修正が必要です（主に空行末の余分な空白、`except` 内での例外チェーン明示、未使用変数/インポートの除去など）。
- このコミットでは自動修正を適用し、`CHANGELOG.md` に修正履歴を追記して一緒にコミットします。

### Chore
- `CHANGELOG.md` を更新して運用ルール（コミット時に必ず追記）に従いました。

---

## 運用・技術的決定
- 変更履歴は「追記のみ」原則。過去分は編集せず、必要に応じて`git checkout HEAD -- CHANGELOG.md`で復元し追記。
- コミット内容とChangelogの整合性を重視。
- PythonとTypeScriptの技術的差異は「Python開発者向け補足」として随時記載。

## [0.1.0] - 2025-12-27

### Added
- プロジェクト初期化: ディレクトリ・README・CHANGELOG・Steeringファイル作成
- `.kiro/steering/product.md`, `tech.md`, `structure.md`（プロダクトビジョン・技術方針・構造）
- `src/common/consensus/orchestrators/group_chat_consensus.py`（絶対パスインポート対応）
- `src/common/mcp/foundry_tool_registry.py`（Pydantic v2 `ConfigDict`構文）
- `.gitignore`に`cc-sdd/`サブモジュール除外、Pythonキャッシュ/テスト生成物除外
- `feature/agent-framework-integration`ブランチ作成（Phase 1.5開発用）

### Changed
- セマンティックバージョニングとKeep a Changelog形式の厳格運用を明文化
- Changelogの編集方針を「過去分は編集せず、追記のみ」に統一

### Fixed
- `src/stock_magi/agents/melchior_agent.py` の重複関数定義を修正し、Phase 1実装に復元
- `src/common/mcp/foundry_tool_registry.py` の型アノテーション警告（Optional→| None）を修正予定
- Pydantic v2バリデーションエラー対応

### Chore
- Agent Framework準備: `azure-ai-projects`/`azure-identity`依存追加、`pyproject.toml`修正
- Phase 1 MVP完了マーク・コードフォーマット適用
- プロジェクト整理・不要サブモジュール除外

### Test
- 包括的テストスイート実装（TDDアプローチ）
- Phase 1 MVP: 全37テスト合格、カバレッジ95%

### 運用・技術的決定
- 変更履歴は「追記のみ」原則。過去分は編集せず、必要に応じて`git checkout HEAD -- CHANGELOG.md`で復元し追記。
- コミット内容とChangelogの整合性を重視。
- PythonとTypeScriptの技術的差異は「Python開発者向け補足」として随時記載。

---

## 運用方針
- 変更履歴は「追記のみ」原則。過去分は編集せず、必要に応じて`git checkout HEAD -- CHANGELOG.md`で復元し追記。
- コミット内容とChangelogの整合性を重視。
```
