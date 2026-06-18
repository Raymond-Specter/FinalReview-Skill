from __future__ import annotations

from finalreview.utils.text_utils import normalize_text


def clean_text(text: str) -> str:
    return normalize_text(text)
