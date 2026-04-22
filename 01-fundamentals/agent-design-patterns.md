# 🏗️ Agent 设计模式大全 — 从单 Agent 到多 Agent 协作

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 架构设计模式 |
| **适用** | Agent 开发者、架构师 |
| **相关仓库** | [LangGraph Patterns](https://github.com/langchain-ai/langgraph), [AutoGen](https://github.com/microsoft/autogen), [CrewAI](https://github.com/crewAIInc/crewAI) |

---

## 🎯 一句话理解

> **不同的任务需要不同的 Agent 编排方式——就像不同场合需要不同的组织架构：一个人单干、领导带团队、流水线、还是各自为战再汇总。**

---

## 🧩 单 Agent 模式

### 1. Simple Reflection（自我反思）

Agent 执行任务后，自己评估结果，不满意就改进重做。

```
┌──────────────────────────────┐
│         用户请求              │
│             ↓                │
│    ┌──────────────┐          │
│    │   执行任务    │ ←──────┐ │
│    └──────┬───────┘        │ │
│           ↓                │ │
│    ┌──────────────┐        │ │
│    │   评估结果    │        │ │
│    └──────┬───────┘        │ │
│       ┌───┴───┐            │ │
│       ↓       ↓            │ │
│    满意？   不满意 ────────┘ │
│       ↓                     │
│    返回结果                  │
└──────────────────────────────┘
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 写作润色、代码优化、翻译改进 |
| **优点** | 简单，自我迭代提升质量 |
| **缺点** | 可能陷入循环，需要设定最大重试次数 |

```python
# 伪代码
def reflect_and_improve(task, max_iterations=3):
    result = agent.execute(task)
    for i in range(max_iterations):
        feedback = agent.evaluate(result, criteria=task.criteria)
        if feedback.is_satisfied:
            return result
        result = agent.improve(result, feedback)
    return result
```

### 2. ReAct（Reasoning + Acting）

Agent 交替进行"思考"和"行动"，像人一样推理后执行。

```
用户：北京明天天气怎么样？

Agent 思考（Thought）：我需要查天气，可以用 weather 工具
Agent 行动（Action）：weather(city="北京", date="明天")
工具返回：北京明天 晴 28°C
Agent 思考（Thought）：我已经得到天气信息了
Agent 回答：北京明天晴天，气温 28°C，适合出行。
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 需要工具调用的任务（搜索、计算、API） |
| **优点** | 可解释性强，推理过程透明 |
| **缺点** | 思考步骤多时 Token 消耗大 |

```python
def react_loop(query, max_steps=10):
    history = [{"role": "user", "content": query}]
    for step in range(max_steps):
        # 思考
        thought = agent.think(history)
        # 决定行动
        if thought.needs_tool:
            observation = tool.execute(thought.tool, thought.args)
            history.append({"role": "tool", "content": observation})
        else:
            return thought.final_answer
    return "达到最大步骤限制"
```

### 3. Plan-and-Execute（先规划后执行）

先制定完整计划，再逐步执行，遇到问题再调整计划。

```
┌──────────────────────────────────────┐
│           用户请求                    │
│               ↓                      │
│      ┌───────────────┐               │
│      │  制定计划      │               │
│      │  Step 1: ...  │               │
│      │  Step 2: ...  │               │
│      │  Step 3: ...  │               │
│      └───────┬───────┘               │
│              ↓                       │
│      ┌───────────────┐    ┌────────┐ │
│      │  执行 Step 1  │───→│ 复查   │ │
│      └───────┬───────┘    │ 计划   │ │
│              ↓           └────────┘ │
│      ┌───────────────┐               │
│      │  执行 Step 2  │               │
│      └───────┬───────┘               │
│              ↓                       │
│      ┌───────────────┐               │
│      │  执行 Step 3  │               │
│      └───────┬───────┘               │
│              ↓                       │
│         返回最终结果                  │
└──────────────────────────────────────┘
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 复杂多步骤任务（写报告、做研究、项目管理） |
| **优点** | 全局视角，步骤可复用，便于人审核 |
| **缺点** | 计划可能不完美，动态调整成本高 |

```python
def plan_and_execute(task):
    # Planner: 制定计划
    plan = planner.create_plan(task)
    # Executor: 逐步执行
    results = []
    for step in plan.steps:
        result = executor.execute(step)
        results.append(result)
        # Replanner: 根据结果调整后续计划
        if result.needs_replanning:
            plan = replanner.adjust(plan, results)
    return aggregator.combine(results)
```

---

## 🤝 多 Agent 模式

### 4. Router Agent（路由分发）

一个"前台"Agent 接收请求，分发给专业 Agent 处理。

```
                用户请求
                   ↓
           ┌───────────────┐
           │  Router Agent │
           │  (分类/路由)   │
           └──┬──┬──┬──┬───┘
              ↓  ↓  ↓  ↓
          ┌───┐┌──┐┌──┐┌──┐
          │代码││写作││翻译││搜索│
          │Agent│Agent│Agent│Agent│
          └───┘└──┘└──┘└──┘
              ↓  ↓  ↓  ↓
           汇总返回给用户
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 客服系统、多领域问答、工具选择 |
| **优点** | 专业分工，响应快 |
| **缺点** | Router 分类可能出错 |

```python
class RouterAgent:
    def __init__(self):
        self.agents = {
            "code": CodeAgent(),
            "writing": WritingAgent(),
            "translation": TranslationAgent(),
            "search": SearchAgent(),
        }

    async def handle(self, query):
        category = await self.classify(query)
        agent = self.agents[category]
        return await agent.handle(query)
```

### 5. Supervisor（监督者）

一个管理者 Agent 协调多个工作 Agent，决定谁做什么。

```
           ┌──────────────────┐
           │   Supervisor     │
           │  (管理者 Agent)  │
           └──┬──────────┬───┘
              ↓          ↓
      ┌──────────┐ ┌──────────┐
      │ Researcher│ │ Writer   │
      │ (研究员)  │ │ (写手)   │
      └──────────┘ └──────────┘
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 内容生产、研究项目、需要协调的任务 |
| **优点** | Supervisor 统筹全局，可以动态分配 |
| **缺点** | Supervisor 是单点，容易成为瓶颈 |

**对比 Router**：Router 是"前台接待"，只做分类不参与后续；Supervisor 是"项目经理"，全程参与协调。

### 6. Swarm / Delegate（群体协作）

Agent 之间可以互相转交任务（Handoff），像接力赛。

```
用户 → [客服 Agent] --handoff--> [技术 Agent] --handoff--> [退款 Agent]
                                                        ↓
                                                     返回结果
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 多步骤客服、工单处理、需要转交的场景 |
| **优点** | 灵活，Agent 自主决定何时转交 |
| **缺点** | 转交链可能过长，调试困难 |
| **代表** | [OpenAI Swarm](https://github.com/openai/swarm) |

```python
# Swarm 风格的 Handoff
async def customer_service_agent(messages):
    if user_wants_technical_help(messages):
        return handoff(technical_agent)  # 转交
    return answer(messages)
```

### 7. Sequential Pipeline（顺序流水线）

Agent 按固定顺序依次处理，像工厂流水线。

```
输入 → [Agent A] → [Agent B] → [Agent C] → 输出
       研究员       写手        编辑
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 内容创作（研究→起草→编辑）、数据处理管道 |
| **优点** | 简单可靠，步骤清晰 |
| **缺点** | 不灵活，任何一步卡住都阻塞后续 |

### 8. Parallel Fan-out（并行扇出）

多个 Agent 同时处理同一任务的不同部分，最后汇总。

```
                输入
        ┌───────┼───────┐
        ↓       ↓       ↓
   [Agent A] [Agent B] [Agent C]
   分析市场   分析竞品   分析趋势
        └───────┼───────┘
                ↓
            汇总输出
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 多维度分析、并行研究、数据并行处理 |
| **优点** | 速度快，覆盖全面 |
| **缺点** | Token 消耗大（每个 Agent 都要处理输入） |

### 9. Map-Reduce（映射归约）

并行处理（Map）→ 归纳合并（Reduce），处理大规模数据。

```
Map 阶段:
  文档1 → [Agent] → 摘要1
  文档2 → [Agent] → 摘要2
  文档3 → [Agent] → 摘要3
  ...

Reduce 阶段:
  摘要1, 摘要2, 摘要3 → [Agent] → 最终总结
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 大量文档总结、批量数据处理 |
| **优点** | 可水平扩展，处理量大 |
| **缺点** | 信息可能在 Reduce 阶段丢失 |

### 10. Hierarchical（层级结构）

多层级的 Agent 组织，高层管理低层。

```
        ┌──────────────┐
        │  CEO Agent   │
        └──┬────────┬──┘
           ↓        ↓
    ┌──────────┐ ┌──────────┐
    │ 研发总监  │ │ 市场总监  │
    └──┬───┬───┘ └──┬───┬───┘
       ↓   ↓        ↓   ↓
     前端  后端    运营  推广
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 大型项目、企业级 Agent 系统 |
| **优点** | 符合真实组织架构，可扩展 |
| **缺点** | 层级过多导致延迟，成本高 |

### 11. Mixture of Agents（混合体）

多个 Agent 同时思考，由"裁判"选择最佳答案。

```
           输入
    ┌──────┼──────┼──────┐
    ↓      ↓      ↓      ↓
 [Agent1] [Agent2] [Agent3] [Agent4]
    ↓      ↓      ↓      ↓
    └──────┼──────┼──────┘
           ↓
     ┌──────────┐
     │ Aggregator│
     │ (裁判)    │
     └─────┬────┘
           ↓
        最佳答案
```

| 项目 | 说明 |
|------|------|
| **适用场景** | 需要高质量输出的任务（诊断、决策） |
| **优点** | 多角度思考，质量高 |
| **缺点** | 成本是单 Agent 的 N 倍 |

---

## 🌳 选型决策树

```
需要多个 Agent 吗？
├── 否 → 单 Agent
│   ├── 需要自我改进？→ Reflection
│   ├── 需要调用工具？→ ReAct
│   └── 多步骤复杂任务？→ Plan-and-Execute
│
└── 是 → 多 Agent
    ├── 任务需要分类分发？→ Router
    ├── 需要协调管理？→ Supervisor
    ├── 任务可以并行？→ Parallel Fan-out / Map-Reduce
    ├── 固定处理顺序？→ Sequential Pipeline
    ├── Agent 之间要互相转交？→ Swarm/Delegate
    ├── 大型组织架构？→ Hierarchical
    └── 需要多角度选最佳？→ Mixture of Agents
```

---

## 📊 模式对比总结

| 模式 | 复杂度 | Agent 数 | 适用场景 | 成本 |
|------|--------|---------|---------|------|
| Reflection | ⭐ | 1 | 写作润色 | 低 |
| ReAct | ⭐⭐ | 1 | 工具调用 | 低 |
| Plan-and-Execute | ⭐⭐ | 1-2 | 复杂任务 | 中 |
| Router | ⭐⭐ | 2-10 | 客服/分发 | 中 |
| Supervisor | ⭐⭐⭐ | 3-10 | 协调任务 | 中高 |
| Swarm | ⭐⭐ | 2-10 | 转交流程 | 中 |
| Sequential | ⭐⭐ | 2-5 | 流水线 | 中 |
| Parallel Fan-out | ⭐⭐⭐ | 3-10 | 并行分析 | 高 |
| Map-Reduce | ⭐⭐⭐ | N+1 | 批量处理 | 高 |
| Hierarchical | ⭐⭐⭐⭐ | 5-50 | 企业级 | 很高 |
| Mixture of Agents | ⭐⭐⭐ | 3-10 | 高质量输出 | 高 |

---

## 📎 参考链接

| 资源 | 链接 |
|------|------|
| LangGraph Patterns | https://github.com/langchain-ai/langgraph |
| OpenAI Swarm | https://github.com/openai/swarm |
| AutoGen | https://github.com/microsoft/autogen |
| CrewAI | https://github.com/crewAIInc/crewAI |
| Mixture of Agents 论文 | https://arxiv.org/abs/2406.04692 |
| ReAct 论文 | https://arxiv.org/abs/2210.03629 |

---

*上一篇：[MCP 模型上下文协议](./mcp-model-context-protocol.md) | 下一篇：[Agent 编排框架对比](../02-frameworks/agent-orchestration-comparison.md)*
