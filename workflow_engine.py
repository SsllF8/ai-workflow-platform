"""
工作流引擎 - 负责解析和执行工作流
"""
import time
from typing import Any
from nodes import NodeResult, NODE_REGISTRY


class WorkflowEngine:
    """工作流执行引擎"""
    
    def __init__(self):
        self.nodes = []  # 有序的节点列表
        self.logs = []   # 执行日志
    
    def add_node(self, node_config: dict):
        """
        添加节点到工作流
        node_config: {"type": "ai_text", "config": {"prompt": "..."}} 
        """
        self.nodes.append(node_config)
    
    def remove_node(self, index: int):
        """移除指定位置的节点"""
        if 0 <= index < len(self.nodes):
            self.nodes.pop(index)
    
    def clear(self):
        """清空工作流"""
        self.nodes = []
        self.logs = []
    
    def run(self, initial_input: str = "") -> dict:
        """
        执行工作流
        返回: {"success": bool, "output": str, "logs": list, "node_results": list}
        """
        self.logs = []
        node_results = []
        current_data = initial_input
        success = True
        
        for i, node_config in enumerate(self.nodes):
            node_type = node_config.get("type")
            config = node_config.get("config", {})
            
            # 查找节点类
            node_class = NODE_REGISTRY.get(node_type)
            if not node_class:
                self.logs.append(f"[节点 {i+1}] 错误：未知节点类型 '{node_type}'")
                success = False
                break
            
            node = node_class()
            self.logs.append(f"[节点 {i+1}] {node.name} - 开始执行...")
            start_time = time.time()
            
            try:
                result: NodeResult = node.execute(current_data, config)
                elapsed = time.time() - start_time
                
                if result.success:
                    self.logs.append(f"[节点 {i+1}] 完成 ({elapsed:.1f}s)")
                    node_results.append({
                        "index": i + 1,
                        "name": node.name,
                        "icon": node.icon,
                        "success": True,
                        "elapsed": f"{elapsed:.1f}s",
                        "output_preview": result.output[:200] + "..." if len(result.output) > 200 else result.output
                    })
                    current_data = result.output  # 传递给下一个节点
                else:
                    self.logs.append(f"[节点 {i+1}] 失败：{result.error}")
                    node_results.append({
                        "index": i + 1,
                        "name": node.name,
                        "icon": node.icon,
                        "success": False,
                        "elapsed": f"{elapsed:.1f}s",
                        "error": result.error
                    })
                    success = False
                    break
                    
            except Exception as e:
                elapsed = time.time() - start_time
                self.logs.append(f"[节点 {i+1}] 异常：{str(e)}")
                node_results.append({
                    "index": i + 1,
                    "name": node.name,
                    "icon": node.icon,
                    "success": False,
                    "elapsed": f"{elapsed:.1f}s",
                    "error": str(e)
                })
                success = False
                break
        
        return {
            "success": success,
            "output": current_data,
            "logs": self.logs,
            "node_results": node_results
        }
    
    def get_node_names(self) -> list:
        """获取当前工作流中的节点信息"""
        names = []
        for i, node_config in enumerate(self.nodes):
            node_type = node_config.get("type")
            node_class = NODE_REGISTRY.get(node_type)
            if node_class:
                node = node_class()
                names.append({"index": i, "name": node.name, "icon": node.icon, "type": node_type})
        return names
