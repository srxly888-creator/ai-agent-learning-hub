# MAS Factory + OpenClaw 快速入门

## 🎯 集成方案

- **方案 2**: 双模型策略（GLM-5 规划 + GLM-4-Flash 执行）
- **方案 3**: OpenClaw 调用 MAS Factory

## 📦 已配置

1. **配置文件**: `~/.openclaw/workspace/masfactory_config.py`
   - 规划模型: GLM-5
   - 执行模型: GLM-4-Flash
   - baseUrl: https://open.bigmodel.cn/api/coding/paas/v4

2. **OpenClaw Skill**: `~/.openclaw/skills/masfactory-workflow/`
   - 可从 OpenClaw 对话直接调用 MAS Factory

3. **测试脚本**: `~/.openclaw/workspace/test_masfactory.py`

## ⚠️ 需要手动设置 API Key

由于 OpenClaw 不暴露 API key 给外部程序，你需要手动设置：

```bash
# 方式 1：设置环境变量（推荐）
export ZHIPU_API_KEY="your-zhipu-api-key"

# 方式 2：添加到 ~/.bashrc
echo 'export ZHIPU_API_KEY="your-zhipu-api-key"' >> ~/.bashrc
source ~/.bashrc
```

**获取 API Key**:
1. 访问：https://open.bigmodel.cn/
2. 登录 → 控制台 → API Keys
3. 复制你的 API Key

## 🚀 测试运行

```bash
# 1. 设置 API Key
export ZHIPU_API_KEY="your-api-key"

# 2. 运行测试
cd ~/.openclaw/workspace
python test_masfactory.py
```

**预期输出**:
```
🔧 测试 MAS Factory + OpenClaw 集成
==================================================
✅ 工作流创建成功
📊 节点：analyze → answer

✅ 工作流构建成功

🚀 运行测试：
问题：我想学习 AI Agent，但不知道从哪里开始

✅ 执行成功！

📝 回答：
[AI 的回答]

==================================================
🎉 测试通过！MAS Factory + OpenClaw 集成成功
```

## 💡 使用方式

### 方式 1：直接在 Python 中使用

```python
from masfactory import RootGraph, Agent, NodeTemplate
from masfactory_config import invoke_model

BaseAgent = NodeTemplate(Agent, model=invoke_model)

g = RootGraph(
    name="my_workflow",
    nodes=[
        ("step1", BaseAgent(instructions="第一步")),
        ("step2", BaseAgent(instructions="第二步")),
    ],
    edges=[
        ("entry", "step1", {"input": "用户输入"}),
        ("step1", "step2", {"output": "第一步输出"}),
        ("step2", "exit", {"result": "最终结果"}),
    ],
)

g.build()
out, _ = g.invoke({"input": "测试"})
print(out["result"])
```

### 方式 2：从 OpenClaw 对话调用

**你说**：
```
用 MAS Factory 设计一个代码审查工作流
```

**OpenClaw 会**：
1. 识别你的需求
2. 加载 masfactory-workflow skill
3. 调用 MAS Factory API
4. 返回结果

### 方式 3：Vibe Graphing（自然语言生成工作流）

```python
from masfactory import RootGraph, VibeGraph
from masfactory_config import build_model, invoke_model

g = RootGraph(name="vibe_demo")

vibe = g.create_node(
    VibeGraph,
    name="vibe_graph",
    invoke_model=invoke_model,  # 执行
    build_model=build_model,    # 规划
    build_instructions="设计一个软件开发流程：需求分析→编码→测试→部署",
)

g.edge_from_entry(receiver=vibe, keys={})
g.edge_to_exit(sender=vibe, keys={})

g.build()
g.invoke(input={}, attributes={})
```

## 📊 成本对比

| 方案 | 规划模型 | 执行模型 | 成本 |
|------|----------|----------|------|
| 传统 | GPT-4 | GPT-4 | $6.08 |
| 双模型 | GLM-5 | GLM-4-Flash | $0.26 |
| **节省** | - | - | **95%** |

## 🔧 故障排查

### 问题 1：❌ 未找到 API key

**解决**:
```bash
export ZHIPU_API_KEY="your-api-key"
```

### 问题 2：❌ 网络连接失败

**可能原因**:
- 网络问题
- baseUrl 错误

**检查**:
```bash
curl https://open.bigmodel.cn/api/coding/paas/v4/models
```

### 问题 3：❌ 模型名称错误

**可用模型**:
- `glm-5` - 高阶推理（规划模型）
- `glm-4-air` - 轻量级执行（执行模型）
- `glm-4.7` - 通用
- `glm-4.7-flash` - 快速
- `glm-4.7-flashx` - 极速

## 📚 学习资源

- **官方文档**: https://bupt-gamma.github.io/MASFactory/
- **论文**: http://arxiv.org/abs/2603.06007
- **本地仓库**: `~/.openclaw/workspace/MASFactory`
- **配置文件**: `~/.openclaw/workspace/masfactory_config.py`
- **测试脚本**: `~/.openclaw/workspace/test_masfactory.py`

## 🎯 下一步

1. ✅ 设置 API Key
2. ✅ 运行测试脚本
3. ✅ 学习基础示例
4. ✅ 设计自己的工作流
5. ✅ 集成到 OpenClaw 对话
