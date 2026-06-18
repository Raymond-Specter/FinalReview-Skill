from finalreview.models import SourceRef
from finalreview.processing.source_tracker import format_source


def test_source_ref_formatting():
    ref = SourceRef(file_name="第3章.pptx", slide_number=18, text_snippet="最少拍控制")
    assert format_source(ref) == "《第3章.pptx》第18页幻灯片"
