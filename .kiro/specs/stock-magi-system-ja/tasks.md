# Implementation Plan

## Overview
本タスクリストは、**Agent Framework ベースの Stock Magi System** の実装を段階的に進めるための作業計画です。
フレームワークを最大限活用することで、**カスタム実装を最小化**し、教育的価値を重視します。

**実装戦略**: Framework-First Approach（Agent Framework の組み込み機能を優先し、必要最小限のグルーコードのみ実装）

**推定コード量**: 300-500行（Agent Framework 活用により、フルスクラッチ実装の約30%）

---

## Phase 1: MVP - Common Framework + 1 Agent (Week 1-2)

### 1. Project Initialization and Environment Setup
- [ ] 1.1 Create Python project with Poetry
  - Initialize `pyproject.toml` with Python 3.11+
  - Install core dependencies: `agent-framework-azure-ai --pre`, `fastapi`, `uvicorn`
  - Configure `ruff.toml` for linting and formatting
  - Create `.env.example` for environment variables
  - _目的: Agent Framework の最新機能を使用できる環境を構築_

- [ ] 1.2 Set up Microsoft Foundry connection
  - Create Foundry project in Azure Portal
  - Deploy GPT-4o model
  - Configure `.env` with `FOUNDRY_ENDPOINT`, `FOUNDRY_API_KEY`, `FOUNDRY_DEPLOYMENT`
  - Test connection with simple `azure-ai-agent` call
  - _学習ポイント: Foundry のモデル管理とデプロイメント_

