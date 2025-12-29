## Changelog

このプロジェクトの重要な変更はここに記録します。
形式は Keep a Changelog に準拠し、リリース見出しには参照可能な短いコミットハッシュを併記してトレースできるようにします。

## [Unreleased]

### Uncommitted changes (work-in-progress)
- `src/stock_magi/api/endpoints.py`: API endpoint adjustments and exception-chaining fixes. (uncommitted)
- `tests/test_foundry_tool_registry.py`: test updates aligning with Pydantic v2 changes. (uncommitted)

注: 上記はワーキングツリーにある未コミットの変更を短く記録したものです。コミット後、各エントリに代表的な短いコミットハッシュを追記します。ハッシュが増えた場合は、セマンティックバージョニング（マイナーバージョン）を適切に増やして管理してください。

## [0.1.1] - 2025-12-29 (trace: f0c8a8d, e18cfb1, 05601a9)

### Added
- `infra/runner` の systemd スクリプトとコンテナ化サンプルを追加（セルフホスト runner 用）。
- ローカル開発用の Git フック（`.githooks/pre-commit`, `.githooks/pre-push`）およびスモーク/フルテストスクリプトを追加。

### Changed
- コードスタイルと型注釈を `ruff` に合わせて整備し、自動修正・手動修正を適用（自動修正 ≒100件 + 手動修正）。
- `src/common/mcp/foundry_tool_registry.py` を含む Pydantic v2 対応の調整を反映。

### Fixed
- Pydantic v2 移行に伴う環境変数/設定読み込みの不整合を修正（`model_config` の調整、`Field(..., alias=...)` の適用）。
- `ruff` に起因する多数のスタイル問題を解消し、`ruff check .` が通過する状態にしました。

### Chore
- 依存ロックファイルを更新（`poetry lock` → `poetry.lock` を更新・コミット）。

### Test
- スモークテストとフルテストを実行し、既存のテストはすべて合格（37 tests passed）。

---

## [0.1.0] - 2025-12-28 (trace: 772d4a6, e05b888, c0582cd)

### Added
- プロジェクト初期化と Steering 設定（初期コミット含む）。
- 汎用マルチエージェント基盤モジュールと株式ドメイン（Melchior エージェント + FastAPI）を初期実装。

### Changed
- セマンティックバージョニングと Keep a Changelog 形式の運用を明文化。

### Fixed
- Pydantic v2 対応と環境変数読み込み修正（初期移行対応）。

### Test
- Phase 1 MVP: 基本テストスイートを整備・合格。

---

## Notes / Trial & Error (short summary)

- 作業中は Pydantic v2 の env 設定、`ruff` によるスタイル指摘、ローカル git フックによる push ブロック、`poetry.lock` の更新が主要な作業点でした。上記の trace ハッシュを使えば、どのコミットでどの修正が行われたか辿れます。

---

（追記ルール）
- 変更履歴は原則「追記のみ」とし、過去エントリは編集しない運用を推奨します。必要なら各エントリに短い trace ハッシュを併記してください。
````markdown
### 試行錯誤・運用履歴
- Pydantic v2系移行時、`ConfigDict`/`BaseSettings`の環境変数prefixやenv_fileの適用順序でバリデーションエラー多発 → `model_config`構文で安定化。 (trace: dc06b65)
- MelchiorAgent のファクトリ関数が Phase 1 / 1.5 の混在で重複・破損したため復元と段階的リファクタリングに移行。 (trace: ca77c4c)
- API シグネチャ変更による互換性確保のため、新機能は別ブランチで開発。 (trace: 772d4a6)
- Spec-Driven Development 用サブモジュール（cc-sdd/）が混入したため `.gitignore` と `git rm --cached` で除外。 (trace: 3c95275)
- 変更履歴は「追記のみ」運用：過去分は編集せず、追記で履歴を残す。 (trace: 54b1100)

注記: 上記は代表的な変更に紐づく短いコミットハッシュを併記しています。重複する説明が複数エントリにある場合、それらが同一のコミットハッシュを参照しているときは「マージ可能」とみなせます。具体的なマージはユーザ側で手動対応してください（例: 同一ハッシュは同一変更の重複記録であるため統合して差し支えありません）。

---
# Changelog

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づき、セマンティック・バージョニングを採用しています。

---

## [Unreleased]

No unreleased changes.

## [0.1.1] - 2025-12-29

