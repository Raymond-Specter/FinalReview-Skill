from __future__ import annotations

import re

from finalreview.models import DocumentChunk, ExerciseItem
from finalreview.processing.deduplicator import mark_duplicates
from finalreview.utils.text_utils import short_snippet, stable_id

EXERCISE_START_RE = re.compile(
    r"^\s*((?:例题|练习|习题|作业|题目|问题)?\s*(?:\d+[.、）)]|（\d+）|Q\d+|Question\s+\d+|Exercice\s+\d+)|(?:选择|计算|证明|设计|简答|填空)题?)",
    re.IGNORECASE,
)


def extract_exercises(chunks: list[DocumentChunk]) -> list[ExerciseItem]:
    exercises: list[ExerciseItem] = []
    for chunk in chunks:
        blocks = split_question_blocks(chunk.text)
        for block in blocks:
            exercises.append(
                ExerciseItem(
                    id=stable_id("ex", block, len(exercises)),
                    question_text=block,
                    answer_text=extract_answer(block),
                    explanation=extract_explanation(block),
                    chapter=infer_chapter(chunk.file_name),
                    module=infer_module(block),
                    question_type=infer_question_type(block),
                    difficulty=infer_difficulty(block),
                    related_exam_points=[],
                    source_refs=[chunk.source],
                )
            )
    return mark_duplicates(exercises)


def split_question_blocks(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    blocks: list[str] = []
    current: list[str] = []
    for line in lines:
        is_start = bool(EXERCISE_START_RE.search(line)) or any(word in line for word in ["例题", "练习", "习题", "作业"])
        if is_start and current:
            blocks.append("\n".join(current))
            current = [line]
        elif is_start or current:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return [b for b in blocks if len(b) >= 6]


def extract_answer(text: str) -> str:
    match = re.search(r"(?:答案|参考答案)[:：]\s*(.+)", text)
    return match.group(1).strip() if match else ""


def extract_explanation(text: str) -> str:
    match = re.search(r"(?:解析|解答|说明)[:：]\s*(.+)", text)
    return match.group(1).strip() if match else ""


def infer_question_type(text: str) -> str:
    if re.search(r"[A-D][.、]", text) or "选择" in text:
        return "choice"
    if "填空" in text or "____" in text:
        return "fill_blank"
    if "计算" in text or "=" in text:
        return "calculation"
    if "证明" in text:
        return "proof"
    if "设计" in text:
        return "design"
    return "short_answer"


def infer_difficulty(text: str) -> str:
    if any(word in text for word in ["综合", "证明", "设计", "推导"]):
        return "hard"
    if len(text) < 60:
        return "easy"
    return "medium"


def infer_module(text: str) -> str:
    if "Z" in text or "z" in text or "变换" in text:
        return "Z变换"
    if "控制" in text or "G(z)" in text or "D(z)" in text:
        return "控制系统"
    return "综合"


def infer_chapter(file_name: str) -> str:
    match = re.search(r"第[一二三四五六七八九十0-9]+章", file_name)
    return match.group(0) if match else "未识别章节"
