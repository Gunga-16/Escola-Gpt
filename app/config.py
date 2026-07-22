from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "EscolaGPT"
    model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", "12"))


SETTINGS = Settings()
