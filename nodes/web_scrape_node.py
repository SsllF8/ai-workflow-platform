"""
网页抓取节点
"""
import requests
from bs4 import BeautifulSoup
from nodes import BaseNode, NodeResult, register_node


@register_node("web_scrape")
class WebScrapeNode(BaseNode):
    name = "网页抓取"
    icon = "🌐"
    description = "抓取网页正文内容"
    config_fields = [
        {"key": "url", "label": "网页URL", "type": "text", "default": "https://"}
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        url = config.get("url", "").strip()
        if not url:
            url = input_data.strip()
        
        if not url or not url.startswith("http"):
            return NodeResult(success=False, output="", error="请输入有效的URL")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # 移除脚本和样式
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            
            # 提取正文
            text = soup.get_text(separator="\n", strip=True)
            
            # 清理空行
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            clean_text = "\n".join(lines[:200])  # 限制长度
            
            if not clean_text:
                return NodeResult(success=False, output="", error="未能提取到网页内容")
            
            return NodeResult(success=True, output=f"[来源: {url}]\n\n{clean_text}")
            
        except requests.exceptions.Timeout:
            return NodeResult(success=False, output="", error="请求超时，请检查URL是否正确")
        except requests.exceptions.ConnectionError:
            return NodeResult(success=False, output="", error="无法连接到该网页")
        except Exception as e:
            return NodeResult(success=False, output="", error=f"抓取失败：{str(e)}")
