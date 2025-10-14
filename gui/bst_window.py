# gui/bst_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QSpinBox
)
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
from core.bst_tree import BSTree


class BSTWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二叉搜索树（BST）可视化 - 支持多集合与随机生成")
        self.resize(1000, 650)

        # ========== 数据部分 ==========
        self.tree = BSTree()
        self.tree.add_listener(self.on_update)

        # ========== 图形绘制 ==========
        self.fig = Figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        # ========== 界面布局 ==========
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.addWidget(self.canvas)

        ctrl = QHBoxLayout()
        layout.addLayout(ctrl)

        # ---- 输入框与操作按钮 ----
        self.inputVal = QLineEdit()
        self.inputVal.setPlaceholderText("输入整数")
        ctrl.addWidget(self.inputVal)

        self.btnInsert = QPushButton("插入")
        self.btnInsert.clicked.connect(self.insert)
        ctrl.addWidget(self.btnInsert)

        self.btnSearch = QPushButton("查找")
        self.btnSearch.clicked.connect(self.search)
        ctrl.addWidget(self.btnSearch)

        self.btnDelete = QPushButton("删除")
        self.btnDelete.clicked.connect(self.delete)
        ctrl.addWidget(self.btnDelete)

        self.btnInorder = QPushButton("中序遍历")
        self.btnInorder.clicked.connect(self.show_inorder)
        ctrl.addWidget(self.btnInorder)

        # ---- 随机生成 BST ----
        ctrl.addWidget(QLabel("随机节点数:"))
        self.spinN = QSpinBox()
        self.spinN.setRange(1, 50)
        self.spinN.setValue(10)
        ctrl.addWidget(self.spinN)

        self.btnRandom = QPushButton("随机生成 BST")
        self.btnRandom.clicked.connect(self.random_build)
        ctrl.addWidget(self.btnRandom)

        # 状态栏
        self.status = QLabel("就绪")
        layout.addWidget(self.status)

        # 动画定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_path)
        self.path_nodes = []
        self.path_index = 0

        self.coords = {}
        self.draw_tree(None)

    # ========== 基础操作 ==========
    def insert(self):
        try:
            val = int(self.inputVal.text())
        except:
            QMessageBox.warning(self, "错误", "请输入整数")
            return
        self.tree.insert(val)

    def search(self):
        try:
            val = int(self.inputVal.text())
        except:
            QMessageBox.warning(self, "错误", "请输入整数")
            return
        self.tree.search(val)

    def delete(self):
        try:
            val = int(self.inputVal.text())
        except:
            QMessageBox.warning(self, "错误", "请输入整数")
            return
        self.tree.delete(val)

    def show_inorder(self):
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        seq = self.tree.inorder()
        self.status.setText(f"中序遍历序列（考虑频率）: {seq}")

    def random_build(self):
        """随机生成 BST"""
        n = self.spinN.value()
        values = self.tree.build_random(n=n, value_range=(0, 100))
        self.status.setText(f"随机生成 {n} 个节点: {values}")

    # ========== 动画逻辑 ==========
    def _animate_path(self):
        if self.path_index >= len(self.path_nodes):
            self.timer.stop()
            self.draw_tree(self.tree.root)
            return
        node = self.path_nodes[self.path_index]
        self.draw_tree(self.tree.root, highlight=node)
        self.path_index += 1

    # ========== 数据更新回调 ==========
    def on_update(self, state):
        action = state.get("action")
        node = state.get("node")
        extra = state.get("extra") or []

        if extra and isinstance(extra, list):
            # 若 extra 为节点路径，则动画显示
            if all(hasattr(x, "val") for x in extra):
                self.path_nodes = extra
                self.path_index = 0
                self.timer.start(450)

        # 更新状态栏并绘制
        if action == "insert":
            self.status.setText(f"插入节点 {node.val}")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "increase_freq":
            self.status.setText(f"节点 {node.val} 频率 +1 -> {node.freq}")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "decrease_freq":
            self.status.setText(f"节点 {node.val} 频率 -1 -> {node.freq}")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "delete":
            self.status.setText(f"删除节点 {node.val if node else '?'}")
            self.draw_tree(self.tree.root)
        elif action == "found":
            self.status.setText(f"查找成功：{node.val} (freq={getattr(node,'freq',1)})")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "not_found":
            self.status.setText("查找失败")
            self.draw_tree(self.tree.root)
        elif action == "build":
            self.status.setText("随机生成 BST 完成")
            self.draw_tree(self.tree.root)

    # ========== 绘制 ==========
    def draw_tree(self, node, highlight=None):
        self.ax.clear()
        self.coords = {}
        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return

        # 计算布局
        max_depth = self._compute_depth(node)
        def layout(n, x, depth, span):
            if not n:
                return
            self.coords[n] = (x, -depth)
            gap = span / 2
            layout(n.left, x - gap, depth + 1, gap)
            layout(n.right, x + gap, depth + 1, gap)

        layout(node, 0, 0, 8)

        # 连线
        for n, (x, y) in self.coords.items():
            if n.left:
                x2, y2 = self.coords[n.left]
                self.ax.plot([x, x2], [y, y2], "k-")
            if n.right:
                x2, y2 = self.coords[n.right]
                self.ax.plot([x, x2], [y, y2], "k-")

        # 节点
        for n, (x, y) in self.coords.items():
            color = "#FF6347" if highlight is n else "#87CEFA"
            lw = 2 if highlight is n else 1
            circ = patches.Circle((x, y), 0.28, facecolor=color, edgecolor="black", linewidth=lw)
            self.ax.add_patch(circ)
            label = f"{n.val}" if n.freq == 1 else f"{n.val}-{n.freq}"
            self.ax.text(x, y, label, ha="center", va="center", fontsize=9)

        self.ax.axis("off")
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 1, max(xs) + 1)
            self.ax.set_ylim(min(ys) - 1, max(ys) + 1)
        self.canvas.draw_idle()

    def _compute_depth(self, root):
        if not root:
            return 0
        q = [(root, 1)]
        maxd = 1
        for n, d in q:
            maxd = max(maxd, d)
            if n.left:
                q.append((n.left, d + 1))
            if n.right:
                q.append((n.right, d + 1))
        return maxd
