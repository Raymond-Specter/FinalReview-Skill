from __future__ import annotations

from datetime import date

from finalreview.models import ExamPoint, ExerciseItem, FormulaItem


def generate_study_plan(
    points: list[ExamPoint],
    formulas: list[FormulaItem],
    exercises: list[ExerciseItem],
    *,
    days: int = 7,
    exam_date: date | None = None,
) -> str:
    high = [p for p in points if p.importance == "high"] or points
    days = max(days, 1)
    lines = ["# 复习计划", ""]
    if exam_date:
        lines.append(f"考试日期：{exam_date.isoformat()}")
        lines.append("")
    lines.append(f"计划天数：{days} 天")
    lines.append("")
    for day in range(1, days + 1):
        focus = high[(day - 1) :: days][:4]
        lines.append(f"## Day {day}")
        lines.append("")
        lines.append("* 复习考点：" + "、".join(p.title for p in focus) if focus else "* 复习考点：整理课程目录")
        lines.append(f"* 公式复盘：{min(len(formulas), max(1, len(formulas) // days or 1))} 个")
        lines.append(f"* 练习任务：{min(len(exercises), max(2, len(exercises) // days or 2))} 题")
        lines.append("* 收尾动作：把不会的题加入错题本，并回看来源材料。")
        lines.append("")
    return "\n".join(lines)
