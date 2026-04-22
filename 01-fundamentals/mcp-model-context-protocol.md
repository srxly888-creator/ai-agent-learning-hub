# 🔌 MCP (Model Context Protocol) — AI Agent 的万能插头

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **发布方** | Anthropic |
| **发布时间** | 2024 年 11 月 |
| **协议类型** | AI Agent 工具集成开放协议 |
| **GitHub** | https://github.com/modelcontextprotocol |
| **官网** | https://modelcontextprotocol.io |
| **Python SDK** | `pip install mcp` |
| **TypeScript SDK** | `npm install @modelcontextprotocol/sdk` |
| **规范** | https://spec.modelcontextprotocol.io |

---

## 🎯 一句话理解

> **MCP 就像 AI 的 USB-C 接口——不管什么工具，插上就能用。以前每个 AI 工具都要单独写集成代码，现在用 MCP 标准协议，一个 Server 适配所有 AI 客户端。**

---

## 🔍 为什么需要 MCP

### 当前 AI 工具集成的问题

| 问题 | 描述 | 例子 |
|------|------|------|
| **重复开发** | 每个工具都要为每个 AI 写适配器 | GitHub 工具要写 Claude 版、GPT 版、Gemini 版... |
| **协议碎片化** | 各家标准不统一 | OpenAI 用 Function Calling，Anthropic 用 Tools API |
| **维护成本高** | API 变了要改 N 个适配器 | GitHub API 改版 → 所有集成全挂 |
| **生态割裂** | 工具无法跨平台共享 | 我写的工具你用不了 |

### MCP 怎么解决的

```
❌ 以前（N×M 问题）:
  AI 客户端A ←→ 工具X适配器
  AI 客户端A ←→ 工具Y适配器
  AI 客户端B ←→ 工具X适配器
  AI 客户端B ←→ 工具Y适配器
  ... N 个客户端 × M 个工具 = N×M 个适配器

✅ 有了 MCP（标准化）:
  AI 客户端A ←→ MCP Client ←→ MCP Server（工具X）
  AI 客户端B ←→ MCP Client ←→ MCP Server（工具X）
  ... N 个客户端 + M 个工具 = N+M 个组件
```

### 类比理解

| 类比 | MCP 对应 |
|------|---------|
| USB-C 统一了充电接口 | MCP 统一了 AI 工具接口 |
| HTTP 统一了网页通信 | MCP 统一了 Agent-Tool 通信 |
| Docker 镜像标准 | MCP Server 是标准化的"工具镜像" |

---

## 🏗️ 核心架构

### 三层架构

```
┌─────────────────────────────────────────────────┐
│                   Host（宿主）                    │
│  Claude Desktop / VS Code / IDE / 自定义应用     │
│                                                   │
│  ┌─────────────────────────────────────────┐     │
│  │           MCP Client（客户端）            │     │
│  │  管理 1:N 个 Server 连接                  │     │
│  │  协议：JSON-RPC 2.0                      │     │
│  └──────┬──────────┬──────────┬────────────┘     │
│         │          │          │                    │
└─────────┼──────────┼──────────┼────────────────────┘
          │          │          │
    ┌─────┴───┐ ┌────┴────┐ ┌──┴──────┐
    │ Server A│ │ Server B│ │ Server C│
    │ GitHub  │ │ SQLite  │ │ Weather │
    │(stdio)  │ │(stdio)  │ │(SSE)    │
    └─────────┘ └─────────┘ └─────────┘
```

### 三种通信方式

| 方式 | 说明 | 适用场景 |
|------|------|---------|
| **stdio** | 通过标准输入/输出通信 | 本地工具，最常用 |
| **SSE (Server-Sent Events)** | HTTP 长连接 | 远程工具、云服务 |
| **Streamable HTTP** | HTTP 请求/响应流 | 2026 新增，SSE 的升级版 |

### Server 提供的三种能力

| 能力 | 说明 | 类比 |
|------|------|------|
| **Tools（工具）** | Agent 可以调用的函数 | 手机的 App |
| **Resources（资源）** | Agent 可以读取的数据 | 手机的照片/文件 |
| **Prompts（提示词）** | Agent 可以使用的模板 | 手机的快捷指令 |

