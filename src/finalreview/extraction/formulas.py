from __future__ import annotations

import re

from finalreview.models import DocumentChunk, FormulaItem
from finalreview.utils.text_utils import short_snippet, stable_id

FORMULA_RE = re.compile(
    r"(\$[^$]+\$|\\\(.+?\\\)|\\\[.+?\\\]|[A-Za-zΦφΔΣ∫][A-Za-z0-9_(){}\-\^]*\s*=\s*[^。\n；;]{1,120}|(?:G|D|Φ|phi)\(z\)|z\^-?1|lim|Σ|∫|Δ)"
)


def extract_formulas(chunks: list[DocumentChunk]) -> list[FormulaItem]:
    formulas: list[FormulaItem] = []
    seen: set[str] = set()
    for chunk in chunks:
        for line in chunk.text.splitlines():
            text = line.strip()
            if not text or len(text) > 220:
                continue
            if FORMULA_RE.search(text):
                key = text.lower()
                if key in seen:
                    continue
                seen.add(key)
                formulas.append(
                    FormulaItem(
                        id=stable_id("formula", text, len(formulas)),
                        formula_text=text,
                        formula_latex=text if "$" in text or "\\" in text else "",
                        name=infer_formula_name(text),
                        meaning=short_snippet(text, 120),
                        variables=infer_variables(text),
                        conditions="请结合来源材料确认适用条件。",
                        common_mistakes=["符号方向、下标、延迟拍数和适用条件容易混淆。"],
                        source_refs=[chunk.source],
                    )
                )
    return formulas


def infer_formula_name(text: str) -> str:
    if "G(z)" in text or "D(z)" in text:
        return "离散控制传递函数相关公式"
    if "z^-1" in text or "z-1" in text:
        return "Z 变换延迟算子"
    if "=" in text:
        return text.split("=")[0].strip()[:40] or "公式"
    return "公式"


def infer_variables(text: str) -> list[str]:
    return sorted(set(re.findall(r"\b[A-Za-zΦφΔ]\w*(?:\(z\))?", text)))[:12]
