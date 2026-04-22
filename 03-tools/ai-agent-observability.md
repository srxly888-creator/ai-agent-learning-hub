# 🔍 Agent 可观测性工具 — 监控、调试、优化你的 AI Agent

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 可观测性工具对比与实践 |
| **适用** | Agent 开发者、AI 工程师、DevOps |
| **前置知识** | [Agent 架构](../01-fundamentals/ai-agent-architecture.md) |

---

## 🎯 一句话理解

> **开发 Agent 就像放飞一只看不见的风筝——可观测性工具就是那根线，让你能看见它在做什么、飞得怎么样、哪里出了问题。没有可观测性，你就是在盲飞。**

---

## ❓ 为什么 Agent 需要可观测性？

传统软件的调试很简单——看日志、打断点。但 Agent 不一样：

```
传统软件：
输入 → 固定逻辑 → 输出
（每一步都是确定的，容易调试）

AI Agent：
输入 → LLM 推理（黑盒）→ 工具调用 → LLM 再推理 → ...
（每一步都不确定，调试噩梦）
```

你可能会遇到这些问题：

| 问题 | 表现 | 没有可观测性时 |
|------|------|--------------|
| 🐛 回答质量差 | Agent 给出错误答案 | 不知道哪一步出了错 |
| 🐌 响应慢 | 用户等了很久 | 不知道时间花在哪里 |
| 💸 Token 浪费 | 费用超出预期 | 不知道哪次调用最贵 |
| 🔄 死循环 | Agent 反复做同一件事 | 发现不了 |
| 🔧 工具失败 | API 调用出错 | 不知道哪个工具、为什么失败 |

**可观测性 = 可见性 + 可调试性 + 可优化性**

---

## 📏 可观测性三支柱

在 AI Agent 领域，可观测性也有经典的"三支柱"：

```
┌──────────────────────────────────────┐
│        AI Agent 可观测性三支柱        │
│                                       │
│  📊 Traces（追踪）                     │
│  - Agent 执行的完整链路               │
│  - 每一步的输入输出                    │
│  - 工具调用记录                       │
│                                       │
│  📈 Metrics（指标）                    │
│  - 响应时间                           │
│  - Token 使用量                       │
│  - 成功率/失败率                      │
│  - 成本追踪                          │
│                                       │
│  📝 Logs（日志）                      │
│  - 错误日志                           │
│  - 调试信息                           │
│  - 用户反馈                          │
└──────────────────────────────────────┘
```

---

## 🛠️ 主流工具对比

### 全景图

| 工具 | 开发者 | 开源 | 核心特点 | 定价 |
|------|--------|------|---------|------|
| **LangSmith** | LangChain | ❌ | LangChain 生态深度集成 | 免费层 + 付费 |
| **Weave** | Weights & Biases | ✅ | 实验追踪 + 评估 | 免费层 + 付费 |
| **Phoenix (Arize)** | Arize AI | ✅ | LLM 专用的可观测性 | 免费开源 |
| **Langfuse** | 社区 | ✅ | 开源 LangSmith 替代 | 自托管免费 |
| **Helicone** | Helicone | ✅ | 代理模式，零代码接入 | 免费层 + 付费 |
| **Braintrust** | Braintrust | ✅ | 评估 + 可观测 | 免费层 + 付费 |

---

## 🔷 工具一：LangSmith

LangSmith 是 LangChain 官方的可观测性平台，与 LangChain/LangGraph 深度集成。

### 核心功能

```
1. 🔗 Trace 追踪
   - 完整的 Agent 执行链路
   - 每个步骤的耗时、Token 使用
   - LLM 输入输出的完整记录

2. 📊 评估
   - 自动化评估流水线
   - 自定义评估指标
   - A/B 测试

3. 📂 数据集管理
   - 保存测试用例
   - 版本管理
   - 回归测试

4. 🔍 调试
   - 逐步回放 Agent 执行过程
   - 查看每一步的 Prompt 和 Response
   - 标注和标注管理
```

### 快速接入

```bash
pip install langsmith
```

```python
import os
from langsmith import Client

# 设置环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__your_api_key"
os.environ["LANGCHAIN_PROJECT"] = "my-agent-project"

# 就这么简单！LangChain 会自动上报数据到 LangSmith
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("你好")
# 这个调用会自动出现在 LangSmith Dashboard 中
```

