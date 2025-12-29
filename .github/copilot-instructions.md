## 開発者向け重要指示（自動エージェント / Copilot 向け）

このファイルはリポジトリ直下の `.github/` に置くことで、Human や自動エージェントが最初に確認すべき重要手順をまとめています。

必ず目を通してください：特にテスト実行や devcontainer の再ビルド手順はこのとおり実行してください。

---

### 1) ローカル（Poetry 仮想環境）でのテスト実行

依存関係と dev-deps は `poetry` で管理しています。プロジェクトルートで次を実行してください：

```bash
# 仮想環境作成 / シェルで有効化済みの場合
poetry install
poetry run pytest
```

特定テストだけ実行する例：

```bash
poetry run pytest tests/test_foundry_tool_registry.py::test_list_available_tools -q
```

カバレッジ HTML を生成する例：

```bash
poetry run pytest --cov=src --cov-report=html
```

> 注意: `pyproject.toml` の `tool.pytest.ini_options.addopts` に coverage オプションが含まれるため、直接 `pytest` を呼ぶと環境によりプラグイン不足で失敗することがあります。必ず `poetry run pytest` を推奨します。

### 2) 開発コンテナ（Dev Container）でテストする場合

VS Code の Dev Container を使う場合は、コンテナを再ビルドしてからテスト実行してください：

1. コマンドパレット → `Dev Containers: Rebuild Container` を選択
2. コンテナ内ターミナルで：

```bash
poetry install
poetry run pytest
```

devcontainer には GitHub CLI (`gh`) をインストールする feature を追加しています。
問題がある場合は、コンテナ内で次を実行して手動でインストールできます：

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install -y gh
```

### 3) テスト用の環境変数

テストは `tests/conftest.py` の autouse fixture により、`FOUNDRY_` で始まる環境変数をテスト毎に明示的にセットします。
実行時に独自の Foundry 設定を使いたい場合は、環境変数を適切に上書きしてください（ただし CI ではテストの再現性保持のためデフォルト fixture を尊重してください）。

### 4) CI の設定について


このリポジトリにはセルフホスト向けの CI ワークフロー `./github/workflows/ci-self-hosted.yml` を追加済みです。

セルフホストランナーのメリット:
- GitHub の有料実行分を消費しない（GitHub Actions の課金対象外）
- 自分のインフラで自由に実行できるためコスト制御が可能

注意点（重要）:
- セルフホストランナーはご自身でマシンを用意し、リポジトリに runner を登録する必要があります。マシンは常時起動している必要はありませんが、実行中にジョブを受信できる状態である必要があります。
- セキュリティ: セルフホストランナー上では任意のジョブが実行されうるため、パブリックリポジトリや未審査ブランチでは信頼できるランナーのみを使ってください。

簡易セットアップ手順（セルフホストランナー）:

1. GitHub リポジトリの Settings → Actions → Runners → New self-hosted runner を開く
2. OS とアーキテクチャを選び、表示される登録コマンドを実行する（例: `./config.sh --url https://github.com/OWNER/REPO --token XXX`）
3. ランナーをサービスとして登録して常時稼働させる（任意）

ワークフローファイルのポイント:
- ファイル: `.github/workflows/ci-self-hosted.yml`
- 実行環境: `runs-on: [self-hosted, linux]`（自分で用意するランナーが実行されます）
- ステップ: Checkout → Poetry install → `ruff` → `mypy` → `pytest`

もし希望であれば、私がランナーのための Docker コンテナ定義（systemd もしくは runner を常駐させるスクリプト）や、簡易の Ansible/Cloud-Init スニペットを作成します。どれを希望しますか？

---

このファイルは自動エージェント（Copilot / CI）や新しい開発者が最初に開くことを想定しています。必要に応じて簡潔に追記してください。
