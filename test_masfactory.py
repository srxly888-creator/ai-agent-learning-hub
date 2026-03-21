"""
测试 MAS Factory + OpenClaw 集成
"""

import os
import sys

# 添加工作区路径
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace"))

from masfactory import RootGraph, Agent, NodeTemplate
from masfactory_config import invoke_model

print("🔧 测试 MAS Factory + OpenClaw 集成")
print("=" * 50)

# 创建基础 Agent 模板
BaseAgent = NodeTemplate(Agent, model=invoke_model)

# 创建两阶段问答工作流
g = RootGraph(
    name="two_stage_qa",
    nodes=[
        ("analyze", BaseAgent(
            instructions="你是问题分析专家，分析用户问题的核心需求。",
            prompt_template="用户问题：{query}\n\n请分析这个问题的核心需求。"
        )),
        ("answer", BaseAgent(
            instructions="你是解决方案专家，基于分析给出最终回答。",
            prompt_template="问题：{query}\n分析：{analysis}\n\n请给出最终回答。"
        )),
    ],
    edges=[
        ("entry", "analyze", {"query": "用户问题"}),
        ("analyze", "answer", {"query": "原始问题", "analysis": "分析结果"}),
        ("answer", "exit", {"answer": "最终回答"}),
    ],
)

print("✅ 工作流创建成功")
print("📊 节点：analyze → answer")
print()

# 构建工作流
g.build()
print("✅ 工作流构建成功")
print()

# 运行测试
print("🚀 运行测试：")
test_query = "我想学习 AI Agent，但不知道从哪里开始"
print(f"问题：{test_query}")
print()

try:
    out, _attrs = g.invoke({"query": test_query})
    print("✅ 执行成功！")
    print()
    print("📝 回答：")
    print(out.get("answer", "无输出"))
    print()
    print("=" * 50)
    print("🎉 测试通过！MAS Factory + OpenClaw 集成成功")
except Exception as e:
    print(f"❌ 执行失败：{e}")
    print()
    print("💡 可能的原因：")
    print("1. API key 未设置")
    print("2. 网络连接问题")
    print("3. 模型名称错误")
    print()
    print("请检查 masfactory_config.py 中的配置")
