from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel, QTextEdit, QMessageBox)
from PySide6.QtCore import QTimer, QDateTime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
# from huffman_tree import HuffmanTree, HuffmanNode# 在 huffman_window.py 中
from core.huffman_tree import HuffmanTree, HuffmanNode  # 正确的导入路径
from dsl.huffman.huffman_dsl_parser import HuffmanDSLParser
from dsl.huffman.huffman_dsl_executor import HuffmanDSLExecutor
NODE_RADIUS = 0.3
MIN_NODE_SIZE_INCH = 0.5  # 节点直径最小0.5英寸（约1.27cm）
NODE_RADIUS = MIN_NODE_SIZE_INCH / 2  # 节点半径（基于最小尺寸）
TEXT_PADDING = 0.1  # 文本与节点边缘的间距（英寸）


class HuffmanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("哈夫曼树可视化")
        self.resize(1400, 800)  # 适当增大窗口尺寸，适配三栏布局
        
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
        
        # 主布局 - 三栏布局：左(DSL)、中(树图+控件)、右(编码记录)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 左侧：DSL面板
        self._init_dsl_panel()
        main_layout.addWidget(self.dsl_panel, 2)  # 占比2
        
        # 2. 中间：树图和控件
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setSpacing(8)
        main_layout.addWidget(middle_panel, 7)  # 占比7
        
        # 控件区（放在树图上方）
        ctrl_layout = QHBoxLayout()
        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("输入文本内容（用于构建哈夫曼树）")
        ctrl_layout.addWidget(self.input_text)
        
        self.btn_build = QPushButton("构建哈夫曼树")
        self.btn_build.clicked.connect(self.build_huffman)
        ctrl_layout.addWidget(self.btn_build)
        
        self.btn_clear = QPushButton("清空")
        self.btn_clear.clicked.connect(self.clear)
        ctrl_layout.addWidget(self.btn_clear)

        self.btn_save = QPushButton("保存哈夫曼树")
        self.btn_save.clicked.connect(self.save_tree)
        ctrl_layout.addWidget(self.btn_save)

        self.btn_load = QPushButton("加载哈夫曼树")
        self.btn_load.clicked.connect(self.load_tree)
        ctrl_layout.addWidget(self.btn_load)
        
        # 添加控件区到中间面板
        middle_layout.addLayout(ctrl_layout)
        
        # 树图画布（中间面板的主要部分）
        middle_layout.addWidget(self.canvas, stretch=1)  # 拉伸填充剩余空间
        
        # 状态标签
        self.status = QLabel("就绪 - 请输入文本构建哈夫曼树")
        middle_layout.addWidget(self.status)
        
        # 3. 右侧：编码记录区域
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(right_panel, 3)  # 占比3
        
        # 右侧标题
        code_title = QLabel("哈夫曼编码记录")
        code_title.setStyleSheet("font-weight:bold;font-size:14px;padding:5px;")
        right_layout.addWidget(code_title)
        
        # 编码显示区域
        right_layout.addWidget(self.code_display)
        
        # 初始化DSL解析器和执行器
        self.dsl_parser = HuffmanDSLParser()
        self.dsl_executor = HuffmanDSLExecutor(self)

        # 初始绘制空树
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
        
    def _compute_depth(self, node):
        """辅助函数：计算树的最大深度"""
        if not node:
            return 0
        return 1 + max(self._compute_depth(node.left), self._compute_depth(node.right))

    def _draw_build_step(self, left, right, merged):
        """
        绘制哈夫曼树合并步骤 (调整为圆形节点样式)
        核心优化：固定节点物理尺寸，精准控制画布范围
        """
        self.ax.clear()
        self.coords = {}
        
        # 简单布局（物理坐标，单位：英寸）
        self.coords[left] = (-1, 0)
        self.coords[right] = (1, 0)
        self.coords[merged] = (0, 1)
        
        # 绘制连接线 (Zorder 确保线在节点下方)
        lx, ly = self.coords[left]
        rx, ry = self.coords[right]
        mx, my = self.coords[merged]
        self.ax.plot([lx, mx], [ly, my], 'k-', zorder=1)
        self.ax.plot([rx, mx], [ry, my], 'k-', zorder=1) 
        
        # 标记0和1（固定字体大小，不受画布缩放影响）
        self.ax.text((lx + mx)/2 - 0.1, (ly + my)/2, "0", 
                    fontsize=12, color='blue', weight='bold', zorder=2)
        self.ax.text((rx + mx)/2 + 0.1, (ry + my)/2, "1", 
                    fontsize=12, color='blue', weight='bold', zorder=2)
        
        # 绘制节点（固定物理尺寸，确保最小大小）
        for node, (x, y) in self.coords.items():
            color = "#87CEFA" if node.char is None else "#90EE90"
            # 固定半径的圆形（物理尺寸，不受画布缩放影响）
            circ = patches.Circle((x, y), NODE_RADIUS, 
                                facecolor=color, edgecolor='black', linewidth=1, zorder=3)
            self.ax.add_patch(circ)
            
            # 文本内容：频率和字符（居中，固定字体大小）
            label = f"{node.freq}"
            if node.char is not None:
                label += f"\n'{node.char}'"
            self.ax.text(x, y, label, ha='center', va='center', fontsize=9, zorder=5)
            
        self.ax.axis('off')
        
        # 精准控制画布范围（仅保留必要留白，压缩无效空间）
        x_min = min(lx, rx, mx) - NODE_RADIUS - TEXT_PADDING
        x_max = max(lx, rx, mx) + NODE_RADIUS + TEXT_PADDING
        y_min = min(ly, ry, my) - NODE_RADIUS - TEXT_PADDING
        y_max = max(ly, ry, my) + NODE_RADIUS + TEXT_PADDING
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_aspect('equal')  # 确保圆形不失真
        
        # 强制设置画布物理尺寸匹配内容（关键：避免缩放导致节点变小）
        self.fig.set_size_inches(x_max - x_min, y_max - y_min, forward=True)
        self.canvas.draw_idle()

    def draw_tree(self, root):
        """
        绘制完整哈夫曼树，带0/1标记
        核心优化：固定节点物理尺寸 + 优化布局间距 + 精准画布范围
        """
        self.ax.clear()
        self.coords = {}
        
        if not root:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.ax.axis('off')
            self.canvas.draw_idle()
            return
            
        # 递归布局（优化间距：基于节点物理尺寸计算，避免过挤/过松）
        def layout(node, x, depth, span):
            if not node:
                return
            self.coords[node] = (x, -depth)
            # 子节点间距 = 节点直径 + 最小间隙（确保节点不重叠）
            child_span = max(MIN_NODE_SIZE_INCH * 2, span / 2)
            if node.left:
                layout(node.left, x - child_span, depth + 1, child_span)
            if node.right:
                layout(node.right, x + child_span, depth + 1, child_span)
                
        max_depth = self._compute_depth(root)
        # 初始跨度：基于树深度 + 节点物理尺寸，避免底层节点过挤
        initial_span = max(MIN_NODE_SIZE_INCH * 3, 2 **(max_depth // 2))
        layout(root, 0, 0, initial_span)
        
        # 绘制连接线和0/1标记
        for node, (x, y) in self.coords.items():
            # 左子节点（0）
            if node.left and node.left in self.coords:
                x2, y2 = self.coords[node.left]
                self.ax.plot([x, x2], [y, y2], 'k-', zorder=1)
                # 标记0（居中，固定字体大小）
                self.ax.text((x + x2)/2, (y + y2)/2, "0", 
                            fontsize=10, color='blue', weight='bold', zorder=2)
            # 右子节点（1）
            if node.right and node.right in self.coords:
                x2, y2 = self.coords[node.right]
                self.ax.plot([x, x2], [y, y2], 'k-', zorder=1)
                # 标记1（居中，固定字体大小）
                self.ax.text((x + x2)/2, (y + y2)/2, "1", 
                            fontsize=10, color='blue', weight='bold', zorder=2)
        
        # 绘制节点（固定物理尺寸，确保最小大小）
        xs = []
        ys = []
        for node, (x, y) in self.coords.items():
            xs.append(x)
            ys.append(y)
            # 叶子节点/非叶子节点颜色区分
            color = "#87CEFA" if node.char is None else "#90EE90"
            # 固定半径的圆形（物理尺寸）
            circ = patches.Circle((x, y), NODE_RADIUS, 
                                facecolor=color, edgecolor='black', linewidth=1, zorder=3)
            self.ax.add_patch(circ)
            
            # 文本内容：频率、字符、编码（居中，固定字体大小）
            label = f"{node.freq}"
            if node.char is not None:
                label += f"\n'{node.char}'"
                if hasattr(node, 'code') and node.code:
                    label += f"\n{node.code}"
            self.ax.text(x, y, label, ha='center', va='center', fontsize=8, zorder=5)
            
        self.ax.axis('off')
        
        # 精准控制画布范围（仅保留必要留白，压缩上下无效空间）
        if xs and ys:
            x_min = min(xs) - NODE_RADIUS - TEXT_PADDING
            x_max = max(xs) + NODE_RADIUS + TEXT_PADDING
            y_min = min(ys) - NODE_RADIUS - TEXT_PADDING
            y_max = max(ys) + NODE_RADIUS + TEXT_PADDING
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            self.ax.set_aspect('equal')  # 确保圆形不失真
            
            # 强制画布物理尺寸匹配内容（核心：避免缩放导致节点变小）
            self.fig.set_size_inches(
                x_max - x_min, 
                y_max - y_min, 
                forward=True
            )
        
        self.canvas.draw_idle()

    def _compute_depth(self, root):
        if not root:
            return 0
        return 1 + max(self._compute_depth(root.left), self._compute_depth(root.right))
    
    def save_tree(self):
        from PySide6.QtWidgets import QFileDialog
        if not self.tree.root:
            QMessageBox.information(self, "提示", "当前哈夫曼树为空")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "保存哈夫曼树", "", "JSON 文件 (*.json)"
        )
        if path:
            self.tree.save_to_file(path)
            QMessageBox.information(self, "成功", "哈夫曼树保存成功")

    def load_tree(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "加载哈夫曼树", "", "JSON 文件 (*.json)"
        )
        if path:
            self.tree.load_from_file(path)
            self.draw_tree(self.tree.root)
            QMessageBox.information(self, "成功", "哈夫曼树加载完成")

    def _init_dsl_panel(self):
        self.dsl_panel = QWidget()
        layout = QVBoxLayout(self.dsl_panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        title = QLabel("DSL 绘制模块（Huffman）")
        title.setStyleSheet("font-weight:bold;font-size:14px;padding:5px;")
        layout.addWidget(title)

        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText(
            """示例：
clear MyHuff;
build MyHuff text="abbccc";
draw MyHuff;
show_codes MyHuff;
"""
        )
        # 设置DSL输入框的最小高度
        self.dsl_input.setMinimumHeight(300)
        layout.addWidget(self.dsl_input, stretch=1)

        btns = QHBoxLayout()
        self.btn_exec_dsl = QPushButton("执行 DSL")
        self.btn_exec_dsl.clicked.connect(self.execute_dsl)

        self.btn_clear_dsl = QPushButton("清空")
        self.btn_clear_dsl.clicked.connect(self.dsl_input.clear)

        btns.addWidget(self.btn_exec_dsl)
        btns.addWidget(self.btn_clear_dsl)
        layout.addLayout(btns)

    def execute_dsl(self):
        script = self.dsl_input.toPlainText().strip()
        if not script:
            QMessageBox.warning(self, "警告", "请输入DSL脚本内容")
            return

        try:
            ast = self.dsl_parser.parse(script)
            self.dsl_executor.execute_ast(ast)
            self.status.setText("DSL 执行完成")
            QMessageBox.information(self, "成功", "DSL脚本执行成功")
        except Exception as e:
            QMessageBox.critical(self, "DSL 执行错误", str(e))