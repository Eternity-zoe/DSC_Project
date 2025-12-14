# dsl/avl/avl_dsl_executor.py
from .avl_dsl_ast import (
    Program, ClearStatement, InsertStatement, DeleteStatement,
    SearchStatement, InorderStatement, RandomStatement, PredecessorStatement,
    SuccessorStatement, LowerBoundStatement, DelayStatement
)
from core.avl_tree import AVLTree
from PySide6.QtCore import QTimer, QCoreApplication
from typing import Callable, List

class AVLDslExecutor:
    """AVL树DSL执行器"""
    def __init__(self, tree: AVLTree, log_callback: Callable[[str], None], 
                 update_ui_callback: Callable[[], None]):
        self.tree = tree
        self.log_callback = log_callback  # 用于记录日志
        self.update_ui_callback = update_ui_callback  # 用于更新UI
        self.current_statement = 0  # 当前执行的语句索引
        self.statements: List = []  # 语句列表

    def execute(self, program: Program):
        """执行程序"""
        self.log_callback("=== 开始执行DSL脚本 ===")
        self.statements = program.statements
        self.current_statement = 0
        self._execute_next()

    def _execute_next(self):
        """执行下一条语句"""
        if self.current_statement >= len(self.statements):
            self.log_callback("=== DSL脚本执行完成 ===")
            return

        stmt = self.statements[self.current_statement]
        self.current_statement += 1
        self.log_callback(f"执行: {stmt}")

        # 根据语句类型执行相应操作
        if isinstance(stmt, ClearStatement):
            self._execute_clear()
        elif isinstance(stmt, InsertStatement):
            self._execute_insert(stmt)
        elif isinstance(stmt, DeleteStatement):
            self._execute_delete(stmt)
        elif isinstance(stmt, SearchStatement):
            self._execute_search(stmt)
        elif isinstance(stmt, InorderStatement):
            self._execute_inorder()
        elif isinstance(stmt, RandomStatement):
            self._execute_random(stmt)
        elif isinstance(stmt, PredecessorStatement):
            self._execute_predecessor(stmt)
        elif isinstance(stmt, SuccessorStatement):
            self._execute_successor(stmt)
        elif isinstance(stmt, LowerBoundStatement):
            self._execute_lower_bound(stmt)
        elif isinstance(stmt, DelayStatement):
            self._execute_delay(stmt)

    def _execute_clear(self):
        """执行清空操作"""
        self.tree.root = None
        self.log_callback("树已清空")
        self.update_ui_callback()
        QTimer.singleShot(500, self._execute_next)

    def _execute_insert(self, stmt: InsertStatement):
        """执行插入操作"""
        def step_callback(msg: str):
            self.log_callback(f"插入步骤: {msg}")
        
        self.tree.insert(stmt.value, step_callback)
        QTimer.singleShot(1000, self._execute_next)

    def _execute_delete(self, stmt: DeleteStatement):
        """执行删除操作"""
        def step_callback(msg: str):
            self.log_callback(f"删除步骤: {msg}")
        
        self.tree.delete(stmt.value, step_callback)
        QTimer.singleShot(1000, self._execute_next)

    def _execute_search(self, stmt: SearchStatement):
        """执行查找操作"""
        def step_callback(msg: str):
            self.log_callback(f"查找步骤: {msg}")
        
        node = self.tree.search(stmt.value, step_callback)
        result = "找到" if node else "未找到"
        self.log_callback(f"查找结果: {result} 值为 {stmt.value} 的节点")
        QTimer.singleShot(1000, self._execute_next)

    def _execute_inorder(self):
        """执行中序遍历"""
        result = self.tree.inorder()
        self.log_callback(f"中序遍历结果: {result}")
        self.update_ui_callback()
        QTimer.singleShot(1000, self._execute_next)

    def _execute_random(self, stmt: RandomStatement):
        """执行随机生成"""
        def step_callback(msg: str):
            self.log_callback(f"随机生成步骤: {msg}")
        
        values = self.tree.build_random(stmt.count, step_callback=step_callback)
        self.log_callback(f"随机生成节点值: {values}")
        QTimer.singleShot(1000, self._execute_next)

    def _execute_predecessor(self, stmt: PredecessorStatement):
        """执行查找前驱"""
        def step_callback(msg: str):
            self.log_callback(f"查找前驱步骤: {msg}")
        
        pred, _ = self.tree.predecessor(stmt.value, step_callback)
        result = f"前驱为 {pred.val}" if pred else "无前驱节点"
        self.log_callback(f"查找前驱结果: {result}")
        QTimer.singleShot(1000, self._execute_next)

    def _execute_successor(self, stmt: SuccessorStatement):
        """执行查找后继"""
        def step_callback(msg: str):
            self.log_callback(f"查找后继步骤: {msg}")
        
        succ, _ = self.tree.successor(stmt.value, step_callback)
        result = f"后继为 {succ.val}" if succ else "无后继节点"
        self.log_callback(f"查找后继结果: {result}")
        QTimer.singleShot(1000, self._execute_next)

    def _execute_lower_bound(self, stmt: LowerBoundStatement):
        """执行查找下界"""
        def step_callback(msg: str):
            self.log_callback(f"查找下界步骤: {msg}")
        
        lb, _ = self.tree.lower_bound(stmt.value, step_callback)
        result = f"首个≥{stmt.value}的节点是 {lb.val}" if lb else "无符合条件的节点"
        self.log_callback(f"查找下界结果: {result}")
        QTimer.singleShot(1000, self._execute_next)

    def _execute_delay(self, stmt: DelayStatement):
        """执行延迟操作"""
        self.log_callback(f"延迟 {stmt.milliseconds} 毫秒")
        QTimer.singleShot(stmt.milliseconds, self._execute_next)