### Added
- `infra/runner` の systemd スクリプトとコンテナ化サンプルを追加（セルフホスト runner 用）。
- ローカル開発用の Git フック（`.githooks/pre-commit`, `.githooks/pre-push`）およびスモーク/フルテストスクリプトを追加。

### Changed
- コードスタイルと型注釈を `ruff` に合わせて整備し、自動修正・手動修正を適用（自動修正約100件＋手動修正）。
- `src/common/mcp/foundry_tool_registry.py` を含む Pydantic v2 対応の調整を反映。

### Fixed
- Pydantic v2 移行に伴う環境変数/設定読み込みの不整合を修正（`model_config` の調整、`Field(..., alias=...)` の適用）。
- リント（`ruff`）関連の多数のスタイル問題を解消し、`ruff check .` が通過する状態にしました。

### Chore
- 依存ロックファイルを更新（`poetry lock` → `poetry.lock` を更新・コミット）。
- `CHANGELOG.md` に今回の作業内容を追記（コミットルールに従い記録）。

### Test
- スモークテストとフルテストを実行し、既存のテストはすべて合格（37 tests passed）。

### Development Notes — Trial & Error

- 2025-12-28 → 2025-12-29: Pydantic v2 移行中に複数の問題が発生。最初の試行では `FoundryConfig` 周辺で環境変数の alias/読み込み順序によりバリデーションエラーが多発し、テストが失敗しました。
  - 対処: `FoundryConfig` を `ConfigDict` と `Field(..., alias=...)` に合わせて書き換え、`model_config` 設定で env_file と prefix の挙動を明確化しました。

- ローカルでの確認中に、コミット/プッシュ時の Git フック（ローカル `.githooks/pre-commit` と `.githooks/pre-push`）が開発フローに影響することが判明しました。
  - 具体的には、`pre-push` が `ruff` を実行しており、スタイル違反があると push がブロックされるため、最初の push が失敗しました。

- `ruff` による静的解析で多数の指摘（W293: 空行末の空白、I001: import 整列、F401/F841: 未使用 import/変数、UP007/B904: 型注釈・例外チェーンの改善など）が報告されました。
  - 対処の流れ:
    1. `poetry run ruff check . --fix` を実行し、自動修正可能な問題を適用（約100件の自動修正）。
    2. 自動修正で残った警告に対して手動修正を実施（例: 未使用プロンプト変数を `_analysis_prompt` に変更、`except ...: raise ... from e` の適用など）。
    3. 行末空白については一括トリム（sed）で削除し、再度 `ruff` を実行して残りを解消しました。

- `pre-commit` はスモークテストを実行する構成のため、コミット時にテストが通ることを確認しつつコミットを積み上げました（各コミットはスモークテスト成功を確認）。

- 依存関係の記述 (`pyproject.toml`) とロックファイル（`poetry.lock`）に差があり、作業の過程で `poetry lock` を実行して `poetry.lock` を更新しました。これにより、CI やフックでの依存解決が安定しました。

- 最終的に、`ruff check .` は全てパスし、スモークテスト・フルテストともに成功した状態で `fix/pydantic-v2-env-alias` ブランチをリモートへプッシュしました。

- 注意点・残件:
  - 本件はスタイル整備・Pydantic v2 対応・ローカルフック運用の改善が中心で、機能的な大規模変更は行っていません。今後、別タスクで追加リファクタリング（型注釈の細部調整、ドキュメントの補完）を検討してください。
  - 本作業で発生したファイル追加（`infra/runner` 等）はドキュメント整備と runner 運用を容易にするためのサンプルです。実運用では GitHub の runner 登録トークンを取得してホストで登録する必要があります。

---

## [0.1.0] - 2025-12-28

### Added
- プロジェクト初期化と Steering 設定（54b1100, 182df49）
- cc-sdd リポジトリを VS Code Git 管理から除外（3c95275）
- プロジェクト基盤・開発環境セットアップ（331bee0）
- 汎用マルチエージェント基盤モジュール実装（ca77c4c）
- 株式ドメイン実装 - Melchior エージェント + FastAPI（c0582cd）
- 包括的テストスイート実装（ffe3f23）
- 包括的ドキュメント整備（b684187）

### Changed
- セマンティックバージョニングと Keep a Changelog 形式の厳格運用を明文化（772d4a6）
- コードフォーマット適用（278060c）

### Fixed
- Pydantic v2 対応と環境変数読み込み修正（dc06b65）
- Pydantic v2 バリデーションエラーに対応したテスト修正（7adbf27）
- `src/stock_magi/agents/melchior_agent.py` の重複関数定義を修正し、Phase 1 実装に復元