### 深度使用：自定义 Trace

```python
from langsmith import traceable

@traceable(name="my_custom_function")
def my_agent_step(query: str) -> str:
    """自定义追踪函数"""
    # 这步会被 LangSmith 记录
    search_result = search_engine.search(query)
    
    # 子函数也会被追踪
    answer = generate_answer(query, search_result)
    
    return answer

@traceable(name="search_engine")
def search_engine_search(query):
    # 嵌套的 trace
    return web_search(query)
```

### 评估功能

```python
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# 定义评估指标
evaluators = [
    LangChainStringEvaluator("criteria", config={
        "criteria": {
            "helpfulness": "回答是否有帮助",
            "accuracy": "回答是否准确",
            "clarity": "回答是否清晰"
        }
    })
]

# 运行评估
dataset = client.create_dataset("agent-qa-dataset")

evaluate(
    lambda inputs: my_agent(inputs["question"]),
    data=dataset.name,
    evaluators=evaluators,
    experiment_prefix="agent-v2-eval"
)
```

### LangSmith 的优缺点

| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 与 LangChain 无缝集成 | 非开源（数据在第三方） |
| 功能全面（追踪+评估+数据集） | 免费层有限制 |
| UI 漂亮好用 | 强依赖 LangChain 生态 |
| 团队协作支持好 | 价格较贵 |

---

## 🔷 工具二：Weave (Weights & Biases)

Weave 是 W&B 推出的 LLM 可观测性工具，专注于**实验追踪和评估**。

### 核心功能

```
1. 📊 Op 追踪
   - 记录函数调用（类似 LangSmith 的 Trace）
   - 自动捕获输入输出
   - 支持嵌套调用

2. 🧪 评估
   - 自动化评估框架
   - 支持自定义指标
   - 评估结果可视化

3. 📈 实验管理
   - 对比不同版本的 Agent
   - 追踪模型和 Prompt 变更
```

### 快速接入

```bash
pip install weave
```

```python
import weave

# 初始化
weave.init("my-agent-project")

# 用 @weave.op 装饰器追踪函数
@weave.op
def search_and_answer(question: str) -> str:
    """搜索并回答"""
    results = web_search(question)
    answer = llm.generate(f"根据{results}回答：{question}")
    return answer

# 调用函数，数据自动上报
result = search_and_answer("什么是 AI Agent？")
```

### 评估功能

```python
import weave

# 定义评估模型
@weave.op
def answer_quality(question: str, model_output: str) -> dict:
    """用 LLM 评估回答质量"""
    score = llm.evaluate(f"""
    问题：{question}
    回答：{model_output}
    请评分 1-10。
    """)
    return {"score": int(score)}

# 创建评估集
evaluation = weave.Evaluation(
    dataset=[{"question": "什么是 Agent？"}, {"question": "RAG 是什么？"}],
    scorers=[answer_quality]
)

# 运行评估
results = evaluation.evaluate(search_and_answer)
```

### Weave 的优缺点

| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 开源（核心部分） | LLM 生态集成不如 LangSmith |
| W&B 生态强大 | 评估功能相对基础 |
| 实验管理成熟 | UI 不如 LangSmith 直观 |
| 社区活跃 | 复杂场景配置较多 |

---

## 🔷 工具三：Phoenix (Arize AI)

Phoenix 是一个**完全开源**的 LLM 可观测性平台，专注于 LLM 应用监控。

### 核心功能

```
1. 🔍 Trace 可视化
   - 直观的执行链路图
   - 支持 OpenTelemetry 标准
   - 本地部署，数据不出境

2. 📊 仪表盘
   - 延迟分布图
   - 错误率监控
   - Token 使用量

3. 🧪 评估
   - 内置多种评估指标
   - 支持自定义评估器
   - 标注工具

4. 🔌 集成
   - LangChain
   - LlamaIndex
   - OpenAI
   - 任何 OpenTelemetry 兼容的系统
```

### 快速接入

```bash
pip install arize-phoenix
```

```python
import phoenix as px

# 启动 Phoenix（本地）
session = px.launch_app()

# 方式1：LangChain 集成
from langchain_openai import ChatOpenAI
from langchain.callbacks import CallbackHandler

# Phoenix 会自动捕获所有 LangChain 调用
```

