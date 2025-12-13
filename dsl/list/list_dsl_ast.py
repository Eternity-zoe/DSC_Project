# dsl/list/list_dsl_ast.py

class ListCmd: pass

class ClearCmd(ListCmd): pass

class ModeCmd(ListCmd):
    def __init__(self, mode):
        self.mode = mode  # "singly" | "doubly"

class BuildCmd(ListCmd):
    def __init__(self, values):
        self.values = values

class InsertHeadCmd(ListCmd):
    def __init__(self, value):
        self.value = value

class InsertTailCmd(ListCmd):
    def __init__(self, value):
        self.value = value

class InsertIndexCmd(ListCmd):
    def __init__(self, index, value):
        self.index = index
        self.value = value

class DeleteHeadCmd(ListCmd): pass
class DeleteTailCmd(ListCmd): pass

class DeleteIndexCmd(ListCmd):
    def __init__(self, index):
        self.index = index

class DrawCmd(ListCmd): pass
