from __future__ import annotations

from pathlib import Path

from finalreview.models import DocumentChunk
from finalreview.parsers.base import BaseParser
from finalreview.utils.text_utils import normalize_text


class ImageParser(BaseParser):
    file_types = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    def parse(self, file_path: Path) -> list[DocumentChunk]:
        try:
            import pytesseract
            from PIL import Image
        except Exception as exc:
            return [
                self.make_chunk(
                    file_path,
                    f"图片 OCR 未启用：请安装 pytesseract、Pillow 和系统 Tesseract。原因：{exc}",
                    0,
                    metadata={"ocr_available": False, "ocr_needed": True},
                )
            ]
        try:
            text = normalize_text(pytesseract.image_to_string(Image.open(file_path), lang="chi_sim+eng"))
            if not text:
                text = "图片 OCR 未识别到文本。"
            return [self.make_chunk(file_path, text, 0, metadata={"ocr_available": True})]
        except Exception as exc:
            return [
                self.make_chunk(
                    file_path,
                    f"图片 OCR 失败：{exc}",
                    0,
                    metadata={"parse_error": str(exc), "ocr_needed": True},
                )
            ]
