from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, get_args, get_origin, get_type_hints


class CompatModel:
    def model_dump(self, mode: str = "python") -> dict[str, Any]:
        data = asdict(self)
        if mode == "json":
            return _jsonable(data)
        return data

    @classmethod
    def model_validate(cls, data):
        if isinstance(data, cls):
            return data
        return _build_dataclass(cls, data)

    @classmethod
    def model_validate_json(cls, text: str):
        return cls.model_validate(json.loads(text))

    def model_copy(self):
        return self.__class__.model_validate(self.model_dump(mode="json"))


def _jsonable(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def _build_dataclass(cls, data: dict):
    hints = get_type_hints(cls)
    kwargs = {}
    for key, typ in hints.items():
        if key not in data:
            continue
        kwargs[key] = _coerce(data[key], typ)
    return cls(**kwargs)


def _coerce(value, typ):
    origin = get_origin(typ)
    if origin is list:
        inner = get_args(typ)[0]
        return [_coerce(item, inner) for item in value]
    if origin is dict:
        return value
    if typ is Path:
        return Path(value)
    if typ is datetime and isinstance(value, str):
        return datetime.fromisoformat(value)
    if isinstance(typ, type) and issubclass(typ, CompatModel) and isinstance(value, dict):
        return typ.model_validate(value)
    return value


@dataclass
class SourceRef(CompatModel):
    file_name: str
    page_number: int | None = None
    slide_number: int | None = None
    paragraph_index: int | None = None
    text_snippet: str = ""

    def label(self) -> str:
        parts = [f"《{self.file_name}》"]
        if self.page_number is not None:
            parts.append(f"第{self.page_number}页")
        if self.slide_number is not None:
            parts.append(f"第{self.slide_number}页幻灯片")
        if self.paragraph_index is not None:
            parts.append(f"第{self.paragraph_index}段")
        return "".join(parts)


@dataclass
class DocumentChunk(CompatModel):
    id: str
    text: str
    source: SourceRef
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def file_name(self) -> str:
        return self.source.file_name

    @property
    def file_path(self) -> str:
        return str(self.metadata.get("file_path", ""))

    @property
    def file_type(self) -> str:
        return str(self.metadata.get("file_type", ""))

    @property
    def page_number(self) -> int | None:
        return self.source.page_number

    @property
    def slide_number(self) -> int | None:
        return self.source.slide_number

    @property
    def paragraph_index(self) -> int | None:
        return self.source.paragraph_index


@dataclass
class CourseProject(CompatModel):
    course_name: str
    input_dir: Path
    output_dir: Path
    created_at: datetime = field(default_factory=datetime.now)
    files: list[str] = field(default_factory=list)


ExamType = Literal["choice", "fill_blank", "calculation", "short_answer", "proof", "design", "unknown"]


@dataclass
class ExamPoint(CompatModel):
    id: str
    title: str
    chapter: str = "未识别章节"
    module: str = "综合"
    importance: Literal["high", "medium", "low"] = "medium"
    exam_type: ExamType = "unknown"
    explanation: str = ""
    possible_question_forms: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    source_refs: list[SourceRef] = field(default_factory=list)


@dataclass
class FormulaItem(CompatModel):
    id: str
    formula_text: str
    formula_latex: str = ""
    name: str = "未命名公式"
    meaning: str = ""
    variables: list[str] = field(default_factory=list)
    conditions: str = ""
    common_mistakes: list[str] = field(default_factory=list)
    related_exam_points: list[str] = field(default_factory=list)
    source_refs: list[SourceRef] = field(default_factory=list)


@dataclass
class ExerciseItem(CompatModel):
    id: str
    question_text: str
    answer_text: str = ""
    explanation: str = ""
    chapter: str = "未识别章节"
    module: str = "综合"
    question_type: ExamType = "unknown"
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    related_exam_points: list[str] = field(default_factory=list)
    source_refs: list[SourceRef] = field(default_factory=list)
    is_duplicate: bool = False
    duplicate_group_id: str | None = None
    duplicate_count: int = 1


@dataclass
class MockExam(CompatModel):
    title: str
    questions: list[ExerciseItem] = field(default_factory=list)
    answer_key: list[str] = field(default_factory=list)
    duration_minutes: int = 120
    difficulty: str = "medium"


@dataclass
class AnkiCard(CompatModel):
    front: str
    back: str
    tags: list[str] = field(default_factory=list)
    source_refs: list[SourceRef] = field(default_factory=list)
