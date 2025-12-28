"""Stock MAGI system package"""

from .agents import MelchiorAgent, create_melchior_agent
from .prompts import (
    MELCHIOR_SYSTEM_MESSAGE,
    create_melchior_analysis_prompt,
)

__all__ = [
    "MelchiorAgent",
    "create_melchior_agent",
    "MELCHIOR_SYSTEM_MESSAGE",
    "create_melchior_analysis_prompt",
]
