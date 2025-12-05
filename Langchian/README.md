# LangChain 核心模块解析

本项目是对 LangChain 核心功能模块的拆解与示例实现，涵盖 LLM 调用、工具链、记忆系统、Agent 等关键能力。

## 项目目录树

```
├── LCEL.py # LangChain 表达式语言（LCEL）示例
├── MCP.py # MCP 协议工具对接实现
├── Model.py # 大语言模型（LLM）调用封装
├── Parser.py # 输出解析器工具
├── Prompt.py # 提示词模板管理
├── RAG.py # 检索增强生成（RAG）实现
├── Tool.py # 自定义工具封装
├── agent.py # Agent 智能体逻辑
├── memory-bot.py # 带记忆功能的对话机器人案例
└── memory.py # 记忆系统核心实现v
```


## 文件功能说明

### 1. LCEL.py
LangChain 表达式语言（LCEL）的实践示例，包含：
- 用 LCEL 拼接 Chain（如 `prompt | model | parser`）
- 流式输出、并行执行等 LCEL 特性演示
- 自定义 LCEL 组件的封装方法


### 2. MCP.py
MCP（Model Context Protocol）协议的对接实现，包含：
- MCP 工具与 LangChain Tool 的转换逻辑
- 远程 MCP 服务的客户端封装
- MCP 工具的调用流程示例


### 3. Model.py
大语言模型（LLM）的统一调用接口，包含：
- 主流 LLM（如 OpenAI、Claude）的配置与初始化
- 同步/异步调用的封装
- 模型输出格式的统一处理


### 4. Parser.py
输出解析器的实现，包含：
- 文本到结构化数据（JSON、Pydantic 模型）的解析
- 错误处理与格式校验
- 针对不同 LLM 输出的适配逻辑


### 5. Prompt.py
提示词模板的管理工具，包含：
- 动态提示词模板的定义（变量替换、条件渲染）
- 多轮对话的提示词拼接逻辑
- 提示词优化（如少样本示例、角色设定）的示例


### 6. RAG.py
检索增强生成（RAG）的核心流程，包含：
- 文档加载、分割、向量化的实现
- 向量数据库的对接（如 Chroma、Pinecone）
- 检索结果与 LLM 的结合逻辑


### 7. Tool.py
自定义工具的封装与注册，包含：
- LangChain Tool 基类的扩展
- 工具入参校验与权限控制
- 工具调用结果的格式化处理


### 8. agent.py
Agent 智能体的核心逻辑，包含：
- 不同类型 Agent（Zero-Shot、React）的初始化
- Agent 工具选择的策略配置
- 多轮思考-行动循环的实现


### 9. memory-bot.py
**带记忆功能的对话机器人案例**，包含：
- 记忆系统与对话 Chain 的集成
- 多轮对话中上下文的保留与调用
- 实际可运行的对话交互演示


### 10. memory.py
记忆系统的核心实现，包含：
- 不同记忆类型（短期记忆、长期记忆）的封装
- 记忆的存储、检索与更新逻辑
- 记忆与 LLM 输入的结合方式
