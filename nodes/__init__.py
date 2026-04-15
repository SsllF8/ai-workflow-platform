"""
节点基类和注册中心
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class NodeResult:
    """节点执行结果"""
    success: bool
    output: str
    error: str = ""


class BaseNode:
    """所有节点的基类"""
    
    name: str = "基础节点"
    icon: str = "📦"
    description: str = ""
    config_fields: list = []  # 配置字段定义 [{"key": "xxx", "label": "xxx", "type": "text/select", "options": [...]}]
    
    def execute(self, input_data: str, config: dict) -> NodeResult:
        """
        执行节点逻辑
        input_data: 上一个节点的输出
        config: 用户配置的参数
        """
        raise NotImplementedError


# 节点注册中心
NODE_REGISTRY: dict[str, type[BaseNode]] = {}

def register_node(node_type: str):
    """节点注册装饰器"""
    def decorator(cls):
        NODE_REGISTRY[node_type] = cls
        return cls
    return decorator
