# Research & Design Decisions

---
**Purpose**: Stock MAGI Systemの技術設計に関する調査結果と設計判断の根拠を記録する。

**Usage**: 設計フェーズの調査活動と成果を文書化し、将来の監査や再利用のためのエビデンスを提供する。
---

## Summary
- **Feature**: `stock-magi-system-ja`
- **Discovery Scope**: 新規機能（Complex Integration - Multi-agent System with MCP Protocol）
- **Key Findings**:
  - **🎯 Microsoft Agent Framework採用**: 組み込みMulti-Agent OrchestrationとMCPネイティブ統合でコード量を70%削減
  - **再利用可能な共通基盤**: 合議エンジンとMCP統合モジュールを汎用化し、株式以外のドメインにも適用可能
  - Microsoft Foundry (旧 Azure AI Foundry) でモデル管理、Python推奨（最新機能が豊富）
  - Agent Framework のGroupChatOrchestrator/SequentialOrchestratorで合議機能を実装
  - MCPプロトコルはAgent Framework のPlugin Ecosystemでネイティブサポート
  - DuckDB統合もMCPプラグインとして実装可能

## Research Log

### Microsoft Agent Framework Investigation
- **Context**: マルチエージェントシステムの実装方法調査（フルスクラッチ vs フレームワーク活用）
- **Sources Consulted**: 
  - Microsoft Agent Framework Documentation (github.com/microsoft/agent-framework)
  - Azure AI Agent Service Best Practices
  - AI Toolkit Agent Code Generation Guidelines
- **Findings**:
  - **Agent Framework の主要機能**:
    - Multi-Agent Orchestration: GroupChat, Sequential, Concurrent, Handoff patterns
    - Plugin Ecosystem: Native functions, OpenAPI, **Model Context Protocol (MCP)** サポート
    - LLM Support: Microsoft Foundry, Azure OpenAI, OpenAI, Anthropic
    - Cross-Platform: Python (推奨・最新機能多数) / .NET
  - **コード削減効果**:
    - 自前Orchestrator実装 (約1,500行) → Agent Framework使用 (約300-500行) = **70%削減**
    - 組み込みGroupChatOrchestratorで合議機能を実装
    - MCP統合がネイティブサポート（自前ラッパー不要）
  - **インストール** (Python推奨):
    ```bash
    pip install agent-framework-azure-ai --pre
    ```
    ⚠️ `--pre` フラグ必須（プレビュー期間中）
- **Implications**:
  - **アーキテクチャ変更**: Hexagonal Architecture → Agent Framework ベースに簡略化
  - **エージェント実装**: `Agent` クラスを継承、`system_message` でペルソナ定義
  - **合議機能**: `GroupChatOrchestrator` で3エージェントの討論を実現
  - **MCP統合**: Plugin Ecosystem の MCP サポートを直接利用

### Reusable Multi-Agent Consensus Module Design
- **Context**: 株式分析以外のドメインにも流用可能な汎用合議モジュールの設計
- **Sources Consulted**:
  - Agent Framework Multi-Agent Patterns (Reflection, Fan-out/Fan-in)
  - Generic Orchestration Patterns
- **Findings**:
  - **汎用化の鍵**:
    - エージェントの「ペルソナ」と「ドメインロジック」を分離
    - 合議アルゴリズムをドメイン非依存に設計（投票、重み付け、信頼度集約）
    - MCP統合を抽象化（データソース種別に依存しない）
  - **共通基盤モジュール構成**:
    ```
    src/common/
      consensus/
        orchestrators/
          group_chat_consensus.py      # GroupChat型合議
          sequential_consensus.py      # 順次型合議
        strategies/
          voting_strategy.py           # 投票戦略（多数決、重み付け）
          confidence_aggregation.py    # 信頼度集約
      mcp/
        plugin_registry.py             # MCPプラグイン管理
        data_source_adapter.py         # 汎用データソースアダプター
    ```
  - **株式ドメイン固有部分**:
    ```
    src/stock_magi/
      agents/
        melchior_agent.py              # ファンダメンタルズ分析ペルソナ
        balthasar_agent.py             # バランス分析ペルソナ
        casper_agent.py                # テクニカル分析ペルソナ
      prompts/
        stock_analysis_prompts.py      # 株式分析用プロンプトテンプレート
    ```
