from __future__ import annotations

from finalreview.models import DocumentChunk
from finalreview.rag.vector_store import TfidfVectorStore


def retrieve(store: TfidfVectorStore, question: str, top_k: int = 5) -> list[tuple[DocumentChunk, float]]:
    return store.search(question, top_k=top_k)
