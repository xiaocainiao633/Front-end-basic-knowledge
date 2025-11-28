# 将大预言模型的原始输出解析为JSON,XML,YAML等结构化数据
# 字符串解析器
from langchain_core.parsers import StrOutParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama imort ChatOllama
from loguru import logger

chat_prompt = ChatPromptTemplate.from_template([
    ("system", "你是一个{role}，请简短回答我提出的问题"),
    ("human", "请回答:{question}")
])

prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain"})
logger.info(prompt)

model = ChatOllama(model = "qwen3:14b", reasoning = False)

result = model.invoke(prompt)
logger.info(f"模型原始输出: {result}")

parser = StrOutputParser ()
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
# 打印类型
logger.info(f"结果类型: {type(response)}")
# 2025-10-26 09:21:17.693 | INFO     | __main__:<module>:14 - messages=[SystemMessage(content='你是一个AI助手，请简短回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:什么是LangChain', additional_kwargs={}, response_metadata={})]
# 2025-10-26 09:21:18.755 | INFO     | __main__:<module>:21 - 模型原始输出:
# content='LangChain 是一个用于构建基于语言模型的应用程序的框架，它提供了一系列工具和模块，帮助开发者更高效地创建和集成大型语言模型（LLM）到各种应用中。' additional_kwargs={} response_metadata={'model': 'qwen3:14b', 'created_at': '2025-10-26T01:21:18.755088718Z', 'done': True, 'done_reason': 'stop', 'total_duration': 994595117, 'load_duration': 16219578, 'prompt_eval_count': 38, 'prompt_eval_duration': 3534602, 'eval_count': 42, 'eval_duration': 972211135, 'model_name': 'qwen3:14b', 'model_provider': 'ollama'} id='lc_run--d26777d2-85e0-426a-8e2f-d4bf9403f5ae-0' usage_metadata={'input_tokens': 38, 'output_tokens': 42, 'total_tokens': 80}
# 2025-10-26 09:21:18.756 | INFO     | __main__:<module>:28 - 解析后的结构化结果:
# LangChain 是一个用于构建基于语言模型的应用程序的框架，它提供了一系列工具和模块，帮助开发者更高效地创建和集成大型语言模型（LLM）到各种应用中。
# 2025-10-26 09:21:18.756 | INFO     | __main__:<module>:31 - 结果类型: <class 'str'>

# JSON解析器
parser = JsonOutputParser()
# 调用解析器处理结果数据，将输入转换为JSON格式的响应
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")

# 打印类型
logger.info(f"结果类型: {type(response)}")
# 2025-10-26 09:22:49.818 | INFO     | __main__:<module>:14 - messages=[SystemMessage(content='你是一个AI助手，请简短回答我提出的问题，结果返回json格式，q字段表示问题，a字段表示答案。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:什么是LangChain', additional_kwargs={}, response_metadata={})]
# 2025-10-26 09:22:51.206 | INFO     | __main__:<module>:21 - 模型原始输出:
# content='```json\n{\n  "q": "什么是LangChain",\n  "a": "LangChain是一个用于构建应用程序的框架，它使开发人员能够利用大型语言模型（LLMs）和提示工程，以创建更复杂和实用的应用程序。"\n}\n```' additional_kwargs={} response_metadata={'model': 'qwen3:14b', 'created_at': '2025-10-26T01:22:51.206190176Z', 'done': True, 'done_reason': 'stop', 'total_duration': 1324524815, 'load_duration': 14647905, 'prompt_eval_count': 54, 'prompt_eval_duration': 4026242, 'eval_count': 57, 'eval_duration': 1303445312, 'model_name': 'qwen3:14b', 'model_provider': 'ollama'} id='lc_run--07fad35e-f0eb-4233-8b16-515c91169e72-0' usage_metadata={'input_tokens': 54, 'output_tokens': 57, 'total_tokens': 111}
# 2025-10-26 09:22:51.207 | INFO     | __main__:<module>:26 - 解析后的结构化结果:
# {'q': '什么是LangChain', 'a': 'LangChain是一个用于构建应用程序的框架，它使开发人员能够利用大型语言模型（LLMs）和提示工程，以创建更复杂和实用的应用程序。'}
# 2025-10-26 09:22:51.207 | INFO     | __main__:<module>:29 - 结果类型: <class 'dict'>

# 列表解析器
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from loguru import logger

