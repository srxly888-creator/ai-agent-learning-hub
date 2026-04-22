# 🔄 LangGraph 深度解析 — 图结构编排 Agent 工作流

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | LangGraph 框架深度使用指南 |
| **适用** | Agent 开发者、AI 工程师、后端开发者 |
| **前置知识** | [什么是 AI Agent](../01-fundamentals/what-is-agent.md)、[Agent 设计模式](../01-fundamentals/agent-design-patterns.md) |
| **官方仓库** | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |

---

## 🎯 一句话理解

> **LangGraph 让你用"画流程图"的方式编排 Agent——节点是处理步骤，边是流转条件，你可以轻松实现条件分支、循环、人机协作等复杂逻辑。**

---

## ❓ 为什么需要 LangGraph？

如果你用过 LangChain，你可能遇到过这种困境：

```python
# LangChain 的 Chain 是线性的：
input → Step1 → Step2 → Step3 → output

# 但实际 Agent 需要的是：
# 1. 条件分支：如果搜索没结果 → 换个关键词重试
# 2. 循环：不断反思改进直到满意
# 3. 并行：同时搜索多个数据源
# 4. 人工介入：某些步骤需要人类确认

# 线性 Chain 搞不定这些 😅
```

**LangGraph 就是为了解决这些问题而生的**。它把 Agent 工作流建模成一个**有向图（Graph）**：

```
LangGraph 的核心理念：

节点 (Node) → 做什么（处理步骤）
边 (Edge)   → 去哪里（流转条件）
状态 (State) → 记住什么（共享数据）

就像画流程图一样来写 Agent！
```

---

## 🏗️ 核心概念

### 1. State（状态）

State 是整个图中所有节点**共享的数据**。每个节点都可以读取和修改状态。

```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    """定义 Agent 的共享状态"""
    # 对话消息列表（add_messages 会自动合并新消息）
    messages: Annotated[list, add_messages]
    
    # 当前步骤
    current_step: str
    
    # 搜索结果
    search_results: list[str]
    
    # 最终答案
    answer: str
    
    # 需要人工审核的标记
    needs_review: bool
    
    # 迭代次数
    iteration: int
```

### 2. Node（节点）

节点就是一个 Python 函数，接收当前状态，返回状态更新。

```python
def search_node(state: AgentState) -> dict:
    """搜索节点：根据用户问题搜索信息"""
    # 从状态中读取消息
    last_message = state["messages"][-1]
    query = last_message.content
    
    # 执行搜索
    results = search_engine.search(query)
    
    # 返回状态更新（会合并到当前状态）
    return {
        "search_results": results,
        "current_step": "answering"
    }


def answer_node(state: AgentState) -> dict:
    """回答节点：根据搜索结果生成答案"""
    messages = state["messages"]
    results = state["search_results"]
    
    # 用 LLM 生成答案
    prompt = f"根据以下搜索结果回答用户问题：\n{results}\n\n问题：{messages[-1].content}"
    answer = llm.generate(prompt)
    
    return {
        "answer": answer,
        "current_step": "done"
    }
```

### 3. Edge（边）

边定义了节点之间的**流转规则**。

```python
from langgraph.graph import StateGraph, START, END

# 创建图
graph = StateGraph(AgentState)

# 添加节点
graph.add_node("search", search_node)
graph.add_node("answer", answer_node)

# 添加边
graph.add_edge(START, "search")  # 起始 → 搜索
graph.add_edge("search", "answer")  # 搜索 → 回答
graph.add_edge("answer", END)  # 回答 → 结束
```

---

## 🚀 快速开始

### 安装

```bash
pip install langgraph langchain-openai
```

### 第一个 LangGraph Agent

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

# 定义节点
def chatbot(state: MessagesState):
    """简单的聊天节点"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 构建图
graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# 编译并运行
app = graph.compile()

# 使用
result = app.invoke({
    "messages": [("user", "你好！介绍一下你自己")]
})
print(result["messages"][-1].content)
```

---

## 🧩 条件路由（Conditional Routing）

这是 LangGraph 最强大的功能之一——根据条件决定下一步走哪条路。

```python
from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    messages: Annotated[list, add_messages]
    query_type: str  # "math" / "search" / "chat"

def classify_query(state: RouterState) -> dict:
    """分类用户的问题类型"""
    query = state["messages"][-1].content
    
    # 用 LLM 分类
    prompt = f"""判断以下问题的类型：
    - math: 数学计算
    - search: 需要搜索信息
    - chat: 普通聊天

    问题：{query}
    只返回类型（math/search/chat）"""
    
    query_type = llm.invoke(prompt).content.strip()
    return {"query_type": query_type}

def math_handler(state: RouterState) -> dict:
    """处理数学问题"""
    result = calculator(state["messages"][-1].content)
    return {"messages": [("assistant", f"计算结果：{result}")]}

def search_handler(state: RouterState) -> dict:
    """处理搜索问题"""
    results = web_search(state["messages"][-1].content)
    return {"messages": [("assistant", f"搜索结果：{results}")]}

def chat_handler(state: RouterState) -> dict:
    """处理普通聊天"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def route_query(state: RouterState) -> str:
    """路由函数：根据问题类型决定走哪条边"""
    return state["query_type"]

