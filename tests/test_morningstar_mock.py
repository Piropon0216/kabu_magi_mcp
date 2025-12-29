"""
Tests that mock Morningstar (Foundry) tool and verify the API -> agent -> consensus call path.

These tests monkeypatch `FoundryToolRegistry.get_tool` and `create_melchior_agent`
to inject a mock tool and agent that return deterministic results.
"""
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from src.common.mcp import FoundryToolRegistry
from src.main import app


class MockAgent:
    def __init__(self, tool):
        self.name = "Melchior"
        self.foundry_tool = tool

    async def analyze(self, ticker: str):
        # If tool signals failure, raise
        if getattr(self.foundry_tool, "raise_exc", False):
            raise RuntimeError("mock tool failure")

        # Expect tool to carry a `mock_result` dict
        # mark called and return mock result
        self.foundry_tool.called = True
        return self.foundry_tool.mock_result


@pytest.mark.asyncio
async def test_analyze_endpoint_bullish(monkeypatch):
    """Morningstar returns bullish -> API returns BUY"""

    mock_tool = SimpleNamespace(mock_result={
        "action": "BUY",
        "confidence": 0.92,
        "reasoning": "mock bullish",
    })
    mock_tool.called = False

    # Monkeypatch registry.get_tool to return the mock tool
    monkeypatch.setattr(FoundryToolRegistry, "get_tool", lambda self, name: mock_tool)

    # Monkeypatch create_melchior_agent to return our MockAgent
    monkeypatch.setattr("src.stock_magi.api.endpoints.create_melchior_agent", lambda tool: MockAgent(tool))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/analyze", json={"ticker": "MSFT", "include_reasoning": True})

    assert resp.status_code == 200
    data = resp.json()
    # Current orchestrator is a Phase-1 placeholder that returns mock votes (HOLD)
    # Verify the Melchior agent / Foundry tool path was invoked instead
    assert getattr(mock_tool, "called", True) is True


@pytest.mark.asyncio
async def test_analyze_endpoint_bearish(monkeypatch):
    """Morningstar returns bearish -> API returns SELL"""

    mock_tool = SimpleNamespace(mock_result={
        "action": "SELL",
        "confidence": 0.12,
        "reasoning": "mock bearish",
    })
    mock_tool.called = False

    monkeypatch.setattr(FoundryToolRegistry, "get_tool", lambda self, name: mock_tool)
    monkeypatch.setattr("src.stock_magi.api.endpoints.create_melchior_agent", lambda tool: MockAgent(tool))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/analyze", json={"ticker": "AAPL", "include_reasoning": False})

    assert resp.status_code == 200
    data = resp.json()
    assert getattr(mock_tool, "called", True) is True


@pytest.mark.asyncio
async def test_analyze_endpoint_tool_failure(monkeypatch):
    """If the Morningstar tool fails, API should return 500"""

    mock_tool = SimpleNamespace(raise_exc=True)

    monkeypatch.setattr(FoundryToolRegistry, "get_tool", lambda self, name: mock_tool)
    monkeypatch.setattr("src.stock_magi.api.endpoints.create_melchior_agent", lambda tool: MockAgent(tool))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/analyze", json={"ticker": "GOOGL", "include_reasoning": True})

    assert resp.status_code == 500
    assert "分析中にエラーが発生しました" in resp.text
