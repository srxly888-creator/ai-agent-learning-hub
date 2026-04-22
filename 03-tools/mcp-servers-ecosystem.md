# MCP 服务器生态：从入门到自建

> Model Context Protocol 服务器大全，热门服务器详解 + 自建教程

## 📋 目录

- [前言](#前言)
- [一、MCP 协议快速回顾](#一mcp-协议快速回顾)
- [二、官方参考服务器](#二官方参考服务器)
- [三、热门第三方服务器详解](#三热门第三方服务器详解)
- [四、开发工具类服务器](#四开发工具类服务器)
- [五、数据与搜索类服务器](#五数据与搜索类服务器)
- [六、自建 MCP 服务器教程](#六自建-mcp-服务器教程)
- [七、配置与管理](#七配置与管理)
- [八、最佳实践](#八最佳实践)
- [九、总结](#九总结)

---

## 前言

MCP（Model Context Protocol）是 Anthropic 在 2024 年底推出的开放协议，让 AI 模型能通过标准化接口连接外部工具和数据源。

如果把 AI 模型比作"大脑"，那 MCP 服务器就是给大脑装上的"眼睛、耳朵和手"——让 AI 能读写文件、搜索网络、操作数据库、控制浏览器等。

> 💡 **小白提示**：如果你还不了解 MCP，建议先看 [《MCP 协议详解》](../01-fundamentals/mcp-model-context-protocol.md)。

---

## 一、MCP 协议快速回顾

### 1.1 架构一句话

```
AI 客户端（如 Claude Desktop） ←→ MCP 协议 ←→ MCP 服务器（提供工具和数据）
```

### 1.2 MCP 服务器能做什么？

```
📖 读文件         🔍 搜索网络       💾 操作数据库
📁 管理文件系统    🌐 抓取网页       🐙 操作 Git
🖥️ 控制浏览器     📊 查询 API       📝 记笔记
```

---

## 二、官方参考服务器

Anthropic 官方维护了几个参考实现，代码质量和稳定性最好。

### 2.1 Filesystem Server（文件系统）

**功能**：让 AI 读写本地文件和目录。

**安装配置**：

```json
// Claude Desktop 的 claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-filesystem",
        "/Users/you/projects"  // 允许访问的目录
      ]
    }
  }
}
```

**常用功能**：

```
可用工具：
  read_file          — 读取文件内容
  write_file         — 写入文件
  list_directory     — 列出目录内容
  create_directory   — 创建目录
  move_file          — 移动/重命名文件
  search_files       — 搜索文件
  get_file_info      — 获取文件信息
```

**安全建议**：只授权必要的目录，不要授权整个用户目录。

### 2.2 Sequential Thinking Server（顺序思考）

**功能**：让 AI 进行多步骤的推理和思考，适合复杂问题。

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sequential-thinking"]
    }
  }
}
```

**使用场景**：
- 复杂数学推理
- 多步逻辑分析
- 架构设计决策
- 问题排查诊断

**原理**：把大问题拆成小步骤，每步独立思考，逐步推进。

### 2.3 Memory Server（记忆服务器）

**功能**：给 AI 提供持久化记忆，跨会话记住信息。

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-memory"]
    }
  }
}
```

**可用工具**：
```
create_entities     — 创建记忆实体
search_entities     — 搜索记忆
create_relations    — 创建实体间关系
open_nodes          — 打开特定节点
```

**使用示例**：
```
用户：记住，我的项目使用 React + TypeScript + Tailwind
AI：✅ 已保存到记忆

（新会话）
用户：我的项目用什么技术栈？
AI：根据记忆，你的项目使用 React + TypeScript + Tailwind
```

---

## 三、热门第三方服务器详解

### 3.1 Fetch Server（网页抓取）

**功能**：抓取网页内容，让 AI 能阅读网络上的文章和页面。

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-fetch"]
    }
  }
}
```

**可用工具**：
```
fetch       — 抓取网页内容（返回 markdown）
```

**使用场景**：
- 阅读技术文档
- 获取新闻资讯
- 分析竞品网站
- 提取网页数据

```python
# 在代码中使用
import httpx
# MCP fetch 底层就是用 httpx 抓取网页
# 然后用 readability 提取正文
```

### 3.2 Git Server（Git 操作）

**功能**：让 AI 直接操作 Git 仓库。

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-git",
        "--repository", "/path/to/your/repo"
      ]
    }
  }
}
```

**可用工具**：
```
git_status          — 查看仓库状态
git_diff            — 查看变更
git_log             — 查看提交历史
git_commit          — 创建提交
git_create_branch   — 创建分支
git_checkout        — 切换分支
```

**实际应用**：
```
你：帮我看看最近5次提交改了什么
AI：[调用 git_log 和 git_diff]
   最近5次提交：
   1. feat: 添加用户认证模块 (3 files changed)
   2. fix: 修复登录页面bug (1 file changed)
   ...

你：帮我创建一个 feature/login-optimization 分支
AI：[调用 git_create_branch]
   ✅ 已创建分支 feature/login-optimization
```

### 3.3 Puppeteer Server（浏览器自动化）

**功能**：控制 Chrome 浏览器，进行网页操作。

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    }
  }
}
```

**可用工具**：
```
puppeteer_navigate     — 打开网页
puppeteer_screenshot   — 截图
puppeteer_click        — 点击元素
puppeteer_fill         — 填写表单
puppeteer_evaluate     — 执行JS代码
puppeteer_select       — 选择下拉菜单
```

**使用场景**：
- 自动化测试
- 网页数据采集
- 表单自动填写
- 生成网页截图

### 3.4 GitHub Server（GitHub 集成）

**功能**：操作 GitHub API，管理 Issues、PR、代码搜索等。

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**可用工具**：
```
search_repositories     — 搜索仓库
get_file_contents       — 获取文件内容
create_issue            — 创建 Issue
list_issues             — 列出 Issues
create_pull_request     — 创建 PR
search_code             — 搜索代码
```

---

## 四、开发工具类服务器

### 4.1 SQLite Server（数据库操作）

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic/mcp-server-sqlite",
        "--db-path", "/path/to/your/database.db"
      ]
    }
  }
}
```

**功能**：让 AI 直接查询和操作 SQLite 数据库。

```
可用工具：
  read_query    — 执行 SELECT 查询
  write_query   — 执行 INSERT/UPDATE/DELETE
  list_tables   — 列出所有表
  describe_table — 查看表结构
```

### 4.2 PostgreSQL Server

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres", "postgresql://..."]
    }
  }
}
```

### 4.3 Docker Server

```json
{
  "mcpServers": {
    "docker": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-docker"]
    }
  }
}
```

**功能**：管理 Docker 容器和镜像。

---

## 五、数据与搜索类服务器

### 5.1 Brave Search Server

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_api_key"
      }
    }
  }
}
```

