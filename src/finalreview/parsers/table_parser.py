from __future__ import annotations

from pathlib import Path

from finalreview.models import DocumentChunk
from finalreview.parsers.base import BaseParser


class TableParser(BaseParser):
    file_types = {".csv", ".xlsx", ".xls"}

    def parse(self, file_path: Path) -> list[DocumentChunk]:
        try:
            import pandas as pd
        except Exception as exc:
            return [
                self.make_chunk(
                    file_path,
                    f"表格解析依赖 pandas 不可用：{exc}",
                    0,
                    metadata={"parse_error": "missing_pandas"},
                )
            ]
        try:
            if file_path.suffix.lower() == ".csv":
                frames = {"Sheet1": pd.read_csv(file_path)}
            else:
                frames = pd.read_excel(file_path, sheet_name=None)
            chunks: list[DocumentChunk] = []
            for idx, (sheet, df) in enumerate(frames.items(), start=1):
                text = df.fillna("").to_markdown(index=False)
                chunks.append(
                    self.make_chunk(file_path, f"工作表：{sheet}\n\n{text}", idx, metadata={"sheet": sheet})
                )
            return chunks
        except Exception as exc:
            return [
                self.make_chunk(
                    file_path,
                    f"表格解析失败：{exc}",
                    0,
                    metadata={"parse_error": str(exc)},
                )
            ]
