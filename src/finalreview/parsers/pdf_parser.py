from __future__ import annotations

from pathlib import Path

from finalreview.models import DocumentChunk
from finalreview.parsers.base import BaseParser
from finalreview.utils.text_utils import normalize_text


class PDFParser(BaseParser):
    file_types = {".pdf"}

    def parse(self, file_path: Path) -> list[DocumentChunk]:
        try:
            import fitz
        except Exception as exc:
            return [
                self.make_chunk(
                    file_path,
                    f"PDF 解析依赖 PyMuPDF 不可用：{exc}",
                    0,
                    metadata={"parse_error": "missing_pymupdf"},
                )
            ]

        chunks: list[DocumentChunk] = []
        try:
            with fitz.open(file_path) as doc:
                for i, page in enumerate(doc, start=1):
                    text = normalize_text(page.get_text("text"))
                    metadata = {"ocr_needed": len(text) < 30}
                    if not text:
                        text = "该页未提取到足够文本，可能是扫描页，需要 OCR。"
                    chunks.append(
                        self.make_chunk(file_path, text, i, page_number=i, metadata=metadata)
                    )
        except Exception as exc:
            chunks.append(
                self.make_chunk(
                    file_path,
                    f"PDF 解析失败：{exc}",
                    0,
                    metadata={"parse_error": str(exc)},
                )
            )
        return chunks
