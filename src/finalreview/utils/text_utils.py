from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def short_snippet(text: str, length: int = 120) -> str:
    clean = normalize_text(text).replace("\n", " ")
    return clean[:length] + ("..." if len(clean) > length else "")


def stable_id(prefix: str, value: str, index: int = 0) -> str:
    import hashlib

    digest = hashlib.sha1(f"{value}:{index}".encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{digest}"
