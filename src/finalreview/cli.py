from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from finalreview import __version__
from finalreview.config import load_config
from finalreview.extraction.exam_points import extract_exam_points
from finalreview.extraction.exercises import extract_exercises
from finalreview.extraction.formulas import extract_formulas
from finalreview.generation.markdown_writer import write_all_outputs
from finalreview.generation.mock_exam import generate_mock_exam
from finalreview.generation.study_plan import generate_study_plan
from finalreview.llm.base import LLMClient
from finalreview.llm.ollama_client import OllamaClient
from finalreview.llm.openai_client import OpenAIClient
from finalreview.models import ExerciseItem
from finalreview.parsers import get_parser
from finalreview.processing.chunker import split_chunks
from finalreview.processing.source_tracker import read_chunks_jsonl, write_chunks_jsonl, write_source_index
from finalreview.rag.qa import answer_question
from finalreview.rag.vector_store import TfidfVectorStore
from finalreview.utils.file_utils import ensure_dir, iter_supported_files
from finalreview.utils.logging_utils import setup_logging

app = typer.Typer(help="FinalReview-Skill: local-first final exam review generator.")
console = Console()


@app.command()
def run(
    input: Path = typer.Option(..., "--input", "-i", help="课程资料文件夹或单个文件"),
    output: Path = typer.Option(..., "--output", "-o", help="输出目录"),
    course_name: str = typer.Option("未命名课程", "--course-name", help="课程名称"),
    config: Optional[Path] = typer.Option(None, "--config", help="配置文件"),
    verbose: bool = typer.Option(False, "--verbose", help="显示详细日志"),
) -> None:
    """Parse materials and generate all review outputs."""
    setup_logging(verbose)
    cfg = load_config(config)
    files, chunks = parse_materials(input, output, cfg.chunk_size, cfg.chunk_overlap)
    points = extract_exam_points(chunks)
    formulas = extract_formulas(chunks)
    exercises = extract_exercises(chunks)
    write_all_outputs(
        output,
        course_name=course_name,
        files=files,
        chunks=chunks,
        points=points,
        formulas=formulas,
        exercises=exercises,
    )
    build_vector_index(chunks, output)
    console.print(f"[green]完成：已生成复习资料到 {output}[/green]")


@app.command("parse")
def parse_cmd(
    input: Path = typer.Option(..., "--input", "-i"),
    output: Path = typer.Option(..., "--output", "-o"),
    config: Optional[Path] = typer.Option(None, "--config"),
) -> None:
    """Only parse source materials and build local search index."""
    cfg = load_config(config)
    _, chunks = parse_materials(input, output, cfg.chunk_size, cfg.chunk_overlap)
    build_vector_index(chunks, output)
    console.print(f"[green]解析完成：{len(chunks)} 个 chunks[/green]")


@app.command("generate-exam")
def generate_exam_cmd(
    output: Path = typer.Option(..., "--output", "-o"),
    difficulty: str = typer.Option("medium", "--difficulty"),
    duration: int = typer.Option(120, "--duration"),
) -> None:
    data = load_extracted_data(output)
    exercises = [ExerciseItem.model_validate(item) for item in data.get("exercises", [])]
    points = []
    from finalreview.models import ExamPoint

    points = [ExamPoint.model_validate(item) for item in data.get("points", [])]
    mock = generate_mock_exam(exercises, points, difficulty=difficulty, duration=duration)
    from finalreview.generation.markdown_writer import render_mock_exam

    (output / "05_模拟卷A.md").write_text(render_mock_exam(mock, answers=False), encoding="utf-8")
    (output / "06_模拟卷A_答案解析.md").write_text(render_mock_exam(mock, answers=True), encoding="utf-8")
    console.print("[green]模拟卷已更新[/green]")


@app.command("plan")
def plan_cmd(
    output: Path = typer.Option(..., "--output", "-o"),
    exam_date: Optional[str] = typer.Option(None, "--exam-date"),
    days: int = typer.Option(7, "--days"),
) -> None:
    data = load_extracted_data(output)
    from finalreview.models import ExamPoint, FormulaItem

    points = [ExamPoint.model_validate(item) for item in data.get("points", [])]
    formulas = [FormulaItem.model_validate(item) for item in data.get("formulas", [])]
    exercises = [ExerciseItem.model_validate(item) for item in data.get("exercises", [])]
    parsed_date = date.fromisoformat(exam_date) if exam_date else None
    text = generate_study_plan(points, formulas, exercises, days=days, exam_date=parsed_date)
    (output / "10_复习计划.md").write_text(text, encoding="utf-8")
    console.print("[green]复习计划已更新[/green]")


@app.command("ask")
def ask_cmd(
    output: Path = typer.Option(..., "--output", "-o"),
    question: str = typer.Option(..., "--question", "-q"),
    backend: str = typer.Option("none", "--backend", help="none/openai/ollama"),
) -> None:
    llm = make_llm(backend)
    console.print(answer_question(output, question, llm=llm))


@app.command("version")
def version_cmd() -> None:
    console.print(__version__)


def parse_materials(input_path: Path, output_dir: Path, chunk_size: int, chunk_overlap: int):
    ensure_dir(output_dir)
    files = iter_supported_files(input_path)
    raw_chunks = []
    for file_path in files:
        parser = get_parser(file_path)
        raw_chunks.extend(parser.parse(file_path))
    chunks = split_chunks(raw_chunks, size=chunk_size, overlap=chunk_overlap)
    write_chunks_jsonl(chunks, output_dir / "chunks.jsonl")
    write_source_index(chunks, output_dir / "source_index.json")
    return files, chunks


def build_vector_index(chunks, output_dir: Path) -> None:
    store = TfidfVectorStore()
    store.build(chunks)
    store.save(output_dir / "vector_index")


def load_extracted_data(output_dir: Path) -> dict:
    path = output_dir / "extracted_data.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    chunks = read_chunks_jsonl(output_dir / "chunks.jsonl")
    points = extract_exam_points(chunks)
    formulas = extract_formulas(chunks)
    exercises = extract_exercises(chunks)
    return {
        "points": [p.model_dump(mode="json") for p in points],
        "formulas": [f.model_dump(mode="json") for f in formulas],
        "exercises": [e.model_dump(mode="json") for e in exercises],
    }


def make_llm(backend: str) -> LLMClient | None:
    if backend == "openai":
        return OpenAIClient()
    if backend == "ollama":
        return OllamaClient()
    return None
