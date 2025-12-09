# dsc_drawer/__init__.py（主入口）
from .api import DataStructureDrawer  # 直接导出核心API类
from .core.dsl_parser import DSLParser
from .core.mermaid_generator import MermaidGenerator

# 定义工具包版本
__version__ = "1.0.0"

# 对外暴露的核心接口（用户用的时候直接 from dsc_drawer import XXX）
__all__ = [
    "DataStructureDrawer",  # 最常用的API类（优先暴露）
    "DSLParser",            # 高级用户可能需要的DSL解析器
    "MermaidGenerator"      # 高级用户可能需要的生成器
]