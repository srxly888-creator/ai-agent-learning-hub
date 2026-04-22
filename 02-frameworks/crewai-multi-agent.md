# CrewAI 多智能体框架入门到实战

> 面向小白的多智能体编排框架教程，从安装到项目实战

## 📋 目录

- [前言](#前言)
- [一、CrewAI 是什么](#一crewai-是什么)
- [二、安装与快速开始](#二安装与快速开始)
- [三、核心概念：Agent（智能体）](#三核心概念agent智能体)
- [四、核心概念：Task（任务）](#四核心概念task任务)
- [五、核心概念：Crew（团队）](#五核心概念crew团队)
- [六、流程模式详解](#六流程模式详解)
- [七、工具系统](#七工具系统)
- [八、实战：内容创作团队](#八实战内容创作团队)
- [九、实战：代码审查团队](#九实战代码审查团队)
- [十、最佳实践与避坑指南](#十最佳实践与避坑指南)
- [十一、与其他框架对比](#十一与其他框架对比)
- [十二、总结](#十二总结)

---

## 前言

想象一个软件开发团队：产品经理写需求、设计师画原型、程序员写代码、测试工程师找Bug。每个人有自己的职责，协作完成一个大项目。

**CrewAI 就是让 AI 智能体像团队一样协作工作的框架。**

你定义每个智能体的"角色"和"技能"，给他们分配"任务"，然后让他们按照一定的流程自动协作完成工作。

> 💡 **小白提示**：建议先阅读 [《AI Agent 架构详解》](../01-fundamentals/ai-agent-architecture.md) 和 [《多智能体系统》](../01-fundamentals/multi-agent-systems.md) 了解基础概念。

---

## 一、CrewAI 是什么

### 1.1 一句话解释

CrewAI 是一个 Python 框架，让你可以创建多个 AI 智能体，给它们分配角色和任务，让它们像真实团队一样协作完成复杂工作。

### 1.2 核心理念

```
传统编程：你写代码，一步一步完成任务
单体Agent：一个AI完成所有任务
CrewAI：多个AI，各有专长，协作完成
```

### 1.3 为什么需要多智能体？

```
单一 Agent 的问题：
  ❌ 知识面广但不专精
  ❌ 长流程容易跑偏
  ❌ 难以处理需要多种技能的任务

多智能体的优势：
  ✅ 每个Agent专注一个领域
  ✅ 角色分工明确，职责清晰
  ✅ 可以并行处理，效率更高
  ✅ 互相检查，减少错误
```

---

## 二、安装与快速开始

### 2.1 安装

```bash
pip install crewai crewai-tools
```

### 2.2 配置 API Key

```bash
# 推荐使用环境变量
export OPENAI_API_KEY="sk-..."
# 或者用其他模型
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 2.3 Hello World

```python
from crewai import Agent, Task, Crew

# 第一步：创建智能体
researcher = Agent(
    role="研究员",
    goal="搜集关于AI行业的信息",
    backstory="你是一位资深AI行业研究员，擅长信息搜集和分析",
    verbose=True
)

writer = Agent(
    role="作家",
    goal="将研究结果写成通俗易懂的文章",
    backstory="你是一位科普作家，擅长把复杂概念讲清楚",
    verbose=True
)

# 第二步：创建任务
research_task = Task(
    description="研究2026年AI行业的主要趋势",
    agent=researcher  # 分配给研究员
)

writing_task = Task(
    description="根据研究员的发现，写一篇500字的科普文章",
    agent=writer  # 分配给作家
)

# 第三步：组建团队并启动
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

就这么简单！三个步骤：**定义Agent → 分配Task → 组建Crew**。

---

## 三、核心概念：Agent（智能体）

Agent 是 CrewAI 的核心，代表团队中的一个"角色"。

### 3.1 Agent 的关键属性

```python
from crewai import Agent

agent = Agent(
    role="数据分析师",           # 角色：这个Agent是谁
    goal="提供准确的数据分析",     # 目标：它要达成什么
    backstory="你是...",          # 背景故事：塑造行为风格
    llm="gpt-4o",               # 使用的模型（可选）
    tools=[search_tool],         # 可用的工具（可选）
    verbose=True,                # 是否打印思考过程
    allow_delegation=False,      # 是否允许委托任务
    max_iter=15,                 # 最大迭代次数
    max_rpm=10                   # 每分钟最大请求数
)
```

### 3.2 各属性详解

| 属性 | 说明 | 示例 |
|------|------|------|
| `role` | 角色名称，定义Agent的身份 | "资深前端工程师" |
| `goal` | 目标，Agent要达成的目的 | "写出高质量的React代码" |
| `backstory` | 背景故事，影响Agent的行为方式 | "你在BAT工作10年，精通React生态" |
| `llm` | 使用的语言模型 | "gpt-4o", "claude-4-sonnet" |
| `tools` | Agent可以使用的工具列表 | [搜索工具, 计算器工具] |
| `verbose` | 是否输出详细过程 | True（调试时开启） |
| `allow_delegation` | 是否能把任务委托给其他Agent | False（默认） |
| `max_iter` | 最大思考迭代次数 | 15（默认） |

### 3.3 背景故事的重要性

`backstory` 看起来像在"编故事"，但它非常重要——它直接影响Agent的行为风格和决策方式。

```python
# ❌ 不好的背景故事
backstory="你是一个程序员"

# ✅ 好的背景故事
backstory="""
你是一位有15年经验的高级后端工程师，曾在阿里和字节跳动工作。
你精通Python、Go和Java，特别擅长系统架构设计。
你写代码注重可维护性和性能，总是先写测试再写实现。
你习惯用简洁明了的方式解释技术决策。
"""
```

---

## 四、核心概念：Task（任务）

Task 定义了需要完成的具体工作。

### 4.1 基本用法

```python
from crewai import Task

task = Task(
    description="分析用户反馈数据，找出最常见的前5个问题",  # 任务描述
    agent=analyst,          # 执行者
    expected_output="一份包含5个问题的清单，每个问题附频率和影响程度",  # 期望输出
    tools=[data_tool],      # 专用工具
)
```

### 4.2 任务的依赖关系

```python
# Task 2 依赖 Task 1 的结果
task1 = Task(
    description="搜集AI行业新闻",
    agent=researcher,
    expected_output="一份新闻摘要"
)

task2 = Task(
    description="根据新闻摘要写分析报告",
    agent=analyst,
    expected_output="分析报告",
    context=[task1]  # 👈 关键：指定依赖
)

# task2 会自动获取 task1 的输出作为上下文
```

### 4.3 异步任务

```python
# 异步任务可以并行执行
task_a = Task(
    description="研究竞品A",
    agent=researcher_a,
    async_execution=True  # 👈 异步执行
)

task_b = Task(
    description="研究竞品B",
    agent=researcher_b,
    async_execution=True  # 👈 异步执行
)

task_summary = Task(
    description="综合两个竞品研究，写对比报告",
    agent=writer,
    context=[task_a, task_b]  # 等待两个任务都完成
)
```

---

## 五、核心概念：Crew（团队）

Crew 把 Agent 和 Task 组合起来，定义协作流程。

### 5.1 基本用法

```python
from crewai import Crew

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    verbose=True,
    process=Process.sequential,  # 流程模式
    memory=True,                 # 启用记忆
)
```

### 5.2 Crew 的关键参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `agents` | 智能体列表 | 必填 |
| `tasks` | 任务列表 | 必填 |
| `process` | 流程模式 | sequential |
| `verbose` | 详细输出 | True |
| `memory` | 启用长期记忆 | False |
| `max_rpm` | 每分钟最大请求数 | 无限制 |
| `full_output` | 返回完整输出 | False |

### 5.3 启动团队

```python
# 启动（同步）
result = crew.kickoff()

# 启动（异步）
result = await crew.kickoff_async()

# 获取详细输出
result = crew.kickoff(return_full_output=True)
# result.raw — 原始输出
# result.tasks_output — 每个任务的输出
# result.json_dict — JSON格式的输出
```

---

## 六、流程模式详解

CrewAI 支持两种内置流程模式，还可以自定义流程。

### 6.1 Sequential（顺序流程）

任务按定义的顺序，一个接一个执行。

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Task 1   │───→│ Task 2   │───→│ Task 3   │
│ Agent A  │    │ Agent B  │    │ Agent C  │
└──────────┘    └──────────┘    └──────────┘
```

```python
from crewai import Crew, Process

crew = Crew(
    agents=[agent_a, agent_b, agent_c],
    tasks=[task_1, task_2, task_3],
    process=Process.sequential  # 顺序执行
)
```

**适用场景**：有明确先后关系的任务链，比如"调研 → 分析 → 写报告"。

### 6.2 Hierarchical（层级流程）

自动选出一个"管理者"，由它来规划和分配任务。

```
        ┌──────────────┐
        │   Manager    │
        │  (自动生成)   │
        └──────┬───────┘
               │ 规划和分配
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Agent A │ │Agent B │ │Agent C │
└────────┘ └────────┘ └────────┘
```

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,  # 层级流程
    manager_llm="gpt-4o"           # 管理者使用的模型
)
```

**适用场景**：
- 任务之间的顺序不固定
- 需要动态决策执行顺序
- 任务可能需要反复修改

### 6.3 两种模式对比

| 特性 | Sequential | Hierarchical |
|------|-----------|--------------|
| 执行顺序 | 固定 | 动态规划 |
| Token消耗 | 较少 | 较多（Manager需要思考） |
| 灵活性 | 低 | 高 |
| 可控性 | 高 | 中 |
| 适合场景 | 流程明确的任务 | 复杂、灵活的任务 |
| 调试难度 | 容易 | 较难 |

### 6.4 自定义流程

```python
from crewai.flow.flow import Flow, listen, start

class ResearchFlow(Flow):
    @start()
    def research(self):
        return researcher.kickoff(inputs={"topic": "AI趋势"})
    
    @listen(research)
    def analyze(self, research_result):
        return analyst.kickoff(inputs={"data": research_result})
    
    @listen(analyze)
    def write_report(self, analysis_result):
        return writer.kickoff(inputs={"analysis": analysis_result})

# 运行
flow = ResearchFlow()
result = flow.kickoff()
```

---

## 七、工具系统

CrewAI 内置了丰富的工具，也可以自定义工具。

### 7.1 使用内置工具

```python
from crewai_tools import (
    SerperDevTool,       # 网络搜索
    ScrapeWebsiteTool,   # 网页抓取
    FileReadTool,        # 读取文件
    FileWriterTool,      # 写入文件
    DirectoryReadTool,   # 读取目录
    CalculatorTool,      # 计算器
    CodeInterpreterTool, # 代码执行
)

# 给Agent配置工具
researcher = Agent(
    role="研究员",
    goal="搜集信息",
    backstory="...",
    tools=[SerperDevTool(), ScrapeWebsiteTool()]
)
```

### 7.2 自定义工具

```python
from crewai_tools import BaseTool

class SentimentAnalyzer(BaseTool):
    name: str = "情感分析工具"
    description: str = "分析文本的情感倾向（正面/负面/中性）"
    
    def _run(self, text: str) -> str:
        # 你的自定义逻辑
        # 这里可以调用任何Python代码
        from transformers import pipeline
        classifier = pipeline("sentiment-analysis")
        result = classifier(text)
        return str(result)

# 使用
agent = Agent(
    role="情感分析师",
    tools=[SentimentAnalyzer()],
    ...
)
```

---

## 八、实战：内容创作团队

一个完整的内容创作流水线：研究员 → 分析师 → 作家 → 编辑。

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# 1. 定义智能体
researcher = Agent(
    role="资深科技研究员",
    goal="搜集关于指定话题的最新、最全面的信息",
    backstory="你是一位有20年经验的科技记者，擅长深度调研",
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
    verbose=True
)

analyst = Agent(
    role="技术分析师",
    goal="从研究数据中提取关键洞察和趋势",
    backstory="你是前麦肯锡技术顾问，擅长数据分析和趋势预判",
    verbose=True
)

writer = Agent(
    role="科普作家",
    goal="将分析结果转化为通俗易懂、引人入胜的文章",
    backstory="你是一位畅销科普作家，获得过普利策奖",
    verbose=True
)

editor = Agent(
    role="资深编辑",
    goal="审查文章质量，确保准确性和可读性",
    backstory="你是一位严格的杂志主编，对质量要求极高",
    verbose=True
)

# 2. 定义任务
research_task = Task(
    description="全面研究 '{topic}' 这个话题，包括：1)发展历程 2)当前状态 3)未来趋势",
    agent=researcher,
    expected_output="一份结构化的研究报告"
)

analysis_task = Task(
    description="基于研究报告，分析：1)核心驱动力 2)关键挑战 3)投资机会",
    agent=analyst,
    expected_output="一份深度分析报告",
    context=[research_task]
)

writing_task = Task(
    description="基于分析报告，写一篇2000字的科普文章，要求通俗易懂",
    agent=writer,
    expected_output="一篇完整的科普文章",
    context=[analysis_task]
)

editing_task = Task(
    description="审查文章，修正事实错误，优化表达，确保专业性和可读性",
    agent=editor,
    expected_output="最终版文章",
    context=[writing_task]
)

# 3. 组建团队
crew = Crew(
    agents=[researcher, analyst, writer, editor],
    tasks=[research_task, analysis_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)

# 4. 启动
result = crew.kickoff(inputs={"topic": "2026年AI Agent发展趋势"})
print(result)
```

---

## 九、实战：代码审查团队

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool, FileReadTool

# 代码审查团队
code_reader = Agent(
    role="代码阅读器",
    goal="快速扫描代码库，识别需要审查的文件",
    backstory="你是一位经验丰富的代码审查员",
    tools=[DirectoryReadTool(), FileReadTool()],
    verbose=True
)

security_reviewer = Agent(
    role="安全审查专家",
    goal="审查代码中的安全漏洞",
    backstory="你是一位网络安全专家，曾发现多个重大漏洞",
    verbose=True
)

quality_reviewer = Agent(
    role="代码质量专家",
    goal="审查代码质量和最佳实践",
    backstory="你是一位代码质量顾问，精通Clean Code原则",
    verbose=True
)

summarizer = Agent(
    role="审查报告撰写者",
    goal="整合所有审查意见，生成清晰的报告",
    backstory="你擅长技术文档写作",
    verbose=True
)

# 任务定义
scan_task = Task(
    description="扫描 {code_path} 目录下的所有Python文件",
    agent=code_reader,
    expected_output="文件列表和初步评估"
)

security_task = Task(
    description="从安全角度审查代码",
    agent=security_reviewer,
    expected_output="安全审查报告",
    context=[scan_task]
)

quality_task = Task(
    description="从代码质量角度审查代码",
    agent=quality_reviewer,
    expected_output="质量审查报告",
    context=[scan_task]
)

report_task = Task(
    description="整合安全和质量报告，生成最终审查报告",
    agent=summarizer,
    expected_output="完整的代码审查报告",
    context=[security_task, quality_task]
)

# 组建团队（security_task和quality_task可以并行）
crew = Crew(
    agents=[code_reader, security_reviewer, quality_reviewer, summarizer],
    tasks=[scan_task, security_task, quality_task, report_task],
    process=Process.hierarchical,
    verbose=True
)

result = crew.kickoff(inputs={"code_path": "./src"})
```

---

## 十、最佳实践与避坑指南

### 10.1 设计原则

```
1. 单一职责：每个Agent只做一件事
2. 清晰接口：任务之间的输入输出要明确
3. 适量Agent：不是越多越好，3-5个通常足够
4. 好的Prompt：role/goal/backstory 决定Agent质量
5. 工具匹配：给Agent配它需要的工具
```

### 10.2 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Agent 输出质量差 | 背景故事太简单 | 丰富 backstory |
| Token 消耗太高 | Hierarchical 模式太重 | 改用 Sequential |
| 任务超时 | 任务描述不明确 | 明确 expected_output |
| Agent 互相矛盾 | 角色定义冲突 | 明确每个Agent的边界 |
| 结果格式不对 | 没指定输出格式 | 在 description 中指定格式 |

### 10.3 成本控制

```python
# 1. 用便宜的模型做简单任务
researcher = Agent(
    role="研究员",
    goal="...",
    llm="gpt-4o-mini",  # 研究用便宜模型
)

# 2. 只在关键环节用贵模型
writer = Agent(
    role="作家",
    goal="...",
    llm="claude-4-opus",  # 写作用好模型
)

# 3. 限制迭代次数
agent = Agent(
    max_iter=5,  # 默认15，按需降低
)

# 4. 限制并发
crew = Crew(
    max_rpm=10,  # 每分钟最多10个请求
)
```

---

## 十一、与其他框架对比

| 特性 | CrewAI | LangGraph | AutoGen | MAS Factory |
|------|--------|-----------|---------|-------------|
| 上手难度 | ⭐⭐ 简单 | ⭐⭐⭐⭐ 复杂 | ⭐⭐⭐ 中等 | ⭐⭐ 简单 |
| 灵活性 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 最高 | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中等 |
| 角色扮演 | ⭐⭐⭐⭐⭐ 最强 | ⭐⭐⭐ 一般 | ⭐⭐⭐⭐ 强 | ⭐⭐⭐⭐ 强 |
| 流程控制 | ⭐⭐⭐ 有限 | ⭐⭐⭐⭐⭐ 最强 | ⭐⭐⭐⭐ 强 | ⭐⭐⭐ 中等 |
| 社区活跃度 | ⭐⭐⭐⭐ 高 | ⭐⭐⭐⭐⭐ 最高 | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中等 |

> 📚 深入了解框架对比：[《Agent 编排框架对比》](../02-frameworks/agent-orchestration-comparison.md)

---

## 十二、总结

CrewAI 的核心就是三个概念：

```
Agent（智能体）= 角色 + 技能 + 工具
Task（任务）= 要做什么 + 谁来做 + 输出什么
Crew（团队）= Agent + Task + 流程
```

**快速上手清单**：
1. ✅ `pip install crewai crewai-tools`
2. ✅ 定义 2-3 个 Agent（写好 role、goal、backstory）
3. ✅ 定义对应的 Task（明确 description 和 expected_output）
4. ✅ 创建 Crew，选择 Sequential 或 Hierarchical
5. ✅ `crew.kickoff()` 启动

> 📚 **延伸阅读**：
> - [多智能体系统入门](../01-fundamentals/multi-agent-systems.md)
> - [LangGraph 编排详解](../02-frameworks/langgraph-agent-orchestration.md)
> - [MAS Factory 快速开始](../01-fundamentals/masfactory-quickstart.md)