- [ ] 1.3 Configure Morningstar MCP server from Foundry Tool Catalog
  - Configure Morningstar MCP Server in Microsoft Foundry Portal (https://ai.azure.com/)
  - Add tool to project via Tool Catalog → "Morningstar MCP Server"
  - Test connection with simple Agent Framework call
  - _要件: R2.1, R2.2_
  - _学習ポイント: Foundry Tool Catalog の使い方、MCP Server の GUI ベース統合_

### 2. Common Reusable Framework Implementation
- [ ] 2.1 Implement FoundryToolRegistry (Common Module)
  - Create `src/common/mcp/foundry_tool_registry.py`
  - Connect to Foundry Tool Catalog via Azure SDK
  - Wrap Morningstar MCP tool for Agent Framework
  - Add `get_tool()` and `get_tools_for_agent()` methods
  - _目的: Foundry Tool Catalog を他ドメインでも活用可能な汎用基盤_
  - _学習ポイント: Foundry Tool の Python SDK 統合_
  - _要件: R2.3, R2.6_

- [ ] 2.2 Implement ReusableConsensusOrchestrator (Common Module)
  - Create `src/common/consensus/orchestrators/group_chat_consensus.py`
  - Wrap Agent Framework の `GroupChatOrchestrator`
  - Implement `reach_consensus(input_context)` method
  - Add voting strategy abstraction
  - _目的: ドメイン非依存な合議エンジン_
  - _要件: R3.1, R4.1, R4.2_

- [ ] 2.3 Define common data models with Pydantic
  - Create `src/common/models/decision_models.py`
  - Define `Action`, `AgentVote`, `FinalDecision` with validation
  - _学習ポイント: Pydantic による型安全な API 設計_
  - _要件: R3.3, R3.4_

### 3. Stock Domain - MVP Agent (Melchior Only)
- [ ] 3.1 Implement Melchior agent factory
  - Create `src/stock_magi/agents/melchior_agent.py`
  - Implement `create_melchior_agent(foundry_tool)` function
  - Configure Agent Framework の `Agent` with system message
  - Add Morningstar tool (from Foundry Tool Catalog)
  - _学習ポイント: Agent Framework のエージェント定義パターン、Foundry Tool 統合_
  - _要件: R3.2, R3.3_

- [ ] 3.2 Create stock analysis prompts
  - Create `src/stock_magi/prompts/stock_analysis_prompts.py`
  - Define Melchior's persona and analysis guidelines
  - _要件: R3.5_

### 4. FastAPI Endpoint Implementation
- [ ] 4.1 Implement /api/analyze endpoint
  - Create `src/stock_magi/api/endpoints.py`
  - Add POST endpoint accepting `{"ticker": "7203.T"}`
  - Call `ReusableConsensusOrchestrator.reach_consensus()`
  - Return `FinalDecision` JSON
  - _学習ポイント: FastAPI の async/await パターン_
  - _要件: R5.1, R5.2, R5.3_

- [ ] 4.2 Add error handling and validation
  - Validate ticker format with regex
  - Handle MCP connection errors, Foundry API errors
  - Return appropriate HTTP status codes
  - _要件: R1.3_

- [ ] 4.3 Create main.py entry point
  - Create `src/main.py` with FastAPI app initialization
  - Configure CORS, logging
  - _要件: R7.2_

### 5. MVP Testing
- [ ] 5.1 Write unit tests for common framework
  - Test `MCPPluginRegistry.get_plugin()` with mock config
  - Test `ReusableConsensusOrchestrator` with mock agents
  - _ツール: pytest + unittest.mock_
  - _要件: R10.2_

- [ ] 5.2 Write integration test for Melchior agent
  - Test `create_melchior_agent()` with real Foundry connection
  - Mock MCP responses
  - _要件: R10.6_

- [ ] 5.3 Write E2E test for FastAPI endpoint
  - Use `TestClient` to test `/api/analyze`
  - Verify JSON response format
  - _要件: R10.4, R10.5_

### 6. Local Deployment and Documentation
- [ ] 6.1 Create Dockerfile
  - Multi-stage build for Python dependencies
  - Expose port 8000
  - _要件: R7.1_

- [ ] 6.2 Write MVP setup guide
  - Create `docs/MVP_SETUP.md`
  - Step-by-step: Poetry install → Foundry setup → MCP config → Run locally
  - _要件: R9.3_

---

## Phase 2: Multi-Agent System (Week 3)

### 7. Additional Stock Domain Agents
- [ ] 7.1 Implement Balthasar agent (Balanced Analysis)
  - Create `src/stock_magi/agents/balthasar_agent.py`
  - Add Morningstar (Foundry Tool) + Azure Docs tools
  - _要件: R3.5_

- [ ] 7.2 Implement Casper agent (Technical Analysis)
  - Create `src/stock_magi/agents/casper_agent.py`
  - Add Morningstar tool (technical data focus)
  - _要件: R3.5_

- [ ] 7.3 Update orchestrator to use 3 agents
  - Modify `endpoints.py` to initialize all 3 agents
  - Test multi-agent discussion with GroupChat
  - _学習ポイント: Agent Framework の GroupChat 動作_

### 8. Weighted Voting Strategy
- [ ] 8.1 Implement VotingStrategy abstraction
  - Create `src/common/consensus/strategies/voting_strategy.py`
  - Define `MajorityVotingStrategy` and `WeightedVotingStrategy`
  - _要件: R4.4_

- [ ] 8.2 Add weighted voting to orchestrator
  - Accept agent weights in `reach_consensus()`
  - Calculate weighted confidence
  - _要件: R4.5_

- [ ] 8.3 Add conflict detection
  - Detect split votes (e.g., 1 BUY, 1 SELL, 1 HOLD)
  - Generate risk warnings in `FinalDecision.summary`
  - _要件: R4.6_

### 9. Enhanced Testing
- [ ] 9.1 Write unit tests for new agents
  - Test Balthasar and Casper with mock Foundry
  - _要件: R10.2_

- [ ] 9.2 Write integration test for 3-agent consensus
  - Verify discussion history format
  - Test voting strategy logic
  - _要件: R10.6_

### 10. Yahoo Finance MCP Server Integration (Phase 2 - Pending)
- [ ] 10.1 Install Yahoo Finance MCP server via npm
  - Install `@modelcontextprotocol/server-yahoo-finance` globally
  - Create `config/mcp_servers.json` for npm-based MCP servers
  - Test MCP server with `npx` command
  - _目的: Morningstar にない株価チャート、リアルタイムデータを補完_

- [ ] 10.2 Implement npm MCP Server adapter
  - Create `src/common/mcp/npm_mcp_adapter.py`
  - Wrap npm MCP server process management
  - Add to FoundryToolRegistry as custom tool
  - _要件: R2.3_

- [ ] 10.3 Integrate Yahoo Finance into agents
  - Update `create_balthasar_agent()` to use Morningstar + Yahoo Finance
  - Add chart analysis capabilities to Casper agent
  - _要件: R3.5_

---

## Phase 3: Azure Deployment + DuckDB (Week 4 - Pending)

### 11. Azure Container Apps Deployment
- [ ] 11.1 Create Bicep infrastructure definition
  - Create `infra/main.bicep`
  - Define Container App, Container Environment, Application Insights
  - Configure min replicas = 0 for cost optimization
  - _要件: R7.1, R7.4_

- [ ] 11.2 Configure Key Vault for secrets
  - Store `FOUNDRY_API_KEY` in Key Vault
  - Reference from Container App environment variables
  - _要件: R8.2_

- [ ] 11.3 Set up GitHub Actions CI/CD
  - Create `.github/workflows/deploy.yml`
  - Build Docker image → Run tests → Deploy to Container Apps
  - _要件: R7.1_

### 12. DuckDB Integration (Optional - Pending MCP Server)
- [ ] 12.1 Add DuckDB MCP server to registry
  - Configure `config/mcp_servers.json` with DuckDB server
  - Test connection with local DuckDB file
  - _要件: R6.2, R6.3_

- [ ] 12.2 Store analysis results in DuckDB
  - Create `store_decision()` function
  - Save `FinalDecision` to DuckDB table
  - _要件: R6.5_

---

## Educational Documentation Tasks (Continuous)

### 13. Agent Framework Learning Resources
- [ ] 13.1 Create Agent Framework guide
  - Write `docs/AGENT_FRAMEWORK_GUIDE.md`
  - Cover: Agent definition, GroupChat, Plugins, Orchestrators
  - Include code examples with annotations
  - _目的: Agent Framework の学習教材_

- [ ] 13.2 Create MCP integration guide
  - Write `docs/MCP_INTEGRATION.md`
  - Explain MCPServerPlugin usage, MCP protocol basics
  - _目的: MCP の理解を深める_

- [ ] 13.3 Create Microsoft Foundry guide
  - Write `docs/FOUNDRY_GUIDE.md`
  - Cover: Model deployment, prompt experimentation, cost tracking, **Foundry Portal GUI usage**, **DevUI による agent debugging**
  - _目的: Foundry の活用方法を学ぶ（プレリリース版リスク軽減策を含む）_

- [ ] 13.4 Create reusability guide
  - Write `docs/REUSABILITY_GUIDE.md`
  - Explain `src/common/` architecture
  - Provide example: How to create real estate analysis system
  - _目的: 汎用基盤の流用方法を示す_

- [ ] 13.5 Create Python learning path (optional)
  - Write `docs/PYTHON_GUIDE.md` (if needed)
  - Cover: async/await, type hints, Pydantic
  - _目的: Python 初学者向け_

---

## Notes
- **MVP Deliverable**: Phase 1 完了時点で、1エージェント + FastAPI エンドポイント + ローカルテストが動作
- **Data Source Strategy**:
  - **Phase 1 (MVP)**: Morningstar MCP Server (Foundry Tool Catalog - PER/PBR/ROE など詳細財務指標)
  - **Phase 2**: Yahoo Finance MCP Server (npm 経由 - 株価チャート、リアルタイムデータ)
  - **Phase 3**: DuckDB + Jquants API (時系列データ管理)
  - **実装の簡素化**: Foundry Tool Catalog 統合により Phase 1 のコード量をさらに削減
- **Code Reduction**: Agent Framework により、カスタム実装を約70%削減（1,500行 → 300-500行）
- **Reusability**: `src/common/` の全コンポーネントは他ドメインに流用可能
- **Cost Estimate**: Azure Container Apps (min=0) + Foundry (GPT-4o) で月額 **$3-10**
- **Prerequisites**: Python 3.11+, Poetry, npm (MCP サーバー用)
- **Risk Mitigation**: Agent Framework プレリリース版は `pyproject.toml` でバージョン固定。Microsoft Foundry Portal + DevUI で GUI 管理を併用してリスク軽減
