# 并行函数调用
import json
import os
import dotenv
import httpx
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

# 加载环境变量配置
dotenv.load_dotenv()


@tool
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
    注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，则loc参数需要输入'Beijing'；
    :return：OpenWeather API查询即时天气的结果，具体URL请求地址为：https://api.openweathermap.org/data/2.5/weather\
    返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    # Step 1.构建请求
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2.设置查询参数
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 输入API key
        "units": "metric",  # 使用摄氏度而不是华氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3.发送GET请求
    response = httpx.get(url, params=params)

    # Step 4.解析响应
    data = response.json()
    return json.dumps(data)


# 初始化ChatOllama语言模型实例，用于处理自然语言任务
llm = ChatOllama(model="qwen3:14b", reasoning=False)

# 创建聊天提示模板，定义agent的对话结构和角色
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是天气助手，请根据用户的问题，给出相应的天气信息"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 定义可用工具列表，包含获取天气信息的工具函数
tools = [get_weather]

# 创建工具调用agent，整合语言模型、工具和提示模板。该agent能够根据用户问题调用相应工具获取天气信息
agent = create_tool_calling_agent(llm, tools, prompt)

# 创建agent执行器，负责协调agent和工具的执行流程
# agent参数指定要执行的agent实例
# tools参数提供agent可调用的工具列表
# verbose参数设置为True，启用详细输出模式便于调试
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行agent，处理用户关于北京和上海天气的查询请求
result = agent_executor.invoke({"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"})

# 输出执行结果
print(result)

# 多工具串联调用
import json
import os
import dotenv
import httpx
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

# 加载环境变量配置
dotenv.load_dotenv()


@tool
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
    注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，则loc参数需要输入'Beijing'；
    :return：OpenWeather API查询即时天气的结果，具体URL请求地址为：https://api.openweathermap.org/data/2.5/weather\
    返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    # Step 1.构建请求
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2.设置查询参数
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 输入API key
        "units": "metric",  # 使用摄氏度而不是华氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3.发送GET请求
    response = httpx.get(url, params=params)

    # Step 4.解析响应
    data = response.json()
    return json.dumps(data)


@tool
def write_file(content):
    """
    将指定内容写入本地文件。
    :param content: 必要参数，字符串类型，用于表示需要写入文档的具体内容。
    :return：是否成功写入
    """
    print(f"写入文件内容：{content}")
    return "已成功写入本地文件。"


# 初始化ChatOllama语言模型实例，用于处理自然语言任务
llm = ChatOllama(model="qwen3:14b", reasoning=False)

# 创建聊天提示模板，定义系统角色和用户输入格式
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "你是天气助手，请根据用户的问题，给出相应的天气信息，如果用户需要将查询结果写入文件，请使用write_file工具"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 定义可用工具列表，包括获取天气信息和写入文件功能
tools = [get_weather, write_file]

# 创建工具调用代理，整合语言模型、工具和提示模板
agent = create_tool_calling_agent(llm, tools, prompt)

# 创建代理执行器，用于执行代理任务并管理工具调用过程
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行用户查询任务，获取北京和上海的温度信息并写入文件
result = agent_executor.invoke({"input": "查一下北京和上海现在的温度，并将结果写入本地的文件中。"})

print(result)