# 创建逗号分隔列表输出解析器实例
parser = CommaSeparatedListOutputParser()

# 获取格式化指令，用于指导模型输出格式
format_instructions = parser.get_format_instructions()

# 创建聊天提示模板，包含系统消息和人类消息
# 系统消息定义了AI助手的行为规范和输出格式要求
# 人类消息定义了具体的任务请求，使用占位符{topic}表示主题
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", f"你是一个AI助手，你只能输出结构化列表数据。{format_instructions}"),
    ("human", "请生成5个关于{topic}的内容")
])

# 格式化聊天提示消息，将占位符替换为实际值
prompt = chat_prompt.format_messages(topic="小米", format_instructions=format_instructions)

# 记录格式化后的提示消息
logger.info(prompt)

# 创建ChatOllama模型实例，指定使用的模型名称和推理模式
model = ChatOllama(model="qwen3:14b", reasoning=False)

# 调用模型执行推理，传入格式化的提示消息
result = model.invoke(prompt)

# 记录模型返回的原始结果
logger.info(f"模型原始输出:\n{result}")

# 使用解析器处理模型返回的结果，将其转换为结构化列表
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")

# 打印类型
logger.info(f"结果类型: {type(response)}")

# 2025-10-26 09:24:20.830 | INFO     | __main__:<module>:24 - [SystemMessage(content='你是一个AI助手，你只能输出结构化列表数据。Your response should be a list of comma separated values, eg: `foo, bar, baz` or `foo,bar,baz`', additional_kwargs={}, response_metadata={}), HumanMessage(content='请生成5个关于小米的内容', additional_kwargs={}, response_metadata={})]
# 2025-10-26 09:24:21.195 | INFO     | __main__:<module>:33 - 模型原始输出:
# content='小米,手机,智能家居,性价比,生态链' additional_kwargs={} response_metadata={'model': 'qwen3:14b', 'created_at': '2025-10-26T01:24:21.194294372Z', 'done': True, 'done_reason': 'stop', 'total_duration': 300056068, 'load_duration': 15243857, 'prompt_eval_count': 69, 'prompt_eval_duration': 7562467, 'eval_count': 11, 'eval_duration': 274847866, 'model_name': 'qwen3:14b', 'model_provider': 'ollama'} id='lc_run--7275c44c-02a3-4d51-9fe9-7e200e87c003-0' usage_metadata={'input_tokens': 69, 'output_tokens': 11, 'total_tokens': 80}
# 2025-10-26 09:24:21.195 | INFO     | __main__:<module>:37 - 解析后的结构化结果:
# ['小米', '手机', '智能家居', '性价比', '生态链']
# 2025-10-26 09:24:21.195 | INFO     | __main__:<module>:40 - 结果类型: <class 'list'>

# XML解析器
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from loguru import logger

# 创建 XML 输出解析器实例
parser = XMLOutputParser()

# 获取格式化指令（这会告诉模型如何以 XML 格式输出）
format_instructions = parser.get_format_instructions()

# 创建提示模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", f"你是一个AI助手，只能输出XML格式的结构化数据。{format_instructions}"),
    ("human", "请生成5个关于{topic}的内容，每个内容包含<name>和<description>两个字段")
])

# 格式化提示，将 {topic} 替换为实际主题
prompt = chat_prompt.format_messages(topic="小米", format_instructions=format_instructions)

# 打印提示消息
logger.info(prompt)

# 创建 ChatOllama 模型实例
model = ChatOllama(model="qwen3:14b", reasoning=False)

# 执行推理
result = model.invoke(prompt)

# 记录模型原始输出
logger.info(f"模型原始输出:\n{result.content}")

# 解析 XML 输出为结构化 Python 对象（例如字典或列表）
response = parser.invoke(result)

# 打印解析后的结构化结果
logger.info(f"解析后的结构化结果:\n{response}")

# 打印类型
logger.info(f"结果类型: {type(response)}")

