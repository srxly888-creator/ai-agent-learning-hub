# OpenViking + OpenClaw 集成最佳实践（2026-03-21）

## 🎯 目标

> **让 OpenClaw 用上 OpenViking 的上下文管理能力**

---

## 📊 现状分析

### **OpenClaw 当前记忆系统**
```
当前结构：
├── MEMORY.md (长期记忆)
├── memory/YYYY-MM-DD.md (短期记忆)
├── AGENTS.md (工作规则)
├── SOUL.md (身份)
├── TOOLS.md (工具配置)
└── self-improving/ (自我改进)
```

### **问题**
1. ❌ **碎片化** - 记忆分散在多个文件
2. ❌ **检索效率低** - 全文搜索，没有语义理解
3. ❌ **Token 消耗高** - 每次加载所有内容
4. ❌ **不可观测** - 不知道检索了什么

---

## ✨ OpenViking 解决方案

### **集成架构**
```
OpenClaw
    ↓
OpenViking (上下文数据库)
    ↓
L0: 核心记忆 (MEMORY.md + SOUL.md)
L1: 工作记忆 (memory/YYYY-MM-DD.md + AGENTS.md)
L2: 长期记忆 (历史归档 + self-improving)
```

---

## 🚀 集成步骤

### **步骤 1：安装 OpenViking**

```bash
# Python 包
pip install openviking --upgrade --force-reinstall

# Rust CLI（可选，用于高级管理）
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash
```

### **步骤 2：安装 OpenClaw Skill**

```bash
# 安装 OpenViking Skill
npx skills add swizardlv/openclaw_openviking_skill
```

### **步骤 3：配置模型**

创建 `~/.openclaw/openviking_config.json`：

```json
{
  "vlm": {
    "provider": "litellm",
    "model": "zhipu/glm-4",
    "api_key": "YOUR_ZHIPU_API_KEY"
  },
  "embedding": {
    "provider": "litellm",
    "model": "zhipu/embedding-2",
    "api_key": "YOUR_ZHIPU_API_KEY"
  }
}
```

### **步骤 4：迁移现有记忆**

```bash
# 创建 OpenViking 工作区
cd ~/.openclaw
mkdir -p openviking-workspace/{L0,L1,L2}

# 迁移 L0（核心记忆）
cp MEMORY.md openviking-workspace/L0/
cp SOUL.md openviking-workspace/L0/
cp USER.md openviking-workspace/L0/

# 迁移 L1（工作记忆）
cp -r memory openviking-workspace/L1/
cp AGENTS.md openviking-workspace/L1/
cp TOOLS.md openviking-workspace/L1/
cp HEARTBEAT.md openviking-workspace/L1/

# 迁移 L2（长期记忆）
cp -r self-improving openviking-workspace/L2/
```

### **步骤 5：更新 AGENTS.md**

在 `AGENTS.md` 中添加：

```markdown
## OpenViking 集成

### 记忆加载策略
- **L0 (始终加载)**: MEMORY.md, SOUL.md, USER.md
- **L1 (按需加载)**: memory/, AGENTS.md, TOOLS.md, HEARTBEAT.md
- **L2 (归档)**: self-improving/, 历史记忆

### 检索优化
- 使用 OpenViking 的目录递归检索
- 可视化检索轨迹
- 自动会话管理
```

---

## 💡 最佳实践

### **1. L0/L1/L2 分层策略**

| 层级 | 内容 | 加载策略 | Token 占比 |
|------|------|----------|-----------|
| **L0** | 核心身份 | 始终加载 | 10% |
| **L1** | 工作记忆 | 按需加载 | 30% |
| **L2** | 长期记忆 | 归档 | 60% |

### **2. 目录结构设计**

```
~/.openclaw/openviking-workspace/
├── L0/ (核心记忆)
│   ├── MEMORY.md
│   ├── SOUL.md
│   └── USER.md
├── L1/ (工作记忆)
│   ├── memory/
│   │   └── YYYY-MM-DD.md
│   ├── AGENTS.md
│   ├── TOOLS.md
│   └── HEARTBEAT.md
└── L2/ (长期记忆)
    ├── self-improving/
    ├── projects/
    └── archive/
        └── YYYY-MM/
```

