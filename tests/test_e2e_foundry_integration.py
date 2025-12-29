"""
E2E style integration tests that exercise the real Foundry tool client path.

These tests monkeypatch the FoundryHTTPTool.get_fundamentals method so the
HTTP layer is not required during CI, but they exercise the full API ->
MelchiorAgent -> Foundry client -> Orchestrator flow.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.common.mcp.foundry_tool_registry import FoundryToolRegistry


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_e2e_foundry_buy_path(monkeypatch, client):
    """Foundry indicates fair_value > price -> final action should be BUY"""

    async def fake_get_fundamentals(self, ticker: str):
        return {"ticker": ticker, "price": 100.0, "fair_value": 150.0}

    # Patch the registry to return a tool whose get_fundamentals is our fake
    original_get_tool = FoundryToolRegistry.get_tool

    def _get_tool(self, name: str):
        tool = original_get_tool(self, name)
        # monkeypatch the instance method
        monkeypatch.setattr(tool, "get_fundamentals", fake_get_fundamentals.__get__(tool, type(tool)))
        return tool

    monkeypatch.setattr(FoundryToolRegistry, "get_tool", _get_tool)

    response = await client.post("/api/analyze", json={"ticker": "7203.T", "include_reasoning": True})
    assert response.status_code == 200
    data = response.json()

    assert data["ticker"] == "7203.T"
    assert data["final_action"] == "BUY"


@pytest.mark.asyncio
async def test_e2e_foundry_sell_path(monkeypatch, client):
    """Foundry indicates fair_value < price -> final action should be SELL"""

    async def fake_get_fundamentals(self, ticker: str):
        return {"ticker": ticker, "price": 200.0, "fair_value": 120.0}

    original_get_tool = FoundryToolRegistry.get_tool

    def _get_tool(self, name: str):
        tool = original_get_tool(self, name)
        monkeypatch.setattr(tool, "get_fundamentals", fake_get_fundamentals.__get__(tool, type(tool)))
        return tool

    monkeypatch.setattr(FoundryToolRegistry, "get_tool", _get_tool)

    response = await client.post("/api/analyze", json={"ticker": "AAPL", "include_reasoning": True})
    assert response.status_code == 200
    data = response.json()

    assert data["ticker"] == "AAPL"
    assert data["final_action"] == "SELL"


__all__ = []