# 2025-10-26 09:18:48.265 | INFO     | __main__:<module>:22 - [SystemMessage(content='你是一个AI助手，只能输出XML格式的结构化数据。The output should be formatted as a XML file.\n1. Output should conform to the tags below.\n2. If tags are not given, make them on your own.\n3. Remember to always open and close all the tags.\n\nAs an example, for the tags ["foo", "bar", "baz"]:\n1. String "<foo>\n   <bar>\n      <baz></baz>\n   </bar>\n</foo>" is a well-formatted instance of the schema.\n2. String "<foo>\n   <bar>\n   </foo>" is a badly-formatted instance.\n3. String "<foo>\n   <tag>\n   </tag>\n</foo>" is a badly-formatted instance.\n\nHere are the output tags:\n```\nNone\n```', additional_kwargs={}, response_metadata={}), HumanMessage(content='请生成5个关于小米的内容，每个内容包含<name>和<description>两个字段', additional_kwargs={}, response_metadata={})]
# 2025-10-26 09:18:53.270 | INFO     | __main__:<module>:31 - 模型原始输出:
# <items>
#   <item>
#     <name>小米手机</name>
#     <description>小米手机是小米公司推出的一系列智能手机，以高性能和亲民的价格著称。</description>
#   </item>
#   <item>
#     <name>小米电视</name>
#     <description>小米电视以其高清晰度的屏幕和智能功能，成为家庭娱乐的首选设备。</description>
#   </item>
#   <item>
#     <name>小米智能家居</name>
#     <description>小米智能家居提供一系列互联设备，使用户能够通过手机控制家中的各种设备。</description>
#   </item>
#   <item>
#     <name>小米手环</name>
#     <description>小米手环是一款功能丰富的智能手环，支持健康监测、运动记录等多种功能。</description>
#   </item>
#   <item>
#     <name>小米笔记本</name>
#     <description>小米笔记本以其轻便的设计和强大的性能，成为学生和办公用户的理想选择。</description>
#   </item>
# </items>
# 2025-10-26 09:18:53.270 | INFO     | __main__:<module>:37 - 解析后的结构化结果:
# {'items': [{'item': [{'name': '小米手机'}, {'description': '小米手机是小米公司推出的一系列智能手机，以高性能和亲民的价格著称。'}]}, {'item': [{'name': '小米电视'}, {'description': '小米电视以其高清晰度的屏幕和智能功能，成为家庭娱乐的首选设备。'}]}, {'item': [{'name': '小米智能家居'}, {'description': '小米智能家居提供一系列互联设备，使用户能够通过手机控制家中的各种设备。'}]}, {'item': [{'name': '小米手环'}, {'description': '小米手环是一款功能丰富的智能手环，支持健康监测、运动记录等多种功能。'}]}, {'item': [{'name': '小米笔记本'}, {'description': '小米笔记本以其轻便的设计和强大的性能，成为学生和办公用户的理想选择。'}]}]}
# 2025-10-26 09:18:53.270 | INFO     | __main__:<module>:40 - 结果类型: <class 'dict'>

# Pydantic解析器
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from loguru import logger
from pydantic import BaseModel, Field, field_validator

class Product(BaseModel):
    """
    产品信息模型类，用于定义产品的结构化数据格式

    属性:
        name (str): 产品名称
        category (str): 产品类别
        description (str): 产品简介，长度必须大于等于10个字符
    """
    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        """
        验证产品简介字段的长度

        参数:
            value (str): 待验证的产品简介文本

        返回:
            str: 验证通过的产品简介文本

        异常:
            ValueError: 当产品简介长度小于10个字符时抛出
        """
        if len(value) < 10:
            raise ValueError('产品简介长度必须大于等于10')
        return value

# 创建Pydantic输出解析器实例，用于解析模型输出为Product对象
parser = PydanticOutputParser(pydantic_object=Product)

# 获取格式化指令，用于指导模型输出符合Product模型的JSON格式
format_instructions = parser.get_format_instructions()

# 创建聊天提示模板，包含系统消息和人类消息
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，你只能输出结构化的json数据\n{format_instructions}"),
    ("human", "请你输出标题为：{topic}的新闻内容")
])

# 格式化提示消息，填充主题和格式化指令
prompt = prompt_template.format_messages(topic="小米", format_instructions=format_instructions)

# 记录格式化后的提示消息
logger.info(prompt)

# 创建ChatOllama模型实例，使用qwen3:14b模型
model = ChatOllama(model="qwen3:14b", reasoning=False)

# 调用模型获取结果
result = model.invoke(prompt)

# 记录模型返回的结果
logger.info(f"模型原始输出:\n{result.content}")

# 使用解析器将模型结果解析为Product对象
response = parser.invoke(result)

# 打印解析后的结构化结果
logger.info(f"解析后的结构化结果:\n{response}")

# 打印类型
logger.info(f"结果类型: {type(response)}")
