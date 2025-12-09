# 补充完整的类型注解导入（关键修复！）
from typing import List, Dict, Optional, Union
from core.dsl_parser import DataStructure, Node, Field
from core.mermaid_generator import MermaidGenerator

class DataStructureDrawer:
    """Python API：直接构建数据结构并生成Mermaid代码"""
    def __init__(self):
        self.generator = MermaidGenerator()

    def create_array(self, name: str, values: List[Union[str, int, float]], length: Optional[int] = None) -> str:
        """创建数组"""
        nodes = []
        for i, val in enumerate(values):
            nodes.append(Node(
                name=f"arr_{i}",
                fields=[Field(name="value", type=type(val).__name__, value=str(val))]
            ))
        struct = DataStructure(
            type="array",
            name=name,
            nodes=nodes,
            props={"length": str(length) if length else str(len(values))}
        )
        return self.generator.generate(struct)

    def create_linked_list(self, name: str, values: List[Union[str, int, float]]) -> str:
        """创建链表"""
        nodes = []
        for i, val in enumerate(values):
            nodes.append(Node(
                name=f"node_{i}",
                fields=[Field(name="value", type=type(val).__name__, value=str(val))],
                links=[f"node_{i+1}"] if i < len(values)-1 else []
            ))
        struct = DataStructure(type="list", name=name, nodes=nodes)
        return self.generator.generate(struct)

    def create_tree(self, name: str, root: str, children_map: Dict[str, List[str]], node_values: Dict[str, Union[str, int, float]]) -> str:
        """创建树（children_map：父节点->子节点列表；node_values：节点->值）"""
        nodes = []
        for node_name in children_map.keys():
            nodes.append(Node(
                name=node_name,
                fields=[Field(name="value", type=type(node_values[node_name]).__name__, value=str(node_values[node_name]))],
                links=children_map[node_name]
            ))
        struct = DataStructure(
            type="tree",
            name=name,
            nodes=nodes,
            props={"root": root}
        )
        return self.generator.generate(struct)

    def from_dsl(self, dsl_text: str) -> str:
        """从DSL文本生成Mermaid代码"""
        from core.dsl_parser import DSLParser
        parser = DSLParser()
        struct = parser.parse(dsl_text)
        return self.generator.generate(struct)