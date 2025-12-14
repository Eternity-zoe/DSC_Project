from PySide6.QtCore import QTimer
from dsl.binary_tree.binary_tree_dsl_ast import *

class BinaryTreeDSLExecutor:

    def __init__(self, window):
        self.window = window
        self.cmds = []
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)

    def execute(self, cmds):
        self.cmds = cmds
        self.index = 0

        # 一次执行 = 清空 → 重建
        self.window.tree.root = None
        self.window.draw_tree(None)

        self.timer.start(700)

    def _step(self):
        if self.index >= len(self.cmds):
            self.timer.stop()
            return

        cmd = self.cmds[self.index]
        self.index += 1
        w = self.window

        if isinstance(cmd, ClearCmd):
            w.tree.root = None
            w.draw_tree(None)

        elif isinstance(cmd, BuildRandomCmd):
            w.tree.build_random(cmd.n, cmd.complete)

        elif isinstance(cmd, InsertCmd):
            w.tree.insert(cmd.value)

        elif isinstance(cmd, TraverseCmd):
            w.traverse(cmd.mode.replace("order", ""))

        elif isinstance(cmd, DrawCmd):
            w.draw_tree(w.tree.root)
