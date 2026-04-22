# 📏 Agent 评估基准 — 怎么知道你的 Agent 够不够好？

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 评估基准与评测体系 |
| **适用** | Agent 研究者、AI 工程师、产品经理 |
| **前置知识** | [什么是 AI Agent](../01-fundamentals/what-is-agent.md)、[Agent 设计模式](../01-fundamentals/agent-design-patterns.md) |

---

## 🎯 一句话理解

> **你觉得自己开发的 Agent 很厉害？但"厉害"怎么衡量？Agent 评估基准就像考试——给 Agent 出题、打分、排名，让你知道它到底几斤几两。**

---

## ❓ 为什么需要评估基准？

在 LLM 时代，我们已经有 MMLU、HumanEval 等经典基准。但 Agent 不一样：

```
LLM 评估：给一个输入，看输出对不对
Agent 评估：给一个任务，看它能不能完成

区别：
- Agent 需要多步推理
- Agent 需要使用工具
- Agent 的执行路径不唯一
- Agent 可能"歪打正着"（过程错但结果对）
- Agent 的"好"是多维度的（准确、高效、安全...）
```

**没有评估 = 盲目优化**。你改了一个 Prompt，Agent 变好了还是变差了？不知道。你换了一个模型，效果提升了多少？不知道。你需要**量化评估**。

---

## 📊 评估维度

评估一个 Agent，通常从以下几个维度看：

```
┌─────────────────────────────────────────┐
│           Agent 评估维度                  │
│                                          │
│  🎯 任务完成度 (Task Completion)          │
│  - 能不能完成任务？                       │
│  - 完成率是多少？                         │
│                                          │
│  ⚡ 效率 (Efficiency)                     │
│  - 花了多少步？                           │
│  - 用了多少 Token？                       │
│  - 耗时多久？                             │
│                                          │
│  🧠 推理质量 (Reasoning Quality)          │
│  - 推理过程是否合理？                     │
│  - 是否选择了正确的工具？                  │
│                                          │
│  🛡️ 安全性 (Safety)                       │
│  - 是否执行了危险操作？                    │
│  - 是否泄露了敏感信息？                    │
│                                          │
│  💰 成本 (Cost)                           │
│  - 每次 Agent 调用花费多少？               │
│  - 是否可以优化？                         │
└─────────────────────────────────────────┘
```

---

## 🏆 主流评估基准详解

### 1. AgentBench

**AgentBench** 是最早的综合性 Agent 评估基准之一，由清华团队提出。

```
基本信息：
- 提出时间：2023年
- 来源：清华大学
- 论文：AgentBench: Evaluating LLMs as Agents

评测场景：
┌─────────────────────────┐
│ 1. 操作系统 (OSWorld)    │ → 在真实操作系统中执行任务
│ 2. 数据库查询            │ → 用 SQL 查数据
│ 3. 网页浏览              │ → 用浏览器完成网页任务
│ 4. 购物                  │ → 在购物网站上买东西
│ 5. 房屋搜索              │ → 搜索房源信息
│ 6. LLM Agent 对话        │ → Agent 之间的对话
│ 7. 无限沙盒              │ → 在沙盒环境中编程
│ 8. 数字游戏              │ → 玩数字游戏
└─────────────────────────┘
```

**评估方式**：
- 每个场景有不同的评估指标
- 综合得分 = 各场景得分加权平均
- 支持多种 LLM 作为 Agent 的后端

**经典结果**（仅供参考）：
```
GPT-4 在 AgentBench 上的表现最好
Claude 紧随其后
开源模型差距明显（但差距在缩小）
```

### 2. WebArena

**WebArena** 专门评估 Agent 在**真实网站**上的操作能力。

```
基本信息：
- 提出时间：2023年
- 来源：CMU + Meta
- 论文：WebArena: A Realistic Web Environment for Building Autonomous Agents

评测环境：
- 自建了 8 个真实网站（电商、论坛、地图、Git仓库等）
- Agent 需要在这些网站上完成真实任务

任务示例：
┌──────────────────────────────────────┐
│ "在电商网站上搜索 iPhone 15，           │
│  找到评分最高的商品，                   │
│  添加到购物车"                         │
│                                      │
│ "在论坛上发一个帖子，                   │
│  标题是...，内容是..."                 │
│                                      │
│ "在 Git 仓库中创建一个 PR，            │
│  修改 README 文件"                     │
└──────────────────────────────────────┘

评估指标：
- 成功率：能否完成任务
- 步骤效率：用了多少步完成
- 最终URL匹配：是否到达了正确页面
```

**核心挑战**：
- 网站是动态的（DOM结构复杂）
- 需要理解网页内容
- 需要多步操作（搜索 → 筛选 → 点击 → 操作）
- 状态管理（登录、购物车等）

