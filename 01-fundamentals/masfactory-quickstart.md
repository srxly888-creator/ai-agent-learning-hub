# MAS Factory 快速开始指南（修复版）

> **修复时间**: 2026-03-22 12:11
> **问题**: 原链接 `/01-fundamentals/masfactory-quickstart.md` 不存在
> **解决方案**: 创建此文件

---

## 🚀 MAS Factory 是什么？

MAS Factory 是一个多智能体编排框架，可以帮助你：
- 🤖 **快速构建 AI Agent 工作流**
- 🔄 **自动编排多个 AI 智能体**
- 🎯 **用自然语言描述任务，让 AI 执行**

**GitHub**: https://github.com/nopinduoduo/MASFactory  
**Stars**: 125+**开发**: 北邮 GAMMA 实验室

---

## 📋 10 分钟快速开始

### **前置要求**
- Python 3.8+
- pip

### **步骤 1: 安装**

```bash
pip install masfactory
```

### **步骤 2: 创建第一个 Agent**

```python
from masfactory import Agent

# 创建一个简单的 Agent
agent = Agent(
    name="我的第一个 Agent",
    description="这是一个示例 Agent"
)

# 运行 Agent
result = agent.run("帮我写一个 Python 脚本")
print(result)
```

### **步骤 3: 多智能体编排**

```python
from masfactory import Workflow

# 创建工作流
workflow = Workflow()

# 添加多个 Agent
workflow.add_agent(agent1)
workflow.add_agent(agent2)

# 运行工作流
workflow.run("分析这个数据集并生成报告")
```

### **步骤 4: VS Code 插件（推荐）**

1. 打开 VS Code
2. 搜索 "MAS Factory Visualizer"
3. 安装插件
4. 可视化你的 Agent 工作流

---

## 🎯 核心功能

### **1. Vibe Graphing**
- 用自然语言描述任务
- AI 自动生成工作流图

### **2. 双模型策略**
- **规划模型**: 理解任务，- **执行模型**: 执行具体操作
- 成本优化

### **3. 开源**
- 完全开源
- MIT 协议
- 活跃社区

---

## 📚 学习资源

- **官方文档**: https://github.com/nopinduoduo/MASFactory
- **VS Code 插件**: 搜索 "MAS Factory Visualizer"
- **社区**: GitHub Issues

---

## 💡 与其他工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| **MAS Factory** | Vibe Graphing | 自然语言描述工作流 |
| **LangGraph** | 图结构编排 | 复杂工作流 |
| **AutoGen** | 对话式编排 | 多轮对话 |
| **CrewAI** | 角色扮演 | 团队协作 |

---

## ⚠️ 常见问题

### **Q: 支持哪些 LLM？**
A: 支持 OpenAI、Claude、Gemini、GLM 等

### **Q: 是否需要 GPU？**
A: 不需要，MAS Factory 只负责编排
不负责模型推理

### **Q: 如何调试？**
A: 使用 VS Code 插件可视化工作流

---

## 🔗 相关链接

- **GitHub**: https://github.com/nopinduoduo/MASFactory
- **VS Code 插件**: 搜索 "MAS Factory Visualizer"
- **学习仓库**: https://github.com/srxly888-creator/ai-agent-learning-hub

---

**修复完成！链接已更新为**
