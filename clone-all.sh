#!/bin/bash

# 一键克隆所有 AI Agent 学习仓库

echo "🚀 开始克隆 AI Agent Learning Hub 相关仓库..."
echo ""

# 定义仓库列表
repos=(
  "https://github.com/srxly888-creator/ai-agent-learning-hub.git"
  "https://github.com/srxly888-creator/ai-agent-workflow-engine.git"
  "https://github.com/srxly888-creator/rag-knowledge-system.git"
  "https://github.com/srxly888-creator/ai-business-automation.git"
  "https://github.com/srxly888-creator/ai-security-governance.git"
)

# 定义 Fork 的原始仓库
forks=(
  "https://github.com/BUPT-GAMMA/MASFactory.git"
  "https://github.com/wuyayru/MiroFish.git"
  "https://github.com/nopinduoduo/OpenViking.git"
  "https://github.com/Ai4Finance/TradingAgents.git"
)

# 创建目录
mkdir -p ai-agent-ecosystem
cd ai-agent-ecosystem

echo "📁 创建目录: ai-agent-ecosystem"
echo ""

# 克隆主仓库
echo "1️⃣ 克隆主学习仓库..."
git clone https://github.com/srxly888-creator/ai-agent-learning-hub.git
echo ""

# 克隆分类仓库
echo "2️⃣ 克隆分类仓库..."
for repo in "${repos[@]:1}"; do
  if [ "$repo" != "https://github.com/srxly888-creator/ai-agent-learning-hub.git" ]; then
    echo "   - $(basename "$repo" .git)"
    git clone "$repo"
  fi
done
echo ""

# 克隆 Fork 的原始仓库（可选)
read -p "是否克隆原始仓库（MASFactory, MiroFish, OpenViking, TradingAgents）? [y/N] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "3️⃣ 克隆原始仓库..."
  for fork in "${forks[@]}"; do
    echo "   - $(basename "$fork" .git)"
    git clone "$fork"
  done
  echo ""
fi

# 完成
echo "✅ 克隆完成！"
echo ""
echo "📊 仓库统计:"
echo "   - 主仓库: 1 个"
echo "   - 分类仓库: 4 个"
echo "   - 原始仓库: 4 个（可选）"
echo ""
echo "📂 目录结构:"
ls -la
echo ""
echo "💡 下一步:"
echo "   1. cd ai-agent-learning-hub"
echo "   2. cat README.md"
echo "   3. 开始学习！"