- **Implications**:
  - **Phase 1**: 共通基盤モジュール（`src/common/`）を先に実装
  - **Phase 2**: 株式ドメイン固有実装（`src/stock_magi/`）を追加
  - **将来拡張**: 他ドメイン（例: 不動産分析、医療診断支援）は `src/<domain>/` 追加のみ

### Runtime and Deployment Architecture
- **Context**: Agent Framework アプリケーションのデプロイ方法調査
- **Sources Consulted**:
  - Agent Framework Deployment Documentation
  - Azure Container Apps Best Practices
- **Findings**:
  - **推奨ランタイム**: Azure Container Apps (Pythonベースアプリに最適)
    - FastAPI/Flask でREST API提供
    - Agent Framework エージェントをバックエンドサービスとして実行
    - Auto-scaling、低コスト（従量課金）
  - **代替案**: Azure Functions (Python)
    - HTTP Trigger で分析リクエスト受付
    - Agent Framework を Functions 内で実行可能
    - ただし実行時間制限（最大10分）に注意
  - **ローカル開発**: FastAPI + Agent Framework
    ```python
    from fastapi import FastAPI
    from agent_framework import Agent, GroupChatOrchestrator
    
    app = FastAPI()
    
    @app.post("/api/analyze")
    async def analyze(ticker: str):
        # Agent Framework でマルチエージェント実行
        result = await orchestrator.run(ticker)
        return result
    ```
- **Implications**:
  - **MVP**: FastAPI + Azure Container Apps
  - **Phase 2**: Azure Functions オプション追加（軽量リクエスト用）
  - TypeScript → Python 変更（Agent Framework のPython実装が最新機能豊富）

### Model Context Protocol (MCP) with Agent Framework
- **Context**: Agent Framework のMCPネイティブ統合パターンの調査
- **Sources Consulted**:
  - Agent Framework MCP Plugin Documentation
  - MCP公式ドキュメント
  - github.com/microsoft/agent-framework MCP samples
- **Findings**:
  - **Agent Framework MCP統合**:
    - Plugin Ecosystem で MCP プロトコルをネイティブサポート
    - `MCPServerPlugin` クラスで MCP サーバーに接続
    - エージェントが自動的に MCP ツールを利用可能
    ```python
    from agent_framework import Agent
    from agent_framework.plugins.mcp import MCPServerPlugin
    
    # MCP サーバー接続
    mcp_plugin = MCPServerPlugin(
        server_command="npx @modelcontextprotocol/server-yahoo-finance"
    )
    
    # エージェントに MCP プラグイン追加
    agent = Agent(
        name="Melchior",
        plugins=[mcp_plugin]  # 自動的に株価取得ツール利用可能
    )
    ```
  - **汎用MCPアダプター設計**:
    - データソース種別（株式、クラウドドキュメント、DB）に依存しない抽象化
    - `src/common/mcp/plugin_registry.py` で統一管理
  - **複数MCPサーバー対応**: 1エージェントに複数MCPプラグイン登録可能
- **Implications**:
  - **自前MCPラッパー不要**: Agent Framework の組み込み機能を直接利用
  - **MVP Phase 1**: Yahoo Finance MCP サーバー1つ
  - **Phase 2**: Azure Docs MCP サーバー追加
  - **Phase 3**: DuckDB MCP サーバー追加（コネクタ確定後）

### Multi-Agent Consensus with GroupChatOrchestrator
- **Context**: Agent Framework のGroupChatOrchestratorを使った合議機能の設計
- **Sources Consulted**:
  - Agent Framework GroupChat Documentation
  - Multi-agent orchestration patterns
