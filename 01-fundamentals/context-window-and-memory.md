# 🧠 上下文窗口与记忆系统 — 为什么 Agent 会"失忆"？

## 📚 基本信息

| 项目 | 内容 |
|------|------|
| **主题** | AI Agent 的记忆系统设计 |
| **适用** | Agent 开发者、产品经理、AI 爱好者 |
| **前置知识** | [什么是 AI Agent](./what-is-agent.md)、[RAG 检索增强生成](./rag-retrieval-augmented-generation.md) |

---

## 🎯 一句话理解

> **大模型就像一个记忆力有限的天才——它什么都懂，但转头就忘。记忆系统就是帮它"记笔记"的笔记本，让它在对话中不再"失忆"。**

---

## ❓ 为什么 Agent 会"失忆"？

你一定遇到过这种场景：

```
第一轮对话：
你："我叫小明，今年25岁，做前端的"
AI："你好小明！很高兴认识你~"

... 聊了几十轮之后 ...

你："我叫什么名字来着？"
AI："抱歉，我没有保存你之前的信息 😅"
```

这就是经典的 **Agent 失忆问题**。原因很简单：

### 上下文窗口（Context Window）有限

大语言模型每次处理信息时，都有一个"容量上限"，叫做 **上下文窗口**：

| 模型 | 上下文窗口 | 大约能记住 |
|------|-----------|-----------|
| GPT-4o | 128K tokens | ~10 万字 |
| Claude 3.5 Sonnet | 200K tokens | ~15 万字 |
| Gemini 1.5 Pro | 1M tokens | ~75 万字 |
| GPT-4o-mini | 128K tokens | ~10 万字 |

> **注意**：虽然看起来很大，但这里装的不只是你的对话，还包括系统提示词、工具定义、函数返回结果等。实际留给"记忆"的空间远比你想象的小。

### Token 是什么？

简单说，**1 个 token ≈ 0.75 个英文单词 ≈ 0.5 个中文字**。

```
"你好世界" → 大约 4-6 个 tokens
"I love AI" → 大约 3-4 个 tokens
```

所以 128K tokens 大概能装：
- 一本中等长度的小说（~10 万中文字）
- 或几十轮深度对话 + 工具调用结果

---

## 🧩 三种记忆：短期、长期、外部

Agent 的记忆系统一般分三层，类比人脑：

```
┌─────────────────────────────────────┐
│         Agent 记忆架构               │
│                                      │
│  ┌───────────────────────────────┐  │
│  │  📋 短期记忆（工作记忆）       │  │
│  │  - 当前对话上下文              │  │
│  │  - 最近几轮交互               │  │
│  │  - 容量：几K~几十K tokens     │  │
│  └───────────────┬───────────────┘  │
│                  ↓                    │
│  ┌───────────────────────────────┐  │
│  │  📖 长期记忆（持久化记忆）     │  │
│  │  - 用户偏好 & 历史信息         │  │
│  │  - 知识库 & 经验              │  │
│  │  - 容量：理论上无限            │  │
│  └───────────────┬───────────────┘  │
│                  ↓                    │
│  ┌───────────────────────────────┐  │
│  │  💾 外部记忆（向量数据库）     │  │
│  │  - 向量化存储的语义记忆         │  │
│  │  - 按相关性检索                │  │
│  │  - 容量：取决于存储            │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 1. 短期记忆（Working Memory）

就是**当前对话窗口里的内容**。你跟 AI 说了什么、AI 回了什么，全在这个窗口里。

```python
# 短期记忆本质上就是一个消息列表
short_term_memory = [
    {"role": "system", "content": "你是一个友好的助手"},
    {"role": "user", "content": "我叫小明"},
    {"role": "assistant", "content": "你好小明！"},
    {"role": "user", "content": "我今年25岁"},
    {"role": "assistant", "content": "25岁，正是好年纪！"},
    # ... 对话越长，这个列表越长
    # 一旦超出上下文窗口，最早的消息就会被"挤出去"
]
```

**特点**：
- ✅ 实时性好，直接存在于上下文中
- ❌ 容量有限，会被新内容"挤掉"
- ❌ 对话结束后就消失了

**优化技巧**：

```python
# 技巧1：消息截断 — 保留最近 N 轮对话
def truncate_messages(messages, max_rounds=10):
    """只保留最近 10 轮（20条）消息"""
    # 保留系统提示
    system_msg = [m for m in messages if m["role"] == "system"]
    # 保留最近的对话
    recent = messages[-(max_rounds * 2):]
    return system_msg + recent

