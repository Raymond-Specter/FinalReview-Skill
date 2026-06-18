from __future__ import annotations

from finalreview.models import DocumentChunk
from finalreview.utils.text_utils import short_snippet, stable_id


def split_chunks(chunks: list[DocumentChunk], size: int = 900, overlap: int = 120) -> list[DocumentChunk]:
    if size <= 0:
        raise ValueError("size must be positive")
    overlap = max(0, min(overlap, size - 1))
    result: list[DocumentChunk] = []
    for chunk in chunks:
        text = chunk.text.strip()
        if not text:
            continue
        if len(text) <= size:
            result.append(chunk)
            continue
        start = 0
        part = 0
        while start < len(text):
            piece = text[start : start + size].strip()
            if piece:
                new_source = chunk.source.model_copy()
                new_source.text_snippet = short_snippet(piece)
                metadata = dict(chunk.metadata)
                metadata["parent_chunk_id"] = chunk.id
                metadata["chunk_part"] = part
                result.append(
                    DocumentChunk(
                        id=stable_id("chunk", f"{chunk.id}:{part}:{piece}", part),
                        text=piece,
                        source=new_source,
                        metadata=metadata,
                    )
                )
            part += 1
            start += size - overlap
    return result