- **Findings**:
  - **GroupChatOrchestrator の特徴**:
    - 複数エージェントが順番に発言し、討論形式で結論を出す
    - Termination条件（最大ターン数、合意検出）を設定可能
    - エージェント間のメッセージ履歴を自動管理
  - **汎用合議エンジン設計**:
    ```python
    # src/common/consensus/orchestrators/group_chat_consensus.py
    from agent_framework import GroupChatOrchestrator, Agent
    from typing import List, Dict
    
    class ReusableConsensusOrchestrator:
        """ドメイン非依存の合議エンジン"""
        
        def __init__(self, agents: List[Agent], voting_strategy: str = "majority"):
            self.agents = agents
            self.voting_strategy = voting_strategy
            self.orchestrator = GroupChatOrchestrator(agents=agents)
        
        async def reach_consensus(self, input_context: Dict) -> Dict:
            """汎用合議実行"""
            # GroupChat で討論
            discussion = await self.orchestrator.run(input_context)
            
            # 投票戦略で最終判断
            final_decision = self._apply_voting_strategy(discussion)
            return final_decision
    ```
  - **株式ドメイン適用**:
    - 3エージェント（Melchior, Balthasar, Casper）をGroupChatに登録
    - 銘柄コードをコンテキストとして渡し、討論開始
    - 最終的に Buy/Sell/Hold + 信頼度を返却
- **Implications**:
  - **自前Consensus Engine不要**: GroupChatOrchestrator活用
  - **汎用性**: 株式以外（不動産、医療など）でも同じオーケストレーター使用可能
  - **Phase 1**: 単純多数決投票
  - **Phase 2**: 重み付け投票、信頼度ベース集約

### Microsoft Foundry (旧 Azure AI Foundry) Integration
- **Context**: モデル管理とデプロイのためのMicrosoft Foundry調査
- **Sources Consulted**:
  - Microsoft Foundry Documentation
  - Agent Framework + Foundry integration patterns
- **Findings**:
  - **Foundry の主要機能**:
    - モデルカタログ: GPT-4o, Claude, Llama など統一管理
    - プロンプトフロー: エージェントプロンプトの実験・評価
    - エンドポイント管理: モデルデプロイと推論API提供
    - コスト追跡: トークン使用量・コストの可視化
  - **Agent Framework 統合**:
    ```python
    from agent_framework_azure_ai import AzureAIClientConfiguration
    
    config = AzureAIClientConfiguration(
        endpoint=os.getenv("FOUNDRY_ENDPOINT"),
        api_key=os.getenv("FOUNDRY_API_KEY"),
        deployment="gpt-4o"
    )
    
    agent = Agent(name="Melchior", model_client=config)
    ```
  - **教育的価値**: 
    - Python初学者向けに Foundry UI でプロンプト調整 → コード化の流れ
    - コスト最適化の可視化（トークン数、推論時間）
- **Implications**:
  - **MVP**: Microsoft Foundry プロジェクト作成、GPT-4o デプロイ
  - **Phase 2**: プロンプトフローで3エージェントのプロンプト最適化
  - **教育ドキュメント**: `docs/FOUNDRY_GUIDE.md` 作成

### Python Best Practices for Agent Development
- **Context**: Python開発環境とコーディング規約の調査
- **Sources Consulted**:
  - Agent Framework Python Documentation
  - Python Type Hints Best Practices
- **Findings**:
  - **推奨Python環境**:
    - Python 3.11+ (Agent Framework 要件)
    - Poetry または pip-tools で依存管理
    - Ruff (linter + formatter) で高速コード品質管理
  - **型ヒント必須**:
    ```python
    from typing import List, Dict, Optional
    from agent_framework import Agent
    
    async def analyze_stock(
        ticker: str,
        agents: List[Agent]
    ) -> Dict[str, Any]:
        """株式分析実行（型ヒント必須）"""
        ...
    ```
  - **非同期パターン**: Agent Framework は async/await ベース
  - **エラーハンドリング**: カスタム例外クラスで種別を区別
- **Implications**:
  - **言語変更**: TypeScript → Python (Agent Framework のPython実装が最新)
  - **開発環境**: Poetry + Ruff + pytest
  - **教育ドキュメント**: `docs/PYTHON_GUIDE.md` (Python初学者向け)
  - TypeScript Steering は参考として保持（Azure Functions オプション用）

