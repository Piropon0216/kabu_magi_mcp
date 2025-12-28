# Changelog

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

形式は[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、
このプロジェクトは[セマンティック バージョニング](https://semver.org/lang/ja/)に準拠しています。

---

## [Unreleased]

## [0.1.0] - 2025-12-28

### Added (追加)

#### Phase 1 MVP 完全実装

**Microsoft Agent Framework ベースのマルチエージェント株式分析システムの基盤実装完了**

##### 1. プロジェクト基盤・開発環境

- **DevContainer 環境** (`.devcontainer/devcontainer.json`)
  - ARM64 Copilot+ PC 対応の Python 3.11 開発環境
  - Poetry + Node.js (MCP サーバー用) 自動セットアップ
  - VS Code 拡張機能統合 (Python, Pylance, Docker, Ruff)

- **依存関係管理** (`pyproject.toml`)
  - Microsoft Agent Framework v1.0.0b251223 (プレリリース版バージョン固定)
  - FastAPI + uvicorn (非同期 API サーバー)
  - Pydantic v2 (データバリデーション)
  - pytest + pytest-asyncio (テストフレームワーク)
  - Ruff (高速 Linter + Formatter)

- **コンテナ化** (`Dockerfile`, `docker-compose.yml`)
  - マルチステージビルド (依存関係分離)
  - 非 root ユーザー実行
  - ヘルスチェック統合
  - 開発環境用 Docker Compose 設定

- **環境変数テンプレート** (`.env.example`)
  - Microsoft Foundry 接続設定
  - Phase 1 では Morningstar を Foundry Tool Catalog から利用

##### 2. 共通基盤モジュール (`src/common/`) - 汎用再利用可能コンポーネント

**設計哲学**: ドメイン非依存な基盤を構築し、株式以外のドメイン (不動産、医療など) にも流用可能

- **合議エンジン** (`src/common/consensus/`)
  - `ReusableConsensusOrchestrator`: GroupChat 型マルチエージェント合議
  - `VotingStrategy`: 投票戦略抽象化 (Phase 1: 多数決、Phase 2: 加重投票)
  - Agent Framework の GroupChatOrchestrator をラップ

- **MCP 統合** (`src/common/mcp/`)
  - `FoundryToolRegistry`: Foundry Tool Catalog 統一管理
  - Phase 1: Morningstar (GUI ベース設定)
  - Phase 2: Yahoo Finance (npm MCP Server)
  - Phase 3: DuckDB 対応予定

- **共通データモデル** (`src/common/models/`)
  - `Action`: BUY/SELL/HOLD 判定 (Enum)
  - `AgentVote`: エージェント個別投票 (Pydantic モデル)
  - `FinalDecision`: 合議結果 (信頼度、対立検出含む)
  - Pydantic によるバリデーション (confidence 0.0-1.0、reasoning 最低文字数)

##### 3. 株式ドメイン実装 (`src/stock_magi/`)

- **Melchior エージェント** (`src/stock_magi/agents/melchior_agent.py`)
  - ファンダメンタルズ分析専門エージェント
  - Phase 1: モック実装 (HOLD + confidence 0.5)
  - Phase 2: Agent Framework 完全統合予定

- **プロンプト定義** (`src/stock_magi/prompts/stock_analysis_prompts.py`)
  - `MELCHIOR_SYSTEM_MESSAGE`: エージェントペルソナ定義
  - `create_melchior_analysis_prompt()`: 分析プロンプト生成
  - Phase 2: Balthasar (テクニカル), Casper (センチメント) 追加予定

- **FastAPI エンドポイント** (`src/stock_magi/api/endpoints.py`)
  - `POST /api/analyze`: 銘柄分析エンドポイント
  - `GET /api/health`: ヘルスチェック
  - Pydantic モデルによるリクエスト/レスポンス検証
  - 自動 OpenAPI (Swagger) ドキュメント生成

- **アプリケーションエントリーポイント** (`src/main.py`)
  - FastAPI アプリケーション初期化
  - CORS ミドルウェア設定
  - Lifespan イベント (起動/終了処理)
  - ルートエンドポイント (API 情報提供)

##### 4. 包括的テストスイート (`tests/`)

**TDD アプローチによる高品質保証**

- **共通基盤テスト**
  - `test_decision_models.py`: Pydantic モデルバリデーション (8 テスト)
  - `test_foundry_tool_registry.py`: MCP ツール管理 (8 テスト)
  - `test_consensus_orchestrator.py`: 合議ロジック (7 テスト)

- **ドメイン固有テスト**
  - `test_melchior_agent.py`: Melchior エージェント統合テスト (5 テスト)

- **E2E テスト**
  - `test_api_endpoints.py`: FastAPI エンドポイント (9 テスト)
  - 正常系・異常系・バリデーションエラーを網羅

**テストカバレッジ**: pytest + pytest-asyncio + unittest.mock で実装

##### 5. ドキュメント

- **開発コンテキスト** (`docs/CONTEXT.md`)
  - アーキテクチャ決定事項
  - Agent Framework プレリリース版の注意事項
  - データソース戦略 (Phase 1-3)
  - DevContainer 開始手順

- **MVP セットアップガイド** (`docs/MVP_SETUP.md`)
  - Foundry Portal セットアップ (20 分)
  - Morningstar Tool Catalog 設定 (2 分)
  - DevContainer/Docker Compose/ローカル Python の 3 パターン
  - トラブルシューティング

- **技術仕様書** (`.kiro/specs/stock-magi-system-ja/`)
  - `requirements.md`: 機能要件・非機能要件 (10 カテゴリ)
  - `design.md`: アーキテクチャ設計 (20,000 行)
  - `research.md`: 技術調査結果とトレードオフ分析 (24,000 行)
  - `tasks.md`: 実装タスクリスト (Phase 1-3, 10,000 行)

##### 6. MCP サーバー設定

- **MCP 設定ファイル** (`config/mcp_servers.json`)
  - Phase 1: Morningstar (Foundry Tool Catalog - GUI 設定のみ)
  - Phase 2: Yahoo Finance (npm MCP Server - 定義済み)
  - 将来拡張用の構造化設定

### Changed (変更)

- **言語選択の変更**: TypeScript → Python 3.11+
  - 理由: Agent Framework の Python 実装が最新機能豊富
  - ARM64 互換性: DevContainer で解決

### Technical Highlights (技術的ハイライト)

#### コード削減効果
- **従来のアプローチ** (フルスクラッチ Hexagonal Architecture): ~1,500 行
- **Agent Framework 活用**: ~500 行 (共通基盤 200 行 + ドメイン 150 行 + API 100 行 + テスト 150 行)
- **削減率**: **約 70%**

#### 再利用性設計
- `src/common/` は完全にドメイン非依存
- 他ドメインへの流用例:
  - 不動産分析: `src/real_estate/agents/` 追加のみ
  - 医療診断: `src/medical/agents/` 追加のみ

#### Agent Framework プレリリース版リスク軽減策
- バージョン固定: `agent-framework-azure-ai = "1.0.0b251223"`
- Microsoft Foundry Portal (https://ai.azure.com/) で GUI ベース管理
- DevUI によるエージェント動作ビジュアルデバッグ

#### データソース戦略
- **Phase 1 (MVP)**: Morningstar (Foundry Tool Catalog - PER/PBR/ROE など財務指標)
- **Phase 2**: Yahoo Finance (npm MCP Server - 株価チャート、リアルタイムデータ)
- **Phase 3**: DuckDB + Jquants API (時系列データ管理)

### Development Workflow (開発ワークフロー)

#### セットアップ時間
- **手動作業**: 25-30 分 (Foundry Portal セットアップ 20 分 + 環境変数 5 分)
- **自動作業**: 5-10 分 (DevContainer ビルド)

#### テスト実行
```bash
poetry run pytest tests/ -v --cov=src --cov-report=html
```

#### ローカル起動
```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Docker 起動
```bash
docker compose up --build
```

### Next Steps (次のステップ)

#### Phase 2: Multi-Agent System (Week 3)
- Balthasar エージェント (バランス型分析)
- Casper エージェント (テクニカル分析)
- 加重投票ロジック
- Yahoo Finance MCP Server 統合

#### Phase 3: Azure Deployment (Week 4)
- Azure Container Apps デプロイ (Bicep)
- DuckDB 統合 (Jquants API)
- GitHub Actions CI/CD

### Educational Value (教育的価値)

このプロジェクトで学べること:
1. **Microsoft Agent Framework**: マルチエージェント合議の実装パターン
2. **MCP Protocol**: MCP サーバーの統合方法
3. **Microsoft Foundry**: LLM モデルの管理とデプロイ
4. **Reusable Architecture**: ドメイン非依存な基盤設計
5. **Python + FastAPI**: 非同期 API 開発

### Breaking Changes (破壊的変更)

なし (初回リリース)

### Deprecated (非推奨)

なし (初回リリース)

### Removed (削除)

なし (初回リリース)

### Fixed (修正)

なし (初回リリース)

### Security (セキュリティ)

- 環境変数による機密情報管理 (`.env.example` 提供)
- Docker 非 root ユーザー実行
- Phase 2 で Azure Key Vault 統合予定

---

## [Unreleased] (旧エントリ保持)

### Added (追加)

#### プロジェクト初期化 - 2025-12-28

**概要**: Stock MAGI Systemプロジェクトの基本構造を確立

**追加されたファイル**:
- `.kiro/steering/product.md`: プロダクトビジョン、MVP戦略、開発方針
- `.kiro/steering/tech.md`: 技術スタック、アーキテクチャパターン、TypeScript規約
- `.kiro/steering/structure.md`: ディレクトリ構成、命名規則、Git管理方針
- `README.md`: プロジェクト概要とセットアップ手順
- `CHANGELOG.md`: 変更履歴（このファイル）

**技術的決定**:

1. **言語選択: TypeScript**
   - 理由: Copilot+ PC (ARM64)でのPythonライブラリ互換性問題を回避
   - Pythonとの違い: 静的型付け、コンパイル必要、`any`型使用禁止
   - Python開発者への配慮: 詳細なコメント、TypeScriptガイド作成予定

2. **クラウドプラットフォーム: Azure**
   - 理由: Microsoft Foundry統合、Azure OpenAI利用
   - 主要サービス:
     - Azure Functions: サーバーレス実行（Pythonの`azure.functions`に相当）
     - Azure OpenAI: LLM推論（Pythonの`openai`パッケージに相当）
     - Azure Storage: データ永続化（Pythonの`azure-storage-blob`に相当）

3. **アーキテクチャパターン: ヘキサゴナル（Ports & Adapters）**
   - コアドメイン: ビジネスロジック（エージェント、合議）
   - ポート: インターフェース定義（Pythonの`Protocol`や抽象基底クラスに相当）
   - アダプター: 外部システム統合（Pythonのアダプターパターンと同様）
   - メリット: テスト容易性、拡張性、依存関係の明確化

4. **プラグインアーキテクチャ**
   - エージェントレジストリ: 動的登録（Pythonの`importlib`に似た概念）
   - MCPコネクタ: プラグイン方式（Pythonのパッケージエントリーポイントに相当）

5. **テスト戦略: TDD + 80%カバレッジ**
   - フレームワーク: Vitest（Pythonの`pytest`に相当）
   - カバレッジ: c8（Pythonの`coverage.py`に相当）
   - モック: MSW（Pythonの`unittest.mock`や`responses`に相当）

**Git管理**:
- 新しいリポジトリを初期化
- ブランチ戦略: Git Flow（main, develop, feature/*, hotfix/*）
- コミット規約: Conventional Commits

**次のステップ**:
1. 基本的なTypeScriptプロジェクトセットアップ（`package.json`, `tsconfig.json`）
2. ディレクトリ構造作成（`src/core/`, `src/adapters/`, etc.）
3. 型定義ファイル作成（`src/core/models/`）
4. エージェント基底インターフェース実装
5. 最初のユニットテスト作成

**Python開発者向け補足**:
- TypeScriptは型定義が必須です。すべての変数、関数の引数、戻り値に型を指定します
- `any`型は使用禁止（Pythonの動的型付けに相当しますが、型安全性を損なうため）
- インターフェース（`interface`）はPythonの`Protocol`や抽象基底クラスに似ています
- ヘキサゴナルアーキテクチャは、Pythonでもよく使われるクリーンアーキテクチャの一種です

**影響範囲**:
- 新規プロジェクトのため、既存コードへの影響なし
- 今後のすべての開発は、このSteering定義に従う

**参考リンク**:
- [TypeScript公式ドキュメント](https://www.typescriptlang.org/docs/)
- [ヘキサゴナルアーキテクチャ](https://alistair.cockburn.us/hexagonal-architecture/)
- [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/)

---

## 変更履歴の記録方法

### カテゴリ
- **Added (追加)**: 新機能
- **Changed (変更)**: 既存機能の変更
- **Deprecated (非推奨)**: 将来削除予定の機能
- **Removed (削除)**: 削除された機能
- **Fixed (修正)**: バグ修正
- **Security (セキュリティ)**: 脆弱性対応

### エントリ形式

各変更には以下を含める:
1. **概要**: 何を変更したか（1-2行）
2. **詳細**: なぜ変更したか、どのように実装したか
3. **技術的決定**: TypeScript特有の実装方法
4. **Python開発者向け補足**: Pythonとの対応関係
5. **影響範囲**: どのコンポーネントが影響を受けるか
6. **次のステップ**: 次に何をすべきか（該当する場合）

### 例

```markdown
#### エージェントレジストリ実装 - 2025-12-28

**概要**: 動的なエージェント登録・管理機能を実装

**詳細**:
- `AgentRegistry`クラスを作成
- `register()`, `unregister()`, `getAll()`メソッド実装
- ジェネリック型を使用して型安全性を確保

**技術的決定**:
- TypeScriptのMap型を使用（Pythonの`dict`に相当）
- ジェネリック`<T extends Agent>`で型制約（Pythonの`TypeVar`に相当）

**Python開発者向け補足**:
```python
# Python equivalent
class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
    
    def register(self, name: str, agent: Agent) -> None:
        self._agents[name] = agent
```

TypeScriptでは以下のように実装:
```typescript
class AgentRegistry {
  private agents: Map<string, Agent> = new Map();
  
  register(name: string, agent: Agent): void {
    this.agents.set(name, agent);
  }
}
```

**影響範囲**:
- `src/core/agents/registry.ts`: 新規作成
- `tests/unit/agents/registry.test.ts`: ユニットテスト追加

**次のステップ**:
1. エージェント基底インターフェース定義
2. 短期トレーダーエージェント実装
```