# 技巧2：消息摘要 — 把旧对话压缩成摘要
def summarize_old_messages(messages, summarizer):
    """把旧对话压缩成一段摘要"""
    old_messages = messages[:-10]  # 最近10轮之前的
    if not old_messages:
        return messages
    summary = summarizer(f"请用3句话总结以下对话要点：\n{old_messages}")
    return [
        {"role": "system", "content": f"之前的对话摘要：{summary}"},
        *messages[-10:]  # 最近10轮完整保留
    ]
```

### 2. 长期记忆（Long-term Memory）

把重要信息**持久化存储**到数据库或文件中，下次对话还能调出来。

```
短期记忆 → 对话结束就没了
长期记忆 → 存到数据库，永远都在（只要你存了）
```

**常见实现方式**：

```python
# 方式1：简单的 JSON 文件存储
import json

class SimpleMemory:
    def __init__(self, filepath="user_memory.json"):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self):
        try:
            with open(self.filepath) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save(self, key, value):
        """保存一条记忆"""
        self.data[key] = value
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def recall(self, key):
        """回忆一条记忆"""
        return self.data.get(key, "我不记得了")

# 使用
memory = SimpleMemory()
memory.save("name", "小明")
memory.save("age", 25)
print(memory.recall("name"))  # 输出: 小明
```

```python
# 方式2：关系型数据库（适合结构化数据）
import sqlite3

class SQLMemory:
    def __init__(self, db_path="agent_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                key TEXT,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def save(self, user_id, key, value):
        self.conn.execute(
            'INSERT INTO memories (user_id, key, value) VALUES (?, ?, ?)',
            (user_id, key, value)
        )
        self.conn.commit()
    
    def recall(self, user_id, key):
        cursor = self.conn.execute(
            'SELECT value FROM memories WHERE user_id=? AND key=? ORDER BY timestamp DESC LIMIT 1',
            (user_id, key)
        )
        row = cursor.fetchone()
        return row[0] if row else None
```

### 3. 外部记忆（向量数据库 + RAG）

这是最强大的记忆方式——把信息**向量化**存入向量数据库，需要时按**语义相似度**检索。

```
用户问："我之前跟你说过我喜欢什么运动吗？"

→ 问题向量化 → [0.12, -0.34, 0.56, ...]
→ 在向量数据库中搜索相似向量
→ 找到："我喜欢打篮球和游泳"（相似度 0.92）
→ 把这条记忆注入到上下文中
→ AI 回答："你之前说过喜欢打篮球和游泳 🏀🏊"
```

```python
# 用 ChromaDB 实现向量记忆
import chromadb
from chromadb.utils import embedding_functions

class VectorMemory:
    def __init__(self):
        # 使用本地嵌入函数
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.client = chromadb.PersistentClient(path="./memory_db")
        self.collection = self.client.get_or_create_collection(
            name="agent_memory",
            embedding_function=self.embedding_fn
        )
    
    def save(self, content, metadata=None):
        """保存一条记忆（自动向量化）"""
        import uuid
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[metadata or {}]
        )
        return doc_id
    
    def recall(self, query, n_results=3):
        """根据语义检索相关记忆"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

# 使用
memory = VectorMemory()
memory.save("小明喜欢打篮球和游泳", {"type": "preference", "user": "xiaoming"})
memory.save("小明做前端的，用 React", {"type": "profile", "user": "xiaoming"})
memory.save("小明之前做了一个电商项目", {"type": "project", "user": "xiaoming"})

# 语义检索
results = memory.recall("小明的工作")
# 结果可能返回："小明做前端的，用 React"（语义最相关）
```

---

## 🏗️ 主流记忆方案对比

### 方案一：MemGPT（Letta）

**MemGPT** 是一个革命性的记忆系统，灵感来自操作系统虚拟内存的概念。

```
传统 LLM：
┌─────────────────────┐
│   有限上下文窗口     │ → 信息满了就丢失
└─────────────────────┘

MemGPT：
┌─────────────────────┐
│   主上下文窗口       │ → 类似"内存"
├─────────────────────┤
│   换出区（磁盘）     │ → 类似"硬盘"
├─────────────────────┤
│   检索记忆           │ → 类似"按需加载"
└─────────────────────┘

当上下文快满时，MemGPT 会：
1. 把不常用的对话"换出"到外部存储
2. 需要时再"换入"回来
3. 就像操作系统管理内存一样！
```

**核心特点**：
- 🔄 自动管理上下文窗口，不会"爆内存"
- 📝 内置记忆管理函数（插入、搜索、替换记忆）
- 🧠 支持对话记忆 + 召回记忆 + 归档记忆

```python
# MemGPT 使用示例
from memgpt import Agent, Client

client = Client()

# 创建带记忆的 Agent
agent = client.create_agent(
    name="我的助手",
    system_prompt="你是一个有记忆的助手，能记住用户的偏好和历史对话",
    memory_functions=True  # 启用记忆函数
)

# Agent 会自动调用这些记忆函数：
# - core_memory_append()    → 添加核心记忆
# - core_memory_replace()   → 替换核心记忆
# - conversation_search()   → 搜索历史对话
# - conversation_search_date() → 按日期搜索对话
# - archival_memory_insert() → 归档记忆
# - archival_memory_search() → 搜索归档记忆
```

### 方案二：Memu 记忆系统

**Memu** 是一个更轻量的记忆方案，专注于给 Agent 提供结构化的记忆能力。

```python
# Memu 核心概念
class MemuMemory:
    """
    Memu 的记忆层次：
    1. 核心记忆 (Core) - Agent 的人设、目标、关键信息
    2. 场景记忆 (Scenario) - 特定场景下的事件记忆
    3. 概念记忆 (Concept) - 从交互中提炼的知识
    """
    pass
```

> 📖 想深入了解 Memu？请看我们的 [Memu 记忆系统详解](../04-advanced/memu-memory-system.md)

### 方案三：RAG 作为记忆

用 RAG（检索增强生成）来做记忆，是最实用的方案：

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

class RAGMemory:
    """用 RAG 实现的 Agent 记忆系统"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_texts([], self.embeddings)
        self.llm = ChatOpenAI(temperature=0)
    
    def remember(self, text, metadata=None):
        """Agent 记住一条信息"""
        self.vectorstore.add_texts([text], metadatas=[metadata or {}])
    
    def recall(self, question, k=3):
        """Agent 回忆相关信息"""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        return qa.run(question)