---

## ⚔️ MCP vs 其他方案

| 特性 | MCP | Function Calling | OpenAPI | ChatGPT Plugins | LangChain Tools |
|------|-----|-----------------|---------|----------------|----------------|
| **标准化** | ✅ 开放标准 | ❌ 各家不同 | ✅ REST 标准 | ❌ 仅 OpenAI | ❌ 框架绑定 |
| **双向通信** | ✅ Server 可推送 | ❌ 单向 | ❌ 单向 | ❌ 单向 | ❌ 单向 |
| **资源访问** | ✅ Resources | ❌ | ✅ | ❌ | ❌ |
| **提示词模板** | ✅ Prompts | ❌ | ❌ | ❌ | ❌ |
| **工具发现** | ✅ 自动发现 | ❌ 手动注册 | ✅ Swagger | ✅ | ❌ |
| **跨客户端** | ✅ 任何 MCP Client | ❌ 绑定模型 | ✅ 任何 HTTP | ❌ 仅 ChatGPT | ❌ 仅 LangChain |
| **生态共享** | ✅ Server 可复用 | ❌ | ⚠️ 有限 | ❌ | ⚠️ 有限 |

---

## 🚀 快速上手

### Python MCP Server — 天气查询

```python
# weather_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """查询城市天气"""
    # 模拟天气数据
    weather_db = {
        "北京": "晴天 25°C, 湿度 40%",
        "上海": "多云 22°C, 湿度 65%",
        "深圳": "阵雨 28°C, 湿度 80%",
    }
    return weather_db.get(city, f"{city}的天气数据暂不可用")

@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """查询未来几天天气预报"""
    return f"{city}未来{days}天天气预报：多云转晴，气温18-26°C"

@mcp.resource("weather://alerts")
async def get_alerts() -> str:
    """获取天气预警信息"""
    return "今日无天气预警"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

运行：
```bash
pip install mcp
python weather_server.py
```

### Claude Desktop 配置

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    }
  }
}
```

配置文件位置：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### TypeScript MCP Server

```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "calculator-server",
  version: "1.0.0",
});

server.tool("calculate", "执行数学计算", {
  expression: { type: "string", description: "数学表达式" },
}, async ({ expression }) => {
  try {
    // 安全计算（仅允许数字和基本运算符）
    const sanitized = expression.replace(/[^0-9+\-*/().%\s]/g, "");
    const result = Function(`"use strict"; return (${sanitized})`)();
    return { content: [{ type: "text", text: `${expression} = ${result}` }] };
  } catch (e) {
    return { content: [{ type: "text", text: `计算错误: ${e}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 🔥 热门 MCP Server 推荐

### 官方 Servers

