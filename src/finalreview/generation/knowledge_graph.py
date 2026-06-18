from __future__ import annotations

import re

from finalreview.models import ExamPoint, ExerciseItem, FormulaItem


def generate_knowledge_graph(points: list[ExamPoint], formulas: list[FormulaItem], exercises: list[ExerciseItem]) -> str:
    lines = ["# 知识图谱", "", "```mermaid", "graph TD"]
    if not points:
        lines.append('  A["课程资料"] --> B["待提取考点"]')
    for idx, point in enumerate(points[:30], start=1):
        point_id = f"P{idx}"
        lines.append(f'  C["{escape(point.chapter)}"] --> {point_id}["{escape(point.title)}"]')
    for idx, formula in enumerate(formulas[:20], start=1):
        target = f"P{((idx - 1) % max(1, min(len(points), 30))) + 1}" if points else 'B'
        lines.append(f'  F{idx}["{escape(formula.name)}"] --> {target}')
    for idx, exercise in enumerate(exercises[:20], start=1):
        target = f"P{((idx - 1) % max(1, min(len(points), 30))) + 1}" if points else 'B'
        lines.append(f'  E{idx}["{escape(exercise.question_type)}题"] --> {target}')
    lines.extend(["```", ""])
    return "\n".join(lines)


def escape(text: str) -> str:
    return re.sub(r'["\n\r]', " ", text)[:60]
