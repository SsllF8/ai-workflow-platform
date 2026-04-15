"""
AI 文本生成节点 - 翻译/润色/改写/自定义任务
"""
import os
from openai import OpenAI
from nodes import BaseNode, NodeResult, register_node


@register_node("ai_text")
class AITextNode(BaseNode):
    name = "AI 文本处理"
    icon = "🤖"
    description = "使用 AI 处理文本（翻译/润色/改写/自定义）"
    config_fields = [
        {"key": "task_type", "label": "处理类型", "type": "select", "options": [
            "翻译成英文", "翻译成中文", "润色优化", "改写简化", "正式化改写", "扩写", "自定义任务"
        ], "default": "翻译成英文"},
        {"key": "custom_prompt", "label": "自定义指令", "type": "text", "default": ""},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        task_type = config.get("task_type", "翻译成英文")
        custom_prompt = config.get("custom_prompt", "")
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有输入内容可处理")
        
        # 根据任务类型构造 prompt
        task_prompts = {
            "翻译成英文": f"请将以下文本翻译成英文，只输出翻译结果，不要解释：\n\n{input_data}",
            "翻译成中文": f"请将以下文本翻译成中文，只输出翻译结果，不要解释：\n\n{input_data}",
            "润色优化": f"请润色优化以下文本，使其更通顺流畅、表达更清晰，只输出优化后的文本：\n\n{input_data}",
            "改写简化": f"请用更简洁的语言改写以下文本，保留核心含义，只输出改写结果：\n\n{input_data}",
            "正式化改写": f"请将以下文本改写为正式商务语气，只输出改写结果：\n\n{input_data}",
            "扩写": f"请对以下内容进行合理扩写，增加细节和深度，只输出扩写结果：\n\n{input_data}",
            "自定义任务": f"{custom_prompt}\n\n以下是需要处理的文本：\n{input_data}",
        }
        
        prompt = task_prompts.get(task_type, task_prompts["翻译成英文"])
        
        try:
            client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            return NodeResult(success=True, output=result)
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"AI 处理失败：{str(e)}")
