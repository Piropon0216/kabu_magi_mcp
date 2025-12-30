"""
Reusable Consensus Orchestrator using Microsoft Agent Framework.

This orchestrator wraps Agent Framework's GroupChatOrchestrator to provide
a domain-agnostic consensus mechanism for multi-agent systems.
"""

import datetime
import inspect
import json
import logging
import os
from typing import Any

from src.common.models.decision_models import Action, AgentVote, FinalDecision

_logger = logging.getLogger(__name__)


class ReusableConsensusOrchestrator:
    """
    ドメイン非依存の汎用マルチエージェント合議エンジン

    Agent Framework の GroupChatOrchestrator をラップし、
    投票ベースの合議ロジックを提供します。

    使用例:
      - 株式分析: 3エージェント(Melchior, Balthasar, Casper)で Buy/Sell/Hold判定
      - 不動産分析: 3エージェント(Location, Finance, Risk)で投資判定
      - 医療診断: 3エージェント(Radiology, Pathology, Clinical)で診断支援

    Phase 1 (MVP): シンプルな多数決
    Phase 2: 加重投票、対立検出
    """

    def __init__(self, agents: list[Any], voting_strategy: str | None = "majority"):
        """
        Initialize the consensus orchestrator

        Args:
            agents: Agent Framework の Agent インスタンスリスト
            voting_strategy: 投票戦略 ("majority" or "weighted")
                - "majority": 多数決 (Phase 1)
                - "weighted": 加重投票 (Phase 2)
        """
        self.agents = agents
        self.voting_strategy = voting_strategy

        # Phase 2 で Agent Framework の GroupChatOrchestrator を実装
        # from agent_framework import GroupChatOrchestrator
        # self.group_chat = GroupChatOrchestrator(agents=agents)

    async def reach_consensus(self, input_context: dict[str, Any]) -> FinalDecision:
        """
        マルチエージェント合議を実行し、最終決定を返す

        Args:
            input_context: 分析対象データ (例: {"ticker": "7203.T", "market_data": {...}})

        Returns:
            FinalDecision: 合議結果

        Phase 1 実装:
            1. 各エージェントに独立して推論を依頼
            2. 投票結果を集計
            3. 多数決で最終アクションを決定

        Phase 2 拡張予定:
            - Agent Framework の GroupChat による自動ディスカッション
            - 加重投票ロジック
            - 対立検出とリスク警告
        """
        # Phase 1: Placeholder implementation
        # 実際の Agent Framework 統合は次のステップで実装

        votes: list[AgentVote] = []

        # 各エージェントから投票を収集
        for idx, agent in enumerate(self.agents):
            agent_name = getattr(agent, "name", "UnknownAgent")

            # If caller already provided an analysis result for the first agent, use it
            if idx == 0 and "analysis_result" in input_context:
                provided = input_context.get("analysis_result")
                if isinstance(provided, dict):
                    action_str = provided.get("action")
                    confidence = float(provided.get("confidence", 0.5))
                    reasoning = provided.get("reasoning", "")
                    try:
                        action_enum = Action(action_str)
                    except Exception:
                        action_enum = (
                            Action(action_str.upper())
                            if isinstance(action_str, str)
                            else Action.HOLD
                        )
                    votes.append(
                        AgentVote(
                            agent_name=agent_name,
                            action=action_enum,
                            confidence=confidence,
                            reasoning=reasoning,
                        )
                    )
                    continue

            # If agent exposes async `analyze`, call it and parse the result.
            # Use `inspect.iscoroutinefunction` to avoid awaiting MagicMock
            # attributes (MagicMock provides attributes dynamically).
            analyze_attr = getattr(agent, "analyze", None)
            if analyze_attr and inspect.iscoroutinefunction(analyze_attr):
                try:
                    result = await analyze_attr(input_context.get("ticker", ""))
                    # Expect result to be a dict like {"action": "BUY", "confidence": 0.8, "reasoning": "..."}
                    action_str = result.get("action") if isinstance(result, dict) else None
                    confidence = (
                        float(result.get("confidence", 0.5)) if isinstance(result, dict) else 0.5
                    )
                    reasoning = result.get("reasoning", "") if isinstance(result, dict) else ""

                    if isinstance(action_str, str):
                        try:
                            action_enum = Action(action_str)
                        except Exception:
                            # Upper-case mapping fallback
                            action_enum = (
                                Action(action_str.upper())
                                if isinstance(action_str, str)
                                else Action.HOLD
                            )
                    else:
                        action_enum = Action.HOLD

                    vote = AgentVote(
                        agent_name=agent_name,
                        action=action_enum,
                        confidence=confidence,
                        reasoning=reasoning,
                    )
                    votes.append(vote)
                    continue
                except Exception:
                    # On agent error, append a neutral HOLD vote
                    votes.append(
                        AgentVote(
                            agent_name=agent_name,
                            action=Action.HOLD,
                            confidence=0.0,
                            reasoning="agent error",
                        )
                    )
                    continue

            # Fallback mock vote
            votes.append(
                AgentVote(
                    agent_name=agent_name,
                    action=Action.HOLD,
                    confidence=0.5,
                    reasoning="Phase 1 MVP - モック実装。",
                )
            )

        # 多数決で最終アクションを決定
        final_action = self._calculate_majority_vote(votes)

        # 合議結果を作成
        decision = FinalDecision(
            final_action=final_action,
            votes=votes,
            weighted_confidence=None,  # Phase 2 で実装
            summary=f"Phase 1 MVP: {len(votes)}エージェントによる合議結果。最終アクション: {final_action.value}",
            has_conflict=False,  # Phase 2 で自動検出
        )

        # Structured JSON-lines logging for audit/replay if path is configured
        try:
            log_path = os.environ.get("CONSENSUS_LOG_PATH")
            if log_path:
                record = {
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "ticker": input_context.get("ticker"),
                    "final_action": decision.final_action.value,
                    "summary": decision.summary,
                    "votes": [
                        {
                            "agent_name": v.agent_name,
                            "action": v.action.value
                            if hasattr(v.action, "value")
                            else str(v.action),
                            "confidence": float(v.confidence)
                            if getattr(v, "confidence", None) is not None
                            else None,
                            "reasoning": getattr(v, "reasoning", ""),
                        }
                        for v in decision.votes
                    ],
                }
                dirpath = os.path.dirname(log_path) or "."
                os.makedirs(dirpath, exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                _logger.debug("Consensus recorded to %s", log_path)
        except Exception:
            _logger.exception("Failed to write consensus log")

        return decision

    def _calculate_majority_vote(self, votes: list[AgentVote]) -> Action:
        """
        多数決でアクションを決定

        Args:
            votes: エージェント投票リスト

        Returns:
            最多票のアクション
        """
        if not votes:
            return Action.HOLD  # デフォルト

        # 投票数をカウント
        vote_counts: dict[Action, int] = {}
        for vote in votes:
            vote_counts[vote.action] = vote_counts.get(vote.action, 0) + 1

        # 最多票のアクションを返す
        return max(vote_counts, key=vote_counts.get)  # type: ignore


class VotingStrategy:
    """
    投票戦略の抽象クラス (Phase 2 で実装予定)

    サブクラス:
        - MajorityVotingStrategy: 多数決
        - WeightedVotingStrategy: 加重投票 (エージェント重み付け)
    """

    pass


# エクスポート
__all__ = ["ReusableConsensusOrchestrator", "VotingStrategy"]
