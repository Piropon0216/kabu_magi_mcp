# Stock MAGI System - Development Context

**作成日**: 2025-12-28
**対象**: DevContainer 環境で作業を引き継ぐ開発者向け

---

## 🎯 プロジェクト概要

エヴァンゲリオンの MAGI システムをモチーフとした、**3 エージェント合議型株式分析システム**の MVP 実装。

### 目的
1. **Microsoft Agent Framework の教育**: マルチエージェント合議の実装パターンを学ぶ
2. **汎用基盤の構築**: `src/common/` 配下のモジュールを他ドメインに流用可能にする
3. **コード量削減**: Agent Framework 活用により、フルスクラッチ実装の **70% 削減** (1,500 行 → 300-500 行)

---

## 🏗️ アーキテクチャ決定事項

### 技術スタック
| Component | Technology | 理由 |
|-----------|-----------|------|
| **言語** | Python 3.11+ | Agent Framework の最新機能対応 |
| **フレームワーク** | Microsoft Agent Framework (v1.0.0b251223) | マルチエージェント + MCP ネイティブサポート |
| **LLM** | Microsoft Foundry (GPT-4o) | モデル管理 GUI、コスト追跡、プロンプト実験 |
| **API** | FastAPI | 高速、非同期、自動 OpenAPI 生成 |
| **MCP** | Agent Framework MCP Plugin | ネイティブ MCP 統合 |
| **デプロイ** | Azure Container Apps | Python 最適化、Auto-scaling、min replicas=0 |
| **テスト** | pytest + pytest-asyncio | Python 標準 |
| **Linter** | Ruff | 超高速 Linter + Formatter |

### アーキテクチャパターン
```
src/
├── common/              # ドメイン非依存の汎用基盤（他プロジェクトに流用可能）
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
    │   ├── balthasar_agent.py  # バランス型分析
    │   └── casper_agent.py     # テクニカル分析
    ├── prompts/         # エージェント用プロンプト
    └── api/             # FastAPI エンドポイント
        └── endpoints.py
```

---

## 🚨 重要な制約と決定

