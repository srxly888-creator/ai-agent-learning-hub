# 🛠️ 工具使用与规划能力 — Agent 如何"思考"使用工具？

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 的推理策略与工具使用 |
| **适用** | Agent 开发者、AI 工程师、算法爱好者 |
| **前置知识** | [什么是 AI Agent](./what-is-agent.md)、[Function Calling](./function-calling.md) |

---

## 🎯 一句话理解

> **Agent 和普通 ChatGPT 最大的区别，就是它能"思考"后使用工具。就像你不仅会回答问题，还会上网查资料、用计算器算数、打开地图导航——Agent 也能，关键在于它怎么"想"。**

---

## 🤔 从"对话"到"行动"

普通的大模型聊天是这样的：

```
用户：北京到上海的高铁要多久？
AI：大约需要4-6个小时...（凭记忆回答，可能不准确）
```

Agent 是这样的：

```
用户：北京到上海的高铁要多久？

Agent 思考：用户问高铁时长，我需要查一下实时信息
Agent 行动：调用 search_train("北京", "上海")
工具返回：最快 G1次 4小时18分
Agent 思考：拿到结果了，可以回答了
Agent 回答：北京到上海最快的高铁是G1次，大约4小时18分钟🚄
```

**区别就在"思考"和"行动"的循环**——Agent 不是直接回答，而是先想想该用什么工具、用完工具再回答。

---

## 🧠 核心推理策略

### 策略一：ReAct（Reasoning + Acting）

**ReAct** 是最经典的 Agent 推理策略，让模型交替进行"推理"和"行动"。

```
ReAct 循环：
┌─────────────┐
│   用户问题   │
└──────┬──────┘
       ↓
┌──────────────┐
│  思考 (Thought) │ ← 分析问题，决定下一步
└──────┬───────┘
       ↓
┌──────────────┐
│  行动 (Action)  │ ← 调用工具
└──────┬───────┘
       ↓
┌──────────────┐
│  观察 (Observation)│ ← 工具返回结果
└──────┬────────┘
       ↓
   需要更多步骤？
   ├─ 是 → 回到"思考"
   └─ 否 → 输出最终答案
```

**实际例子**：

```
用户：帮我查一下 Python 的 list.sort() 和 sorted() 有什么区别？

Thought 1: 用户问 Python 两个排序方法的区别，我需要搜索相关信息
Action 1: search("Python list.sort() vs sorted() difference")
Observation 1: list.sort() 是原地排序，返回 None；sorted() 返回新列表...

Thought 2: 搜索结果提供了基本信息，但我应该确认一下性能差异
Action 2: search("Python sort vs sorted performance benchmark")
Observation 2: sorted() 通常比 list.sort() 稍慢，因为要创建新列表...

Thought 3: 我已经收集了足够的信息来回答这个问题
Answer: list.sort() 和 sorted() 的主要区别：
1. list.sort() 原地排序，修改原列表，返回 None
2. sorted() 返回新列表，不修改原列表
3. 性能上 list.sort() 略快...
```

**代码实现**：

```python
def react_agent(question, tools, llm, max_steps=5):
    """
    ReAct Agent 的核心循环
    
    参数：
    - question: 用户问题
    - tools: 可用工具字典 {"tool_name": tool_function}
    - llm: 大语言模型
    - max_steps: 最大推理步骤
    """
    # 构建 ReAct 提示词
    prompt = f"""你是一个能使用工具来解决问题的助手。

可用工具：
{chr(10).join(f'- {name}: {func.__doc__}' for name, func in tools.items())}

请用以下格式回答：
Thought: 你的思考过程
Action: 工具名(参数)
或者
Answer: 最终答案

用户问题：{question}"""

    history = [{"role": "user", "content": prompt}]
    
    for step in range(max_steps):
        response = llm.chat(history)
        history.append({"role": "assistant", "content": response})
        
        # 解析 Agent 的输出
        if response.startswith("Answer:"):
            return response  # 最终答案
        
        if response.startswith("Action:"):
            # 解析工具调用
            tool_name, args = parse_action(response)
            if tool_name in tools:
                # 执行工具
                result = tools[tool_name](**args)
                # 把结果反馈给 Agent
                history.append({
                    "role": "user", 
                    "content": f"Observation: {result}"
                })
    
    return "抱歉，我无法在有限步骤内解决这个问题。"
```

**ReAct 的优缺点**：

