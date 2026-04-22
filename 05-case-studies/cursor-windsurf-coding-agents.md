# 💻 Cursor / Windsurf 编程 Agent 实战 — AI 编码助手的架构分析与最佳实践

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI 编程 Agent（Cursor / Windsurf）深度解析 |
| **适用** | 开发者、AI 工具爱好者、技术管理者 |
| **前置知识** | [Vibe Coding 入门](../01-fundamentals/vibe-coding-intro.md)、[Agent 架构](../01-fundamentals/ai-agent-architecture.md) |

---

## 🎯 一句话理解

> **Cursor 和 Windsurf 不是"会写代码的聊天机器人"——它们是能读你的项目、理解你的代码库、自动编辑文件的"AI 程序员"。关键区别在于：它们能在你的代码库上下文中思考和行动。**

---

## ❓ 什么是 AI 编程 Agent？

先理清概念：

```
AI 编码工具的进化：

第一代：代码补全（Copilot）
├─ 你写一行，它补一行
├─ 没有全局理解
└─ 像一个打字速度很快的实习生

第二代：代码生成（ChatGPT + 代码）
├─ 你描述需求，它生成代码
├─ 不了解你的项目
└─ 像一个远程程序员（看不到你的屏幕）

第三代：编程 Agent（Cursor / Windsurf）
├─ 读取整个代码库
├─ 理解项目结构
├─ 自动编辑多个文件
├─ 运行命令、调试错误
└─ 像一个坐在你旁边的结对编程伙伴
```

---

## 🔷 Cursor 深度解析

### 核心架构

```
Cursor 架构图：

┌──────────────────────────────────────────┐
│                Cursor IDE                │
│                                           │
│  ┌─────────────┐  ┌────────────────────┐ │
│  │   编辑器层    │  │    Agent 层         │ │
│  │  (VS Code)   │  │                    │ │
│  │              │  │  ┌──────────────┐  │ │
│  │  - 文件编辑  │  │  │  上下文管理   │  │ │
│  │  - 终端      │←→│  │  - 代码库索引 │  │ │
│  │  - Git       │  │  │  - 当前文件   │  │ │
│  │  - Diff查看  │  │  │  - 对话历史   │  │ │
│  │              │  │  └──────┬───────┘  │ │
│  └─────────────┘  │         ↓           │ │
│                    │  ┌──────────────┐  │ │
│                    │  │  规划引擎     │  │ │
│                    │  │  - 任务分解   │  │ │
│                    │  │  - 文件依赖   │  │ │
│                    │  │  - 执行计划   │  │ │
│                    │  └──────┬───────┘  │ │
│                    │         ↓           │ │
│                    │  ┌──────────────┐  │ │
│                    │  │  工具层       │  │ │
│                    │  │  - 读文件     │  │ │
│                    │  │  - 写文件     │  │ │
│                    │  │  - 运行命令   │  │ │
│                    │  │  - 搜索代码   │  │ │
│                    │  │  - Git 操作   │  │ │
│                    │  └──────┬───────┘  │ │
│                    └─────────┼──────────┘ │
│                              ↓            │
│                    ┌──────────────────┐   │
│                    │   LLM 后端       │   │
│                    │  Claude / GPT-4o │   │
│                    └──────────────────┘   │
└──────────────────────────────────────────┘
```

### 核心功能详解

#### 1. 代码库索引（Codebase Indexing）

这是 Cursor 最核心的能力——**理解你整个项目**。

```
Cursor 如何理解你的代码库？

1. 首次打开项目时，自动扫描所有文件
2. 构建代码索引（基于 Embedding）
3. 当你提问时，自动检索相关代码片段
4. 把相关代码作为上下文发送给 LLM

你不需要手动告诉它代码在哪里——它自己知道。
```

