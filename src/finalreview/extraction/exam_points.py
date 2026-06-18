from __future__ import annotations

import re
from collections import Counter

from finalreview.extraction.teacher_emphasis import has_teacher_emphasis
from finalreview.models import DocumentChunk, ExamPoint
from finalreview.utils.text_utils import short_snippet, stable_id

POINT_PATTERNS = [
    r"(?:重点|难点|掌握|熟悉|了解|必考|可能考|定义|性质|定理|步骤|公式)[:：]?\s*([^。\n]{2,60})",
    r"^#{1,4}\s*(.+)$",
    r"^(?:第[一二三四五六七八九十0-9]+章|[0-9]+[.、])\s*(.+)$",
]


def extract_exam_points(chunks: list[DocumentChunk], limit: int = 80) -> list[ExamPoint]:
    candidates: list[tuple[str, DocumentChunk, str]] = []
    for chunk in chunks:
        lines = [line.strip() for line in chunk.text.splitlines() if line.strip()]
        for line in lines:
            for pattern in POINT_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    title = re.sub(r"[:：。；;]+$", "", match.group(1).strip())
                    if 2 <= len(title) <= 80:
                        candidates.append((title, chunk, line))
        if has_teacher_emphasis(chunk.text):
            candidates.append((short_snippet(chunk.text, 40), chunk, chunk.text))

    counts = Counter(title for title, _, _ in candidates)
    seen: set[str] = set()
    points: list[ExamPoint] = []
    for index, (title, chunk, line) in enumerate(candidates):
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        importance = "high" if counts[title] > 1 or has_teacher_emphasis(line) else "medium"
        points.append(
            ExamPoint(
                id=stable_id("point", title, index),
                title=title,
                chapter=infer_chapter(chunk),
                module=infer_module(title),
                importance=importance,
                exam_type=infer_exam_type(line),
                explanation=short_snippet(line, 160),
                possible_question_forms=[f"解释/计算/应用：{title}"],
                prerequisites=[],
                source_refs=[chunk.source],
            )
        )
        if len(points) >= limit:
            break
    return points


def infer_chapter(chunk: DocumentChunk) -> str:
    match = re.search(r"第[一二三四五六七八九十0-9]+章[^_\-\s]*", chunk.file_name)
    return match.group(0) if match else "未识别章节"


def infer_module(text: str) -> str:
    if "Z" in text or "z" in text or "变换" in text:
        return "Z变换"
    if "控制" in text or "传递函数" in text:
        return "控制系统"
    if "公式" in text:
        return "公式"
    return "综合"


def infer_exam_type(text: str) -> str:
    if "计算" in text or "=" in text:
        return "calculation"
    if "证明" in text:
        return "proof"
    if "设计" in text:
        return "design"
    if "选择" in text:
        return "choice"
    return "unknown"
