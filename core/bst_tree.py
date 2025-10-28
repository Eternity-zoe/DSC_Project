# core/bst_tree.py
import random
from collections import deque
from .tree_traversals import inorder_traversal  # 导入中序遍历

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

    def insert(self, val):
        if not self.root:#空树
            self.root = BSTNode(val)
            self.notify("insert", self.root, extra=[self.root])
            return self.root

        parent = None
        cur = self.root
        path = []
        while cur:
            path.append(cur)  # 记录查找路径
            parent = cur      # 保存当前节点的父节点
            if val < cur.val:
                cur = cur.left  # 小于当前值，向左子树查找
            elif val > cur.val:
                cur = cur.right  # 大于当前值，向右子树查找
            else:
                # 找到相等节点：增加频率，不创建新节点
                cur.freq += 1
                self.notify("increase_freq", cur, extra=path + [cur])
                return cur

        new_node = BSTNode(val)
        if val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
        path.append(new_node)  # 路径包含新节点
        self.notify("insert", new_node, extra=path)  # 通知插入事件
        return new_node

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
            #通知删除
            self.notify("delete", cur, extra=path + [cur])
            return True

        # 对于情形 1&2，通知删除
        self.notify("delete", cur, extra=path)
        return True

    # ---------- 中序（返回值序列） ----------
    def inorder(self):
        """中序遍历（返回值序列）"""
        # 使用通用遍历算法获取节点列表
        nodes = inorder_traversal(
            root=self.root,
            get_left=lambda node: node.left,
            get_right=lambda node: node.right
        )
        # 转换为值序列（考虑频率）
        res = []
        for node in nodes:
            res.extend([node.val] * node.freq)
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
        """返回第一个 >= val 的节点（带路径）"""
        cur = self.root
        res = None
        path = []
        while cur:
            path.append(cur)
            if cur.val >= val:
                res = cur
                cur = cur.left
            else:
                cur = cur.right
        self.notify("trace_path", None, extra=path)
        return res, path

    def successor(self, val):
        """返回比 val 大的最小节点（带路径）"""
        path = []
        cur = self.root
        succ = None
        while cur:
            path.append(cur)
            if val < cur.val:
                succ = cur
                cur = cur.left
            elif val > cur.val:
                cur = cur.right
            else:
                break
        self.notify("trace_path", None, extra=path)
        return succ, path

    def predecessor(self, val):
        """返回比 val 小的最大节点（带路径）"""
        path = []
        cur = self.root
        pred = None
        while cur:
            path.append(cur)
            if val > cur.val:
                pred = cur
                cur = cur.right
            elif val < cur.val:
                cur = cur.left
            else:
                break
        self.notify("trace_path", None, extra=path)
        return pred, path