```
你的项目：
├── src/
│   ├── api/
│   │   ├── users.py      # 用户API
│   │   └── auth.py       # 认证API
│   ├── models/
│   │   └── user.py       # 用户模型
│   └── utils/
│       └── helpers.py     # 工具函数

当你在 Cursor 中问：
"帮我给用户API添加一个删除接口"

Cursor 会自动：
1. 检索到 src/api/users.py（最相关）
2. 检索到 src/models/user.py（用户模型）
3. 检索到 src/api/auth.py（可能有权限相关逻辑）
4. 理解你的代码风格和模式
5. 生成符合项目风格的代码
```

#### 2. Composer（多文件编辑）

Composer 是 Cursor 的"大杀器"——**同时编辑多个文件**。

```
普通 Copilot：
你说："添加一个用户删除功能"
它：给你一段代码片段
你：手动找到文件、复制粘贴、修改

Cursor Composer：
你说："添加一个用户删除功能"
它：
1. 读取相关文件
2. 修改 api/users.py（添加删除接口）
3. 修改 models/user.py（添加删除方法）
4. 修改 tests/test_users.py（添加测试）
5. 生成 Diff，你一键接受或拒绝
```

#### 3. .cursorrules 文件

这是 Cursor 的"项目级配置"——告诉 Agent 你的项目规范。

```markdown
# .cursorrules 示例

## 技术栈
- 后端：Python + FastAPI
- 前端：React + TypeScript
- 数据库：PostgreSQL
- ORM：SQLAlchemy

## 代码规范
- 使用 Python 3.11+ 特性
- 函数必须有类型注解
- 使用 async/await
- 错误处理用自定义异常类
- 测试用 pytest

## 项目结构
- API 路由在 src/api/
- 数据模型在 src/models/
- 工具函数在 src/utils/
- 测试在 tests/

## 注意事项
- 不要使用 deprecated 的 API
- 所有用户输入需要验证
- 数据库操作需要事务管理
```

#### 4. Agent 模式

Cursor 有两种主要模式：

```
Chat 模式（Ctrl+L）：
- 对话式交互
- 适合提问、解释代码
- 不会自动修改文件

Agent 模式（Ctrl+I / Composer）：
- 自主行动模式
- 自动读取文件、编辑代码、运行命令
- 适合复杂的多步任务
```

---

## 🔶 Windsurf 深度解析

### Windsurf vs Cursor

```
Windsurf（由 Codeium 开发）是 Cursor 的主要竞争对手：

相同点：
- 都基于 VS Code
- 都有代码库索引
- 都支持多文件编辑
- 都有 Agent 模式

不同点：
┌──────────────┬──────────────┬──────────────┐
│    特性       │   Cursor     │   Windsurf   │
├──────────────┼──────────────┼──────────────┤
│ LLM 后端     │ Claude/GPT   │ 自有模型+第三方│
│ 上下文管理   │ 手动+自动    │ Cascade 自动  │
│ 流式编辑     │ ✅           │ ✅            │
│ 终端集成     │ ✅           │ ✅            │
│ 定价         │ $20/月       │ 免费层更大    │
│ 社区         │ 更大         │ 增长中        │
└──────────────┴──────────────┴──────────────┘
```

### Windsurf 的特色：Cascade

**Cascade** 是 Windsurf 的核心 Agent 系统，特点是**更流畅的上下文管理**：

```
Cascade 的工作方式：

1. 自动感知上下文
   - 你在编辑文件时，Cascade 自动读取相关文件
   - 不需要手动 @ 引用文件

2. 实时流式编辑
   - 修改代码时实时显示变更
   - 可以随时中断和修正

3. 智能工具调用
   - 自动判断需要运行什么命令
   - 自动查看错误日志并修复
```

---

## 🛠️ 实战：用 Cursor 开发一个完整功能

### 场景：给一个 FastAPI 项目添加用户认证

```bash
# 1. 用 Cursor 打开项目
cursor ./my-api-project

# 2. 打开 Agent 模式（Ctrl+I）
# 3. 输入需求
```

**在 Cursor 中输入**：

```
帮我给这个 FastAPI 项目添加 JWT 用户认证功能，包括：
1. 用户注册接口 POST /auth/register
2. 用户登录接口 POST /auth/login
3. JWT Token 验证中间件
4. 密码用 bcrypt 加密
5. 对应的单元测试

请遵循项目现有的代码风格和结构。
```