### 3. SWE-bench

**SWE-bench** 是目前最火的 **代码 Agent** 评估基准。

```
基本信息：
- 提出时间：2023年
- 来源：Princeton
- 论文：SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- 官网：swe-bench.github.io

评测方式：
- 从真实的 GitHub 仓库中收集 Issue
- Agent 需要阅读代码、定位 Bug、编写修复
- 运行测试验证修复是否正确

任务流程：
┌──────────────────────────────────────┐
│ 1. 给定一个 GitHub Issue（Bug 报告）   │
│ 2. Agent 阅读代码库                    │
│ 3. 定位问题代码                       │
│ 4. 编写修复                           │
│ 5. 运行测试                           │
│ 6. 提交修复                           │
└──────────────────────────────────────┘

评估指标：
- Resolved：修复是否通过所有测试
- Test Coverage：测试覆盖率
- Code Quality：代码质量评分

难度等级：
- SWE-bench（完整版）：500个真实Issue
- SWE-bench Lite：300个精选Issue（更常用）
- SWE-bench Verified：人工验证过的子集（500个）
```

**2024-2025 排行榜变化**：

```
早期的 SWE-bench：
- 最高 Resolved 率只有 4% 左右（2023年底）

2024年进展：
- SWE-agent (CMU) 达到 ~12%
- Devin (Cognition) 宣称 13.86%
- 各大厂商激烈竞争

2025年突破：
- 多个系统达到 30-50%+ 的 Resolved 率
- SWE-bench Verified 成为标准评测集
- Multi-agent 方案表现突出
```

### 4. TAU-bench

**TAU-bench**（Tool-use Agent Under test）专注于评估 Agent 的**工具使用能力**。

```
基本信息：
- 提出时间：2024年
- 来源：Salesforce AI Research
- 论文：TAU-bench: A Benchmark for Tool-Use Agents

评测特点：
- 专注于 Agent 使用工具的能力
- 包含真实场景（航空、零售）
- 评估工具选择的正确性

任务类型：
┌──────────────────────────────────────┐
│ 航空领域：                            │
│ - 查询航班信息                        │
│ - 预订机票                           │
│ - 修改预订                           │
│                                      │
│ 零售领域：                            │
│ - 查询商品信息                        │
│ - 处理退换货                          │
│ - 会员管理                           │
└──────────────────────────────────────┘

评估指标：
- 任务完成率
- 工具使用正确率
- 对话质量
- 策略效率（用了多少步）
```

### 5. OSWorld

**OSWorld** 评估 Agent 在**真实操作系统**上的操作能力。

```
基本信息：
- 提出时间：2024年
- 来源：港科大 + CMU

评测环境：
- 真实的 Ubuntu / macOS / Windows 环境
- Agent 拥有完整的操作权限
- 需要执行真实的系统操作

任务示例：
- "安装 Chrome 浏览器"
- "下载一个 PDF 文件并转换为 TXT"
- "用 Python 写一个 HTTP 服务器"
- "配置 SSH 并连接到远程服务器"
```

### 6. 其他重要基准

| 基准 | 评测重点 | 特点 |
|------|---------|------|
| **GAIA** | 通用 Agent 能力 | 多模态任务，难度高 |
| **HumanEval** | 代码生成 | Agent 基础能力 |
| **MATH** | 数学推理 | 推理能力 |
| **MT-Bench** | 对话质量 | 人工评审 |
| **ALFWorld** | 家庭环境 | 模拟环境中的操作 |
| **WebShop** | 网页购物 | 电商场景 |

---

## 📊 基准对比一览

```
                难度     真实性     流行度
AgentBench      ⭐⭐⭐    ⭐⭐⭐     ⭐⭐⭐⭐
WebArena        ⭐⭐⭐⭐   ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐
SWE-bench       ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐
TAU-bench       ⭐⭐⭐⭐   ⭐⭐⭐⭐   ⭐⭐⭐
OSWorld         ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐
GAIA            ⭐⭐⭐⭐⭐  ⭐⭐⭐     ⭐⭐⭐
```

| 基准 | 主要场景 | 评估方式 | 适合谁 |
|------|---------|---------|--------|
| AgentBench | 综合多场景 | 自动+人工 | 通用 Agent |
| WebArena | 网页操作 | 自动 | 浏览器 Agent |
| SWE-bench | 代码修复 | 自动（测试） | 编程 Agent |
| TAU-bench | 工具使用 | 自动 | 工具型 Agent |
| OSWorld | 系统操作 | 自动 | 系统 Agent |
| GAIA | 通用推理 | 人工评审 | 研究 |

---

## 🛠️ 如何为自己的 Agent 做评估？