### DuckDB Integration Planning
- **Context**: Phase 3でのDuckDB統合準備とインターフェース設計
- **Sources Consulted**:
  - DuckDB公式ドキュメント
  - Jquants API連携パターン
- **Findings**:
  - **DuckDB特徴**: 分析用OLAP DB、高速SQL実行、ファイルベース
  - **MCP統合**: DuckDB用MCPサーバー経由でSQL問い合わせ実行
  - **データソース**: Jquants APIからの時系列株式データ
  - **インターフェース**: Phase 1でプレースホルダー定義、Phase 3で実装
- **Implications**:
  - `src/ports/database.port.ts`でDatabaseProviderインターフェース定義
  - MVP Phase 1ではモックまたはメモリ内データ
  - Phase 3でDuckDB MCPコネクタ実装（コネクタ仕様確定後）
  - 要件6の実装を「Phase 3 - Pending」として明記

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| **Agent Framework + Reusable Modules** | Microsoft Agent Framework をベースに、共通合議エンジンとMCP統合モジュールを汎用化 | - コード量70%削減<br>- MCP/Multi-Agent機能が組み込み<br>- 他ドメインへの流用容易<br>- Microsoft公式サポート | - Agent Framework依存<br>- Python推奨（TypeScript選択肢減少） | **✅ 採用**: 要件の拡張性・再利用性・低コストを全て満たす |
| Hexagonal + Plugin (自前実装) | ヘキサゴナルアーキテクチャ + プラグイン方式（フルスクラッチ） | - 完全制御可能<br>- TypeScript使用可能 | - 実装コスト大（1,500行+）<br>- 保守負担<br>- MCP統合自前実装必要 | 教育目的なら有益だが、実用性で劣る |
| Simple Layered | 単純3層アーキテクチャ | - 実装速度速い | - 拡張性に制約<br>- 再利用困難 | プロトタイプ用のみ |
| Microservices | エージェント単位の分散サービス | - スケーラビリティ | - 運用複雑度極大<br>- 低コスト要件と矛盾 | 規模に不適合 |

**選定結果**: Agent Framework + Reusable Modules Architecture
- **コア**: Microsoft Agent Framework (GroupChatOrchestrator, MCP Plugin)
- **共通基盤**: `src/common/` に汎用合議エンジン・MCP統合モジュール
- **ドメイン固有**: `src/stock_magi/` に株式分析エージェント・プロンプト
- **再利用性**: 他ドメイン実装時は `src/<domain>/` 追加のみ

## Design Decisions

### Decision: `Architecture - Agent Framework + Reusable Modules`
- **Context**: マルチエージェント合議システムとMCP統合を、株式以外のドメインにも流用可能な形で実装
- **Alternatives Considered**:
  1. **Agent Framework + Reusable Modules**: Microsoft公式フレームワーク + 汎用共通基盤
  2. **Hexagonal + Plugin (自前)**: フルスクラッチでヘキサゴナルアーキテクチャ実装
  3. **Simple Layered**: 単純3層アーキテクチャ
- **Selected Approach**: Agent Framework + Reusable Modules
  - **Framework層**: Microsoft Agent Framework (GroupChat, MCP, Sequential)
  - **共通基盤**: `src/common/consensus/`, `src/common/mcp/` （ドメイン非依存）
  - **ドメイン層**: `src/stock_magi/agents/`, `src/stock_magi/prompts/` （株式固有）
- **Rationale**:
  - **コード削減**: 自前実装(1,500行) → Agent Framework使用(300-500行) = 70%削減
  - **再利用性**: 共通基盤を他ドメイン（不動産、医療など）にコピー不要で流用可能
  - **MCP統合**: ネイティブサポートで自前ラッパー不要
  - **教育価値**: Agent Framework のベストプラクティスを学べる
  - **保守性**: Microsoft公式フレームワークのアップデートに追従
- **Trade-offs**:
  - **Benefits**: 実装速度向上、保守負担軽減、他ドメイン展開容易
  - **Compromises**: Agent Framework依存、Python推奨（TypeScript選択肢減）
