from __future__ import annotations

EMPHASIS_KEYWORDS = ["重点", "难点", "考试", "必考", "可能考", "这个要会", "大家注意", "容易错", "掌握", "熟悉"]


def has_teacher_emphasis(text: str) -> bool:
    return any(keyword in text for keyword in EMPHASIS_KEYWORDS)
