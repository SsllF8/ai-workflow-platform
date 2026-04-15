"""
AI 数据提取节点 - 从文本中提取结构化数据
"""
import os
import json
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_extract")
class AIExtractNode(BaseNode):
    name = "AI 数据提取"
    icon = "📊"
    description = "从文本中提取结构化信息（人名/地名/数字/日期等）"
    config_fields = [
        {"key": "extract_type", "label": "提取类型", "type": "select", "options": [
            "人名和机构", "数字和金额", "时间和日期", "地址和地点", "自定义规则"
        ], "default": "人名和机构"},
        {"key": "custom_rule", "label": "自定义提取规则", "type": "text", "default": ""},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        extract_type = config.get("extract_type", "人名和机构")
        custom_rule = config.get("custom_rule", "")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容可分析")
        
        rules = {
            "人名和机构": "提取文本中所有的人名和机构/公司名称",
            "数字和金额": "提取文本中所有涉及数字、金额、百分比、比例的信息",
            "时间和日期": "提取文本中所有的时间、日期、周期信息",
            "地址和地点": "提取文本中所有的地名、地址、场所信息",
            "自定义规则": f"按以下规则提取信息：{custom_rule}",
        }
        
        prompt = f"""请从以下文本中提取信息。

提取规则：{rules.get(extract_type, rules['人名和机构'])}

要求：
1. 以列表形式输出提取结果
2. 每个提取项注明在原文中的上下文
3. 如果没有找到相关信息，说明"未找到相关信息"

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
                max_tokens=1500,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            return NodeResult(success=True, output=result)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"数据提取失败：{str(e)}")
