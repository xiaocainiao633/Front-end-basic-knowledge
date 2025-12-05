import os
from datetime import datetime
from langchain_core.documents import Document
from langchain.document_loaders.base import BaseLoader

class SimpleQALoader(BaseLoader):
    """
    简单的问答文件加载器
    
    该加载器用于从文本文件中加载问答对，文件格式要求每两行为一组，
    第一行为问题(Q)，第二行为答案(A)
    
    Args:
        file_path (str): 问答文件的路径
        time_fmt (str): 时间格式字符串，默认为 "%Y-%m-%d %H:%M:%S"
    """

    def __init__(self, file_path: str, time_fmt: str = "%Y-%m-%d %H:%M:%S"):
        self.file_path = file_path
        self.time_fmt = time_fmt

    def load(self):
        """
        加载并解析问答文件
        
        读取文件中的问答对，每两行构成一个问答文档，第一行为问题，第二行为答案。
        每个文档包含问题和答案的组合内容，以及文件的元数据信息。
        
        Returns:
            list[Document]: 包含问答内容的文档列表，每个文档包含page_content和metadata
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        docs = []
        created_ts = os.path.getctime(self.file_path)
        created_at = datetime.fromtimestamp(created_ts).strftime(self.time_fmt)

        # 每两行构成一个 Q/A
        for i in range(0, len(lines), 2):
            q = lines[i].lstrip("Q：:").strip()
            a = lines[i+1].lstrip("A：:").strip()
            page_content = f"Q: {q}\nA: {a}"

            doc = Document(
                page_content=page_content,
                metadata={
                    "source": self.file_path,
                    "created_at": created_at,
                }
            )
            docs.append(doc)

        return docs


# 使用示例
if __name__ == "__main__":
    loader = SimpleQALoader("faq.txt")
    docs = loader.load()
    print(f"共解析到 {len(docs)} 个文档")
    for i, d in enumerate(docs, 1):
        print(f"\n--- 文档 {i} ---")
        print(d.page_content)
        print("元数据：", d.metadata)

# 自定义文本分割器
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import TextSplitter


class CustomTextSplitter(TextSplitter):
    """
    自定义文本分割器类
    
    该类继承自TextSplitter，用于将文本按照特定规则进行分割
    分割策略：首先按段落分割，然后对每个段落提取第一句话
    """

    def split_text(self, text: str) -> List[str]:
        """
        将输入文本分割成多个文本片段
        
        参数:
            text (str): 需要分割的原始文本字符串
            
        返回:
            List[str]: 分割后的文本片段列表，每个片段为段落的第一句话
        """
        text = text.strip()
        # 1.按段落进行分割
        text_array = text.split("\n\n")

        result_texts = []
        for text_item in text_array:
            strip_text_item = text_item.strip()
            if strip_text_item is None:
                continue
            # 2.按句进行分割
            result_texts.append(strip_text_item.split("。")[0])
        return result_texts


# 1.文档加载
loader = TextLoader(file_path="RAG入门.md")
documents = loader.load()
document_text = documents[0].page_content

# 2.定义文本分割器
splitter = CustomTextSplitter()

# 3.文本分割
splitter_texts = splitter.split_text(document_text)
for splitter_text in splitter_texts:
    print(
        f"文本分割片段大小：{len(splitter_text)}, 文本内容：{splitter_text}")

# 向量数据库
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
import dotenv

# 读取env配置
dotenv.load_dotenv()

# 初始化 Embedding 模型
embedding = OllamaEmbeddings(model="deepseek-r1:14b")

# ========== 存储数据 ==========
# 定义待处理的文本数据列表
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]

# 获取文本向量
# 使用embedding模型将文本转换为向量表示
embeddings = embedding.embed_documents(texts)

# 打印结果
# 遍历并打印每个文本及其对应的向量信息
for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i-1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前5个向量值: {vec[:10]}\n")

# 定义每条文本对应的元数据信息
metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]

# 配置Redis连接参数和索引名称
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:6379",
)

# 创建Redis向量存储实例
vector_store = RedisVectorStore(embedding, config=config)

# 将文本和元数据添加到向量存储中
ids = vector_store.add_texts(texts, metadata)

# 打印前5个存储记录的ID
print(ids[0:5])


# 检索
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
import dotenv

# 读取env配置
dotenv.load_dotenv()

# 初始化 Embedding 模型
embedding = OllamaEmbeddings(model="deepseek-r1:14b")

# 配置Redis连接参数和索引名称
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:6379",
)

# 创建Redis向量存储实例
vector_store = RedisVectorStore(embedding, config=config)


# ========== 查询数据 ==========
# 定义查询文本
query = "我喜欢用什么手机"

# 将查询语句向量化，并在Redis中做相似度检索
results = vector_store.similarity_search_with_score(query, k=3)

print("=== 查询结果 ===")
for i, (doc, score) in enumerate(results, 1):
    similarity = 1 - score  #  score 是距离，可以转成相似度
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")
