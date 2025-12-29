"""
Stock MAGI System - FastAPI Application

Microsoft Agent Framework + Foundry を使用した株式分析 API
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.stock_magi.api import router

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan イベント
    
    起動時: ロギング、初期化処理
    終了時: クリーンアップ処理
    """
    logger.info("🚀 Stock MAGI System starting...")
    logger.info("📊 Phase 1 MVP - Melchior agent + Morningstar tool")

    # Phase 2 で追加予定: Agent Framework 初期化
    # - DevUI 起動 (visual debugging)
    # - Foundry 接続確認

    yield

    logger.info("🛑 Stock MAGI System shutting down...")


# FastAPI アプリケーション
app = FastAPI(
    title="Stock MAGI System",
    description="エヴァンゲリオン MAGI システム inspired 株式分析 API (Agent Framework + Foundry)",
    version="0.1.0 (Phase 1 MVP)",
    lifespan=lifespan
)


# CORS 設定 (開発環境用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーター登録
app.include_router(router)


# ルートエンドポイント
@app.get("/")
async def root():
    """
    ルートエンドポイント
    
    Returns:
        API 情報
    """
    return {
        "name": "Stock MAGI System",
        "version": "0.1.0 (Phase 1 MVP)",
        "description": "MAGI システム inspired 株式分析 API",
        "endpoints": {
            "analyze": "POST /api/analyze",
            "health": "GET /api/health",
            "docs": "GET /docs"
        },
        "phase": "Phase 1 - Melchior agent + Morningstar tool (Foundry Tool Catalog)",
        "next_phase": "Phase 2 - Balthasar, Casper agents + Yahoo Finance"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開発環境のみ
        log_level="info"
    )