# 构建图
graph = StateGraph(RouterState)

# 添加节点
graph.add_node("classify", classify_query)
graph.add_node("math", math_handler)
graph.add_node("search", search_handler)
graph.add_node("chat", chat_handler)

# 添加边
graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_query,  # 路由函数
    {
        "math": "math",
        "search": "search",
        "chat": "chat"
    }
)
graph.add_edge("math", END)
graph.add_edge("search", END)
graph.add_edge("chat", END)

# 编译
app = graph.compile()

# 使用
result = app.invoke({"messages": [("user", "1+1等于几？")]})
# → classify 判定为 "math" → 走 math 节点
```

图的可视化：

```
        ┌──────────┐
START → │ classify │
        └────┬─────┘
             │ (路由函数)
        ┌────┼────────┐
        ↓    ↓        ↓
    ┌──────┐ ┌──────┐ ┌──────┐
    │ math │ │search│ │ chat │
    └──┬───┘ └──┬───┘ └──┬───┘
       ↓        ↓        ↓
      END      END      END
```

---

## 🔄 循环与迭代

LangGraph 天然支持循环——这是实现 Reflexion（自我反思）的关键。

```python
class ReflectionState(TypedDict):
    messages: Annotated[list, add_messages]
    draft: str          # 当前草稿
    feedback: str       # 反馈意见
    iteration: int      # 迭代次数
    max_iterations: int # 最大迭代次数

def writer(state: ReflectionState) -> dict:
    """写作节点：生成/改进草稿"""
    prompt = f"""
    请根据以下要求写一段内容：
    {state["messages"][-1].content}
    
    {f'之前的草稿：{state["draft"]}' if state.get("draft") else ''}
    {f'改进建议：{state["feedback"]}' if state.get("feedback") else ''}
    """
    
    draft = llm.invoke(prompt).content
    return {
        "draft": draft,
        "iteration": state.get("iteration", 0) + 1
    }

def reviewer(state: ReflectionState) -> dict:
    """审稿节点：评估草稿并给出反馈"""
    prompt = f"""
    请评估以下草稿的质量（1-10分）：
    {state["draft"]}
    
    如果分数低于8分，请给出具体的改进建议。
    如果分数8分及以上，回复"满意"。
    """
    
    feedback = llm.invoke(prompt).content
    return {"feedback": feedback}

def should_continue(state: ReflectionState) -> str:
    """判断是否需要继续迭代"""
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    if "满意" in state.get("feedback", ""):
        return "end"
    return "revise"

# 构建图
graph = StateGraph(ReflectionState)
graph.add_node("writer", writer)
graph.add_node("reviewer", reviewer)

graph.add_edge(START, "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "revise": "writer",  # 不满意 → 回到写作
        "end": END           # 满意 → 结束
    }
)

app = graph.compile()
```

图的可视化：

```
    START
      ↓
  ┌───────┐
  │ writer │ ←──────────┐
  └───┬───┘            │
      ↓                │
  ┌─────────┐          │
  │reviewer │          │
  └───┬─────┘          │
      ↓                │
  不满意？──是─────────┘
      │
      否
      ↓
     END
```

---

## 🤝 人机协作（Human-in-the-Loop）

在许多实际场景中，某些步骤需要人类来确认或修改。LangGraph 通过 **interrupt** 机制实现这一点。

```python
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver

class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    action_plan: str
    approved: bool

def plan_action(state: ApprovalState) -> dict:
    """制定行动方案"""
    query = state["messages"][-1].content
    
    plan = llm.invoke(f"""
    用户请求：{query}
    请制定一个执行方案。
    """).content
    
    return {"action_plan": plan}

def human_review(state: ApprovalState) -> dict:
    """等待人类审核"""
    # ⚡ 关键：这里会暂停执行，等待人类输入
    approval = interrupt({
        "question": "请审核以下方案：",
        "plan": state["action_plan"],
        "options": ["approve", "reject", "modify"]
    })
    
    return {"approved": approval == "approve"}

