# core/sequence_list.py
import copy

class SequenceList:
    """顺序表"""
    def __init__(self):
        self.data = []
        self._listeners = []

    def add_listener(self, cb):
        self._listeners.append(cb)

    def _notify(self, action=None):
        state = {"array": copy.deepcopy(self.data), "action": action}
        for cb in self._listeners:
            cb(state)

    def build(self, items):
        self.data = list(items)
        self._notify({"type": "build", "items": items})

    def insert(self, index, value):
        if index < 0 or index > len(self.data):
            raise IndexError("索引越界")
        self.data.insert(index, value)
        self._notify({"type": "insert", "index": index, "value": value})

    def delete(self, index):
        if index < 0 or index >= len(self.data):
            raise IndexError("索引越界")
        val = self.data.pop(index)
        self._notify({"type": "delete", "index": index, "value": val})
