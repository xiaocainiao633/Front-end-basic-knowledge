# RAG-QA 系统（问答增强生成）

本项目基于“检索-增强-生成”(Retrieval-Augmented Generation, RAG) 流程，自动完成：
1. 爬取 FAQ → 2. 清洗存储 → 3. 向量索引 → 4. 相似度召回 → 5. Prompt 组装 → 6. 大模型回答。

## 目录树

```
RAG/
├── playwright.py        # 1️⃣ 网页爬取：批量获取问答对并保存本地
├── text_manage.py       # 2️⃣ 文本治理：清洗、切分、导出 JSON
├── Embedding_model.py   # 3️⃣ 向量索引：创建索引 & 写入 Redis
├── Similarity.py        # 4️⃣ 相似检索：把用户问题转向量并召回 Top-K
├── prompt.py            # 5️⃣ 提示词：根据召回结果生成大模型 prompt
└── llm.py               # 6️⃣ 答案生成：调用大模型并返回最终答案
```

## 文件职责速览

| 文件 | 核心功能 | 输入 | 输出 |
| ---- | -------- | ---- | ---- |
| `playwright.py` | 用 Playwright 驱动浏览器，从目标站点批量抓取“问题-答案”对 | 起始 URL / 选择器 | `raw_qa.jsonl` |
| `text_manage.py` | 去重、去噪、长度截断、统一编码，并切分为标准 JSON 格式 | `raw_qa.jsonl` | `clean_qa.json` |
| `Embedding_model.py` | 调用 DashScope 多模态嵌入模型，创建 RediSearch 向量索引，写入问题向量 | `clean_qa.json` | Redis 索引 `faq_index` |
| `Similarity.py` | 把用户实时问题转向量，在 Redis 做 KNN 搜索，召回最相似 FAQ | 用户问题 | `top_k docs` |
| `prompt.py` | 将召回结果组装成带约束条件的 prompt（禁止幻觉） | 用户问题 + 召回 docs | 最终 prompt 字符串 |
| `llm.py` | 调用通义千问（或其他 LLM）生成答案，支持流式/非流式返回 | prompt | 最终答案 |

## 快速开始

1. 安装依赖
```bash
   pip install -r requirements.txt
```

2.配置环境变量
```
cp .env.example .env
# 编辑 .env 填入 DASHSCOPE_API_KEY 与 Redis 连接信息
```

3.一键跑通示例
```
python playwright.py          # 1. 爬取
python text_manage.py         # 2. 清洗
python Embedding_model.py     # 3. 建索引
python llm.py                 # 4. 直接提问体验端到端效果
```

4.效果演示：每个文件中都有具体示例
