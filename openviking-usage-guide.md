# OpenViking 使用指南（2026-03-21）

## 📚 项目信息

- **GitHub**: https://github.com/volcengine/OpenViking
- **Fork**: https://github.com/srxly888-creator/OpenViking
- **Stars**: 17,338
- **开发**: 字节跳动火山引擎
- **本地路径**: ~/.openclaw/workspace/OpenViking

---

## 💥 核心价值

> **OpenViking is an open-source Context Database designed specifically for AI Agents**

---

## ✨ 核心特性

### **1. 文件系统范式**
- ✅ 统一管理记忆、资源、技能
- ✅ 像管理本地文件一样管理 Agent 上下文
- ✅ 解决碎片化问题

### **2. 三层结构（L0/L1/L2）**
- ✅ **L0**：核心记忆（始终加载）
- ✅ **L1**：工作记忆（按需加载）
- ✅ **L2**：长期记忆（归档）
- ✅ 大幅降低 token 消耗

### **3. 目录递归检索**
- ✅ 原生文件系统检索
- ✅ 目录定位 + 语义搜索
- ✅ 递归精准获取上下文

### **4. 可视化检索轨迹**
- ✅ 可视化检索路径
- ✅ 清晰观察问题根源
- ✅ 引导检索优化

### **5. 自动会话管理**
- ✅ 自动压缩对话内容
- ✅ 提取长期记忆
- ✅ Agent 越用越聪明

---

## 🚀 快速开始

### **1. 安装**

```bash
# Python 包
pip install openviking --upgrade --force-reinstall

# Rust CLI（可选）
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash
```

### **2. 配置模型**

#### **支持的三种提供商**

| 提供商 | 说明 | 获取 API Key |
|--------|------|-------------|
| `volcengine` | 火山引擎豆包模型 | [控制台](https://console.volcengine.com/ark) |
| `openai` | OpenAI 官方 API | [OpenAI Platform](https://platform.openai.com) |
| `litellm` | 统一接入第三方模型 | [LiteLLM 文档](https://docs.litellm.ai/docs/providers) |

#### **配置示例**

**OpenAI:**
```json
{
  "vlm": {
    "provider": "openai",
    "model": "gpt-4o",
    "api_key": "your-api-key",
    "api_base": "https://api.openai.com/v1"
  }
}
```

**Claude (via LiteLLM):**
```json
{
  "vlm": {
    "provider": "litellm",
    "model": "claude-3-5-sonnet-20240620",
    "api_key": "your-anthropic-api-key"
  }
}
```

**智谱 GLM (via LiteLLM):**
```json
{
  "vlm": {
    "provider": "litellm",
    "model": "zhipu/glm-4",
    "api_key": "your-zhipu-api-key"
  }
}
```

---

## 💡 与 MSA 的对比

| 特性 | MSA | OpenViking |
|------|-----|------------|
| **可用性** | ❌ 未开源 | ✅ 已开源 |
| **Stars** | - | 17,338 |
| **记忆方式** | 原生稀疏注意力 | 文件系统范式 |
| **层级结构** | - | L0/L1/L2 |
| **门槛** | 高（需重新训练） | 低（即装即用） |
| **性能** | 4B 干翻 235B RAG | token 砍半，完成率+40% |

---

## 🎯 使用场景

### **1. 长期记忆管理**
- Agent 会话历史
- 用户偏好
- 任务记忆

### **2. 资源管理**
- 文档库
- 知识库
- 工具集

### **3. 技能管理**
- Agent Skills
- 工作流
- 任务模板

---

## 📊 性能数据

- ✅ **Token 消耗**: 砍半
- ✅ **任务完成率**: +40%
- ✅ **检索效率**: 大幅提升
- ✅ **可观测性**: 完整可视化

---

## 🔧 与 OpenClaw 集成

### **官方集成**
- ✅ OpenClaw 官方支持
- ✅ 专门的 Skill: `openclaw_openviking_skill`
- ✅ GitHub: https://github.com/swizardlv/openclaw_openviking_skill

### **集成步骤**
1. 安装 OpenViking
2. 配置模型
3. 安装 OpenClaw Skill
4. 配置 OpenClaw 使用 OpenViking

---

## 🎯 行动计划

### **今天**
- [x] Fork OpenViking
- [ ] 阅读完整文档
- [ ] 理解 L0/L1/L2 结构

### **本周**
- [ ] 安装并配置
- [ ] 测试基本功能
- [ ] 评估性能提升

### **两周内**
- [ ] 集成到 OpenClaw
- [ ] 实战测试
- [ ] 分享使用经验

---

## 🔗 相关链接

- **官网**: https://openviking.ai
- **GitHub**: https://github.com/volcengine/OpenViking
- **Fork**: https://github.com/srxly888-creator/OpenViking
- **文档**: https://www.openviking.ai/docs
- **Discord**: https://discord.com/invite/eHvx8E9XF3
- **X**: https://x.com/openvikingai

---

## 💬 金句

> **像管理本地文件一样管理 Agent 的上下文**

> **L0/L1/L2 三层结构，加载按需，显著节省成本**

---

## 📈 市场影响

### **对开发者**
- 简化 Agent 开发
- 降低上下文管理成本
- 提升 Agent 性能

### **对 OpenClaw 用户**
- 原生支持
- 完整集成
- 性能提升 40%

### **对行业**
- 新的上下文管理范式
- 文件系统思路
- 可观测性提升

---

## ⚠️ 注意事项

### **前置要求**
- Python 3.10+
- Go 1.22+（构建 AGFS）
- C++ 编译器（GCC 9+ / Clang 11+）
- 网络连接（下载依赖）

### **模型要求**
- VLM 模型（图像理解）
- Embedding 模型（向量化）

---

**最后更新**: 2026-03-21 23:45
**来源**: 字节火山引擎
**Stars**: 17,338
**状态**: ✅ 已 Fork，可用
