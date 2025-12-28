"""
Integration tests for Melchior Agent
"""

import pytest
from unittest.mock import MagicMock
from src.stock_magi.agents import create_melchior_agent, MelchiorAgent
from src.common.models import Action


@pytest.mark.asyncio
async def test_create_melchior_agent():
    """create_melchior_agent factory function のテスト"""
    mock_tool = MagicMock()
    mock_tool.name = "morningstar"
    
    agent = create_melchior_agent(mock_tool)
    
    assert isinstance(agent, MelchiorAgent)
    assert agent.name == "Melchior"
    assert agent.role == "ファンダメンタルズ分析"
    assert agent.foundry_tool == mock_tool


@pytest.mark.asyncio
async def test_melchior_agent_analyze():
    """Melchior エージェントの analyze メソッドテスト"""
    mock_tool = MagicMock()
    mock_tool.name = "morningstar"
    
    agent = create_melchior_agent(mock_tool)
    
    # 分析実行
    result = await agent.analyze("7203.T")
    
    assert "action" in result
    assert "confidence" in result
    assert "reasoning" in result
    assert result["action"] in ["BUY", "SELL", "HOLD"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert len(result["reasoning"]) >= 10  # 最低文字数


@pytest.mark.asyncio
async def test_melchior_agent_analyze_phase1_mock():
    """
    Phase 1: モック実装のテスト
    
    Phase 2: 実際の Agent Framework 統合後に更新
    """
    mock_tool = MagicMock()
    agent = create_melchior_agent(mock_tool)
    
    result = await agent.analyze("7203.T")
    
    # Phase 1: デフォルト HOLD を返す
    assert result["action"] == "HOLD"
    assert result["confidence"] == 0.5
    assert "Phase 1 MVP" in result["reasoning"]


@pytest.mark.asyncio
async def test_melchior_agent_different_tickers():
    """異なる銘柄コードでの分析テスト"""
    mock_tool = MagicMock()
    agent = create_melchior_agent(mock_tool)
    
    tickers = ["7203.T", "AAPL", "MSFT"]
    
    for ticker in tickers:
        result = await agent.analyze(ticker)
        
        assert "action" in result
        assert "confidence" in result
        assert "reasoning" in result


@pytest.mark.asyncio
async def test_melchior_agent_properties():
    """Melchior エージェントのプロパティテスト"""
    mock_tool = MagicMock()
    agent = create_melchior_agent(mock_tool)
    
    assert agent.name == "Melchior"
    assert agent.role == "ファンダメンタルズ分析"
    assert hasattr(agent, "foundry_tool")


__all__ = []  # テストモジュールはエクスポート不要
