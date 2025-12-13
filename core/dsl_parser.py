# dsl_parser.py
"""
增强版 DSL 解析器（为你的四种树定制）
- 支持结构类型：bst, avl, binary_tree, huffman 等
- 节点 body 解析支持：
    * 字段：int val = 10;
    * 链接：left = n3; right = n7; next = nX; prev = nY;
    * 旧式：link to n1, n2;
- parse_script 返回: List[Union[StructureDeclaration, Command]]
- StructureDeclaration.nodes 是 List[DSLNode]
- DSLNode:
    name: 节点 ID（如 n5）
    fields: List[Field] （Field 有 name 和 value）
    links: List[str] （格式 'left=n3' 或 'right=n7'）
- props: dict (例如 Huffman 的 prop text = "abracadabra")
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum


# -----------------------
# 数据结构与枚举定义
# -----------------------
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
    BINARY_TREE = "binary_tree"
    HUFFMAN = "huffman"


class CommandType(Enum):
    INSERT = "insert"
    DELETE = "delete"
    UPDATE = "update"
    SEARCH = "search"
    TRAVERSE = "traverse"
    CLEAR = "clear"
    BUILD = "build"
    GET_CODES = "get_codes"
    ENCODE = "encode"
    OTHER = "other"


@dataclass
class Field:
    """节点字段：name / value"""
    name: str
    value: Any


@dataclass
class DSLNode:
    """
    统一节点结构（便于 GUI 使用）
    - name: 节点 id，如 'n5'
    - fields: List[Field]，例如 Field('val', 10)
    - links: List[str]，例如 ['left=n3','right=n7']
    """
    name: str
    fields: List[Field] = field(default_factory=list)
    links: List[str] = field(default_factory=list)


@dataclass
class StructureDeclaration:
    """声明式结构定义"""
    name: str
    type: StructureType
    nodes: List[DSLNode] = field(default_factory=list)
    edges: List[Dict[str, Any]] = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Command:
    """命令式操作定义"""
    struct_name: str
    type: CommandType
    params: Dict[str, Any] = field(default_factory=dict)


class DSLParseError(Exception):
    """DSL 解析异常"""
    pass


# -----------------------
# DSLParser 实现
# -----------------------
class DSLParser:
    def __init__(self):
        # 解析上下文：存储已声明的结构（name -> StructureDeclaration）
        self.context: Dict[str, StructureDeclaration] = {}

        self.regex_patterns = {
            # 结构声明匹配：匹配像 "bst MyTree { ... }"、"avl MyAVL { ... }"、"binary_tree MyBin { ... }"
            "structure_decl": re.compile(
                r"(?P<type_word>\w+)\s+(?P<name>\w+)\s*\{(?P<body>[\s\S]*?)\}",
                re.IGNORECASE
            ),
            # 节点声明：node id { body }
            "node_decl": re.compile(
                r"node\s+(?P<id>\w+)\s*\{(?P<body>[\s\S]*?)\}",
                re.IGNORECASE
            ),
            # 属性 prop key = value;
            "prop_decl": re.compile(
                r"prop\s+(?P<key>\w+)\s*=\s*(?P<value>[\s\S]*?)\s*;",
                re.IGNORECASE
            ),
            # 边（图专用） edge a -> b weight = 1;
            "edge_decl": re.compile(
                r"edge\s+(?P<from>\w+)\s*->\s*(?P<to>\w+)\s*(weight\s*=\s*(?P<weight>[\d\.]+))?\s*;",
                re.IGNORECASE
            ),
            # 命令匹配：Name.action(param=val, ...)
            "command": re.compile(
                r"(?P<struct>\w+)\.(?P<action>\w+)\s*\((?P<params>[\s\S]*?)\)\s*;",
                re.IGNORECASE
            ),
            # 参数解析： key = value (逗号分隔)
            "param": re.compile(
                r"(?P<key>\w+)\s*=\s*(?P<value>\"[^\"]*\"|'[^']*'|[^\s,]+)",
                re.IGNORECASE
            ),
            # 字段解析：int val = 10; 或 string name = "Bob";
            "field": re.compile(
                r"(?P<type>int|string|float|bool)\s+(?P<key>\w+)\s*=\s*(?P<value>\"[^\"]*\"|'[^']*'|[^\s;]+)\s*;",
                re.IGNORECASE
            )
        }

    # -----------------------
    # 公共 API
    # -----------------------
    def parse_script(self, dsl_text: str) -> List[Union[StructureDeclaration, Command]]:
        """
        解析完整 DSL 脚本
        返回：结构声明与命令的混合列表（按在文本中出现的顺序出现结构声明，随后命令可被追加）
        """
        # 重置上下文
        self.context.clear()
        results: List[Union[StructureDeclaration, Command]] = []

        # 预处理文本
        cleaned = self._preprocess_text(dsl_text)

        # 第一遍：解析所有结构声明（支持多种结构类型）
        for struct_match in self.regex_patterns["structure_decl"].finditer(cleaned):
            # 需要判断 type_word 是不是我们识别的结构类型（例如 bst, avl, binary_tree, huffman）
            type_word = struct_match.group("type_word").lower()
            name = struct_match.group("name")
            body = struct_match.group("body")

            # 如果 type_word 是 'node' 或其他，跳过（结构声明的正确格式应该是类型名在前）
            # 但我们仍然尝试解析常见别名：binary -> binary_tree, huffman -> huffman
            struct_type = self._map_type_word_to_struct_type(type_word)
            if struct_type is None:
                # 不是结构声明（可能是 node ... 的内部匹配），跳过
                continue

            struct_decl = self._parse_structure_from_body(name, struct_type, body)
            self.context[struct_decl.name] = struct_decl
            results.append(struct_decl)

        # 第二遍：解析命令（command 的匹配依赖于清洗后的文本）
        for cmd_match in self.regex_patterns["command"].finditer(cleaned):
            command = self._parse_command(cmd_match)
            results.append(command)

        return results

    def get_structure(self, name: str) -> Optional[StructureDeclaration]:
        """从上下文获取已声明的结构"""
        return self.context.get(name)

    def clear_context(self):
        self.context.clear()

    # -----------------------
    # 内部解析方法
    # -----------------------
    def _preprocess_text(self, text: str) -> str:
        """预处理：去注释、规范空白、确保语句分号等不破坏结构体大括号内部"""
        # 移除行注释 // ...
        text = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
        # 移除块注释 /* ... */
        text = re.sub(r"/\*[\s\S]*?\*/", "", text, flags=re.MULTILINE)
        # 将连续空白规范为单个空格（但保留换行不会影响 {} 捕获）
        # 为了更稳健地处理，我们只把制表符替换为空格并去掉多余空格
        text = text.replace("\t", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _map_type_word_to_struct_type(self, word: str) -> Optional[StructureType]:
        """把 DSL 中的类型词映射为 StructureType"""
        w = word.lower()
        if w in ("array",):
            return StructureType.ARRAY
        if w in ("singly", "singly_list", "singlylist"):
            return StructureType.SINGLY_LIST
        if w in ("doubly", "doubly_list", "doublylist"):
            return StructureType.DOUBLY_LIST
        if w in ("stack",):
            return StructureType.STACK
        if w in ("queue",):
            return StructureType.QUEUE
        if w in ("bst", "binary_search_tree"):
            return StructureType.BST
        if w in ("avl",):
            return StructureType.AVL
        if w in ("heap",):
            return StructureType.HEAP
        if w in ("directed_graph", "directed", "graph_directed"):
            return StructureType.DIRECTED_GRAPH
        if w in ("undirected_graph", "undirected"):
            return StructureType.UNDIRECTED_GRAPH
        if w in ("hash", "hash_table"):
            return StructureType.HASH
        if w in ("binary_tree", "binary"):
            return StructureType.BINARY_TREE
        if w in ("huffman",):
            return StructureType.HUFFMAN
        # 不支持的类型
        return None

    def _parse_structure_from_body(self, name: str, struct_type: StructureType, body: str) -> StructureDeclaration:
        """解析单个结构的 body：提取 node、prop、edge（若有）"""
        nodes: List[DSLNode] = []
        props: Dict[str, Any] = {}
        edges: List[Dict[str, Any]] = []

        # 解析节点
        for node_match in self.regex_patterns["node_decl"].finditer(body):
            node_id = node_match.group("id")
            node_body = node_match.group("body")
            fields = self._parse_fields(node_body)
            links = self._parse_links_v2(node_body)
            nodes.append(DSLNode(name=node_id, fields=fields, links=links))

        # 解析 props（例如 Huffman 的 prop text = "abracadabra";）
        for prop_match in self.regex_patterns["prop_decl"].finditer(body):
            key = prop_match.group("key").strip()
            raw_val = prop_match.group("value").strip()
            value = self._parse_value(raw_val)
            props[key] = value

        # 解析 edge（仅图类）
        if struct_type in (StructureType.DIRECTED_GRAPH, StructureType.UNDIRECTED_GRAPH):
            for edge_match in self.regex_patterns["edge_decl"].finditer(body):
                edge = {
                    "from": edge_match.group("from"),
                    "to": edge_match.group("to"),
                    "weight": self._parse_value(edge_match.group("weight") or "1")
                }
                edges.append(edge)

        return StructureDeclaration(name=name, type=struct_type, nodes=nodes, edges=edges, props=props)

    def _parse_fields(self, body: str) -> List[Field]:
        """解析字段声明（int/string/float/bool ...）返回 Field 列表"""
        fields: List[Field] = []
        for m in self.regex_patterns["field"].finditer(body):
            ftype = m.group("type").lower()
            key = m.group("key")
            raw_val = m.group("value")
            val = self._parse_value(raw_val, ftype)
            fields.append(Field(name=key, value=val))
        return fields

    def _parse_links_v2(self, body: str) -> List[str]:
        """
        解析链接信息并返回字符串列表，支持：
        - left = n3; right = n7;
        - next = nX; prev = nY;
        - link to n1, n2;  （作为后备）
        返回格式例如： ['left=n3', 'right=n7']
        """
        links: List[str] = []

        # 1) 解析 left/right/next/prev = id;
        p1 = re.compile(r"(left|right|next|prev)\s*=\s*(?P<id>\w+)", re.IGNORECASE)
        for m in p1.finditer(body):
            key = m.group(1).lower()
            target = m.group("id")
            links.append(f"{key}={target}")

        # 2) 解析旧式 "link to n1, n2;"
        p2 = re.compile(r"link\s+to\s+(?P<ids>[\w,\s]+)", re.IGNORECASE)
        for m in p2.finditer(body):
            ids_raw = m.group("ids")
            for id_token in ids_raw.split(","):
                id_token = id_token.strip()
                if id_token:
                    # 将其视为通用链接（没有明确 key），用 'link=n' 形式返回，GUI 如果遇到 link=... 可以兼容处理
                    links.append(f"link={id_token}")

        return links

    def _parse_value(self, raw: str, field_type: Optional[str] = None) -> Any:
        """把 raw 字符串转换为对应类型（int/float/bool/string/null）"""
        if raw is None:
            return None
        s = raw.strip()
        # 去掉末尾分号（如果存在）和两端引号
        if s.endswith(";"):
            s = s[:-1].strip()
        # 字符串（双引号或单引号）
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        # null
        if s.lower() == "null":
            return None
        # 根据 field_type 优先解析
        if field_type == "int":
            try:
                return int(s)
            except:
                raise DSLParseError(f"无法将值解析为 int: {s}")
        if field_type == "float":
            try:
                return float(s)
            except:
                raise DSLParseError(f"无法将值解析为 float: {s}")
        if field_type == "bool":
            if s.lower() in ("true", "false"):
                return s.lower() == "true"
            raise DSLParseError(f"无法将值解析为 bool: {s}")
        # 如果未指定类型，尝试智能解析
        if re.match(r"^-?\d+$", s):
            return int(s)
        if re.match(r"^-?\d+\.\d+$", s):
            return float(s)
        if s.lower() in ("true", "false"):
            return s.lower() == "true"
        # 默认返回字符串（不去引号）
        return s

    def _parse_command(self, match: re.Match) -> Command:
        """解析命令如: Name.insert(value=3);"""
        struct_name = match.group("struct")
        action = match.group("action").lower()
        params_text = match.group("params") or ""

        # 校验命令类型（优雅回退到 OTHER）
        cmd_type = CommandType.OTHER
        try:
            cmd_type = CommandType(action)
        except ValueError:
            # 支持一些扩展命令名（build, get_codes, encode 等）
            if action == "build":
                cmd_type = CommandType.BUILD
            elif action == "get_codes":
                cmd_type = CommandType.GET_CODES
            elif action == "encode":
                cmd_type = CommandType.ENCODE
            else:
                cmd_type = CommandType.OTHER

        # 解析参数对
        params: Dict[str, Any] = {}
        if params_text.strip():
            for pm in self.regex_patterns["param"].finditer(params_text):
                key = pm.group("key").lower()
                raw_val = pm.group("value")
                params[key] = self._parse_value(raw_val)

        # Note: 不在此处强制要求 struct 已声明，因为命令可能在解析顺序中出现在结构声明之后或之前。
        # 具体检查应该在调用端（例如 GUI）去验证 target struct 是否存在。
        return Command(struct_name=struct_name, type=cmd_type, params=params)


# -----------------------
# 简单测试（当作脚本运行时）
# -----------------------
if __name__ == "__main__":
    sample = """
    // BST 声明
    bst MyTree {
        node root { int val = 10; left = n5; right = n15; }
        node n5 { int val = 5; left = n3; right = n7; }
        node n3 { int val = 3; }
        node n7 { int val = 7; }
        node n15 { int val = 15; right = n20; }
        node n20 { int val = 20; }
        prop comment = "sample bst";
    }

    // AVL 示例（命令式、也可声明空结构）
    avl MyAVL {
    }

    // BinaryTree 示例
    binary_tree MyBin {
        node b0 { int val = 1; left = b1; right = b2; }
        node b1 { int val = 2; left = b3; right = b4; }
        node b2 { int val = 3; }
        prop is_complete = true;
    }

    // Huffman 示例
    huffman MyHuff {
        prop text = "abracadabra";
    }

    // 命令式操作
    MyTree.insert(value=6);
    MyTree.delete(value=3);
    MyBin.traverse(type=inorder);
    MyHuff.build();
    MyHuff.get_codes();
    """

    parser = DSLParser()
    try:
        res = parser.parse_script(sample)
        print("Parsed items:", len(res))
        for item in res:
            if isinstance(item, StructureDeclaration):
                print(f"STRUCT: {item.name} type={item.type}")
                print("  nodes:")
                for n in item.nodes:
                    print(f"    - {n.name}: fields={[ (f.name,f.value) for f in n.fields ]} links={n.links}")
                print("  props:", item.props)
            elif isinstance(item, Command):
                print(f"CMD: {item.struct_name}.{item.type} params={item.params}")
    except DSLParseError as e:
        print("Parse error:", e)
