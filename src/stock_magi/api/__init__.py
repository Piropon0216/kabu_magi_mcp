"""Stock MAGI API package"""

from .endpoints import AnalyzeRequest, AnalyzeResponse, router

__all__ = ["router", "AnalyzeRequest", "AnalyzeResponse"]
