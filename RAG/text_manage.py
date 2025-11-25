# 文档处理：文本清洗、分段切分、原数据标注等
import re
import json
from pathlib import Path
from datatime import datetime, timezone

def clean_text(text: str) -> str:
    """
    清洗文本内容，去除HTML标签和多余空格及无效字符。

    参数:
        text (str): 需要清洗的原始文本。

    返回:
        str: 清洗后的文本内容。
    """
    # 去掉 HTML 标签（如果有残留）
    text = re.sub(r"<.*?>", "", text)
    # 去掉多余空格并过滤空行
    lines = [line.strip() for line in text.aplitlines() if lines.strip()]
    return "\n".join(lines)


def split_faq(text: str):
    """
    根据 Q/A 规则将FAQ文本切分为问题和答案对。

    参数：
        text(str): 包含FAQ内容的文本字符串
    
    返回：
        list[dict]: 每个元素是一个包含'question'和'answer'键的字典列表
    """
    # 按Q:  或Q: 分割文本
    parts = re.split(r"(?:^|\n)Q[:：]", text) # 找到Q开头的地方
    # 切完后 parts 大概长这样：['', '问题1\n答案1\n\n', '问题2\n答案2\n\n', '问题3\n答案3']
    qa_pairs = [] # 装结果列表
    for part in parts:
        part = part.strip() # 去掉首尾空白、换行
        if not part:
            continue
        # 将第一行当问题，其余部分作为答案
        lines = part.splitlines() # 按行切，返回列表
        question = lines[0] # 固定当问题
        answer = "\n".join(lines[1:]) if len(lines) > 1 else "" # 答案
        qa_pairs.append({
            "question": question,
            "answer": answer
        }) # 装进列表
        return qa_pairs

def process_faq(input_file: str, output_file: str, source_url: str, category="FAQ"):
    """
    处理FAQ文本文件，清洗、分割并添加元数据后保存为JSON格式。

    参数:
        input_file (str): 输入的原始FAQ文本文件路径。
        output_file (str): 输出处理后的JSON文件路径。
        source_url (str): 数据来源URL。
        category (str): FAQ分类，默认为"FAQ"。

    返回:
        None
    """
    # 读文件读成str,清洗拆分
    raw_text = Path(input_file).read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)
    qa_pairs = split_faq(cleaned_text)
    # 生成UTC时间戳
    now = datetime.now(timezone.utc).isoformat()

    # 给每条问答挂元数据
    processed = []
    for qa in qa_pairs:
        processed.append({
            "question": qa["question"],
            "answer": qa["answer"],
            "metadata": {
                "source": source_url,
                "category": category,
                "crawl_time": now
            }
        })
    # 写JSON文件
    Path(output_file).write_text(
        # Python对象->JSON字符串，缩进两个空格
        json.dumps(processed, ensure_ascii = False, indent = 2),
        encoding = "utf-8"
    )
    print(f"✅ 已处理 {len(processed)} 条 FAQ，结果保存到 {output_file}")

if __name__ == "__main__":
    process_faq(
        imput_file = "faq_text",
        output_file = "faq_processed.json",
        source_url = "https://waimai.meituan.com/help/faq",
        category = "支付问题"
    )

"""
# head -n 20 faq_processed.json
[
  {
    "question": "在线支付问题",
    "answer": "",
    "metadata": {
      "source": "https://waimai.meituan.com/help/faq",
      "category": "支付问题",
      "crawl_time": "2025-09-04T02:38:28.261319+00:00"
    }
  },
  {
    "question": "在线支付取消订单后钱怎么返还？",
    "answer": "订单取消后，款项会在一个工作日内，直接返还到您的美团账户余额。",
    "metadata": {
      "source": "https://waimai.meituan.com/help/faq",
      "category": "支付问题",
      "crawl_time": "2025-09-04T02:38:28.261319+00:00"
    }
  },
  {
"""