**Cursor 的工作流程**：

```
Step 1: 理解项目
├─ 读取现有文件结构
├─ 理解数据库模型
├─ 理解 API 路由风格
└─ 识别已有的依赖

Step 2: 规划实现
├─ 安装依赖：python-jose[cryptography], passlib[bcrypt]
├─ 创建 src/api/auth.py（认证路由）
├─ 修改 src/models/user.py（添加密码字段）
├─ 创建 src/utils/auth.py（JWT 工具）
├─ 创建 src/middleware/auth.py（验证中间件）
└─ 创建 tests/test_auth.py（测试）

Step 3: 逐个文件实现
├─ 编辑 requirements.txt
├─ 创建新文件
├─ 修改现有文件
└─ 生成每个变更的 Diff

Step 4: 验证
├─ 运行测试
├─ 检查是否有语法错误
└─ 如果有错误，自动修复
```

### 实际操作技巧

#### 技巧1：善用 @ 引用

```
在 Cursor Chat 中：
@src/models/user.py 请解释这个用户模型

@src/api/ @src/models/ 这两个目录的关系是什么？

@terminal 请查看刚才运行的错误日志
```

#### 技巧2：用 Composer 处理复杂任务

```
Ctrl+I → 打开 Composer

适合用 Composer 的场景：
- 涉及多个文件的修改
- 需要添加新功能
- 重构代码
- 修复跨文件的 Bug

不适合用 Composer 的场景：
- 简单的代码补全
- 快速问答
- 解释一小段代码
```

#### 技巧3：学会审阅 Diff

```
Cursor 的 Diff 视图：

+ 新增的行（绿色）
- 删除的行（红色）
~ 修改的行（黄色）

操作：
- Accept All：接受所有更改
- Accept File：接受单个文件的更改
- Reject：拒绝更改
- 手动编辑：在 Diff 中直接修改
```

#### 技巧4：让 Agent 自动修错

```
当 Cursor 的代码有错误时：

1. 运行代码/测试
2. 看到错误信息
3. 在 Cursor 中说："刚才的代码有错误，请修复：[粘贴错误信息]"
4. Agent 会读取错误信息，定位问题，生成修复

或者更简单：
- 有些情况下 Cursor 会自动检测到错误
- 直接在终端中显示错误
- Agent 会自动尝试修复
```

---

## 📊 最佳实践

### 1. 项目配置

```markdown
# .cursorrules — 必须配置！

## 基础信息
- 这是一个 [你的项目类型] 项目
- 使用 [技术栈]
- 代码风格：[PEP8 / ESLint 配置等]

## 关键文件说明
- src/api/ — API 路由
- src/models/ — 数据模型
- src/utils/ — 工具函数
- tests/ — 测试文件
- migrations/ — 数据库迁移

## 编码规范
- [你的具体规范]
- [错误处理方式]
- [命名规范]

## 禁止事项
- 不要修改 [某些文件]
- 不要使用 [某些库]
- 不要删除 [某些代码]
```

### 2. Prompt 编写技巧

```
❌ 不好的 Prompt：
"帮我改一下代码"

✅ 好的 Prompt：
"在 src/api/users.py 中添加一个 PUT /users/{id} 接口，
 用于更新用户信息。只允许更新 email 和 username 字段，
 需要验证 email 格式，返回更新后的用户信息。
 遵循现有的路由风格（参考 GET /users/{id}）。"

关键要素：
1. 明确的位置（哪个文件）
2. 具体的需求（什么功能）
3. 约束条件（什么限制）
4. 参考对象（参考什么风格）
```

### 3. 分步处理复杂任务

```
❌ 一次性给太多任务：
"帮我重构整个后端，添加认证、缓存、日志、监控"

✅ 分步处理：
Step 1: "先帮我添加 JWT 认证"
Step 2: "现在添加 Redis 缓存层"
Step 3: "添加请求日志中间件"
Step 4: "添加 Prometheus 监控指标"

每一步都确认无误后再进行下一步。
```

