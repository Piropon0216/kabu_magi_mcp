"""
Unit tests for decision models
"""

import pytest

from src.common.models.decision_models import Action, AgentVote, FinalDecision


def test_action_enum():
    """Action enum の値をテスト"""
    assert Action.BUY.value == "BUY"
    assert Action.SELL.value == "SELL"
    assert Action.HOLD.value == "HOLD"


def test_agent_vote_valid():
    """AgentVote の正常系テスト"""
    vote = AgentVote(
        agent_name="Melchior",
        action=Action.BUY,
        confidence=0.85,
        reasoning="PER 12.5, ROE 15%, 自己資本比率 50% で財務健全"
    )

    assert vote.agent_name == "Melchior"
    assert vote.action == Action.BUY
    assert vote.confidence == 0.85
    assert "PER" in vote.reasoning


def test_agent_vote_confidence_range():
    """AgentVote の confidence 範囲チェック"""
    # 正常範囲
    vote = AgentVote(
        agent_name="Melchior",
        action=Action.HOLD,
        confidence=0.5,
        reasoning="不確実性が高いため HOLD を推奨します"
    )
    assert vote.confidence == 0.5

    # 範囲外 (0.0 未満) - Pydantic v2 では ValidationError
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        AgentVote(
            agent_name="Melchior",
            action=Action.BUY,
            confidence=-0.1,
            reasoning="Invalid confidence value test"
        )

    # 範囲外 (1.0 超過)
    with pytest.raises(ValidationError, match="less than or equal to 1"):
        AgentVote(
            agent_name="Melchior",
            action=Action.BUY,
            confidence=1.5,
            reasoning="Invalid confidence value test"
        )


def test_agent_vote_reasoning_min_length():
    """AgentVote の reasoning 最小文字数チェック"""
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="at least 10 characters"):
        AgentVote(
            agent_name="Melchior",
            action=Action.BUY,
            confidence=0.8,
            reasoning="Short"  # 10文字未満
        )


def test_final_decision_valid():
    """FinalDecision の正常系テスト"""
    votes = [
        AgentVote(
            agent_name="Melchior",
            action=Action.BUY,
            confidence=0.85,
            reasoning="ファンダメンタルズが良好で割安です"
        ),
        AgentVote(
            agent_name="Balthasar",
            action=Action.BUY,
            confidence=0.75,
            reasoning="上昇トレンドが継続しています"
        ),
    ]

    decision = FinalDecision(
        final_action=Action.BUY,
        votes=votes,
        weighted_confidence=0.80,
        summary="2エージェントが BUY 判定。ファンダメンタルズとテクニカル両面で買いシグナル。",
        has_conflict=False
    )

    assert decision.final_action == Action.BUY
    assert len(decision.votes) == 2
    assert decision.weighted_confidence == 0.80
    assert not decision.has_conflict


def test_final_decision_summary_min_length():
    """FinalDecision の summary 最小文字数チェック"""
    from pydantic import ValidationError
    votes = [
        AgentVote(
            agent_name="Melchior",
            action=Action.HOLD,
            confidence=0.5,
            reasoning="判断材料が不足しています"
        )
    ]

    with pytest.raises(ValidationError, match="at least 20 characters"):
        FinalDecision(
            final_action=Action.HOLD,
            votes=votes,
            summary="Short",  # 20文字未満
            has_conflict=False
        )


def test_final_decision_empty_votes():
    """FinalDecision の votes 空リストチェック"""
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="at least 1 item"):
        FinalDecision(
            final_action=Action.HOLD,
            votes=[],
            summary="エージェントが存在しないため判定不可能です",
            has_conflict=False
        )


def test_final_decision_conflict_detection_placeholder():
    """
    FinalDecision の has_conflict フラグテスト
    
    Phase 1: 手動設定
    Phase 2: 自動検出実装予定
    """
    votes = [
        AgentVote(
            agent_name="Melchior",
            action=Action.BUY,
            confidence=0.8,
            reasoning="ファンダメンタルズが良好です"
        ),
        AgentVote(
            agent_name="Casper",
            action=Action.SELL,
            confidence=0.7,
            reasoning="ネガティブなセンチメントが優勢です"
        ),
    ]

    decision = FinalDecision(
        final_action=Action.HOLD,
        votes=votes,
        summary="エージェント間で意見が対立しているため HOLD を推奨します。",
        has_conflict=True  # Phase 1: 手動設定
    )

    assert decision.has_conflict is True


__all__ = []  # テストモジュールはエクスポート不要
