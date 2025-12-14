# dsl/bst/bst_dsl_parser.py
import re
from dsl.bst.bst_dsl_ast import *

class BSTDSLParser:
    """BST DSL解析器"""
    
    def parse(self, script: str):
        """解析整个脚本"""
        cmds = []
        for lineno, raw_line in enumerate(script.splitlines(), start=1):
            line = raw_line.strip()
            # 跳过空行和注释
            if not line or line.startswith("//"):
                continue
            # 检查分号结尾
            if not line.endswith(";"):
                raise SyntaxError(f"第{lineno}行缺少分号")
            # 移除分号
            line = line[:-1].strip()
            try:
                cmd = self._parse_line(line)
                cmds.append(cmd)
            except Exception as e:
                raise SyntaxError(f"第{lineno}行: {str(e)}")
        return cmds
    
    def _parse_line(self, line: str):
        """解析单行命令"""
        if line == "clear":
            return ClearCmd()
            
        if line.startswith("build"):
            m = re.search(r"\[(.*)\]", line)
            if not m:
                raise SyntaxError("build语法错误，正确格式: build [1,2,3]")
            values = [int(x.strip()) for x in m.group(1).split(",") if x.strip()]
            return BuildCmd(values)
            
        if line.startswith("insert"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("insert语法错误，正确格式: insert 5")
            return InsertCmd(int(parts[1]))
            
        if line.startswith("search"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("search语法错误，正确格式: search 5")
            return SearchCmd(int(parts[1]))
            
        if line.startswith("delete"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("delete语法错误，正确格式: delete 5")
            return DeleteCmd(int(parts[1]))
            
        if line.startswith("find_predecessor"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("find_predecessor语法错误，正确格式: find_predecessor 5")
            return FindPredecessorCmd(int(parts[1]))
            
        if line.startswith("find_successor"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("find_successor语法错误，正确格式: find_successor 5")
            return FindSuccessorCmd(int(parts[1]))
            
        if line.startswith("find_lower_bound"):
            parts = line.split()
            if len(parts) != 2:
                raise SyntaxError("find_lower_bound语法错误，正确格式: find_lower_bound 5")
            return FindLowerBoundCmd(int(parts[1]))
            
        if line == "inorder":
            return InorderCmd()
            
        if line == "draw":
            return DrawCmd()
            
        raise SyntaxError(f"无法识别的命令: {line}")