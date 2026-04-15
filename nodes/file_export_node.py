"""
文件导出节点
"""
import os
import json
from datetime import datetime
from nodes import BaseNode, NodeResult, register_node


@register_node("file_export")
class FileExportNode(BaseNode):
    name = "导出文件"
    icon = "📤"
    description = "将结果保存为 TXT 或 JSON 文件"
    config_fields = [
        {"key": "format", "label": "文件格式", "type": "select", "options": ["TXT", "JSON"], "default": "TXT"},
        {"key": "filename", "label": "文件名（可选）", "type": "text", "default": ""},
    ]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        file_format = config.get("format", "TXT")
        filename = config.get("filename", "").strip()
        
        if not input_data or not input_data.strip():
            return NodeResult(success=False, output="", error="没有内容可导出")
        
        # 确保输出目录存在
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workflow_output_{timestamp}"
        
        try:
            if file_format == "JSON":
                filepath = os.path.join(output_dir, f"{filename}.json")
                # 尝试将文本解析为 JSON
                try:
                    data = json.loads(input_data)
                except json.JSONDecodeError:
                    data = {"content": input_data}
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                filepath = os.path.join(output_dir, f"{filename}.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(input_data)
            
            return NodeResult(
                success=True, 
                output=f"文件已保存：{filepath}\n\n{input_data}"
            )
            
        except Exception as e:
            return NodeResult(success=False, output="", error=f"导出失败：{str(e)}")
