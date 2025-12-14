# dsl/binary_tree/binary_tree_dsl_ast.py

class BTCommand: pass

class ClearCmd(BTCommand): pass

class BuildRandomCmd(BTCommand):
    def __init__(self, n, complete=False):
        self.n = n
        self.complete = complete

class InsertCmd(BTCommand):
    def __init__(self, value):
        self.value = value

class TraverseCmd(BTCommand):
    def __init__(self, mode):
        self.mode = mode  # "preorder" | "inorder" | "postorder"

class DrawCmd(BTCommand): pass
