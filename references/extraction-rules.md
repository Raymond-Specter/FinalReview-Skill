# Extraction Rules

## Exam Points

Extract an exam point when a chunk contains one or more of:

- Explicit teacher/exam signals: `重点`, `难点`, `掌握`, `熟悉`, `了解`, `考试`, `必考`, `可能考`, `这个要会`, `大家注意`, `容易错`
- Structural signals: chapter/section headings, slide titles, syllabus scope, review outline
- Knowledge-unit signals: `定义`, `性质`, `定理`, `公式`, `步骤`, `算法`, `设计方法`, `证明`, `推导`
- Frequency signals: repeated terms across slides, homework, quizzes, and past papers

For each exam point, capture:

- title
- chapter/module
- importance: high / medium / low
- likely exam forms
- one-sentence explanation
- prerequisites, if evident
- source references

Importance heuristic:

- High: appears in review scope, past papers, repeated homework, teacher emphasis, or multiple source types
- Medium: appears in headings, formulas, examples, or one major source
- Low: appears once without exam signal

## Formulas

Extract formulas and formula-like expressions containing:

- LaTeX math
- `=`, `Σ`, `∫`, `lim`, `Δ`, `Φ`, `G(z)`, `D(z)`, `z^-1`, transfer functions, error equations, controller equations
- Engineering calculation procedures where variables and conditions matter

For each formula, keep:

- exact original formula text
- LaTeX only if safely available
- name or nearby heading
- variable meanings if source states them
- conditions/applicability if source states them
- common mistakes when source or exam pattern implies them
- source references

Do not rewrite formulas unless necessary for readability. If conversion is uncertain, preserve the original.

## Exercises

Extract exercises from:

- keywords: `例题`, `练习`, `习题`, `作业`, `题`, `选择`, `填空`, `判断`, `计算`, `证明`, `设计`, `综合`
- numbering: `1.`, `1）`, `（1）`, `Q1`, `Question 1`, `Exercise 1`, `Exercice 1`
- past paper or homework sections

For each exercise, capture:

- question stem
- options if present
- answer if present
- explanation if present
- source
- chapter/module
- question type
- difficulty
- related exam points

Do not fabricate missing answers. If generating a practice answer or supplemental question, label it as generated.

## Duplicate / High-Frequency Patterns

Treat exercises as duplicates or variants when they share:

- same target concept and same solving procedure
- near-identical wording
- same formula with changed parameters
- repeated past-paper style

Do not delete duplicates. Group them and report:

- duplicate group id
- occurrence count
- all sources
- what changed across variants

High-frequency question types should include:

- pattern name
- occurrence count
- related exam points
- common wording
- typical solution path
- common mistakes
- recommended practice order

## Completeness Checks

Flag missing or weak materials:

- no past papers
- no answer keys
- no review scope
- only slides and no exercises
- only exercises and no explanations
- scanned PDF/images needing OCR
- parse/OCR failures
- missing chapters inferred from file names or syllabus
- duplicate/low-quality files

Output suggestions as concrete next actions, not vague warnings.
