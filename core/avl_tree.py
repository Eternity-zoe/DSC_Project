# core/avl_tree.py
import random

class AVLNode:
    def __init__(self, val):
        self.val = val
        self.freq = 1
        self.left = None
        self.right = None
        self.parent = None  # 新增父节点引用
        self.height = 1  # AVL树节点高度

class AVLTree:
    def __init__(self):
        self.root = None
        self.listeners = []
        self.state_list = []  # 状态列表用于回溯

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

    # 右旋转（带通知：旋转前通知与旋转后通知）
    def _right_rotate(self, y):
        # 更新父节点引用
        parent = y.parent
        is_left_child = parent and parent.left == y

        # 在实际改变指针之前，通知 GUI 记录旋转前状态
        try:
            if y and y.left:
                self.notify("rotation_prepare", node=y, extra={
                    "type": "right", 
                    "pivot": y.left.val,
                    "bf": self._balance_factor(y),
                    "child_bf": self._balance_factor(y.left)
                })
        except Exception:
            pass

        x = y.left
        T2 = x.right

        # 旋转操作（标准）
        x.right = y
        y.left = T2
        
        # 更新父节点引用
        x.parent = parent
        y.parent = x
        if T2:
            T2.parent = y

        if parent:
            if is_left_child:
                parent.left = x
            else:
                parent.right = x
        else:
            self.root = x  # 如果y是根节点，更新根

        # 更新高度
        self._update_height(y)
        self._update_height(x)

        # 旋转完成，通知 GUI 记录旋转后状态并启动动画
        try:
            self.notify("rotation", node=x, extra={"type": "right", "pivot": x.val})
        except Exception:
            pass

        return x

    # 左旋转（带通知）
    def _left_rotate(self, x):
        # 更新父节点引用
        parent = x.parent
        is_left_child = parent and parent.left == x

        # 通知 GUI 记录旋转前状态
        try:
            if x and x.right:
                self.notify("rotation_prepare", node=x, extra={
                    "type": "left", 
                    "pivot": x.right.val,
                    "bf": self._balance_factor(x),
                    "child_bf": self._balance_factor(x.right)
                })
        except Exception:
            pass

        y = x.right
        T2 = y.left

        # 旋转操作（标准）
        y.left = x
        x.right = T2
        
        # 更新父节点引用
        y.parent = parent
        x.parent = y
        if T2:
            T2.parent = x

        if parent:
            if is_left_child:
                parent.left = y
            else:
                parent.right = y
        else:
            self.root = y  # 如果x是根节点，更新根

        # 更新高度
        self._update_height(x)
        self._update_height(y)

        if y.parent:
            print(f"旋转后节点{y.val}的父节点为{y.parent.val}")
        else:
            print(f"旋转后节点{y.val}为根节点（父节点None）")

        # 通知 GUI 旋转后状态
        try:
            self.notify("rotation", node=y, extra={"type": "left", "pivot": y.val})
        except Exception:
            pass

        return y

    # 插入节点
    def insert(self, val, step_callback=None,skip_balance_notify=False):
        path = []
        
        def _insert(node, val, parent=None):
            if not node:
                new_node = AVLNode(val)
                new_node.parent = parent
                path.append(new_node)
                return new_node, path
            
            path.append(node)
            if val < node.val:
                node.left, _ = _insert(node.left, val, parent=node)
            elif val > node.val:
                node.right, _ = _insert(node.right, val, parent=node)
            else:
                # 值相等，增加频率
                node.freq += 1
                if step_callback:
                    step_callback(f"节点 {val} 已存在，频率+1 -> {node.freq}")
                return node, path

            # 更新当前节点高度
            self._update_height(node)
            return node, path

        
        if step_callback:
            step_callback(f"开始插入值：{val}")
            
        self.root, path = _insert(self.root, val)
        
        # 只有非随机生成时才执行这些通知
        if not skip_balance_notify:
            # 通知插入完成（BST阶段）
            new_node = path[-1]
            self.notify("bst_insert_complete", new_node, extra=path)
            if step_callback:
                step_callback(f"BST插入完成：节点 {val}")

            # 从插入节点向上检查平衡
            current = new_node
            while current:
                # 计算平衡因子
                bf = self._balance_factor(current)
                
                # 通知检查当前节点
                self.notify("check_balance", current, {
                    "bf": bf,
                    "is_balanced": abs(bf) <= 1,
                    "path": path
                })
                if step_callback:
                    status = "正常" if abs(bf) <= 1 else "失衡"
                    step_callback(f"检查节点 {current.val}，平衡因子={bf}（{status}）")

                # 处理失衡情况
                if bf > 1:  # 左偏失衡
                    left_child = current.left
                    left_bf = self._balance_factor(left_child) if left_child else 0
                    
                    # 通知检测到左偏失衡
                    self.notify("left_imbalance", current, {
                        "bf": bf,
                        "child": left_child,
                        "child_bf": left_bf
                    })
                    
                    if left_bf >= 0:  # 左左情况：右单旋
                        if step_callback:
                            step_callback(f"左左不平衡，对节点 {current.val} 执行右旋转")
                        current = self._right_rotate(current)
                    else:  # 左右情况：先左后右双旋
                        if step_callback:
                            step_callback(f"左右不平衡，先对 {left_child.val} 左旋转，再对 {current.val} 右旋转")
                        current.left = self._left_rotate(left_child)
                        current = self._right_rotate(current)
                        
                elif bf < -1:  # 右偏失衡
                    right_child = current.right
                    right_bf = self._balance_factor(right_child) if right_child else 0
                    
                    # 通知检测到右偏失衡
                    self.notify("right_imbalance", current, {
                        "bf": bf,
                        "child": right_child,
                        "child_bf": right_bf
                    })
                    
                    if right_bf <= 0:  # 右右情况：左单旋
                        if step_callback:
                            step_callback(f"右右不平衡，对节点 {current.val} 执行左旋转")
                        current = self._left_rotate(current)
                    else:  # 右左情况：先右后左双旋
                        if step_callback:
                            step_callback(f"右左不平衡，先对 {right_child.val} 右旋转，再对 {current.val} 左旋转")
                        current.right = self._right_rotate(right_child)
                        current = self._left_rotate(current)

                # 移动到父节点
                next_node = current.parent
                if next_node:
                    self.notify("move_to_parent", current, {"next_node": next_node})
                    if step_callback:
                        step_callback(f"移动到父节点 {next_node.val} 继续检查")
                current = next_node

            # 通知平衡检查完成
            self.notify("balance_complete", self.root, {})
            if step_callback:
                step_callback("所有节点检查完毕，树已平衡")

        return self.root

    # 删除节点
    def delete(self, val, step_callback=None):
        path = []
        deleted_node = None
        
        def _delete(node, val, parent=None):
            nonlocal deleted_node
            if not node:
                return node, path
                
            path.append(node)
            if val < node.val:
                node.left, _ = _delete(node.left, val, node)
            elif val > node.val:
                node.right, _ = _delete(node.right, val, node)
            else:
                # 找到要删除的节点
                deleted_node = node
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
                node.left, _ = _delete(node.left, temp.val, node)

            # 如果树只有一个节点，删除后为空
            if not node:
                return node, path

            # 更新父节点引用
            if node.left:
                node.left.parent = node
            if node.right:
                node.right.parent = node
                
            # 更新高度
            self._update_height(node)
            return node, path


        if step_callback:
            step_callback(f"开始删除值：{val}")
            
        self.root, path = _delete(self.root, val)
        
        # 通知删除完成（BST阶段）
        self.notify("bst_delete_complete", deleted_node, extra=path)
        if step_callback:
            step_callback(f"BST删除完成：节点 {val}")

        # 从删除节点的父节点向上检查平衡
        current = path[-1].parent if path else None
        while current:
            # 计算平衡因子
            bf = self._balance_factor(current)
            
            # 通知检查当前节点
            self.notify("check_balance", current, {
                "bf": bf,
                "is_balanced": abs(bf) <= 1,
                "path": path
            })
            if step_callback:
                status = "正常" if abs(bf) <= 1 else "失衡"
                step_callback(f"检查节点 {current.val}，平衡因子={bf}（{status}）")

            # 处理失衡情况（与插入相同的逻辑）
            if bf > 1:  # 左偏失衡
                left_child = current.left
                left_bf = self._balance_factor(left_child) if left_child else 0
                
                self.notify("left_imbalance", current, {
                    "bf": bf,
                    "child": left_child,
                    "child_bf": left_bf
                })
                
                if left_bf >= 0:  # 左左情况：右单旋
                    if step_callback:
                        step_callback(f"左左不平衡，对节点 {current.val} 执行右旋转")
                    current = self._right_rotate(current)
                else:  # 左右情况：先左后右双旋
                    if step_callback:
                        step_callback(f"左右不平衡，先对 {left_child.val} 左旋转，再对 {current.val} 右旋转")
                    current.left = self._left_rotate(left_child)
                    current = self._right_rotate(current)
                    
            elif bf < -1:  # 右偏失衡
                right_child = current.right
                right_bf = self._balance_factor(right_child) if right_child else 0
                
                self.notify("right_imbalance", current, {
                    "bf": bf,
                    "child": right_child,
                    "child_bf": right_bf
                })
                
                if right_bf <= 0:  # 右右情况：左单旋
                    if step_callback:
                        step_callback(f"右右不平衡，对节点 {current.val} 执行左旋转")
                    current = self._left_rotate(current)
                else:  # 右左情况：先右后左双旋
                    if step_callback:
                        step_callback(f"右左不平衡，先对 {right_child.val} 右旋转，再对 {current.val} 左旋转")
                    current.right = self._right_rotate(right_child)
                    current = self._left_rotate(current)

            # 移动到父节点
            next_node = current.parent
            if next_node:
                self.notify("move_to_parent", current, {"next_node": next_node})
                if step_callback:
                    step_callback(f"移动到父节点 {next_node.val} 继续检查")
            current = next_node

        # 通知平衡检查完成
        self.notify("balance_complete", self.root, {})
        if step_callback:
            step_callback("所有节点检查完毕，树已平衡")
        
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
            # 随机插入时跳过平衡检查的通知流程
            self.insert(v, step_callback=step_callback)
            if step_callback:
                step_callback(f"插入第 {i+1} 个节点：{v}")
        # 所有插入结束后，重新计算整棵树高度 + 平衡因子
        self._recalculate_all(self.root)
        
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
