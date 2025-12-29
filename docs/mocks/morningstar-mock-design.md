# Morningstar Mock Tests — Design

目的
- FastAPI の `/api/analyze` エンドポイントから Melchior エージェント経由で Morningstar (Foundry) 呼び出し経路が期待どおり動作することをモックで検証する。

検証対象
- API レイヤ -> `FoundryToolRegistry.get_tool("morningstar")` -> `create_melchior_agent(tool)` -> `MelchiorAgent.analyze()` の呼び出し経路
- ツールの正常応答 (BUY/SELL) とツール失敗時の例外ハンドリング

テストケース
1. bullish: Morningstar が BUY を返す → API が `final_action == "BUY"` を返す
2. bearish: Morningstar が SELL を返す → API が `final_action == "SELL"` を返す
3. failure: Morningstar が例外を発生させる → API が 500 エラーを返す

モック戦略
- `FoundryToolRegistry.get_tool` を monkeypatch してダミーの `mock_tool` を返す
- `create_melchior_agent` を monkeypatch して `MockAgent(tool)` を返す。`MockAgent.analyze` は `tool.mock_result` を返すか、`tool.raise_exc` が設定されていれば例外を投げる

実行方法
- テストは `tests/test_morningstar_mock.py` に実装
- 実行コマンド:
```bash
poetry run pytest tests/test_morningstar_mock.py -q
```

備考
- 既存の `MelchiorAgent.analyze` は Phase 1 のモック実装で実際に `foundry_tool` を呼び出していないため、テストでは `create_melchior_agent` を差し替える手法を採用します。
- 将来、`MelchiorAgent` が実際に `foundry_tool` を呼ぶようになれば、テストを修正して `FoundryToolRegistry.get_tool` のモックだけで十分になります。
