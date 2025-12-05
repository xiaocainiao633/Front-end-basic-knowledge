from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.utilities import PythonREPL
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from loguru import logger


def debug_print(x):
    """
    调试打印函数，用于在链式调用中输出中间结果

    参数:
        x: 任意类型的输入值，将被打印并原样返回

    返回值:
        与输入值x相同的值
    """
    logger.info(f"中间结果:{x}")
    return x


# 创建Python REPL工具实例，用于执行生成的Python代码
tool = PythonREPL()

# 初始化Ollama语言模型，使用qwen3:8b模型
llm = ChatOllama(model="qwen3:8b", reasoning=False)

# 定义聊天提示模板，包含系统指令和用户问题占位符
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你只返回纯净的 Python 代码，不要解释。代码必须是单行或多行 print。"),
        ("human", "{question}")
    ]
)

# 创建调试节点，用于在链式调用中插入调试信息输出
debug_node = RunnableLambda(debug_print)

# 创建字符串输出解析器，用于解析模型输出
parser = StrOutputParser()

# 构建处理链：提示模板 -> 语言模型 -> 调试输出 -> 输出解析 -> 代码执行
chain = prompt | llm | debug_node | parser | RunnableLambda(lambda code: tool.run(code))

# 执行链式调用，计算1到100的整数总和
result = chain.invoke({"question": "计算1到100的整数总和"})
logger.info(result)

# 装饰器
from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field


class FieldInfo(BaseModel):
    """
    定义加法运算所需的参数信息
    """
    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")

# 通过args_schema定义参数信息，也可以定义name、description、return_direct参数
@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    """
    两个整数相加
    """
    return a + b


# 打印工具的基本信息
logger.info(f"name = {add_number.name}")
logger.info(f"args = {add_number.args}")
logger.info(f"description = {add_number.description}")
logger.info(f"return_direct = {add_number.return_direct}")

# 调用工具执行加法运算
res = add_number.invoke({"a": 1, "b": 2})
logger.info(res)


# StructuredTool
from langchain_core.tools import StructuredTool
from loguru import logger
from pydantic import BaseModel, Field


class FieldInfo(BaseModel):
    """
    定义加法运算所需的参数信息
    """
    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")


def add_number(a: int, b: int) -> int:
    """
    两个整数相加
    """
    return a + b


func = StructuredTool.from_function(
    func=add_number,
    name="Add",
    description="两个整数相加",
    args_schema=FieldInfo
)
logger.info(f"name = {func.name}")
logger.info(f"description = {func.description}")
logger.info(f"args = {func.args}")

res = func.invoke({"a": 1, "b": 2})
logger.info(res)

# llm判断
from datetime import date
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from loguru import logger


@tool
def get_today() -> str:
    """
    获取当前系统日期

    Returns:
        str: 今天的日期字符串，格式为 yyyy-MM-dd
    """
    logger.info("执行工具：get_today")
    return date.today().isoformat()


# 设置本地模型，不使用深度思考
llm = ChatOllama(model="qwen3:14b", reasoning=False)
# 将工具绑定到语言模型
llm_with_tools = llm.bind_tools([get_today])
# 用户提问
question_list = ["你是谁？","今天是几号？"]
for question in question_list:
    logger.info(f"用户问题：{question}")
    # 调用语言模型处理用户问题
    ai_msg = llm_with_tools.invoke(question)
    logger.info(f"LLM回复：{ai_msg}")
    # 检查是否有工具调用
    if ai_msg.tool_calls:
        logger.info(ai_msg.tool_calls)
        # 获取第一个工具调用信息
        tool_call = ai_msg.tool_calls[0]
        # 执行对应的工具函数并获取结果
        tool_result = locals()[tool_call["name"]].invoke(tool_call["args"])
        logger.info(f"调用工具结果：{tool_result}")
    else:
        # 直接输出语言模型的回答
        logger.info(f"LLM 直接作答：{ai_msg.content}")