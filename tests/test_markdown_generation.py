from pathlib import Path

from finalreview.generation.markdown_writer import write_all_outputs
from finalreview.models import DocumentChunk, ExamPoint, FormulaItem, SourceRef


def test_markdown_generation(tmp_path: Path):
    ref = SourceRef(file_name="a.md", paragraph_index=1)
    chunk = DocumentChunk(id="c1", text="重点：Z变换", source=ref)
    point = ExamPoint(id="p1", title="Z变换", explanation="重点", source_refs=[ref])
    formula = FormulaItem(id="f1", formula_text="X(z)=Σx(k)z^-k", source_refs=[ref])
    write_all_outputs(
        tmp_path,
        course_name="测试课",
        files=[Path("a.md")],
        chunks=[chunk],
        points=[point],
        formulas=[formula],
        exercises=[],
    )
    assert (tmp_path / "00_期末总复习指南.md").exists()
    assert "# 考点清单" in (tmp_path / "01_考点清单.md").read_text(encoding="utf-8")
