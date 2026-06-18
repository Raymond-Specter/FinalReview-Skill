from __future__ import annotations

from finalreview.models import ExamPoint, ExerciseItem, MockExam


def generate_mock_exam(
    exercises: list[ExerciseItem],
    points: list[ExamPoint],
    *,
    title: str = "模拟卷A",
    difficulty: str = "medium",
    duration: int = 120,
) -> MockExam:
    selected = [ex for ex in exercises if difficulty == "medium" or ex.difficulty == difficulty][:12]
    if len(selected) < 5:
        for point in points[: 5 - len(selected)]:
            selected.append(
                ExerciseItem(
                    id=f"ai_{point.id}",
                    question_text=f"【AI生成题】请简述：{point.title}。",
                    answer_text=point.explanation,
                    explanation="根据考点自动补充的概念题，请结合来源复核。",
                    chapter=point.chapter,
                    module=point.module,
                    question_type="short_answer",
                    difficulty=difficulty if difficulty in {"easy", "medium", "hard"} else "medium",
                    related_exam_points=[point.title],
                    source_refs=point.source_refs,
                )
            )
    return MockExam(
        title=title,
        questions=selected,
        answer_key=[q.answer_text or "请参考原始资料整理答案。" for q in selected],
        duration_minutes=duration,
        difficulty=difficulty,
    )
