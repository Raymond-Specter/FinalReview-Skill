# 架构说明

FinalReview-Skill 的核心流水线是：

1. `parsers` 将不同格式资料统一解析成 `DocumentChunk`。
2. `processing` 清洗、切分文本并写入 `chunks.jsonl`、`source_index.json`。
3. `extraction` 用规则方法提取考点、公式、练习题和完整性信号。
4. `generation` 写出 Markdown、CSV、Mermaid 和模拟卷。
5. `rag` 使用 TF-IDF 建立本地索引并完成带来源的问答。
6. `llm` 提供 OpenAI/Ollama/none 三种后端的扩展接口。

所有核心对象都定义在 `models.py`，并保留来源引用，便于生成内容后回到原始资料核查。