| 项目 | 说明 |
|------|------|
| ✅ 优点 | 可解释性强（能看到思考过程）、灵活、容易调试 |
| ❌ 缺点 | Token 消耗大（每步都要写 Thought）、可能走弯路 |

---

### 策略二：Plan-and-Execute（先规划再执行）

与其一步一步"边想边做"，不如**先制定完整计划，再按计划执行**。

```
Plan-and-Execute 流程：
┌──────────────┐
│   用户问题    │
└──────┬───────┘
       ↓
┌──────────────────────────────┐
│  📋 制定计划（Planner）        │
│  Step 1: 搜索相关资料         │
│  Step 2: 整理关键信息          │
│  Step 3: 对比分析             │
│  Step 4: 生成最终报告         │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  ⚡ 逐步执行（Executor）       │
│  执行 Step 1 → 得到结果       │
│  执行 Step 2 → 得到结果       │
│  ...                         │
│  执行 Step N → 得到结果       │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  🔄 可能需要重新规划          │
│  如果某步失败 → 调整计划       │
└──────────────────────────────┘
```

**实际例子**：

```
用户：帮我规划一个3天的东京旅行

Planner:
计划如下：
Step 1: 搜索东京必去景点
Step 2: 搜索东京美食推荐
Step 3: 搜索东京交通攻略
Step 4: 根据景点位置规划路线
Step 5: 整合成3天行程

Executor:
执行 Step 1: search("东京必去景点 2024")
  → 浅草寺、秋叶原、涩谷、新宿、明治神宫...
执行 Step 2: search("东京美食推荐")
  → 寿司、拉面、烧肉、天妇罗...
执行 Step 3: search("东京交通攻略")
  → 购买 Suica 卡、JR Pass...
执行 Step 4: 按区域规划路线
  → Day1 浅草+秋叶原（东京东部）
  → Day2 涩谷+新宿（东京西部）
  → Day3 明治神宫+原宿+购物
执行 Step 5: 生成完整行程
```

**代码实现**：

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class PlanAndExecuteAgent:
    def __init__(self, tools):
        self.planner = ChatOpenAI(model="gpt-4o", temperature=0)
        self.executor = ChatOpenAI(model="gpt-4o", temperature=0)
        self.tools = tools
    
    def plan(self, question):
        """第一步：制定计划"""
        tool_list = "\n".join(f"- {name}: {desc}" for name, desc in self.tools.items())
        
        prompt = f"""用户问题：{question}

可用工具：{tool_list}

请制定一个分步执行计划。每步说明：
1. 要做什么
2. 用什么工具
3. 预期结果

格式：
Step 1: [描述] → 使用 [工具名]
Step 2: [描述] → 使用 [工具名]
..."""
        
        return self.planner.predict(prompt)
    
    def execute_step(self, step, previous_results=""):
        """第二步：执行单个步骤"""
        prompt = f"""执行以下步骤：

{step}

之前的执行结果：
{previous_results}

请执行此步骤，输出结果。"""
        
        return self.executor.predict(prompt)
    
    def run(self, question):
        """完整流程"""
        # 1. 制定计划
        plan = self.plan(question)
        print(f"📋 计划：\n{plan}\n")
        
        # 2. 逐步执行
        results = []
        steps = plan.strip().split("Step")[1:]  # 分割步骤
        
        for i, step in enumerate(steps):
            step_text = f"Step {step}"
            result = self.execute_step(step_text, "\n".join(results))
            results.append(f"Step {i+1} 结果: {result}")
            print(f"✅ Step {i+1} 完成: {result[:100]}...")
        
        # 3. 综合结果
        return self.synthesize(question, results)
```

**对比 ReAct**：

| 维度 | ReAct | Plan-and-Execute |
|------|-------|-----------------|
| **策略** | 边想边做 | 先想后做 |
| **全局观** | 弱（可能走弯路） | 强（整体规划） |
| **灵活性** | 高（随时调整） | 中（需要重新规划） |
| **Token 消耗** | 中等 | 较高（规划也需要 Token） |
| **适合场景** | 简单~中等任务 | 复杂多步任务 |

---

### 策略三：Reflexion（反思改进）

Agent 执行完任务后，**反思自己的表现**，如果做得不好就改进重做。

```
Reflexion 循环：
┌──────────────┐
│   执行任务    │
└──────┬───────┘
       ↓
┌──────────────┐
│  评估结果     │
└──────┬───────┘
       ↓
   结果满意？
   ├─ 是 → 输出结果 ✅
   └─ 否 → 反思哪里做得不好
              ↓
        生成改进策略
              ↓
        重新执行 → 回到"评估结果"
