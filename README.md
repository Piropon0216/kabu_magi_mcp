# Stock MAGI System

MAGI システムをモチーフとした、3 エージェント合議型株式分析システム (MVP)

## 🎯 概要

Stock MAGI System は、エヴァンゲリオンの MAGI システムに着想を得た **Microsoft Agent Framework ベースのマルチエージェント株式分析プラットフォーム**です。3 つの AI エージェント (Melchior, Balthasar, Casper) が異なる視点で株式を分析し、合議により投資判断を提供します。

### プロジェクトの目的
1. **Microsoft Agent Framework の教育**: マルチエージェント合議の実装パターンを学ぶ
2. **汎用基盤の構築**: `src/common/` 配下のモジュールを他ドメインに流用可能にする
3. **コード量削減**: Agent Framework 活用により、フルスクラッチ実装の **70% 削減** (1,500 行 → 300-500 行)

## ✨ 主な特徴

- 🤖 **3 エージェント合議**: Melchior (基本分析)、Balthasar (バランス型)、Casper (テクニカル分析)
- 🔄 **Agent Framework 活用**: GroupChatOrchestrator による組み込み合議機能
- 🔌 **MCP ネイティブ統合**: MCPServerPlugin で Yahoo Finance/モーニングスター/DuckDB に接続
- ☁️ **Microsoft Foundry**: GUI ベースのモデル管理、プロンプト実験、コスト追跡
- 🏗️ **再利用可能設計**: `src/common/` は不動産分析・医療診断など他ドメインに流用可能
- 🧪 **完全 TDD**: pytest + pytest-asyncio でテストカバレッジ 80%+

## 🛠️ 技術スタック

- **言語**: Python 3.11+
- **フレームワーク**: Microsoft Agent Framework (v1.0.0b251223 - プレリリース版バージョン固定)
- **LLM**: Microsoft Foundry (GPT-4o)
- **API**: FastAPI (非同期、自動 OpenAPI 生成)
- **MCP**: Agent Framework MCP Plugin (ネイティブサポート)
- **デプロイ**: Azure Container Apps (Python 最適化、Auto-scaling、min replicas=0)
- **テスト**: pytest + pytest-asyncio + unittest.mock
- **Linter**: Ruff (超高速 Linter + Formatter)

## 📋 開発フェーズ

### Phase 1: MVP - Common Framework + 1 Agent (Week 1-2) ✅ 進行中
- ✅ DevContainer セットアップ (ARM64 対応)
- ✅ Poetry プロジェクト初期化
- 🔲 Common Framework 実装 (MCPPluginRegistry, ReusableConsensusOrchestrator)
- 🔲 Melchior エージェント実装 (基本的分析)
- 🔲 FastAPI エンドポイント (`POST /api/analyze`)
- 🔲 pytest テスト + Dockerfile

**目標**: 1 エージェント + FastAPI + ローカルテスト動作 (推定コード量: 150-200 行)

### Phase 2: Multi-Agent System (Week 3) 🔜
- 🔲 Balthasar エージェント (バランス型分析)
- 🔲 Casper エージェント (テクニカル分析)
- 🔲 加重投票ロジック実装
- 🔲 **モーニングスター MCP Server 実装** (カスタム実装)

### Phase 3: Azure Deployment + DuckDB (Week 4) 🔜
- 🔲 Azure Container Apps デプロイ (Bicep)
- 🔲 DuckDB MCP Server 統合 (Jquants API)
- 🔲 GitHub Actions CI/CD

---

## 🚀 クイックスタート (DevContainer)