# 使用示例
memory = RAGMemory()
memory.remember("用户偏好暗色主题的代码编辑器")
memory.remember("用户主要使用 Python 和 TypeScript")

# 语义检索
answer = memory.recall("用户喜欢什么样的编辑器？")
# → "根据记忆，用户偏好暗色主题的代码编辑器"
```

---

## 📊 三种方案对比

| 特性 | 简单存储 | MemGPT | RAG 向量记忆 |
|------|---------|--------|-------------|
| **实现复杂度** | ⭐ 简单 | ⭐⭐⭐ 较高 | ⭐⭐ 中等 |
| **记忆类型** | 精确匹配 | 智能管理 | 语义检索 |
| **容量** | 有限 | 理论无限 | 取决于存储 |
| **自动管理** | ❌ 手动 | ✅ 自动换入换出 | ❌ 手动/规则 |
| **语义理解** | ❌ | ✅ | ✅ |
| **适用场景** | 简单偏好存储 | 长对话助手 | 知识密集型 Agent |

---

## 🛠️ 实战：构建一个完整的记忆系统

下面是一个综合了三种记忆层次的完整示例：

```python
import json
import chromadb
from datetime import datetime

class CompleteMemorySystem:
    """
    三层记忆系统：
    1. 短期记忆 - 对话上下文
    2. 长期记忆 - 结构化存储
    3. 外部记忆 - 向量数据库
    """
    
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.short_term = []  # 当前对话的消息列表
        
        # 长期记忆：JSON 文件
        self.long_term_path = f"./memories/{user_id}_long_term.json"
        self.long_term = self._load_long_term()
        
        # 外部记忆：向量数据库
        self.vector_client = chromadb.PersistentClient(path="./vector_memory")
        self.collection = self.vector_client.get_or_create_collection(
            name=f"memory_{user_id}"
        )
    
    def _load_long_term(self):
        try:
            with open(self.long_term_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {"profile": {}, "preferences": {}, "history": []}
    
    def add_message(self, role, content):
        """添加消息到短期记忆"""
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def extract_and_save(self, content):
        """
        从对话中提取重要信息并保存
        （实际项目中用 LLM 来提取，这里简化处理）
        """
        # 保存到长期记忆
        self.long_term["history"].append({
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_long_term()
        
        # 保存到向量记忆
        import uuid
        self.collection.add(
            documents=[content],
            ids=[str(uuid.uuid4())],
            metadatas=[{"timestamp": datetime.now().isoformat()}]
        )
    
    def get_context(self, max_messages=10):
        """
        获取完整的上下文（用于发送给 LLM）
        包含：长期记忆摘要 + 最近对话
        """
        # 构建系统提示（包含长期记忆）
        profile = self.long_term.get("profile", {})
        profile_text = "\n".join(f"- {k}: {v}" for k, v in profile.items())
        
        system_prompt = f"""你是一个有记忆的 AI 助手。

关于用户的信息：
{profile_text}

请根据这些记忆信息来回答问题。"""

        # 获取最近的对话
        recent_messages = self.short_term[-max_messages:]
        
        return [
            {"role": "system", "content": system_prompt},
            *recent_messages
        ]
    
    def search_memory(self, query, n=3):
        """在向量记忆中搜索"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )
        return results['documents'][0] if results['documents'] else []
    
    def _save_long_term(self):
        with open(self.long_term_path, 'w') as f:
            json.dump(self.long_term, f, ensure_ascii=False, indent=2)
```

---

## 💡 最佳实践

### 1. 什么该记，什么不该记？

```
✅ 应该记住的：
- 用户的基本信息（名字、职业、偏好）
- 重要的决策和结论
- 用户反复提到的需求
- 项目关键信息

❌ 不需要记住的：
- 闲聊内容（"哈哈"、"好的"）
- 临时性的问题（"今天天气怎么样"）
- 敏感信息（密码、银行卡号）
```

### 2. 记忆过期策略

```python
import time

class ExpiringMemory:
    """带过期时间的记忆"""
    
    def save(self, key, value, ttl_seconds=86400*30):  # 默认30天过期
        memory_item = {
            "value": value,
            "created_at": time.time(),
            "ttl": ttl_seconds
        }
        # 保存到数据库...
    
    def recall(self, key):
        item = self._load(key)
        if item and time.time() - item["created_at"] < item["ttl"]:
            return item["value"]
        return None  # 过期了，当作不记得
```

### 3. 记忆的分层加载

不要一股脑把所有记忆都塞进上下文，按需加载：

```python
def build_context_for_query(query, user_memory):
    """根据问题智能加载记忆"""
    
    # 始终加载：核心人设信息（很短）
    always_load = user_memory.get_core_profile()
    
    # 按需加载：根据问题检索相关记忆
    relevant_memories = user_memory.search(query, n=3)
    
    # 组装上下文
    context = f"""
    核心信息：{always_load}
    
    相关记忆：
    {chr(10).join(relevant_memories)}
    """
    
    return context
```

### 4. 用 LLM 提取关键信息

```python
EXTRACTION_PROMPT = """
请从以下对话中提取值得记住的关键信息。
返回 JSON 格式：

对话：
{conversation}

返回格式：
{{
    "profile": {{"key": "value"}},
    "preferences": ["偏好1", "偏好2"],
    "important_facts": ["事实1", "事实2"]
}}
"""
```

---

## 🔮 记忆系统的未来趋势

### 1. 自主记忆管理
Agent 自动决定什么该记、什么该忘，不需要人工干预。

### 2. 记忆压缩
像人脑一样，把详细记忆压缩成"要点"，长期保留要点而非原文。

### 3. 跨 Agent 记忆共享
多个 Agent 之间共享记忆池，协同工作。

### 4. 情景记忆
不仅记住"说了什么"，还记住"在什么情境下说的"。

---

## 📚 总结

```
Agent 记忆系统 = 短期记忆 + 长期记忆 + 外部记忆

短期记忆 → 当前对话上下文，容量有限
长期记忆 → 持久化存储，结构化数据
外部记忆 → 向量数据库，语义检索

入门推荐：先从 RAG 向量记忆开始
进阶推荐：尝试 MemGPT 的自动记忆管理
终极目标：Agent 自主管理自己的记忆
```

| 层级 | 类比 | 技术 | 适用场景 |
|------|------|------|---------|
| 短期记忆 | 聊天窗口 | 消息列表 | 当前对话 |
| 长期记忆 | 笔记本 | JSON/DB | 用户偏好 |
| 外部记忆 | 图书馆 | 向量数据库 | 知识检索 |

> 💡 **核心要点**：没有记忆的 Agent 只是一个无状态的计算器。记忆系统让 Agent 从"工具"变成了"伙伴"。

---

## 🔗 相关链接

- [RAG 检索增强生成](./rag-retrieval-augmented-generation.md)
- [Memu 记忆系统详解](../04-advanced/memu-memory-system.md)
- [MSA 记忆架构](../04-advanced/msa-memory.md)
- [Agent 设计模式](./agent-design-patterns.md)
- [什么是 AI Agent](./what-is-agent.md)
