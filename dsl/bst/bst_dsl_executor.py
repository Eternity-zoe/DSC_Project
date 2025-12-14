# dsl/bst/bst_dsl_executor.py
from PySide6.QtCore import QTimer
from dsl.bst.bst_dsl_ast import *

class BSTDSLExecutor:
    """BST DSL执行器"""
    
    def __init__(self, window):
        self.window = window  # 持有BST窗口引用
        self.cmds = []
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._step)
        self.delay = 800  # 命令执行间隔(毫秒)
    
    def execute(self, cmds):
        """执行一系列命令"""
        # 按照要求：一次执行 = 清空 → 重建 → 动画
        self.window.tree.root = None
        self.window.draw_tree(None)
        self.cmds = cmds
        self.index = 0
        self.timer.start(self.delay)
    
    def _step(self):
        """单步执行命令"""
        if self.index >= len(self.cmds):
            self.timer.stop()
            self.window.status.setText("DSL脚本执行完成")
            return
            
        cmd = self.cmds[self.index]
        self.index += 1
        self._execute_cmd(cmd)
    
    def _execute_cmd(self, cmd):
        """执行单个命令"""
        w = self.window
        
        if isinstance(cmd, ClearCmd):
            w.tree.root = None
            w.add_step("DSL操作: 清空树")
            w.draw_tree(None)
            
        # dsl/bst/bst_dsl_executor.py (修改部分)
        elif isinstance(cmd, BuildCmd):
            w.add_step(f"DSL操作: 构建BST，值序列: {cmd.values}")
            for i, val in enumerate(cmd.values):
                w.add_step(f"[insert] 开始插入 {val}")
                # 移除 skip_animation 参数
                w.tree.insert(val, step_callback=w.add_step)
                w.add_step(f"[build] 已插入第 {i+1} 个: {val}")
            w.draw_tree(w.tree.root)
            w.add_step("构建BST完成")
            
        elif isinstance(cmd, InsertCmd):
            w.add_step(f"DSL操作: 插入值 {cmd.value}")
            w.tree.insert(cmd.value, step_callback=w.add_step)
            
        elif isinstance(cmd, SearchCmd):
            w.add_step(f"DSL操作: 查找值 {cmd.value}")
            w.tree.search(cmd.value, step_callback=w.add_step)
            
        elif isinstance(cmd, DeleteCmd):
            w.add_step(f"DSL操作: 删除值 {cmd.value}")
            w.tree.delete(cmd.value, step_callback=w.add_step)
            
        elif isinstance(cmd, FindPredecessorCmd):
            w.add_step(f"DSL操作: 查找 {cmd.value} 的前驱")
            node, path = w.tree.predecessor(cmd.value, step_callback=w.add_step)
            w._animate_special_path("前驱", cmd.value, node, path)
            
        elif isinstance(cmd, FindSuccessorCmd):
            w.add_step(f"DSL操作: 查找 {cmd.value} 的后继")
            node, path = w.tree.successor(cmd.value, step_callback=w.add_step)
            w._animate_special_path("后继", cmd.value, node, path)
            
        elif isinstance(cmd, FindLowerBoundCmd):
            w.add_step(f"DSL操作: 查找 {cmd.value} 的下界")
            node, path = w.tree.lower_bound(cmd.value, step_callback=w.add_step)
            w._animate_special_path("下界", cmd.value, node, path)
            
        elif isinstance(cmd, InorderCmd):
            seq = w.tree.inorder()
            seq_text = " -> ".join(map(str, seq))
            w.add_step(f"DSL操作: 中序遍历结果: {seq_text}")
            w.status.setText(f"中序遍历: {seq_text}")
            
        elif isinstance(cmd, DrawCmd):
            w.add_step("DSL操作: 绘制树")
            w.draw_tree(w.tree.root)