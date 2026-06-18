---
name: finalreview-skill
description: Exam-scoring-oriented final review skill for Codex, Claude Code, and similar agents. Use for university final exam review, exam cramming, course-material cleanup, knowledge point extraction, question generation, answer explanation, mock exam creation, Anki card generation, weak-point practice, wrong-question books, source-cited QA, and completeness checks from user-provided PDFs, PPT/PPTX, Word docs, Markdown/TXT, spreadsheets, images/OCR text, assignments, quizzes, past papers, review scopes, and lecture transcripts. Prioritize past papers, teacher slides, homework, and cleaned Markdown; generate outputs that help the student know what to memorize, what to write, and how to score.
---

# FinalReview Skill

## Core Idea

This is not a random quiz generator and not a generic tutor. It is a stable, reusable final-review protocol.

The student brings the materials. The agent extracts, cleans, ranks, turns them into exam-facing notes and questions, and explains answers in a way that helps score points.

Default principles:

- Work from user-provided materials first; do not rely on random external question banks.
- Convert materials to Markdown before serious analysis whenever possible.
- Clean first, extract second, generate questions third.
- Prefer exam-scoring usefulness over archival completeness.
- Preserve source evidence; exact page/slide citations are best, but category-level source labels are acceptable when exact locations are unavailable.
- Never invent source-backed facts, answers, formulas, or exam scope.

## Core Workflow

1. Confirm the exam shape.
   - Identify known question types, scoring style, open/closed book constraints, teacher emphasis, review scope, and common exam patterns.
   - If the user already provided this, do not ask again.
   - If unknown, proceed with explicit assumptions and mark uncertain areas.

2. Inventory the materials.
   - Classify each file by role: past paper, teacher PPT/slides, homework, reading assignment, review scope, textbook note, lecture transcript, quick-course material, handwritten/scan/image, spreadsheet/data.
   - Use this priority for deciding what matters:
     1. Past papers / real exams
     2. Teacher PPT/slides
     3. Homework / reading assignments / quizzes
     4. Review scope / syllabus constraints
     5. Quick-course materials
     6. AI supplemental questions
   - Quick-course materials have lower question-source priority but high value for structure, knowledge-point extraction, and review order.

3. Convert to Markdown.
   - Prefer `markitdown` when available.
   - Use PDF, document, presentation, spreadsheet, and OCR tools as needed.
   - For scans/images, run OCR when available; otherwise flag the file clearly.
   - Keep file names and page/slide/section metadata where possible.

4. Clean the Markdown.
   - Remove mojibake, duplicate blocks, decorative noise, navigation text, and low-value filler.
   - Merge repeated definitions, conclusions, and method steps.
   - Preserve definitions, properties, theorems, formulas, standard methods, typical exam forms, teacher emphasis, and common mistakes.
   - The goal is `清晰、可背、可考`, not full archival storage.

5. Extract the exam-facing knowledge base.
   - Extract exam points, formulas, question patterns, exercises, answer fragments, teacher-emphasis phrases, and weak-completeness signals.
   - Use `references/extraction-rules.md` for detailed extraction rules.

6. Generate exam-scoring outputs.
   - If the user asks for a subset, generate only that subset.
   - If the user asks broadly for final review materials, follow `references/output-spec.md`.
   - Question quantity is not evenly distributed. Dense, frequent, multi-form, teacher-emphasized points get more questions.
   - Each knowledge point usually gets `1~6` questions depending on importance and examability.

7. Separate questions and answers unless the format says otherwise.
   - Plain Markdown/text: put questions first and answers/explanations later.
   - HTML/interactive output: answers may appear under each question but should be collapsed by default.

8. Validate before delivery.
   - Check that outputs mention uncertain areas and missing materials.
   - Check formulas are copied exactly from source when possible.
   - Check generated questions are labeled `AI补充` or `AI生成题`.
   - Check answers are not presented as source-backed when they are inferred.

## Question Generation Rules

Generate questions according to likely real exam types, not a balanced template.

Match question type to knowledge type:

- Recognition / discrimination -> choice, true-false, fill blank
- Definition / comparison -> short answer
- Formula / procedure -> calculation
- theorem / construction / algorithm -> proof, design, comprehensive
- repeated past-paper pattern -> variant question

Every generated question should carry a lightweight source label:

- `题源：历年真题`
- `题源：老师PPT`
- `题源：平时作业`
- `题源：复习范围`
- `题源：速成课框架改编`
- `题源：综合改编`
- `题源：AI补充`

Use exact file/page/slide citations when available. When not available, category-level labels are acceptable, but do not fake precision.

## Explanation Rules

Explanations must serve exam scoring, not just correctness.

For objective questions, include:

- `这题核心知识点`
- key definition/property/judgment basis
- why wrong options are wrong, if options exist
- easy-confusion point

For subjective questions, include:

- `这题答题核心点`
- `必须出现`
- `常见失分点`
- standard answer structure
- what to write first to grab partial credit

Avoid motivational filler. Prefer exact wording students can reuse in an exam.

## RAG / QA Behavior

When answering questions from generated or uploaded course materials:

1. Retrieve the most relevant source chunks.
2. Answer only from those chunks.
3. Cite every substantive claim.
4. If evidence is insufficient, say: `当前资料中没有找到足够依据`.
5. In no-LLM/local mode, return the best original snippets with citations instead of a synthesized answer.

## Long-Term Rule Sync

When working in a repository that contains `AGENT.md`, `CLAUDE.md`, or similar long-term agent rule files, check whether they are consistent with this skill after using or updating the skill.

Sync long-term rules when:

- the user asks for "以后默认这样做";
- the repository is clearly a final-review skill/rules repository;
- this skill changes stable behavior;
- old `AGENT.md` / `CLAUDE.md` rules conflict with this skill.

Do not blindly paste the full `SKILL.md`. Put stable defaults into `AGENT.md` / `CLAUDE.md`: source priority, Markdown conversion and cleanup, question generation rules, answer separation, explanation rules, and scoring-oriented behavior.

Respect explicit user exceptions such as "不要改 AGENT.md" or "只在本次对话里这样".

## When Working in a Repo

This skill is primarily an agent workflow and rule package. Do not default to scaffolding a Python app.

For a publishable repository, use this structure:

```text
finalreview-skill/
├── SKILL.md
├── AGENT.md
├── README.md
├── agents/openai.yaml
└── references/
    ├── extraction-rules.md
    └── output-spec.md
```

Add implementation code only if the user explicitly asks for scripts/tools beyond agent rules.
