from __future__ import annotations

from difflib import SequenceMatcher

from finalreview.models import ExerciseItem


def mark_duplicates(exercises: list[ExerciseItem], threshold: float = 0.86) -> list[ExerciseItem]:
    groups: list[list[int]] = []
    used: set[int] = set()
    for i, item in enumerate(exercises):
        if i in used:
            continue
        group = [i]
        used.add(i)
        for j in range(i + 1, len(exercises)):
            if j in used:
                continue
            score = SequenceMatcher(None, item.question_text, exercises[j].question_text).ratio()
            if score >= threshold:
                group.append(j)
                used.add(j)
        groups.append(group)
    for group_index, group in enumerate(groups, start=1):
        if len(group) < 2:
            continue
        gid = f"dup_{group_index:03d}"
        for idx in group:
            exercises[idx].is_duplicate = True
            exercises[idx].duplicate_group_id = gid
            exercises[idx].duplicate_count = len(group)
    return exercises