- **Follow-up**: Phase 1で共通基盤実装、Phase 2で株式ドメイン追加

### Decision: `Consensus Engine - GroupChatOrchestrator + Voting Strategies`
- **Context**: 3エージェント（Melchior, Balthasar, Casper）による合議機能の実装
- **Alternatives Considered**:
  1. **GroupChatOrchestrator**: Agent Framework組み込みの討論型合議
  2. **SequentialOrchestrator**: 順次実行型（合議なし）
  3. **自前Consensus Engine**: 戦略パターンでアルゴリズム実装
- **Selected Approach**: GroupChatOrchestrator + Reusable Voting Strategies
  - Agent Framework の GroupChatOrchestrator で3エージェントの討論を実行
  - `src/common/consensus/strategies/voting_strategy.py` で投票アルゴリズムを汎用化
    - MajorityVotingStrategy: 多数決（MVP Phase 1）
    - WeightedVotingStrategy: 重み付け投票（Phase 2）
    - ConfidenceAggregationStrategy: 信頼度ベース集約（Phase 2）
- **Rationale**:
  - GroupChatOrchestrator でエージェント間のメッセージ管理が自動化
  - 投票戦略を分離することで、ドメイン非依存な合議ロジックを実現
  - 段階的進化（MVP: 単純投票 → Phase 2: 重み付け）に対応
- **Trade-offs**:
  - **Benefits**: 実装簡略化、討論履歴の自動記録、他ドメイン流用容易
  - **Compromises**: GroupChatの実行時間（エージェント数×LLM呼び出し）
- **Follow-up**: MVP でMajorityVotingStrategy実装、Phase 2で重み付け追加
  - `IConsensusStrategy`インターフェース定義
  - `SimpleVotingStrategy`, `WeightedVotingStrategy`実装
  - `ConsensusEngine`が戦略を動的に選択
- **Rationale**:
  - MVP→Phase 2の段階的拡張に対応
  - 新しい合議アルゴリズム追加が容易（Open-Closed Principle）
  - エージェント数N個での動作保証
- **Trade-offs**:
  - **Benefits**: 拡張性、アルゴリズム交換容易性
  - **Compromises**: 戦略クラス数増加
- **Follow-up**: Phase 1でSimpleVoting実装、Phase 2でWeightedVoting追加

### Decision: `Data Storage - Phase-based Approach`
- **Context**: MVP Phase 1でのデータ永続化とPhase 3でのDuckDB統合準備
- **Alternatives Considered**:
  1. **Phase-based**: Phase 1 Azure Blob → Phase 2 Table Storage → Phase 3 DuckDB
  2. **PostgreSQL**: 即座にリレーショナルDB導入
  3. **Cosmos DB**: Azure NoSQL DB利用
- **Selected Approach**: Phase-based Storage Evolution
  - **Phase 1**: Azure Blob Storage（JSON形式）、軽量・低コスト
  - **Phase 2**: Azure Table Storage または Cosmos DB（NoSQL）
  - **Phase 3**: DuckDB MCP Connector（コネクタ仕様確定後）
- **Rationale**:
  - MVPで過剰な機能導入を回避、低コスト要件遵守
  - DuckDB統合がPhase 3 Pending（外部依存）
  - `IDatabaseProvider`インターフェースで将来拡張準備
- **Trade-offs**:
  - **Benefits**: 段階的コスト増、要件変更への柔軟性
  - **Compromises**: Phase間でのマイグレーション発生
- **Follow-up**: Phase 1でBlob実装、Phase 3でDuckDBコネクタ仕様待ち

### Decision: `LLM Provider Abstraction`
- **Context**: Azure OpenAI利用だが、将来的なローカルLLM対応を準備
- **Alternatives Considered**:
  1. **Abstraction Layer**: ILLMProvider経由で実装切り替え
  2. **Direct Integration**: Azure OpenAI直接利用
