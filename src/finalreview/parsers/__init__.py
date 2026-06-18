from __future__ import annotations

from pathlib import Path

from finalreview.parsers.base import BaseParser, UnsupportedParser
from finalreview.parsers.docx_parser import DOCXParser
from finalreview.parsers.image_parser import ImageParser
from finalreview.parsers.pdf_parser import PDFParser
from finalreview.parsers.pptx_parser import PPTXParser
from finalreview.parsers.table_parser import TableParser
from finalreview.parsers.text_parser import TextParser


PARSERS: list[BaseParser] = [
    PDFParser(),
    PPTXParser(),
    DOCXParser(),
    TextParser(),
    TableParser(),
    ImageParser(),
]


def get_parser(file_path: Path) -> BaseParser:
    suffix = file_path.suffix.lower()
    for parser in PARSERS:
        if suffix in parser.file_types:
            return parser
    return UnsupportedParser()
