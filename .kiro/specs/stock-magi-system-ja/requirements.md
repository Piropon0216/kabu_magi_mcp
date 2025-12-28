# Requirements Document

## Project Description (Input)
MicrosoftFoundryを活用して、効率よく、以下要件の仕組みを作りたいです。
・モーニングスターなどの株情報を拾ってきたい
・複数のエージェント（短期トレーダ人格、中期トレーダ人格、イベントトレーダ人格）による、アンサンブルでの合議性の意思決定の仕組みを作りたい。とある条件や情報を渡すことで、それぞれのエージェントの結論、合議結果の結論が見えるようなアプリにしたい。
・MCPも活用可能にしたい。可能であれば、クラウドのナレッジ(Azure/AWSのナレッジ)についても、MCPから質問して取得できるようにしたい（この部分を入れ替えることで、他の経済情報も取得できるように汎用的な構成にできるアプリにしたい）
・できるだけ低コストに運用したい
・可能ならＤＢのデータ（個人でストックしたＤＢの株情報など）も、合議のインプットにできるようにしたい。

## Introduction
本要件定義書は、MicrosoftFoundryを活用した株式取引支援システム「Stock MAGI System」の要件を定義する。本システムは、複数のAIトレーダーエージェント（短期・中期・イベント）がMCP（Model Context Protocol）を通じて株式情報を収集し、アンサンブル合議により投資判断を提供する低コストな意思決定支援アプリケーションである。

### 開発アプローチ
- **MVP戦略**: 小さく始めて段階的に機能を追加し、価値を積み上げる
### Requirement 1: 株式情報データ収集（MVP Phase 1）
**Objective:** As a システム利用者, I want 外部ソースから株式情報を自動収集する機能, so that 最新の市場データに基づいた投資判断が可能になる

#### Acceptance Criteria (MVP)
1. When システム起動時, the Stock MAGI System shall 設定されたAPIから株価データを取得する
2. When データ取得リクエストを受信, the Stock MAGI System shall 指定された銘柄の最新株価、出来高を取得する
3. If データ取得に失敗した場合, then the Stock MAGI System shall エラーログを記録し、リトライ処理を実行する
4. The Stock MAGI System shall 取得したデータを標準化されたフォーマットで保存する

#### Acceptance Criteria (Phase 2+)
5. The Stock MAGI System shall モーニングスターAPIから詳細な財務指標を取得する
6. The Stock MAGI System shall Jquants APIから日本株の企業情報データを取得する
7. The Stock MAGI System shall データ取得頻度を設定可能にする（リアルタイム、日次、週次など）
**Objective:** As a システム利用者, I want 複数の外部ソースから株式情報を自動収集する機能, so that 最新の市場データに基づいた投資判断が可能になる

#### Acceptance Criteria
1. When システム起動時, the Stock MAGI System shall モーニングスターAPIから株価データを取得する
2. The Stock MAGI System shall Jquants APIから日本株の株価、財務、企業情報データを取得する
3. When データ取得リクエストを受信, the Stock MAGI System shall 指定された銘柄の最新株価、出来高、財務指標を取得する
4. If データ取得に失敗した場合, then the Stock MAGI System shall エラーログを記録し、リトライ処理を実行する
5. The Stock MAGI System shall 取得したデータを標準化されたフォーマットで保存する
6. The Stock MAGI System shall データ取得頻度を設定可能にする（リアルタイム、日次、週次など）
### Requirement 2: MCPによる拡張可能なデータソース統合（MVP Phase 1）
**Objective:** As a システム管理者, I want MCPプロトコルを活用した汎用的なデータソース接続機能, so that 株式情報以外の経済情報も柔軟に取得できる

#### Acceptance Criteria (MVP)
1. The Stock MAGI System shall MCPプロトコルを使用してデータソースに接続する基本機能を実装する
2. The Stock MAGI System shall 最低1つのMCPサーバー（株式データまたはクラウドナレッジ）に接続できる
3. The Stock MAGI System shall MCPサーバーの設定（エンドポイント、認証情報）を外部設定ファイルで管理する

#### Acceptance Criteria (Phase 2)
4. When 新しいデータソースを追加, the Stock MAGI System shall プラグイン方式で外部データソースを統合できる
5. Where Azure/AWSナレッジベースが利用可能, the Stock MAGI System shall MCPを通じてクラウドドキュメントを検索・取得できる
6. The Stock MAGI System shall DuckDB用MCPサーバーとクラウドナレッジ用MCPサーバーを同時に利用できる

#### Acceptance Criteria (Phase 3 - Pending)
### Requirement 3: 拡張可能なトレーダーエージェント実装（MVP Phase 1-2）
**Objective:** As a システム利用者, I want 異なる投資戦略を持つ複数のAIエージェントを動的に追加できる, so that 多角的な視点から投資判断を得られる