- **Selected Approach**: LLM Provider Interface with Azure OpenAI Primary
  - `ILLMProvider`ポート定義
  - `AzureOpenAIAdapter`実装（`@azure/openai`）
  - `LocalLLMAdapter`プレースホルダー（将来用）
- **Rationale**:
  - プロバイダー切り替え容易性
  - ローカルLLMへの将来移行準備（コスト最適化）
  - テストでモックLLM注入可能
- **Trade-offs**:
  - **Benefits**: 拡張性、テスト容易性
  - **Compromises**: 抽象化レイヤー追加
- **Follow-up**: Phase 1でAzure OpenAI実装、ローカルLLMは要件次第

### Decision: `TypeScript with Strict Type Safety`
- **Context**: Python互換性問題（ARM64）回避のためTypeScript採用、型安全性強化
- **Alternatives Considered**:
  1. **TypeScript with `strict: true`**: 厳格な型チェック
  2. **TypeScript with `any` allowed**: 緩い型チェック
  3. **Python**: 当初想定だがARM64互換性問題
- **Selected Approach**: TypeScript 5.3+ with Strict Mode
  - `tsconfig.json`で`strict: true`, `noImplicitAny: true`
  - `any`型使用禁止、`unknown`推奨
  - Zodでランタイムバリデーション
- **Rationale**:
  - ARM64互換性問題回避
  - 型安全性によるバグ削減
  - IDE補完・リファクタリング支援
- **Trade-offs**:
  - **Benefits**: 実行時エラー削減、保守性向上
  - **Compromises**: Python開発者の学習コスト
- **Follow-up**: `docs/TYPESCRIPT_GUIDE.md`でPython開発者向けガイド作成

## Risks & Mitigations

### Risk 1: DuckDB Connector Specification Delay
- **Risk**: Phase 3でのDuckDB統合がコネクタ仕様未確定により遅延
- **Mitigation**: 
  - Phase 1で`IDatabaseProvider`インターフェース定義
  - 要件6を「Phase 3 - Pending」として明示
  - モックデータで先行開発、コネクタ仕様確定後に実装

### Risk 2: Azure OpenAI API Rate Limits
- **Risk**: 無料/低コストプランでの API rate limit超過
- **Mitigation**:
  - リトライロジック実装（Exponential Backoff）
  - ローカルキャッシング（分析結果の一時保存）
  - ローカルLLM対応準備（ILLMProvider抽象化）

### Risk 3: Agent Scalability (N agents)
- **Risk**: エージェント数増加による合議処理時間増大
- **Mitigation**:
  - 並列処理（Promise.all()でエージェント並列実行）
  - タイムアウト設定（遅延エージェントのスキップ）
  - Phase 2でパフォーマンスベンチマーク実施

### Risk 4: TypeScript Learning Curve for Python Developers
- **Risk**: Python開発者のTypeScript習熟に時間がかかる
- **Mitigation**:
  - `docs/TYPESCRIPT_GUIDE.md`作成（Python対応表付き）
  - `CHANGELOG.md`で詳細な技術説明
  - コード内に教育的コメント記載
  - `docs/LEARNING_PATH.md`で段階的学習パス提供

### Risk 5: MCP Protocol Compatibility Issues
- **Risk**: 外部MCPサーバーとの互換性問題
- **Mitigation**:
  - MCP基底クラスでエラーハンドリング統一
  - 各MCPアダプターで接続テスト実装
  - フォールバックメカニズム（MCP失敗時のデフォルト動作）

## References

### Official Documentation
- [Azure Functions TypeScript](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-node?pivots=nodejs-model-v4) - v4 Programming Model
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/) - GPT-4 integration
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) - Type system and best practices
- [Vitest Documentation](https://vitest.dev/) - Testing framework

### Architecture Patterns
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Ports & Adapters pattern
- [Plugin Architecture](https://refactoring.guru/design-patterns/strategy) - Strategy pattern for consensus

### Azure Services
- [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/) - Phase 1 data persistence
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/) - Secret management

### Code Samples
- Microsoft Learn Code Samples - Azure Functions TypeScript実装例
- `@azure/functions` v4 - HTTP trigger handlers
