# FinalReview-Skill

FinalReview-Skill 是一个 local-first 的期末周复习资料生成工具。它会读取一门课程的 PDF、PPTX、DOCX、Markdown、TXT、CSV/XLSX 和图片资料，生成考点清单、公式表、练习题题库、模拟卷、Anki 卡片、知识图谱、复习计划、资料完整性检查，以及带来源引用的本地 RAG 问答。

本项目不能保证 100% 准确。生成内容必须结合原始资料复核；项目会尽量保留来源引用，方便用户检查。

## 功能

* 多格式资料解析：PDF、PPTX、DOCX、TXT、MD、CSV、XLSX、图片 OCR 可选
* 规则抽取：考点、公式、练习题、老师强调语气
* 题目去重：基于文本相似度生成重复组
* 输出资料：复习指南、考点清单、公式表、题库、高频题型、模拟卷、错题本、Anki CSV、知识图谱、复习计划、完整性报告
* 本地 RAG：TF-IDF 检索，回答必须引用来源
* 可插拔 LLM：none / OpenAI / Ollama
* CLI 和 Streamlit Web UI

## 安装

```bash
python -m pip install -e ".[dev,ui,ocr,openai,ollama]"
```

只需要 CLI 时：

```bash
python -m pip install -e .
```

## 快速开始

```bash
python -m finalreview run --input examples/course_materials --output examples/output --course-name 示例课程
python -m finalreview ask --output examples/output --question "Z^-1 为什么表示延迟一拍？"
```

## CLI 示例

```bash
python -m finalreview parse --input course_materials --output output
python -m finalreview generate-exam --output output --difficulty medium --duration 120
python -m finalreview plan --output output --exam-date 2026-06-25 --days 5
python -m finalreview version
```

## Web UI

```bash
streamlit run src/finalreview/ui/streamlit_app.py
```

浏览器中上传多个课程文件，设置课程名，选择 LLM 后端，然后生成复习资料和下载 zip。

## 输入输出

输入示例：

```text
course_materials/
├── 第1章_绪论.pptx
├── 第2章_Z变换.pdf
├── 作业题.docx
└── 课堂录音转写.txt
```

输出示例：

```text
output/
├── 00_期末总复习指南.md
├── 01_考点清单.md
├── 02_公式表.md
├── 03_练习题题库.md
├── 04_高频题型.md
├── 05_模拟卷A.md
├── 06_模拟卷A_答案解析.md
├── 07_错题本模板.md
├── 08_Anki卡片.csv
├── 09_知识图谱.md
├── 10_复习计划.md
├── 11_资料完整性检查.md
├── chunks.jsonl
├── source_index.json
└── vector_index/
```

## LLM 配置

默认 `none` 模式不调用云服务。

OpenAI：

```bash
set OPENAI_API_KEY=...
python -m finalreview ask --output output --question "问题" --backend openai
```

Ollama：

```bash
ollama serve
python -m finalreview ask --output output --question "问题" --backend ollama
```

## OCR 配置

图片 OCR 使用可选依赖 `pytesseract` 和系统 Tesseract。未安装时不会崩溃，程序会输出清晰提示。

## 项目结构

```text
src/finalreview/
├── cli.py
├── config.py
├── models.py
├── parsers/
├── processing/
├── extraction/
├── llm/
├── rag/
├── generation/
├── prompts/
├── ui/
└── utils/
```

## 开发

```bash
python -m pytest
python -m finalreview version
```

## 常见问题

* `.doc` 文件暂不直接支持，请转换为 `.docx`。
* 扫描 PDF 需要 OCR，本项目会标记疑似 OCR 页。
* RAG 回答只基于已解析资料；资料不足时会明确说明没有足够依据。

## License

MIT
