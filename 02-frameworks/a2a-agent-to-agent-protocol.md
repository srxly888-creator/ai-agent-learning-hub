# 🤝 A2A (Agent-to-Agent) 协议 — 让 Agent 之间自由对话

## 📚 基本信息

- **发布方**: Google
- **发布时间**: 2025 年 4 月
- **协议类型**: Agent 互操作性开放协议
- **GitHub**: https://github.com/google/A2A
- **文档**: https://google.github.io/A2A/
- **规范**: https://github.com/google/A2A/blob/main/specification.md
- **Python SDK**: https://github.com/google/A2A/tree/main/python

---

## 🎯 一句话理解

> **A2A 让不同的 AI Agent 像人一样互相沟通协作，不管它们是谁开发的、用什么框架构建的。**

---

## 🔍 为什么需要 A2A

### 当前 Agent 生态的困境

在 A2A 出现之前，AI Agent 生态面临一个核心问题：

| 问题 | 描述 |
|------|------|
| **孤岛效应** | 每个 Agent 都是独立系统，无法互操作 |
| **定制集成** | 两个 Agent 想协作，必须写专门的集成代码 |
| **协议碎片** | LangChain Agent、AutoGen、CrewAI 各有各的通信方式 |
| **扩展困难** | N 个 Agent 需要 N×(N-1)/2 个集成点 |
| **供应商锁定** | 用了某个框架就很难切换到另一个 |

### 类比理解

```
互联网之前的世界：
  电话公司 A 的用户 ❌ 不能呼叫 电话公司 B 的用户

互联网之后的世界：
  任何人 ✅ 都可以通过标准协议（TCP/IP）互相通信

Agent 世界之前：
  Agent A ❌ 不能和 Agent B 协作（不同框架）

A2A 之后的世界：
  任何 Agent ✅ 都可以通过 A2A 协议互相通信
```

---

## 📐 A2A vs MCP：核心区别

这是理解 A2A 最重要的概念：

### MCP = Agent ↔ Tool（模型上下文协议）

```
┌──────────┐         ┌──────────┐
│  Agent   │ ◄─────► │   Tool   │
│ (客户端)  │  MCP   │ (服务端)  │
└──────────┘         └──────────┘

Agent 调用工具获取数据或执行操作
方向：单向请求-响应
关系：Agent 控制，Tool 服从
```

### A2A = Agent ↔ Agent（Agent 间协议）

```
┌──────────┐         ┌──────────┐
│  Agent A │ ◄─────► │  Agent B │
│ (客户端)  │  A2A   │ (服务端)  │
└──────────┘         └──────────┘
         ◄─────►
┌──────────┐
│  Agent C │
└──────────┘

Agent 之间平等对话、协商、分工
方向：双向、多轮、多 Agent
关系：对等协作
```

### 对比表

| 维度 | MCP | A2A |
|------|-----|-----|
| **全称** | Model Context Protocol | Agent-to-Agent Protocol |
| **通信方** | Agent ↔ Tool/Server | Agent ↔ Agent |
| **关系** | 主从（Agent 控制工具） | 对等（Agent 协作） |
| **交互模式** | 请求-响应 | 多轮对话、异步任务 |
| **状态管理** | 无状态 | 有状态（Task 生命周期） |
| **发现机制** | 需要手动配置 | Agent Card 自描述 |
| **核心对象** | Tool, Resource, Prompt | Task, Message, Agent Card |
| **适用场景** | 给 Agent 接工具 | 多 Agent 协作 |

### 两者互补

```
┌─────────────────────────────────────────────────┐
│              AI Agent 生态系统                     │
│                                                   │
│   ┌─────────┐  MCP   ┌──────────┐               │
│   │ Agent A  │◄──────►│ Database │               │
│   └────┬─────┘       └──────────┘               │
│        │ A2A                                     │
│        ▼                                         │
│   ┌─────────┐  MCP   ┌──────────┐               │
│   │ Agent B  │◄──────►│  API 服务  │               │
│   └─────────┘       └──────────┘               │
│                                                   │
│   MCP：Agent 接工具  │  A2A：Agent 互相协作       │
└─────────────────────────────────────────────────┘
```

