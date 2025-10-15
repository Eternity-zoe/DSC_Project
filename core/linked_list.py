# core/linked_list.py
import copy

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    """单链表"""
    def __init__(self):
        self.head = None
        self._listeners = []

    def add_listener(self, cb):
        self._listeners.append(cb)

    def _notify(self, action=None):
        nodes = []
        cur = self.head
        while cur:#遍历
            nodes.append(cur.val)
            cur = cur.next
        state = {"array": nodes, "action": action}
        for cb in self._listeners:
            cb(state)

    def build(self, items):
        self.head = None
        tail = None
        for val in items:
            node = Node(val)
            if self.head is None:
                self.head = node
            else:
                tail.next = node
            tail = node#更新尾结点
        self._notify({"type": "build", "items": items})

    def insert(self, index, value):
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(index - 1):
                if prev is None:
                    raise IndexError("索引越界")
                prev = prev.next
            if prev is None:
                raise IndexError("索引越界")
            new_node.next = prev.next
            prev.next = new_node
        self._notify({"type": "insert", "index": index, "value": value})

    def delete(self, index):
        if self.head is None:
            raise IndexError("空链表")
        if index == 0:
            val = self.head.val
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index - 1):
                if prev.next is None:
                    raise IndexError("索引越界")
                prev = prev.next
            if prev.next is None:
                raise IndexError("索引越界")
            val = prev.next.val
            prev.next = prev.next.next
        self._notify({"type": "delete", "index": index, "value": val})