```python
# 方式2：手动上报
from phoenix.trace import using_project
from openinference.instrumentation.openai import OpenAIInstrumentor

# 自动 instrument OpenAI 调用
OpenAIInstrumentor().instrument()

with using_project("my-agent"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "你好"}]
    )
    # 这个调用会被 Phoenix 自动追踪
```

### Phoenix 的优缺点

| ✅ 优点 | ❌ 缺点 |
|---------|---------|
| 完全开源 | UI 相对简陋 |
| 本地部署，数据安全 | 功能不如 LangSmith 全面 |
| 支持 OpenTelemetry | 文档相对较少 |
| 轻量级 | 生态不如 W&B |

---

## 🔷 工具四：Langfuse

Langfuse 是一个**开源的 LangSmith 替代品**，社区驱动。

### 核心功能

```
1. 🔗 Trace + Span
   - 完整的调用链追踪
   - 自定义标注
   - Prompt 版本管理

2. 📊 评估
   - 自动评估
   - 人工标注
   - A/B 测试

3. 📝 Prompt 管理
   - 版本控制
   - 在线编辑
   - A/B 测试

4. 🔌 多框架集成
   - LangChain
   - LlamaIndex
   - 直接 SDK
```

### 快速接入

```bash
# 自托管
docker compose up -d

pip install langfuse
```

```python
from langfuse import Langfuse
from langfuse.decorators import observe

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="http://localhost:3000"  # 自托管地址
)

@observe()
def my_agent(question: str):
    # 自动追踪
    search_result = search(question)
    answer = generate(search_result)
    
    # 记录评分
    langfuse.score(
        trace_id=langfuse.get_trace_id(),
        name="quality",
        value=8.5
    )
    
    return answer
```

### Prompt 版本管理

```python
# 在 Langfuse Dashboard 中管理 Prompt 版本
# 代码中按版本引用
from langfuse import Langfuse

langfuse = Langfuse()

# 获取特定版本的 Prompt
prompt = langfuse.get_prompt("agent-system-prompt", version=3)
system_message = prompt.compile(user_name="小明")
```

---

## 🔷 工具五：Helicone

Helicone 采用**代理模式**，几乎零代码接入。

```bash
# 只需改一下 API 的 base URL
export OPENAI_API_BASE="https://oai.hconeai.com/v1"
export HELICONE_API_KEY="your-key"
```

```python
# 正常使用 OpenAI SDK，Helicone 自动代理和记录
from openai import OpenAI

client = OpenAI()  # 自动通过 Helicone 代理
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好"}]
)
# Helicone Dashboard 自动显示这次调用
```

**适合场景**：快速接入、不想改代码、只需要基础监控。

---

## 📊 工具选择指南

```
你的情况是什么？

├─ 用 LangChain/LangGraph 开发？
│  → 首选 LangSmith（集成最好）
│  → 或 Langfuse（开源替代）
│
├─ 需要本地部署、数据安全？
│  → 首选 Phoenix 或 Langfuse
│
├─ 做大量实验和 A/B 测试？
│  → 首选 Weave (W&B)
│
├─ 想零代码接入？
│  → 首选 Helicone
│
├─ 预算有限？
│  → Phoenix / Langfuse / Weave（都有免费开源版）
│
└─ 需要全面的企业级方案？
   → LangSmith（最全面）
```

| 需求 | 最佳选择 | 备选 |
|------|---------|------|
| LangChain 生态 | LangSmith | Langfuse |
| 开源/自托管 | Phoenix | Langfuse |
| 实验追踪 | Weave | LangSmith |
| 零代码接入 | Helicone | — |
| Prompt 管理 | Langfuse | LangSmith |
| 最全面功能 | LangSmith | Weave |

---

## 🛠️ 实战：搭建 Agent 监控体系

### 方案：Langfuse 自托管 + 自定义指标

```bash
# 1. 启动 Langfuse
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d

# 2. 安装 SDK
pip install langfuse langchain-openai
```