---

## 🏗️ A2A 协议架构

### 整体架构图

```
┌──────────────────────────────────────────────────────────┐
│                     A2A 协议层                            │
│                                                           │
│  ┌──────────┐                          ┌──────────┐      │
│  │ Agent A  │   ┌────────────────┐    │  Agent B  │      │
│  │          │   │   HTTP/HTTPS   │    │          │      │
│  │ ┌──────┐ │   │  JSON-RPC 2.0  │    │ ┌──────┐ │      │
│  │ │ Client│ │──▶│                │◀──▶│ │Server│ │      │
│  │ └──────┘ │   │                │    │ └──────┘ │      │
│  │          │   └────────────────┘    │          │      │
│  │ ┌──────┐ │                          │ ┌──────┐ │      │
│  │ │Server│ │◀────────────────────────▶│ │Client│ │      │
│  │ └──────┘ │                          │ └──────┘ │      │
│  └──────────┘                          └──────────┘      │
│       │                                      │           │
│  ┌────▼────┐                           ┌────▼────┐      │
│  │Agent Card│                           │Agent Card│      │
│  │(发现机制) │                           │(发现机制) │      │
│  └─────────┘                           └─────────┘      │
└──────────────────────────────────────────────────────────┘
```

### 通信方式

A2A 使用 **HTTP + JSON-RPC 2.0** 作为传输层：

```json
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "id": "unique-request-id",
  "params": {
    "id": "task-id",
    "sessionId": "session-id",
    "message": {
      "role": "user",
      "parts": [
        { "type": "text", "text": "请帮我分析这份报告" }
      ]
    }
  }
}
```

---

## 📇 Agent Card — Agent 的"名片"

Agent Card 是 A2A 协议中最核心的发现机制。每个 Agent 都会暴露一个 Agent Card，告诉其他 Agent：

> **"我是谁，我能做什么，怎么和我交互"**

### Agent Card 格式

```json
{
  "name": "Code Review Agent",
  "description": "专业的代码审查 Agent，支持 Python、JavaScript、Go 等语言",
  "url": "https://code-review.example.com/a2a",
  "provider": {
    "organization": "Example Corp",
    "url": "https://example.com"
  },
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": [
      {
        "type": "oauth2",
        "authorizationUrl": "https://auth.example.com/authorize",
        "tokenUrl": "https://auth.example.com/token",
        "scopes": ["read", "write"]
      }
    ]
  },
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "code-review",
      "name": "代码审查",
      "description": "审查代码质量、安全漏洞、性能问题",
      "tags": ["code", "review", "security", "performance"],
      "examples": [
        "请审查这段 Python 代码的性能问题",
        "检查这个函数是否有安全漏洞"
      ]
    },
    {
      "id": "code-explain",
      "name": "代码解释",
      "description": "解释复杂代码逻辑",
      "tags": ["code", "explain", "documentation"]
    }
  ]
}
```

### Agent Card 字段详解

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | Agent 名称 |
| `description` | ✅ | Agent 描述 |
| `url` | ✅ | A2A 服务端点 URL |
| `version` | ✅ | 版本号 |
| `provider` | ❌ | 提供者信息 |
| `capabilities` | ✅ | 能力声明 |
| `authentication` | ❌ | 认证方式 |
| `skills` | ❌ | 技能列表 |
| `defaultInputModes` | ❌ | 支持的输入格式 |
| `defaultOutputModes` | ❌ | 支持的输出格式 |

### 发现 Agent Card

```bash
# GET 请求获取 Agent Card
curl https://code-review.example.com/.well-known/agent.json

# 或直接访问 A2A 端点
curl https://code-review.example.com/a2a/agent-card
```

