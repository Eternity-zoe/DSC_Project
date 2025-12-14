# dsl/stack/stack_dsl_executor.py

from PySide6.QtCore import QTimer
import random

class StackDSLExecutor:
    def __init__(self, window):
        self.win = window
        self.cmds = []
        self.pc = 0

    def load(self, cmds):
        self.cmds = cmds
        self.pc = 0

        # 每次 DSL 执行 = 清空
        self.win._clear_stack()

    def step(self):
        if self.pc >= len(self.cmds):
            self.win.status_bar.showMessage("DSL 执行完成")
            return

        cmd = self.cmds[self.pc]
        self.pc += 1
        self.execute(cmd)

    def execute(self, cmd):
        op = cmd[0]

        if op == "stack":
            self.win.status_bar.showMessage(f"DSL: 栈 {cmd[1]}")
            QTimer.singleShot(300, self.step)

        elif op == "push":
            self.win._start_animation("push", cmd[1])
            self._wait_anim()

        elif op == "pop":
            self.win._start_animation("pop")
            self._wait_anim()

        elif op == "peek":
            self.win._peek()
            QTimer.singleShot(500, self.step)

        elif op == "clear":
            self.win._clear_stack()
            QTimer.singleShot(300, self.step)

        elif op == "random":
            self.win._clear_stack()
            for _ in range(cmd[1]):
                self.win.stack.push(
                    random.randint(self.win.stack.MIN_VAL, self.win.stack.MAX_VAL)
                )
            self.win._draw_stack()
            QTimer.singleShot(500, self.step)

        elif op == "sleep":
            QTimer.singleShot(cmd[1], self.step)

        elif op == "end":
            self.win.status_bar.showMessage("DSL 结束")

    def _wait_anim(self):
        def check():
            if not self.win.anim_timer.isActive():
                self.win.anim_timer.timeout.disconnect(check)
                self.step()
        self.win.anim_timer.timeout.connect(check)
