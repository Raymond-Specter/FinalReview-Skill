# finalreview-skill

面向 Codex、Claude Code、WorkBuddy 等 agent 的期末复习 Skill。

它的核心不是脚本工具链，而是一套稳定、可复用、偏考试得分导向的复习规则：学生提供课程资料，Agent 负责清洗、提炼、排序、出题、讲解、生成复习计划，并尽量保留来源依据。

## 适合什么场景

* 你已经有课程资料：PPT/PPTX、PDF、Word、Markdown、TXT、图片、表格、课堂转写、作业、往年卷
* 你希望 AI 基于资料整理知识点、公式、题型、易错点
* 你希望题目贴近真实考试，而不是随机题库风格
* 你希望答案解析顺手告诉你“怎么写才能得分”
* 你希望生成模拟卷、Anki 卡片、错题本、复习计划和资料完整性检查

## 这个 Skill 做什么

`finalreview-skill` 会引导 Agent 按下面思路工作：

1. 先确认考试题型、老师强调点、复习范围和常见考法
2. 按题源优先级判断什么最值得复习
3. 优先把上传资料用 `markitdown` 或文件工具转成 Markdown
4. 先清洗 Markdown，再提知识点、公式和题型
5. 按真实考试题型生成题目，不平均分配
6. 每个知识点通常生成 `1~6` 题
7. 默认题答分离
8. 客观题补“这题核心知识点”
9. 主观题补“这题答题核心点 / 必须出现 / 常见失分点”
10. 解析默认服务考试拿分

## 核心规则

### 题源优先级

出题和判断重点时，按以下顺序优先：

1. 历年真题 / 往年卷
2. 老师 PPT / 课堂 slides
3. 平时作业 / 阅读作业 / quiz
4. 复习范围 / syllabus
5. 速成课题目
6. AI 补充题

速成课题目优先级较低，但在知识点梳理、框架搭建、易错点总结上很有价值。

### 材料处理规则

所有资料默认先转成 Markdown，建议优先使用：

```bash
markitdown
```

统一流程：

1. 先转 Markdown
2. 再清洗 Markdown
3. 再提知识点、公式、题型
4. 最后出题和生成复习资料

清洗重点：

* 去乱码
* 去重复
* 去低价值废话
* 合并重复定义和结论
* 保留定义、性质、定理、公式、标准方法、常见考法、易错点

目标不是“完整存档”，而是“清晰、可背、可考”。

### 出题规则

* 先按真实考试题型出题，不做平均分配
* 每个知识点通常出 `1~6` 题
* 知识点越密、越高频、考法越多，题量越多
* 题型要匹配知识点最可能考法
* 材料不足时可以补 AI 题，但必须标注 `AI补充` 或 `AI生成题`

### 题源标记规则

默认至少保留轻量类别级题源标记：

* `题源：历年真题`
* `题源：老师PPT`
* `题源：平时作业`
* `题源：复习范围`
* `题源：速成课框架改编`
* `题源：综合改编`
* `题源：AI补充`

如果可以拿到页码、幻灯片编号、段落位置，再进一步保留精确引用。

### 输出规则

普通 Markdown / 文本输出：

* 前面只放题目
* 答案统一放最后
* 题目区和答案区明显分开

HTML / 交互式输出：

* 答案可以放在题目下面
* 答案默认折叠隐藏
* 点击后再展开答案和解析

### 解析规则

解析不只解释对错，还要服务拿分。

客观题重点补：

* `这题核心知识点`
* 关键定义 / 性质 / 判定依据
* 易混点

主观题重点补：

* `这题答题核心点`
* `必须出现`
* `常见失分点`
* 标准作答框架
* 先写什么能抢步骤分

## 仓库结构

```text
finalreview-skill/
├── SKILL.md
├── AGENT.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    ├── extraction-rules.md
    └── output-spec.md
```

* `SKILL.md`：Codex skill 主入口，包含触发描述和核心工作流
* `AGENT.md`：可同步到 Claude Code / Codex / 其他 agent 的长期默认规则
* `references/extraction-rules.md`：考点、公式、题型、完整性检查的详细规则
* `references/output-spec.md`：完整复习资料包的输出格式

## 如何使用

在 Codex 中，把本仓库放到：

```text
C:\Users\<你的用户名>\.codex\skills\finalreview-skill
```

然后直接说：

```text
请使用 finalreview-skill，基于我上传的课程资料生成期末复习资料。
```

或者：

```text
Use finalreview-skill to create exam points, formulas, practice questions, mock exams, Anki cards, a study plan, and source-cited QA from these course files.
```

如果你的 Agent 支持长期规则文件，可以把 `AGENT.md` 的内容同步到项目级 `AGENT.md`、`CLAUDE.md` 或类似规则文件中。

## 完整输出能力

该 skill 可以指导 Agent 生成：

* 考点清单
* 公式表
* 练习题题库
* 高频题型
* 重点程度排序
* 模拟卷
* 答案解析
* Anki 卡片
* 知识图谱
* 复习计划
* 错题本模板
* 本地资料问答
* 资料完整性检查

## Contributing

欢迎基于真实复习经验改进：

* 更好的题源优先级策略
* 更稳的 Markdown 清洗规则
* 更贴近考试的出题协议
* 更强的客观题 / 主观题解析模板
* 具体学科专用复习规则

建议贡献流程：

1. Fork 本仓库
2. 新建分支
3. 修改 `SKILL.md`、`AGENT.md`、`README.md` 或 `references/`
4. 提交 commit
5. 发起 Pull Request

## License

MIT
