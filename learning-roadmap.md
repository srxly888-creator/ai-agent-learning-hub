# 学习路线图（2026-03-21）

## 🚀 立即可用（零门槛）

### 1. Codex CLI ✅ 已安装
- **状态**: 已配置 gpt-4o-mini
- **用途**: 代码生成、重构、调试
- **上手难度**: ⭐
- **立即可用**: 是

### 2. Whisper ✅ 已安装
- **状态**: 已配置 ffmpeg + medium 模型
- **用途**: 语音转文字
- **上手难度**: ⭐
- **立即可用**: 是

### 3. PUA Skill
- **GitHub**: https://github.com/tanweai/pua
- **Fork**: srxly888-creator/pua (待重试)
- **用途**: PUA 话术鞭策 AI，强制验证
- **上手难度**: ⭐⭐
- **安装**: 复制 skill 到 ~/.openclaw/skills/
- **预计时间**: 10分钟

### 4. Chrome DevTools MCP
- **用途**: AI 接管浏览器，复用登录状态
- **安装**: `claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect`
- **设置**: chrome://inspect/#remote-debugging
- **上手难度**: ⭐⭐
- **预计时间**: 15分钟

---

## 📚 本周学习（中等难度）

### 5. MAS Factory ✅ 已 fork + 已配置
- **GitHub**: https://github.com/BUPT-GAMMA/MASFactory
- **Fork**: srxly888-creator/MASFactory
- **核心**: Vibe Graphing（自然语言 → 多智能体工作流）
- **上手难度**: ⭐⭐⭐
- **配置状态**: ✅ 双模型策略已配置（GLM-5 + GLM-4-Flash）
- **集成状态**: ✅ OpenClaw skill 已创建
- **学习步骤**:
  1. ⚠️ 设置 API Key: `export ZHIPU_API_KEY="your-key"`
  2. ✅ 运行测试: `python ~/.openclaw/workspace/test_masfactory.py`
  3. ✅ 阅读快速入门: `MASFACTORY_QUICKSTART.md`
  4. ✅ 运行示例: `python -m applications.vibegraph_demo.main`
  5. ✅ 学习核心概念（Node/Edge/Loop/Switch）
  6. ✅ 设计自己的工作流
- **预计时间**: 1-2小时（配置10分钟 + 学习1小时 + 实战30分钟）

### 6. PageAgent（阿里）
- **GitHub**: https://github.com/alibaba/page-agent
- **Fork**: srxly888-creator/page-agent
- **核心**: 一行代码让网页变 AI 可控
- **上手难度**: ⭐⭐⭐
- **学习步骤**:
  1. 阅读文档
  2. 测试示例网页
  3. 集成到自己的项目
- **预计时间**: 2小时

### 7. Skillgrade（单元测试）
- **GitHub**: https://github.com/mgechev/skillgrade
- **Fork**: srxly888-creator/skillgrade
- **核心**: Agent Skills 单元测试
- **上手难度**: ⭐⭐⭐
- **学习步骤**:
  1. `skillgrade init`
  2. `skillgrade --smoke`
  3. 编写测试用例
- **预计时间**: 1-2小时

---

## 🔬 深度研究（高难度）

### 8. MSA（记忆稀疏注意力）
- **论文**: 17岁高中生，Kimi 团队采用
- **难度**: ⭐⭐⭐⭐⭐
- **需要**: 深度学习基础、Transformer 知识
- **预计时间**: 1-2天

### 9. OpenViking（字节）
- **核心**: L0/L1/L2 三层记忆，token 砍半
- **难度**: ⭐⭐⭐⭐
- **需要**: 理解向量检索、记忆管理
- **预计时间**: 半天

### 10. Tmux Agent 团队
- **核心**: Claude 当大脑 + 3个 Codex 并行
- **难度**: ⭐⭐⭐⭐
- **需要**: tmux、git worktree、多 Agent 协作
- **预计时间**: 3-4小时

---

## 🎯 推荐学习顺序

### 今天（1小时）
1. ✅ 重试 fork PUA 项目
2. ✅ 安装 PUA Skill
3. ✅ 配置 Chrome DevTools MCP
4. ✅ 测试 Whisper 语音转文字

### 本周（每天2-3小时）
- **周一**: MAS Factory 基础（安装 + 运行示例）
- **周二**: MAS Factory 进阶（Vibe Graphing 实战）
- **周三**: PageAgent（网页 AI 化）
- **周四**: Skillgrade（Skills 单元测试）
- **周五**: OpenViking（记忆管理）
- **周末**: MSA 论文深度研究

### 两周内
- Tmux Agent 团队实战
- bb-browser（50+网站 CLI 化）
- ossless-claw（OpenClaw 持久化）

---

## 📊 难度评估

| 项目 | 难度 | 实用性 | 优先级 |
|------|------|--------|--------|
| Codex CLI | ⭐ | ⭐⭐⭐⭐⭐ | 已完成 |
| Whisper | ⭐ | ⭐⭐⭐⭐ | 已完成 |
| PUA Skill | ⭐⭐ | ⭐⭐⭐⭐ | 高 |
| Chrome DevTools MCP | ⭐⭐ | ⭐⭐⭐⭐⭐ | 高 |
| MAS Factory | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 最高 |
| PageAgent | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |
| Skillgrade | ⭐⭐⭐ | ⭐⭐⭐ | 中 |
| MSA | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 低 |
| OpenViking | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |
| Tmux Agent | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |

---

## 🎓 学习资源

### MAS Factory
- 文档: https://bupt-gamma.github.io/MASFactory/
- 视频: https://www.youtube.com/watch?v=ANynzVfY32k
- 论文: http://arxiv.org/abs/2603.06007

### PageAgent
- GitHub: https://github.com/alibaba/page-agent
- Star: 9.6k+

### 其他
- Claude Code Skills 手册: https://x.com/berryxia/status/2034039046692093977
- OpenClaw 843页指南: https://x.com/indiehackercase/status/2033507786286682593

---

## 💡 快速上手建议

**最推荐先学**: MAS Factory
- 理由: Vibe Graphing 能让自然语言直接变成多智能体工作流
- 成果: 代码量暴砍 90%，成本从 $6 降到 $0.26
- 门槛: 中等，但有完整文档和示例

**其次推荐**: Chrome DevTools MCP
- 理由: 让 AI 接管浏览器，日常操作自动化
- 成果: 复用登录状态，无需重复认证
- 门槛: 低，15分钟配置完成
