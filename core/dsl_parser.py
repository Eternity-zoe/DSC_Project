import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum

# ======================== 核心数据结构定义 ========================
class StructureType(Enum):
    ARRAY = "array"
    SINGLY_LIST = "singly_list"
    DOUBLY_LIST = "doubly_list"
    STACK = "stack"
    QUEUE = "queue"
    BST = "bst"
    AVL = "avl"
    HEAP = "heap"
    DIRECTED_GRAPH = "directed_graph"
    UNDIRECTED_GRAPH = "undirected_graph"
    HASH = "hash"

class CommandType(Enum):
    INSERT = "insert"
    DELETE = "delete"
    UPDATE = "update"
    SEARCH = "search"
    TRAVERSE = "traverse"
    CLEAR = "clear"

@dataclass
class DSLNode:
    """DSL节点数据结构"""
    id: str
    fields: Dict[str, Any] = field(default_factory=dict)
    links: List[str] = field(default_factory=list)  # 链接的节点ID列表

@dataclass
class StructureDeclaration:
    """声明式结构定义"""
    name: str
    type: StructureType
    nodes: Dict[str, DSLNode] = field(default_factory=dict)
    edges: List[Dict[str, Any]] = field(default_factory=list)  # 仅图使用
    props: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Command:
    """命令式操作定义"""
    struct_name: str
    type: CommandType
    params: Dict[str, Any] = field(default_factory=dict)

# ======================== 解析器实现 ========================
class DSLParseError(Exception):
    """DSL解析异常"""
    pass

