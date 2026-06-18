from finalreview.extraction.exercises import extract_exercises
from finalreview.models import DocumentChunk, SourceRef


def test_exercise_extraction_and_duplicates():
    chunks = [
        DocumentChunk(
            id="c1",
            text="1. 计算题：为什么 z^-1 表示延迟一拍？\n答案：延迟一个采样周期。",
            source=SourceRef(file_name="作业.md"),
        ),
        DocumentChunk(
            id="c2",
            text="1. 计算题：为什么 z^-1 表示延迟一拍？\n答案：延迟一个采样周期。",
            source=SourceRef(file_name="往年卷.md"),
        ),
    ]
    exercises = extract_exercises(chunks)
    assert len(exercises) == 2
    assert exercises[0].is_duplicate
    assert exercises[0].duplicate_group_id == exercises[1].duplicate_group_id
