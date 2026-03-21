# MAS Factory 学习仓库

MAS Factory 多智能体编排框架的学习资料和实战代码。

## 📚 文档索引

1. **快速入门** - [MASFACTORY_QUICKSTART.md](./MASFACTORY_QUICKSTART.md)
   - 安装配置
   - API Key 设置
   - 测试运行
   - 使用方式

2. **深度研究** - [MASFACTORY_DEEP_DIVE.md](./MASFACTORY_DEEP_DIVE.md)
   - Vibe Graphing 工作原理
   - 双模型策略详解
   - ChatDev 实战案例
   - 工具系统说明
   - 快速开始示例

3. **学习路线图** - [learning-roadmap.md](./learning-roadmap.md)
   - 立即可用项目
   - 本周学习计划
   - 难度评估
   - 学习资源

## 🚀 快速开始

### 1. 配置 API Key

```bash
export ZHIPU_API_KEY="your-zhipu-api-key"
```

### 2. 运行测试

```bash
python test_masfactory.py
```

### 3. 使用示例

```python
from masfactory import RootGraph, Agent, NodeTemplate
from masfactory_config import invoke_model

BaseAgent = NodeTemplate(Agent, model=invoke_model)

g = RootGraph(
    name="two_stage_qa",
    nodes=[
        ("analyze", BaseAgent(instructions="分析问题")),
        ("answer", BaseAgent(instructions="给出答案")),
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

## 📖 核心概念

- **Vibe Graphing** - 自然语言 → 图结构
- **双模型策略** - GLM-5 规划 + GLM-4-Air 执行
- **成本优化** - $6.08 → $0.26（暴砍 95%）

## 🔗 相关链接

- **官方文档**: https://bupt-gamma.github.io/MASFactory/
- **论文**: http://arxiv.org/abs/2603.06007
- **GitHub**: https://github.com/BUPT-GAMMA/MASFactory
- **Fork**: https://github.com/srxly888-creator/MASFactory

## 📂 仓库结构

```
masfactory-learning/
├── README.md                    # 本文件
├── MASFACTORY_QUICKSTART.md     # 快速入门
├── MASFACTORY_DEEP_DIVE.md      # 深度研究
├── learning-roadmap.md          # 学习路线图
├── masfactory_config.py         # 配置文件
└── test_masfactory.py           # 测试脚本
```

## 🎯 学习进度

- [x] Fork MAS Factory 项目
- [x] 配置双模型策略
- [x] 创建学习文档
- [ ] 设置 API Key
- [ ] 运行测试脚本
- [ ] 学习基础示例
- [ ] 设计自己的工作流

## 📊 成本对比

| 方案 | 规划模型 | 执行模型 | 成本 |
|------|----------|----------|------|
| 传统 | GPT-4 | GPT-4 | $6.08 |
| 双模型 | GLM-5 | GLM-4-Air | $0.26 |
| **节省** | - | - | **95%** |

## 💬 社区

- **Discord**: https://discord.gg/SSxm8yrDGt
- **QQ群**: 2157069383

---

**最后更新**: 2026-03-21
**维护者**: srxly888-creator
