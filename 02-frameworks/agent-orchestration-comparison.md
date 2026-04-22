# 🔄 Agent 编排框架对比 — LangGraph vs CrewAI vs AutoGen vs Swarm

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | 主流 AI Agent 编排框架横向对比 |
| **更新时间** | 2026 年 4 月 |
| **涵盖框架** | LangGraph, CrewAI, AutoGen, OpenAI Swarm, MAS Factory |

---

## 🎯 为什么需要编排框架？

写单个 Agent 调一次 API 就行，但当你需要：
- 多个 Agent 协作
- 复杂的工作流（条件分支、循环、人工审批）
- 状态管理和持久化
- 可观测性和调试

手动管理这些会变得非常痛苦。编排框架就是来解决这些问题的。

```
手动编排的痛苦:
  ❌ 自己管理对话历史
  ❌ 自己处理错误重试
  ❌ 自己实现 Agent 间通信
  ❌ 自己做状态持久化
  ❌ 自己加日志和监控

用框架:
  ✅ 内置状态管理
  ✅ 内置错误处理
  ✅ 标准化 Agent 接口
  ✅ 可视化调试
  ✅ 一键部署
```

---

## 1. LangGraph

> **图 + 状态 = 万能工作流引擎**

| 项目 | 内容 |
|------|------|
| **开发者** | LangChain 团队 |
| **GitHub** | https://github.com/langchain-ai/langgraph |
| **Stars** | 10k+ |
| **语言** | Python, TypeScript |
| **核心概念** | State Graph（状态图） |

### 架构

```
┌─────────────────────────────────────┐
│           LangGraph Graph           │
│                                      │
│  ┌─────────┐     ┌─────────────┐   │
│  │  Node A  │────→│   Node B    │   │
│  │ (Agent)  │     │  (Tool)     │   │
│  └─────────┘     └──────┬──────┘   │
│       ↑                  ↓          │
│  ┌────┴─────┐     ┌─────────────┐   │
│  │Condition │←────│   Node C    │   │
│  │ (路由)    │     │  (Router)   │   │
│  └──────────┘     └─────────────┘   │
│                                      │
│  State: 共享状态对象贯穿所有节点      │
└─────────────────────────────────────┘
```

### 代码示例

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 定义工具
def search(query: str) -> str:
    return f"搜索结果: {query}"

def calculator(expression: str) -> str:
    return str(eval(expression))

tools = [search, calculator]
tool_node = ToolNode(tools)

# 定义图
graph = StateGraph(MessagesState)

# 添加节点
graph.add_node("agent", call_model)      # LLM 节点
graph.add_node("tools", tool_node)       # 工具节点

# 添加边
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    "end": END,
})
graph.add_edge("tools", "agent")         # 工具执行后回到 Agent

app = graph.compile()
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 最灵活，能表达任意工作流 | 学习曲线陡峭 |
| 内置状态管理和持久化 | 概念多（Node, Edge, State） |
| LangChain 生态完整 | 过度工程化（简单任务太重） |
| 可视化调试（LangSmith） | 依赖 LangChain |

### 适用场景

- ✅ 复杂条件分支工作流
- ✅ 需要 Human-in-the-loop
- ✅ 长时间运行的多步任务
- ✅ 已在使用 LangChain 的项目

---

## 2. CrewAI

> **角色扮演式多 Agent 协作**

| 项目 | 内容 |
|------|------|
| **开发者** | CrewAI Inc. |
| **GitHub** | https://github.com/crewAIInc/crewAI |
| **Stars** | 30k+ |
| **语言** | Python |
| **核心概念** | Crew + Agent + Task |

### 架构

```
┌─────────────────────────────┐
│           Crew              │
│  ┌───────┐  ┌───────────┐  │
│  │Researcher│  │  Writer  │  │
│  │ 研究员   │→│  写手     │  │
│  └───────┘  └───────────┘  │
│       Tasks     Tasks       │
│  ┌───────┐  ┌───────────┐  │
│  │ Editor │  │ Reviewer  │  │
│  │ 编辑   │→│  审稿人   │  │
│  └───────┘  └───────────┘  │
└─────────────────────────────┘
```

