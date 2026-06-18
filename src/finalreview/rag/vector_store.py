from __future__ import annotations

import math
import pickle
import re
from collections import Counter
from pathlib import Path

from finalreview.models import DocumentChunk


class TfidfVectorStore:
    def __init__(self) -> None:
        self.backend = "simple"
        self.vectorizer = None
        self.matrix = None
        self.chunks: list[DocumentChunk] = []
        self.simple_vectors: list[Counter[str]] = []

    def build(self, chunks: list[DocumentChunk]) -> None:
        self.chunks = [chunk for chunk in chunks if chunk.text.strip()]
        texts = [chunk.text for chunk in self.chunks] or [""]
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            self.backend = "sklearn"
            self.vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
            self.matrix = self.vectorizer.fit_transform(texts)
        except Exception:
            self.backend = "simple"
            self.simple_vectors = [Counter(tokenize(text)) for text in texts]

    def search(self, question: str, top_k: int = 5) -> list[tuple[DocumentChunk, float]]:
        if not self.chunks:
            return []
        if self.backend == "sklearn" and self.vectorizer is not None and self.matrix is not None:
            from sklearn.metrics.pairwise import cosine_similarity

            query = self.vectorizer.transform([question])
            scores = cosine_similarity(query, self.matrix).ravel()
            ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top_k]
            return [(self.chunks[idx], float(score)) for idx, score in ranked if score > 0]
        query_vec = Counter(tokenize(question))
        scores = [cosine(query_vec, vec) for vec in self.simple_vectors]
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top_k]
        return [(self.chunks[idx], float(score)) for idx, score in ranked if score > 0]

    def save(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        with (path / "tfidf.pkl").open("wb") as f:
            pickle.dump(
                {
                    "backend": self.backend,
                    "vectorizer": self.vectorizer,
                    "matrix": self.matrix,
                    "chunks": self.chunks,
                    "simple_vectors": self.simple_vectors,
                },
                f,
            )

    @classmethod
    def load(cls, path: Path) -> "TfidfVectorStore":
        store = cls()
        with (path / "tfidf.pkl").open("rb") as f:
            data = pickle.load(f)
        store.backend = data.get("backend", "simple")
        store.vectorizer = data.get("vectorizer")
        store.matrix = data.get("matrix")
        store.chunks = data.get("chunks", [])
        store.simple_vectors = data.get("simple_vectors", [])
        return store


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]", text.lower())
    return words


def cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[key] * b.get(key, 0) for key in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
