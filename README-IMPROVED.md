# AI Agent Learning Hub

> **从零到精通：系统学习 AI Agent 开发的完整路径**

[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

---

## 🎯 这个仓库是给谁的？

- ✅ **AI Agent 开发者** - 想要构建智能 Agent 系统
- ✅ **Vibe Coding 爱好者** - 对自然语言编程感兴趣
- ✅ **多智能体系统研究者** - 研究群体智能和协作
- ✅ **AI 工具使用者** - 想要提升工作效率

**学完你将能够**：
- 独立开发 AI Agent 系统
- 配置多智能体协作
- 使用最新的 Agent 框架和工具
- 理解前沿研究（ICML 2026 论文）

---

## 🚀 5分钟快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/srxly888-creator/ai-agent-learning-hub.git
cd ai-agent-learning-hub

# 2. 查看学习路径
cat ROADMAP.md

# 3. 开始第一个教程
cd 01-fundamentals
cat what-is-agent.md
```

---

## 📚 学习路径

### **Level 1: 入门（1周）**
- [ ] 理解什么是 AI Agent
- [ ] 了解 Agent 架构
- [ ] 安装 MAS Factory
- [ ] 运行第一个 Agent
- [ ] 理解 Vibe Coding

### **Level 2: 进阶（2周）**
- [ ] 学习多智能体协作
- [ ] 配置记忆系统（OpenViking）
- [ ] 研究 Skill 基础设施
- [ ] 复现实战案例
- [ ] 开发第一个 Skill

### **Level 3: 高级（1月）**
- [ ] 研究 OpenSage 论文（ICML 2026）
- [ ] 理解 MSA 记忆机制
- [ ] 探索自编程 Agent
- [ ] 贡献开源社区
- [ ] 发布自己的项目

---

## 🔥 Top 10 必读（按优先级）

### **1. 基础概念（必读）**
1. **[什么是 AI Agent](./01-fundamentals/what-is-agent.md)** - 5分钟理解核心概念
2. **[MAS Factory 快速开始](./01-fundamentals/masfactory-quickstart.md)** - 10分钟运行第一个 Agent
3. **[Vibe Coding 方法论](./01-fundamentals/vibe-coding-intro.md)** - 理解自然语言编程

### **2. 核心框架（进阶）**
4. **[OpenSage 论文解读](./04-advanced/opensage-icml2026.md)** - ICML 2026，自编程 ADK
5. **[OpenViking 记忆系统](./02-frameworks/openviking.md)** - Token 砍半，分层记忆
6. **[MiroFish 预测引擎](./05-case-studies/mirofish-prediction.md)** - 37k Stars, 10天完成

### **3. 实战案例（应用）**
7. **[Polymarket 套利案例](./05-case-studies/polymarket-arbitrage.md)** - 16岁高中生赚钱实战
8. **Karpathy 多 Agent 协作** - 10+ Agent 并行
9. **[代码即 Prompt](./05-case-studies/code-as-prompt.md)** - 响马的编程哲学

### **4. 工具生态（扩展）**
10. **[90个 AI 工具清单](./03-tools/90-ai-tools-list.md)** - 完整工具生态

---

## 📂 仓库结构

```
ai-agent-learning-hub/
├── README.md（你在这里）
├── ROADMAP.md（学习路径）
├── CONTRIBUTING.md（贡献指南）
│
├── 01-fundamentals/（基础概念）
│   ├── what-is-agent.md
│   ├── agent-architecture.md
│   ├── vibe-coding.md
│   └── masfactory-quickstart.md
│
├── 02-frameworks/（框架与工具）
│   ├── masfactory-framework.md
│   ├── openviking-memory.md
│   ├── magicskills-infrastructure.md
│   └── skills-manager.md
│
├── 03-tools/（工具生态）
│   ├── 90-ai-tools-list.md
│   ├── polymarket-tools.md
│   └── development-tools.md
│
├── 04-advanced/（高级主题）
│   ├── opensage-icml2026.md
│   ├── msa-memory.md
│   ├── mirofish-prediction.md
│   └── self-programming-agents.md
│
├── 05-case-studies/（实战案例）
│   ├── polymarket-arbitrage.md
│   ├── karpathy-multi-agent.md
│   └── code-as-prompt.md
│
└── 06-resources/（资源链接）
    ├── papers.md
    ├── github-repos.md
    └── official-docs.md
```

---

## 🌟 重磅推荐

### **中国开源力量（60%+）**

| 项目 | Stars | 团队 | 特点 | 学习价值 |
|------|-------|------|------|----------|
| **MiroFish** | 37,844 | 北邮学生 | 10天完成，已在赚钱 | ⭐⭐⭐⭐⭐ |
| **OpenViking** | 17,338 | 字节 | Token 砍半，完成率+40% | ⭐⭐⭐⭐⭐ |
| **OpenSage** | - | 中国团队 | ICML 2026，自编程 ADK | ⭐⭐⭐⭐⭐ |
| **MAS Factory** | 125 | 北邮 | 多智能体编排 | ⭐⭐⭐⭐ |
| **TradingAgents** | 30,000+ | 中国团队 | 30.5% 年化收益 | ⭐⭐⭐⭐ |

---

## 💡 核心洞察

### **范式转变**
```
传统：Human-centered（以人为中心）
    ↓
未来：AI-centered（以 AI 为中心）
```

### **自动化演进**
```
Level 0: 人工设计所有组件
Level 1: 人工定义拓扑，AI 选择工具
Level 2: AI 定义拓扑，AI 选择工具
Level 3: AI 自动创建 Agent + 拓扑 + 工具（OpenSage）
```

### **效率提升**
- Token 消耗: ↓60%
- 检索速度: ↑3x
- 开发效率: ↑10x

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### **如何贡献**
1. Fork 本仓库
2. 创建你的 Feature Branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到 Branch (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### **贡献内容**
- ✅ 新工具发现
- ✅ 实战案例
- ✅ 学习心得
- ✅ 代码示例
- ✅ 翻译（英文/中文）

---

## 📈 更新日志

### **2026-03-22 - v2.0**
- ✅ 重组仓库结构（知识层次）
- ✅ 创建清晰的学习路径（ROADMAP.md）
- ✅ 精选 Top 10 必读内容
- ✅ 优化 README（社区友好）
- ✅ 添加贡献指南

### **2026-03-21 - v1.0**
- ✅ 初始版本
- ✅ 收集 38 篇学习笔记
- ✅ Fork 12 个重要项目
- ✅ 整理 90+ AI 工具

---

## 🔗 重要链接

### **Fork 项目**
- [MiroFish](https://github.com/srxly888-creator/MiroFish) - 群体智能预测引擎
- [MAS Factory](https://github.com/srxly888-creator/MASFactory) - 多智能体编排框架
- [OpenViking](https://github.com/srxly888-creator/OpenViking) - 上下文数据库
- [MagicSkills](https://github.com/srxly888-creator/MagicSkills) - Skill 基础设施

### **论文**
- [OpenSage](https://arxiv.org/abs/2602.16891) - ICML 2026

### **社区**
- GitHub Issues: 提问和讨论
- Pull Requests: 贡献内容

---

## 📜 许可证

MIT License

---

## 🙏 致谢

感谢所有开源项目和社区贡献者！

特别感谢：
- **MiroFish 团队** - 10天完成震撼项目
- **OpenSage 团队** - ICML 2026 论文
- **字节跳动** - OpenViking 开源
- **北邮 GAMMA 实验室** - MAS Factory
- **北大 Narwhal-Lab** - MagicSkills

---

**最后更新**: 2026-03-22 00:30
**维护者**: @srxly888-creator
**Stars**: ⭐ 欢迎支持！

---

> **"从 Human-centered 到 AI-centered，从手动设计到自动生成"**
