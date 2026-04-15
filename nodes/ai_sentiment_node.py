"""
AI 情感分析节点
"""
import os
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_sentiment")
class AISentimentNode(BaseNode):
    name = "AI 情感分析"
    icon = "😎"
    description = "分析文本的情感倾向和情绪"
    config_fields = [
        {"key": "detail_level", "label": "分析深度", "type": "select", "options": [
            "简单（正面/负面/中性）", "详细（含情绪分析）"
        ], "default": "简单（正面/负面/中性）"},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        detail_level = config.get("detail_level", "简单（正面/负面/中性）")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容可分析")
        
        if "详细" in detail_level:
            prompt = f"""请对以下文本进行详细的情感分析，包括：

1. 整体情感倾向：正面 / 负面 / 中性
2. 情感强度：0-100分
3. 主要情绪：如喜悦、愤怒、焦虑、期待等
4. 关键情感词：标注文本中表达情感的关键词汇
5. 简短解释

文本：
{input_data}"""
        else:
            prompt = f"""请判断以下文本的情感倾向，输出格式如下：

情感：正面/负面/中性
置信度：高/中/低
一句话解释原因

文本：
{input_data}"""
        
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            return NodeResult(success=True, output=result)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"情感分析失败：{str(e)}")
