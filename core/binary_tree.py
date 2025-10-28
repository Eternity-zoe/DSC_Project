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

    def build_random(self, n=7, is_complete=False, max_children=4):
        """
        生成随机二叉树
        :param n: 节点数量
        :param is_complete: 是否生成完全二叉树
        :param max_children: 非完全二叉树时最大子节点数（最多4个）
        """
        if n <= 0:
            self.root = None
            self.notify("build")
            return
        
        values = [random.randint(0, 100) for _ in range(n)]
        nodes = [TreeNode(v, nid=self._new_id()) for v in values]
        self.root = nodes[0] if nodes else None

        if is_complete:
            # 生成完全二叉树（按层序填充）
            for i in range(n):
                if 2 * i + 1 < n:
                    nodes[i].left = nodes[2 * i + 1]
                if 2 * i + 2 < n:
                    nodes[i].right = nodes[2 * i + 2]
        else:
            # 生成普通二叉树，每个节点最多max_children个子节点（最多4个）
            # 确保根节点存在
            if not nodes:
                self.notify("build")
                return
                
            # 使用队列进行层序遍历分配子节点
            q = deque([nodes[0]])
            current_idx = 1  # 从第二个节点开始分配
            
            while q and current_idx < n:
                current_node = q.popleft()
                # 随机生成子节点数量（1到max_children之间，不超过剩余节点数）
                remaining = n - current_idx
                num_children = random.randint(1, min(max_children, remaining))
                
                # 分配左子树（最多2个左子节点，模拟二叉树扩展）
                left_count = min(num_children, 2)
                if left_count >= 1:
                    current_node.left = nodes[current_idx]
                    q.append(nodes[current_idx])
                    current_idx += 1
                if left_count >= 2 and current_idx < n:
                    # 第二个左子节点作为左子树的右节点
                    current_node.left.right = nodes[current_idx]
                    q.append(nodes[current_idx])
                    current_idx += 1
                
                # 分配右子树（剩余的子节点数量）
                right_count = num_children - left_count
                if right_count >= 1 and current_idx < n:
                    current_node.right = nodes[current_idx]
                    q.append(nodes[current_idx])
                    current_idx += 1
                if right_count >= 2 and current_idx < n:
                    # 第二个右子节点作为右子树的右节点
                    current_node.right.right = nodes[current_idx]
                    q.append(nodes[current_idx])
                    current_idx += 1

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