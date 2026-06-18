from __future__ import annotations

from pathlib import Path

from finalreview.llm.base import LLMClient
from finalreview.processing.source_tracker import format_source
from finalreview.rag.retriever import retrieve
from finalreview.rag.vector_store import TfidfVectorStore


def answer_question(output_dir: Path, question: str, llm: LLMClient | None = None, top_k: int = 5) -> str:
    index_dir = output_dir / "vector_index"
    if not (index_dir / "tfidf.pkl").exists():
        return "当前资料中没有找到足够依据：vector_index 不存在，请先运行 run 或 parse。"
    store = TfidfVectorStore.load(index_dir)
    hits = retrieve(store, question, top_k=top_k)
    if not hits:
        return "当前资料中没有找到足够依据。"
    context = "\n\n".join(
        f"[{i}] {format_source(chunk.source)}：{chunk.text}" for i, (chunk, _) in enumerate(hits, start=1)
    )
    if llm is None:
        lines = ["当前为无 LLM 模式，返回最相关原文片段："]
        for i, (chunk, score) in enumerate(hits, start=1):
            lines.append(f"\n{i}. {format_source(chunk.source)} 相似度 {score:.3f}\n{chunk.text}")
        return "\n".join(lines)
    prompt = (
        "你是严谨的期末复习助手。只能根据给定资料回答，必须引用来源。"
        "如果资料不足，回答“当前资料中没有找到足够依据”。\n\n"
        f"问题：{question}\n\n资料：\n{context}\n\n请给出简洁答案。"
    )
    try:
        return llm.generate(prompt)
    except Exception as exc:
        return f"LLM 调用失败，改为返回原文依据。\n\n{context}\n\n错误：{exc}"