### 5.2 Slack Server

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T..."
      }
    }
  }
}
```

### 5.3 Google Maps Server

```json
{
  "mcpServers": {
    "google-maps": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-google-maps"],
      "env": {
        "GOOGLE_MAPS_API_KEY": "your_key"
      }
    }
  }
}
```

---

## 六、自建 MCP 服务器教程

### 6.1 用 Python 自建（推荐）

```bash
pip install mcp
```

```python
# my_server.py — 一个简单的计算器 MCP 服务器
from mcp.server.fastmcp import FastMCP

# 创建服务器
mcp = FastMCP("my-calculator")

# 定义工具
@mcp.tool()
def add(a: float, b: float) -> float:
    """两数相加"""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """两数相乘"""
    return a * b

@mcp.tool()
def calculate(expression: str) -> float:
    """
    计算数学表达式
    示例: "2 + 3 * 4"
    """
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"计算错误: {e}"

# 定义资源（让AI能读取数据）
@mcp.resource("config://app")
def get_config() -> str:
    """获取应用配置"""
    return "应用版本: 1.0.0\n最大计算精度: 浮点数"

# 启动服务器
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 6.2 用 TypeScript 自建

```bash
npm init -y
npm install @modelcontextprotocol/sdk
```

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 注册工具
server.setRequestHandler(
  { method: "tools/list" },
  async () => ({
    tools: [
      {
        name: "get_weather",
        description: "获取指定城市的天气信息",
        inputSchema: {
          type: "object",
          properties: {
            city: { type: "string", description: "城市名称" }
          },
          required: ["city"]
        }
      }
    ]
  })
);

server.setRequestHandler(
  { method: "tools/call" },
  async (request) => {
    const { name, arguments: args } = request.params;
    if (name === "get_weather") {
      const weather = await fetchWeather(args.city);
      return { content: [{ type: "text", text: weather }] };
    }
  }
);

// 启动
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 6.3 自建进阶：带状态的天气服务器

