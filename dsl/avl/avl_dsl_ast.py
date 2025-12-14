# dsl/avl/avl_dsl_ast.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Statement:
    """所有语句的基类"""
    pass

@dataclass
class ClearStatement(Statement):
    """清空树语句"""
    pass

@dataclass
class InsertStatement(Statement):
    """插入语句"""
    value: int

@dataclass
class DeleteStatement(Statement):
    """删除语句"""
    value: int

@dataclass
class SearchStatement(Statement):
    """查找语句"""
    value: int

@dataclass
class InorderStatement(Statement):
    """中序遍历语句"""
    pass

@dataclass
class RandomStatement(Statement):
    """随机生成语句"""
    count: int

@dataclass
class PredecessorStatement(Statement):
    """查找前驱语句"""
    value: int

@dataclass
class SuccessorStatement(Statement):
    """查找后继语句"""
    value: int

@dataclass
class LowerBoundStatement(Statement):
    """查找下界语句"""
    value: int

@dataclass
class DelayStatement(Statement):
    """延迟执行语句"""
    milliseconds: int

@dataclass
class Program:
    """程序（语句列表）"""
    statements: List[Statement]