#### Acceptance Criteria (MVP)
1. The Stock MAGI System shall エージェントをプラグイン方式で登録・管理できるエージェントレジストリを実装する
2. The Stock MAGI System shall 最低1つのトレーダーエージェント（例: 短期トレーダー）を実装する
3. When 市場データを受信, the Stock MAGI System shall 登録されたエージェントが独立して分析を実行する
4. The Stock MAGI System shall 各エージェントの判断根拠を構造化データとして出力する

#### Acceptance Criteria (Phase 2)
5. The Stock MAGI System shall 短期トレーダーエージェント、中期トレーダーエージェント、イベントトレーダーエージェントの3つのエージェントを実装する
### Requirement 4: アンサンブル合議による意思決定（MVP Phase 1-2）
**Objective:** As a システム利用者, I want 複数エージェントの合議による最終判断, so that 単一の視点に偏らないバランスの取れた投資判断が得られる

#### Acceptance Criteria (MVP)
1. When 各エージェントが分析を完了, the Stock MAGI System shall エージェント間の合議プロセスを実行する
2. The Stock MAGI System shall 各エージェントの判断（買い/売り/ホールド）と信頼度スコアを収集する
3. The Stock MAGI System shall シンプルな多数決方式または平均投票方式で最終的な投資判断を決定する

#### Acceptance Criteria (Phase 2)
4. The Stock MAGI System shall 重み付け投票方式で最終的な投資判断を決定する
5. The Stock MAGI System shall エージェント間の意見の一致度を可視化する
6. When エージェント間で意見が大きく分かれる場合, the Stock MAGI System shall 警告を表示し、リスク評価を提示する
7. The Stock MAGI System shall 合議プロセスの履歴を記録する

#### Acceptance Criteria (Extensibility - All Phases)
8. The Stock MAGI System shall エージェント数がN個の場合でも合議アルゴリズムが動作する
### Requirement 5: インタラクティブな分析インターフェース（MVP Phase 1-2）
**Objective:** As a システム利用者, I want 条件や情報を入力すると各エージェントと合議結果を表示するUI, so that 投資判断のプロセスを理解し活用できる

#### Acceptance Criteria (MVP)
1. The Stock MAGI System shall CLIまたはシンプルなWebベースのインターフェースを提供する
2. When ユーザーが銘柄コードを入力, the Stock MAGI System shall 各エージェントの分析結果を個別に表示する
3. The Stock MAGI System shall 合議結果をテキスト形式で表示する

#### Acceptance Criteria (Phase 2)
4. The Stock MAGI System shall Webベースのダッシュボードを提供する
5. When ユーザーが分析条件を入力, the Stock MAGI System shall 各エージェントの分析結果を視覚的に表示する
6. The Stock MAGI System shall 合議結果を視覚的に分かりやすく表示する（ダッシュボード形式）
7. The Stock MAGI System shall 各エージェントの判断根拠を詳細モードで閲覧できる
8. When ユーザーがパラメータを変更, the Stock MAGI System shall リアルタイムで再分析を実行する
9. The Stock MAGI System shall 過去の分析結果と比較機能を提供する
1. When 各エージェントが分析を完了, the Stock MAGI System shall エージェント間の合議プロセスを実行する
2. The Stock MAGI System shall 各エージェントの判断（買い/売り/ホールド）と信頼度スコアを収集する
3. The Stock MAGI System shall 重み付け投票方式で最終的な投資判断を決定する
4. The Stock MAGI System shall エージェント間の意見の一致度を可視化する
5. When エージェント間で意見が大きく分かれる場合, the Stock MAGI System shall 警告を表示し、リスク評価を提示する
6. The Stock MAGI System shall 合議プロセスの履歴を記録する
### Requirement 6: データベース統合とデータ永続化（Phase 3 - Pending）
**Objective:** As a システム管理者, I want 個人でストックしたDBデータを合議のインプットに活用, so that 過去の取引履歴やカスタムデータを分析に組み込める

#### Acceptance Criteria (Phase 3 - Pending)
1. The Stock MAGI System shall DuckDBコネクタインターフェースを定義する（実装はコネクタ仕様確定後）
2. When DuckDB統合が有効化されている場合, the Stock MAGI System shall Jquants API由来の時系列データを取得する
3. When MCP経由でDuckDBにアクセス, the Stock MAGI System shall SQL問い合わせにより株式情報を取得する
4. The Stock MAGI System shall 過去の取引履歴、財務時系列データ、カスタム指標をエージェント分析のコンテキストとして利用する
5. The Stock MAGI System shall 分析結果と判断履歴をデータベースに保存する
6. The Stock MAGI System shall DuckDBスキーマを拡張可能な設計にする

#### Acceptance Criteria (Future Extension)
7. The Stock MAGI System shall PostgreSQL、MySQL、Cosmos DBなどの外部データベースもオプションとして接続できる
8. If データベース接続に失敗した場合, then the Stock MAGI System shall エラーメッセージを表示し、接続設定の見直しを促す
**Objective:** As a システム管理者, I want DuckDBに蓄積したJquants API由来の株式情報を合議のインプットに活用, so that 過去の取引履歴やカスタムデータを分析に組み込める

