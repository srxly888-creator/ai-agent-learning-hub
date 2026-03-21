# Codex Autoresearch - 自主目标驱动实验引擎

## 🎯 概述

**Codex 的自主目标驱动实验引擎**

一个 Codex skill，在你的代码库上运行 **"修改-验证-决策"** 循环。

---

## 🔄 核心机制

### **Modify-Verify-Decide Loop**

```
┌─────────────┐
│  Modify     │ ← 每次迭代做一个原子改动
└──────┬──────┘
       ↓
┌─────────────┐
│   Verify    │ ← 用机械化指标验证
└──────┬──────┘
       ↓
┌─────────────┐
│   Decide    │ ← 保留或丢弃
└──────┬──────┘
       │
       ├─ 成功 → 提交到 git
       └─ 失败 → 自动回滚
```

---

## ✨ 特性

- ✅ **原子改动** - 每次迭代只改一处
- ✅ **机械化验证** - 用指标判断成功/失败
- ✅ **自动回滚** - 失败自动撤销
- ✅ **进展累积** - 成功的改动累积在 git 中
- ✅ **跨语言** - 适用于任何语言、任何框架
- ✅ **可测量目标** - 任何可测量的目标都能优化

---

## 🚀 快速开始

### 1. 安装

```bash
# 方式 1：手动安装
git clone https://github.com/leo-lilinxiao/codex-autoresearch.git
cp -r codex-autoresearch your-project/.agents/skills/codex-autoresearch

# 方式 2：Codex 内置安装器
$skill-installer install https://github.com/leo-lilinxiao/codex-autoresearch
```

### 2. 使用

```text
$codex-autoresearch
I want to get rid of all the `any` types in my TypeScript code
```

### 3. Codex 自动运行

```
Codex: I found 47 `any` occurrences across src/**/*.ts.

       Confirmed:
       - Target: eliminate `any` types in src/**/*.ts
       - Metric: `any` count (current: 47), direction: lower
       - Verify: grep + tsc --noEmit as guard

       Need to confirm:
       - Run until all gone, or cap at N iterations?

       Reply "go" to start, or tell me what to change.

You:   Go, run overnight.

Codex: Starting -- baseline: 47. Iterating until interrupted.
```

---

## 📊 适用场景

### **代码质量**
- 消除 `any` 类型
- 减少代码复杂度
- 提高测试覆盖率
- 修复 lint 警告

### **性能优化**
- 降低延迟
- 减少内存占用
- 优化算法复杂度

### **重构**
- 提取重复代码
- 简化条件逻辑
- 优化数据结构

---

## 🎯 与 Karpathy Autoresearch 的关系

**灵感来源**: [Karpathy's autoresearch](https://github.com/karpathy/autoresearch)

**核心思想**:
> 一个简单的循环 —— 修改、验证、保留或丢弃、重复 —— 可以在夜间将 ML 训练从基线推向新高。

**codex-autoresearch 的创新**:
> 将这个循环泛化到软件工程中所有可以用数字衡量的东西。

---

## 🔧 架构

```
┌────────────────────────────────────┐
│          Codex Autoresearch        │
├────────────────────────────────────┤
│  ┌──────────────────────────────┐  │
│  │  Modify - Verify - Decide    │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Git Integration             │  │
│  │  - Progress tracking         │  │
│  │  - Auto-rollback             │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌──────────────────────────────┐  │
│  │  Metric System               │  │
│  │  - Any measurable goal       │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

---

## 📖 文档

- **安装指南**: [INSTALL.md](https://github.com/leo-lilinxiao/codex-autoresearch/blob/main/docs/INSTALL.md)
- **使用手册**: [GUIDE.md](https://github.com/leo-lilinxiao/codex-autoresearch/blob/main/docs/GUIDE.md)
- **示例配方**: [EXAMPLES.md](https://github.com/leo-lilinxiao/codex-autoresearch/blob/main/docs/EXAMPLES.md)

---

## 🔗 链接

- **GitHub**: https://github.com/leo-lilinxiao/codex-autoresearch
- **Fork**: https://github.com/srxly888-creator/codex-autoresearch
- **来源**: https://x.com/qingq77/status/2035189655180808445
- **作者**: @leo-lilinxiao

---

## 💡 关键洞察

1. **简单循环的力量** - 修改-验证-决策，三个步骤就够了
2. **机械化指标** - 用数字说话，避免主观判断
3. **原子改动** - 每次只改一处，易于追踪和回滚
4. **自动回滚** - 失败自动撤销，不影响代码库
5. **过夜运行** - 适合长时间、无监督的优化任务

---

## 🎯 与 MAS Factory 的对比

| 特性 | MAS Factory | Codex Autoresearch |
|------|-------------|-------------------|
| **类型** | 多智能体编排 | 单目标优化 |
| **适用场景** | 复杂工作流 | 可测量目标 |
| **核心机制** | 图结构协作 | 修改-验证循环 |
| **时间尺度** | 分钟级 | 小时/过夜级 |
| **人工介入** | Vibe Graphing | 仅启动时确认 |

---

## 🚀 实战建议

### **最佳使用场景**
- 大规模重构（消除 `any` 类型）
- 性能优化（降低延迟）
- 代码质量提升（提高测试覆盖率）

### **不适合的场景**
- 需要人工判断的任务
- 无法量化的目标
- 需要即时反馈的任务

---

**最后更新**: 2026-03-21 21:10
**来源**: @QingQ77
