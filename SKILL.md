---
name: finalreview-skill
description: Exam-focused course material review workflow for Codex, Claude Code, and similar coding agents. Use when the user provides or references university course materials such as PDFs, slides, Word documents, Markdown/TXT notes, spreadsheets, screenshots, OCR text, assignments, quizzes, past papers, syllabi, or lecture transcripts and asks for final exam review outputs including exam-point lists, formula sheets, practice questions, high-frequency question types, mock exams, answers, Anki cards, knowledge graphs, study plans, wrong-question templates, source-cited QA, or material completeness checks.
---

# FinalReview Skill

## Goal

Turn messy course materials into exam-oriented review artifacts. Prioritize scoring value, source traceability, and practical study use over polished prose.

Default to a local, evidence-first workflow. Do not invent facts, formulas, answers, exam scope, or source citations. When evidence is weak, say so and point to the closest source material.

## Core Workflow

1. Inventory the materials.
   - List files by type and likely role: slides, textbook notes, assignments, past papers, review scope, lecture transcript, handwritten/scan/image, spreadsheet/data.
   - Prefer course-provided materials over generic knowledge.
   - Identify missing high-value files: past papers, answer keys, review scope, homework solutions, teacher emphasis, formula sheets.

2. Extract text with source locations.
   - Use existing document/PDF/spreadsheet/presentation skills or available tools for file conversion and extraction.
   - Preserve source metadata for every extracted chunk: file name, page number, slide number, paragraph/section, sheet name, or image name.
   - For scanned PDFs/images, run OCR when available. If OCR is unavailable or low confidence, flag the file instead of pretending it was read.

3. Clean and chunk.
   - Normalize obvious encoding/spacing issues.
   - Split by chapter, slide, page, heading, question block, or transcript paragraph.
   - Keep enough surrounding text to support citations and later QA.

4. Rank exam relevance.
   - Strong signals: review scope, past papers, homework, quizzes, repeated exercise patterns, teacher phrases such as `重点`, `必考`, `考试`, `这个要会`, `大家注意`, `容易错`.
   - Medium signals: section headings, definitions, theorem/property/formula/steps language, repeated terms across slides and exercises.
   - Low signals: isolated textbook exposition without exercise or teacher emphasis.

5. Produce requested artifacts.
   - If the user asked for a subset, generate only that subset.
   - If the user asked broadly for final review materials, generate the standard artifact set in `references/output-spec.md`.
   - Always include source references where source-backed claims appear.

6. Validate before final delivery.
   - Check that outputs mention uncertain areas and missing materials.
   - Check formulas are copied exactly from source when possible.
   - Check answers and mock questions are labeled when inferred or generated.
   - Check citations point to real extracted locations.

## Extraction Rules

Use `references/extraction-rules.md` when extracting exam points, formulas, exercises, high-frequency question types, teacher emphasis, duplicates, and completeness warnings.

Use these defaults unless the user gives a different preference:

- Importance: `high`, `medium`, `low`
- Question types: choice, fill_blank, true_false, calculation, short_answer, proof, design, comprehensive, unknown
- Difficulty: easy, medium, hard
- Citation format: `《文件名》第N页`, `《文件名》第N页幻灯片`, `《文件名》第N段`, or the closest available equivalent
- Language: match the user/course language, usually Chinese for Chinese course materials

## Output Style

Write like an exam coach, not a textbook. Prefer compact tables, checklists, and source-backed bullet points.

For each generated review artifact:

- Put highest-value exam content first.
- Separate source-backed content from inferred/generated content.
- Mark generated questions as `AI生成题` when not directly from source.
- Add `资料不足` or `当前资料中没有找到足够依据` when source evidence is missing.

For complete review packs, follow `references/output-spec.md`.

## RAG / QA Behavior

When answering questions from generated or uploaded course materials:

1. Retrieve the most relevant source chunks.
2. Answer only from those chunks.
3. Cite every substantive claim.
4. If evidence is insufficient, say: `当前资料中没有找到足够依据`.
5. In no-LLM/local mode, return the best original snippets with citations instead of a synthesized answer.

## When Working in a Repo

If the user wants a reusable implementation, create or update project files only after confirming they want code. This skill itself is primarily an agent workflow; do not default to scaffolding a Python package.

If the user wants to publish this skill, keep the package minimal:

```text
finalreview-skill/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── extraction-rules.md
    └── output-spec.md
```

Do not add unrelated README, demo app, or source-code scaffolding unless explicitly requested.
