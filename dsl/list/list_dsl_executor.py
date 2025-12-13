# dsl/list/list_dsl_executor.py
from PySide6.QtCore import QTimer
from dsl.list.list_dsl_ast import *

class ListDSLExecutor:

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
        self.window._clear_list()
        self.timer.start(600)

    def _step(self):
        if self.index >= len(self.cmds):
            self.timer.stop()
            return

        cmd = self.cmds[self.index]
        self.index += 1

        w = self.window

        if isinstance(cmd, ClearCmd):
            w._clear_list()

        elif isinstance(cmd, ModeCmd):
            w.mode_combo.setCurrentText(
                "单链表" if cmd.mode == "singly" else "双链表"
            )

        elif isinstance(cmd, BuildCmd):
            w.list.clear()
            for v in cmd.values:
                w.list.insert_tail(v)
            w._draw_list()

        elif isinstance(cmd, InsertHeadCmd):
            w._start_animation("insert_head", cmd.value)

        elif isinstance(cmd, InsertTailCmd):
            w._start_animation("insert_tail", cmd.value)

        elif isinstance(cmd, InsertIndexCmd):
            w._start_animation("insert_index", cmd.value, cmd.index)

        elif isinstance(cmd, DeleteHeadCmd):
            w._start_animation("delete_head")

        elif isinstance(cmd, DeleteTailCmd):
            w._start_animation("delete_tail")

        elif isinstance(cmd, DeleteIndexCmd):
            w._start_animation("delete_index", index=cmd.index)

        elif isinstance(cmd, DrawCmd):
            w._draw_list()
