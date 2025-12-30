# Tasks — Pydantic v2 対応ワーク

ブランチ: `fix/pydantic-v2-env-alias`

最終更新: 2025-12-28

## 現状（完了した主要作業）
- ブランチ `fix/pydantic-v2-env-alias` を作成して作業を隔離しました。
- `src/common/mcp/foundry_tool_registry.py` の `FoundryConfig` に対して、Pydantic v2 で環境変数が確実にバインドされるように以下を実施しました:
  - `foundry_endpoint: str = Field(..., alias="FOUNDRY_ENDPOINT")` など、各フィールドに `alias` を明示
  - `model_config` は `env_file=None` のみを残す（`.env` の勝手な注入を避けるため）
  - `pydantic` の `Field` を import して NameError を解消
- テスト環境の安定化のため、`tests/conftest.py` の fixture で `FOUNDRY_` 環境変数をテスト毎に明示的にセットするようにして、環境変数の漏洩やテスト間干渉を防止しました。
- 全テストを実行し（`PYTHONPATH=./src poetry run pytest -v`）、現時点で全テストがパスしました。
- `CHANGELOG.md` をセマンティックバージョニングに従って更新し、今回の修正を `1.0.1` として記録しました。

## 残タスク（優先度順）
1. Open PR for review (高)
   - ブランチ `fix/pydantic-v2-env-alias` から main へ Pull Request を作成
   - PR の説明に今回の背景、試行錯誤、影響範囲、テスト結果を添える
   - CI（pytest, ruff, mypy）を実行し、問題なければレビュー依頼
   - コマンド例:
```bash
git push origin fix/pydantic-v2-env-alias
# GitHub CLI があれば:
gh pr create --base main --head fix/pydantic-v2-env-alias --title "fix: pydantic v2 env alias for FoundryConfig" --body "...詳細..."
```

2. CI and integration checks (中)
   - CI 設定があれば PR 上で全チェックを実行
   - コンテナイメージやデプロイ環境に差分がないか確認

3. Audit other BaseSettings usages (中)
   - リポジトリ全体で `BaseSettings` / `pydantic` を使っている箇所を検索
   - v2移行に伴う破壊的変更が残っていないかを列挙
   - 必要なら同様の alias 対応か、`pydantic` バージョン固定を検討
   - コマンド例:
```bash
rg "BaseSettings|pydantic" -S
```

4. Decide long-term pydantic strategy (中〜低)
   - 運用方針を決定：
     - 全面で v2 に移行し alias を追加する（工数大）
     - 一時的に `pydantic<2.0` に pin して段階的移行する
   - ドキュメントと開発ガイドに反映

5. Consider LLM-assisted review (低)
   - 高性能LLMにPRの差分レビューや移行箇所の自動検出を依頼することは有効です。
   - ただし、次の点で必ず人間が最終判断する必要があります:
     - シークレットや環境変数（APIキー等）の取り扱い
     - 影響範囲の妥当性（ビルド / CI の挙動）
     - セキュリティと運用手順

## LLM（高性能モデル）利用に関する私見
- 何を任せるべきか:
  - 大量の差分から互換性問題を検出するスキャン（例: `BaseSettings` の全出現箇所に対する修正案）
  - PR本文の自動生成（変更理由、影響範囲、テスト結果の要約）
  - 単純なルールベースの修正（例: `env_prefix` → `Field(..., alias=...)` 変換提案の草案）

- 人間がやるべきこと:
  - シークレットの確認・除外（LLMに秘密を与えない）
  - 本番環境での動作検証、デプロイ前の安全チェック
  - 最終的なコードレビューと承認

- 結論:
  - プレミアムの高性能LLMが利用可能になったら、**スキャン・提案・PRドラフト作成**など多くの反復作業を任せる価値は高いです。
  - ただし、マージと本番反映は必ず人間の判断に依存してください。

## 次のアクション提案（すぐできる）
1. ローカルで再度テストと lint を実行して、CIで同一挙動かを確認
```bash
PYTHONPATH=./src poetry run pytest -q
poetry run ruff check src tests
poetry run mypy src
```
2. `fix/pydantic-v2-env-alias` をリモートへ push して PR を作成
3. PR にこの `tasks.md` と `CHANGELOG.md` の要約を添えてレビュー依頼

---

必要なら、私の方で PR を作成（`gh` が使える環境なら可）し、CI が回るまで監視して自動でコメントや修正提案を追加することもできます。対応希望を教えてください。