### 1. Agent Framework プレリリース版の使用
- **バージョン固定**: `agent-framework-azure-ai = "1.0.0b251223"` (pyproject.toml)
- **リスク軽減策**:
  - Microsoft Foundry Portal (https://ai.azure.com/) で GUI ベースのモデル管理
  - DevUI (Agent Framework 付属) でエージェント動作のビジュアルデバッグ
  - コード依存を最小化し、GUI ツールで補完

### 2. データソース戦略
| Phase | データソース | 実装方法 |
|-------|------------|---------|
| **Phase 1 (MVP)** | Morningstar | Foundry Tool Catalog (GUI ベース設定のみ) |
| **Phase 2** | Yahoo Finance | npm MCP Server (`@modelcontextprotocol/server-yahoo-finance`) |
| **Phase 3** | Jquants + DuckDB | DuckDB MCP Server + カスタム統合 |

**重要**: MVP では Morningstar (Foundry Tool Catalog) のみ使用。Yahoo Finance は Phase 2 で追加。

**実装の簡素化**:
- Morningstar は Foundry Portal (https://ai.azure.com/) で GUI 設定するのみ
- MCP Server のローカル実行、npm インストール不要 (Phase 1)
- Agent Framework が Foundry Tool を自動的に統合

### 3. Copilot+ PC (ARM64) 対応
- **DevContainer 使用**: `.devcontainer/devcontainer.json` で ARM64 Python 環境を構築
- **ベースイメージ**: `mcr.microsoft.com/devcontainers/python:3.11-bullseye`
- **自動セットアップ**: Poetry + Node.js (MCP サーバー用)

---

## 📋 Phase 1 実装計画 (MVP)

### 目標成果物
- 1 エージェント (Melchior) + FastAPI エンドポイント + ローカルテスト動作
- **推定コード量**: 150-200 行 (Agent Framework 活用)

### 実装タスク
1. **Task 1.1**: Project Initialization
   - `pyproject.toml` 作成 (Poetry)
   - 依存関係: `agent-framework-azure-ai --pre`, `fastapi`, `uvicorn`, `ruff`
   - `.env.example` 作成

2. **Task 2**: Common Framework
   - `src/common/mcp/plugin_registry.py` - MCP サーバー統合管理
   - `src/common/consensus/orchestrators/group_chat_consensus.py` - 汎用合議エンジン
   - `src/common/models/decision_models.py` - Pydantic モデル

3. **Task 3**: Melchior Agent
   - `src/stock_magi/agents/melchior_agent.py` - エージェント定義
   - `src/stock_magi/prompts/stock_analysis_prompts.py` - プロンプト定義

4. **Task 4**: FastAPI Endpoint
   - `src/stock_magi/api/endpoints.py` - POST /api/analyze
   - `src/main.py` - アプリケーションエントリーポイント

5. **Task 5-6**: Testing & Documentation
   - pytest テスト (unit + integration + E2E)
   - Dockerfile
   - `docs/MVP_SETUP.md`

---

## 🔧 必須の手動作業 (実装前)

### 1. Microsoft Foundry セットアップ (約 20 分)
```
1. Azure Portal (https://portal.azure.com/) にログイン
2. Microsoft Foundry Portal (https://ai.azure.com/) を開く
3. 「Create new project」で新規プロジェクト作成
4. GPT-4o モデルをデプロイ:
   - Model catalog → gpt-4o → Deploy
   - Deployment name: "gpt-4o" (推奨)
5. Morningstar MCP Server を追加 (Phase 1 MVP):
   - Tool Catalog → "Morningstar MCP Server" を検索
   - "Add to project" をクリック
   - 設定はデフォルトで OK
6. API キーと Endpoint URL を取得:
   - プロジェクト設定 → Keys and Endpoint
```

### 2. 環境変数の設定 (実装後)
実装完了後、プロジェクトルートに `.env` ファイルを作成:

```bash
FOUNDRY_ENDPOINT=https://<your-project>.openai.azure.com/
FOUNDRY_API_KEY=<your-api-key>
FOUNDRY_DEPLOYMENT=gpt-4o
```

---

## 📚 参考ドキュメント

### 関連ファイル
- **要件定義**: `.kiro/specs/stock-magi-system-ja/requirements.md`
- **技術設計**: `.kiro/specs/stock-magi-system-ja/design.md`
- **タスクリスト**: `.kiro/specs/stock-magi-system-ja/tasks.md`
- **技術方針**: `.kiro/steering/tech.md`
- **プロジェクト構造**: `.kiro/steering/structure.md`

### 公式ドキュメント
- Agent Framework: https://github.com/microsoft/agent-framework
- Microsoft Foundry: https://learn.microsoft.com/azure/ai-studio/
- MCP Protocol: https://modelcontextprotocol.io/

---

## 🚀 DevContainer での開始手順

```bash
# 1. DevContainer でコンテナを開く (VS Code)
# 「Dev Containers: Reopen in Container」を実行

# 2. Poetry で依存関係をインストール
poetry install

# 3. 環境変数を設定
cp .env.example .env
# .env を編集して Foundry の認証情報を入力

# 4. 開発サーバーを起動
poetry run uvicorn src.main:app --reload

# 5. API テスト
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "7203.T"}'
```

---

## 💡 実装のポイント

### Agent Framework の活用
- **GroupChatOrchestrator**: 合議機能は組み込み済み、カスタム実装不要
- **MCPServerPlugin**: MCP サーバーの接続は 1 行で完結
- **Agent**: エージェント定義は system message + plugin の組み合わせのみ

### コード例 (Melchior エージェント定義)
```python
from agent_framework import Agent

def create_melchior_agent(mcp_plugin):
    return Agent(
        name="Melchior",
        system_message="あなたは基本的な株式分析を担当する AI エージェントです...",
        plugins=[mcp_plugin]
    )
```

### コード削減の理由
- **Hexagonal Architecture (自作)**: ~1,500 行
  - Ports/Adapters/Core の手動実装
  - MCP クライアントの自作
  - 合議ロジックの自作

- **Agent Framework (今回)**: ~300-500 行
  - GroupChat 組み込み機能
  - MCP ネイティブサポート
  - エージェント定義の簡素化

---

## ⚠️ トラブルシューティング

### ARM64 環境での注意点
- 一部 Python パッケージは ARM64 ネイティブビルドが必要
- DevContainer の Python イメージは ARM64 対応済み
- Poetry は自動的に適切なパッケージを選択

### Agent Framework プレリリース版
- バージョンが固定されているため、`poetry update` は慎重に実行
- 問題が発生した場合は Foundry Portal/DevUI で GUI デバッグ

---

## 📝 次のステップ

### Phase 1 完了後
1. Balthasar エージェント実装 (Phase 2)
2. Casper エージェント実装 (Phase 2)
3. 加重投票ロジック実装 (Phase 2)
4. モーニングスター MCP Server 実装 (Phase 2)

### Phase 2 完了後
1. Azure Container Apps デプロイ (Phase 3)
2. DuckDB 統合 (Phase 3)
3. CI/CD パイプライン構築 (Phase 3)

---

## 🎓 学習リソース

### このプロジェクトで学べること
1. **Microsoft Agent Framework**: マルチエージェント合議の実装パターン
2. **MCP Protocol**: MCP サーバーの統合方法
3. **Microsoft Foundry**: LLM モデルの管理とデプロイ
4. **Reusable Architecture**: ドメイン非依存な基盤設計
5. **Python + FastAPI**: 非同期 API 開発

### 推奨学習順序
1. Phase 1 実装を通じて Agent Framework の基礎を理解
2. `docs/AGENT_FRAMEWORK_GUIDE.md` で詳細を学習 (Phase 1 完了後作成)
3. `docs/MCP_INTEGRATION.md` で MCP の仕組みを理解
4. `docs/REUSABILITY_GUIDE.md` で他ドメインへの応用を学習

---

**このドキュメントは実装進捗に応じて更新されます。**