### 代码示例

```python
from crewai import Agent, Task, Crew, Process

# 定义 Agent
researcher = Agent(
    role="高级研究员",
    goal="深入调研 AI Agent 领域最新进展",
    backstory="你是一位经验丰富的技术研究员，擅长信息搜集和分析",
    tools=[search_tool, web_scraper],
    llm="gpt-4o",
)

writer = Agent(
    role="技术写手",
    goal="将研究结果转化为通俗易懂的文章",
    backstory="你是一位优秀的技术作者，擅长把复杂概念讲清楚",
    llm="gpt-4o",
)

# 定义 Task
research_task = Task(
    description="调研 2026 年 AI Agent 框架的最新发展",
    expected_output="一份 500 字的研究报告",
    agent=researcher,
)

writing_task = Task(
    description="基于研究报告写一篇科普文章",
    expected_output="一篇 1000 字的中文文章",
    agent=writer,
    context=[research_task],  # 依赖研究任务
)

# 组建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # 顺序执行
)

result = crew.kickoff()
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 上手简单，概念直观 | 灵活性不如 LangGraph |
| 角色扮演方式易理解 | 复杂工作流难以表达 |
| 内置记忆和工具 | 社区资源不如 LangChain |
| 适合内容生产 | 自定义程度有限 |

### 适用场景

- ✅ 内容创作流水线
- ✅ 角色明确的协作任务
- ✅ 快速原型验证
- ❌ 复杂条件分支
- ❌ 需要精细控制的工作流

---

## 3. AutoGen

> **微软出品，对话式多 Agent 框架**

| 项目 | 内容 |
|------|------|
| **开发者** | Microsoft Research |
| **GitHub** | https://github.com/microsoft/autogen |
| **Stars** | 40k+ |
| **语言** | Python, .NET |
| **核心概念** | Agent + Conversation |

### 架构

```
┌─────────────────────────────────────┐
│        AutoGen Conversation          │
│                                      │
│  User ──→ Assistant ──→ User         │
│    ↑         ↓                       │
│    └── GroupChat ←── Assistant      │
│              ↕                       │
│         Assistant B                  │
└─────────────────────────────────────┘
```

### 代码示例

```python
import autogen

# 配置 LLM
config_list = [{"model": "gpt-4o", "api_key": "sk-xxx"}]
llm_config = {"config_list": config_list}

# 创建 Agent
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # 不需要人工输入
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="写一个 Python 脚本分析 CSV 数据",
)
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 微软背书，维护有保障 | API 变动频繁（v0.2→v0.4 大改） |
| 内置代码执行环境 | 文档有时跟不上版本 |
| GroupChat 支持好 | 概念较多 |
| 研究级质量 | 生产级工具链不如 LangGraph |

### 适用场景

- ✅ 研究原型
- ✅ 代码生成 + 执行
- ✅ 多 Agent 对话协作
- ✅ 对话式任务

---

## 4. OpenAI Swarm

> **极简多 Agent 切换框架**

| 项目 | 内容 |
|------|------|
| **开发者** | OpenAI |
| **GitHub** | https://github.com/openai/swarm |
| **Stars** | 15k+ |
| **语言** | Python |
| **核心概念** | Agent + Handoff |
| **状态** | ⚠️ 实验性项目，OpenAI 推荐转向 Agents SDK |

### 架构

```
用户 → [Sales Agent] --handoff--> [Tech Support] --handoff--> [Billing]
                                                                    ↓
                                                                 回复用户
```

### 代码示例