---

## 🔄 Task 生命周期

Task 是 A2A 协议的核心抽象，代表 Agent 之间的一个协作任务。

### 状态机

```
                    ┌─────────┐
          创建任务   │         │  完成
        ──────────▶│ created │────────▶ completed
                    │         │
                    └────┬────┘
                         │ 开始工作
                         ▼
                    ┌─────────┐
                    │ working │◀──────┐
                    └────┬────┘       │
                         │           │
                    ┌────▼────┐  继续 │
              需要  │         │◀──────┘
           输入时  │         │
          ─────────│ input-  │
                    │ required│
                    └─────────┘
                         │
                    ┌────▼────┐
              Agent  │         │
              拒绝时 │ rejected│
                    └─────────┘
                         │
                    ┌────▼────┐
              取消时 │         │
                    │ canceled│
                    └─────────┘
                         │
                    ┌────▼────┐
              失败时 │         │
                    │ failed  │
                    └─────────┘
                         │
                    ┌────▼────┐
              需要用户 │         │
              确认时  │auth-    │
                    │required │
                    └─────────┘
```

### Task 状态说明

| 状态 | 说明 |
|------|------|
| `created` | 任务已创建，等待 Agent 处理 |
| `working` | Agent 正在处理任务 |
| `input-required` | Agent 需要更多信息才能继续 |
| `completed` | 任务成功完成 |
| `failed` | 任务执行失败 |
| `rejected` | Agent 拒绝执行任务 |
| `canceled` | 任务被取消 |
| `auth-required` | 需要用户授权才能继续 |

### Task 对象结构

```json
{
  "id": "task-abc123",
  "sessionId": "session-xyz",
  "status": {
    "state": "working",
    "timestamp": "2025-04-22T10:00:00Z"
  },
  "message": {
    "role": "agent",
    "parts": [
      {
        "type": "text",
        "text": "我正在分析代码，请稍候..."
      }
    ]
  },
  "history": [
    {
      "role": "user",
      "parts": [
        { "type": "text", "text": "审查这段代码" }
      ]
    }
  ],
  "artifacts": [
    {
      "name": "review-report",
      "type": "text/markdown",
      "parts": [
        {
          "type": "text",
          "text": "# 审查报告\n\n## 发现的问题\n..."
        }
      ]
    }
  ]
}
```

---

## 📡 核心方法（JSON-RPC）

A2A 定义了一组 JSON-RPC 方法：

### 任务管理

| 方法 | 说明 |
|------|------|
| `tasks/send` | 发送新任务或消息 |
| `tasks/sendSubscribe` | 发送任务并订阅流式更新（SSE） |
| `tasks/get` | 获取任务状态和内容 |
| `tasks/cancel` | 取消正在执行的任务 |

### 消息部分类型（Message Parts）

```json
// 文本
{ "type": "text", "text": "你好" }

// 文件
{
  "type": "file",
  "name": "report.pdf",
  "mimeType": "application/pdf",
  "bytes": "base64-encoded-content"
}

// 数据（结构化数据）
{
  "type": "data",
  "data": { "key": "value" },
  "metadata": { "source": "database" }
}
```

---

## 💻 代码示例

### 示例 1：最简单的 A2A Client

```python
# pip install a2a-sdk
import asyncio
from a2a.client import A2AClient

async def main():
    # 连接到远程 Agent
    client = A2AClient("https://code-review.example.com/a2a")
    
    # 获取 Agent Card
    card = await client.get_agent_card()
    print(f"Agent: {card.name}")
    print(f"技能: {[s.name for s in card.skills]}")
    
    # 发送任务
    task = await client.send_task(
        message="请审查这段 Python 代码的性能问题:\n```python\ndef slow(items):\n    result = []\n    for item in items:\n        result.append(item * 2)\n    return result\n```"
    )
    
    print(f"任务状态: {task.status.state}")
    print(f"结果: {task.message.parts[0].text}")

asyncio.run(main())
```

