"""
Live integration tests against a real Foundry endpoint.

These tests are skipped unless the required environment variables are present:
- FOUNDRY_ENDPOINT
- FOUNDRY_API_KEY
- FOUNDRY_DEPLOYMENT
- FOUNDRY_API_VERSION

They are intended to be run in a protected CI environment with secrets configured,
or locally by a developer with valid credentials. Marked with pytest marker `integration`.
"""

import os

import pytest
from httpx import ASGITransport, AsyncClient

from src.common.mcp import FoundryToolRegistry
from src.main import app

REQUIRED = ["FOUNDRY_ENDPOINT", "FOUNDRY_API_KEY", "FOUNDRY_DEPLOYMENT", "FOUNDRY_API_VERSION"]


def has_foundry_envs() -> bool:
    return all(os.environ.get(k) for k in REQUIRED)


@pytest.mark.skipif(not has_foundry_envs(), reason="FOUNDRY env vars not set")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_foundry_buy_path():
    registry = FoundryToolRegistry()
    tool = registry.get_tool("morningstar")

    # perform a live call (may raise on network/auth issues)
    data = await tool.get_fundamentals("7203.T")
    assert isinstance(data, dict)


@pytest.mark.skipif(not has_foundry_envs(), reason="FOUNDRY env vars not set")
@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_invoke_live_foundry():
    # Ensure API endpoint flow works end-to-end against live Foundry
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/analyze", json={"ticker": "7203.T", "include_reasoning": False}
        )
        assert resp.status_code == 200


__all__ = []
