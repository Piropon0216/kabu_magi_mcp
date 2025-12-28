"""
Common data models for agent consensus decisions.

These Pydantic models define the structure for agent votes and final decisions,
ensuring type safety and validation across all domain applications.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Action(str, Enum):
    """
    投資判断のアクション
    
    他ドメインへの流用例:
      - 不動産分析: BUY (購入), HOLD (保留), SELL (売却)
      - 医療診断: POSITIVE (陽性), NEGATIVE (陰性), UNCERTAIN (不明)
      - リスク評価: HIGH_RISK, MEDIUM_RISK, LOW_RISK
    """
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class AgentVote(BaseModel):
    """
    エージェント1つの投票結果
    
    Attributes:
        agent_name: エージェント名 (例: "Melchior", "Balthasar", "Casper")
        action: 推奨アクション
        confidence: 信頼度 (0.0-1.0)
        reasoning: 判断理由
    """
    agent_name: str = Field(..., description="エージェント名")
    action: Action = Field(..., description="推奨アクション")
    confidence: float = Field(..., ge=0.0, le=1.0, description="信頼度 (0.0-1.0)")
    reasoning: str = Field(..., min_length=10, description="判断理由 (最低10文字)")
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """信頼度が0-1の範囲内であることを検証"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return round(v, 2)  # 小数点2桁に丸める


class FinalDecision(BaseModel):
    """
    最終的な合議結果
    
    Attributes:
        final_action: 合議による最終アクション
        votes: 各エージェントの投票結果
        weighted_confidence: 加重平均された信頼度 (Phase 2 で実装)
        summary: 合議結果のサマリー
        has_conflict: 投票に対立があったか (例: 1票 BUY, 1票 SELL)
    """
    final_action: Action = Field(..., description="最終アクション")
    votes: list[AgentVote] = Field(..., min_length=1, description="エージェント投票リスト")
    weighted_confidence: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0, 
        description="加重平均信頼度 (Phase 2)"
    )
    summary: str = Field(..., min_length=20, description="合議結果サマリー (最低20文字)")
    has_conflict: bool = Field(False, description="投票対立フラグ")
    
    @field_validator('votes')
    @classmethod
    def validate_votes(cls, v: list[AgentVote]) -> list[AgentVote]:
        """投票リストが空でないことを検証"""
        if not v:
            raise ValueError("At least one agent vote is required")
        return v
    
    @field_validator('has_conflict')
    @classmethod
    def detect_conflict(cls, v: bool, info) -> bool:
        """投票の対立を自動検出 (Phase 2 で使用)"""
        # Phase 1 では手動設定、Phase 2 で自動検出ロジック追加
        return v


# エクスポート
__all__ = ["Action", "AgentVote", "FinalDecision"]
