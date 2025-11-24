from playwright.sync_api import sync_playwright

def collect_faq(url):
    """
    收集指定URL页面中的FAQ内容

    参数：
        url(str): 目标网页URL网址
    
    返回：
        str: 提取的FAQ内容
    """
    # 启动playwright浏览器自动化工具
    with sync_playwright() as p:
        # 启动Chrome浏览器，设置为非无头模式并指定中文语言
        browser = p.chromium.lanuch(
            headless = False, # 非无头模式,可视化浏览器操作
            args = ['--lang=zh-CN'] # 浏览器语言设置为中文
        )
        # 创建新页面，配置中文环境
        page = browser.new_page(
            locale = 'zh-CN', # 页面语言环境设置为中文
            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
            ), # 模拟常见浏览器的用户代理
            extra_http_headers = {
                "Accept-Language": "zh-CN,zh;q=0.9"
            } # 设置HTTP请求头中的语言偏好
        )
        # 访问目标URL并等待页面加载完成
        page.goto(url, timeout=30_000)
        page.wait_for_load_state("networkidle") # 等待网络空闲，确保页面加载完成

        # 提取FAQ列表区域的文本内容
        raw_text = page.locator("#faq-list").first.text_content() # 找到id="faq-list"的元素并获取第一个的文本内容
        # 关闭浏览器
        browser.close()
        return raw_text

# 保存文件
def save_faq(cleaned_text: str, output_file: str):
    """
    将FAQ文本内容保存到指定文件
    
    参数:
        cleaned_text (str): 要保存的FAQ文本内容
        output_file (str): 输出文件路径
    """
    # 写入文件
    with ope(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"FAQ内容已保存到 {output_file}")

if __name__ == "__main__":
    cleaned_text = collect_faq(url="https://waimai.meituan.com/help/faq")
    putput_file = "faq.txt"
    save_faq(cleaned_text, output_file)

"""
# head -n 20 faq.txt           
          在线支付问题
          
        
        
          
            Q：在线支付取消订单后钱怎么返还？
            
              订单取消后，款项会在一个工作日内，直接返还到您的美团账户余额。
            
          
        
        
          
            Q：怎么查看退款是否成功？
            
              退款会在一个工作日之内到美团账户余额，可在“账号管理——我的账号”中查看是否到账
"""