```python
# weather_server.py
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    获取指定城市的当前天气
    
    Args:
        city: 城市名称，如"北京"、"上海"
    
    Returns:
        天气信息字符串
    """
    # 使用免费的天气API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://wttr.in/{city}?format=j1"
        )
        data = response.json()
    
    current = data["current_condition"][0]
    return f"""
    {city} 当前天气：
    温度：{current['temp_C']}°C
    体感温度：{current['FeelsLikeC']}°C
    天气：{current['weatherDesc'][0]['value']}
    湿度：{current['humidity']}%
    风速：{current['windspeedKmph']} km/h
    """

@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """
    获取天气预报
    
    Args:
        city: 城市名称
        days: 预报天数（1-3）
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://wttr.in/{city}?format=j1"
        )
        data = response.json()
    
    result = f"{city} 未来{days}天预报：\n"
    for day in data["weather"][:days]:
        result += f"""
  {day['date']}:
    最高温：{day['maxtempC']}°C
    最低温：{day['mintempC']}°C
    天气：{day['hourly'][4]['weatherDesc'][0]['value']}
"""
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 6.4 配置自建服务器

```json
{
  "mcpServers": {
    "my-calculator": {
      "command": "python",
      "args": ["/path/to/my_server.py"]
    },
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    }
  }
}
```

---

## 七、配置与管理

### 7.1 Claude Desktop 配置文件位置

```
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
```

### 7.2 多服务器组合配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/Users/me/projects"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-fetch"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sqlite", "--db-path", "./mydb.db"]
    },
    "my-custom": {
      "command": "python",
      "args": ["/Users/me/mcp_servers/my_server.py"]
    }
  }
}
```

### 7.3 调试 MCP 服务器

```bash
# 手动测试服务器（stdio 模式）
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python my_server.py

# 使用 MCP Inspector 调试
npx @anthropic/mcp-inspector python my_server.py
```

---

## 八、最佳实践

### 8.1 安全原则

```
1. 最小权限：只授权必要的目录和操作
2. 敏感数据：不要在配置文件中明文存储密钥
3. 输入验证：自建服务器一定要验证输入
4. 沙箱执行：代码执行类工具要在沙箱中运行
5. 审计日志：记录所有工具调用
```

### 8.2 性能优化

```python
# 1. 使用缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_query(query: str) -> str:
    """带缓存的结果"""
    return do_expensive_work(query)

# 2. 异步操作
@mcp.tool()
async def fetch_data(url: str) -> str:
    """异步获取数据，不阻塞其他请求"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### 8.3 服务器设计原则

```
1. 工具描述要清晰：AI根据描述决定是否调用
2. 输入输出要简单：用字符串或简单JSON
3. 错误处理要友好：返回有意义的错误信息
4. 幂等性：同样的输入应该返回同样的结果
5. 超时设置：避免工具调用卡死
```

---

## 九、总结

MCP 服务器生态正在快速增长，以下是最常用的服务器速查表：

| 类别 | 服务器 | 功能 | 推荐指数 |
|------|--------|------|---------|
| 文件 | filesystem | 读写文件 | ⭐⭐⭐⭐⭐ |
| 网络 | fetch | 抓取网页 | ⭐⭐⭐⭐⭐ |
| 版本控制 | git | Git操作 | ⭐⭐⭐⭐⭐ |
| 浏览器 | puppeteer | 浏览器自动化 | ⭐⭐⭐⭐ |
| 数据库 | sqlite | 数据库查询 | ⭐⭐⭐⭐ |
| 开发 | github | GitHub集成 | ⭐⭐⭐⭐ |
| 搜索 | brave-search | 网络搜索 | ⭐⭐⭐⭐ |
| 思考 | sequential-thinking | 顺序推理 | ⭐⭐⭐ |
| 记忆 | memory | 持久化记忆 | ⭐⭐⭐⭐ |

**自建三步走**：
1. ✅ 用 `FastMCP`（Python）或 `@modelcontextprotocol/sdk`（TS）
2. ✅ 用 `@mcp.tool()` 定义工具
3. ✅ 配置到客户端的 `claude_desktop_config.json`

> 📚 **延伸阅读**：
> - [MCP 协议详解](../01-fundamentals/mcp-model-context-protocol.md)
> - [90个AI工具大全](./90-ai-tools-list.md)
> - [AI Agent 可观测性](./ai-agent-observability.md)
