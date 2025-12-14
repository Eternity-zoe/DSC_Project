# dsl/bst/bst_dsl_ast.py
class BSTCmd:
    """BST DSL命令基类"""
    pass

class ClearCmd(BSTCmd):
    """清空命令"""
    pass

class BuildCmd(BSTCmd):
    """构建BST命令"""
    def __init__(self, values):
        self.values = values

class InsertCmd(BSTCmd):
    """插入命令"""
    def __init__(self, value):
        self.value = value

class SearchCmd(BSTCmd):
    """查找命令"""
    def __init__(self, value):
        self.value = value

class DeleteCmd(BSTCmd):
    """删除命令"""
    def __init__(self, value):
        self.value = value

class FindPredecessorCmd(BSTCmd):
    """查找前驱命令"""
    def __init__(self, value):
        self.value = value

class FindSuccessorCmd(BSTCmd):
    """查找后继命令"""
    def __init__(self, value):
        self.value = value

class FindLowerBoundCmd(BSTCmd):
    """查找下界命令"""
    def __init__(self, value):
        self.value = value

class InorderCmd(BSTCmd):
    """中序遍历命令"""
    pass

class DrawCmd(BSTCmd):
    """绘制命令"""
    pass