def execute_action(state: ApprovalState) -> dict:
    """执行被批准的方案"""
    if not state["approved"]:
        return {"messages": [("assistant", "方案已被拒绝，请告诉我您的要求。")]}
    
    # 执行方案...
    result = execute(state["action_plan"])
    return {"messages": [("assistant", f"方案已执行：{result}")]}

def review_result(state: ApprovalState) -> str:
    """审核后的路由"""
    if state.get("approved"):
        return "execute"
    return "reject"

# 构建图（使用 MemorySaver 支持暂停/恢复）
graph = StateGraph(ApprovalState)
graph.add_node("plan", plan_action)
graph.add_node("review", human_review)
graph.add_node("execute", execute_action)

graph.add_edge(START, "plan")
graph.add_edge("plan", "review")
graph.add_conditional_edges("review", review_result, {
    "execute": "execute",
    "reject": END
})
graph.add_edge("execute", END)

# 编译（必须使用 checkpointer）
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# 使用
config = {"configurable": {"thread_id": "session-1"}}

# 第一次运行：会在 human_review 处暂停
result = app.invoke(
    {"messages": [("user", "帮我删除所有旧日志文件")]},
    config=config
)
# → 执行到 human_review，暂停等待审核

# 人类审核后恢复
result = app.invoke(
    Command(resume="approve"),  # 批准方案
    config=config
)
# → 继续执行 execute_action
```

---

## 📊 状态机模式

LangGraph 可以轻松实现**有限状态机（FSM）**，适合客服机器人、工作流引擎等场景。

```python
class CustomerServiceState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str       # "greeting" / "complaint" / "refund" / "unknown"
    order_id: str
    resolved: bool

def detect_intent(state: CustomerServiceState) -> dict:
    """检测用户意图"""
    query = state["messages"][-1].content
    intent = llm.invoke(f"""
    分类用户意图：greeting / complaint / refund / unknown
    用户说：{query}
    只返回类型。
    """).content.strip()
    return {"intent": intent}

def handle_greeting(state: CustomerServiceState) -> dict:
    return {"messages": [("assistant", "你好！有什么可以帮你的？")]}

def handle_complaint(state: CustomerServiceState) -> dict:
    return {"messages": [("assistant", "很抱歉给您带来不便，请描述一下您的问题。")]}

def handle_refund(state: CustomerServiceState) -> dict:
    return {"messages": [("assistant", "好的，请提供您的订单号。")]}

def route_intent(state: CustomerServiceState) -> str:
    intent_map = {
        "greeting": "greeting",
        "complaint": "complaint",
        "refund": "refund"
    }
    return intent_map.get(state["intent"], "unknown")

# 构建状态机
graph = StateGraph(CustomerServiceState)
graph.add_node("detect", detect_intent)
graph.add_node("greeting", handle_greeting)
graph.add_node("complaint", handle_complaint)
graph.add_node("refund", handle_refund)

