# MAS Factory 深度研究笔记

## 📖 核心概念详解

### 1. **Vibe Graphing 工作原理**

**输入**: 自然语言描述的需求（如"设计一个软件开发流程"）

**处理**: 
1. **Build Model**（GLM-5）解析自然语言，生成图结构设计
2. **生成 JSON Blueprint**（graph_design.json）
3. **Compile** 成可执行的工作流

**输出**: 可运行的多智能体协作工作流

---

### 2. **双模型策略详解**

| 模型 | 用途 | 特点 | 成本 |
|------|------|------|------|
| **GLM-5** | 规划（build_model） | 高阶推理，生成图结构 | 高 |
| **GLM-4-Air** | 执行（invoke_model） | 轻量级执行，完成任务 | 低 |

**成本优化**: $6.08 → $0.26（暴砍 95%）

---

### 3. **核心组件**

| 组件 | 用途 | 示例 |
|------|------|------|
| **Agent** | 执行单元 | CEO, CTO, 程序员 |
| **Graph** | 子图 | 需求分析阶段 |
| **Loop** | 循环执行 | 测试循环（最多3次）|
| **Switch** | 分支判断 | 根据条件选择路径 |
| **Human** | 人工介入 | 代码审查确认 |

---

## 🏗️ 实战案例：ChatDev 软件开发流程

### **工作流结构**

```
START 
  ↓
demand_analysis_phase（需求分析）
  ↓
language_choose_phase（语言选择）
  ↓
coding_phase（编码）
  ↓
test_loop（测试循环）
  ↓
END
```

### **每个 Phase 的结构**

```python
# 每个 Phase 包含两个 Agent
InstructorAgent → AssistantAgent
AssistantAgent → InstructorAgent
InstructorAgent → CONTROLLER
```

### **6 个 Phase 详解**

#### 1. **demand_analysis_phase**
- **目标**: 分析用户需求
- **Agent**: CEO（指导） + CPO（执行）
- **输入**: task（任务描述）
- **输出**: modality（产品形态）

#### 2. **language_choose_phase**
- **目标**: 选择编程语言
- **Agent**: CEO（指导） + CTO（执行）
- **输入**: task, modality
- **输出**: language（编程语言）

#### 3. **coding_phase**
- **目标**: 编写代码
- **Agent**: CTO（指导） + 程序员（执行）
- **输入**: task, modality, language
- **输出**: codes（代码文件列表）
- **工具**: codes_check_and_processing_tool, check_code_completeness_tool

#### 4. **test_loop**
- **目标**: 测试和修复循环
- **最大迭代**: 3次
- **终止条件**: 
  - error_summary 包含 "No errors found"
  - exist_bugs_flag 为 False
  - modification_conclusion 等于 "Finished!"

#### 5. **test_error_summary_phase**
- **目标**: 总结测试错误
- **Agent**: 测试工程师（指导） + 程序员（执行）
- **工具**: run_tests_tool

#### 6. **test_modification_phase**
- **目标**: 修复代码
- **Agent**: 测试工程师（指导） + 程序员（执行）
- **工具**: codes_check_and_processing_tool

---

## 🔧 工具系统

### 1. **codes_check_and_processing_tool**
- **用途**: 检查并处理代码文件
- **参数**: codes（代码列表）
- **功能**: 
  - 验证代码格式
  - 更新代码管理器
  - 写入磁盘

### 2. **check_code_completeness_tool**
- **用途**: 检查未实现的代码
- **返回**: {"has_unimplemented": bool, "filename": str}

### 3. **run_tests_tool**
- **用途**: 运行测试并收集错误
- **返回**: test_reports, error_summary, exist_bugs_flag

---

## 💡 学习要点

### 1. **Vibe Graphing 的优势**
- ✅ 自然语言描述需求
- ✅ AI 自动生成工作流
- ✅ 人工迭代修正
- ✅ 编译成可执行代码

### 2. **双模型策略的优势**
- ✅ 贵模型做规划（用量少）
- ✅ 便宜模型做执行（用量大）
- ✅ 成本暴砍 95%

### 3. **图结构编程的优势**
- ✅ 可视化工作流
- ✅ 易于调试
- ✅ 可复用组件
- ✅ 支持循环和分支

---

## 🚀 快速开始示例

### 示例 1：简单两阶段问答

```python
from masfactory import RootGraph, Agent, OpenAIModel, NodeTemplate
from masfactory_config import invoke_model

BaseAgent = NodeTemplate(Agent, model=invoke_model)

g = RootGraph(
    name="two_stage_qa",
    nodes=[
        ("analyze", BaseAgent(
            instructions="分析问题",
            prompt_template="用户问题：{query}"
        )),
        ("answer", BaseAgent(
            instructions="给出答案",
            prompt_template="问题：{query}\n分析：{analysis}"
        )),
    ],
    edges=[
        ("entry", "analyze", {"query": "用户问题"}),
        ("analyze", "answer", {"query": "原始问题", "analysis": "分析结果"}),
        ("answer", "exit", {"answer": "最终回答"}),
    ],
)

g.build()
out, _ = g.invoke({"query": "什么是 AI Agent？"})
print(out["answer"])
```

### 示例 2：Vibe Graphing（自然语言生成工作流）

```python
from masfactory import RootGraph, VibeGraph
from masfactory_config import build_model, invoke_model

g = RootGraph(name="vibe_demo")

vibe = g.create_node(
    VibeGraph,
    name="vibe_graph",
    invoke_model=invoke_model,  # 执行
    build_model=build_model,    # 规划
    build_instructions="设计一个代码审查工作流：编写→审查→修复",
)

g.edge_from_entry(receiver=vibe, keys={})
g.edge_to_exit(sender=vibe, keys={})

g.build()
g.invoke(input={}, attributes={})
```

---

## 📚 学习资源

### 官方文档
- **在线文档**: https://bupt-gamma.github.io/MASFactory/
- **论文**: http://arxiv.org/abs/2603.06007
- **视频**: 
  - https://www.youtube.com/watch?v=QFlQuX_cddk（Vibe Graphing）
  - https://www.youtube.com/watch?v=ANynzVfY32k（Demo）

### 本地资源
- **仓库**: ~/.openclaw/workspace/MASFactory
- **配置**: ~/.openclaw/workspace/masfactory_config.py
- **测试**: ~/.openclaw/workspace/test_masfactory.py
- **快速入门**: ~/.openclaw/workspace/MASFACTORY_QUICKSTART.md

### 示例代码
- **VibeGraph Demo**: applications/vibegraph_demo/
- **ChatDev Lite**: applications/chatdev_lite/
- **CAMEL**: applications/camel/

---

## 🎯 下一步学习计划

### 今天（1小时）
1. ✅ 设置 API Key
2. ✅ 运行测试脚本
3. ✅ 学习基础示例（两阶段问答）
4. ✅ 理解核心概念

### 本周（每天2-3小时）
- **周一**: 学习 Agent 和 Graph 组件
- **周二**: 学习 Loop 和 Switch 组件
- **周三**: Vibe Graphing 基础
- **周四**: Vibe Graphing 进阶
- **周五**: ChatDev Lite 实战
- **周末**: 设计自己的工作流

### 两周内
- 集成到 OpenClaw
- 开发实用工作流
- 优化成本和性能

---

## 💬 社区资源

- **Discord**: https://discord.gg/SSxm8yrDGt
- **QQ群**: 2157069383
- **GitHub Issues**: https://github.com/BUPT-GAMMA/MASFactory/issues

---

**最后更新**: 2026-03-21 20:55
**作者**: OpenClaw Agent
