"""
Melchior Agent: ファンダメンタルズ分析専門エージェント

Microsoft Agent Framework を使用した実装。
Phase 1 では Morningstar MCP Server (Foundry Tool Catalog) を使用。
"""

import inspect
from typing import Any

from ..prompts.stock_analysis_prompts import (
    create_melchior_analysis_prompt,
)


class MelchiorAgent:
    """
    Melchior エージェント - ファンダメンタルズ分析専門

    Phase 1 実装:
        - Agent Framework の Agent クラスをラップ
        - Morningstar tool (Foundry Tool Catalog) を使用
        - BUY/SELL/HOLD 判定を返す

    Phase 2 拡張予定:
        - Agent Framework の完全な Agent 実装
        - Tool calling の自動実行
        - 履歴管理とコンテキスト保持
    """

    def __init__(self, foundry_tool: Any):
        """
        Initialize Melchior agent

        Args:
            foundry_tool: Foundry Tool Catalog から取得した Morningstar tool

        Phase 1: モック実装
        Phase 2: Agent Framework の Agent クラスで実装
        """
        self.name = "Melchior"
        self.role = "ファンダメンタルズ分析"
        self.foundry_tool = foundry_tool

        # Phase 2 で Agent Framework 統合
        # from agent_framework import Agent
        # self.agent = Agent(
        #     name=self.name,
        #     system_message=MELCHIOR_SYSTEM_MESSAGE,
        #     tools=[foundry_tool]
        # )

    async def analyze(self, ticker: str) -> dict[str, Any]:
        """
        銘柄を分析し、投資判断を返す

        Args:
            ticker: 銘柄コード (例: "7203.T")

        Returns:
            {
                "action": "BUY/SELL/HOLD",
                "confidence": 0.0-1.0,
                "reasoning": "分析根拠"
            }

        Phase 1 実装:
            1. Morningstar tool で市場データ取得 (モック)
            2. プロンプト生成
            3. 投資判断を返す (Phase 1: 固定値)

        Phase 2 拡張:
            - Agent Framework の Agent.run() で自動実行
            - Tool calling で実際の Morningstar データ取得
            - LLM による動的判断
        """
        # If a Foundry tool client exists and exposes an async `get_fundamentals`, use it.
        gf = getattr(self.foundry_tool, "get_fundamentals", None)
        if gf is not None and inspect.iscoroutinefunction(gf):
            try:
                market_data = await gf(ticker)
            except Exception:
                return {"action": "HOLD", "confidence": 0.0, "reasoning": "Foundry call failed"}

            # Prompt still generated for future LLM integration
            _analysis_prompt = create_melchior_analysis_prompt(ticker, market_data)

            # Simple heuristic mapping from foundry output to action
            rec = market_data.get("recommendation") if isinstance(market_data, dict) else None
            if isinstance(rec, str):
                if rec.lower() in ("buy", "strong_buy"):
                    return {
                        "action": "BUY",
                        "confidence": 0.8,
                        "reasoning": f"Foundry recommendation: {rec}",
                    }
                if rec.lower() in ("sell", "strong_sell"):
                    return {
                        "action": "SELL",
                        "confidence": 0.8,
                        "reasoning": f"Foundry recommendation: {rec}",
                    }

            fair = market_data.get("fair_value")
            price = market_data.get("price")
            if isinstance(fair, int | float) and isinstance(price, int | float):
                if fair > price:
                    return {"action": "BUY", "confidence": 0.7, "reasoning": "fair_value > price"}
                if fair < price:
                    return {"action": "SELL", "confidence": 0.7, "reasoning": "fair_value < price"}

        # Fallback Phase 1 mock response
        _analysis_prompt = create_melchior_analysis_prompt(ticker, {"ticker": ticker})
        return {
            "action": "HOLD",
            "confidence": 0.5,
            "reasoning": f"Phase 1 MVP - {ticker} のモック分析。",
        }


def create_melchior_agent(foundry_tool: Any) -> MelchiorAgent:
    """
    Melchior エージェントを作成 (Factory function)

    Args:
        foundry_tool: Foundry Tool Catalog から取得した Morningstar tool

    Returns:
        MelchiorAgent インスタンス

    使用例:
        >>> from src.common.mcp import FoundryToolRegistry
        >>> registry = FoundryToolRegistry()
        >>> morningstar_tool = registry.get_tool("morningstar")
        >>> melchior = create_melchior_agent(morningstar_tool)
        >>> result = await melchior.analyze("7203.T")
    """
    return MelchiorAgent(foundry_tool)


__all__ = ["MelchiorAgent", "create_melchior_agent"]