### 示例 2：创建一个 A2A Server（Agent）

```python
from a2a.server import A2AServer
from a2a.types import Task, Message, TextPart, AgentCard

# 定义 Agent Card
agent_card = AgentCard(
    name="翻译 Agent",
    description="中英文互译 Agent",
    version="1.0.0",
    url="http://localhost:8000/a2a",
    skills=[
        {
            "id": "translate",
            "name": "翻译",
            "description": "中英文互译",
            "tags": ["translation", "中文", "English"]
        }
    ]
)

# 创建 Server
app = A2AServer(agent_card=agent_card)

@app.on_task
async def handle_task(task: Task) -> Task:
    # 提取用户消息
    user_text = task.message.parts[0].text
    
    # 调用 LLM 进行翻译
    translated = await translate_with_llm(user_text)
    
    # 返回结果
    return Task(
        id=task.id,
        status={"state": "completed"},
        message=Message(
            role="agent",
            parts=[TextPart(text=translated)]
        )
    )

# 启动服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

### 示例 3：流式响应

```python
import asyncio
from a2a.client import A2AClient

async def stream_example():
    client = A2AClient("https://research-agent.example.com/a2a")
    
    # 流式接收任务更新
    async for event in client.send_task_stream(
        message="帮我研究 RAG 技术的最新进展"
    ):
        if event.type == "task_update":
            print(f"[状态] {event.task.status.state}")
        elif event.type == "message":
            print(f"[消息] {event.message.parts[0].text}", end="", flush=True)

asyncio.run(stream_example())
```

### 示例 4：多 Agent 协作

```python
import asyncio
from a2a.client import A2AClient

async def multi_agent_workflow():
    # 连接多个 Agent
    researcher = A2AClient("https://research.example.com/a2a")
    writer = A2AClient("https://writer.example.com/a2a")
    reviewer = A2AClient("https://review.example.com/a2a")
    
    # Step 1: 研究员 Agent 搜索资料
    research_task = await researcher.send_task(
        message="搜索 2025 年 AI Agent 框架的最新进展"
    )
    research_result = research_task.message.parts[0].text
    
    # Step 2: 写作 Agent 根据资料写文章
    writing_task = await writer.send_task(
        message=f"基于以下资料写一篇技术文章：\n{research_result}"
    )
    article = writing_task.message.parts[0].text
    
    # Step 3: 审阅 Agent 审查文章
    review_task = await reviewer.send_task(
        message=f"审查以下文章的质量：\n{article}"
    )
    review = review_task.message.parts[0].text
    
    return {
        "research": research_result,
        "article": article,
        "review": review
    }

result = asyncio.run(multi_agent_workflow())
```

### 示例 5：用 HTTP 原生调用

```bash
# 1. 获取 Agent Card
curl -s https://research-agent.example.com/.well-known/agent.json | jq .

# 2. 发送任务
curl -X POST https://research-agent.example.com/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tasks/send",
    "id": "req-001",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          { "type": "text", "text": "搜索最新的 AI 新闻" }
        ]
      }
    }
  }'

# 3. 流式订阅（SSE）
curl -X POST https://research-agent.example.com/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tasks/sendSubscribe",
    "id": "req-002",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          { "type": "text", "text": "写一篇 AI 文章" }
        ]
      }
    }
  }'