| Server | 功能 | Stars |
|--------|------|-------|
| [filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | 文件系统读写 | ⭐⭐⭐⭐⭐ |
| [github](https://github.com/modelcontextprotocol/servers/tree/main/src/github) | GitHub API 集成 | ⭐⭐⭐⭐⭐ |
| [postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | PostgreSQL 数据库 | ⭐⭐⭐⭐ |
| [sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) | SQLite 数据库 | ⭐⭐⭐⭐ |
| [puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) | 浏览器自动化 | ⭐⭐⭐⭐ |
| [brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search) | Brave 搜索引擎 | ⭐⭐⭐⭐ |
| [memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | 知识图谱记忆 | ⭐⭐⭐⭐ |
| [slack](https://github.com/modelcontextprotocol/servers/tree/main/src/slack) | Slack 集成 | ⭐⭐⭐ |
| [google-maps](https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps) | Google Maps | ⭐⭐⭐ |

### 社区热门

| Server | 功能 | GitHub |
|--------|------|--------|
| **notion-mcp** | Notion 读写 | 搜索 `notion mcp` |
| **linear-mcp** | Linear 项目管理 | 搜索 `linear mcp` |
| **figma-mcp** | Figma 设计稿 | 搜索 `figma mcp` |
| **sentry-mcp** | 错误监控 | 搜索 `sentry mcp` |
| **playwright-mcp** | 浏览器测试 | 搜索 `playwright mcp` |

### 发现更多 Server

- **Smithery**: https://smithery.ai — MCP Server 目录，可一键安装
- **MCP Hub**: https://github.com/punkpeye/mcp-hub — 社区维护的 Server 列表
- **GitHub 搜索**: `topic:mcp-server` 或 `topic:mcp`

```bash
# 一键安装 Smithery 上的 Server
npx @smithery/cli install @modelcontextprotocol/server-github
```

---

## 🌐 MCP 生态现状（2026）

### 大厂支持情况

| 公司 | 支持方式 | 状态 |
|------|---------|------|
| **Anthropic** | Claude Desktop / Claude Code 原生支持 | ✅ 深度集成 |
| **OpenAI** | ChatGPT / Codex 支持 MCP | ✅ 2025 年加入 |
| **Google** | Gemini / AI Studio 支持 MCP | ✅ 2025 年加入 |
| **Cursor** | IDE 内置 MCP Client | ✅ 原生支持 |
| **Windsurf** | IDE 内置 MCP Client | ✅ 原生支持 |
| **VS Code** | GitHub Copilot 支持 MCP | ✅ 2025 年加入 |

### 规范版本

| 版本 | 时间 | 主要变化 |
|------|------|---------|
| **2024-11-05** | 2024.11 | 初始版本 |
| **2025-03-26** | 2025.03 | 新增 Streamable HTTP 传输 |
| **2025-06** | 2025.06 | 采样支持、元数据改进 |

### 社区规模

- GitHub `modelcontextprotocol` 组织: 20+ 官方 Server
- 社区 MCP Server: 1000+ 个
- Smithery 目录收录: 500+ 个可安装 Server
- MCP 协议已成为 AI 工具集成的事实标准

---

## ✅ 最佳实践

### 1. 安全考虑

```python
# ✅ 好的做法：限制文件访问范围
mcp = FastMCP("safe-fs-server")
mcp.settings.allowed_directories = ["/data/documents"]

# ❌ 坏的做法：开放整个文件系统
# mcp.settings.allowed_directories = ["/"]
```

| 安全措施 | 说明 |
|---------|------|
| **权限最小化** | Server 只申请必要的权限 |
| **沙箱执行** | 代码执行类 Server 使用沙箱 |
| **输入验证** | 所有用户输入都要验证 |
| **审计日志** | 记录所有 Tool 调用 |
| **敏感数据** | 不要在 Tool 描述中暴露内部信息 |

### 2. 性能优化

```python
# ✅ 连接复用：Server 启动时建立连接，而不是每次调用
class DatabaseServer:
    def __init__(self):
        self.pool = create_connection_pool()  # 启动时创建

    @mcp.tool()
    async def query(self, sql: str):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql)
```

### 3. 错误处理

```python
@mcp.tool()
async def search_web(query: str) -> str:
    """搜索网页内容"""
    try:
        results = await search_api(query)
        if not results:
            return "未找到相关结果，请尝试其他关键词"
        return format_results(results)
    except SearchAPIError as e:
        # 返回错误信息而不是抛异常
        return f"搜索服务暂时不可用: {e.message}"
    except Exception as e:
        return f"未知错误: {str(e)}"
```

### 4. 版本兼容

- 始终在 Server 响应中包含 `protocolVersion`
- 使用渐进式增强：新功能放在可选字段中
- 文档中注明最低支持的 MCP 版本

---

## 📎 参考链接

| 资源 | 链接 |
|------|------|
| MCP 官方规范 | https://spec.modelcontextprotocol.io |
| MCP GitHub | https://github.com/modelcontextprotocol |
| 官方 Python SDK | https://github.com/modelcontextprotocol/python-sdk |
| 官方 TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk |
| Smithery（Server 目录） | https://smithery.ai |
| MCP Hub（社区列表） | https://github.com/punkpeye/mcp-hub |
| Anthropic MCP 文档 | https://docs.anthropic.com/en/docs/build-with-mcp |
| MCP 入门教程 | https://modelcontextprotocol.io/quickstart |

---

*下一篇：[Agent 设计模式大全](./agent-design-patterns.md)*