```

**实际例子**：

```
任务：写一个 Python 快速排序

第一轮执行：
def quicksort(arr):
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)

反思：这个实现有问题！
1. 没有处理空列表的情况（会无限递归）
2. 没有处理重复元素（等于 pivot 的元素会丢失）
3. 性能不是最优的（创建了太多临时列表）

改进策略：
1. 添加 base case
2. 使用 in-place 排序减少内存使用
3. 用三路分区处理重复元素

第二轮执行（改进版）：
def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)
    return arr

评估：✅ 正确！base case 处理了，支持重复元素，in-place 排序
```

**代码实现**：

```python
def reflexion_agent(task, executor, evaluator, max_attempts=3):
    """
    Reflexion Agent：自我反思和改进
    
    参数：
    - task: 任务描述
    - executor: 执行函数
    - evaluator: 评估函数（返回分数和反馈）
    - max_attempts: 最大尝试次数
    """
    history = []  # 记录历史尝试
    
    for attempt in range(max_attempts):
        # 执行任务（如果有历史，把之前的反思也传入）
        result = executor(task, previous_attempts=history)
        
        # 评估结果
        score, feedback = evaluator(result, task)
        
        print(f"尝试 {attempt + 1}: 得分 {score}/10")
        print(f"反馈: {feedback}")
        
        if score >= 8:  # 满意阈值
            print("✅ 结果满意！")
            return result
        
        # 反思并记录
        reflection = {
            "attempt": attempt + 1,
            "result": result,
            "score": score,
            "feedback": feedback
        }
        history.append(reflection)
    
    # 返回最佳结果
    best = max(history, key=lambda x: x["score"])
    print(f"⚠️ 达到最大尝试次数，返回最佳结果（得分 {best['score']}/10）")
    return best["result"]


# 评估函数示例
def code_evaluator(code, task):
    """评估代码质量"""
    criteria = []
    
    # 检查是否有 base case
    if "if" in code and "return" in code:
        criteria.append(("边界处理", True, "有条件判断和返回"))
    else:
        criteria.append(("边界处理", False, "缺少边界条件处理"))
    
    # 检查是否有递归终止
    if "return" in code.split("def")[1] if "def" in code else False:
        criteria.append(("终止条件", True, "有返回值"))
    else:
        criteria.append(("终止条件", False, "可能缺少递归终止"))
    
    score = sum(1 for _, passed, _ in criteria if passed) / len(criteria) * 10
    feedback = "\n".join(f"- {name}: {'✅' if passed else '❌'} {comment}" 
                        for name, passed, comment in criteria)
    
    return score, feedback
```

---

### 策略四：Function Calling（函数调用）

这是目前最主流的工具使用方式，模型直接输出结构化的函数调用，无需手动解析。

```python
import openai

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网获取信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            }
        }
    }
]

# Agent 循环
messages = [{"role": "user", "content": "北京和上海今天哪个更热？"}]

