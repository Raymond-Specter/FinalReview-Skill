from __future__ import annotations

import csv
from pathlib import Path

from finalreview.models import AnkiCard, ExamPoint, FormulaItem
from finalreview.processing.source_tracker import format_source


def build_anki_cards(points: list[ExamPoint], formulas: list[FormulaItem]) -> list[AnkiCard]:
    cards: list[AnkiCard] = []
    for point in points:
        cards.append(
            AnkiCard(
                front=f"什么是 {point.title}？",
                back=point.explanation or point.title,
                tags=["考点", point.importance, point.module],
                source_refs=point.source_refs,
            )
        )
    for formula in formulas:
        cards.append(
            AnkiCard(
                front=f"{formula.name} 的公式是什么？",
                back=f"{formula.formula_text}\n{formula.meaning}",
                tags=["公式"],
                source_refs=formula.source_refs,
            )
        )
    return cards


def write_anki_csv(cards: list[AnkiCard], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["front", "back", "tags", "source"])
        writer.writeheader()
        for card in cards:
            writer.writerow(
                {
                    "front": card.front,
                    "back": card.back,
                    "tags": " ".join(card.tags),
                    "source": "；".join(format_source(ref) for ref in card.source_refs),
                }
            )
