import re
from dataclasses import dataclass
from typing import List, Dict, Union, Optional

@dataclass
class Field:
    """字段定义：名称+类型+值"""
    name: str
    type: str
    value: Optional[Union[str, int, float]] = None

@dataclass
class Node:
    """节点定义：名称+字段列表+关联节点"""
    name: str
    fields: List[Field]
    links: List[str] = None  # 关联的节点名称列表

@dataclass
class DataStructure:
    """数据结构定义：类型+名称+节点列表+属性"""
    type: str  # array/list/stack/queue/tree/graph/hash
    name: str
    nodes: List[Node]
    props: Dict[str, str] = None  # 额外属性（如数组长度、树的根节点）

class DSLParser:
    """DSL解析器：将自定义DSL转换为DataStructure对象"""
    def __init__(self):
        self.structure_pattern = re.compile(r'(\w+)\s+(\w+)\s*\{(.*?)\}', re.DOTALL)
        self.node_pattern = re.compile(r'node\s+(\w+)\s*\{(.*?)\}', re.DOTALL)
        self.field_pattern = re.compile(r'(\w+)\s+(\w+)(?:\s*=\s*([^;]+))?;', re.DOTALL)
        self.link_pattern = re.compile(r'link\s+to\s+(\w+(?:,\s*\w+)*);', re.DOTALL)
        self.prop_pattern = re.compile(r'prop\s+(\w+)\s*=\s*([^;]+);', re.DOTALL)

    def parse(self, dsl_text: str) -> DataStructure:
        """解析DSL文本"""
        # 提取结构类型和名称
        struct_match = self.structure_pattern.match(dsl_text.strip())
        if not struct_match:
            raise SyntaxError("Invalid DSL: 结构定义格式错误")
        
        struct_type, struct_name, content = struct_match.groups()
        nodes = []
        props = {}

        # 提取节点定义
        node_matches = self.node_pattern.findall(content)
        for node_name, node_content in node_matches:
            # 提取字段
            fields = []
            field_matches = self.field_pattern.findall(node_content)
            for field_type, field_name, field_value in field_matches:
                fields.append(Field(
                    name=field_name,
                    type=field_type,
                    value=field_value.strip() if field_value else None
                ))
            
            # 提取关联
            link_matches = self.link_pattern.findall(node_content)
            links = []
            for link_str in link_matches:
                links.extend([link.strip() for link in link_str.split(',')])
            
            nodes.append(Node(name=node_name, fields=fields, links=links))
        
        # 提取属性
        prop_matches = self.prop_pattern.findall(content)
        for prop_name, prop_value in prop_matches:
            props[prop_name] = prop_value.strip()
        
        return DataStructure(
            type=struct_type.lower(),
            name=struct_name,
            nodes=nodes,
            props=props
        )