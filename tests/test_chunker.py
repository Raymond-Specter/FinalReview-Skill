from finalreview.models import DocumentChunk, SourceRef
from finalreview.processing.chunker import split_chunks


def test_chunker_splits_with_overlap():
    chunk = DocumentChunk(id="c1", text="abcdef", source=SourceRef(file_name="a.txt"), metadata={})
    parts = split_chunks([chunk], size=4, overlap=1)
    assert [p.text for p in parts] == ["abcd", "def"]


def test_chunker_skips_empty():
    chunk = DocumentChunk(id="c1", text="   ", source=SourceRef(file_name="a.txt"), metadata={})
    assert split_chunks([chunk]) == []
