from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from finalreview.models import DocumentChunk, SourceRef
from finalreview.utils.text_utils import short_snippet, stable_id


class BaseParser(ABC):
    file_types: set[str] = set()

    @abstractmethod
    def parse(self, file_path: Path) -> list[DocumentChunk]:
        raise NotImplementedError

    def make_chunk(
        self,
        file_path: Path,
        text: str,
        index: int,
        *,
        page_number: int | None = None,
        slide_number: int | None = None,
        paragraph_index: int | None = None,
        metadata: dict | None = None,
    ) -> DocumentChunk:
        meta = {
            "file_path": str(file_path),
            "file_type": file_path.suffix.lower().lstrip("."),
        }
        meta.update(metadata or {})
        source = SourceRef(
            file_name=file_path.name,
            page_number=page_number,
            slide_number=slide_number,
            paragraph_index=paragraph_index,
            text_snippet=short_snippet(text),
        )
        return DocumentChunk(
            id=stable_id("chunk", f"{file_path}:{index}:{text}", index),
            text=text.strip(),
            source=source,
            metadata=meta,
        )


class UnsupportedParser(BaseParser):
    def parse(self, file_path: Path) -> list[DocumentChunk]:
        return [
            self.make_chunk(
                file_path,
                f"暂不支持解析 {file_path.suffix} 文件，请转换为 PDF、DOCX、PPTX、TXT、MD、CSV 或 XLSX。",
                0,
                metadata={"parse_error": "unsupported_file_type"},
            )
        ]
