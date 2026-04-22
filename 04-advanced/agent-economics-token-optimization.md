# Agent 经济学：Token 消耗优化策略

> 省钱也是技术活——掌握 Token 优化，把 Agent 运营成本降 80%

## 📋 目录

- [前言](#前言)
- [一、理解 Token 和成本](#一理解-token-和成本)
- [二、成本分析框架](#二成本分析框架)
- [三、上下文压缩策略](#三上下文压缩策略)
- [四、缓存机制](#四缓存机制)
- [五、模型路由与分级](#五模型路由与分级)
- [六、Prompt 优化减少消耗](#六prompt-优化减少消耗)
- [七、工具调用优化](#七工具调用优化)
- [八、成本监控与预算控制](#八成本监控与预算控制)
- [九、实战：成本优化案例](#九实战成本优化案例)
- [十、总结](#十总结)

---

## 前言

AI Agent 调一次 API 几分钱，看起来不多。但当成千上万的用户每天使用时，账单可能让你大吃一惊：

```
一个中等规模的客服 Agent：
  日活用户：10,000
  每人每天 5 次对话
  每次对话平均 3,000 tokens（输入+输出）
  日消耗：1.5 亿 tokens
  使用 GPT-4o：$1,500/天 → $45,000/月 😱
```

好消息是：通过合理的优化策略，成本可以降低 **50%-90%**。本文教你如何系统性地优化 Token 消耗。

---

## 一、理解 Token 和成本

### 1.1 什么是 Token

Token 是大模型处理文本的基本单位，大致对应：

```
英文：1 token ≈ 0.75 个单词
中文：1 token ≈ 0.5-1 个汉字
代码：1 token ≈ 3-4 个字符

示例：
  "Hello, world!"        → 4 tokens
  "你好，世界！"          → 6 tokens
  "print('hello')"       → 5 tokens
```

### 1.2 成本构成

```
总成本 = 输入Token × 输入单价 + 输出Token × 输出单价

以 GPT-4o 为例：
  输入：$2.50 / 百万 tokens
  输出：$10.00 / 百万 tokens
  （输出比输入贵 4 倍！）

这意味着：
  减少输入 → 省一点
  减少输出 → 省很多
  减少总次数 → 省最多
```

### 1.3 成本直觉表

| 场景 | 大致Token数 | GPT-4o成本 |
|------|-----------|-----------|
| 短问答（100字） | ~300 | $0.002 |
| 中等对话（1000字） | ~3,000 | $0.02 |
| 长文分析（5000字） | ~15,000 | $0.10 |
| 读一本书（10万字） | ~150,000 | $1.00 |
| RAG检索+生成 | ~5,000-50,000 | $0.03-$0.30 |

---

## 二、成本分析框架

### 2.1 成本归因

```python
class CostAnalyzer:
    """Token成本分析器"""
    
    def __init__(self):
        self.records = []
    
    def record(self, call_info: dict):
        """记录一次API调用"""
        self.records.append({
            "model": call_info["model"],
            "input_tokens": call_info["input_tokens"],
            "output_tokens": call_info["output_tokens"],
            "cost": self._calculate_cost(call_info),
            "category": call_info.get("category", "unknown"),
            "timestamp": call_info.get("timestamp"),
        })
    
    def _calculate_cost(self, call_info: dict) -> float:
        """计算成本"""
        pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "claude-4-sonnet": {"input": 3.00, "output": 15.00},
            "claude-4-haiku": {"input": 0.80, "output": 4.00},
            "deepseek-v3": {"input": 0.27, "output": 1.10},
        }
        
        model = call_info["model"]
        if model not in pricing:
            return 0
        
        p = pricing[model]
        input_cost = call_info["input_tokens"] / 1_000_000 * p["input"]
        output_cost = call_info["output_tokens"] / 1_000_000 * p["output"]
        return input_cost + output_cost
    
    def summary(self) -> dict:
        """生成成本报告"""
        total_cost = sum(r["cost"] for r in self.records)
        total_input = sum(r["input_tokens"] for r in self.records)
        total_output = sum(r["output_tokens"] for r in self.records)
        
        # 按类别统计
        by_category = {}
        for r in self.records:
            cat = r["category"]
            if cat not in by_category:
                by_category[cat] = {"count": 0, "cost": 0, "tokens": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["cost"] += r["cost"]
            by_category[cat]["tokens"] += r["input_tokens"] + r["output_tokens"]
        
        return {
            "total_cost": total_cost,
            "total_calls": len(self.records),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "avg_cost_per_call": total_cost / max(len(self.records), 1),
            "by_category": by_category,
        }

# 使用示例
analyzer = CostAnalyzer()
analyzer.record({
    "model": "gpt-4o",
    "input_tokens": 5000,
    "output_tokens": 1000,
    "category": "customer_service"
})
print(analyzer.summary())
```

---

## 三、上下文压缩策略

### 3.1 为什么压缩上下文

每次 API 调用都要发送完整的上下文（包括历史对话、系统提示、检索结果等）。上下文越长，Token 消耗越大。

```
优化前：
  系统提示: 500 tokens
  历史对话: 10,000 tokens（20轮对话）
  检索结果: 5,000 tokens
  用户问题: 200 tokens
  总输入: 15,700 tokens → $0.039/次

优化后：
  系统提示: 500 tokens（不变）
  历史摘要: 1,000 tokens（压缩10倍）
  精选检索: 1,000 tokens（筛选2倍）
  用户问题: 200 tokens
  总输入: 2,700 tokens → $0.007/次
  节省: 83%！
```

### 3.2 对话历史压缩

```python
class ConversationCompressor:
    """对话历史压缩器"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.max_history_tokens = 2000  # 最多保留2000 tokens的历史
    
    def compress(self, messages: list) -> list:
        """压缩对话历史"""
        if not messages:
            return messages
        
        # 保留系统提示
        system_msg = [m for m in messages if m["role"] == "system"]
        conversation = [m for m in messages if m["role"] != "system"]
        
        # 如果在限制内，不压缩
        total_tokens = sum(self._estimate_tokens(m["content"]) for m in conversation)
        if total_tokens <= self.max_history_tokens:
            return messages
        
        # 策略1：滑动窗口（保留最近N轮）
        recent = conversation[-6:]  # 最近3轮（每轮2条消息）
        older = conversation[:-6]
        
        if older:
            # 策略2：用LLM总结旧对话
            summary = self._summarize(older)
            summary_msg = {"role": "system", "content": f"之前的对话摘要：{summary}"}
            return system_msg + [summary_msg] + recent
        
        return system_msg + recent
    
    def _summarize(self, messages: list) -> str:
        """用便宜的模型总结对话"""
        conversation_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        
        response = self.llm.chat(
            model="gpt-4o-mini",  # 用便宜模型做总结
            messages=[{
                "role": "user",
                "content": f"用3-5句话总结以下对话的关键信息：\n{conversation_text}"
            }],
            max_tokens=200,
        )
        return response
    
    def _estimate_tokens(self, text: str) -> int:
        """粗略估算token数"""
        return len(text) * 2  # 中文约2字符/token
```

### 3.3 RAG 结果精选

```python
class RAGResultOptimizer:
    """RAG检索结果优化"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def optimize(self, query: str, documents: list, max_docs: int = 3) -> list:
        """
        从检索结果中精选最相关的文档
        
        Args:
            query: 用户问题
            documents: 检索到的文档列表
            max_docs: 最多保留几篇文档
        """
        if len(documents) <= max_docs:
            return documents
        
        # 方法1：用 embedding 去重相似文档
        unique_docs = self._deduplicate(documents)
        
        if len(unique_docs) <= max_docs:
            return unique_docs
        
        # 方法2：用 LLM 精选最相关的
        selected = self._select_relevant(query, unique_docs, max_docs)
        return selected
    
    def _select_relevant(self, query: str, docs: list, max_docs: int) -> list:
        """让LLM选择最相关的文档"""
        doc_list = "\n".join(
            f"[文档{i+1}] {doc[:200]}..." if len(doc) > 200 else f"[文档{i+1}] {doc}"
            for i, doc in enumerate(docs)
        )
        
        response = self.llm.chat(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"""
问题：{query}

以下文档中，选出最相关的{max_docs}篇。
只返回文档编号，用逗号分隔。

{doc_list}
"""
            }],
            max_tokens=50,
        )
        
        # 解析结果
        try:
            indices = [int(x) - 1 for x in response.strip().split(",")]
            return [docs[i] for i in indices if 0 <= i < len(docs)]
        except:
            return docs[:max_docs]
```

---

## 四、缓存机制

### 4.1 语义缓存

```python
import hashlib
import json
from functools import lru_cache

class SemanticCache:
    """语义缓存：相似的问题复用答案"""
    
    def __init__(self, embedding_client, similarity_threshold=0.95):
        self.embedding_client = embedding_client
        self.threshold = similarity_threshold
        self.cache = {}  # {query_hash: {"embedding": ..., "response": ...}}
    
    def get(self, query: str) -> str | None:
        """查找缓存"""
        query_embedding = self.embedding_client.embed(query)
        
        for key, value in self.cache.items():
            similarity = self._cosine_similarity(query_embedding, value["embedding"])
            if similarity >= self.threshold:
                print(f"💡 缓存命中（相似度: {similarity:.2f}）")
                return value["response"]
        
        return None
    
    def set(self, query: str, response: str):
        """存入缓存"""
        query_embedding = self.embedding_client.embed(query)
        query_hash = hashlib.md5(query.encode()).hexdigest()
        
        self.cache[query_hash] = {
            "embedding": query_embedding,
            "response": response,
        }
        
        # 限制缓存大小
        if len(self.cache) > 1000:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
    
    def _cosine_similarity(self, a: list, b: list) -> float:
        """计算余弦相似度"""
        import numpy as np
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# 使用示例
cache = SemanticCache(embedding_client)

# 第一次调用 → 调用LLM
response1 = llm.chat("什么是机器学习？")
cache.set("什么是机器学习？", response1)

# 相似问题 → 直接返回缓存
response2 = cache.get("请解释一下机器学习")
if response2:
    print(response2)  # 直接用缓存，不调用LLM！
else:
    response2 = llm.chat("请解释一下机器学习")
    cache.set("请解释一下机器学习", response2)
```

### 4.2 Prompt 缓存（利用厂商缓存）

```python
class CachedAgent:
    """利用模型厂商的 Prompt Caching"""
    
    def __init__(self, client):
        self.client = client
        self.system_prompt_hash = None
    
    def chat(self, system_prompt: str, user_message: str) -> str:
        """
        使用 Prompt Caching
        
        原理：如果 system_prompt 和前缀没有变化，
        厂商会缓存计算结果，输入价格降低 50-90%
        
        Claude: 缓存写入免费，缓存读取 $0.30/$M（原价 $3.00）
        GPT-4o: 缓存读取 $1.25/$M（原价 $2.50）
        """
        # 确保系统提示一致（利用缓存）
        response = self.client.messages.create(
            model="claude-4-sonnet-20250514",
            max_tokens=1000,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}  # 👈 启用缓存
                }
            ],
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        # 检查缓存命中情况
        if hasattr(response, 'usage'):
            cache_tokens = getattr(response.usage, 'cache_read_input_tokens', 0)
            if cache_tokens > 0:
                print(f"✅ 缓存命中：{cache_tokens} tokens")
        
        return response.content[0].text
```

### 4.3 精确缓存（用于确定性结果）

```python
from cachetools import TTLCache

# 精确匹配缓存，带过期时间
response_cache = TTLCache(maxsize=500, ttl=3600)  # 500条，1小时过期

def get_cached_response(query: str, model_func):
    """精确缓存：完全相同的问题直接返回"""
    cache_key = hashlib.md5(query.encode()).hexdigest()
    
    if cache_key in response_cache:
        print("✅ 精确缓存命中")
        return response_cache[cache_key]
    
    response = model_func(query)
    response_cache[cache_key] = response
    return response
```

---

## 五、模型路由与分级

### 5.1 智能模型路由

```python
class ModelRouter:
    """智能模型路由器：简单任务用便宜模型，复杂任务用贵模型"""
    
    def __init__(self):
        self.models = {
            "simple": {"model": "gpt-4o-mini", "cost_per_1m": 0.60},
            "medium": {"model": "claude-4-haiku", "cost_per_1m": 4.00},
            "complex": {"model": "claude-4-sonnet", "cost_per_1m": 15.00},
            "expert": {"model": "claude-4-opus", "cost_per_1m": 75.00},
        }
    
    def classify_complexity(self, query: str) -> str:
        """分类任务复杂度"""
        simple_keywords = ["你好", "谢谢", "再见", "是什么", "谁", "什么时候"]
        complex_keywords = ["分析", "对比", "推理", "设计", "优化", "架构"]
        expert_keywords = ["数学证明", "代码调试", "安全审计", "复杂算法"]
        
        for kw in expert_keywords:
            if kw in query:
                return "expert"
        
        for kw in complex_keywords:
            if kw in query:
                return "complex"
        
        for kw in simple_keywords:
            if kw in query:
                return "simple"
        
        # 默认：短问题用简单模型，长问题用中等模型
        return "simple" if len(query) < 50 else "medium"
    
    def route(self, query: str) -> str:
        """路由到合适的模型"""
        complexity = self.classify_complexity(query)
        model_info = self.models[complexity]
        print(f"📋 复杂度: {complexity} → 模型: {model_info['model']}")
        return model_info["model"]

# 使用示例
router = ModelRouter()

print(router.route("你好"))                    # simple → gpt-4o-mini
print(router.route("帮我分析这两个方案的优劣"))    # complex → claude-4-sonnet
print(router.route("帮我设计一个分布式缓存系统"))  # expert → claude-4-opus
```

### 5.2 成本对比表

```
假设每天处理 10,000 个请求：
  - 30% simple（3,000次）
  - 50% medium（5,000次）
  - 15% complex（1,500次）
  - 5% expert（500次）

全用 GPT-4o：
  10,000 × $0.02 = $200/天 → $6,000/月

智能路由：
  3,000 × $0.002（mini）= $6
  5,000 × $0.01（haiku）= $50
  1,500 × $0.05（sonnet）= $75
  500 × $0.50（opus）= $250
  合计：$381/天 → $11,430/月... 等等这不对

重新算（按实际消耗）：
  每次请求平均 3000 tokens（输入+输出）
  
  全用 Claude 4 Sonnet：10,000 × 3000/1M × $15 = $450/天
  智能路由：
    3000 × 3000/1M × $0.60 = $5.4
    5000 × 3000/1M × $4.00 = $60
    1500 × 3000/1M × $15 = $67.5
    500 × 3000/1M × $75 = $112.5
    合计：$245.4/天

  节省：($450 - $245) / $450 = 45%
```

---

## 六、Prompt 优化减少消耗

### 6.1 精简系统提示

```python
# ❌ 冗长的系统提示（浪费 Token）
verbose_prompt = """
你是一个非常专业的、经验丰富的、知识渊博的AI助手。
你在以下领域都有深入的了解：计算机科学、数学、物理学、
工程学、经济学、金融学、管理学、心理学、哲学、文学、
历史学、艺术学、音乐学、体育学、医学、法学等。
你应该用专业但易懂的语言回答用户的问题。
如果不确定，请诚实地告诉用户你不确定。
请始终保持友好和专业的态度。
"""
# ~200 tokens，每次调用都发送

# ✅ 精简的系统提示
concise_prompt = """你是专业AI助手。不确定时请诚实说明。保持专业友好。"""
# ~20 tokens，节省 90%
```

### 6.2 使用指令而非示例

```python
# ❌ 用多个示例教模型（Token多）
few_shot_prompt = """
问题：2+2等于几？
回答：4

问题：3×5等于几？
回答：15

问题：10-3等于几？
回答：7

问题：{user_question}
回答：
"""

# ✅ 用指令（Token少）
instruction_prompt = """
请直接计算并返回数字答案，不要解释过程。
问题：{user_question}
回答：
"""
```

### 6.3 限制输出长度

```python
# 通过 max_tokens 和 prompt 双重限制
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "简洁回答，不超过100字。"},
        {"role": "user", "content": user_question}
    ],
    max_tokens=150,  # 硬性限制输出长度
)
```

---

## 七、工具调用优化

### 7.1 减少不必要的工具调用

```python
class SmartToolCaller:
    """智能工具调用：减少不必要的API调用"""
    
    def __init__(self):
        self.tool_cache = {}
    
    def call_tool(self, tool_name: str, params: dict) -> dict:
        """调用工具（带缓存）"""
        cache_key = f"{tool_name}:{json.dumps(params, sort_keys=True)}"
        
        # 1. 检查缓存
        if cache_key in self.tool_cache:
            cached = self.tool_cache[cache_key]
            # 5分钟内的缓存视为有效
            import time
            if time.time() - cached["timestamp"] < 300:
                print(f"✅ 工具缓存命中: {tool_name}")
                return cached["result"]
        
        # 2. 实际调用
        result = self._execute_tool(tool_name, params)
        
        # 3. 存入缓存
        self.tool_cache[cache_key] = {
            "result": result,
            "timestamp": time.time()
        }
        
        return result
    
    def _execute_tool(self, tool_name: str, params: dict) -> dict:
        """执行工具调用"""
        # 你的工具调用逻辑
        pass
```

---

## 八、成本监控与预算控制

### 8.1 预算控制中间件

```python
class BudgetController:
    """预算控制器"""
    
    def __init__(self, daily_budget: float):
        self.daily_budget = daily_budget
        self.spent_today = 0
        self.alert_thresholds = [0.5, 0.8, 0.95]  # 50%/80%/95% 告警
    
    def check_budget(self, estimated_cost: float) -> bool:
        """检查是否还有预算"""
        if self.spent_today + estimated_cost > self.daily_budget:
            return False
        
        # 检查告警阈值
        ratio = self.spent_today / self.daily_budget
        for threshold in self.alert_thresholds:
            if ratio >= threshold and ratio < threshold + 0.05:
                print(f"⚠️ 预算告警：已使用 {ratio:.0%} 的日预算")
        
        return True
    
    def record_cost(self, cost: float):
        """记录花费"""
        self.spent_today += cost
    
    def get_fallback_model(self) -> str:
        """预算不足时的备用模型"""
        return "gpt-4o-mini"  # 超预算时切换到最便宜的模型

# 使用
budget = BudgetController(daily_budget=100)  # 日预算$100

if budget.check_budget(estimated_cost=0.05):
    response = call_model("claude-4-sonnet", query)
    budget.record_cost(actual_cost)
else:
    response = call_model(budget.get_fallback_model(), query)
```

---

## 九、实战：成本优化案例

### 9.1 某客服Agent优化全流程

```
优化前（月成本：$15,000）：
  模型：全部用 Claude 4 Opus
  上下文：保留全部对话历史
  缓存：无
  工具调用：每次都重新查询数据库

优化后（月成本：$3,000，降低80%）：
  1. 模型路由：简单问题用 Haiku（节省40%）
  2. 对话压缩：滑动窗口+摘要（节省25%）
  3. 语义缓存：相似问题复用答案（节省20%）
  4. Prompt缓存：系统提示利用厂商缓存（节省10%）
  5. 工具缓存：相同查询结果缓存5分钟（节省5%）
```

---

## 十、总结

Token 优化策略优先级排序：

| 优先级 | 策略 | 节省幅度 | 实现难度 |
|--------|------|---------|---------|
| 🥇 P0 | 模型路由（大+小模型） | 30-60% | ⭐⭐ |
| 🥈 P1 | Prompt 缓存（厂商原生） | 20-50% | ⭐ |
| 🥉 P2 | 对话历史压缩 | 20-40% | ⭐⭐ |
| 4 | 语义缓存 | 15-30% | ⭐⭐⭐ |
| 5 | RAG 结果精选 | 10-20% | ⭐⭐ |
| 6 | Prompt 精简 | 10-30% | ⭐ |
| 7 | 工具调用缓存 | 5-15% | ⭐⭐ |
| 8 | 预算控制+熔断 | 防止超支 | ⭐⭐ |

**核心理念**：不是所有请求都值得用最贵的模型，也不是所有信息都需要每次重新计算。合理的路由和缓存能带来最大的成本优化。

> 📚 **延伸阅读**：
> - [2026年AI大模型对比](../01-fundamentals/ai-models-comparison-2026.md)
> - [上下文窗口与记忆](../01-fundamentals/context-window-and-memory.md)
> - [Agent 评估基准](./agent-evaluation-benchmarks.md)