while True:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
    
    choice = response.choices[0]
    
    if choice.finish_reason == "tool_calls":
        # Agent 想调用工具，执行并返回结果
        for tool_call in choice.message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # 执行对应的工具
            result = execute_tool(function_name, function_args)
            
            # 把工具结果反馈给 Agent
            messages.append(choice.message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
    else:
        # Agent 给出了最终回答
        print(choice.message.content)
        break
```

> 📖 Function Calling 的更多细节请看 [Function Calling 详解](./function-calling.md)

---

## 🔄 策略选择指南

不同场景适合不同策略：

```
简单问答 → 直接回答（不需要工具）
需要查信息 → ReAct（边想边查）
复杂多步任务 → Plan-and-Execute（先规划后执行）
需要高质量输出 → Reflexion（做完反思改进）
精确工具调用 → Function Calling（结构化调用）
```

| 场景 | 推荐策略 | 原因 |
|------|---------|------|
| 天气查询 | ReAct / Function Calling | 简单的工具调用 |
| 旅行规划 | Plan-and-Execute | 多步骤、有依赖关系 |
| 代码生成 | Reflexion | 需要多次迭代改进 |
| 数据分析 | Plan-and-Execute + Reflexion | 先规划分析步骤，再优化 |
| 客服问答 | Function Calling | 查询数据库、调用API |

---

## 🛠️ 实战：构建一个多功能 Agent

```python
import json
from datetime import datetime

class SmartAgent:
    """
    综合 Agent：支持 ReAct + Function Calling
    """
    
    def __init__(self, tools):
        self.tools = tools
        self.tool_schemas = self._build_schemas()
        self.conversation_history = []
    
    def _build_schemas(self):
        """构建工具的 JSON Schema（给模型看）"""
        schemas = []
        for name, tool in self.tools.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return schemas
    
    def run(self, question, strategy="auto"):
        """运行 Agent"""
        
        if strategy == "auto":
            # 自动选择策略
            strategy = self._choose_strategy(question)
        
        print(f"🧠 使用策略: {strategy}")
        
        if strategy == "direct":
            return self._direct_answer(question)
        elif strategy == "react":
            return self._react_loop(question)
        elif strategy == "plan_execute":
            return self._plan_and_execute(question)
    
    def _choose_strategy(self, question):
        """根据问题复杂度自动选择策略"""
        # 简单判断（实际可以用 LLM 来判断）
        simple_keywords = ["你好", "谢谢", "是什么", "是谁"]
        complex_keywords = ["规划", "分析", "对比", "多步", "报告"]
        
        if any(kw in question for kw in simple_keywords):
            return "direct"
        elif any(kw in question for kw in complex_keywords):
            return "plan_execute"
        else:
            return "react"

# 注册工具
tools = {
    "get_weather": {
        "description": "获取天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        },
        "handler": lambda city: f"{city}今天晴，28°C"
    },
    "search": {
        "description": "搜索互联网",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        },
        "handler": lambda query: f"搜索结果：关于'{query}'的前3条结果..."
    },
    "calculate": {
        "description": "数学计算",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        },
        "handler": lambda expr: str(eval(expr))
    }
}

# 使用
agent = SmartAgent(tools)
agent.run("北京天气怎么样？")           # → ReAct
agent.run("帮我规划一次旅行")           # → Plan-and-Execute
agent.run("你好！")                    # → Direct
```

---

## ⚡ 性能优化技巧

### 1. 并行工具调用

当多个工具调用之间没有依赖关系时，可以并行执行：

```python
import asyncio

async def parallel_tool_calls(tool_calls):
    """并行执行多个工具调用"""
    tasks = [execute_tool_async(call) for call in tool_calls]
    results = await asyncio.gather(*tasks)
    return results

# 例如：同时查两个城市的天气
# get_weather("北京") + get_weather("上海") → 并行执行
```

### 2. 工具缓存

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_weather_cached(city, date):
    """缓存天气查询结果（同一天同一城市只查一次）"""
    return get_weather(city, date)
```

### 3. 动态工具选择

不要给 Agent 塞所有工具，根据任务动态选择：

```python
def select_tools_for_task(task_description):
    """根据任务描述选择最相关的工具子集"""
    # 可以用向量相似度来匹配
    task_embedding = embed(task_description)
    tool_scores = {}
    
    for tool_name, tool_info in all_tools.items():
        tool_embedding = embed(tool_info["description"])
        similarity = cosine_similarity(task_embedding, tool_embedding)
        tool_scores[tool_name] = similarity
    
    # 只返回相似度高于阈值的前N个工具
    top_tools = sorted(tool_scores.items(), key=lambda x: -x[1])[:5]
    return {name: all_tools[name] for name, score in top_tools if score > 0.7}
```

---

## 📚 总结

```
Agent 推理策略全景图：

1. ReAct — 边想边做
   适合：中等复杂度任务
   特点：可解释、灵活
   
2. Plan-and-Execute — 先想后做
   适合：复杂多步任务
   特点：全局观强、结构化
   
3. Reflexion — 做完反思
   适合：需要高质量输出的任务
   特点：自我迭代、持续改进
   
4. Function Calling — 结构化调用
   适合：精确的工具调用场景
   特点：标准化、可靠

最佳实践：
- 简单任务用 Function Calling
- 复杂任务用 Plan-and-Execute
- 需要高质量用 Reflexion
- 不确定用 ReAct
```

> 💡 **核心要点**：好的 Agent 不是"什么都会"，而是"知道什么时候用什么"。工具使用的核心不是工具本身，而是**选择和规划**的能力。

---

## 🔗 相关链接

- [Function Calling 详解](./function-calling.md)
- [Agent 设计模式](./agent-design-patterns.md)
- [Prompt Engineering](./prompt-engineering.md)
- [什么是 AI Agent](./what-is-agent.md)
- [MCP 协议](./mcp-model-context-protocol.md)
