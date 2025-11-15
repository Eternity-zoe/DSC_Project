# core/bst_tree.py
# 完整的 BST 数据结构（支持 multiset via freq）并提供可视化/动画友好的回调与路径信息
import random
from collections import deque

class BSTNode:
    def __init__(self, val, parent=None):
        self.val = val
        self.freq = 1
        self.left = None
        self.right = None
        self.parent = parent  # 父指针，便于向上遍历 / 更新

        # AVL/统计属性（即使不平衡也保持这些属性以便展示）
        self.height = 1
        self.bf = 0          # balance factor = left.height - right.height
        self.sz = 1          # 子树大小（包含freq计数时这里记录节点个数，不重复计数freq；选择第k小时会考虑freq）

        # 可视化属性占位（UI 端可以在节点上写入 cx/cy / state）
        self.cx = None
        self.cy = None
        self.state = "default"  # 可选值：default / highlight / visited 等

    def __repr__(self):
        return f"BSTNode({self.val},freq={self.freq})"

class BSTree:
    def __init__(self):
        self.root = None
        self.listeners = []

    def add_listener(self, func):
        self.listeners.append(func)

    def notify(self, action, node=None, extra=None):
        """
        统一通知，用于 UI 更新。
        action: 'insert','increase_freq','decrease_freq','delete','found','not_found','build','trace_path','update'
        node: 发生操作的节点（或 None）
        extra: 附加信息，通常为路径列表（节点对象列表）或直接的数据
        """
        payload = {"action": action, "node": node, "tree": self.root, "extra": extra}
        for f in self.listeners:
            try:
                f(payload)
            except Exception:
                # listener 不应影响核心逻辑
                pass

    # ---------- 辅助：节点属性更新 ----------
    def _update_node(self, node):
        """根据子节点更新 node.height, node.bf, node.sz"""
        if not node:
            return
        lh = node.left.height if node.left else 0
        rh = node.right.height if node.right else 0
        node.height = 1 + max(lh, rh)
        node.bf = lh - rh
        # 注意：sz 记录节点个数（节点数量，不重复频率），选择第k小时我们会按 freq 处理
        lsz = node.left.sz if node.left else 0
        rsz = node.right.sz if node.right else 0
        node.sz = 1 + lsz + rsz

    def _update_path_from(self, node):
        """从 node 向上更新到根的 height/bf/sz"""
        cur = node
        while cur:
            self._update_node(cur)
            cur = cur.parent

    # ---------- 插入 ----------
    def insert(self, val, step_callback=None):
        """
        插入 val（支持频率计数）
        step_callback: 可选，string 类型步骤记录函数（例如 UI 的 add_step）
        返回插入或增加频率的节点
        """
        if step_callback:
            step_callback(f"[insert] 开始插入 {val}")

        if not self.root:
            self.root = BSTNode(val)
            self._update_path_from(self.root)
            self.notify("insert", self.root, extra=[self.root])
            if step_callback:
                step_callback(f"[insert] 创建根节点 {val}")
            return self.root

        cur = self.root
        parent = None
        path = []
        while cur:
            path.append(cur)
            parent = cur
            if val < cur.val:
                if step_callback:
                    step_callback(f"[insert] 比较 {val} < {cur.val} -> 向左")
                cur = cur.left
            elif val > cur.val:
                if step_callback:
                    step_callback(f"[insert] 比较 {val} > {cur.val} -> 向右")
                cur = cur.right
            else:
                # 相等：频率+1
                cur.freq += 1
                # 更新上游统计信息
                self._update_path_from(cur)
                self.notify("increase_freq", cur, extra=path + [cur])
                if step_callback:
                    step_callback(f"[insert] 值已存在，频率增加到 {cur.freq}")
                return cur

        # 插入新节点
        new_node = BSTNode(val, parent=parent)
        if val < parent.val:
            parent.left = new_node
            if step_callback:
                step_callback(f"[insert] 在 {parent.val} 左侧插入 {val}")
        else:
            parent.right = new_node
            if step_callback:
                step_callback(f"[insert] 在 {parent.val} 右侧插入 {val}")

        # 更新路径属性
        self._update_path_from(new_node)
        # 通知，extra 使用插入路径（便于动画）
        path.append(new_node)
        self.notify("insert", new_node, extra=path)
        return new_node

    # ---------- 搜索 ----------
    def search(self, val, step_callback=None):
        """精确搜索（返回节点或 None），并通过 notify 发送路径（用于动画）"""
        if step_callback:
            step_callback(f"[search] 开始查找 {val}")
        cur = self.root
        path = []
        while cur:
            path.append(cur)
            if step_callback:
                step_callback(f"[search] 比较目标 {val} 与 节点 {cur.val}")
            if val == cur.val:
                self.notify("found", cur, extra=path)
                if step_callback:
                    step_callback(f"[search] 找到节点 {cur.val} (freq={cur.freq})")
                return cur
            elif val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        self.notify("not_found", None, extra=path)
        if step_callback:
            step_callback(f"[search] 未找到 {val}")
        return None

    # ---------- lower_bound / successor / predecessor（均返回 node, path） ----------
    def lower_bound(self, val, step_callback=None):
        """返回第一个 >= val 的节点（以及访问路径）"""
        if step_callback:
            step_callback(f"[lower_bound] 查找首个 >= {val}")
        cur = self.root
        res = None
        path = []
        while cur:
            path.append(cur)
            if cur.val >= val:
                if step_callback:
                    step_callback(f"[lower_bound] {cur.val} >= {val}，记为候选，向左继续")
                res = cur
                cur = cur.left
            else:
                if step_callback:
                    step_callback(f"[lower_bound] {cur.val} < {val}，向右继续")
                cur = cur.right
        self.notify("trace_path", None, extra=path)
        return res, path

    def successor(self, val, step_callback=None):
        """返回 > =? 这里实现：返回严格大于 val 的最小节点（如果存在等于则返回该节点的后继），以及路径"""
        if step_callback:
            step_callback(f"[successor] 查找 {val} 的后继")
        path = []
        cur = self.root
        succ = None
        # first find path while searching for val (or where it would be)
        while cur:
            path.append(cur)
            if val < cur.val:
                succ = cur
                cur = cur.left
                if step_callback:
                    step_callback(f"[successor] {cur.parent.val if cur and cur.parent else '...'} 向左 (候选后继={succ.val})")
            elif val > cur.val:
                cur = cur.right
                if step_callback:
                    step_callback(f"[successor] 向右")
            else:
                # 找到节点：其后继是其右子树的最左节点（如存在），否则就是上层最后一次向左转的祖先（succ 已记录）
                if cur.right:
                    n = cur.right
                    path.append(n)
                    while n.left:
                        n = n.left
                        path.append(n)
                    succ = n
                break
        self.notify("trace_path", None, extra=path)
        return succ, path

    def predecessor(self, val, step_callback=None):
        """返回 < val 的最大节点（若存在等于，返回其前驱），以及路径"""
        if step_callback:
            step_callback(f"[predecessor] 查找 {val} 的前驱")
        path = []
        cur = self.root
        pred = None
        while cur:
            path.append(cur)
            if val > cur.val:
                pred = cur
                cur = cur.right
                if step_callback:
                    step_callback(f"[predecessor] {cur.parent.val if cur and cur.parent else '...'} 向右 (候选前驱={pred.val})")
            elif val < cur.val:
                cur = cur.left
                if step_callback:
                    step_callback(f"[predecessor] 向左")
            else:
                # 找到节点：其前驱是其左子树的最右节点（如存在）
                if cur.left:
                    n = cur.left
                    path.append(n)
                    while n.right:
                        n = n.right
                        path.append(n)
                    pred = n
                break
        self.notify("trace_path", None, extra=path)
        return pred, path

    # ---------- 删除 ----------
    def delete(self, val, step_callback=None):
        """
        删除 val（处理频率 >1 时只减频率）
        返回 True/False 表示是否发生删除（或频率递减）
        """
        if step_callback:
            step_callback(f"[delete] 开始删除 {val}")
        parent = None
        cur = self.root
        path = []
        # 查找节点并记录路径
        while cur and cur.val != val:
            path.append(cur)
            parent = cur
            if val < cur.val:
                if step_callback:
                    step_callback(f"[delete] 比较 {val} < {cur.val} -> 向左")
                cur = cur.left
            else:
                if step_callback:
                    step_callback(f"[delete] 比较 {val} > {cur.val} -> 向右")
                cur = cur.right

        if not cur:
            self.notify("not_found", None, extra=path)
            if step_callback:
                step_callback(f"[delete] 未找到节点 {val}")
            return False

        path.append(cur)
        # 若 freq>1, 仅递减频率
        if cur.freq > 1:
            cur.freq -= 1
            self._update_path_from(cur)
            self.notify("decrease_freq", cur, extra=path)
            if step_callback:
                step_callback(f"[delete] 节点存在，频率减为 {cur.freq}")
            return True

        # 三种情况
        if not cur.left and not cur.right:
            # 叶子
            if parent is None:
                self.root = None
            else:
                if parent.left == cur:
                    parent.left = None
                else:
                    parent.right = None
            self.notify("delete", cur, extra=path)
            if step_callback:
                step_callback(f"[delete] 叶子节点 {val} 已删除")
            # 更新父链
            if parent:
                self._update_path_from(parent)
            return True

        if not cur.left or not cur.right:
            # 单子节点：提升子节点
            child = cur.left or cur.right
            if parent is None:
                child.parent = None
                self.root = child
            else:
                if parent.left == cur:
                    parent.left = child
                else:
                    parent.right = child
                child.parent = parent
            self.notify("delete", cur, extra=path)
            if step_callback:
                step_callback(f"[delete] 单子节点 {val} 已删除，子节点提升")
            # 更新父链
            self._update_path_from(child.parent or child)
            return True

        # 双子节点：使用前驱（左子树最大）替换（也可用后继）
        pred_parent = cur
        pred = cur.left
        # 记录从 cur 到 pred 的路径用于动画
        while pred.right:
            pred_parent = pred
            pred = pred.right

        if step_callback:
            step_callback(f"[delete] 双子节点情况，用前驱 {pred.val} 替换 {cur.val}")

        # 把前驱的值和频率搬到 cur
        cur.val = pred.val
        cur.freq = pred.freq

        # 然后删除 pred 节点（pred 至多有左子树）
        if pred_parent == cur:
            # pred 是 cur.left 的位置
            pred_parent.left = pred.left
            if pred.left:
                pred.left.parent = pred_parent
        else:
            pred_parent.right = pred.left
            if pred.left:
                pred.left.parent = pred_parent

        # 更新属性
        # 更新从 pred_parent 开始向上
        self._update_path_from(pred_parent)
        # notify 时把 cur 作为被“替换后被删除/更新”的节点返回（方便UI显示）
        self.notify("delete", cur, extra=path + [pred])
        if step_callback:
            step_callback(f"[delete] 前驱 {pred.val} 已删除，替换完成")
        return True

    # ---------- 遍历（返回序列）并支持路径/动画 ----------
    def inorder(self, step_callback=None, animate=False):
        """返回中序序列。若 animate=True 会通过 notify(trace_path) 发送访问序列（节点列表）"""
        res = []
        visit_path = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            # 把节点按 freq 次数加入结果；但 visit_path 只记录节点对象一次（UI 在显示时可根据 freq 重复或标注）
            for _ in range(node.freq):
                res.append(node.val)
            visit_path.append(node)
            dfs(node.right)
        dfs(self.root)

        if animate:
            # 发送遍历路径以供动画
            self.notify("trace_path", None, extra=visit_path)
        if step_callback:
            step_callback(f"[inorder] 中序遍历结果: {res}")
        return res

    def preorder(self, step_callback=None, animate=False):
        res = []
        visit_path = []
        def dfs(node):
            if not node:
                return
            for _ in range(node.freq):
                res.append(node.val)
            visit_path.append(node)
            dfs(node.left)
            dfs(node.right)
        dfs(self.root)
        if animate:
            self.notify("trace_path", None, extra=visit_path)
        if step_callback:
            step_callback(f"[preorder] 前序遍历结果: {res}")
        return res

    def postorder(self, step_callback=None, animate=False):
        res = []
        visit_path = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            for _ in range(node.freq):
                res.append(node.val)
            visit_path.append(node)
        dfs(self.root)
        if animate:
            self.notify("trace_path", None, extra=visit_path)
        if step_callback:
            step_callback(f"[postorder] 后序遍历结果: {res}")
        return res

    # ---------- 选择第 k 小元素（1-based，考虑频率） ----------
    def kth_smallest(self, k, step_callback=None):
        """
        选择第 k 小元素（k 从 1 开始），返回 (node, path, local_index)
        local_index: 如果返回节点的频率>1，local_index 表示在该节点的第几次出现（从1开始）
        path: 访问过的节点顺序（用于动画）
        """
        if step_callback:
            step_callback(f"[kth] 选择第 {k} 小元素")
        path = []
        cur = self.root
        if not cur:
            if step_callback:
                step_callback("[kth] 树为空")
            return None, path, None

        # 为了支持 freq，我们需要在遍历时考虑左子树的“总元素数（含频率）”
        # 为效率，我们先构造一个辅助函数来计算以 node 为根的 total_count（含频率）
        def total_count(node):
            if not node:
                return 0
            l = total_count(node.left)
            r = total_count(node.right)
            return l + node.freq + r

        # 为避免重复大量计算，可在每个节点上按需缓存 total_count（这里直接用递归且树中节点数通常较小）
        # 下面用迭代：在每步计算左子树的总元素数
        while cur:
            path.append(cur)
            left_count = total_count(cur.left)
            if step_callback:
                step_callback(f"[kth] 在节点 {cur.val}，左子元素数={left_count}, 节点freq={cur.freq}")
            if k <= left_count:
                cur = cur.left
            elif k <= left_count + cur.freq:
                # 在当前节点的频率范围内
                local_index = k - left_count  # 1..freq
                self.notify("trace_path", None, extra=path)
                if step_callback:
                    step_callback(f"[kth] 找到：节点 {cur.val}，是其第 {local_index} 次")
                return cur, path, local_index
            else:
                k = k - (left_count + cur.freq)
                cur = cur.right

        # 若循环结束未返回
        self.notify("not_found", None, extra=path)
        if step_callback:
            step_callback("[kth] 未找到对应第 k 小（k 越界）")
        return None, path, None

    # ---------- 构建随机树（保持原 API） ----------
    def build_random(self, n=7, value_range=(0, 100), step_callback=None):
        """
        随机生成 n 个键并插入（支持重复）。与旧版本兼容，返回生成的值序列。
        """
        low, high = value_range
        if step_callback:
            step_callback(f"[build_random] 生成 {n} 个随机值，范围 {low}..{high}")
        if n <= 0:
            self.root = None
            self.notify("build", None, extra=[])
            if step_callback:
                step_callback("[build_random] 生成空树")
            return []

        rng = high - low + 1
        if n <= rng:
            values = random.sample(range(low, high + 1), n)
        else:
            values = random.choices(range(low, high + 1), k=n)
        random.shuffle(values)

        if step_callback:
            step_callback(f"[build_random] 值序列: {values}")
        # 清空树并插入
        self.root = None
        for i, v in enumerate(values):
            self.insert(v, step_callback=step_callback)
            if step_callback:
                step_callback(f"[build_random] 已插入第 {i+1} 个: {v}")
        self.notify("build", None, extra=values)
        return values

    # ---------- 额外工具：清空树 ----------
    def clear(self):
        self.root = None
        self.notify("update", None, extra=[])