graph.add_edge(START, "detect")
graph.add_conditional_edges("detect", route_intent, {
    "greeting": "greeting",
    "complaint": "complaint",
    "refund": "refund",
    "unknown": END
})
graph.add_edge("greeting", END)
graph.add_edge("complaint", END)
graph.add_edge("refund", END)
```

---

## 🌟 LangGraph vs 其他框架

| 特性 | LangGraph | LangChain Chain | CrewAI | AutoGen |
|------|-----------|----------------|--------|---------|
| **编排方式** | 图结构 | 线性链 | 角色协作 | 对话式 |
| **条件路由** | ✅ 原生支持 | ❌ 需要变通 | ✅ 支持 | ✅ 支持 |
| **循环** | ✅ 原生支持 | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| **人机协作** | ✅ interrupt | ❌ 不支持 | ❌ 有限 | ❌ 有限 |
| **状态管理** | ✅ 共享状态 | ❌ 有限 | ❌ 独立 | ❌ 共享消息 |
| **可视化** | ✅ 自动生成图 | ❌ 无 | ❌ 无 | ❌ 无 |
| **学习曲线** | 中等 | 低 | 低 | 中等 |
| **灵活性** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🛠️ 实战：构建一个研究助手

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState, add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated

class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    topic: str
    search_results: list[str]
    outline: str
    draft: str
    iteration: int

def search_web(state: ResearchState) -> dict:
    """搜索相关资料"""
    topic = state["topic"]
    results = []
    
    # 搜索多个关键词
    keywords = [
        f"{topic} 最新研究",
        f"{topic} 综述",
        f"{topic} 技术方案"
    ]
    for kw in keywords:
        results.extend(web_search(kw))
    
    return {
        "search_results": results,
        "messages": [("assistant", f"已搜索到 {len(results)} 条相关资料")]
    }

def create_outline(state: ResearchState) -> dict:
    """生成大纲"""
    context = "\n".join(state["search_results"][:5])
    outline = llm.invoke(f"""
    主题：{state["topic"]}
    参考资料：{context}
    
    请生成一个详细的文章大纲。
    """).content
    
    return {
        "outline": outline,
        "messages": [("assistant", f"大纲已生成：\n{outline}")]
    }

def write_draft(state: ResearchState) -> dict:
    """根据大纲写草稿"""
    draft = llm.invoke(f"""
    主题：{state["topic"]}
    大纲：{state["outline"]}
    参考资料：{chr(10).join(state["search_results"][:10])}
    
    请根据大纲写一篇完整的文章。
    """).content
    
    return {
        "draft": draft,
        "iteration": state.get("iteration", 0) + 1
    }

def review_draft(state: ResearchState) -> dict:
    """审阅草稿"""
    feedback = llm.invoke(f"""
    请审阅以下文章草稿，给出评分（1-10）和改进建议：
    
    {state["draft"]}
    """).content
    
    return {"messages": [("assistant", f"审阅结果：{feedback}")]}

def should_continue(state: ResearchState) -> str:
    if state.get("iteration", 0) >= 3:
        return "done"
    return "revise"

# 构建图
graph = StateGraph(ResearchState)
graph.add_node("search", search_web)
graph.add_node("outline", create_outline)
graph.add_node("draft", write_draft)
graph.add_node("review", review_draft)

graph.add_edge(START, "search")
graph.add_edge("search", "outline")
graph.add_edge("outline", "draft")
graph.add_edge("draft", "review")
graph.add_conditional_edges("review", should_continue, {
    "revise": "draft",
    "done": END
})

app = graph.compile(checkpointer=MemorySaver())

# 运行
result = app.invoke({
    "messages": [("user", "帮我研究 AI Agent 的记忆系统")],
    "topic": "AI Agent 记忆系统"
})
```

---

## 💡 最佳实践

### 1. 状态设计原则
```
✅ 好的状态设计：
- 每个字段都有明确的用途
- 字段之间没有冗余
- 使用 TypedDict 获得类型提示

❌ 不好的状态设计：
- 把所有东西塞进一个字符串
- 字段之间有循环依赖
- 状态无限增长（需要清理机制）
```

### 2. 节点粒度
```
太粗 → 一个节点做太多事，难以调试
太细 → 图太复杂，维护困难

建议：一个节点做一件事，命名清晰
```

### 3. 错误处理
```python
def robust_node(state: MyState) -> dict:
    try:
        # 正常逻辑
        result = do_something(state)
        return {"data": result}
    except Exception as e:
        # 错误处理：返回错误信息到状态
        return {"error": str(e), "messages": [("assistant", f"出错了：{e}")]}
```

### 4. 使用 Checkpointer
```python
# 开发时用内存 checkpointer
checkpointer = MemorySaver()

# 生产环境用持久化 checkpointer
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string("postgresql://...")

# 编译时传入
app = graph.compile(checkpointer=checkpointer)
```

---

## 📚 总结

```
LangGraph 核心概念：

State（状态）  → 所有节点共享的数据
Node（节点）   → 处理步骤（Python 函数）
Edge（边）     → 流转规则
Conditional   → 条件分支
Loop          → 循环迭代
Interrupt     → 人机协作
Checkpoint    → 状态持久化

适用场景：
✅ 需要条件分支的复杂工作流
✅ 需要循环迭代（如反思改进）
✅ 需要人工审核确认
✅ 需要状态持久化和恢复
✅ 多步骤的自动化流程

不适合：
❌ 简单的线性任务（用 LangChain Chain 就够了）
❌ 纯对话场景（不需要图结构）
```

> 💡 **核心要点**：LangGraph 的价值在于把"流程控制"从代码逻辑中解放出来，变成可视化的图结构。这让复杂的 Agent 工作流变得可理解、可调试、可维护。

---

## 🔗 相关链接

- [Agent 设计模式](../01-fundamentals/agent-design-patterns.md)
- [Agent 编排框架对比](./agent-orchestration-comparison.md)
- [A2A 协议](./a2a-agent-to-agent-protocol.md)
- [工具使用与规划](../01-fundamentals/tool-use-and-planning.md)
- [官方文档](https://langchain-ai.github.io/langgraph/)
