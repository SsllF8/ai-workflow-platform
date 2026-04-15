"""
AI 摘要总结节点
"""
import os
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_summary")
class AISummaryNode(BaseNode):
    name = "AI 摘要总结"
    icon = "📋"
    description = "使用 AI 生成文本摘要"
    config_fields = [
        {"key": "style", "label": "摘要风格", "type": "select", "options": [
            "简洁摘要（3-5句话）", "要点列表", "详细摘要", "一句话总结"
        ], "default": "简洁摘要（3-5句话）"},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        style = config.get("style", "简洁摘要（3-5句话）")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容可总结")
        
        style_prompts = {
            "简洁摘要（3-5句话）": "请用3-5句话概括以下内容的核心要点：",
            "要点列表": "请用要点列表的形式总结以下内容，每个要点一行：",
            "详细摘要": "请详细总结以下内容，保留重要细节：",
            "一句话总结": "请用一句话概括以下内容的核心含义：",
        }
        
        prompt = f"{style_prompts.get(style, style_prompts['简洁摘要（3-5句话）'])}\n\n{input_data}"
        
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.5
            )
            
            result = response.choices[0].message.content.strip()
            return NodeResult(success=True, output=result)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"AI 总结失败：{str(e)}")