### 前提条件
- ✅ Docker Desktop インストール済み
- ✅ VS Code + Dev Containers 拡張機能
- ✅ Microsoft Foundry プロジェクト作成済み ([セットアップ手順](docs/CONTEXT.md#必須の手動作業-実装前))

### 1. DevContainer で開く
```bash
# VS Code で Ctrl+Shift+P → "Dev Containers: Reopen in Container"
# ARM64 (Copilot+ PC) 環境で自動的に適切な Python イメージを使用
```

### 2. 依存関係のインストール
```bash
# Poetry で Python パッケージをインストール
poetry install

# MCP サーバー (Yahoo Finance) をインストール
npm install -g @modelcontextprotocol/server-yahoo-finance
```

### 3. 環境変数の設定
```bash
cp .env.example .env
# .env を編集して Microsoft Foundry の認証情報を入力:
# FOUNDRY_ENDPOINT=https://your-project.openai.azure.com/
# FOUNDRY_API_KEY=your-api-key-here
# FOUNDRY_DEPLOYMENT=gpt-4o
```

### 4. 開発サーバーの起動
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. API テスト
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "7203.T", "include_reasoning": true}'
```

---

## 🏗️ アーキテクチャ

```
src/
├── common/              # ドメイン非依存の汎用基盤 (他プロジェクトに流用可能)
│   ├── consensus/       # 合議エンジン
│   │   ├── orchestrators/
│   │   │   └── group_chat_consensus.py  # ReusableConsensusOrchestrator
│   │   └── strategies/
│   │       └── voting_strategy.py       # VotingStrategy 抽象化
│   ├── mcp/             # MCP プラグイン管理
│   │   └── plugin_registry.py           # MCPPluginRegistry
│   └── models/          # 共通データモデル
│       └── decision_models.py           # Action, AgentVote, FinalDecision
│
└── stock_magi/          # 株式ドメイン固有実装
    ├── agents/          # エージェント定義
    │   ├── melchior_agent.py   # 基本的分析
    │   ├── balthasar_agent.py  # バランス型分析 (Phase 2)
    │   └── casper_agent.py     # テクニカル分析 (Phase 2)
    ├── prompts/         # エージェント用プロンプト
    └── api/             # FastAPI エンドポイント
        └── endpoints.py
```

### データソース戦略
| Phase | データソース | 実装方法 |
|-------|------------|---------|
| **Phase 1 (MVP)** | Yahoo Finance | MCP Server (`@modelcontextprotocol/server-yahoo-finance`) |
| **Phase 2** | モーニングスター | カスタム MCP Server 実装 (REST API ラップ) ※公式コネクタなし |
| **Phase 3** | Jquants + DuckDB | DuckDB MCP Server + カスタム統合 |

---

## 🧪 テスト

```bash
# 全テスト実行
poetry run pytest

# カバレッジ付き
poetry run pytest --cov=src --cov-report=html

# 特定のテストのみ実行
poetry run pytest tests/test_melchior_agent.py
```

---

## 📝 開発ガイドライン

### コードスタイル
```bash
# Ruff でフォーマット
poetry run ruff format src/

# Ruff でリント
poetry run ruff check src/ --fix

# 型チェック
poetry run mypy src/
```

---

## 📚 ドキュメント

- **[CONTEXT.md](docs/CONTEXT.md)**: プロジェクト全体のコンテキスト (必読)
  - アーキテクチャ決定事項
  - Phase 別実装計画
  - ARM64 環境対応
  - リスク軽減策 (プレリリース版使用時)
- **要件定義**: `.kiro/specs/stock-magi-system-ja/requirements.md`
- **技術設計**: `.kiro/specs/stock-magi-system-ja/design.md`
- **タスクリスト**: `.kiro/specs/stock-magi-system-ja/tasks.md`

---

## 🎓 学習リソース

### このプロジェクトで学べること
1. **Microsoft Agent Framework**: マルチエージェント合議の実装パターン
2. **MCP Protocol**: MCP サーバーの統合方法
3. **Microsoft Foundry**: LLM モデルの管理とデプロイ
4. **Reusable Architecture**: ドメイン非依存な基盤設計
5. **Python + FastAPI**: 非同期 API 開発

### 推奨学習順序
1. [CONTEXT.md](docs/CONTEXT.md) でプロジェクト全体を理解
2. Phase 1 実装を通じて Agent Framework の基礎を習得
3. `docs/AGENT_FRAMEWORK_GUIDE.md` で詳細を学習 (Phase 1 完了後作成)
4. `docs/REUSABILITY_GUIDE.md` で他ドメインへの応用を学習

---

## ⚠️ 注意事項

### Agent Framework プレリリース版
- **バージョン固定**: `agent-framework-azure-ai = "1.0.0b251223"` (pyproject.toml)
- **リスク軽減策**:
  - Microsoft Foundry Portal (https://ai.azure.com/) で GUI ベースのモデル管理
  - DevUI (Agent Framework 付属) でエージェント動作のビジュアルデバッグ
  - コード依存を最小化し、GUI ツールで補完

### ARM64 環境 (Copilot+ PC)
- DevContainer で自動的に ARM64 対応 Python イメージを使用
- Poetry が適切なパッケージを自動選択

---

## 💰 コスト見積もり

**Phase 1 (MVP)**: 月額 **$3-10**
- Azure Container Apps (min replicas=0): ~$2
- Microsoft Foundry (GPT-4o): ~$5-8 (推論トークン従量課金)

---

## 🤝 コントリビューション

Phase 1 完了後、他ドメインへの応用例を `docs/REUSABILITY_GUIDE.md` に追加予定。

---

## 📄 ライセンス

MIT License

---

## 🙏 謝辞

- **Microsoft Agent Framework** チームに感謝
- **Model Context Protocol** コミュニティに感謝
- **エヴァンゲリオン** の MAGI システムにインスパイア

---

## 📞 サポート

質問や問題が発生した場合は、[CONTEXT.md](docs/CONTEXT.md) の「トラブルシューティング」セクションを参照してください。
