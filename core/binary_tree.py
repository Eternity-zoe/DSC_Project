# core/binary_tree.py
import random
from typing import List 
from collections import deque
from .tree_traversals import preorder_traversal, inorder_traversal, postorder_traversal  # 导入新模块

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

    def build_random(self, n=7, is_complete=False):
        """按层产生 n 个随机节点组成二叉树"""
        if n <= 0:
            self.root = None
            self.notify("build")
            return
        values = [random.randint(0, 100) for _ in range(n)]
        nodes = [TreeNode(v, nid=self._new_id()) for v in values]
        
        # 完全二叉树逻辑：只连接前 floor(n/2) 个节点的子节点
        max_parent = n // 2 if is_complete else n
        
        for i in range(max_parent):
            if 2 * i + 1 < n:
                nodes[i].left = nodes[2 * i + 1]
            if 2 * i + 2 < n:
                nodes[i].right = nodes[2 * i + 2]
        self.root = nodes[0] if nodes else None
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
    def preorder_nodes(self) -> List[TreeNode]:
        """获取前序遍历节点列表"""
        return preorder_traversal(
            root=self.root,
            get_left=lambda node: node.left,
            get_right=lambda node: node.right
        )

    def inorder_nodes(self) -> List[TreeNode]:
        """获取中序遍历节点列表"""
        return inorder_traversal(
            root=self.root,
            get_left=lambda node: node.left,
            get_right=lambda node: node.right
        )

    def postorder_nodes(self) -> List[TreeNode]:
        """获取后序遍历节点列表"""
        return postorder_traversal(
            root=self.root,
            get_left=lambda node: node.left,
            get_right=lambda node: node.right
        )