```python
from langfuse.decorators import observe, langfuse_context
from langfuse import Langfuse
from langchain_openai import ChatOpenAI

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="http://localhost:3000"
)

llm = ChatOpenAI(model="gpt-4o")

@observe(name="customer_service_agent")
def customer_service_agent(user_message: str, user_id: str):
    """带监控的客服 Agent"""
    
    # 意图识别
    intent = classify_intent(user_message)
    langfuse_context.update_current_trace(
        user_id=user_id,
        tags=[intent]
    )
    
    # 根据意图路由
    if intent == "refund":
        result = handle_refund(user_message)
    elif intent == "complaint":
        result = handle_complaint(user_message)
    else:
        result = general_chat(user_message)
    
    # 记录指标
    langfuse_context.score(
        name="response_time",
        value=time_elapsed()
    )
    
    langfuse_context.score(
        name="user_satisfaction",  # 可以后续更新
        value=None  # 占位，等用户反馈后更新
    )
    
    return result

@observe(name="classify_intent")
def classify_intent(message: str) -> str:
    """意图分类"""
    response = llm.invoke(f"""
    分类以下用户消息的意图：refund / complaint / general
    消息：{message}
    只返回类型。
    """)
    return response.content.strip()

@observe(name="handle_refund")
def handle_refund(message: str) -> str:
    """处理退款"""
    # 提取订单号
    order_id = extract_order_id(message)
    
    # 查询订单
    order_info = query_database(order_id)
    
    # 生成退款方案
    response = llm.invoke(f"""
    订单信息：{order_info}
    用户消息：{message}
    请生成退款处理方案。
    """)
    
    return response.content
```

### 监控仪表盘配置

在 Langfuse Dashboard 中可以配置：

```
📊 关键指标看板：

1. 请求量趋势
   - 每日请求总数
   - 按意图分类的请求量
   - 高峰时段

2. 性能指标
   - 平均响应时间
   - P50/P95/P99 延迟
   - 超时率

3. 质量指标
   - 用户满意度评分
   - 错误率
   - 重试率

4. 成本指标
   - 每日 Token 消耗
   - 每次请求平均成本
   - 按意图分类的成本

5. 异常告警
   - 错误率 > 5%
   - 响应时间 > 10s
   - Token 消耗异常增长
```

---

## 💡 最佳实践

### 1. Trace 命名规范

```python
# ✅ 好的命名
@observe(name="agent.search_web")
@observe(name="agent.generate_answer")
@observe(name="tool.calculate_math")

# ❌ 不好的命名
@observe(name="step1")
@observe(name="func")
@observe(name="do_something")
```

### 2. 合理使用 Tag

```python
@observe(name="agent", tags=["production", "v2", "customer-service"])
def my_agent():
    pass

# 按 tag 过滤和分析
# - "production" vs "staging" 对比
# - "v1" vs "v2" 性能对比
# - 按 agent 类型分类分析
```

### 3. 不要过度追踪

```python
# ❌ 过度追踪：每个小函数都追踪
@observe  # 太细了
def format_string(s):
    return s.strip().lower()

# ✅ 合理追踪：只在关键边界追踪
@observe(name="agent.full_pipeline")
def full_pipeline():
    # 内部细节不需要单独追踪
    ...
```

### 4. 持续评估

```python
# 建立定期评估流程
# 1. 保存每次 Agent 运行的 Trace
# 2. 定期抽样人工评审
# 3. 自动化回归测试
# 4. 监控指标趋势变化
```

---

## 📚 总结

```
Agent 可观测性 = 追踪 (Trace) + 指标 (Metrics) + 日志 (Logs)

工具选择：
- LangChain 用户 → LangSmith
- 开源爱好者 → Phoenix / Langfuse
- 实验驱动 → Weave (W&B)
- 零代码 → Helicone
- 企业级 → LangSmith

关键实践：
1. 从第一天就接入可观测性
2. 建立评估数据集
3. 监控 Token 成本和延迟
4. 设置异常告警
5. 定期评审 Trace 质量
```

> 💡 **核心要点**：可观测性不是"锦上添花"，而是 Agent 工程化的"基础设施"。没有可观测性的 Agent，就像没有仪表盘的汽车——你不知道它跑得快不快、油还剩多少、哪里出了问题。

---

## 🔗 相关链接

- [Agent 架构详解](../01-fundamentals/ai-agent-architecture.md)
- [Agent 设计模式](../01-fundamentals/agent-design-patterns.md)
- [LangSmith 官网](https://smith.langchain.com)
- [Phoenix GitHub](https://github.com/Arize-ai/phoenix)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Weave 文档](https://weave-docs.wandb.ai)
