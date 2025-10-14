# core/bst_tree.py
import random
from collections import deque

class BSTNode:
    def __init__(self, val):
        self.val = val
        self.freq = 1          # 多集合频率计数（frequency）
        self.left = None
        self.right = None

class BSTree:
    def __init__(self):
        self.root = None
        self.listeners = []

    def add_listener(self, func):
        self.listeners.append(func)

    def notify(self, action, node=None, extra=None):
        """
        action: 字符串，比如 'insert','found','not_found','delete','increase_freq','decrease_freq','build'
        node: 涉及的节点对象（或 None）
        extra: 可选附加信息（比如路径 node 列表）
        """
        for f in self.listeners:
            f({"action": action, "node": node, "tree": self.root, "extra": extra})

    # ---------- 插入（考虑频率） ----------
    def insert(self, val):
        """向 BST 插入 val；若存在则 freq++ 并通知 increase_freq"""
        if not self.root:
            self.root = BSTNode(val)
            self.notify("insert", self.root, extra=[self.root])
            return self.root

        parent = None
        cur = self.root
        path = []
        while cur:
            path.append(cur)
            parent = cur
            if val < cur.val:
                cur = cur.left
            elif val > cur.val:
                cur = cur.right
            else:
                # 已存在，增加频率
                cur.freq += 1
                self.notify("increase_freq", cur, extra=path + [cur])
                return cur

        new_node = BSTNode(val)
        if val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
        path.append(new_node)
        self.notify("insert", new_node, extra=path)
        return new_node

    # ---------- 查找（返回节点或 None，通知路径） ----------
    def search(self, val):
        cur = self.root
        path = []
        while cur:
            path.append(cur)
            if val == cur.val:
                self.notify("found", cur, extra=path)
                return cur
            elif val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        self.notify("not_found", None, extra=path)
        return None

    # ---------- 删除（考虑 freq：freq>1 则 --freq） ----------
    def delete(self, val):
        parent = None
        cur = self.root
        path = []
        # 先找到节点
        while cur and cur.val != val:
            path.append(cur)
            parent = cur
            cur = cur.left if val < cur.val else cur.right

        if not cur:
            self.notify("not_found", None, extra=path)
            return False

        # 如果频率 >1，优先只减频率，不删除节点
        if getattr(cur, "freq", 1) > 1:
            cur.freq -= 1
            self.notify("decrease_freq", cur, extra=path + [cur])
            return True

        # 情况1: 叶子节点
        if not cur.left and not cur.right:
            if not parent:
                self.root = None
            elif parent.left == cur:
                parent.left = None
            else:
                parent.right = None
        # 情况2: 单子节点
        elif not cur.left or not cur.right:
            child = cur.left or cur.right
            if not parent:
                self.root = child
            elif parent.left == cur:
                parent.left = child
            else:
                parent.right = child
        # 情况3: 双子节点，使用后继（右子树最小）替换
        else:
            succ_parent = cur
            succ = cur.right
            while succ.left:
                succ_parent = succ
                succ = succ.left
            # 将后继值与频率搬到 cur
            cur.val = succ.val
            cur.freq = succ.freq
            # 删除后继节点（succ）
            if succ_parent.left == succ:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right
            # 实际删除的节点是 succ，通知时仍把 cur 作为代表（结构已更新）
            self.notify("delete", cur, extra=path + [cur])
            return True

        # 对于情形 1/2，通知删除
        self.notify("delete", cur, extra=path)
        return True

    # ---------- 中序（返回值序列） ----------
    def inorder(self):
        res = []
        def dfs(node):
            if not node: return
            dfs(node.left)
            # 如果频率>1，把值重复 freq 次或用标记显示，UI 可选择如何显示
            for _ in range(node.freq):
                res.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return res

    # ---------- 构建随机 BST（更不易倾斜） ----------
    def build_random(self, n=7, value_range=(0, 100)):
        """
        随机生成 n 个不重复的键（sample），并按随机顺序插入以减少极端倾斜。
        n: 节点数量
        value_range: (low, high)
        """
        low, high = value_range
        if n <= 0:
            self.root = None
            self.notify("build", None, extra=[])
            return
        # 若 n 大于范围大小，就允许重复，但优先尽量不重复
        rng = high - low + 1
        if n <= rng:
            values = random.sample(range(low, high + 1), n)
        else:
            # 需要重复，使用 random.choices
            values = random.choices(range(low, high + 1), k=n)
        # 为了让树更“随机”，先打乱插入顺序
        random.shuffle(values)
        self.root = None
        for v in values:
            self.insert(v)
        self.notify("build", None, extra=values)
        return values

    # ---------- 额外工具（可选） ----------
    def lower_bound(self, val):
        """返回第一个 >= val 的节点（若无返回 None）"""
        cur = self.root
        res = None
        while cur:
            if cur.val >= val:
                res = cur
                cur = cur.left
            else:
                cur = cur.right
        return res

    def successor(self, val):
        """返回值 > val 的最小节点（后继）"""
        node = self.search(val)
        if node and node.right:
            cur = node.right
            while cur.left:
                cur = cur.left
            return cur
        succ = None
        cur = self.root
        while cur:
            if val < cur.val:
                succ = cur
                cur = cur.left
            elif val > cur.val:
                cur = cur.right
            else:
                break
        return succ

    def predecessor(self, val):
        node = self.search(val)
        if node and node.left:
            cur = node.left
            while cur.right:
                cur = cur.right
            return cur
        pred = None
        cur = self.root
        while cur:
            if val > cur.val:
                pred = cur
                cur = cur.right
            elif val < cur.val:
                cur = cur.left
            else:
                break
        return pred