### 4. 善用"学习"能力

```
Cursor 会记住：
- 你之前问过的问题
- 你接受的代码修改
- 你的代码风格偏好

利用这个特性：
- 保持一致的交互方式
- 及时纠正不满意的输出
- 使用 .cursorrules 固化规范
```

---

## ⚠️ 常见陷阱

### 1. 盲目信任

```
❌ 危险行为：
- 不看 Diff 直接 Accept All
- 不运行测试就提交
- 不理解代码就合并

✅ 安全行为：
- 逐个文件审阅 Diff
- 运行测试验证
- 理解每处修改的含义
- 特别注意数据库操作和权限相关代码
```

### 2. 上下文不足

```
❌ 问题：
- 项目太大，Agent 抓不住重点
- 相关文件没被索引到
- 输出不符合项目规范

✅ 解决：
- 用 @ 引用关键文件
- 配置 .cursorrules
- 把大任务拆成小任务
- 先解释项目结构给 Agent 听
```

### 3. 过度依赖

```
⚠️ 注意：
- AI 编程 Agent 是工具，不是替代品
- 你需要理解它写的每一行代码
- 架构决策需要自己做
- 安全和性能需要自己把关

好的关系：
- 你做架构和决策
- Agent 做实现和细节
- 你做审查和验证
```

---

## 🔄 Cursor + Claude Code 协作

很多高级开发者会组合使用多种 AI 编码工具：

```
Cursor → 日常编码、快速迭代
Claude Code → 复杂重构、深度分析
GitHub Copilot → 基础代码补全

工作流示例：
1. 用 Cursor 快速实现功能
2. 遇到复杂问题切换到 Claude Code
3. 用 Cursor 做日常修改
4. 用 Claude Code 做大规模重构
```

> 📖 更多 Claude Code 的用法请看 [Claude Code 技能指南](../06-agent-tools/claude-code-skills-cn.md)

---

## 🔮 未来趋势

### 1. 更强的自主性
```
当前：你说一步，它做一步
未来：你说目标，它自主完成整个项目
```

### 2. 多 Agent 协作
```
当前：一个 Agent 做所有事
未来：多个 Agent 各司其职
- 架构师 Agent：设计系统
- 开发者 Agent：写代码
- 测试 Agent：写测试
- 审查 Agent：Code Review
```

### 3. 全栈 Agent
```
当前：主要写后端/逻辑代码
未来：前后端、数据库、部署一条龙
```

### 4. 学习你的风格
```
当前：通过 .cursorrules 配置
未来：自动学习你的编码习惯和偏好
```

---

## 📚 总结

```
AI 编程 Agent 核心能力：
1. 代码库理解（索引 + 检索）
2. 多文件编辑（Composer）
3. 自动运行和调试（终端集成）
4. 项目规范遵循（.cursorrules）

Cursor vs Windsurf：
- Cursor：生态更大，功能更成熟
- Windsurf：免费层更大，上下文管理更智能

最佳实践：
1. 配置 .cursorrules
2. 学会写好 Prompt
3. 分步处理复杂任务
4. 始终审阅 Diff
5. 运行测试验证
6. 不要盲目信任

核心心态：
AI 编程 Agent = 增强你的能力，不是替代你。
你是架构师和决策者，Agent 是你的超级助手。
```

> 💡 **核心要点**：AI 编程 Agent 已经从"噱头"变成了"生产力工具"。掌握 Cursor/Windsurf 的使用方法，就像学会了用 IDE 代替记事本——不是可选的升级，而是必备的技能。

---

## 🔗 相关链接

- [Vibe Coding 入门](../01-fundamentals/vibe-coding-intro.md)
- [Code as Prompt 实战](./code-as-prompt.md)
- [Claude Code 技能指南](../06-agent-tools/claude-code-skills-cn.md)
- [Claude Code 子 Agent](../06-agent-tools/claude-code-subagents-cn.md)
- [Cursor 官网](https://cursor.sh)
- [Windsurf 官网](https://codeium.com/windsurf)