### 方法一：使用现有基准

```python
# 以 SWE-bench 为例
# 安装
pip install swebench

# 下载数据集
from swebench.harness.constants import TestSpec
from swebench.metrics.getters import get_swebench_dataset

# 获取测试集
dataset = get_swebench_dataset("princeton-nlp/SWE-bench_Lite")
print(f"共 {len(dataset)} 个测试用例")

# 每个 test case 包含：
# - repo: GitHub 仓库
# - instance_id: 唯一标识
# - problem_statement: Issue 描述
# - hints_text: 提示信息
# - created_at: 创建时间
# - version: 版本信息
# - base_commit: 基准 commit
# - test_patch: 测试补丁
```

### 方法二：自定义评估框架

```python
from typing import TypedDict
from dataclasses import dataclass

@dataclass
class EvalResult:
    """评估结果"""
    task_id: str
    completed: bool           # 是否完成
    correct: bool             # 结果是否正确
    steps_used: int           # 使用了多少步
    tokens_used: int          # 使用了多少 Token
    latency_seconds: float    # 耗时
    tools_called: list[str]   # 调用了哪些工具
    errors: list[str]         # 遇到的错误
    
    @property
    def score(self) -> float:
        """综合评分（0-100）"""
        if not self.completed:
            return 0
        base = 50 if self.correct else 20
        efficiency_bonus = max(0, 30 - self.steps_used) * 2  # 步骤越少分越高
        return min(100, base + efficiency_bonus)

class AgentEvaluator:
    """Agent 评估器"""
    
    def __init__(self, agent, test_cases: list[dict]):
        self.agent = agent
        self.test_cases = test_cases
        self.results: list[EvalResult] = []
    
    def run_evaluation(self) -> dict:
        """运行完整评估"""
        import time
        
        for case in self.test_cases:
            start_time = time.time()
            
            try:
                # 运行 Agent
                result = self.agent.run(case["input"])
                
                # 检查结果
                is_correct = self.check_result(result, case["expected"])
                
                eval_result = EvalResult(
                    task_id=case["id"],
                    completed=True,
                    correct=is_correct,
                    steps_used=result.get("steps", 1),
                    tokens_used=result.get("tokens", 0),
                    latency_seconds=time.time() - start_time,
                    tools_called=result.get("tools", []),
                    errors=[]
                )
            except Exception as e:
                eval_result = EvalResult(
                    task_id=case["id"],
                    completed=False,
                    correct=False,
                    steps_used=0,
                    tokens_used=0,
                    latency_seconds=time.time() - start_time,
                    tools_called=[],
                    errors=[str(e)]
                )
            
            self.results.append(eval_result)
        
        return self.generate_report()
    
    def check_result(self, actual, expected) -> bool:
        """检查结果是否正确（可自定义）"""
        if isinstance(expected, str):
            return expected.lower() in str(actual).lower()
        return actual == expected
    
    def generate_report(self) -> dict:
        """生成评估报告"""
        total = len(self.results)
        completed = sum(1 for r in self.results if r.completed)
        correct = sum(1 for r in self.results if r.correct)
        avg_score = sum(r.score for r in self.results) / total
        avg_latency = sum(r.latency_seconds for r in self.results) / total
        
        return {
            "total_tasks": total,
            "completion_rate": completed / total,
            "accuracy": correct / total,
            "average_score": avg_score,
            "average_latency": avg_latency,
            "per_task_results": [
                {
                    "id": r.task_id,
                    "score": r.score,
                    "correct": r.correct,
                    "steps": r.steps_used,
                    "latency": r.latency_seconds
                }
                for r in self.results
            ]
        }

# 使用
test_cases = [
    {
        "id": "test_001",
        "input": "北京明天的天气怎么样？",
        "expected": "晴"
    },
    {
        "id": "test_002",
        "input": "帮我计算 (15 + 27) * 3",
        "expected": "126"
    },
    # ... 更多测试用例
]

evaluator = AgentEvaluator(my_agent, test_cases)
report = evaluator.run_evaluation()

print(f"完成率: {report['completion_rate']:.1%}")
print(f"准确率: {report['accuracy']:.1%}")
print(f"平均分: {report['average_score']:.1f}")
print(f"平均延迟: {report['average_latency']:.2f}s")
```

### 方法三：LLM-as-Judge（用 LLM 评 LLM）

当没有客观答案时，用另一个 LLM 来评分：