```python
from swarm import Swarm, Agent

client = Swarm()

def transfer_to_technical(context):
    return technical_agent

sales_agent = Agent(
    name="Sales Agent",
    instructions="你是销售代表，回答产品相关问题。技术问题转交技术支持。",
    functions=[transfer_to_technical],
)

technical_agent = Agent(
    name="Technical Support",
    instructions="你是技术支持工程师，帮助解决技术问题。",
)

messages = [{"role": "user", "content": "你们的 API 怎么调用？"}]
response = client.run(agent=sales_agent, messages=messages)
print(response.messages[-1]["content"])
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 极简 API，5 分钟上手 | 功能太简单，不适合复杂场景 |
| Handoff 概念优雅 | 无状态管理 |
| 官方出品 | 无持久化 |
| 零依赖 | ⚠️ 实验性，不再积极维护 |

### 适用场景

- ✅ 简单的 Agent 切换/转交
- ✅ 客服路由
- ❌ 复杂工作流
- ❌ 需要状态持久化

---

## 5. MAS Factory

> **仓库自研框架：Session + Capability + Policy**

| 项目 | 内容 |
|------|------|
| **开发者** | srxly888-creator |
| **核心概念** | Session（会话）, Capability（能力）, Policy（策略） |

详见本仓库 `02-frameworks/mas-factory.md`

---

## 📊 全面对比

| 特性 | LangGraph | CrewAI | AutoGen | Swarm | MAS Factory |
|------|-----------|--------|---------|-------|-------------|
| **架构** | 图/状态 | 角色/任务 | 对话 | Handoff | Session/Policy |
| **学习曲线** | 陡峭 | 简单 | 中等 | 极简 | 中等 |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **多 Agent** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **状态管理** | ✅ 内置 | ⚠️ 有限 | ⚠️ 有限 | ❌ | ✅ |
| **持久化** | ✅ 内置 | ❌ | ⚠️ | ❌ | ✅ |
| **可视化** | ✅ LangSmith | ⚠️ | ⚠️ | ❌ | ⚠️ |
| **代码执行** | ✅ | ❌ | ✅ 内置 | ❌ | ⚠️ |
| **Human-in-loop** | ✅ | ⚠️ | ✅ | ❌ | ✅ |
| **MCP 支持** | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ |
| **生产就绪** | ✅ | ✅ | ⚠️ | ❌ | ⚠️ |
| **Stars** | 10k+ | 30k+ | 40k+ | 15k+ | - |

---

## 🎯 选型建议

```
你的需求是什么？

├── 简单 Agent 切换 → OpenAI Swarm（或 Agents SDK）
├── 角色协作/内容生产 → CrewAI
├── 对话式/代码执行 → AutoGen
├── 复杂工作流/生产级 → LangGraph
├── 自研 Agent 底座 → MAS Factory
└── 不知道选什么 → 先试 CrewAI（最易上手）
```

| 场景 | 推荐 | 原因 |
|------|------|------|
| 快速原型 | CrewAI | 5 分钟上手 |
| 生产工作流 | LangGraph | 最灵活，最成熟 |
| 学术研究 | AutoGen | 微软背书，论文多 |
| 客服系统 | Swarm/Agents SDK | Handoff 天然适合 |
| 内容创作 | CrewAI | 角色概念契合 |
| 数据分析流水线 | LangGraph | 条件分支灵活 |
| 已有 LangChain 项目 | LangGraph | 无缝集成 |

---

## 📎 参考链接

| 资源 | 链接 |
|------|------|
| LangGraph 文档 | https://langchain-ai.github.io/langgraph/ |
| LangGraph GitHub | https://github.com/langchain-ai/langgraph |
| CrewAI 文档 | https://docs.crewai.com |
| CrewAI GitHub | https://github.com/crewAIInc/crewAI |
| AutoGen 文档 | https://microsoft.github.io/autogen/ |
| AutoGen GitHub | https://github.com/microsoft/autogen |
| Swarm GitHub | https://github.com/openai/swarm |
| MAS Factory | 见本仓库 `02-frameworks/mas-factory.md` |

---

*上一篇：[Agent 设计模式大全](../01-fundamentals/agent-design-patterns.md) | 下一篇：[A2A 协议](./a2a-agent-to-agent-protocol.md)*
