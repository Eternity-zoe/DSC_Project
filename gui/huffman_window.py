
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QTextEdit, QMessageBox)
from PySide6.QtCore import QTimer, QDateTime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
# from huffman_tree import HuffmanTree, HuffmanNode# 在 huffman_window.py 中
from core.huffman_tree import HuffmanTree, HuffmanNode  # 正确的导入路径

class HuffmanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("哈夫曼树可视化")
        self.resize(1200, 700)
        
        # 初始化哈夫曼树
        self.tree = HuffmanTree()
        self.tree.add_listener(self.on_update)
        
        # 图形相关
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标
        
        # 动画相关
        self.build_steps = []
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_build)
        
        # 编码显示区域
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setPlaceholderText("哈夫曼编码将显示在这里...")
        
        # 主布局
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # 左侧：树图和控件
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        main_layout.addWidget(left_panel, 7)
        main_layout.addWidget(self.code_display, 3)
        
        # 控件区
        ctrl = QHBoxLayout()
        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("输入文本内容（用于构建哈夫曼树）")
        ctrl.addWidget(self.input_text)
        
        self.btn_build = QPushButton("构建哈夫曼树")
        self.btn_build.clicked.connect(self.build_huffman)
        ctrl.addWidget(self.btn_build)
        
        self.btn_clear = QPushButton("清空")
        self.btn_clear.clicked.connect(self.clear)
        ctrl.addWidget(self.btn_clear)
        
        # 组装左侧布局
        left_layout.addWidget(self.canvas)
        left_layout.addLayout(ctrl)
        
        self.status = QLabel("就绪 - 请输入文本构建哈夫曼树")
        left_layout.addWidget(self.status)
        
        self.draw_tree(None)
        
    def build_huffman(self):
        text = self.input_text.text().strip()
        if not text:
            QMessageBox.warning(self, "输入错误", "请输入文本内容")
            return
            
        self.status.setText(f"正在构建哈夫曼树...")
        self.tree.build(text)
        
    def clear(self):
        self.input_text.clear()
        self.code_display.clear()
        self.tree = HuffmanTree()
        self.tree.add_listener(self.on_update)
        self.draw_tree(None)
        self.status.setText("已清空")
        
    def on_update(self, state):
        action = state.get("action")
        if action == "build":
            self.root = state.get("tree")
            extra = state.get("extra", {})
            self.build_steps = extra.get("steps", [])
            self.code_map = extra.get("code_map", {})
            
            # 显示编码
            code_text = "哈夫曼编码表：\n"
            for char, code in self.code_map.items():
                code_text += f"'{char}' -> {code}\n"
            self.code_display.setText(code_text)
            
            # 开始构建动画
            self.step_index = 0
            self.timer.start(1000)
            self.status.setText("哈夫曼树构建完成，正在播放构建动画")
        
    def _animate_build(self):
        if self.step_index < len(self.build_steps):
            left, right, merged = self.build_steps[self.step_index]
            # 绘制当前合并步骤
            self._draw_build_step(left, right, merged)
            self.step_index += 1
        else:
            self.timer.stop()
            self.draw_tree(self.root)
            self.status.setText(f"哈夫曼树构建完成（共 {len(self.build_steps)} 步合并）")
        
    def _draw_build_step(self, left, right, merged):
        """绘制合并步骤"""
        self.ax.clear()
        self.coords = {}
        
        # 简单布局
        self.coords[left] = (-1, 0)
        self.coords[right] = (1, 0)
        self.coords[merged] = (0, 1)
        
        # 绘制连接线
        lx, ly = self.coords[left]
        rx, ry = self.coords[right]
        mx, my = self.coords[merged]
        self.ax.plot([lx, mx], [ly, my], 'k-')
        self.ax.plot([rx, mx], [ry, my], 'k-')
        
        # 标记0和1
        self.ax.text((lx + mx)/2, (ly + my)/2, "0", fontsize=12, color='blue')
        self.ax.text((rx + mx)/2, (ry + my)/2, "1", fontsize=12, color='blue')
        
        # 绘制节点
        for node, (x, y) in self.coords.items():
            color = "#87CEFA" if node.char is None else "#90EE90"
            circ = patches.Circle((x, y), 0.3, facecolor=color, edgecolor='black')
            self.ax.add_patch(circ)
            label = f"{node.freq}"
            if node.char is not None:
                label += f"\n'{node.char}'"
            self.ax.text(x, y, label, ha='center', va='center', fontsize=9)
            
        self.ax.axis('off')
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-0.5, 2)
        self.canvas.draw_idle()
        
    def draw_tree(self, root):
        """绘制完整哈夫曼树，带0/1标记"""
        self.ax.clear()
        self.coords = {}
        
        if not root:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return
            
        # 递归布局
        def layout(node, x, depth, span):
            if not node:
                return
            self.coords[node] = (x, -depth)
            child_span = span / 2
            if node.left:
                layout(node.left, x - child_span, depth + 1, child_span)
            if node.right:
                layout(node.right, x + child_span, depth + 1, child_span)
                
        max_depth = self._compute_depth(root)
        layout(root, 0, 0, max(4, 2 **(max_depth - 1)))
        
        # 绘制连接线和0/1标记
        for node, (x, y) in self.coords.items():
            if node.left and node.left in self.coords:
                x2, y2 = self.coords[node.left]
                self.ax.plot([x, x2], [y, y2], 'k-')
                # 标记0
                self.ax.text((x + x2)/2, (y + y2)/2, "0", 
                           fontsize=10, color='blue', weight='bold')
            if node.right and node.right in self.coords:
                x2, y2 = self.coords[node.right]
                self.ax.plot([x, x2], [y, y2], 'k-')
                # 标记1
                self.ax.text((x + x2)/2, (y + y2)/2, "1", 
                           fontsize=10, color='blue', weight='bold')
        
        # 绘制节点
        for node, (x, y) in self.coords.items():
            # 叶子节点用不同颜色
            color = "#87CEFA" if node.char is None else "#90EE90"
            circ = patches.Circle((x, y), 0.3, facecolor=color, edgecolor='black')
            self.ax.add_patch(circ)
            label = f"{node.freq}"
            if node.char is not None:
                label += f"\n'{node.char}'"
                # 显示编码
                if node.code:
                    label += f"\n{node.code}"
            self.ax.text(x, y, label, ha='center', va='center', fontsize=8)
            
        self.ax.axis('off')
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 1, max(xs) + 1)
            self.ax.set_ylim(min(ys) - 1, max(ys) + 1)
        self.canvas.draw_idle()
        
    def _compute_depth(self, root):
        if not root:
            return 0
        return 1 + max(self._compute_depth(root.left), self._compute_depth(root.right))