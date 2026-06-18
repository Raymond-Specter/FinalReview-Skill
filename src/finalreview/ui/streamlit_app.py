from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import streamlit as st

from finalreview.cli import build_vector_index, make_llm, parse_materials
from finalreview.config import AppConfig
from finalreview.extraction.exam_points import extract_exam_points
from finalreview.extraction.exercises import extract_exercises
from finalreview.extraction.formulas import extract_formulas
from finalreview.generation.markdown_writer import write_all_outputs
from finalreview.rag.qa import answer_question


st.set_page_config(page_title="FinalReview-Skill", layout="wide")
st.title("FinalReview-Skill")

course_name = st.text_input("课程名", value="示例课程")
backend = st.selectbox("LLM 后端", ["none", "openai", "ollama"])
uploaded = st.file_uploader("上传课程资料文件", accept_multiple_files=True)

if "output_dir" not in st.session_state:
    st.session_state.output_dir = None

if st.button("生成复习资料", type="primary", disabled=not uploaded):
    with st.spinner("正在解析和生成..."):
        work = Path(tempfile.mkdtemp(prefix="finalreview_"))
        input_dir = work / "course_materials"
        output_dir = work / "output"
        input_dir.mkdir(parents=True, exist_ok=True)
        for file in uploaded:
            (input_dir / file.name).write_bytes(file.getbuffer())
        cfg = AppConfig()
        files, chunks = parse_materials(input_dir, output_dir, cfg.chunk_size, cfg.chunk_overlap)
        points = extract_exam_points(chunks)
        formulas = extract_formulas(chunks)
        exercises = extract_exercises(chunks)
        write_all_outputs(
            output_dir,
            course_name=course_name,
            files=files,
            chunks=chunks,
            points=points,
            formulas=formulas,
            exercises=exercises,
        )
        build_vector_index(chunks, output_dir)
        st.session_state.output_dir = output_dir
        st.success("生成完成")

if st.session_state.output_dir:
    output_dir = Path(st.session_state.output_dir)
    st.subheader("生成结果")
    for path in sorted(output_dir.glob("*.md")):
        with st.expander(path.name):
            st.markdown(path.read_text(encoding="utf-8"))
    zip_path = shutil.make_archive(str(output_dir), "zip", output_dir)
    st.download_button("下载 output.zip", Path(zip_path).read_bytes(), file_name="output.zip")
    question = st.text_input("RAG 问答")
    if st.button("提问") and question:
        st.write(answer_question(output_dir, question, llm=make_llm(backend)))
