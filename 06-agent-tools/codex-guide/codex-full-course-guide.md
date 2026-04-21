# OpenAI Codex 完整指南 - Part 1：基础入门 笔记

> 📝 来源：[ai-knowledge-graph](https://github.com/nxs9bg24js-tech/ai-knowledge-graph) — YouTube 字幕整理笔记

> **视频标题**：OpenAI Codex Complete Guide
> **作者**：Riley Brown
> **时长**：1:43:15
> **链接**：https://www.youtube.com/watch?v=KXIdYEdOPys
> **笔记范围**：Part 1 — 基础入门（00:00 ~ 45:00）

---

## 1. 下载安装 Codex 桌面应用 `[00:00 - 03:20]`

- 浏览器搜索 `codex app download`，进入 **chatgpt.com/codex desktop app** 页面
- 支持 **macOS** 下载安装
- 首次打开界面：
  - **左侧面板**：5 个主要选项（Projects / Chats / Plugins / Automations / Search）
  - **右侧聊天区**：类似 ChatGPT 界面
- 核心区别：Codex 不仅能对话，还能**控制你的电脑**（创建、编辑、删除文件，甚至操控鼠标和键盘）

---

## 2. 项目(Projects)与文件夹结构 `[03:20 - 06:00]`

- 创建项目的本质是**选择本地文件夹**作为工作目录
- 建议创建一个总文件夹（如 `Riley's Codex Projects`），在下面再建子项目文件夹
- 操作流程：
  1. 点击 **New Folder** → 命名（如 `Codex Desktop Research`）→ **Create**
  2. 选中文件夹 → **Open** → 项目创建完成
- 项目出现在左侧面板，所有在该项目下创建的**文件**都会保存到对应文件夹中
- 通过项目旁的 **三个点(···)** → **Open in Finder** 可随时查看文件

---

## 3. Chats 聊天功能与命名 `[06:00 - 10:40]`

- 每个项目下可以创建**多个 Chat**，点击 `+` 新建
- Chat 会**自动命名**（AI 根据内容生成，如 `Find New Codex App Features`）
- 多个 Chat 可以**同时运行**，运行中显示旋转图标，完成后显示**蓝色圆点**通知
- **@引用文件**：在同一个项目文件夹内，可以用 `@文件名` 引用已创建的文件，方便跨 Chat 协作
- 示例：`@codex-desktop-features do research let me know if I miss anything`

---

## 4. 权限设置（Full Access 推荐）`[10:40 - 11:30]`

- 权限设置位于聊天输入框上方
- 控制 Agent 能做什么、是否需要用户审批
- **推荐使用 Full Access**：让 Agent 自由操作（"let it cook"），无需逐一审批
- 其他选项包括需要逐步确认的模式（适合不熟悉场景）

---

## 5. 模型选择与 Effort 级别 `[11:30 - 11:50]`

- **模型**：默认 **GPT 5.4**
- **Effort 级别**：默认 **Extra High**（推荐）
- 这两个设置位于聊天输入框上方的控制栏

---

## 6. 预览功能(Preview)与全屏模式 `[08:30 - 09:30]`

- Agent 创建的文件（如 `.xlsx`）可以点击 **Open** 在侧边预览
- **全屏模式**：点击预览窗口顶部的全屏按钮，隐藏侧边面板，专注查看文件
- **切换视图**：可以在全屏预览和分屏聊天视图之间自由切换
- 可同时打开**多个文件**预览（标签页形式）
- 可以直接在全屏预览中**继续对话**，让 AI 编辑当前文件

---

## 7. 创建与编辑文档、Excel 表格 `[07:30 - 10:40]`

- 在 Chat 中直接要求创建文件：`Please create a spreadsheet of...`
- Agent 自动创建 `.xlsx` 文件，保存在项目的 `outputs` 文件夹中
- 创建后可在侧栏预览，也可用 AI 继续编辑：
  - 示例：`Please remove the source page column`
- 所有文件存储在**本地项目文件夹**中，可随时通过 Finder 访问
- 内置 **Word 文档 Skill**（`/docs`）可生成 `.docx` 报告

---

## 8. 文件夹组织（outputs 目录）`[08:20 - 12:15]`

- Agent 创建的文件自动归入项目文件夹下的 **`outputs/`** 目录
- Chat 记录不会保存在文件夹中，只有**实际文件**会保存
- 组织结构示例：
  ```
  Riley's Codex Projects/
  ├── Codex Desktop Research/
  │   └── outputs/
  │       ├── codex-desktop-features.xlsx
  │       └── ...
  ├── General Agent Tasks/
  │   └── outputs/
  │       └── ...
  └── My New Business/
      └── outputs/
          └── ...
  ```

---

## 9. 搜索功能 `Cmd+G` `[12:46 - 14:30]`

- 快捷键：**`Cmd + G`**（Mac）/ **`Ctrl + G`**（推测 Windows）
- 搜索所有历史 Chat，按关键词查找
- 即使项目已从侧边面板移除，Chat 内容仍可通过搜索找到
- 搜索结果可直接点击打开，也可将对应项目**拖回**侧边面板
- 项目从侧边面板移除 ≠ 删除，只是隐藏（文件夹仍在本地）

---

## 10. Plugins vs Skills 区别 `[14:30 - 16:00]`

| 概念 | 定义 | 类比 |
|------|------|------|
| **Skill（技能）** | 可复用的工作流包，针对特定任务类型 | 可复用的**配方/食谱** |
| **Plugin（插件）** | 可安装的扩展单元，为 Codex 增加新能力 | **安装包/连接器** |

- 两者的界限**有些模糊**，不同工具有不同叫法：
  - Claude Code：Customize Tab → Skills + Connectors
  - OpenAI Codex：**Plugins + Skills**
- 本质上都是**扩展模型能力**的方式
- 让 Codex 能做的事（如查邮件、操作日历）默认没有，需要通过 Skill/Plugin 赋予

---

## 11. Google Calendar 插件演示 `[15:55 - 17:30]`

- 操作步骤：
  1. 进入 **Plugins** 页面
  2. 找到 **Google Calendar** 插件 → **Install Google Calendar**
  3. 自动跳转浏览器 → 登录 Google 账号 → **Select All** → **Continue**
  4. 验证完成后提示 `Google Calendar is now connected`
- 使用方式：在 Chat 中直接提问，如 `Please list out the events for this week for me`
- 也可用 `/` 斜杠触发相关技能

---

## 12. Gmail 插件演示 `[16:40 - 18:00]`

- 类似 Calendar，在 Plugins 中安装 **Gmail** 插件
- 连接后可让 Agent 查看邮件：
  - 示例：`Check my email and tell me all of the urgent messages sent today`
- 可配合创建自动化任务（如每周日历回顾 + 邮件摘要）

---

## 13. 自定义 Skill 创建流程 `[28:10 - 32:00]`

**完整流程（以 YouTube Researcher Skill 为例）**：

1. **发现需求**：反复做某件事（如手动提取 YouTube 字幕）
2. **找 API**：让 AI 推荐方案 → 获得 API（如 **Super Data** API，每月 100 次免费）
3. **获取 API Key**：注册 Super Data → 复制 API Key
4. **在 Codex 中创建 Skill**：
   - 新建 Chat → 输入 `skill creator`（触发技能创建器）
   - 描述需求 + 提供 API Key
   - AI 自动研究 API 用法并生成 Skill
5. **使用 Skill**：
   - 创建**新 Chat**（必须在新建会话中才能使用新 Skill）
   - 使用 `/YouTube-researcher` 触发
   - 示例：`/YouTube-researcher look at Riley Brown's latest 10 videos, pull transcripts and summarize them`

**自定义 Skill 的其他方式**：
- 从其他工具迁移：如将 Claude Design Tool 的工作方式复制给 Codex
- 使用 MCP（Model Context Protocol）：很多工具提供官方 MCP（如 Paper MCP、Figma MCP），可让 AI 创建包装 Skill
- 管理 Skill：**Plugins** → **Skills** → **Manage** → 可查看所有已安装的 MCP 和 Skill

---

## 14. Automations 自动化创建 `[33:20 - 35:30]`

- 在 Chat 中直接要求创建自动化：
  - 示例：`On the last day of every month, create a YouTube report using /YouTube-researcher and /docs`
- Agent 会将 Skill 组合起来，设定**定时执行**
- 查看已创建的自动化：**Automations 标签页**
- 已创建示例：
  - **Monthly YouTube Report**（每月 YouTube 分析报告）
  - **Weekly Calendar Recap**（每周日历回顾）
- 自动化可以引用 Skills（`/YouTube-researcher`、`/docs` 等）

---

## 15. Computer Use 电脑控制 `[04:30 - 05:00, 20:20 - 22:50]`

- Codex 最强大的功能之一：Agent 可以**完全控制你的鼠标和键盘**
- 应用场景：
  - **Figma 集成**：直接在 Figma 画布上操作（切换工具、放置文字、生成设计）
  - **Paper 集成**：通过 Paper MCP 在设计画板上创建 Landing Page
- 操作方式：直接在 Chat 中描述你想让 Agent 在电脑上做什么
- 示例：`Go to Figma and create a mockup design for my new shoe company`
- Agent 会自动切换应用、操作界面、使用内置图片生成等工具

---

## 16. Steering（转向/实时干预）`[25:25 - 26:30]`

- **Message Queuing**：在 Agent 工作时输入新指令，默认排队等待
- **Steering**：点击 **Steer** 按钮，指令会**立即插入**当前工作流，无需等待
- 应用场景：Agent 生成设计时发现按钮重叠，直接发截图 + `fix this`，Agent 会在当前任务中间处理

---

## 17. Mini Window（迷你窗口）`[24:20 - 25:00]`

- 右键点击 Chat → **Open in Mini Window**
- 在独立小窗口中运行 Chat，同时可以使用其他应用
- 适合：让 Agent 在后台工作的同时，在前台查看结果（如 Paper 设计画板）

---

## 18. 语音输入（Whisper Flow）`[21:00 - 21:15]`

- 工具：**Whisper Flow**（第三方工具）
- 使用方式：按住 **Fn 键** → 说话 → 自动转文字输入
- 有免费计划，适合不想打字的用户

---

## 19. Figma 与 Paper 集成对比 `[20:20 - 27:30]`

| 工具 | 特点 | 评价 |
|------|------|------|
| **Figma MCP** | 直接操作 Figma 画布 | 集成体验一般，更适合从 Figma 转 Code |
| **Paper** | 专为 AI Agent 设计的画板工具 | 体验更好，支持实时动画、多版本并行 |

- **Paper** 工作流：
  1. 创建新文件 → 输入 `/paper` 或描述需求
  2. Agent 在 Paper 画板上实时生成设计
  3. 可要求生成多个变体（`Create four more variations`）
  4. 支持 Steering 实时修正

---

## 关键工具与快捷键汇总

| 工具/功能 | 说明 |
|-----------|------|
| `Cmd + G` | 全局搜索所有 Chat |
| `Fn`（Whisper Flow） | 按住语音输入 |
| `/skill-name` | 斜杠触发特定 Skill |
| `@filename` | 引用项目中的文件 |
| `Open in Finder` | 通过 Finder 查看项目文件 |
| `Open in Mini Window` | 在独立窗口中运行 Chat |
| `Steer` 按钮 | 实时干预 Agent 工作流 |
| Full Access | 权限模式（推荐） |
| GPT 5.4 | 默认模型 |
| Extra High | 默认 Effort 级别 |
| Skill Creator | 内置技能创建器 |

---

## Part 1 小结 `[35:25 - 36:50]`

Part 1 涵盖了 Codex 的核心基础：
1. ✅ 应用下载安装与界面概览
2. ✅ 项目管理与文件组织
3. ✅ Chat 功能、权限、模型设置
4. ✅ 预览与全屏模式
5. ✅ 文档/表格创建与编辑
6. ✅ 搜索功能
7. ✅ Plugins 与 Skills 区别及使用
8. ✅ Google Calendar / Gmail 插件
9. ✅ 自定义 Skill 创建（YouTube Researcher）
10. ✅ Automations 自动化
11. ✅ Computer Use 电脑控制
12. ✅ Steering 实时干预、Mini Window

> **Part 2** 将进入多任务实战：同时创建 6 个项目（iOS App、Web App、Investor Deck、Launch Video、Landing Page、Expo 自动化），学习高效 AI 多任务协作。
# Codex 完整指南 — Part 2: 多任务实战笔记

> 来源视频时长 1:43:15，以下内容从 **45:00** 开始，涵盖多任务并行构建完整产品的方法论与实操。

---

## 多任务并行(Multitasking)方法论

**时间戳：45:00 – 58:00 | 1:08:10 – 1:08:18 | 1:41:45 – 1:42:40**

### 核心理念

- **同时开多个 Chat**：Codex 支持在同一个项目文件夹下开多个对话，各自独立运行
- **任务间切换**：当一个 Agent 在处理需要 5-6 分钟的任务时，立即切换到另一个对话发起新任务
- **进度管理**：使用 Excalidraw 创建 Project Plan，实时标记每个任务的进度（Done / In Progress）
- **对话命名与固定**：右键重命名对话（如 `plan`、`mobile app`、`web app`、`screen design`），并将 Plan 固定到顶部
- **Fork 对话**：当一个任务完成后，可以右键 → Fork into local，创建新对话继续衍生工作（如从 mobile app fork 出 investor deck）

### 多任务流程示例

1. **对话1**：iOS App 开发（Swift + Xcode）
2. **对话2**：Landing Page（React + Tally）
3. **对话3**：Launch Video（Remotion）
4. **对话4**：Investor Deck（PowerPoint）
5. **对话5**：Typefully 自动化（API Skill）
6. **Plan 对话**：Excalidraw 看板，追踪所有任务状态

> **关键工具**：Excalidraw（看板/设计）、Codex Chat（多对话并行）

---

## iOS App 设计流程（Excalidraw Skill）

**时间戳：45:00 – 46:10**

- 在 Codex 中使用 **Excalidraw** 插件绘制 App 界面原型
- 设计了 Chorus App 的多个屏幕：Learn、Platforms、Build、Saved
- 将设计稿保存在项目的 `my new business` 文件夹中
- 通过 Codex 将 Excalidraw 设计直接转化为 Swift 代码：*"Please integrate the screens in the my new business folder in the mobile app"*

> **工具**：Excalidraw（Codex 内置插件）

---

## iOS App 开发（Swift + Xcode）

**时间戳：48:45 – 52:00 | 49:00 – 51:55**

### 技术栈
- **语言**：Swift
- **IDE**：Xcode
- **运行方式**：Xcode Simulator 或真机
- **框架**：SwiftUI

### 开发要点
- Codex 直接生成完整的 Swift 项目代码
- 每次修改后需要在 Xcode 中 **点击 Play 重新构建** 才能在设备上看到变化
- 设计风格：白色极简、黑色文字、底部 Tab Bar、顶部固定导航栏
- UI 细节优化：滚动时顶部/底部模糊效果（blur）、列表项渐隐效果
- Codex 会将设计稿中的多页面（Learn / Platforms / Build / Saved）全部实现为可导航的 Tab

### App 图标生成
- Codex 内置 **图片生成能力**，可生成 10 个无背景的 iOS App 图标候选
- 上传选中的图标到 Xcode 项目

> **工具**：Xcode、SwiftUI、Codex Image Generation

---

## 真机调试和部署

**时间戳：1:22:20 – 1:23:55**

### 步骤
1. 用 USB 连接 iPhone 到 Mac
2. 在 Xcode 顶部设备选择器中，从 iOS Simulator 切换到真实设备（如 "Riley's iPhone"）
3. 点击 Play，Xcode 会将 App 安装到真机上运行
4. 真机上确认功能：页面导航、数据展示、触觉反馈（haptics）

> **工具**：Xcode、iPhone 真机

---

## Supabase 后端集成

**时间戳：52:00 – 53:20 | 55:20 – 59:30 | 1:02:10 – 1:04:15**

### 选型决策
- 向 Codex 提问最佳数据库方案 → 推荐使用 **Supabase + PostgreSQL**
- Supabase 是 AI 应用最常用的数据库平台（估值 $100 亿），Lovable 等平台也使用它

### 设置流程
1. 在 [supabase.com](https://supabase.com) 创建新项目
2. 设置项目名称和密码，启用 Data API
3. 获取 URL 和 Region 信息
4. 通过 **MCP（Model Context Protocol）** 连接 Codex 与 Supabase
   - 在 Supabase 控制台 → Connect → 选择 Codex → 复制 MCP 配置
   - ⚠️ 添加 MCP 后需要 **重启 Codex** 才能在当前会话中使用
5. 重启后，让 Codex 创建完整数据库 Schema

### 数据库表结构
- `skill_categories`：技能分类（Research、GTM、Build、Ops）
- `platforms`：平台列表（Claude Code、Codex、Cursor、OpenClaw、Hermes、Manis、Perplexity Computer）
- `skills`：具体技能（Competitor Scan、Landing Critic、YouTube Researcher 等）
- `saved_items`：用户收藏

### 数据验证
- 在 Supabase Table Editor 中可查看所有数据表
- App 中添加的数据实时同步到 Supabase

> **工具**：Supabase、PostgreSQL、MCP（Model Context Protocol）

---

## 邮箱/密码认证

**时间戳：1:23:55 – 1:31:30**

### 实现方式
- 最初考虑 Google OAuth 和 Clerk，最终选择最简单的 **邮箱 + 密码认证**
- 通过 Supabase Auth 实现，无需额外服务

### 关键步骤
1. 让 Codex 添加认证功能
2. 在 Supabase Dashboard 中 **关闭 Email Confirmation**（开发阶段方便测试）
3. 用户可创建账户、登录、查看个人资料
4. 登录后数据（收藏的平台、技能）与用户账户绑定

### 功能确认
- 创建账户 ✓
- 登录 ✓
- 数据持久化到 Supabase ✓
- 个人资料显示收藏数量 ✓

> **工具**：Supabase Auth

---

## TestFlight 发布

**时间戳：1:31:30 – 1:34:10 | 1:37:45 – 1:38:30**

### 流程
1. 在 Codex 中让 Agent 执行 TestFlight 准备工作：*"Please do everything to prep for TestFlight"*
2. Xcode 创建 Build 并上传到 **App Store Connect**
3. 在 App Store Connect 中启用 TestFlight
4. 获取 TestFlight 链接，分发给测试用户
5. 用户通过链接安装 App、登录账户、使用全部功能

### 关键信息
- App 名称：Chorus（"A trusted curator for the AI agent era"）
- 账号：Not a Number（演示用开发者账号）
- 状态：已成功生成 TestFlight 构建版本

> **工具**：Xcode、App Store Connect、TestFlight

---

## 网页应用 Landing Page 开发

**时间戳：46:10 – 48:40 | 1:07:17 – 1:13:30**

### 技术栈
- **框架**：React
- **表单**：Tally.so（嵌入式）
- **设计优化**：Claude Code（终端调用）

### 开发流程
1. 在 Codex 中创建 React 应用：*"Create a basic web app landing page that can collect data from interested users"*
2. 在 **Tally.so** 创建注册表单（模板：姓名、邮箱）
3. 复制 Tally 嵌入代码，让 Codex 集成到 Landing Page
4. 设计风格与 iOS App 保持一致（白色、简洁字体、极简风格）

### Claude Code 设计优化
- Codex 的 Web 设计能力有限，转而使用 **Claude Code** 优化
- 在 Codex 终端中运行：`claude --dangerously-skip-permissions`
- 给 Claude 上下文：查看 Chorus App 代码、匹配风格、保留 Tally 嵌入
- Claude Code 输出的设计明显优于 Codex
- 添加平台 Logo（Codex、Claude Code、OpenClaw、Hermes、Gemini）

> **工具**：React、Tally.so、Claude Code（`claude --dangerously-skip-permissions`）

---

## Vercel 部署

**时间戳：1:33:06 – 1:35:20 | 1:37:00 – 1:37:50**

### 部署流程
1. 在 Codex 中请求部署：*"Deploy this to Vercel and give me the public link"*
2. Codex 自动完成 Vercel 部署
3. 获取公开链接：`chorus-ba-2.vercel.app`
4. 在浏览器（Arc）中打开验证功能
5. 测试 Tally 表单提交 → 确认数据回传到 Tally 后台

### 验证结果
- 网站可公开访问 ✓
- Tally 表单正常工作 ✓
- 提交数据在 Tally 后台可见 ✓
- 可后续绑定自定义域名

> **工具**：Vercel、Arc Browser

---

## Tally 表单集成

**时间戳：46:40 – 48:10 | 1:37:00 – 1:37:30**

- **Tally.so**：在线表单工具，用于收集用户邮箱注册信息
- 使用预设模板（Waitlist 模板）：First Name、Last Name、Email Address
- 表单标题：*"Sign up for Chorus"*
- 提交成功提示：*"Done. Your registration is complete. We will reach out in a few days."*
- 通过 **标准嵌入（Standard Embed）** 方式集成到 React 应用
- 复制嵌入代码 → 粘贴给 Codex → 自动集成

> **工具**：Tally.so

---

## Investor Deck (PPT) 创建

**时间戳：1:17:00 – 1:20:00 | 1:27:10 – 1:32:55**

### 创建流程
1. **Fork** mobile app 对话 → 创建新对话命名为 `investor deck`
2. 让 Codex 分析 App 功能和资源：*"Analyze the features and assets from this application and create an investor slide deck"*
3. 使用 Codex 内置的 **PowerPoint Skill**
4. 搜索 2026 年 4 月投资者关注趋势，参考在线模板风格
5. Codex 生成 PPT 后，再用 **Claude Code** 优化设计
   - 减少文字、增加图表和视觉元素
   - 调整叙事重点：更多讲故事和市场机会，少讲技术细节
   - 关键文案：*"Curate, Test, Monetize"* / *"Curation is the wedge. Agents are the business."*
   - *"Most startups pray for distribution. We start with it."*
   - *"Every consumer is about to decide which agents to trust. Nobody is guiding them."*

> **工具**：Codex PowerPoint Skill、Claude Code、CleanShot Pro（截图标注工具）

---

## 导出 Canva 编辑

**时间戳：1:20:20 – 1:20:45 | 1:31:55 – 1:32:50**

- Codex 生成的 PPT 可以 **一键导出到 Canva** 进行手动编辑
- 在 Codex 中点击文件 → 选择 "Open in Canva"
- Canva 中可进行最后 5-10% 的精细调整：
  - 修改颜色、调整布局
  - 添加背景、图标
  - 删除不需要的元素（如顶部导航栏）
  - 优化动画效果
- Canva 中预览效果明显更好

> **工具**：Canva

---

## Claude Code + Codex 协作（用 Claude 做设计优化）

**时间戳：1:09:42 – 1:12:05 | 1:25:50 – 1:27:20 | 1:41:00 – 1:41:15**

### 协作模式
- **Codex**：更好的界面、项目管理、多任务并行
- **Claude Code（Opus）**：更好的设计能力、更精致的 UI 输出
- 在 Codex 的 **终端（Terminal）** 中直接运行 Claude Code

### 使用方法
```bash
# 在 Codex 终端中启动 Claude Code（跳过权限确认）
claude --dangerously-skip-permissions
```

### 协作场景
1. **Landing Page 设计**：Codex 生成基础版 → Claude Code 优化为精致版
2. **Investor Deck 优化**：Codex 生成 PPT → Claude Code 减少文字、增加视觉
3. **Launch Video**：Remotion Skill 在 Codex 中创建 → Claude Code 优化动画细节

### 注意事项
- Claude Code 在终端中运行时，没有 Codex 对话的上下文，需要手动提供文件路径和上下文
- 可以最小化终端窗口，Claude Code 会在后台继续工作
- Claude Code 执行时间通常较长（7-10 分钟），但输出质量更高

> **工具**：Claude Code（Claude Opus 模型）、Codex Terminal

---

## Launch Video（Remotion 动态视频）

**时间戳：54:06 – 59:55 | 1:05:06 – 1:08:30 | 1:15:00 – 1:25:10 | 1:38:45 – 1:41:10**

### 工具
- **Remotion**：Codex 插件，通过代码生成动态视频（Motion Graphics）
- 在 Plugins 中搜索 "Remotion" → Add to Codex
- 使用方式：输入 `@remotion` 调用技能

### 制作流程
1. **规划**：让 Remotion Skill 先思考视频框架和注意事项
2. **测试**：创建简单测试视频验证 Skill 是否正常工作
3. **构建场景**：
   - 场景1：黑屏文字 *"Agents are taking over the world"* + Toggle 开关动画
   - 场景2：iPhone Mockup 出现，展示 App 界面（Learn 页面）
   - 场景3：放大 "Learning about Skills" → 转场到技能展示（彩色卡片轮播）
   - 场景4：复制 Skill → 粘贴到 Codex App
   - 场景5：复制 Skill → 粘贴到 Claude Code → 生成 App 设计稿
4. **精确控制**：
   - 视频以 30fps 运行，可通过帧数精确指定修改位置
   - 开启标尺（View → Show Rulers）获取精确坐标
   - 使用 **Steer** 功能在 Agent 加载时提前输入修改指令

### 优化迭代
- 调整鼠标点击位置（坐标精确到像素）
- 修改转场效果（从渐隐改为硬切）
- 添加背景音乐（拖入音频文件，设置 50% 音量）
- 使用 **Claude Code** 优化动画设计（字体、转场、布局）

### 输出
- 通过 localhost 链接在浏览器中预览视频
- 带有时间轴编辑器，可实时调整

> **工具**：Remotion（Codex Plugin）、Claude Code

---

## Typefully API Skill 创建（自动发推）

**时间戳：1:35:30 – 1:39:20**

### 背景
- **Typefully**：Twitter/X 多账号管理工具
- 演示者管理 6 个 Twitter 账号，合计 275,000+ 粉丝
- 支持用 AI 起草推文

### Skill 创建流程
1. 在 Typefully 设置中获取 **API Key**（Settings → API → Create New API Key）
2. 在 Codex 中请求创建 Skill：*"Search Typefully and create a skill for full control with their API V3"*
3. 粘贴 API Key（注意保密，视频外操作）
4. Codex 自动搜索 API 文档、创建 Skill、测试功能
5. 测试方式：用水果 emoji 🍎 标记 AI 发送的测试推文

### 测试结果
- Skill 创建成功（实际使用的是 V2 API，但仍可创建草稿）
- 成功在 Riley Brown 账号创建草稿推文
- 可在 Typefully 后台查看和编辑草稿

> **工具**：Typefully、Typefully API（V2/V3）

---

## Automations 定时任务（每日推文草稿、周报）

**时间戳：1:39:20 – 1:41:35**

### 创建流程
1. Typefully Skill 创建后，让 Codex 设置自动化：*"Create an automation that researches and drafts 3 tweets every morning"*
2. 使用 `/typefully` 调用刚创建的 Skill
3. Codex 自动创建定时自动化任务

### 自动化内容
- **每日推文草稿**：每天早上自动研究并生成 3 条推文草稿
- 可指定发布账号（如 Riley Brown / Vibe Coding Explain）
- 草稿保存在 Typefully 中，人工审核后发布

### 最终状态
- 自动化任务数：3 个
- 状态：全部激活
- 包含每日推文草稿自动化

> **工具**：Typefully、Codex Automations

---

## 精华要点总结（10 条最值得记住的 Tips）

1. **多任务并行是 Codex 的杀手锏** — 同时开多个对话，利用等待时间处理其他任务，效率倍增

2. **不确定怎么做？直接问 Agent** — 如果不知道用什么数据库、怎么部署，直接让 Agent 给出方案和推荐，它会告诉你选项并帮你执行

3. **Codex + Claude Code 是最佳拍档** — Codex 擅长项目管理和多任务，Claude Code（Opus）擅长设计，在 Codex 终端中调用 `claude --dangerously-skip-permissions` 即可协作

4. **Supabase 是 AI 应用首选数据库** — 免费起步、PostgreSQL 底层、内置 Auth、通过 MCP 直连 Codex，估值 $100 亿不是没有原因

5. **对话命名和 Fork 提升组织力** — 给每个对话起名（plan/mobile app/web app），固定 Plan 到顶部；任务完成后 Fork 对话衍生新任务

6. **Remotion 用代码做动态视频** — 通过 `@remotion` 调用，30fps 精确帧控制，开启标尺获取坐标，用 Steer 提前输入修改指令

7. **PPT 一键导出 Canva** — Codex 生成的 Investor Deck 可以直接在 Canva 中打开编辑，做最后 5-10% 的精细调整

8. **Tally.so 是最快的表单方案** — 无需后端，嵌入代码一行搞定，与 React 应用完美集成，数据实时回传

9. **添加 MCP 后必须重启 Codex** — 新增的 MCP Server（如 Supabase）需要重启应用才能在当前会话中生效

10. **每个 Skill 都可以自动创建** — 不管是 Typefully、YouTube Researcher 还是其他工具，只需提供 API Key，让 Agent 搜索文档并创建 Skill，就能实现自动化工作流

---

## 工具/平台/API 速查表

| 类别 | 名称 | 用途 |
|------|------|------|
| **AI Agent** | OpenAI Codex | 主力开发工具、多任务并行 |
| **AI Agent** | Claude Code (Opus) | 设计优化、精细 UI 调整 |
| **设计** | Excalidraw | App 原型设计、项目看板 |
| **设计** | Canva | PPT 最终编辑 |
| **移动开发** | Swift / SwiftUI | iOS App 开发语言 |
| **移动开发** | Xcode | iOS IDE |
| **移动开发** | TestFlight | iOS App 测试分发 |
| **后端** | Supabase | PostgreSQL 数据库 + Auth |
| **后端** | MCP | Model Context Protocol（Agent 连接外部工具） |
| **前端** | React | Landing Page 框架 |
| **部署** | Vercel | 网站托管部署 |
| **表单** | Tally.so | 用户注册表单 |
| **视频** | Remotion | 代码驱动动态视频生成 |
| **社媒** | Typefully | Twitter 多账号管理 + API |
| **浏览器** | Arc | 日常浏览器 |
| **截图** | CleanShot Pro | 截图标注工具 |
| **App Store** | App Store Connect | iOS 应用发布管理 |
