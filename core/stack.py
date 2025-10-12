# core/stack.py
import copy

class Stack:
    """顺序栈"""
    def __init__(self):
        self.data = []
        self._listeners = []

    def add_listener(self, cb):
        self._listeners.append(cb)

    def _notify(self, action=None):
        state = {"array": copy.deepcopy(self.data), "action": action}
        for cb in self._listeners:
            cb(state)

    def push(self, value):
        self.data.append(value)
        self._notify({"type": "push", "value": value})

    def pop(self):
        if not self.data:
            raise IndexError("空栈")
        val = self.data.pop()
        self._notify({"type": "pop", "value": val})
