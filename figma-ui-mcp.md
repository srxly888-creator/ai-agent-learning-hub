# Figma UI MCP - AI 直接画 UI（2026-03-21）

## 📚 来源

- **推文**: https://x.com/qingq77/status/2035327311680012373
- **作者**: Geek Lite (@QingQ77)
- **时间**: 2026-03-21
- **GitHub**: https://github.com/TranHoaiHung/figma-ui-mcp

---

## 💥 核心亮点

> **把「让 AI 在 Figma 里直接画 UI」做成了标准的 MCP 双向通道**

---

## ✨ 核心功能

### **1. figma_write - AI 画 UI**
- ✅ 用一段 JS 指令画 UI
- ✅ 支持多种元素：
  - Frame（框架）
  - 文本
  - 组件
  - 变量

### **2. figma_read - AI 读 UI**
- ✅ 把现有设计读成结构化树
- ✅ 读取样式信息
- ✅ 甚至截图

---

## 🔄 双向通道

```
Claude（或其他 MCP client）
    ↕️
Figma UI MCP（标准 MCP 通道）
    ↕️
Figma 设计文件
```

---

## 💡 使用场景

### **1. AI 生成 UI**
- 自然语言描述需求
- AI 自动生成 Figma 设计
- 无需手动绘制

### **2. 设计转代码**
- 读取现有 Figma 设计
- 生成代码实现
- 设计到开发无缝衔接

### **3. 设计自动化**
- 批量生成设计
- 模板化设计
- 设计系统维护

---

## 🎯 与 MAS Factory 的关系

### **潜在集成**
```
MAS Factory（工作流设计）
    ↓
Figma UI MCP（设计生成）
    ↓
AI 绘制 UI
    ↓
开发实现
```

### **使用场景**
- 产品设计工作流
- 设计到开发流程
- UI 自动化生成

---

## 📊 对比其他方案

| 方案 | 类型 | 优势 | 劣势 |
|------|------|------|------|
| **Figma UI MCP** | MCP 标准 | 双向、标准 | 需要配置 |
| **直接 Figma API** | API | 灵活 | 复杂 |
| **AI 生成图片** | 图片 | 快速 | 不可编辑 |
| **手绘 UI** | 手动 | 精确 | 慢 |

---

## 💡 学习价值

### **技术层面**
1. **MCP 集成** - 如何实现 MCP 双向通道
2. **Figma API** - 如何操作 Figma 设计
3. **JS 指令** - 如何用代码生成 UI
4. **结构化树** - 如何解析设计结构

### **产品层面**
1. **设计自动化** - AI 自动生成设计
2. **设计开发衔接** - 无缝转换
3. **效率提升** - 减少手动工作
4. **标准化** - MCP 标准通道

---

## 🔧 技术架构

### **核心组件**
```
MCP Client（Claude/Codex）
    ↓
Figma UI MCP Server
    ├─ figma_write（写）
    │   ├─ Frame
    │   ├─ 文本
    │   ├─ 组件
    │   └─ 变量
    └─ figma_read（读）
        ├─ 结构化树
        ├─ 样式信息
        └─ 截图
    ↓
Figma 文件
```

---

## 🚀 快速开始

### **1. 安装**
```bash
# 克隆项目
git clone https://github.com/TranHoaiHung/figma-ui-mcp.git

# 配置 Figma API token
# 配置 MCP server
```

### **2. 使用**
```javascript
// 在 Claude 中说：
"用 figma_write 创建一个登录页面"

// AI 会生成 JS 指令
// 直接在 Figma 中绘制 UI
```

---

## 🎯 适用人群

### **1. 产品经理**
- 快速生成原型
- 验证想法
- 与设计师协作

### **2. 开发者**
- 设计转代码
- UI 自动化
- 设计系统

### **3. 设计师**
- AI 辅助设计
- 批量生成
- 效率提升

---

## 💡 与今天学习的关联

### **MCP 相关**
- **今天学习**: MCP 是已验证概念
- **Figma UI MCP**: MCP 的实际应用案例
- **学习价值**: 理解 MCP 的实际应用

### **设计工具**
- **今天收集**: designprompts.dev（UI 提示词）
- **Figma UI MCP**: AI 直接操作 Figma
- **互补**: 提示词 + 操作工具

---

## 🔗 相关链接

- **推文**: https://x.com/qingq77/status/2035327311680012373
- **作者**: @QingQ77
- **GitHub**: https://github.com/TranHoaiHung/figma-ui-mcp

---

## 🎯 行动计划

### **今天**
- [ ] 了解 Figma UI MCP 的核心功能
- [ ] 查看 GitHub 仓库

### **本周**
- [ ] 配置 Figma API token
- [ ] 测试 figma_write 功能
- [ ] 尝试生成简单 UI

### **两周内**
- [ ] 集成到 MAS Factory 工作流
- [ ] 设计自动化流程
- [ ] 分享使用经验

---

## 💬 金句

> **把「让 AI 在 Figma 里直接画 UI」做成了标准的 MCP 双向通道**

---

## 📈 市场影响

### **对设计师**
- AI 辅助设计
- 效率提升
- 新的工作方式

### **对开发者**
- 设计转代码
- 自动化流程
- 无缝衔接

### **对 AI**
- MCP 标准化
- 更多应用场景
- 双向交互能力

---

## 🔮 未来展望

### **可能的发展**
- 更丰富的元素支持
- 更智能的布局
- 更好的样式管理
- 团队协作功能

### **与 AI 的深度结合**
- 智能设计建议
- 自动化设计系统
- 批量设计生成
- 设计优化建议

---

## ⚠️ 注意事项

### **配置要求**
- 需要 Figma API token
- 需要 MCP client
- 需要一定的技术背景

### **最佳实践**
- 从简单设计开始
- 逐步增加复杂度
- 充分测试验证
- 保持设计一致性

---

**最后更新**: 2026-03-21 21:50
**来源**: @QingQ77
**GitHub**: https://github.com/TranHoaiHung/figma-ui-mcp
