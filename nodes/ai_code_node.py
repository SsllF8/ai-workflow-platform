"""
AI 代码解释/生成节点
"""
import os
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_code")
class AICodeNode(BaseNode):
    name = "AI 代码助手"
    icon = "💻"
    description = "让 AI 解释代码、生成代码或做代码审查"
    config_fields = [
        {"key": "code_task", "label": "代码任务", "type": "select", "options": [
            "解释代码", "生成代码", "代码审查", "添加注释", "优化代码"
        ], "default": "解释代码"},
        {"key": "language", "label": "编程语言", "type": "select", "options": [
            "Python", "JavaScript", "Java", "SQL", "自动检测"
        ], "default": "Python"},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        code_task = config.get("code_task", "解释代码")
        language = config.get("language", "Python")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容")
        
        task_prompts = {
            "解释代码": f"请用中文详细解释以下 {language} 代码的功能和逻辑：\n\n```\n{input_data}\n```",
            "生成代码": f"请根据以下需求生成 {language} 代码，附带简要注释：\n\n{input_data}",
            "代码审查": f"请审查以下 {language} 代码，指出潜在问题和改进建议：\n\n```\n{input_data}\n```",
            "添加注释": f"请为以下 {language} 代码添加详细的中文注释：\n\n```\n{input_data}\n```",
            "优化代码": f"请优化以下 {language} 代码，提升性能和可读性，并说明修改原因：\n\n```\n{input_data}\n```",
        }
        
        prompt = task_prompts.get(code_task, task_prompts["解释代码"])
        
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            return NodeResult(success=True, output=result)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"AI 代码处理失败：{str(e)}")
