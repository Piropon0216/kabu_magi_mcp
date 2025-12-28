"""
Unit tests for Consensus Orchestrator
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.common.consensus.orchestrators import ReusableConsensusOrchestrator
from src.common.models import Action, AgentVote, FinalDecision


@pytest.mark.asyncio
async def test_consensus_orchestrator_single_agent():
    """単一エージェントでの合議テスト"""
    # モックエージェント作成
    mock_agent = MagicMock()
    mock_agent.name = "Melchior"
    
    orchestrator = ReusableConsensusOrchestrator(
        agents=[mock_agent],
        voting_strategy="majority"
    )
    
    # 合議実行
    decision = await orchestrator.reach_consensus(
        input_context={"ticker": "7203.T"}
    )
    
    assert isinstance(decision, FinalDecision)
    assert decision.final_action in [Action.BUY, Action.SELL, Action.HOLD]
    assert len(decision.votes) == 1
    assert decision.votes[0].agent_name == "Melchior"


@pytest.mark.asyncio
async def test_consensus_orchestrator_multiple_agents():
    """複数エージェントでの合議テスト"""
    # モックエージェント作成 (name を文字列で設定)
    mock_agents = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]
    mock_agents[0].name = "Melchior"
    mock_agents[1].name = "Balthasar"
    mock_agents[2].name = "Casper"
    
    orchestrator = ReusableConsensusOrchestrator(
        agents=mock_agents,
        voting_strategy="majority"
    )
    
    # 合議実行
    decision = await orchestrator.reach_consensus(
        input_context={"ticker": "7203.T"}
    )
    
    assert isinstance(decision, FinalDecision)
    assert len(decision.votes) == 3
    assert {vote.agent_name for vote in decision.votes} == {"Melchior", "Balthasar", "Casper"}


@pytest.mark.asyncio
async def test_majority_voting_buy():
    """多数決テスト: BUY が多数の場合"""
    orchestrator = ReusableConsensusOrchestrator(
        agents=[],
        voting_strategy="majority"
    )
    
    votes = [
        AgentVote(agent_name="Melchior", action=Action.BUY, confidence=0.8, reasoning="ファンダメンタルズが良好"),
        AgentVote(agent_name="Balthasar", action=Action.BUY, confidence=0.7, reasoning="上昇トレンドが継続中"),
        AgentVote(agent_name="Casper", action=Action.SELL, confidence=0.6, reasoning="センチメントが悪化中"),
    ]
    
    final_action = orchestrator._calculate_majority_vote(votes)
    
    assert final_action == Action.BUY


@pytest.mark.asyncio
async def test_majority_voting_hold():
    """多数決テスト: HOLD が多数の場合"""
    orchestrator = ReusableConsensusOrchestrator(
        agents=[],
        voting_strategy="majority"
    )
    
    votes = [
        AgentVote(agent_name="Melchior", action=Action.HOLD, confidence=0.5, reasoning="判断材料が不足しています"),
        AgentVote(agent_name="Balthasar", action=Action.HOLD, confidence=0.5, reasoning="トレンドが不明瞭です"),
        AgentVote(agent_name="Casper", action=Action.BUY, confidence=0.6, reasoning="弱い買いシグナル検出"),
    ]
    
    final_action = orchestrator._calculate_majority_vote(votes)
    
    assert final_action == Action.HOLD


@pytest.mark.asyncio
async def test_majority_voting_empty_votes():
    """多数決テスト: 投票が空の場合 (デフォルト HOLD)"""
    orchestrator = ReusableConsensusOrchestrator(
        agents=[],
        voting_strategy="majority"
    )
    
    final_action = orchestrator._calculate_majority_vote([])
    
    assert final_action == Action.HOLD


@pytest.mark.asyncio
async def test_voting_strategy_majority():
    """投票戦略: majority が正しく設定されるかテスト"""
    orchestrator = ReusableConsensusOrchestrator(
        agents=[],
        voting_strategy="majority"
    )
    
    assert orchestrator.voting_strategy == "majority"


@pytest.mark.asyncio
async def test_voting_strategy_weighted_placeholder():
    """
    投票戦略: weighted (Phase 2 実装予定)
    
    Phase 1: パラメータのみ受け入れ可能
    Phase 2: 加重投票ロジック実装
    """
    orchestrator = ReusableConsensusOrchestrator(
        agents=[],
        voting_strategy="weighted"
    )
    
    assert orchestrator.voting_strategy == "weighted"


__all__ = []  # テストモジュールはエクスポート不要