```

---

## 🌍 生态现状

### 已支持的框架和工具

| 项目/公司 | 支持方式 | 说明 |
|-----------|----------|------|
| **Google** | 原生 | 协议发起者，提供参考实现 |
| **LangChain** | 集成 | 通过 langchain-a2a 包支持 |
| **Microsoft AutoGen** | 集成 | 多 Agent 框架原生支持 |
| **CrewAI** | 集成 | Agent 团队协作框架 |
| **OpenAI Agents SDK** | 探索中 | OpenAI 官方 Agent 框架 |
| **IBM** | 支持 | 企业级 Agent 平台 |

### 官方 SDK 结构

```
google/A2A/
├── specification.md      # 协议规范
├── python/               # Python SDK
│   ├── a2a-client/
│   └── a2a-server/
├── typescript/           # TypeScript SDK
│   ├── a2a-client/
│   └── a2a-server/
├── samples/              # 示例代码
│   ├── echo-agent/
│   ├── research-agent/
│   └── multi-agent/
└── docs/                 # 文档
```

### A2A 生态全景

```
┌─────────────────────────────────────────────────┐
│                 A2A 生态                          │
│                                                   │
│  ┌───────────────────────────────────────────┐   │
│  │            Agent 框架层                    │   │
│  │  LangChain  │ AutoGen │ CrewAI │ 自定义    │   │
│  └──────────────────┬────────────────────────┘   │
│                      │ A2A 协议                    │
│  ┌──────────────────▼────────────────────────┐   │
│  │            通信层                          │   │
│  │  HTTP/HTTPS + JSON-RPC 2.0 + SSE          │   │
│  └──────────────────┬────────────────────────┘   │
│                      │                             │
│  ┌──────────────────▼────────────────────────┐   │
│  │            Agent 注册/发现层                │   │
│  │  Agent Card │ .well-known │ 注册中心        │   │
│  └──────────────────┬────────────────────────┘   │
│                      │                             │
│  ┌──────────────────▼────────────────────────┐   │
│  │            Agent 实例                       │   │
│  │  代码审查 │ 研究员 │ 翻译 │ 数据分析 │ ...   │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 🆚 A2A vs 其他 Agent 通信方案

| 方案 | 类型 | 优势 | 劣势 |
|------|------|------|------|
| **A2A** | 开放标准 | 跨框架互操作、标准化 | 较新，生态还在发展 |
| **AutoGen 原生** | 框架内置 | 深度集成 | 仅限 AutoGen |
| **CrewAI** | 框架内置 | 简单易用 | 仅限 CrewAI |
| **自定义 API** | 私有 | 完全可控 | 无互操作性 |
| **LangGraph** | 框架内置 | 状态管理强 | 仅限 LangChain 生态 |

---

## 🎯 A2A 的核心价值

### 1. 互操作性（Interoperability）

```
之前：Agent A (LangChain) ──✕── Agent B (AutoGen)
之后：Agent A (LangChain) ──A2A── Agent B (AutoGen) ✅
```

### 2. 可发现性（Discoverability）

```
之前：需要知道 Agent 的 API 文档才能调用
之后：通过 Agent Card 自动发现能力
```

### 3. 标准化（Standardization）

```
之前：每个框架定义自己的消息格式
之后：统一的消息格式、任务模型、状态机
```

### 4. 可扩展性（Scalability）

```
之前：N 个 Agent 需要 N×(N-1)/2 个集成
之后：每个 Agent 只需要实现 A2A 协议
```

---

## ⚠️ 当前局限与挑战

| 挑战 | 说明 | 预期解决时间 |
|------|------|-------------|
| **生态早期** | 支持的框架和 Agent 数量还不多 | 2025 下半年 |
| **性能开销** | JSON-RPC + HTTP 比 gRPC 重 | 优化中 |
| **安全模型** | 认证/授权机制还在完善中 | 持续 |
| **复杂任务** | 多 Agent 长链路的错误处理复杂 | 需要最佳实践 |
| **离线支持** | 当前依赖 HTTP，无离线模式 | 未计划 |

---

## 🚀 快速上手指南

### Step 1: 安装 SDK

```bash
# Python
pip install a2a-sdk

# TypeScript
npm install @google/a2a
```

### Step 2: 创建你的第一个 A2A Agent

