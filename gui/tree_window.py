# gui/tree_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import math
from core.binary_tree import BinaryTree

class TreeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二叉树链式存储结构可视化")
        self.resize(950, 600)

        self.tree = BinaryTree()
        self.tree.add_listener(self.on_tree_update)

        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.addWidget(self.canvas)

        # 控件区
        ctrl = QHBoxLayout()
        layout.addLayout(ctrl)

        self.btnBuild = QPushButton("随机构建")
        self.btnBuild.clicked.connect(self.build_random)
        ctrl.addWidget(self.btnBuild)

        self.inputVal = QLineEdit(); self.inputVal.setPlaceholderText("节点值")
        ctrl.addWidget(self.inputVal)
        self.btnInsert = QPushButton("插入节点")
        self.btnInsert.clicked.connect(self.insert_node)
        ctrl.addWidget(self.btnInsert)

        self.btnPre = QPushButton("前序遍历")
        self.btnPre.clicked.connect(lambda: self.traverse("pre"))
        ctrl.addWidget(self.btnPre)

        self.btnIn = QPushButton("中序遍历")
        self.btnIn.clicked.connect(lambda: self.traverse("in"))
        ctrl.addWidget(self.btnIn)

        self.btnPost = QPushButton("后序遍历")
        self.btnPost.clicked.connect(lambda: self.traverse("post"))
        ctrl.addWidget(self.btnPost)

        self.status = QLabel("就绪")
        layout.addWidget(self.status)

        # 存放绘图时节点 -> 坐标的映射（node_obj -> (x,y)）
        self.coords = {}

        # 动画相关
        self.highlight_index = 0
        self.order_nodes = []
        self.timer = QTimer()
        self.timer.timeout.connect(self._highlight_next)

        self.draw_tree(None)

    # === 控件逻辑 ===
    def build_random(self):
        self.tree.build_random()
        self.status.setText("已随机生成二叉树")

    def insert_node(self):
        try:
            val = int(self.inputVal.text())
        except:
            QMessageBox.warning(self, "错误", "请输入整数")
            return
        node = self.tree.insert(val)
        self.status.setText(f"插入节点 {val} (id={node.id})")

    def traverse(self, mode):
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        if mode == "pre":
            nodes = self.tree.preorder_nodes()
            txt = [n.val for n in nodes]
            self.status.setText(f"前序遍历值序列: {txt}")
        elif mode == "in":
            nodes = self.tree.inorder_nodes()
            txt = [n.val for n in nodes]
            self.status.setText(f"中序遍历值序列: {txt}")
        else:
            nodes = self.tree.postorder_nodes()
            txt = [n.val for n in nodes]
            self.status.setText(f"后序遍历值序列: {txt}")

        # 动画：按节点对象逐个高亮（只高亮单一节点）
        self.order_nodes = nodes
        self.highlight_index = 0
        self.timer.start(600)  # 每 600ms 高亮下一个

    def _highlight_next(self):
        if self.highlight_index >= len(self.order_nodes):
            self.timer.stop()
            # 绘回常态（无高亮）
            self.draw_tree(self.tree.root)
            return
        node = self.order_nodes[self.highlight_index]
        self.draw_tree(self.tree.root, highlight_node=node)
        self.highlight_index += 1

    # === 监听与绘制 ===
    def on_tree_update(self, state):
        # state["node"] 是最近插入的节点对象（如果有）
        self.draw_tree(state["tree"], highlight_node=state.get("node"))

    def draw_tree(self, node, highlight_node=None):
        """
        计算布局并绘制。重要：在布局时保存 self.coords[node] = (x,y)
        highlight_node 必须是节点对象（TreeNode），按对象精确匹配高亮单个结点。
        """
        self.ax.clear()
        self.coords = {}
        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return

        # 递归布局：给每个节点一个 x,y（y 为 -depth）
        def layout(n, x, depth, span):
            """span 决定子树左右可用寬度"""
            if n is None:
                return
            self.coords[n] = (x, -depth)
            # 左右跨度减半
            child_span = span / 2.0
            if n.left:
                layout(n.left, x - child_span, depth + 1, child_span)
            if n.right:
                layout(n.right, x + child_span, depth + 1, child_span)

        # 初始 span 与根 x=0
        max_depth = self._compute_depth(node)
        # span 根据深度动态设置，使整棵树不拥挤
        initial_span = max(1.5, (2 ** (max_depth - 1)))
        layout(node, 0.0, 0, initial_span)

        # 画边 (父->子)
        for n, (x, y) in self.coords.items():
            if n.left and n.left in self.coords:
                x2, y2 = self.coords[n.left]
                self.ax.plot([x, x2], [y, y2], 'k-')
            if n.right and n.right in self.coords:
                x2, y2 = self.coords[n.right]
                self.ax.plot([x, x2], [y, y2], 'k-')

        # 画节点：若节点等于 highlight_node 则单独高亮
        for n, (x, y) in self.coords.items():
            color = "#87CEFA"
            edge = "black"
            lw = 1.0
            if highlight_node is not None and n is highlight_node:
                color = "#FF6347"
                lw = 2.5
            circ = patches.Circle((x, y), 0.25, facecolor=color, edgecolor=edge, linewidth=lw)
            self.ax.add_patch(circ)
            label = f"{n.val}\n(id:{n.id})"
            self.ax.text(x, y, label, ha='center', va='center', fontsize=8)

        self.ax.axis('off')
        # 根据 coords 动态确定 xlim, ylim
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        if xs and ys:
            xmin, xmax = min(xs) - 0.6, max(xs) + 0.6
            ymin, ymax = min(ys) - 0.6, max(ys) + 0.6
            self.ax.set_xlim(xmin, xmax)
            self.ax.set_ylim(ymin, ymax)
        self.canvas.draw_idle()

    def _compute_depth(self, root):
        # 计算最大深度（层数），用于初始 span 估计
        if not root:
            return 0
        q = [(root, 1)]
        maxd = 1
        for n, d in q:
            maxd = max(maxd, d)
            if n.left:
                q.append((n.left, d+1))
            if n.right:
                q.append((n.right, d+1))
        return maxd