### **3. 检索优化**

#### **3.1 语义搜索**
```python
# OpenViking 自动向量化
# 查询时自动语义匹配
query = "用户喜欢什么沟通风格"
# OpenViking 自动定位到 L0/USER.md
```

#### **3.2 目录递归检索**
```python
# 从 L1 开始检索
# 自动递归到子目录
# 精准定位相关内容
```

#### **3.3 可视化轨迹**
```bash
# 查看检索路径
ov_cli trace --query "MSA 开源进度"
# 输出：L1/HEARTBEAT.md → L2/projects/msa.md
```

### **4. 自动会话管理**

#### **4.1 自动压缩**
- 每次会话结束自动压缩
- 提取关键信息到长期记忆

#### **4.2 自动归档**
```python
# 30天自动降级
L1/memory/2026-02-20.md → L2/archive/2026-02/
```

---

## 📊 性能提升

### **Token 消耗对比**

| 场景 | 传统方式 | OpenViking | 节省 |
|------|----------|-----------|------|
| **启动加载** | 100% | 40% (L0+部分L1) | 60% |
| **检索查询** | 全文扫描 | 语义定位 | 70% |
| **长期运行** | 线性增长 | 自动压缩 | 50% |

### **预期效果**
- ✅ **Token 消耗**: ↓ 60%
- ✅ **检索速度**: ↑ 3x
- ✅ **准确率**: ↑ 40%
- ✅ **可观测性**: 100%

---

## 🔧 高级配置

### **1. 自定义层级**

```json
{
  "layers": {
    "L0": {
      "always_load": true,
      "max_tokens": 2000
    },
    "L1": {
      "on_demand": true,
      "max_tokens": 5000,
      "ttl_days": 30
    },
    "L2": {
      "archive": true,
      "compression": true
    }
  }
}
```

### **2. 检索策略**

```json
{
  "retrieval": {
    "strategy": "hybrid",  // semantic + keyword
    "max_results": 10,
    "min_score": 0.7
  }
}
```

### **3. 自动备份**

```bash
# 每周自动备份到 GitHub
# ~/.openclaw/scripts/backup-memory.sh 已配置
```

---

## ⚠️ 注意事项

### **1. 前置条件**
- ✅ Python 3.10+
- ✅ Go 1.22+（可选）
- ✅ API Key（智谱/OpenAI）

### **2. 迁移风险**
- ⚠️ 现有记忆需要重新组织
- ⚠️ 需要测试检索效果
- ⚠️ 可能需要调整配置

### **3. 成本考虑**
- VLM API 调用成本
- Embedding API 成本
- 但 Token 节省可抵消

---

## 🎯 实施计划

### **Phase 1：准备（今天）**
- [x] 研究 OpenViking 文档
- [ ] 准备 API Key
- [ ] 设计目录结构

### **Phase 2：安装（明天）**
- [ ] 安装 OpenViking
- [ ] 安装 OpenClaw Skill
- [ ] 配置模型

### **Phase 3：迁移（本周）**
- [ ] 迁移现有记忆
- [ ] 测试检索效果
- [ ] 调整配置

### **Phase 4：优化（下周）**
- [ ] 监控性能
- [ ] 优化层级
- [ ] 分享经验

---

## 💬 金句

> **像管理文件一样管理记忆，L0/L1/L2 让 Token 消耗砍半**

---

## 🔗 相关链接

- **OpenViking**: https://github.com/volcengine/OpenViking
- **Fork**: https://github.com/srxly888-creator/OpenViking
- **OpenClaw Skill**: https://github.com/swizardlv/openclaw_openviking_skill
- **文档**: https://www.openviking.ai/docs

---

**最后更新**: 2026-03-21 23:50
**状态**: 📋 规划中，待实施
**预期效果**: Token ↓60%, 检索 ↑3x