class DSLParser:
    def __init__(self):
        # 解析上下文：存储已声明的结构
        self.context: Dict[str, StructureDeclaration] = {}
        
        # 正则表达式模板
        self.regex_patterns = {
            # 结构声明匹配
            "structure_decl": re.compile(
                r"(?P<struct_type>(singly|doubly)\s+)?(array|list|stack|queue|bst|avl|heap|directed|undirected)\s+(graph|hash)?\s+(?P<name>\w+)\s*\{(?P<body>[\s\S]*?)\}",
                re.IGNORECASE
            ),
            # 节点定义匹配
            "node_decl": re.compile(
                r"node\s+(?P<id>\w+)\s*\{(?P<fields>[\s\S]*?)(link\s+to\s+(?P<links>[\w,\s]+?))?\s*\}",
                re.IGNORECASE
            ),
            # 属性定义匹配
            "prop_decl": re.compile(
                r"prop\s+(?P<key>\w+)\s*=\s*(?P<value>[\w\.\"']+?)\s*;",
                re.IGNORECASE
            ),
            # 边定义匹配（仅图）
            "edge_decl": re.compile(
                r"edge\s+(?P<from>\w+)\s*->\s*(?P<to>\w+)\s*(weight\s*=\s*(?P<weight>[\d\.]+))?\s*;",
                re.IGNORECASE
            ),
            # 命令匹配
            "command": re.compile(
                r"(?P<struct>\w+)\.(?P<action>\w+)\s*\((?P<params>[\s\S]*?)\)\s*;",
                re.IGNORECASE
            ),
            # 参数解析
            "param": re.compile(
                r"(?P<key>\w+)\s*=\s*(?P<value>[\w\.\"']+?)(?=,|$)",
                re.IGNORECASE
            ),
            # 字段解析
            "field": re.compile(
                r"(?P<type>int|string|float|bool)\s+(?P<key>\w+)\s*=\s*(?P<value>[\w\.\"']+?)\s*;",
                re.IGNORECASE
            )
        }

    def parse_script(self, dsl_text: str) -> List[Union[StructureDeclaration, Command]]:
        """
        解析完整DSL脚本
        :param dsl_text: DSL文本
        :return: 解析结果列表（混合结构声明和命令）
        """
        # 清空上下文
        self.context.clear()
        results = []
        
        # 预处理：移除注释、多余空白
        cleaned_text = self._preprocess_text(dsl_text)
        
        # 第一步：解析所有结构声明
        struct_matches = self.regex_patterns["structure_decl"].finditer(cleaned_text)
        for match in struct_matches:
            struct_decl = self._parse_structure_declaration(match)
            self.context[struct_decl.name] = struct_decl
            results.append(struct_decl)
        
        # 第二步：解析所有命令
        cmd_matches = self.regex_patterns["command"].finditer(cleaned_text)
        for match in cmd_matches:
            command = self._parse_command(match)
            results.append(command)
        
        return results

    def _preprocess_text(self, text: str) -> str:
        """预处理文本：移除注释、多余空白"""
        # 移除行注释 // ...
        text = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
        # 移除多余空白和换行
        text = re.sub(r"\s+", " ", text)
        # 移除分号前后空白
        text = re.sub(r"\s*;\s*", ";", text)
        return text.strip()

    def _parse_structure_declaration(self, match: re.Match) -> StructureDeclaration:
        """解析单个结构声明"""
        # 提取基础信息
        raw_type = match.group("struct_type") or ""
        struct_subtype = match.group(1) if match.group(1) else ""
        main_type = match.group("graph|hash") or match.group(0).split()[-2]
        name = match.group("name")
        body = match.group("body")
        
        # 确定结构类型
        struct_type = self._resolve_structure_type(raw_type.strip(), main_type.strip())
        
        # 解析节点
        nodes = {}
        node_matches = self.regex_patterns["node_decl"].finditer(body)
        for node_match in node_matches:
            node_id = node_match.group("id")
            fields = self._parse_fields(node_match.group("fields"))
            links = self._parse_links(node_match.group("links"))
            nodes[node_id] = DSLNode(id=node_id, fields=fields, links=links)
        
        # 解析属性
        props = {}
        prop_matches = self.regex_patterns["prop_decl"].finditer(body)
        for prop_match in prop_matches:
            key = prop_match.group("key")
            value = self._parse_value(prop_match.group("value"))
            props[key] = value
        
        # 解析边（仅图结构）
        edges = []
        if struct_type in [StructureType.DIRECTED_GRAPH, StructureType.UNDIRECTED_GRAPH]:
            edge_matches = self.regex_patterns["edge_decl"].finditer(body)
            for edge_match in edge_matches:
                edge = {
                    "from": edge_match.group("from"),
                    "to": edge_match.group("to"),
                    "weight": self._parse_value(edge_match.group("weight") or "1")
                }
                edges.append(edge)
        
        return StructureDeclaration(
            name=name,
            type=struct_type,
            nodes=nodes,
            edges=edges,
            props=props
        )

    def _resolve_structure_type(self, raw_type: str, main_type: str) -> StructureType:
        """解析结构类型枚举"""
        main_type = main_type.lower()
        raw_type = raw_type.lower()
        
        if main_type == "array":
            return StructureType.ARRAY
        elif main_type == "list":
            if "singly" in raw_type:
                return StructureType.SINGLY_LIST
            elif "doubly" in raw_type:
                return StructureType.DOUBLY_LIST
            raise DSLParseError(f"未指定链表类型: {raw_type} list")
        elif main_type == "stack":
            return StructureType.STACK
        elif main_type == "queue":
            return StructureType.QUEUE
        elif main_type == "bst":
            return StructureType.BST
        elif main_type == "avl":
            return StructureType.AVL
        elif main_type == "heap":
            return StructureType.HEAP
        elif main_type == "graph":
            if "directed" in raw_type:
                return StructureType.DIRECTED_GRAPH
            elif "undirected" in raw_type:
                return StructureType.UNDIRECTED_GRAPH
            raise DSLParseError(f"未指定图类型: {raw_type} graph")
        elif main_type == "hash":
            return StructureType.HASH
        else:
            raise DSLParseError(f"不支持的结构类型: {main_type}")

    def _parse_fields(self, fields_text: str) -> Dict[str, Any]:
        """解析节点字段"""
        fields = {}
        field_matches = self.regex_patterns["field"].finditer(fields_text)
        for match in field_matches:
            field_type = match.group("type").lower()
            key = match.group("key")
            value = self._parse_value(match.group("value"), field_type)
            fields[key] = value
        return fields

    def _parse_links(self, links_text: Optional[str]) -> List[str]:
        """解析节点链接"""
        if not links_text:
            return []
        # 分割链接节点ID，去除空白
        links = [link.strip() for link in links_text.split(",") if link.strip()]
        # 处理null值
        return [link if link.lower() != "null" else None for link in links]

    def _parse_value(self, value_str: str, field_type: Optional[str] = None) -> Any:
        """解析值（自动类型转换）"""
        if not value_str:
            return None
        
        value_str = value_str.strip()
        # 处理字符串（引号包裹）
        if (value_str.startswith('"') and value_str.endswith('"')) or (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # 按类型转换
        if field_type == "int" or (not field_type and value_str.isdigit()):
            return int(value_str)
        elif field_type == "float" or (not field_type and re.match(r"^\d+\.\d+$", value_str)):
            return float(value_str)
        elif field_type == "bool" or (not field_type and value_str.lower() in ["true", "false"]):
            return value_str.lower() == "true"
        elif value_str.lower() == "null":
            return None
        
        # 默认返回字符串
        return value_str

    def _parse_command(self, match: re.Match) -> Command:
        """解析单个命令"""
        struct_name = match.group("struct")
        action = match.group("action").lower()
        params_text = match.group("params")
        
        # 校验结构是否已声明
        if struct_name not in self.context:
            raise DSLParseError(f"未声明的结构: {struct_name}")
        
        # 解析命令类型
        try:
            cmd_type = CommandType(action)
        except ValueError:
            raise DSLParseError(f"不支持的命令: {action}")
        
        # 解析命令参数
        params = {}
        if params_text.strip():
            param_matches = self.regex_patterns["param"].finditer(params_text)
            for param_match in param_matches:
                key = param_match.group("key").lower()
                value = self._parse_value(param_match.group("value"))
                params[key] = value
        
        # 校验必要参数
        self._validate_command_params(cmd_type, params)
        
        return Command(
            struct_name=struct_name,
            type=cmd_type,
            params=params
        )

    def _validate_command_params(self, cmd_type: CommandType, params: Dict[str, Any]):
        """校验命令参数"""
        required_params = {
            CommandType.INSERT: ["value"],
            CommandType.DELETE: ["index", "value"],  # 二选一
            CommandType.UPDATE: ["index", "value"],
            CommandType.SEARCH: ["value"],
            CommandType.TRAVERSE: [],  # type为可选
            CommandType.CLEAR: []
        }
        
        # 获取当前命令的必要参数
        req_params = required_params[cmd_type]
        
        if cmd_type == CommandType.DELETE:
            # 删除命令：index或value二选一
            if "index" not in params and "value" not in params:
                raise DSLParseError(f"删除命令需要index或value参数")
        else:
            # 其他命令：检查必要参数
            missing = [p for p in req_params if p not in params]
            if missing:
                raise DSLParseError(f"{cmd_type.value}命令缺少参数: {', '.join(missing)}")

    def get_structure(self, name: str) -> Optional[StructureDeclaration]:
        """从上下文获取已声明的结构"""
        return self.context.get(name)

    def clear_context(self):
        """清空解析上下文"""
        self.context.clear()


# ======================== 测试代码 ========================
if __name__ == "__main__":
    # 测试DSL脚本
    test_dsl = """
// 数组声明
array Scores {
    node arr0 { int value = 95; }
    node arr1 { int value = 88; }
    node arr2 { int value = 92; }
    prop length = 3;
}

// 单链表声明
singly list Students {
    node n0 { int id = 1; string name = "Alice"; link to n1; }
    node n1 { int id = 2; string name = "Bob"; link to n2; }
    node n2 { int id = 3; string name = "Charlie"; link to null; }
    prop head = n0;
}

// 命令操作
Scores.insert(value = 100, index = 3);
Scores.update(index = 0, value = 98);
Students.delete(index = 1);
Students.clear();
"""

    # 初始化解析器并解析
    parser = DSLParser()
    try:
        results = parser.parse_script(test_dsl)
        
        # 打印解析结果
        print("=== 解析结果 ===")
        for item in results:
            if isinstance(item, StructureDeclaration):
                print(f"\n[结构声明] {item.name} ({item.type.value})")
                print(f"  节点数: {len(item.nodes)}")
                print(f"  属性: {item.props}")
            elif isinstance(item, Command):
                print(f"\n[命令] {item.struct_name}.{item.type.value}")
                print(f"  参数: {item.params}")
                
    except DSLParseError as e:
        print(f"解析错误: {e}")