"""
文本输入节点
"""
from nodes import BaseNode, NodeResult, register_node


@register_node("text_input")
class TextInputNode(BaseNode):
    name = "文本输入"
    icon = "📝"
    description = "输入一段文本作为工作流的起始"
    config_fields = [
        {"key": "text", "label": "输入内容", "type": "text", "default": ""}
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        text = config.get("text", "")
        if not text:
            text = input_data
        return NodeResult(success=True, output=text.strip())
