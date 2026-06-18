from __future__ import annotations

import json
from pathlib import Path

from finalreview.models import DocumentChunk, SourceRef


def format_source(ref: SourceRef) -> str:
    return ref.label()


def write_chunks_jsonl(chunks: list[DocumentChunk], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.model_dump(mode="json"), ensure_ascii=False) + "\n")


def read_chunks_jsonl(path: Path) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    if not path.exists():
        return chunks
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(DocumentChunk.model_validate_json(line))
    return chunks


def write_source_index(chunks: list[DocumentChunk], path: Path) -> None:
    files: dict[str, dict] = {}
    for chunk in chunks:
        entry = files.setdefault(
            chunk.file_name,
            {"file_path": chunk.file_path, "file_type": chunk.file_type, "chunks": 0, "warnings": []},
        )
        entry["chunks"] += 1
        if chunk.metadata.get("ocr_needed"):
            entry["warnings"].append("可能需要 OCR")
        if chunk.metadata.get("parse_error"):
            entry["warnings"].append(str(chunk.metadata["parse_error"]))
    path.write_text(json.dumps(files, ensure_ascii=False, indent=2), encoding="utf-8")
