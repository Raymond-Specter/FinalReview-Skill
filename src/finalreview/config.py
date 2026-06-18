from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class AppConfig:
    llm_backend: str = "none"
    openai_model: str = "gpt-4.1-mini"
    ollama_model: str = "qwen2.5:7b"
    chunk_size: int = 900
    chunk_overlap: int = 120
    top_k: int = 5


def load_config(config_path: Path | None = None) -> AppConfig:
    data = {}
    if config_path and config_path.exists():
        data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    config = AppConfig(**data)
    config.llm_backend = os.getenv("FINALREVIEW_LLM_BACKEND", config.llm_backend)
    config.openai_model = os.getenv("OPENAI_MODEL", config.openai_model)
    config.ollama_model = os.getenv("OLLAMA_MODEL", config.ollama_model)
    return config
