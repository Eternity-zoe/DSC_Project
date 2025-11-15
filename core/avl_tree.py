# core/avl_tree.py
import random

class AVLNode:
    def __init__(self, val):
        self.val = val
        self.freq = 1
        self.left = None
        self.right = None
        self.height = 1  # AVL树节点高度

class AVLTree:
    def __init__(self):
        self.root = None
        self.listeners = []

    def add_listener(self, func):
        self.listeners.append(func)

    def notify(self, action, node=None, extra=None):
        for f in self.listeners:
            f({"action": action, "node": node, "tree": self.root, "extra": extra})

    # 辅助函数：获取节点高度
    def _height(self, node):
        return node.height if node else 0

    # 辅助函数：计算平衡因子
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    # 更新节点高度
    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    # 右旋转
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)
        return x

    # 左旋转
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)
        return y

    # 插入节点
    def insert(self, val, step_callback=None):
        path = []
        
        def _insert(node, val):
            if not node:
                new_node = AVLNode(val)
                path.append(new_node)
                return new_node, path
            
            path.append(node)
            if val < node.val:
                node.left, _ = _insert(node.left, val)
            elif val > node.val:
                node.right, _ = _insert(node.right, val)
            else:
                # 值相等，增加频率
                node.freq += 1
                if step_callback:
                    step_callback(f"节点 {val} 已存在，频率+1 -> {node.freq}")
                return node, path

            # 更新当前节点高度
            self._update_height(node)

            # 计算平衡因子
            balance = self._balance_factor(node)

            # 左左情况：右旋转
            if balance > 1 and val < node.left.val:
                if step_callback:
                    step_callback(f"左左不平衡，对节点 {node.val} 执行右旋转")
                return self._right_rotate(node), path

            # 右右情况：左旋转
            if balance < -1 and val > node.right.val:
                if step_callback:
                    step_callback(f"右右不平衡，对节点 {node.val} 执行左旋转")
                return self._left_rotate(node), path

            # 左右情况：先左旋转后右旋转
            if balance > 1 and val > node.left.val:
                if step_callback:
                    step_callback(f"左右不平衡，先对 {node.left.val} 左旋转，再对 {node.val} 右旋转")
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node), path

            # 右左情况：先右旋转后左旋转
            if balance < -1 and val < node.right.val:
                if step_callback:
                    step_callback(f"右左不平衡，先对 {node.right.val} 右旋转，再对 {node.val} 左旋转")
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node), path

            return node, path

        if step_callback:
            step_callback(f"开始插入值：{val}")
            
        self.root, path = _insert(self.root, val)
        
        # 通知更新
        if val < path[-1].val or val > path[-1].val:  # 新节点
            self.notify("insert", path[-1], extra=path)
            if step_callback:
                step_callback(f"插入新节点 {val}")
        else:  # 频率增加
            self.notify("increase_freq", path[-1], extra=path)
            
        return self.root

    # 查找节点
    def search(self, val, step_callback=None):
        if step_callback:
            step_callback(f"开始查找值：{val}")
            
        cur = self.root
        path = []
        while cur:
            path.append(cur)
            if step_callback:
                step_callback(f"比较节点 {cur.val}")
                
            if val == cur.val:
                self.notify("found", cur, extra=path)
                if step_callback:
                    step_callback(f"找到节点 {val}（频率：{cur.freq}）")
                return cur
            elif val < cur.val:
                cur = cur.left
                if step_callback and cur:
                    step_callback(f"前往左子树继续查找")
            else:
                cur = cur.right
                if step_callback and cur:
                    step_callback(f"前往右子树继续查找")

        self.notify("not_found", None, extra=path)
        if step_callback:
            step_callback(f"未找到节点 {val}")
        return None

    # 删除节点
    def delete(self, val, step_callback=None):
        if step_callback:
            step_callback(f"开始删除值：{val}")
            
        path = []
        
        def _delete(node, val):
            if not node:
                return node, path
                
            path.append(node)
            if val < node.val:
                node.left, _ = _delete(node.left, val)
            elif val > node.val:
                node.right, _ = _delete(node.right, val)
            else:
                # 找到要删除的节点
                if step_callback:
                    step_callback(f"找到要删除的节点 {val}")
                    
                # 频率大于1，只减少频率
                if node.freq > 1:
                    node.freq -= 1
                    if step_callback:
                        step_callback(f"节点 {val} 频率-1 -> {node.freq}")
                    return node, path

                # 叶子节点或只有一个子节点
                if not node.left:
                    return node.right, path
                elif not node.right:
                    return node.left, path

                # 有两个子节点，找前驱（左子树最大值）
                temp = self._get_max(node.left)
                if step_callback:
                    step_callback(f"使用前驱节点 {temp.val} 替换待删除节点")
                    
                node.val = temp.val
                node.freq = temp.freq
                
                # 删除前驱节点
                node.left, _ = _delete(node.left, temp.val)

            # 如果树只有一个节点，删除后为空
            if not node:
                return node, path

            # 更新高度
            self._update_height(node)

            # 计算平衡因子
            balance = self._balance_factor(node)

            # 左左
            if balance > 1 and self._balance_factor(node.left) >= 0:
                if step_callback:
                    step_callback(f"左左不平衡，对节点 {node.val} 执行右旋转")
                return self._right_rotate(node), path

            # 左右
            if balance > 1 and self._balance_factor(node.left) < 0:
                if step_callback:
                    step_callback(f"左右不平衡，先对 {node.left.val} 左旋转，再对 {node.val} 右旋转")
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node), path

            # 右右
            if balance < -1 and self._balance_factor(node.right) <= 0:
                if step_callback:
                    step_callback(f"右右不平衡，对节点 {node.val} 执行左旋转")
                return self._left_rotate(node), path

            # 右左
            if balance < -1 and self._balance_factor(node.right) > 0:
                if step_callback:
                    step_callback(f"右左不平衡，先对 {node.right.val} 右旋转，再对 {node.val} 左旋转")
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node), path

            return node, path

        # 获取左子树最大值（前驱）
        def _get_max(node):
            current = node
            while current.right:
                current = current.right
            return current

        self.root, path = _delete(self.root, val)
        
        if self.root or path:
            self.notify("delete", None if not path else path[-1], extra=path)
        
        return self.root

    # 中序遍历
    def inorder(self):
        res = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            for _ in range(node.freq):
                res.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return res

    # 随机生成AVL树
    def build_random(self, n=7, value_range=(1, 100), step_callback=None):
        low, high = value_range
        if n <= 0:
            self.root = None
            self.notify("build", None, extra=[])
            if step_callback:
                step_callback("清空树，生成空AVL树")
            return []
        
        rng = high - low + 1
        if n <= rng:
            values = random.sample(range(low, high + 1), n)
        else:
            values = random.choices(range(low, high + 1), k=n)
        random.shuffle(values)
        
        if step_callback:
            step_callback(f"随机生成值序列：{values}")
        
        self.root = None
        for i, v in enumerate(values):
            self.insert(v, step_callback=step_callback)
            if step_callback:
                step_callback(f"插入第 {i+1} 个节点：{v}")
        
        self.notify("build", None, extra=values)
        return values

    # 高级查找功能
    def lower_bound(self, val, step_callback=None):
        if step_callback:
            step_callback(f"查找值 {val} 的lower_bound（首个≥{val}的节点）")
            
        cur = self.root
        res = None
        path = []
        while cur:
            path.append(cur)
            if step_callback:
                step_callback(f"比较节点 {cur.val}")
                
            if cur.val >= val:
                res = cur
                cur = cur.left
                if step_callback:
                    step_callback(f"当前节点 {res.val} ≥ {val}，继续向左查找更小的符合条件节点")
            else:
                cur = cur.right
                if step_callback:
                    step_callback(f"当前节点 {cur.val if cur else 'None'} < {val}，继续向右查找")
        
        self.notify("trace_path", res, extra=path)
        return res, path

    def successor(self, val, step_callback=None):
        if step_callback:
            step_callback(f"查找值 {val} 的后继（中序遍历后一个节点）")
            
        path = []
        cur = self.root
        succ = None
        while cur:
            path.append(cur)
            if step_callback:
                step_callback(f"比较节点 {cur.val}")
                
            if val < cur.val:
                succ = cur
                cur = cur.left
                if step_callback:
                    step_callback(f"当前节点 {succ.val} 可能是后继，继续向左查找更小的候选")
            elif val > cur.val:
                cur = cur.right
                if step_callback:
                    step_callback(f"当前节点 {cur.val if cur else 'None'} 小于目标，继续向右查找")
            else:
                if step_callback:
                    step_callback(f"找到目标节点 {val}，寻找其右子树最小值")
                # 找到节点，后继是右子树的最小值
                if cur.right:
                    succ = self._get_min(cur.right)
                    path.append(succ)
                break
        
        self.notify("trace_path", succ, extra=path)
        return succ, path

    def predecessor(self, val, step_callback=None):
        if step_callback:
            step_callback(f"查找值 {val} 的前驱（中序遍历前一个节点）")
            
        path = []
        cur = self.root
        pred = None
        while cur:
            path.append(cur)
            if step_callback:
                step_callback(f"比较节点 {cur.val}")
                
            if val > cur.val:
                pred = cur
                cur = cur.right
                if step_callback:
                    step_callback(f"当前节点 {pred.val} 可能是前驱，继续向右查找更大的候选")
            elif val < cur.val:
                cur = cur.left
                if step_callback:
                    step_callback(f"当前节点 {cur.val if cur else 'None'} 大于目标，继续向左查找")
            else:
                if step_callback:
                    step_callback(f"找到目标节点 {val}，寻找其左子树最大值")
                # 找到节点，前驱是左子树的最大值
                if cur.left:
                    pred = self._get_max(cur.left)
                    path.append(pred)
                break
        
        self.notify("trace_path", pred, extra=path)
        return pred, path

    # 辅助函数：获取最小值节点
    def _get_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # 辅助函数：获取最大值节点
    def _get_max(self, node):
        current = node
        while current.right:
            current = current.right
        return current