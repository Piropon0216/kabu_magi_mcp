"""
FastAPI endpoints for Stock MAGI system.

POST /api/analyze - 銘柄分析エンドポイント
"""


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.common.consensus import ReusableConsensusOrchestrator
from src.common.mcp import FoundryToolRegistry
from src.common.models import Action, FinalDecision
from src.stock_magi.agents import create_melchior_agent

router = APIRouter(prefix="/api", tags=["analysis"])


class AnalyzeRequest(BaseModel):
    """銘柄分析リクエスト"""
    ticker: str = Field(..., description="銘柄コード (例: '7203.T' for Toyota)", min_length=1)
    include_reasoning: bool = Field(default=True, description="推論プロセスを含めるか")


class AnalyzeResponse(BaseModel):
    """銘柄分析レスポンス"""
    ticker: str
    final_action: Action
    confidence: float | None = None
    summary: str
    reasoning: list[dict] | None = None
    has_conflict: bool


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_stock(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    銘柄を分析し、投資判断を返す
    
    Phase 1 実装:
        - Melchior エージェントのみ (単一エージェント)
        - Morningstar tool (Foundry Tool Catalog)
        - モック投票による合議
    
    Phase 2 拡張予定:
        - Balthasar, Casper エージェント追加
        - 実際の Agent Framework 統合
        - 加重投票
    
    Args:
        request: 分析リクエスト
    
    Returns:
        分析結果 (FinalDecision)
    
    Raises:
        HTTPException: 分析失敗時
    """
    try:
        # 1. Foundry Tool Registry から Morningstar tool を取得
        registry = FoundryToolRegistry()
        morningstar_tool = registry.get_tool("morningstar")

        # 2. Melchior エージェントを作成
        melchior = create_melchior_agent(morningstar_tool)

        # 3. Phase 1: 単一エージェント分析 (Phase 2 で複数エージェント合議)
        analysis_result = await melchior.analyze(request.ticker)

        # 4. Consensus Orchestrator で合議 (Phase 1: モック投票)
        orchestrator = ReusableConsensusOrchestrator(
            agents=[melchior],
            voting_strategy="majority"
        )

        decision: FinalDecision = await orchestrator.reach_consensus(
            input_context={
                "ticker": request.ticker,
                "analysis_result": analysis_result
            }
        )

        # 5. レスポンスを構築
        response = AnalyzeResponse(
            ticker=request.ticker,
            final_action=decision.final_action,
            confidence=decision.weighted_confidence,
            summary=decision.summary,
            reasoning=[
                {
                    "agent": vote.agent_name,
                    "action": vote.action.value,
                    "confidence": vote.confidence,
                    "reasoning": vote.reasoning
                }
                for vote in decision.votes
            ] if request.include_reasoning else None,
            has_conflict=decision.has_conflict
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析中にエラーが発生しました: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    Returns:
        {"status": "ok"}
    """
    return {"status": "ok"}


__all__ = ["router", "AnalyzeRequest", "AnalyzeResponse"]
