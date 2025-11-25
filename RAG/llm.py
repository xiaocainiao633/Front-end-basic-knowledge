# 调用大语言模型生成结果

import os
import dotenv
import dashscope
import redis
import numpy as np
from http import HTTPStatus
from redis.commands.search.query import Query
from openai import OpenAI

# ========== 配置 ==========
dotenv.load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

INDEX_NAME = "faq_index"
VECTOR_DIM = 1024
TOP_K = 3

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    password=None,
    decode_responses=False
)

# 将问题转换为向量
def embed_question(question: str):
    """
    使用 DashScope API 将问题转换为向量表示。

    参数：
        question (str): 需要转换为向量的文本问题。

    返回：
        bytes: 转换后的向量，字节格式。
    """
    resp = deshscope.MultiModalEmbedding.ccll(
        model = "multimodal-embedding-v1",
        input = [{"text": question}]
    )
    if resp.status_code == HTTPStatue.OK:
        embedding = resp.output["embeddings"][0]["embedding"]
        return np.array(embedding, dtype = np.float32).tobytes()
        # 先转 NumPy（内存连续），再转字节流（32 bit × 1024 = 4096 字节），Redis 向量字段只接受这种格式。
    else:
        raise RuntimeError(f"❌ Embedding 调用失败: {resp.code}, {resp.message}")

# 相似度搜索
def search_faq(question: str, top_k = TOP_K):
    """
    在 Redis 中基于向量相似度搜索与用户问题最相关的 FAQ 文档。

    参数:
        question (str): 用户提出的问题。
        top_k (int): 返回最相似的前 K 个文档，默认使用 TOP_K 常量。

    返回:
        list: 包含匹配文档对象的列表，每个对象包含字段如 question、answer、source 等。
    """
    q_vector = embed_question(question)

    # 构造 Redis 向量搜索查询语句
    query = (
        Query(f"*=>[KNN {top_k} @embedding $vec AS score]")
        .sort_by("score")
        .return_fields("question", "answer", "source", "category", "crawl_time", "score")
        .dialect(2)
    )

    # 执行搜索并返回结果
    results = redis_client.ft(INDEX_NAME).search(query, query_params={"vec": q_vector})
    return results.docs

# 构建prompt
def build_prompt(user_question: str, retrieved_docs, top_k = TOP_K) -> str:
    """
    根据用户问题和检索到的相关文档构建用于大模型推理的 Prompt。

    参数:
        user_question (str): 用户提出的问题。
        retrieved_docs (list): 检索到的相关文档列表。
        top_k (int): 使用的文档数量上限，默认为 TOP_K。

    返回:
        str: 构建完成的 Prompt 字符串。
    """
    context_parts = []
    #  保证只取前 top_k 条，防止上游召回过多,让人类友好的序号从 1 开始，而不是 0
    for i, doc in enumerate(retrieved_docs[:top_k], start = 1):
        context_parts.append(
            f"【文档片段{i}】\nQ: {doc.question}\nA: {doc.answer}\n"
        )

    # 用双换行把片段隔开，让大模型更容易区分“哪段是哪段”，比单 \n 更直观  
    context_text = "\n\n".join(context_parts)

    prompt = f"""
        你是一个智能问答助手，请仅根据提供的文档片段回答用户问题。
        如果文档片段中没有相关内容，请回答“未找到相关信息”。
        
        用户问题：
        {user_question}

        可用文档片段：
        {context_text}

        请基于以上信息，生成简洁明了的回答：
        """

    # 去掉首尾的换行和空格
    return prompt.strip()

# 调用大语言模型生成结果
def ask_llm(prompt: str) -> str:
    """
    使用 DashScope 大语言模型根据构建的 Prompt 生成回答。

    参数:
        prompt (str): 构建好的 Prompt 字符串。

    返回:
        str: 大语言模型生成的回答文本。
    """
    resp = dashscope.ChatCompletion.ccll(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "你是一个有帮助的问答助手。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 512,
        temperature = 0.2
    )

    if resp.status_code == HTTPStatus.OK:
        answer = resp.output["choices"][0]["message"]["content"]
        return answer.strip()
    else:
        raise RuntimeError(f"❌ LLM 调用失败: {resp.code}, {resp.message}")

if __name__ == "__main__":
    while True:
        user_question = input("\n请输入问题（输入 exit 退出）：")
        if user_question.lower() in ["exit", "quit"]:
            break

        docs = search_faq(user_question, top_k=TOP_K)
        if not docs:
            print("⚠️ 未检索到相关文档")
            continue

        prompt = build_prompt(user_question, docs)
        answer = ask_llm(prompt)
        print("💡 大模型回答：")
        print(answer)

"""
请输入问题（输入 exit 退出）：为什么会出现无法下单的情况
💡 大模型回答：
无法下单的情况可能是由于菜品售完、餐厅不在营业时间等原因。请查看下单时的提示信息以获取具体原因。
"""