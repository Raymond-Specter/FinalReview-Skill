from __future__ import annotations

from collections import Counter
from pathlib import Path

from finalreview.models import DocumentChunk, ExerciseItem


def build_completeness_report(files: list[Path], chunks: list[DocumentChunk], exercises: list[ExerciseItem]) -> list[str]:
    suffixes = Counter(path.suffix.lower() for path in files)
    warnings: list[str] = []
    names = " ".join(path.name for path in files)
    if not any("往年" in path.name or "试卷" in path.name for path in files):
        warnings.append("未发现明显的往年卷或试卷文件，建议补充历年真题。")
    if not any("复习" in path.name or "范围" in path.name for path in files):
        warnings.append("未发现明显的复习范围文件，建议补充老师给出的考试范围。")
    if suffixes.get(".pptx", 0) and not exercises:
        warnings.append("检测到课件但未提取到练习题，建议补充作业或题库。")
    if exercises and not any(ex.answer_text for ex in exercises):
        warnings.append("题库中多数题目缺少答案，建议补充答案或解析材料。")
    ocr_needed = [c for c in chunks if c.metadata.get("ocr_needed")]
    if ocr_needed:
        warnings.append(f"有 {len(ocr_needed)} 个片段可能需要 OCR，请检查扫描 PDF 或图片。")
    parse_errors = [c for c in chunks if c.metadata.get("parse_error")]
    if parse_errors:
        warnings.append(f"有 {len(parse_errors)} 个片段存在解析警告，请查看 source_index.json。")
    if "第1章" in names and "第3章" in names and "第2章" not in names:
        warnings.append("文件名显示可能缺少第2章资料。")
    return warnings or ["资料结构基本完整。仍建议人工核对章节、题目和答案是否齐全。"]
