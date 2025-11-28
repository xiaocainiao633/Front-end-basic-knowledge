# 创建项目 uv init LangchainDemo
# 进入项目目录 cd LangchainDemo
# 安装Langchain包 uv add langchain
# 创建密钥环境变量 touch .env
# 编辑 .env 文件，添加 OPENAI_API_KEY=你的密钥
# .env文件内容如下：
DEEPSEEK_API_KEY = XXXX
QWEN_API_KEY = XXXX
OPENAI_API_KEY = XXXX

import os
from dotennv import load_dotenv
load_dotenv(override = True)
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

# 接入大模型：Langchain 中大模型分为几种：LLM, Chat Model, Embedding Model
# 接入ollama
from langchain_ollama import ChatOllama

# 不启动深度思考
model = ChatOllama(base_url = "http:??localhost:11434", model = "qwen3:14b", reasoning = false)
print(model.invoke("什么是LangChain?"))
# 执行结果如下：
# context="**Langchain** 是一个..."

# 接入deepseek
import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
load_dotenv(override=True)
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

model = ChatDeepSeek(
    # 支持模型列表
    # deepseek-chat：通用对话模型
    # deepseek-coder：偏向代码理解与生成
    # deepseek-llm：较大通用模型（如 DeepSeek-VL）
    # deepseek-moe：Mixture of Experts 多专家模型
    model = "deepseek-chat",
    temperature = 0,
    max_token = None,
    timeout = None,
    max_retries = 2,
    api_key = deepseek_api_key,
)

print(model.invoke("什么是Langchain?"))

# 接入通义千问Qwen
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
load_dotenv(override=True)
qwen_api_key = os.getenv("QWEN_API_KEY")

model = ChatTongyi(
    model = "Qwen-VL-Chat-14B",
    temperature = 0,
    max_token = None,
    timeout = None,
    max_retries = 2,
    api_key = qwen_api_key,    
)
print(model.invoke("什么是LangChain?"))

# 接入openAI
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
load_dotenv(override=True)
openai_api_key = os.getenv("OPEN_API_KEY")

model = ChatOpenAI(
    api_key = openai_api_key,
    model = "gpt-4",
    temperature = 0.3,
)
print(model.invoke("什么是LangChain?"))

# 模型调用方法
# 聊天模型，除了将字符串作为输入外，还可以使用聊天消息作为输入，并返回聊天消息作为输出。LangChain有一些内置的消息类型：
# HumanMessage：人类消息，type为"user"，表示来自用户输入。比如“实现 一个快速排序方法”。
# AIMessage： AI 消息，type为"ai"，这可以是文本，也可以是调用工具的请求。
# SystemMessage：系统消息，type为"system"，告诉大模型当前的背景是什么，应该如何做，并不是所有模型提供商都支持这个消息类型
# ToolMessage/FunctionMessage：工具消息，type为"tool"，用于函数调用结果的消息类型
# ChatMessage：可以自定义角色的通用消息类型。

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatPllama(base_url "http://localhost:11434", model = "qwen3:14b", reasoning = False)

messages = [SystemMessage(context = "你叫小亮，是一个乐于助人的人工助手")，
            HumanMessage(content = "你是谁？")
            ]

response = model.invoke(messages)
print(response.content)
print(type(response))
# 我是小亮，一个乐于助人的人工助手。我在这里是为了帮助你解决问题、提供建议和支持。无论是生活上的小烦恼，还是工作上的难题，我都会尽力帮你。有什么需要帮忙的吗？
# <class 'langchain_core.messages.ai.AIMessage'>

# 流式输出
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

model = ChatPllama(base_url "http://localhost:11434", model = "qwen3:14b", reasoning = False)

messages = [SystemMessage(context = "你叫小亮，是一个乐于助人的人工助手")，
            HumanMessage(content = "你是谁？")
            ]

response = model.stream(messages)

for chunk in response:
    print(chunk.content, end = "", flush = True) # 刷新缓冲区 (无换行符，缓冲区未刷新，内容可能不会立即显示

print("\n")
print(type(response))

# 我是小亮，一个乐于助人的人工助手。很高兴认识你！我在这里可以帮助你解决问题、提供信息，或者只是陪你聊天。有什么我可以帮你的吗？
# <class 'generator'>

# 批量调用
from langchain_ollama import ChatOllama

model = ChatOllama(base_url = "http://localhost:11434", model = "qwen3:14b", reasoning = False)

questions = [
    "什么是LangChain？",
    "Python的生成器是做什么的？",
    "解释一下Docker和Kubernetes的关系"    
]

response = model.batch(questions)
for q, r in zip(questions, response):
    print(f"Q: {q}\nA: {r}\n")

# 异步调用
import asyncio
from langchain_ollama import CHatOllama

model = ChatOllama(base_url = "http://localhost:11434", model = "qwen3:14b" reasoning = False)

async def main():
    response = await model.ainvoke("什么是LangChain?")
    print(response)
asyncio.run(main())