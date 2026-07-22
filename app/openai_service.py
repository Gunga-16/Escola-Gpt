from __future__ import annotations

import os
from collections.abc import Iterable

from openai import OpenAI, OpenAIError

from app.config import SETTINGS
from app.prompts import SYSTEM_PROMPT


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "A variável OPENAI_API_KEY não foi configurada. "
            "Crie um arquivo .env a partir do .env.example."
        )
    return OpenAI(api_key=api_key)


def build_input(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    recent = messages[-SETTINGS.max_history_messages :]
    return [
        {"role": item["role"], "content": item["content"]}
        for item in recent
        if item.get("role") in {"user", "assistant"} and item.get("content")
    ]


def stream_answer(messages: list[dict[str, str]]) -> Iterable[str]:
    client = _client()
    try:
        with client.responses.stream(
            model=SETTINGS.model,
            instructions=SYSTEM_PROMPT,
            input=build_input(messages),
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
    except OpenAIError as exc:
        raise RuntimeError(f"Falha ao consultar a OpenAI: {exc}") from exc
