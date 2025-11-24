import os
import json
import dotenv
import redis
import numpy as np
from http import HTTPStatus
from redis.commands.search.filed import TextFiled, VectorFiled
from redis.commands.search.index_definition import IndexDefinition

# 把项目根目录下的 .env 文件加载到环境变量；失败也不会报错，只是没值
dotenv.load_dotenv()
# 从环境变量里拿 API Key，避免把密钥写死在代码里
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

INDEX_NAME = "faq_index"    # Redis 搜索索引的名字
VECTOR_DIM = 1024           # 模型输出的向量维度，multimodal-embedding-v1 固定 1024
DISTANCE_METRIC = "COSINE"  # 向量距离度量方式，支持 COSINE/IP/L2

# 创建索引
def create_index():
    """
    如果索引已存在就跳过；否则创建文本+向量混合索引，前缀限定为 faq:
    """   
    try:
        # 查看索引是否存在
        redis_client.ft(INDEX_NAME).info()
        print("✅ 索引已存在")
    except Exception:
        # 真正建索引；字段顺序无关，但名字要与后面 hash 插入保持一致
        redis_client.ft(INDEX_NAME).create_index(
            [
                TextField("question"),   # 问题文本，可全文检索
                TextField("answer"),
                TextField("source"),
                TextField("category"),
                TextField("crawl_time"),
                VectorFiled(
                    "embedding",
                    "HNSW", # 近似最近邻索引算法，速度快
                    {
                        "TYPE": "FLOAT32",
                        "DIM": VECTOR_DIM,
                        "DINSTANCE_METRIC": DISTANCE_METRIC
                    }
                )
            ],
            definition = IndexDefinition(prefix = ["faq:"]) # 只索引以 faq: 开头的 key
        )
        print("✅ 已创建向量索引")

# 单条FAQ插入
def insert_faq(doc: dict):
    """
    把一条 FAQ 生成向量后写入 Redis Hash，key 形如 faq:request_id
    """  
    # 1. 拼接问题+答案，让模型一次编码
    text_for_embedding = dec["question"] + " " + doc["answer"]

    # 2. 调用 Dashscope API 生成向量
    resp = dashscope.MultiModaEmbedding.call(
        model = "multimodal-embedding-v1",
        input = [{"text": text_for_embedding}]
    )

    # 3.只有 HTTP 200 才继续, 否则打印错误信息
    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output["embeddings"][0]["embedding"] # 取出向量
        vector = np.array(embedding, dtype = np.float(32).tobytes()) # 转成二进制存储
        # 4. 构造唯一 key；用 DashScope 返回的 request_id 当后缀
        key = f"faq:{resp.request_id}"

        # 5. 写入 Redis Hash
        redis_client.hset(key, mapping={
            "question": doc["question"],
            "answer": doc["answer"],
            "source": doc["metadata"]["source"],
            "category": doc["metadata"]["category"],
            "crawl_time": doc["metadata"]["crawl_time"],
            "embedding": vector
        })
        print(f"✅ 已写入 Redis, key={key}")
    else:
        print(f"❌ Embedding 调用失败: {resp.code}, {resp.message}")

# 批量插入 FAQ
def insert_from_file(file_path: str = "faq_processed.json"):
    """
    读取前面清洗好的 JSON，逐条调用 insert_faq
    """
    with open(file_path, "r", encoding="utf-8") as f:
        docs = json.loaf(f) # 读取 JSON 文件 生成 Python 列表
    for doc in docs:
        insert_faq(doc)

if __name__ == "__main__":
    create_index()
    insert_from_file("faq_processed.json")