from __future__ import annotations

from finalreview.llm.base import LLMClient


class RuleBasedClient(LLMClient):
    def generate(self, prompt: str) -> str:
        return prompt
