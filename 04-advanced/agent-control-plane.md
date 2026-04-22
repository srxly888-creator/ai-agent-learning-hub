# 🛫 Agent 控制面 (Control Plane) — 生产级 Agent 管理基础设施

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 生产环境基础设施 |
| **关键词** | Control Plane, AAS, Observability, Governance |
| **相关** | [AAS 底座](https://github.com/autonomous-agent-stack/autonomous-agent-stack) |

---

## 🎯 一句话理解

> **Agent 控制面就像 Kubernetes 之于容器——你写好了 Agent，但怎么管理 100 个 Agent 同时跑、怎么监控、怎么限流、怎么计费？这就是控制面要做的事。**

类比：
- **Kubernetes** 管理容器 → **Agent Control Plane** 管理 Agent
- **Nginx** 做反向代理 → **Agent Router** 做 Agent 路由
- **Grafana** 监控服务 → **Agent Observability** 监控 Agent

---

## 🔍 为什么需要控制面？

### 开发环境 vs 生产环境

| 维度 | 开发环境（Demo） | 生产环境 |
|------|----------------|---------|
| **Agent 数量** | 1-3 个 | 10-1000+ 个 |
| **并发用户** | 你自己 | 1000+ 用户 |
| **错误处理** | 打印日志 | 自动重试 + 告警 |
| **成本控制** | 不关心 | 每月预算 ¥10万+ |
| **安全** | 开发 Key | 权限隔离 + 审计 |
| **监控** | 看终端输出 | Dashboard + 告警 |
| **版本管理** | 改了就跑 | 灰度发布 + 回滚 |

```
没有控制面:
  ❌ 100 个 Agent 每个都自己管理 API Key
  ❌ 不知道哪个 Agent 花了多少钱
  ❌ 一个 Agent 出错导致全部挂掉
  ❌ 无法追踪用户的请求链路
  ❌ 新模型上线要改每个 Agent 的代码

有控制面:
  ✅ 统一 API Key 管理 + 轮转
  ✅ 实时 Token 消耗看板
  ✅ 错误隔离 + 自动降级
  ✅ 全链路追踪（Trace）
  ✅ 一行配置切换模型
```

---

## 🏗️ 核心能力

### 1. Observability（可观测性）

知道每个 Agent 在干什么、花了多少 Token、用了多少时间。

```
┌─────────────────────────────────────────────┐
│              Observability Stack             │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Traces   │  │ Metrics  │  │  Logs    │  │
│  │ 请求链路  │  │ Token/延迟│  │ 错误日志 │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                               │
│  例子:                                         │
│  用户请求 → Router(50ms) → Agent A(2.3s, 1.2K tokens) │
│         → Tool Call(800ms) → Agent B(1.5s, 800 tokens)  │
│         → 总耗时 4.65s, 总消耗 2000 tokens             │
└─────────────────────────────────────────────┘
```

**主流方案：**

| 方案 | 类型 | 特点 | 链接 |
|------|------|------|------|
| **LangSmith** | 商业 | LangChain 官方，功能最全 | https://smith.langchain.com |
| **Weave** | 开源 | Weights & Biases 出品 | https://github.com/wandb/weave |
| **Arize Phoenix** | 开源 | 专注 LLM 可观测性 | https://github.com/Arize-ai/phoenix |
| **Langfuse** | 开源 | 可自托管，功能丰富 | https://github.com/langfuse/langfuse |
| **OpenTelemetry** | 标准 | 通用可观测性标准 | https://opentelemetry.io |

### 2. Cost Management（成本管理）

追踪和控制 Token 消耗。

```
成本管理核心能力:
  📊 实时 Dashboard — 每个 Agent/用户/模型的 Token 消耗
  💰 预算控制 — 设置月度/日度预算，超限告警
  📉 优化建议 — 识别高成本 Agent，推荐替代模型
  🏷️ 分账 — 按 Team/项目/客户分摊成本
  📈 趋势预测 — 基于历史数据预测下月花费
```

**实际例子：**

```
某公司 Agent 成本分析:

Agent            月 Token 消耗    月成本     占比
─────────────────────────────────────────────
客服 Agent       50M              ¥2,500    45%
数据分析 Agent   20M              ¥1,000    18%
代码生成 Agent   15M              ¥750      14%
邮件 Agent       10M              ¥500      9%
其他 Agent       10M              ¥800      14%
─────────────────────────────────────────────
总计              105M             ¥5,550    100%

💡 发现：客服 Agent 用 GPT-4o 太贵
   建议：简单问题用 GPT-4o-mini（省 80%）
   预计月省：¥2,000
```

### 3. Rate Limiting（限流）

防止 API 配额耗尽和突发流量。

```
限流策略:
  ┌─────────────────────────────────────┐
  │         Rate Limiter                 │
  │                                       │
  │  用户级:  每用户 100 次/分钟          │
  │  Agent级: 每 Agent 1000 次/分钟      │
  │  全局级:  总计 10000 次/分钟         │
  │  Token级: 每请求最大 4096 Token      │
  │                                       │
  │  算法: 令牌桶 (Token Bucket)         │
  │  超限: 返回 429 + 排队等待           │
  └─────────────────────────────────────┘
```

### 4. Routing（智能路由）

根据请求特征选择最优 Agent 或模型。

```
用户请求 → Router
              │
              ├── 简单问题 ──→ GPT-4o-mini（便宜快）
              ├── 复杂推理 ──→ Claude Opus（贵但强）
              ├── 代码生成 ──→ Claude Sonnet（擅长代码）
              ├── 中文任务 ──→ DeepSeek V3（中文好+便宜）
              └── 紧急请求 ──→ 高优先级队列
```

### 5. Policy Enforcement（策略执行）

统一执行安全和合规策略。

```
策略引擎:
  ✅ 所有 Agent 必须使用企业 API Key（禁止个人 Key）
  ✅ 敏感数据必须脱敏后再发给 LLM
  ✅ 涉及删除/修改操作的 Agent 必须人工确认
  ✅ 所有请求保留 90 天审计日志
  ✅ 禁止 Agent 访问内网数据库（除白名单外）
  ❌ 禁止 Agent 发送邮件给外部地址（除审批通过外）
```

---

## 🏛️ AAS 底座架构

**AAS = Agent-as-a-Service**，一种面向生产环境的 Agent 治理架构。

### 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Session** | 会话管理 — 一个用户交互的完整生命周期 | 一次通话 |
| **Policy** | 策略治理 — 定义 Agent 可以做什么、不能做什么 | 公司规章制度 |
| **Capability** | 能力注册 — Agent 声称自己能做什么 | 员工技能表 |
| **Promotion** | 发布管理 — Agent 的版本控制和发布流程 | App Store 审核 |

### 架构图

```
┌──────────────────────────────────────────────────┐
│                  AAS Control Plane                │
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Session  │  │ Policy   │  │   Capability     │ │
│  │ Manager  │  │ Engine   │  │   Registry       │ │
│  │          │  │          │  │                  │ │
│  │ • 创建   │  │ • 权限   │  │ • Agent 注册     │ │
│  │ • 恢复   │  │ • 审计   │  │ • 能力发现       │ │
│  │ • 超时   │  │ • 限流   │  │ • 版本管理       │ │
│  │ • 历史   │  │ • 脱敏   │  │ • 依赖关系       │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │              Promotion Manager                │ │
│  │  灰度发布 → A/B 测试 → 全量发布 → 回滚        │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │              Observability                     │ │
│  │  Traces + Metrics + Logs + Cost Tracking      │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
         ↕                    ↕
┌──────────────┐    ┌──────────────────┐
│  AI Agents   │    │  External Tools  │
│  (Workers)   │    │  (MCP Servers)   │
└──────────────┘    └──────────────────┘
```

### GitHub 项目

- **Autonomous Agent Stack**: https://github.com/autonomous-agent-stack/autonomous-agent-stack
  - Session → Policy → Capability → Promotion 的治理架构
  - 支持 Mac/Linux/Win + 影刀 RPA 的调度

---

## 📊 主流方案对比

| 方案 | 类型 | 核心能力 | 价格 |
|------|------|---------|------|
| **LangSmith** | 商业 SaaS | Trace + Eval + Dataset + Playground | $100/月起 |
| **Langfuse** | 开源可托管 | Trace + Eval + Prompt Mgmt | 免费自托管 |
| **Weave** | 开源 | Trace + Experiment | 免费 |
| **Phoenix** | 开源 | Trace + Eval | 免费 |
| **Arize** | 商业 | 全链路 ML 可观测性 | 企业定价 |
| **AAS 底座** | 开源 | Session + Policy + Capability | 自建 |

---

## ✅ 最佳实践

### 1. 从小开始

```
阶段 1（Demo）: Agent + 简单日志
阶段 2（内部）: + Langfuse/LangSmith 追踪
阶段 3（生产）: + 限流 + 预算控制 + 告警
阶段 4（规模）: + 智能路由 + A/B 测试 + 灰度发布
```

### 2. 必须有的监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|---------|
| Token 消耗/分钟 | 成本追踪 | > 日均 2 倍 |
| 请求延迟 P99 | 性能 | > 10 秒 |
| 错误率 | 可靠性 | > 5% |
| API 限流次数 | 容量 | > 100 次/小时 |
| 幻觉率 | 质量 | > 10%（通过 Eval） |

### 3. 成本优化策略

- 分层路由：简单请求用便宜模型，复杂的用贵的
- 缓存：相同查询返回缓存结果（省 80%+）
- Prompt 压缩：减少输入 Token
- 批处理：非实时任务用 Batch API（半价）

---

## 📎 参考链接

| 资源 | 链接 |
|------|------|
| AAS 底座 | https://github.com/autonomous-agent-stack/autonomous-agent-stack |
| LangSmith | https://smith.langchain.com |
| Langfuse | https://github.com/langfuse/langfuse |
| Weave | https://github.com/wandb/weave |
| Phoenix | https://github.com/Arize-ai/phoenix |
| OpenTelemetry | https://opentelemetry.io |
| LangGraph Cloud | https://langchain-ai.github.io/langgraph/concepts/langgraph-cloud/ |

---

*上一篇：[A2A 协议](../02-frameworks/a2a-agent-to-agent-protocol.md) | 下一篇：[Agent 安全与护栏](./agent-safety-guardrails.md)*
