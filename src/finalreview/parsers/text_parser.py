from __future__ import annotations

from pathlib import Path

from finalreview.models import DocumentChunk
from finalreview.parsers.base import BaseParser
from finalreview.utils.text_utils import normalize_text


class TextParser(BaseParser):
    file_types = {".txt", ".md"}

    def parse(self, file_path: Path) -> list[DocumentChunk]:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        blocks = [b for b in normalize_text(text).split("\n\n") if b.strip()]
        if not blocks:
            blocks = [normalize_text(text)]
        return [
            self.make_chunk(file_path, block, idx, paragraph_index=idx + 1)
            for idx, block in enumerate(blocks)
            if block.strip()
        ]
