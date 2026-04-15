"""
AI 关键词提取节点
"""
import os
import json
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_keywords")
class AIKeywordsNode(BaseNode):
    name = "关键词提取"
    icon = "🏷️"
    description = "从文本中提取关键词和标签"
    config_fields = [
        {"key": "max_count", "label": "关键词数量", "type": "select", "options": ["5", "10", "15", "20"], "default": "10"},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        max_count = config.get("max_count", "10")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容可分析")
        
        prompt = f"""请从以下文本中提取最多 {max_count} 个关键词/标签。

要求：
1. 关键词要能准确代表文本主题
2. 输出格式为 JSON 数组，如 ["关键词1", "关键词2", "关键词3"]
3. 只输出 JSON 数组，不要其他内容

文本内容：
{input_data}"""
        
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # 尝试解析 JSON
            try:
                # 处理可能被 markdown 代码块包裹的情况
                if "```" in result_text:
                    result_text = result_text.split("```")[1]
                    if result_text.startswith("json"):
                        result_text = result_text[4:]
                keywords = json.loads(result_text.strip())
                if isinstance(keywords, list):
                    formatted = "\n".join([f"  • {kw}" for kw in keywords])
                    return NodeResult(success=True, output=f"提取到 {len(keywords)} 个关键词：\n{formatted}")
            except json.JSONDecodeError:
                pass
            
            # 如果 JSON 解析失败，直接返回原始文本
            return NodeResult(success=True, output=result_text)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"关键词提取失败：{str(e)}")
