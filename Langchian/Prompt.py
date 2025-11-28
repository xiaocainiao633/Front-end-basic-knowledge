# 文本提示词模板 promptTemplate
# 创建提示词
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(template="你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"，
                        input_variables = ['role', 'question'])

# format()：给input_variables变量赋值，并返回提示词。
prompt = template.format(rols = "python开发", question = "冒泡排序怎么写？")
print(prompt)
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？

# 调用from_template()
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
prompt = template.format(role = "python开发", question = "冒泡排序怎么写？")
print(prompt)
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我

# 部分提示词模板
from datetime import detatime
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",
                                        partial_variables = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
prompt1 = template.format(question = "今天是几号？")
print(prompt1)

template2 = PromptTemplate.from_template("现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",)
partial = template.partial(time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt2 = partial.format(question = "今天是几号？")
print(prompt2)
# 现在时间是：2025-10-22 10:51:26,请对我的问题给出答案，我的问题是：今天是几号？
# 现在时间是：2025-10-22 10:51:26,请对我的问题给出答案，我的问题是：今天是几号？

# 组合提示词模板
from langchain_core.prompts import PromptTemplate

template1 = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n") + "内容不超过{length}个字"
prompt1 = template1.format(topic = "LangChain", length = 20)
print(prompt1)

prompt_a = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
prompt_b = PromptTemplate.from_template("内容不超过{length}个字")
prompt_all = prompt_a + prompt_b
prompt2 = prompt_all.format(topic = "LangChain", length = 20)
print(prompt2)
# 请用一句话介绍量子纠缠，要求通俗易懂
# 内容不超过20个字
# 请用一句话介绍量子纠缠，要求通俗易懂
# 内容不超过20个字

# 提示词方法
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
prompt = template.foemat(role = "python开发", question = "冒泡排序怎么写？")
# 输出生成的提示词
print(prompt)
print(type(prompt))
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
# <class 'str'>

# partial方法
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
partial = template.partial(role = "python开发")
print(partial)
print(type(partial))

prompt = partial.format(question = "冒泡排序怎么写？")
print(prompt)
print(type(prompt))
# input_variables=['question'] input_types={} partial_variables={'role': 'python开发'} template='你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}'
# <class 'langchain_core.prompts.prompt.PromptTemplate'>
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
# <class 'str'>

# invoke方法
from langchain_core.prompts import PromptTemplate
template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
prompt = template.invoke({"role": "python开发", "question": "冒泡排序怎么写？"})
print(prompt)
print(type(prompt))

print(prompt.to_string())
print(type(prompt.to_string()))
# text='你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？'
# <class 'langchain_core.prompt_values.StringPromptValue'>
# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
# <class 'str'>


# 对话提示词模板ChatPromptTemplate
# 创建提示词

from langchain_core.prompts import CHatPromptTemplate

prmpt_template = ChatPromptTemplate([
    ("system", "你是一个AI助手，你的名字是{name}"),
    ("human", "你能做什么事"),
    ("ai", "我可以陪你聊天，讲笑话，写代码"),
    ("human", "{user_input}"),
])

prompt = prompt_template.format(name = "小张", user_input = "你可以做什么？")
print(prompt)
# System: 你是一个AI助手，你的名字是小张
# Human: 你能做什么事
# AI: 我可以陪你聊天，讲笑话，写代码
# Human: 你可以做什么

# 调用from_message()
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请回答我提出的问题"),
    ("human", "请回答:{question}")    
])

prompt_value = chat_prompt.invoke({"role": "python开发工程师", "question": "冒泡排序怎么写"})
print(prompt_value.to_string())
# System: 你是一个python开发工程师，请回答我提出的问题
# Human: 请回答:冒泡排序怎么写

prompt_value = chat_prompt.format_messages(role="python开发工程师", question="冒泡排序怎么写")
print(prompt_value)
# [SystemMessage(content='你是一个python开发工程师，请回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:冒泡排序怎么写', additional_kwargs={}, response_metadata={})]

prompt = chat_prompt.format_prompt(role="python开发工程师", question="冒泡排序怎么写")
print(prompt)
print(prompt.to_messages())

# messages=[SystemMessage(content='你是一个python开发工程师，请回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:冒泡排序怎么写', additional_kwargs={}, response_metadata={})]
# [SystemMessage(content='你是一个python开发工程师，请回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:冒泡排序怎么写', additional_kwargs={}, response_metadata={})]

# 实例化参数类型 str:
from langchain_core.prompts import ChatPromptTemplate

# 创建聊天提示模板，用于构建AI助手的对话上下文
# 该模板包含两个消息：AI助手的自我介绍和用户问题
chat_prompt = ChatPromptTemplate.from_messages([
    "你是AI助手，你的名字叫{name}。",
    "请问：{question}"
])
message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")
print(message)
# [HumanMessage(content='你是AI助手，你的名字叫亮仔。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问：什么是LangChain', additional_kwargs={}, response_metadata={})]

# dict:
chat_prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
    {"role": "user", "content": "请问：{question}"}
])
# [SystemMessage(content='你是AI助手，你的名字叫亮仔。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问：什么是LangChain', additional_kwargs={}, response_metadata={})]

# message:
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你是AI助手，你的名字叫{name}。"),
    HumanMessage(content="请问：{question}")
])
# [SystemMessage(content='你是AI助手，你的名字叫{name}。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问：{question}', additional_kwargs={}, response_metadata={})]

# 少量样本提示词模板
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {"input": "北京下雨吗", "output": "北京"},
    {"input": "上海热吗", "output": "上海"},
]

example_prompt = PromptTemplate(
    input_variables = ["input", "output"],
    template = "输入：{input}\n输出：{output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    prefix = "按提示的格式，输出内容",
    suffix="输入：{input}\n输出：",
    input_variables = ["input"]
)

print(few_shot_prompt.format(input="天津今天刮风吗"))