#### Acceptance Criteria
1. The Stock MAGI System shall DuckDBデータベースに接続できる（必須機能）
2. The Stock MAGI System shall Jquants APIから取得したデータをDuckDBに格納し、時系列データとして管理する
3. When MCP経由でDuckDBにアクセス, the Stock MAGI System shall SQL問い合わせにより株式情報を取得する
4. When データベース接続を設定, the Stock MAGI System shall ユーザー保存済みの株式情報を読み込む
5. The Stock MAGI System shall 過去の取引履歴、財務時系列データ、カスタム指標、メモをエージェント分析のコンテキストとして利用する
6. The Stock MAGI System shall 分析結果と判断履歴をDuckDBに保存する
7. The Stock MAGI System shall DuckDBのスキーマを拡張可能な設計にする
8. The Stock MAGI System shall PostgreSQL、MySQL、Cosmos DBなどの外部データベースもオプションとして接続できる
9. If データベース接続に失敗した場合, then the Stock MAGI System shall エラーメッセージを表示し、接続設定の見直しを促す

### Requirement 7: 低コスト運用とリソース最適化
**Objective:** As a システム管理者, I want できるだけ低コストで運用可能なアーキテクチャ, so that 継続的な利用が可能になる

#### Acceptance Criteria
1. The Stock MAGI System shall サーバーレスアーキテクチャ（Azure Functions、AWS Lambdaなど）を採用する
2. The Stock MAGI System shall 必要な時のみクラウドリソースを使用する従量課金モデルで動作する
3. The Stock MAGI System shall AIモデル推論にコスト効率の高いサービス（Azure OpenAI、Bedrock、またはローカルLLM）を使用する
4. The Stock MAGI System shall データキャッシュ機能により不要なAPI呼び出しを削減する
5. The Stock MAGI System shall リソース使用量とコストをモニタリングする機能を提供する
6. Where ローカル実行が可能, the Stock MAGI System shall オフライン分析モードを提供する

### Requirement 8: セキュリティとデータ保護
**Objective:** As a システム利用者, I want 個人の投資情報が安全に管理される, so that プライバシーとセキュリティが保護される

#### Acceptance Criteria
1. The Stock MAGI System shall ユーザー認証機能を実装する
2. The Stock MAGI System shall API キーと認証情報を暗号化して保存する
3. The Stock MAGI System shall データ通信にHTTPS/TLSを使用する
4. The Stock MAGI System shall ユーザーごとにデータを分離して管理する
5. When 機密データをログ出力する場合, the Stock MAGI System shall マスキング処理を適用する
6. The Stock MAGI System shall 定期的なセキュリティ更新とパッチ適用をサポートする

### Requirement 9: 拡張性と保守性
**Objective:** As a 開発者, I want 新しいエージェントやデータソースを追加しやすいアーキテクチャ, so that システムを継続的に改善できる

#### Acceptance Criteria
1. The Stock MAGI System shall エージェントをプラグイン方式で追加できる設計を採用する
### Requirement 10: テスト駆動開発とモニタリング（All Phases）
**Objective:** As a 開発者, I want TDD手法による包括的なテストスイート, so that 品質を保証しながら段階的に機能を追加できる

#### Acceptance Criteria (MVP - Phase 1)
1. The Stock MAGI System shall ユニットテストフレームワークを導入する（pytest、Jest、xUnit等）
2. The Stock MAGI System shall 各コンポーネント（データ取得、エージェント、合議）のユニットテストを実装する
3. The Stock MAGI System shall テストカバレッジ80%以上を維持する
4. The Stock MAGI System shall CI/CDパイプラインでテストを自動実行する
5. When 新機能を追加する場合, the Stock MAGI System shall テストファーストアプローチで実装する

#### Acceptance Criteria (Phase 2)
6. The Stock MAGI System shall インテグレーションテストを実装する
7. The Stock MAGI System shall エージェント分析結果の精度を追跡する機能を提供する
8. When 分析結果と実際の市場結果を比較, the Stock MAGI System shall エージェントのパフォーマンス指標を算出する

#### Acceptance Criteria (Phase 3)
9. The Stock MAGI System shall システムヘルスチェック機能を実装する
10. The Stock MAGI System shall エラー発生時にアラートを送信する
11. The Stock MAGI System shall バックテスト機能により過去データでの分析精度を検証できる
12. The Stock MAGI System shall E2Eテストをサポートする
1. The Stock MAGI System shall エージェント分析結果の精度を追跡する機能を提供する
2. When 分析結果と実際の市場結果を比較, the Stock MAGI System shall エージェントのパフォーマンス指標を算出する
3. The Stock MAGI System shall システムヘルスチェック機能を実装する
4. The Stock MAGI System shall エラー発生時にアラートを送信する
5. The Stock MAGI System shall バックテスト機能により過去データでの分析精度を検証できる
6. The Stock MAGI System shall ユニットテストとインテグレーションテストをサポートする