```python
# server.py
from a2a.server import A2AServer
from a2a.types import AgentCard, Task, Message, TextPart

card = AgentCard(
    name="Hello Agent",
    description="一个简单的问候 Agent",
    version="1.0.0",
    url="http://localhost:8000/a2a",
)

app = A2AServer(agent_card=card)

@app.on_task
async def handle(task: Task) -> Task:
    text = task.message.parts[0].text
    return Task(
        id=task.id,
        status={"state": "completed"},
        message=Message(
            role="agent",
            parts=[TextPart(text=f"你好！你说了：{text}")]
        )
    )

app.run(port=8000)
```

### Step 3: 从另一个 Agent 调用它

```python
# client.py
import asyncio
from a2a.client import A2AClient

async def main():
    client = A2AClient("http://localhost:8000/a2a")
    card = await client.get_agent_card()
    print(f"发现 Agent: {card.name}")
    
    task = await client.send_task(message="Hello from client!")
    print(f"回复: {task.message.parts[0].text}")

asyncio.run(main())
```

---

## 💡 最佳实践

### 1. 设计好的 Agent Card

```python
# ✅ 好的 Agent Card
AgentCard(
    name="Code Security Scanner",
    description="扫描代码中的安全漏洞，支持 OWASP Top 10 检测",
    skills=[{
        "id": "security-scan",
        "name": "安全扫描",
        "tags": ["security", "vulnerability", "sast"],
        "examples": [
            "扫描这个 Python 文件的安全漏洞",
            "检查 SQL 注入风险"
        ]
    }]
)

# ❌ 差的 Agent Card
AgentCard(
    name="AI Agent",
    description="能做很多事情",
    # 没有技能描述，没有示例
)
```

### 2. 合理使用 Task 状态

```python
# ✅ 使用 input-required 让用户补充信息
if not has_enough_context(task.message):
    return Task(
        id=task.id,
        status={"state": "input-required"},
        message=Message(
            role="agent",
            parts=[TextPart(text="需要更多上下文：请提供目标语言")]
        )
    )

# ✅ 使用 auth-required 处理敏感操作
if is_sensitive_operation(task.message):
    return Task(
        id=task.id,
        status={"state": "auth-required"},
        message=Message(
            role="agent",
            parts=[TextPart(text="此操作需要管理员权限确认")]
        )
    )
```

### 3. 错误处理

```python
try:
    task = await client.send_task(message="do something")
except A2AConnectionError:
    print("Agent 不可达")
except A2AAuthenticationError:
    print("认证失败")
except A2ATimeoutError:
    print("任务超时")
except A2AError as e:
    print(f"A2A 错误: {e}")
```

---

## 🔗 相关资源

### 官方资源

- **GitHub 仓库**: https://github.com/google/A2A
- **协议规范**: https://github.com/google/A2A/blob/main/specification.md
- **官方文档**: https://google.github.io/A2A/
- **Python SDK**: https://github.com/google/A2A/tree/main/python
- **TypeScript SDK**: https://github.com/google/A2A/tree/main/typescript

### 社区资源

- **A2A 示例集合**: https://github.com/google/A2A/tree/main/samples
- **MCP 协议**: https://modelcontextprotocol.io/（互补协议）
- **LangChain A2A 集成**: https://python.langchain.com/docs/integrations/tools/a2a

---

## 📝 总结

| 维度 | 关键点 |
|------|--------|
| **是什么** | Google 发布的 Agent 互操作开放协议 |
| **解决什么** | 让不同框架的 Agent 能互相通信协作 |
| **核心机制** | Agent Card（发现）+ Task（交互）+ JSON-RPC（通信） |
| **与 MCP 关系** | 互补：MCP 管 Agent↔Tool，A2A 管 Agent↔Agent |
| **当前状态** | 生态早期，快速发展中 |
| **适用场景** | 多 Agent 协作、Agent 市场编排、跨团队 Agent 集成 |

> **A2A 是 Agent 世界的 HTTP 协议** — 它不一定是最快的、最强大的，但它是最开放、最标准的。当每个 Agent 都说 A2A，整个生态就活了。

---

*最后更新：2026-04-22*
