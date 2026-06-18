from __future__ import annotations

import os

from finalreview.llm.base import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.model = model

    def generate(self, prompt: str) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY 未设置。")
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(model=self.model, input=prompt)
        return response.output_text
