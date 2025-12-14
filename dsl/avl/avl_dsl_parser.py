# dsl/avl/avl_dsl_parser.py
from .avl_dsl_ast import (
    Program, Statement, ClearStatement, InsertStatement, DeleteStatement,
    SearchStatement, InorderStatement, RandomStatement, PredecessorStatement,
    SuccessorStatement, LowerBoundStatement, DelayStatement
)
import re
from typing import List


class ParserError(Exception):
    """解析器错误"""
    def __init__(self, message: str, line: int = -1):
        if line != -1:
            message = f"第{line}行: {message}"
        super().__init__(message)

class AVLDslParser:
    """AVL树DSL解析器"""
    def __init__(self):
        # 正则表达式匹配各种语句
        self.patterns = {
            'clear': re.compile(r'^\s*clear\s*$'),
            'insert': re.compile(r'^\s*insert\s+(\d+)\s*$'),
            'delete': re.compile(r'^\s*delete\s+(\d+)\s*$'),
            'search': re.compile(r'^\s*search\s+(\d+)\s*$'),
            'inorder': re.compile(r'^\s*inorder\s*$'),
            'random': re.compile(r'^\s*random\s+(\d+)\s*$'),
            'predecessor': re.compile(r'^\s*predecessor\s+(\d+)\s*$'),
            'successor': re.compile(r'^\s*successor\s+(\d+)\s*$'),
            'lower_bound': re.compile(r'^\s*lower_bound\s+(\d+)\s*$'),
            'delay': re.compile(r'^\s*delay\s+(\d+)\s*$')
        }

    def parse(self, code: str) -> Program:
        """解析DSL代码为AST"""
        statements: List[Statement] = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            # 尝试匹配各种语句模式
            matched = False
            
            if self.patterns['clear'].match(line):
                statements.append(ClearStatement())
                matched = True
            elif m := self.patterns['insert'].match(line):
                statements.append(InsertStatement(int(m.group(1))))
                matched = True
            elif m := self.patterns['delete'].match(line):
                statements.append(DeleteStatement(int(m.group(1))))
                matched = True
            elif m := self.patterns['search'].match(line):
                statements.append(SearchStatement(int(m.group(1))))
                matched = True
            elif self.patterns['inorder'].match(line):
                statements.append(InorderStatement())
                matched = True
            elif m := self.patterns['random'].match(line):
                count = int(m.group(1))
                if count < 1:
                    raise ParserError("随机生成节点数必须大于0", line_num)
                statements.append(RandomStatement(count))
                matched = True
            elif m := self.patterns['predecessor'].match(line):
                statements.append(PredecessorStatement(int(m.group(1))))
                matched = True
            elif m := self.patterns['successor'].match(line):
                statements.append(SuccessorStatement(int(m.group(1))))
                matched = True
            elif m := self.patterns['lower_bound'].match(line):
                statements.append(LowerBoundStatement(int(m.group(1))))
                matched = True
            elif m := self.patterns['delay'].match(line):
                ms = int(m.group(1))
                if ms < 0:
                    raise ParserError("延迟时间不能为负数", line_num)
                statements.append(DelayStatement(ms))
                matched = True
            
            if not matched:
                raise ParserError(f"无效的语句: {line}", line_num)
        
        return Program(statements)