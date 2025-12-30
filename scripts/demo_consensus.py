#!/usr/bin/env python3
"""CLI demo for 3-agent consensus (mock / MCP / JQuants optional).

Usage examples:
  python scripts/demo_consensus.py --ticker 7203.T --data-source mock
  MCP: MCP_URL=http://localhost:8000 python scripts/demo_consensus.py --data-source mcp
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx

from src.common.consensus.orchestrators.group_chat_consensus import ReusableConsensusOrchestrator
from src.common.models.decision_models import FinalDecision


class MarketDataProvider:
    def __init__(self, source: str = "mock", mcp_url: str | None = None):
        self.source = source
        self.mcp_url = mcp_url

    def get_price_data(self, ticker: str) -> dict[str, Any]:
        if self.source == "mock":
            # deterministic mock data
            history = [1000.0, 1005.0, 1010.0, 1008.0, 1015.0]
            return {"price": history[-1], "history": history, "prev_close": history[-2]}

        if self.source == "mcp":
            if not self.mcp_url:
                raise RuntimeError("MCP_URL required for mcp data source")
            url = f"{self.mcp_url.rstrip('/')}/tools/jquants/price/{ticker}"
            with httpx.Client(timeout=5.0) as client:
                r = client.get(url)
                r.raise_for_status()
                data = r.json()
                # Expect data to contain price/history if MCP implements it; fall back
                return {
                    "price": float(data.get("price", 0)),
                    "history": data.get("history", []),
                    "prev_close": float(data.get("prev_close", 0)),
                }

        if self.source == "jquants":
            # Try to use local sample client if available
            try:
                from sample import client as sample_client

                c = sample_client.JQuantsAPIClient()
                # sample client may expose get_latest_price; adapt if needed
                price = getattr(c, "get_latest_price", lambda t: {"price": 0})(ticker)
                if isinstance(price, dict) and "price" in price:
                    return {"price": float(price["price"]), "history": price.get("history", []), "prev_close": price.get("prev_close", 0)}
            except Exception:
                raise RuntimeError("jquants data source not implemented in this demo or client unavailable")

        raise RuntimeError("unknown data source")


class BaseAgent:
    def __init__(self, name: str, provider: MarketDataProvider):
        self.name = name
        self.provider = provider

    async def analyze(self, ticker: str) -> dict[str, Any]:
        raise NotImplementedError()


class FundamentalAgent(BaseAgent):
    async def analyze(self, ticker: str) -> dict[str, Any]:
        data = self.provider.get_price_data(ticker)
        price = float(data.get("price", 0))
        # naive rule: price > 1005 -> BUY, <1002 -> SELL, else HOLD
        if price > 1005:
            action = "BUY"
            confidence = 0.7
        elif price < 1002:
            action = "SELL"
            confidence = 0.6
        else:
            action = "HOLD"
            confidence = 0.5
        return {"action": action, "confidence": confidence, "reasoning": f"Fundamental rule on price {price}"}


class TechnicalAgent(BaseAgent):
    async def analyze(self, ticker: str) -> dict[str, Any]:
        data = self.provider.get_price_data(ticker)
        history = data.get("history", [])
        if not history:
            return {"action": "HOLD", "confidence": 0.5, "reasoning": "no history"}
        avg = sum(history) / len(history)
        last = history[-1]
        if last > avg:
            return {"action": "BUY", "confidence": 0.65, "reasoning": "price above moving average"}
        if last < avg:
            return {"action": "SELL", "confidence": 0.6, "reasoning": "price below moving average"}
        return {"action": "HOLD", "confidence": 0.5, "reasoning": "at average"}


class SentimentAgent(BaseAgent):
    async def analyze(self, ticker: str) -> dict[str, Any]:
        data = self.provider.get_price_data(ticker)
        history = data.get("history", [])
        if len(history) < 2:
            return {"action": "HOLD", "confidence": 0.5, "reasoning": "insufficient data"}
        change = history[-1] - history[-2]
        if change > 0:
            return {"action": "BUY", "confidence": 0.55, "reasoning": "recent uptick"}
        if change < 0:
            return {"action": "SELL", "confidence": 0.55, "reasoning": "recent downtick"}
        return {"action": "HOLD", "confidence": 0.5, "reasoning": "no change"}


def to_json(decision: FinalDecision) -> dict[str, Any]:
    return {
        "final_action": decision.final_action.value,
        "votes": [v.model_dump() if hasattr(v, "model_dump") else v.__dict__ for v in decision.votes],
        "summary": decision.summary,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", default="7203.T")
    parser.add_argument("--data-source", choices=["mock", "mcp", "jquants"], default="mock")
    parser.add_argument("--mcp-url", default=os.environ.get("MCP_URL"))
    args = parser.parse_args(argv)

    provider = MarketDataProvider(source=args.data_source, mcp_url=args.mcp_url)

    agents = [FundamentalAgent("Fundamental", provider), TechnicalAgent("Technical", provider), SentimentAgent("Sentiment", provider)]

    orchestrator = ReusableConsensusOrchestrator(agents=agents, voting_strategy="majority")

    import asyncio

    decision = asyncio.run(orchestrator.reach_consensus({"ticker": args.ticker}))

    out = to_json(decision)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("Summary:", decision.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
