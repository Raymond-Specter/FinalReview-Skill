from __future__ import annotations

import json
import urllib.request

from finalreview.llm.base import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, model: str = "qwen2.5:7b", host: str = "http://localhost:11434") -> None:
        self.model = model
        self.host = host.rstrip("/")

    def generate(self, prompt: str) -> str:
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("response", "")
