"""
E2E tests for API endpoints
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture
async def client():
    """AsyncClient fixture for testing"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """ルートエンドポイントのテスト"""
    response = await client.get("/")

    if response.status_code != 200:
        print("[DEBUG] API error response:", response.text)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Stock MAGI System"
    assert data["version"] == "0.1.0 (Phase 1 MVP)"
    assert "endpoints" in data
    assert data["phase"] == "Phase 1 - Melchior agent + Morningstar tool (Foundry Tool Catalog)"


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """ヘルスチェックエンドポイントのテスト"""
    response = await client.get("/api/health")

    if response.status_code != 200:
        print("[DEBUG] API error response:", response.text)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_analyze_endpoint_success(client):
    """POST /api/analyze の正常系テスト"""
    request_data = {"ticker": "7203.T", "include_reasoning": True}

    response = await client.post("/api/analyze", json=request_data)

    if response.status_code != 200:
        print("[DEBUG] API error response:", response.text)
    assert response.status_code == 200
    data = response.json()

    # レスポンススキーマ検証
    assert "ticker" in data
    assert "final_action" in data
    assert "confidence" in data or data["confidence"] is None
    assert "summary" in data
    assert "reasoning" in data
    assert "has_conflict" in data

    # データ型検証
    assert data["ticker"] == "7203.T"
    assert data["final_action"] in ["BUY", "SELL", "HOLD"]
    assert isinstance(data["summary"], str)
    assert isinstance(data["reasoning"], list) or data["reasoning"] is None
    assert isinstance(data["has_conflict"], bool)


@pytest.mark.asyncio
async def test_analyze_endpoint_without_reasoning(client):
    """POST /api/analyze (include_reasoning=False) のテスト"""
    request_data = {"ticker": "AAPL", "include_reasoning": False}

    response = await client.post("/api/analyze", json=request_data)

    if response.status_code != 200:
        print("[DEBUG] API error response:", response.text)
    assert response.status_code == 200
    data = response.json()

    assert data["ticker"] == "AAPL"
    assert data["reasoning"] is None  # include_reasoning=False なので None


@pytest.mark.asyncio
async def test_analyze_endpoint_invalid_ticker():
    """POST /api/analyze の異常系テスト: 空の ticker"""
    request_data = {"ticker": "", "include_reasoning": True}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/analyze", json=request_data)

        # Pydantic バリデーションエラー (422)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_endpoint_missing_ticker():
    """POST /api/analyze の異常系テスト: ticker フィールド欠損"""
    request_data = {"include_reasoning": True}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/analyze", json=request_data)

        # Pydantic バリデーションエラー (422)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_analyze_endpoint_default_include_reasoning(client):
    """POST /api/analyze のデフォルト include_reasoning=True テスト"""
    request_data = {"ticker": "MSFT"}

    response = await client.post("/api/analyze", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # デフォルト True なので reasoning が含まれる
    assert data["reasoning"] is not None


@pytest.mark.asyncio
async def test_analyze_endpoint_multiple_tickers(client):
    """複数の銘柄コードでの E2E テスト"""
    tickers = ["7203.T", "AAPL", "MSFT", "GOOGL"]

    for ticker in tickers:
        request_data = {"ticker": ticker, "include_reasoning": True}

        response = await client.post("/api/analyze", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == ticker


@pytest.mark.asyncio
async def test_openapi_docs_available(client):
    """OpenAPI ドキュメントが利用可能かテスト"""
    response = await client.get("/docs")

    # Swagger UI リダイレクト (307) または成功 (200)
    assert response.status_code in [200, 307]


__all__ = []  # テストモジュールはエクスポート不要
