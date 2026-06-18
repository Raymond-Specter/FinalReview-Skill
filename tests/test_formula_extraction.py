from finalreview.extraction.formulas import extract_formulas
from finalreview.models import DocumentChunk, SourceRef


def test_formula_extraction_keeps_source():
    chunks = [
        DocumentChunk(
            id="c1",
            text="公式：D(z)=Φ(z)/(G(z)(1-Φ(z)))",
            source=SourceRef(file_name="控制.pdf", page_number=3),
        )
    ]
    formulas = extract_formulas(chunks)
    assert formulas
    assert formulas[0].source_refs[0].file_name == "控制.pdf"
