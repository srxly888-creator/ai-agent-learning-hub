"""
MAS Factory 双模型策略配置

规划模型（build_model）: GLM-5（高阶推理）
执行模型（invoke_model）: GLM-4-Air（轻量级执行）

成本优化：$6.08 → $0.26（暴砍 95%）
"""

import os
from masfactory import OpenAIModel

# API 配置（共用 OpenClaw 的 GLM 配置）
# ⚠️ 需要手动设置环境变量：
# export ZHIPU_API_KEY="your-api-key"
API_KEY = os.getenv("ZHIPU_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = "https://open.bigmodel.cn/api/coding/paas/v4"  # OpenClaw 使用的地址

if not API_KEY:
    raise ValueError(
        "❌ 未找到 API key！请设置环境变量：\n"
        "export ZHIPU_API_KEY='your-zhipu-api-key'\n"
        "或\n"
        "export OPENAI_API_KEY='your-zhipu-api-key'"
    )

# 规划模型（贵，但用量少）
build_model = OpenAIModel(
    model_name="glm-5",  # 高阶推理
    api_key=API_KEY,
    base_url=BASE_URL,
)

# 执行模型（便宜，用量大）
invoke_model = OpenAIModel(
    model_name="glm-4-air",  # 轻量级执行
    api_key=API_KEY,
    base_url=BASE_URL,
)

# 导出
__all__ = ["build_model", "invoke_model", "API_KEY", "BASE_URL"]
