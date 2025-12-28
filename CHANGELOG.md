# Changelog

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

形式は[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、
このプロジェクトは[セマンティック バージョニング](https://semver.org/lang/ja/)に準拠しています。

## Python開発者向け注意
各エントリには詳細な説明と、TypeScript特有の実装について補足説明を含めています。

---

## [Unreleased]

### Added (追加)

#### Agent Framework 準備作業 - 2025-12-28

**概要**: Azure AI Agent Framework 統合のための依存関係追加とプロジェクト整理

**追加された依存関係**:
- `azure-ai-projects ^2.0.0b2`: Azure AI Foundry Agent Framework SDK
  - 理由: 公式 Agent Framework クライアントライブラリ
  - `agent-framework-azure-ai` が要求する最小バージョン
- `azure-identity ^1.19.0`: Azure 認証ライブラリ
  - 理由: `AIProjectClient` の認証に必要
  - `DefaultAzureCredential` を使用したトークン取得

**環境変数**:
- `PROJECT_ENDPOINT`: Azure AI Foundry プロジェクトエンドポイント
  - 値: `https://con-agent-poc-resource.openai.azure.com/`
  - 用途: Agent Framework の初期化に使用

**試行錯誤と対策**:

1. **バージョン競合の解決**:
   - 問題: 初回実装で `azure-ai-projects ^1.0.0b1` を指定したが、`agent-framework-azure-ai` が `>=2.0.0b2` を要求
   - 対策: `pyproject.toml` を修正して `^2.0.0b2` に更新
   - 学習: プレリリースパッケージは依存関係を厳密に確認する必要がある

2. **ファイル破損の問題**:
   - 問題: `src/stock_magi/agents/melchior_agent.py` で `create_melchior_agent()` 関数が重複定義
   - 原因: Phase 1 の実装（`foundry_tool` パラメータ）と Phase 1.5 の実装（`project_endpoint` パラメータ）が混在
   - 具体的な破損内容:
     ```python
     def create_melchior_agent(foundry_tool: Any) -> MelchiorAgent:
         """docstring 途中で切れる"""
     def create_melchior_agent(foundry_tool: Any = None, project_endpoint: Optional[str] = None) -> MelchiorAgent:
         """完全な docstring"""
         return MelchiorAgent(project_endpoint=project_endpoint)
     ```
   - 対策: `git checkout HEAD` で Phase 1 の正常な状態に復元
   - 学習: 大規模なリファクタリングは段階的に実施し、各ステップでテストを実行すべき

3. **API 互換性の維持失敗**:
   - 問題: `MelchiorAgent.__init__()` のシグネチャ変更（`foundry_tool` → `project_endpoint`）により、既存の API (`endpoints.py`) が動作しなくなった
   - 対策: Phase 1 実装を維持し、Phase 1.5 実装は別ブランチで慎重に進めることに方針変更
   - 学習: 既存の API 互換性を保ちながらリファクタリングする必要がある（Factory パターンの更新など）

**プロジェクト整理**:
- `cc-sdd/` フォルダを Git 管理から除外
  - 理由: Spec-Driven Development ツールであり、このプロジェクト本体には不要
  - 操作: `git rm --cached -r cc-sdd` でインデックスから削除、`.gitignore` に追加
  - フォルダ自体はユーザーが手動で別の場所に移動

**`.gitignore` 改善**:
- Python 固有の除外パターンを追加:
  - `__pycache__/`, `*.py[cod]`, `*$py.class`, `.coverage`, `poetry.lock`
  - 理由: テスト実行やキャッシュファイルがリポジトリに混入するのを防ぐ

**テスト結果**:
- Phase 1 MVP: 全 37 テスト合格 ✅
- カバレッジ: 95%（主要機能は Phase 1 完成）
- Phase 1.5 実装は一時中断、システムは安定状態

**残件**:
- Task 7.1: Agent Framework への移行（Phase 1.5）
  - 現在: Phase 1 のモック実装で動作中
  - 次回: 別ブランチで慎重に実装し、既存 API との互換性を確保する
  - アプローチ案:
    - Factory 関数でパラメータを柔軟に処理（`foundry_tool` と `project_endpoint` の両方をサポート）
    - `MelchiorAgent.__init__()` を両方のパラメータを受け取れるように設計
    - 段階的移行（まず内部実装を変更、次に外部 API を更新）

**TypeScript 開発者への注意**:
- Python の `Optional[str]` は TypeScript の `string | null | undefined` に相当
- Poetry は npm/yarn に相当するパッケージマネージャー
- `pyproject.toml` は `package.json` に相当（依存関係管理）
- `azure-ai-projects` は Azure SDK for JavaScript の Python 版

---

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
