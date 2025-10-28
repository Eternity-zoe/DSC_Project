# core/binary_tree.py
import random
from collections import deque
from typing import List  # 新增导入

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
        """
        生成随机二叉树
        :param n: 节点数量
        :param is_complete: 是否生成完全二叉树
        """
        if n <= 0:
            self.root = None
            self.notify("build")
            return
            
        values = [random.randint(0, 100) for _ in range(n)]
        nodes = [TreeNode(v, nid=self._new_id()) for v in values]
        
        if is_complete:
            # 生成完全二叉树：按层序填充所有可能的位置
            for i in range(n):
                if 2 * i + 1 < n:
                    nodes[i].left = nodes[2 * i + 1]
                if 2 * i + 2 < n:
                    nodes[i].right = nodes[2 * i + 2]
        else:
            # 生成随机二叉树（每个节点子节点数≤4，实际因二叉树特性最多2个）
            # 先连接根节点
            if n == 0:
                self.root = None
                return
                
            self.root = nodes[0]
            available_nodes = [nodes[0]]  # 可添加子节点的节点队列
            
            # 为剩余节点随机分配父节点
            for i in range(1, n):
                if not available_nodes:
                    break  # 没有可添加子节点的节点了
                    
                # 随机选择一个可用节点作为父节点
                parent_idx = random.randint(0, len(available_nodes) - 1)
                parent = available_nodes[parent_idx]
                
                # 尝试添加左子节点
                if parent.left is None:
                    parent.left = nodes[i]
                    available_nodes.append(nodes[i])  # 新节点加入可用队列
                    # 如果父节点现在有两个子节点，从可用队列移除
                    if parent.right is not None:
                        available_nodes.pop(parent_idx)
                # 尝试添加右子节点
                elif parent.right is None:
                    parent.right = nodes[i]
                    available_nodes.append(nodes[i])  # 新节点加入可用队列
                    available_nodes.pop(parent_idx)  # 父节点已无空位，移除
                else:
                    # 该父节点已满，重新选择（递归调用当前循环）
                    i -= 1
                    continue
        
        self.root = nodes[0] if nodes else None
        self.notify("build")

    def insert(self, val):
        new_node = TreeNode(val, nid=self._new_id())
        if not self.root:
            self.root = new_node
            self.notify("insert", new_node)
            return new_node
        q = deque([self.root])
        # 层序遍历找第一个空位（左子树为空则插左，否则插右）
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
        nodes = []
        def dfs(node):
            if not node: return
            nodes.append(node)
            dfs(node.left)
            dfs(node.right)
        dfs(self.root)
        return nodes

    def inorder_nodes(self) -> List[TreeNode]:
        nodes = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            nodes.append(node)
            dfs(node.right)
        dfs(self.root)
        return nodes

    def postorder_nodes(self) -> List[TreeNode]:
        nodes = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            dfs(node.right)
            nodes.append(node)
        dfs(self.root)
        return nodes