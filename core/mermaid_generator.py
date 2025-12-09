from typing import List
from .dsl_parser import DataStructure, Node, Field

class MermaidGenerator:
    """将DataStructure转换为Mermaid代码"""
    def __init__(self):
        self.template = {
            "array": self._generate_array,
            "list": self._generate_linked_list,
            "stack": self._generate_stack,
            "queue": self._generate_queue,
            "tree": self._generate_tree,
            "graph": self._generate_graph,
            "hash": self._generate_hash_table
        }

    def generate(self, struct: DataStructure) -> str:
        """生成Mermaid代码"""
        if struct.type not in self.template:
            raise ValueError(f"不支持的数据结构类型：{struct.type}")
        
        mermaid_code = "```mermaid\n"
        mermaid_code += self.template[struct.type](struct)
        mermaid_code += "\n```"
        return mermaid_code

    def _generate_array(self, struct: DataStructure) -> str:
        """生成数组的Mermaid代码（使用subgraph和rect）"""
        length = struct.props.get("length", str(len(struct.nodes)))
        mermaid = f"subgraph {struct.name} [数组: {struct.name} 长度: {length}]\n"
        for i, node in enumerate(struct.nodes):
            field = node.fields[0] if node.fields else Field(name="", type="", value="")
            value = field.value or "null"
            mermaid += f"    {node.name}[{i}: {value}]\n"
        mermaid += "end"
        return mermaid

    def _generate_linked_list(self, struct: DataStructure) -> str:
        """生成链表的Mermaid代码（使用flowchart LR）"""
        mermaid = "flowchart LR\n"
        # 生成节点
        for node in struct.nodes:
            fields_str = " | ".join([f"{f.name}: {f.value or 'null'}" for f in node.fields])
            mermaid += f"    {node.name}[{node.name}:\n{fields_str}]\n"
        # 生成链接
        for node in struct.nodes:
            for link in node.links:
                mermaid += f"    {node.name} --> {link}\n"
        return mermaid

    def _generate_stack(self, struct: DataStructure) -> str:
        """生成栈的Mermaid代码（使用flowchart TD，模拟栈底到栈顶）"""
        top = struct.props.get("top", str(len(struct.nodes)-1))
        mermaid = f"flowchart TD\n"
        mermaid += f"    subgraph {struct.name} [栈: {struct.name} 栈顶: {top}]\n"
        # 栈底在上，栈顶在下
        for i, node in reversed(list(enumerate(struct.nodes))):
            value = node.fields[0].value or "null" if node.fields else "null"
            mermaid += f"        {node.name}[{i}: {value}]\n"
            if i < len(struct.nodes)-1:
                mermaid += f"        {node.name} --> {struct.nodes[i+1].name}\n"
        mermaid += "    end"
        return mermaid

    def _generate_queue(self, struct: DataStructure) -> str:
        """生成队列的Mermaid代码（使用flowchart LR，模拟队首到队尾）"""
        front = struct.props.get("front", "0")
        rear = struct.props.get("rear", str(len(struct.nodes)-1))
        mermaid = f"flowchart LR\n"
        mermaid += f"    subgraph {struct.name} [队列: {struct.name} 队首: {front} 队尾: {rear}]\n"
        for i, node in enumerate(struct.nodes):
            value = node.fields[0].value or "null" if node.fields else "null"
            mermaid += f"        {node.name}[{i}: {value}]\n"
            if i < len(struct.nodes)-1:
                mermaid += f"        {node.name} --> {struct.nodes[i+1].name}\n"
        mermaid += "    end"
        return mermaid

    def _generate_tree(self, struct: DataStructure) -> str:
        """生成树的Mermaid代码（使用flowchart TD，根节点在上）"""
        root = struct.props.get("root", struct.nodes[0].name if struct.nodes else "")
        mermaid = "flowchart TD\n"
        mermaid += f"    subgraph {struct.name} [树: {struct.name} 根: {root}]\n"
        # 生成节点
        for node in struct.nodes:
            fields_str = " | ".join([f"{f.name}: {f.value or 'null'}" for f in node.fields])
            mermaid += f"        {node.name}[{node.name}:\n{fields_str}]\n"
        # 生成父子链接
        for node in struct.nodes:
            for child in node.links:
                mermaid += f"        {node.name} --> {child}\n"
        mermaid += "    end"
        return mermaid

    def _generate_graph(self, struct: DataStructure) -> str:
        """生成图的Mermaid代码（使用graph LR）"""
        directed = struct.props.get("directed", "true").lower() == "true"
        graph_type = "digraph" if directed else "graph"
        mermaid = f"{graph_type} LR\n"
        mermaid += f"    subgraph {struct.name} [图: {struct.name}]\n"
        # 生成节点
        for node in struct.nodes:
            fields_str = " | ".join([f"{f.name}: {f.value or 'null'}" for f in node.fields])
            mermaid += f"        {node.name}[{node.name}:\n{fields_str}]\n"
        # 生成边
        edge_symbol = "->" if directed else "--"
        for node in struct.nodes:
            for neighbor in node.links:
                mermaid += f"        {node.name} {edge_symbol} {neighbor}\n"
        mermaid += "    end"
        return mermaid

    def _generate_hash_table(self, struct: DataStructure) -> str:
        """生成哈希表的Mermaid代码（数组+链表）"""
        size = struct.props.get("size", str(len(struct.nodes)))
        mermaid = f"subgraph {struct.name} [哈希表: {struct.name} 大小: {size}]\n"
        # 生成桶（数组）
        for i, node in enumerate(struct.nodes):
            mermaid += f"    bucket_{i}[桶{i}]\n"
            # 生成桶对应的链表
            if node.links:
                mermaid += f"    bucket_{i} --> {node.name}\n"
                # 链表节点链接
                current = node
                for link in current.links:
                    mermaid += f"    {current.name} --> {link}\n"
                    current = next(n for n in struct.nodes if n.name == link)
        # 生成所有节点定义
        for node in struct.nodes:
            fields_str = " | ".join([f"{f.name}: {f.value or 'null'}" for f in node.fields])
            mermaid += f"    {node.name}[{node.name}:\n{fields_str}]\n"
        mermaid += "end"
        return mermaid