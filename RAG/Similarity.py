import os
import dotenv
import dashscope
import redis
import numpy as np
from http import HTTPStatus
from redis.commands.search.query import Query

# ========== 配置 ==========
# 加载环境变量
dotenv.load_dotenv()
# 设置 DashScope API 密钥
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# Redis 向量索引名称
INDEX_NAME = "faq_index"
# 向量维度，用于模型 "multimodal-embedding-v1"
VECTOR_DIM = 1024
# 默认返回最相似的前 K 条结果
TOP_K = 3

# 初始化 Redis 客户端连接
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
    根据用户输入的问题，在 Redis 中进行向量相似度搜索，返回最相关的 FAQ 条目。

    参数:
        question (str): 用户提出的问题。
        top_k (int): 返回最相似的前 K 条结果，默认值为 TOP_K。
    """
    # 将问题转换为向量
    q_vector = embed_question(question)

    # 构造KNN查询语句
    query = (
        # 在所有文档（*）里做 K 近邻搜索，把向量字段 @embedding 与参数 $vec 比距离，返回 top_k 个，并把距离写入临时字段 score
        Query(f"*=>[KNN{top_k} @embedding $vec AS score]")
        .sort_by("score")
        .return_fileds("question", "answer", "source", "category", "crawl_time", "score")
        .dialect(2)
    )

    # 执行查询并获取结果
    results = redis_client.ft(INDEX_NAME).search(query, query_params = {"vec": q_vector})

    print(f"\n🔎 用户问题: {question}")
    print(f"📊 召回 {len(results.docs)} 条结果\n")

     # 打印每条匹配结果的详细信息
    for i, doc in enumerate(results.docs, start=1):
        print(f"--- Top {i} ---")
        print(f"相似度分数: {doc.score}")
        print(f"Q: {doc.question}")
        print(f"A: {doc.answer}")
        print(f"来源: {doc.source}")
        print(f"类别: {doc.category}")
        print(f"时间: {doc.crawl_time}")
        print()

if __name__ == "__main__":
    # 测试用例：模拟用户提问
    test_question = "为什么会出现无法下单的情况？"
    search_faq(test_question, top_k=3)

"""
🔎 用户问题: 为什么会出现无法下单的情况？
📊 召回 3 条结果

--- Top 1 ---
相似度分数: 0.114289164543
Q: 为什么会出现无法下单的情况？
A: 无法下单有很多情况，可能是菜品售完、餐厅不在营业时间等，请查看无法下单时给的提示。
来源: https://waimai.meituan.com/help/faq
类别: 支付问题
时间: 2025-09-04T02:38:28.261319+00:00

--- Top 2 ---
相似度分数: 0.13062286377
Q: 刚下单发现信息填错了怎么办？
A: 如果商家尚未接单，您可以自主取消订单；如果商家已经接单，您可以电话联系商家后由对方取消订单。然后重新下一单。
来源: https://waimai.meituan.com/help/faq
类别: 支付问题
时间: 2025-09-04T02:38:28.261319+00:00

--- Top 3 ---
相似度分数: 0.138350009918
Q: 为什么提示下单次数过多，已无法下单？
A: 同一手机号在同一设备上一天最多可以成功提交7次订单（在线支付以完成支付为准，货到付款以提交订单为准）。
其他问题
来源: https://waimai.meituan.com/help/faq
类别: 支付问题
时间: 2025-09-04T02:38:28.261319+00:00
"""