```python
JUDGE_PROMPT = """
你是一个专业的评估员。请评估以下 AI Agent 的回答质量。

用户问题：{question}
Agent 回答：{answer}

请从以下维度打分（1-10分）：
1. 准确性：信息是否准确
2. 完整性：是否完整回答了问题
3. 清晰性：表达是否清晰易懂
4. 有用性：对用户是否有帮助

请用 JSON 格式返回：
{
    "accuracy": 8,
    "completeness": 7,
    "clarity": 9,
    "usefulness": 8,
    "overall": 8,
    "reasoning": "简要说明评分理由"
}
"""

def llm_judge(question: str, answer: str) -> dict:
    """用 LLM 评估 Agent 回答"""
    prompt = JUDGE_PROMPT.format(question=question, answer=answer)
    response = judge_llm.invoke(prompt)
    return json.loads(response.content)
```

---

## 📈 评估报告示例

一个完整的 Agent 评估报告应该包含：

```
═══════════════════════════════════════
       Agent 评估报告 v2.1
═══════════════════════════════════════

📋 基本信息
- Agent 名称：CustomerServiceBot v2.1
- 评估时间：2025-01-15
- 评估集：200 个真实用户问题
- 模型后端：GPT-4o

📊 核心指标
┌──────────────┬──────────┬──────────┐
│    指标       │  v2.0    │  v2.1    │
├──────────────┼──────────┼──────────┤
│ 完成率        │  85.0%   │  92.5% ↑ │
│ 准确率        │  78.0%   │  86.0% ↑ │
│ 平均步数      │  3.2     │  2.8  ↓  │
│ 平均延迟      │  4.5s    │  3.2s ↓  │
│ Token/请求    │  2,100   │  1,800 ↓ │
│ 成本/请求     │  $0.032  │  $0.027 ↓│
└──────────────┴──────────┴──────────┘

🔍 分类表现
- 退款处理：95% 准确率 ✅
- 商品咨询：90% 准确率 ✅
- 物流查询：88% 准确率 ✅
- 投诉处理：72% 准确率 ⚠️（需改进）

🐛 典型失败案例
1. [test_042] 退款金额计算错误
2. [test_089] 无法处理多商品退换
3. [test_156] 情绪化用户处理不当

💡 改进建议
1. 优化退款计算逻辑
2. 增加多商品退换场景的训练数据
3. 增加情绪识别和安抚策略
═══════════════════════════════════════
```

---

## 💡 最佳实践

### 1. 构建自己的评估数据集

```python
# 从生产环境中收集真实数据
def collect_eval_data_from_production():
    """
    1. 收集真实用户问题
    2. 记录 Agent 的回答
    3. 收集用户反馈（👍/👎）
    4. 人工标注正确答案
    5. 构建评估数据集
    """
    pass

# 数据集应该包含：
# - 简单问题（Agent 应该轻松搞定）
# - 中等难度问题（需要多步推理）
# - 困难问题（边缘情况）
# - 常见错误场景（Agent 容易犯的错）
```

### 2. 持续评估

```python
# 每次改动后都跑一遍评估
# CI/CD 中集成评估流程

def ci_evaluation():
    """
    CI 流程：
    1. 代码变更 → 运行评估
    2. 对比上次结果
    3. 如果关键指标下降 > 5% → 阻止部署
    4. 生成评估报告
    """
    pass
```

### 3. 注意基准的局限性

```
⚠️ 基准分数不等于真实能力

原因：
1. 基准可能过时（被刷榜）
2. 基准可能不代表真实场景
3. Agent 可能过拟合了测试集
4. 分数高不代表用户体验好

建议：
- 多个基准交叉验证
- 结合真实用户反馈
- 关注指标背后的原因
```

---

## 📚 总结

```
Agent 评估基准全景：

综合类 → AgentBench
网页类 → WebArena
代码类 → SWE-bench
工具类 → TAU-bench
系统类 → OSWorld
推理类 → GAIA

评估维度：
- 任务完成度（最重要）
- 效率（步数、Token、延迟）
- 安全性（不犯错）
- 成本（可承受）

最佳实践：
1. 使用多个基准交叉评估
2. 构建自己的评估数据集
3. 每次改动后自动评估
4. 关注真实用户反馈
5. 不要迷信分数
```

> 💡 **核心要点**：评估不是一次性的任务，而是持续的过程。好的评估体系让你能**量化进步、发现退化、指导优化**——这是把 Agent 从"玩具"变成"产品"的关键一步。

---

## 🔗 相关链接

- [SWE-bench 官网](https://swe-bench.github.io/)
- [AgentBench 论文](https://arxiv.org/abs/2308.03688)
- [WebArena 论文](https://arxiv.org/abs/2307.13854)
- [TAU-bench 论文](https://arxiv.org/abs/2406.12045)
- [OSWorld 论文](https://arxiv.org/abs/2404.07972)
- [Agent 设计模式](../01-fundamentals/agent-design-patterns.md)
- [Agent 安全护栏](./agent-safety-guardrails.md)