### Chore
- Agent Framework 準備: `azure-ai-projects` / `azure-identity` 依存追加、`pyproject.toml` 修正（980e756）
- Phase 1 MVP 完了マーク
- プロジェクト整理・不要サブモジュール除外

### Docs
- 教育用途の方針を追加（1a02f30）

### Test
- Phase 1 MVP: 全37テスト合格、カバレッジ95%

---

## 運用・技術的決定
- 変更履歴は「追記のみ」原則。過去分は編集せず、必要に応じて `git checkout HEAD -- CHANGELOG.md` で復元し追記。
- コミット内容と Changelog の整合性を重視。
- Python と TypeScript の技術的差異は「Python 開発者向け補足」として随時記載。

````
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

## [Unreleased]

No unreleased changes.

## [0.1.1] - 2025-12-29

### Added
- `infra/runner` の systemd スクリプトとコンテナ化サンプルを追加（セルフホスト runner 用）。
- ローカル開発用の Git フック（`.githooks/pre-commit`, `.githooks/pre-push`）およびスモーク/フルテストスクリプトを追加。

### Changed
- コードスタイルと型注釈を `ruff` に合わせて整備し、自動修正・手動修正を適用（約100件の自動修正、残り手動修正を適用）。
- `src/common/mcp/foundry_tool_registry.py` を含む Pydantic v2 対応の調整を反映。

### Fixed
- Pydantic v2 移行に伴う環境変数/設定読み込みの不整合を修正（`model_config` の調整、Field alias の適用）。
- リント（`ruff`）関連の多数のスタイル問題を解消し、`ruff check .` が通過する状態にしました。

### Chore
- 依存ロックファイルを更新（`poetry lock` → `poetry.lock` を更新・コミット）。
- `CHANGELOG.md` に今回の作業内容を追記（コミットルールに従い記録）。

### Test
- スモークテストとフルテストを実行し、既存のテストはすべて合格（37 tests passed）。

### Development Notes — Trial & Error

- 2025-12-28 → 2025-12-29: Pydantic v2 移行中に複数の問題が発生。最初の試行では `FoundryConfig` 周辺で環境変数の alias/読み込み順序によりバリデーションエラーが多発し、テストが失敗しました。
	- 対処: `FoundryConfig` を `ConfigDict` と `Field(..., alias=...)` に合わせて書き換え、`model_config` 設定で env_file と prefix の挙動を明確化しました。

- ローカルでの確認中に、コミット/プッシュ時の Git フック（ローカル `.githooks/pre-commit` と `.githooks/pre-push`）が開発フローに影響することが判明しました。
	- 具体的には、`pre-push` が `ruff` を実行しており、スタイル違反があると push がブロックされるため、最初の push が失敗しました。

- `ruff` による静的解析で多数の指摘（W293: 空行末の空白、I001: import 整列、F401/F841: 未使用 import/変数、UP007/B904: 型注釈・例外チェーンの改善など）が報告されました。
	- 対処の流れ:
		1. `poetry run ruff check . --fix` を実行し、自動修正可能な問題を適用（約100件の自動修正）。
		2. 自動修正で残った警告に対して手動修正を実施（例: 未使用プロンプト変数を `_analysis_prompt` に変更、`except ...: raise ... from e` の適用など）。
		3. 行末空白については一括トリム（sed）で削除し、再度 `ruff` を実行して残りを解消しました。

- `pre-commit` はスモークテストを実行する構成のため、コミット時にテストが通ることを確認しつつコミットを積み上げました（各コミットはスモークテスト成功を確認）。

- 依存関係の記述 (`pyproject.toml`) とロックファイル（`poetry.lock`）に差があり、作業の過程で `poetry lock` を実行して `poetry.lock` を更新しました。これにより、CI やフックでの依存解決が安定しました。

- 最終的に、`ruff check .` は全てパスし、スモークテスト・フルテストともに成功した状態で `fix/pydantic-v2-env-alias` ブランチをリモートへプッシュしました。

- 注意点・残件:
	- 本件はスタイル整備・Pydantic v2 対応・ローカルフック運用の改善が中心で、機能的な大規模変更は行っていません。今後、別タスクで追加リファクタリング（型注釈の細部調整、ドキュメントの補完）を検討してください。
	- 本作業で発生したファイル追加（`infra/runner` 等）はドキュメント整備と runner 運用を容易にするためのサンプルです。実運用では GitHub の runner 登録トークンを取得してホストで登録する必要があります。



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
