from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from finalreview.extraction.completeness import build_completeness_report
from finalreview.generation.anki_exporter import build_anki_cards, write_anki_csv
from finalreview.generation.knowledge_graph import generate_knowledge_graph
from finalreview.generation.mock_exam import generate_mock_exam
from finalreview.generation.study_plan import generate_study_plan
from finalreview.generation.wrong_book import generate_wrong_book_template
from finalreview.models import DocumentChunk, ExamPoint, ExerciseItem, FormulaItem, MockExam
from finalreview.processing.source_tracker import format_source


def write_all_outputs(
    output_dir: Path,
    *,
    course_name: str,
    files: list[Path],
    chunks: list[DocumentChunk],
    points: list[ExamPoint],
    formulas: list[FormulaItem],
    exercises: list[ExerciseItem],
    days: int = 7,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    mock = generate_mock_exam(exercises, points)
    (output_dir / "00_期末总复习指南.md").write_text(
        render_guide(course_name, files, points, formulas, exercises), encoding="utf-8"
    )
    (output_dir / "01_考点清单.md").write_text(render_points(points), encoding="utf-8")
    (output_dir / "02_公式表.md").write_text(render_formulas(formulas), encoding="utf-8")
    (output_dir / "03_练习题题库.md").write_text(render_exercises(exercises), encoding="utf-8")
    (output_dir / "04_高频题型.md").write_text(render_frequent_types(exercises, points), encoding="utf-8")
    (output_dir / "05_模拟卷A.md").write_text(render_mock_exam(mock, answers=False), encoding="utf-8")
    (output_dir / "06_模拟卷A_答案解析.md").write_text(render_mock_exam(mock, answers=True), encoding="utf-8")
    (output_dir / "07_错题本模板.md").write_text(generate_wrong_book_template(), encoding="utf-8")
    write_anki_csv(build_anki_cards(points, formulas), output_dir / "08_Anki卡片.csv")
    (output_dir / "09_知识图谱.md").write_text(generate_knowledge_graph(points, formulas, exercises), encoding="utf-8")
    (output_dir / "10_复习计划.md").write_text(
        generate_study_plan(points, formulas, exercises, days=days), encoding="utf-8"
    )
    (output_dir / "11_资料完整性检查.md").write_text(
        render_completeness(files, chunks, exercises), encoding="utf-8"
    )
    write_data_json(output_dir, points, formulas, exercises)


def write_data_json(output_dir: Path, points: list[ExamPoint], formulas: list[FormulaItem], exercises: list[ExerciseItem]) -> None:
    data = {
        "points": [p.model_dump(mode="json") for p in points],
        "formulas": [f.model_dump(mode="json") for f in formulas],
        "exercises": [e.model_dump(mode="json") for e in exercises],
    }
    (output_dir / "extracted_data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def render_guide(
    course_name: str,
    files: list[Path],
    points: list[ExamPoint],
    formulas: list[FormulaItem],
    exercises: list[ExerciseItem],
) -> str:
    high = [p for p in points if p.importance == "high"] or points[:10]
    return f"""# 期末总复习指南

课程：{course_name}

## 1. 课程资料概况

共解析 {len(files)} 个文件，提取 {len(points)} 个考点、{len(formulas)} 条公式、{len(exercises)} 道练习题。

## 2. 最高优先级考点

{bullet(p.title for p in high[:10])}

## 3. 必背公式

{bullet(f.formula_text for f in formulas[:10])}

## 4. 高频题型

{bullet(f"{k}：{v} 次" for k, v in Counter(e.question_type for e in exercises).most_common())}

## 5. 最容易错的地方

* 来源不足或 OCR 失败的材料需要回看原文。
* 公式的适用条件、变量含义和延迟符号需要重点复核。

## 6. 1天冲刺路线

先看高优先级考点，再背公式，最后做模拟卷。

## 7. 3天复习路线

第 1 天整理概念，第 2 天刷题，第 3 天复盘错题和公式。

## 8. 7天复习路线

按章节推进，每天完成考点、公式、练习题和错题复盘。

## 9. 建议先做的练习题

{bullet(e.question_text.splitlines()[0] for e in exercises[:10])}
"""


def render_points(points: list[ExamPoint]) -> str:
    lines = ["# 考点清单", ""]
    for point in points:
        lines.extend(
            [
                f"## {point.title}",
                "",
                f"* 章节：{point.chapter}",
                f"* 重要程度：{point.importance}",
                f"* 可能考法：{point.exam_type}；{'；'.join(point.possible_question_forms)}",
                f"* 一句话解释：{point.explanation}",
                f"* 前置知识：{'、'.join(point.prerequisites) if point.prerequisites else '待结合课程资料补充'}",
                f"* 来源：{join_sources(point.source_refs)}",
                "",
            ]
        )
    return "\n".join(lines)


def render_formulas(formulas: list[FormulaItem]) -> str:
    lines = ["# 公式表", ""]
    for item in formulas:
        lines.extend(
            [
                f"## {item.name}",
                "",
                f"公式：{item.formula_text}",
                "",
                f"含义：{item.meaning}",
                "",
                f"变量：{'、'.join(item.variables) if item.variables else '待补充'}",
                "",
                f"适用条件：{item.conditions}",
                "",
                f"常见错误：{'；'.join(item.common_mistakes)}",
                "",
                f"来源：{join_sources(item.source_refs)}",
                "",
            ]
        )
    return "\n".join(lines)


def render_exercises(exercises: list[ExerciseItem]) -> str:
    grouped: dict[str, list[ExerciseItem]] = defaultdict(list)
    for exercise in exercises:
        grouped[exercise.module].append(exercise)
    lines = ["# 练习题题库", ""]
    for module, items in grouped.items():
        lines.extend([f"## 模块：{module}", ""])
        for idx, item in enumerate(items, start=1):
            duplicate = f"；重复组：{item.duplicate_group_id}，出现 {item.duplicate_count} 次" if item.is_duplicate else ""
            lines.extend(
                [
                    f"### 题目 {idx}",
                    "",
                    f"题型：{item.question_type}",
                    f"难度：{item.difficulty}",
                    f"涉及考点：{'、'.join(item.related_exam_points) if item.related_exam_points else '待关联'}",
                    f"来源：{join_sources(item.source_refs)}{duplicate}",
                    "",
                    "题目：",
                    "",
                    item.question_text,
                    "",
                    f"答案：{item.answer_text or '资料中未提取到答案'}",
                    "",
                    f"解析：{item.explanation or '资料中未提取到解析'}",
                    "",
                    "---",
                    "",
                ]
            )
    return "\n".join(lines)


def render_frequent_types(exercises: list[ExerciseItem], points: list[ExamPoint]) -> str:
    counts = Counter(e.question_type for e in exercises)
    lines = ["# 高频题型", ""]
    for qtype, count in counts.most_common():
        related = [p.title for p in points if p.exam_type == qtype][:5]
        lines.extend(
            [
                f"## {qtype}",
                "",
                f"* 出现次数：{count}",
                f"* 关联考点：{'、'.join(related) if related else '待关联'}",
                "* 常见问法：解释概念、计算关键量、说明步骤或设计方法。",
                "* 典型题：见练习题题库同题型条目。",
                "* 变式题：改变参数、条件或问法后重新求解。",
                "* 复习建议：先复盘来源材料，再做题并记录错因。",
                "",
            ]
        )
    return "\n".join(lines)


def render_mock_exam(mock: MockExam, *, answers: bool) -> str:
    lines = [f"# {mock.title}{'_答案解析' if answers else ''}", "", f"考试时长：{mock.duration_minutes} 分钟", ""]
    for idx, question in enumerate(mock.questions, start=1):
        lines.extend([f"## 第 {idx} 题（{question.question_type}）", "", question.question_text, ""])
        if answers:
            lines.extend([f"答案：{question.answer_text or '请参考原始资料整理答案。'}", "", f"解析：{question.explanation or '暂无解析。'}", ""])
    return "\n".join(lines)


def render_completeness(files: list[Path], chunks: list[DocumentChunk], exercises: list[ExerciseItem]) -> str:
    lines = ["# 资料完整性检查", ""]
    for item in build_completeness_report(files, chunks, exercises):
        lines.append(f"* {item}")
    return "\n".join(lines) + "\n"


def bullet(items) -> str:
    values = [str(item) for item in items if str(item).strip()]
    return "\n".join(f"* {item}" for item in values) if values else "* 暂无可用条目"


def join_sources(refs) -> str:
    return "；".join(format_source(ref) for ref in refs) if refs else "无来源"
