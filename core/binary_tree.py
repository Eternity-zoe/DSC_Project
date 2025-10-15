# core/binary_tree.py
import random
from collections import deque

class TreeNode:
    def __init__(self, val, nid=None):
        self.val = val
        self.left = None
        self.right = None
        self.id = nid  # 唯一 id（由 BinaryTree 分配）

class BinaryTree:
    def __init__(self):
        self.root = None
        self.listeners = []
        self._id_counter = 0

    def _new_id(self):
        self._id_counter += 1
        return self._id_counter

    def add_listener(self, func):
        self.listeners.append(func)

    def notify(self, action, node=None):
        for f in self.listeners:
            # 传回动作、涉及节点对象（如果有）和当前根节点
            f({"action": action, "node": node, "tree": self.root})

    def build_random(self, n=7):
        """按层产生 n 个随机节点组成二叉树（索引性结构，便于演示）"""
        if n <= 0:
            self.root = None
            self.notify("build")
            return
        values = [random.randint(0, 100) for _ in range(n)]
        nodes = [TreeNode(v, nid=self._new_id()) for v in values]
        for i in range(n):
            if 2 * i + 1 < n:
                nodes[i].left = nodes[2 * i + 1]
            if 2 * i + 2 < n:
                nodes[i].right = nodes[2 * i + 2]
        self.root = nodes[0]
        self.notify("build")

    def insert(self, val):
        new_node = TreeNode(val, nid=self._new_id())
        if not self.root:
            self.root = new_node
            self.notify("insert", new_node)
            return new_node
        q = deque([self.root])
        #层序遍历找第一个空位（左子树为空则插左，否则插右）
        while q:
            cur = q.popleft()
            if not cur.left:
                cur.left = new_node
                break
            elif not cur.right:
                cur.right = new_node
                break
            else:
                q.append(cur.left)
                q.append(cur.right)
        self.notify("insert", new_node)
        return new_node

    # ---------- 遍历（返回节点对象列表，而非值） ----------
    def preorder_nodes(self):
        nodes = []
        def dfs(node):
            if not node: return
            nodes.append(node)
            dfs(node.left)
            dfs(node.right)
        dfs(self.root)
        return nodes

    def inorder_nodes(self):
        nodes = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            nodes.append(node)
            dfs(node.right)
        dfs(self.root)
        return nodes

    def postorder_nodes(self):
        nodes = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            dfs(node.right)
            nodes.append(node)
        dfs(self.root)
        return nodes
