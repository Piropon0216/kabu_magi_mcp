"""Prompts package for stock MAGI agents"""

from .stock_analysis_prompts import (
    BALTHASAR_SYSTEM_MESSAGE,
    CASPER_SYSTEM_MESSAGE,
    MELCHIOR_SYSTEM_MESSAGE,
    create_melchior_analysis_prompt,
)

__all__ = [
    "MELCHIOR_SYSTEM_MESSAGE",
    "create_melchior_analysis_prompt",
    "BALTHASAR_SYSTEM_MESSAGE",
    "CASPER_SYSTEM_MESSAGE",
]
