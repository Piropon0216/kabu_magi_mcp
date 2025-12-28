"""
Reusable Consensus Orchestrator using Microsoft Agent Framework.

This orchestrator wraps Agent Framework's GroupChatOrchestrator to provide
a domain-agnostic consensus mechanism for multi-agent systems.
"""

from typing import Any, Optional
from ..models.decision_models import Action, AgentVote, FinalDecision


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
    
    def __init__(self, agents: list[Any], voting_strategy: Optional[str] = "majority"):
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
    
    async def reach_consensus(
        self, 
        input_context: dict[str, Any]
    ) -> FinalDecision:
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
        
        # 各エージェントから投票を収集 (Phase 1: モック実装)
        for agent in self.agents:
            # TODO: Agent Framework の Agent.run() を呼び出し
            # response = await agent.run(input_context)
            # vote = self._parse_agent_response(response)
            
            # モック投票 (Phase 1 MVP)
            vote = AgentVote(
                agent_name=getattr(agent, "name", "UnknownAgent"),
                action=Action.HOLD,  # デフォルト
                confidence=0.5,
                reasoning="Phase 1 MVP - モック実装。Phase 2 で Agent Framework 統合予定。"
            )
            votes.append(vote)
        
        # 多数決で最終アクションを決定
        final_action = self._calculate_majority_vote(votes)
        
        # 合議結果を作成
        decision = FinalDecision(
            final_action=final_action,
            votes=votes,
            weighted_confidence=None,  # Phase 2 で実装
            summary=f"Phase 1 MVP: {len(votes)}エージェントによる合議結果。最終アクション: {final_action.value}",
            has_conflict=False  # Phase 2 で自動検出
        )
        
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
