# 独立学习仓库索引（2026-03-22 01:30）

## 🎯 策略调整

> **不只是一个仓库，每个热门项目都创建独立学习笔记**

---

## ✅ 已创建学习仓库（7个）

### **1. MiroFish - 37,844 Stars**
- **路径**: `~/.openclaw/workspace/MiroFish/LEARNING.md`
- **Quick Start**: 源码部署（Node.js + Python + uv）
- **学习路径**: 体验 → 部署 → 实战

### **2. OpenViking - 17,338 Stars**
- **路径**: `~/.openclaw/workspace/OpenViking/LEARNING.md`
- **Quick Start**: pip install + 模型配置
- **学习路径**: 理解 → 安装 → 集成

### **3. MAS Factory - 125 Stars**
- **路径**: `~/.openclaw/workspace/MASFactory/LEARNING.md`
- **Quick Start**: pip install + VS Code 插件
- **学习路径**: 入门 → 进阶 → 高级

### **4. GPT Researcher - 25,898 Stars**
- **路径**: `~/.openclaw/workspace/gpt-researcher/LEARNING.md`
- **Quick Start**: clone + API keys
- **学习路径**: 体验 → 定制 → 高级

### **5. Cherry Studio - 41,981 Stars**
- **路径**: `~/.openclaw/workspace/cherry-studio/LEARNING.md`
- **Quick Start**: 下载安装 + LLM 配置
- **学习路径**: 体验 → 定制 → 高级

### **6. Conductor - 31,557 Stars**
- **路径**: `~/.openclaw/workspace/conductor/LEARNING.md`
- **Quick Start**: npm install + 60秒启动
- **学习路径**: 体验 → 开发 → 生产

### **7. Pi Mono - 26,582 Stars**
- **路径**: `~/.openclaw/workspace/pi-mono/LEARNING.md`
- **Quick Start**: npm install + coding agent
- **学习路径**: 体验 → 集成 → 高级

---

## 📊 统计

| 项目 | Stars | LEARNING.md | Quick Start |
|------|-------|-------------|-------------|
| **Cherry Studio** | 41,981 | ✅ | ✅ |
| **MiroFish** | 37,844 | ✅ | ✅ |
| **Conductor** | 31,557 | ✅ | ✅ |
| **Pi Mono** | 26,582 | ✅ | ✅ |
| **GPT Researcher** | 25,898 | ✅ | ✅ |
| **OpenViking** | 17,338 | ✅ | ✅ |
| **MAS Factory** | 125 | ✅ | ✅ |
| **总计** | **181,625** | **7** | **7** |

---

## 🎯 原作者 Quick Start 总结

### **1. MiroFish**
```bash
# 前置要求
Node.js 18+, Python 3.11-3.12, uv

# 安装
cp .env.example .env
# 编辑 .env，填入 LLM API keys
cd frontend && npm install
cd ../backend && uv sync

# 启动
cd backend && uv run python main.py
cd frontend && npm run dev
```

### **2. OpenViking**
```bash
# 安装
pip install openviking --upgrade

# 配置模型
{
  "vlm": {
    "provider": "litellm",
    "model": "zhipu/glm-4",
    "api_key": "YOUR_KEY"
  }
}
```

### **3. MAS Factory**
```bash
# 安装
pip install -U masfactory

# VS Code 插件
搜索 "MASFactory Visualizer"
```

### **4. GPT Researcher**
```bash
# 克隆
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher

# 配置
export OPENAI_API_KEY={Your Key}
export TAVILY_API_KEY={Your Key}

# 启动
pip install -r requirements.txt
python main.py
```

### **5. Cherry Studio**
```bash
# 下载安装
访问官网下载

# 配置 LLM
支持 OpenAI, Gemini, Anthropic, Ollama
```

### **6. Conductor**
```bash
# 60秒启动
npm install -g @conductor-oss/conductor-cli
conductor server start

# 运行工作流
conductor workflow create workflow.json
conductor workflow start -w hello_workflow --sync
```

### **7. Pi Mono**
```bash
# 安装
npm install

# 构建
npm run build

# 运行 coding agent
./pi-test.sh
```

---

## 💡 学习路径对比

### **体验（30分钟）**
- MiroFish - Demo 体验
- OpenViking - 理解分层
- MAS Factory - 运行示例
- GPT Researcher - 运行研究
- Cherry Studio - 试用助手
- Conductor - 60秒启动
- Pi Mono - coding agent

### **部署（1-2小时）**
- MiroFish - 源码部署
- OpenViking - pip install
- MAS Factory - VS Code 插件
- GPT Researcher - API 配置
- Cherry Studio - LLM 配置
- Conductor - npm install
- Pi Mono - npm run build

### **实战（1周）**
- MiroFish - 金融预测
- OpenViking - OpenClaw 集成
- MAS Factory - 双模型配置
- GPT Researcher - 定制研究
- Cherry Studio - 自定义助手
- Conductor - 编写 workers
- Pi Mono - 集成工作流

---

## 🔄 下一步

### **继续创建**
- [ ] 为剩余 20+ 项目创建 LEARNING.md
- [ ] 整理原作者 Quick Start
- [ ] 建立学习路径

### **整合**
- [ ] 将所有 LEARNING.md 整合到主仓库
- [ ] 建立 cross-reference
- [ ] 上传到 NotebookLM

### **消耗 Token**
- [ ] 继续横向搜索
- [ ] 创建更多学习笔记
- [ ] 整理到知识流

---

**最后更新**: 2026-03-22 01:35
**策略**: 多仓库 + 独立学习笔记
**已创建**: 7 个 LEARNING.md
**总 Stars**: 181,625
