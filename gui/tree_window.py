# gui/tree_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QCheckBox, QTextEdit,
    QSplitter  # 用于分割布局
)
from PySide6.QtCore import QTimer, Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import math
from core.binary_tree import BinaryTree
from gui.bst_window import BSTWindow
from dsl.binary_tree.binary_tree_dsl_parser import BinaryTreeDSLParser
from dsl.binary_tree.binary_tree_dsl_executor import BinaryTreeDSLExecutor


class TreeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二叉树链式存储结构可视化")
        self.resize(1200, 600)  # 加宽窗口以适应左侧DSL区域

        # 节点半径常量（统一控制节点大小）
        self.NODE_RADIUS = 0.40
        
        self.tree = BinaryTree()
        self.tree.add_listener(self.on_tree_update)

        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        # 主分割器：左右布局
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)

        # ---------------------- 左侧 DSL 面板 ----------------------
        dsl_widget = QWidget()
        dsl_layout = QVBoxLayout(dsl_widget)
        dsl_layout.setContentsMargins(10, 10, 10, 10)
        
        # DSL标题
        dsl_title = QLabel("<b>BinaryTree DSL 编辑器</b>")
        dsl_layout.addWidget(dsl_title)
        
        # DSL输入框
        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText("输入DSL脚本，例如：\nclear;\nbuild random n=7;\ninsert 42;")
        self.dsl_input.setFixedHeight(450)  # 固定高度400像素（核心设置）
        self.dsl_input.setMinimumWidth(300) # 最小宽度300像素
        dsl_layout.addWidget(self.dsl_input)
        
        # DSL操作按钮
        dsl_btn_layout = QHBoxLayout()
        
        self.btnClearDSL = QPushButton("清空DSL")
        self.btnClearDSL.clicked.connect(self.clear_dsl)
        dsl_btn_layout.addWidget(self.btnClearDSL)
        
        self.btnLoadExample = QPushButton("加载示例")
        self.btnLoadExample.clicked.connect(self.load_example_dsl)
        dsl_btn_layout.addWidget(self.btnLoadExample)
        
        self.btnRunDSL = QPushButton("执行DSL")
        self.btnRunDSL.clicked.connect(self.run_dsl)
        dsl_btn_layout.addWidget(self.btnRunDSL)
        
        dsl_layout.addLayout(dsl_btn_layout)
        
        # 填充空白
        dsl_layout.addStretch()
        
        # 将DSL面板添加到分割器左侧
        main_splitter.addWidget(dsl_widget)
        main_splitter.setSizes([350, 850])  # 设置左右面板宽度

        # ---------------------- 右侧 可视化面板 ----------------------
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # 画布
        layout.addWidget(self.canvas)

        # 控件区
        ctrl = QHBoxLayout()
        layout.addLayout(ctrl)

        self.btnBuild = QPushButton("随机构建")
        self.btnBuild.clicked.connect(self.build_random)
        ctrl.addWidget(self.btnBuild)

        # 完全二叉树勾选框
        self.cbComplete = QCheckBox("生成完全二叉树")
        ctrl.addWidget(self.cbComplete)

        # 节点数量输入框
        ctrl.addWidget(QLabel("节点数:"))
        self.spinNodeCount = QLineEdit("7")  # 默认7个节点
        self.spinNodeCount.setMaximumWidth(50)
        ctrl.addWidget(self.spinNodeCount)

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

        self.btnBST = QPushButton("切换到 BST 可视化")
        self.btnBST.clicked.connect(self.open_bst)
        ctrl.addWidget(self.btnBST)

        self.status = QLabel("就绪")
        layout.addWidget(self.status)

        # 将右侧面板添加到分割器
        main_splitter.addWidget(right_widget)

        # 初始化DSL相关
        self.dsl_parser = BinaryTreeDSLParser()
        self.dsl_executor = BinaryTreeDSLExecutor(self)

        # 存放绘图时节点 -> 坐标的映射（node_obj -> (x,y)）
        self.coords = {}

        # 动画相关
        self.highlight_index = 0
        self.order_nodes = []
        self.timer = QTimer()
        self.timer.timeout.connect(self._highlight_next)

        # 绑定鼠标点击事件（点击节点删除）
        self.canvas.mpl_connect('button_press_event', self.on_node_click)

        # 初始绘制空树
        self.draw_tree(None)

    # === 控件逻辑 ===
    def build_random(self):
        # 获取节点数量
        try:
            n = int(self.spinNodeCount.text())
            if n <= 0:
                QMessageBox.warning(self, "错误", "节点数必须为正数")
                return
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的节点数")
            return
            
        # 获取是否生成完全二叉树的勾选状态
        is_complete = self.cbComplete.isChecked()
        self.tree.build_random(n=n, is_complete=is_complete)
        if is_complete:
            self.status.setText(f"已生成 {n} 个节点的完全二叉树")
        else:
            self.status.setText(f"已生成 {n} 个节点的随机二叉树（子节点≤4）")

    def insert_node(self):
        try:
            val = int(self.inputVal.text())
        except:
            QMessageBox.warning(self, "错误", "请输入整数")
            return
        node = self.tree.insert(val)
        # 支持频率属性（兼容BST的freq字段）
        if hasattr(node, 'freq'):
            self.status.setText(f"插入节点 {val} (id={node.id}, 频率={node.freq})")
        else:
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

    # === DSL相关方法 ===
    def clear_dsl(self):
        """清空DSL输入框"""
        self.dsl_input.clear()
        self.status.setText("DSL编辑器已清空")

    def load_example_dsl(self):
        """加载示例DSL代码"""
        example_code = """clear;

build random n=7;

insert 42;
insert 18;

traverse inorder;

draw;"""
        self.dsl_input.setPlainText(example_code)
        self.status.setText("已加载DSL示例代码")

    # === 交互事件 ===
    def on_node_click(self, event):
        """点击节点触发删除确认"""
        if event.inaxes != self.ax:
            return
        
        # 查找点击位置附近的节点
        clicked_node = None
        for node, (x, y) in self.coords.items():
            # 计算点击位置与节点中心的距离
            if math.hypot(event.xdata - x, event.ydata - y) <= self.NODE_RADIUS:
                clicked_node = node
                break
        
        if clicked_node:
            # 显示删除确认对话框
            node_text = f"{clicked_node.val}"
            if hasattr(clicked_node, 'freq') and clicked_node.freq > 1:
                node_text = f"{clicked_node.val}-{clicked_node.freq}"
            
            reply = QMessageBox.question(
                self, 
                "删除节点", 
                f"确定要删除节点 {node_text} (id={clicked_node.id}) 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 执行删除操作
                self.tree.delete_node(clicked_node)
                self.status.setText(f"已删除节点 {clicked_node.val} (id={clicked_node.id})")

    # === 监听与绘制 ===
    def on_tree_update(self, state):
        # state["node"] 是最近插入的节点对象（如果有）
        self.draw_tree(state["tree"], highlight_node=state.get("node"))

    def draw_tree(self, node, highlight_node=None):
        """
        优化后的绘制逻辑，参考BST绘制流程：
        1. 初始化绘制环境
        2. 递归计算节点坐标
        3. 绘制节点连线（底层，zorder=1）
        4. 绘制节点圆圈（中层，zorder=3）
        5. 绘制节点文本（顶层，zorder=5）
        6. 调整画布范围和比例
        7. 刷新画布
        """
        # 1. 初始化绘制环境
        self.ax.clear()
        self.coords = {}
        
        # 空树处理
        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.ax.axis("off")
            self.canvas.draw_idle()
            return

        # 2. 递归计算节点坐标（深度优先）
        def layout(n, x, depth, span):
            """
            递归分配节点坐标：
            - n: 当前节点
            - x: 当前X坐标
            - depth: 当前深度（Y坐标为-depth）
            - span: 子树水平跨度
            """
            if n is None:
                return
            # 存储节点坐标
            self.coords[n] = (x, -depth)
            # 子节点跨度减半
            child_span = span / 2.0
            # 递归处理左右子树
            if n.left:
                layout(n.left, x - child_span, depth + 1, child_span)
            if n.right:
                layout(n.right, x + child_span, depth + 1, child_span)

        # 根节点初始参数：x=0，depth=0，初始span=8
        max_depth = self._compute_depth(node)
        initial_span = max(8, (2 ** (max_depth - 1)) * 0.8)  # 优化初始跨度
        layout(node, 0.0, 0, initial_span)

        # 3. 绘制节点间连线（底层，zorder=1）
        for n, (x, y) in self.coords.items():
            # 绘制左子树连线
            if n.left and n.left in self.coords:
                x2, y2 = self.coords[n.left]
                # 计算连线端点（避开节点圆心，从边缘出发）
                dx = x2 - x
                dy = y2 - y
                distance = math.hypot(dx, dy)
                if distance > 0:
                    # 起点：父节点边缘
                    start_x = x + (dx / distance) * self.NODE_RADIUS
                    start_y = y + (dy / distance) * self.NODE_RADIUS
                    # 终点：子节点边缘
                    end_x = x2 - (dx / distance) * self.NODE_RADIUS
                    end_y = y2 - (dy / distance) * self.NODE_RADIUS
                    # 绘制连线（黑色，zorder=1确保在节点下方）
                    self.ax.plot([start_x, end_x], [start_y, end_y], 'k-', zorder=1)
            
            # 绘制右子树连线
            if n.right and n.right in self.coords:
                x2, y2 = self.coords[n.right]
                # 计算连线端点（避开节点圆心）
                dx = x2 - x
                dy = y2 - y
                distance = math.hypot(dx, dy)
                if distance > 0:
                    start_x = x + (dx / distance) * self.NODE_RADIUS
                    start_y = y + (dy / distance) * self.NODE_RADIUS
                    end_x = x2 - (dx / distance) * self.NODE_RADIUS
                    end_y = y2 - (dy / distance) * self.NODE_RADIUS
                    self.ax.plot([start_x, end_x], [start_y, end_y], 'k-', zorder=1)

        # 4. 绘制节点圆圈（中层，zorder=3）
        for n, (x, y) in self.coords.items():
            # 确定节点样式
            if highlight_node is not None and n is highlight_node:
                # 高亮节点：红色，粗边框
                face_color = "#FF6347"
                edge_color = "black"
                line_width = 2.0
            else:
                # 普通节点：浅蓝色，细边框
                face_color = "#87CEFA"
                edge_color = "black"
                line_width = 1.0
            
            # 绘制圆形节点（zorder=3确保在连线上方）
            circ = patches.Circle(
                (x, y), 
                self.NODE_RADIUS, 
                facecolor=face_color,
                edgecolor=edge_color,
                linewidth=line_width,
                zorder=3
            )
            self.ax.add_patch(circ)

        # 5. 绘制节点文本（顶层，zorder=5）
        for n, (x, y) in self.coords.items():
            # 构建节点文本（支持频率显示）
            if hasattr(n, 'freq') and n.freq > 1:
                label = f"{n.val}-{n.freq}\n(id:{n.id})"
            else:
                label = f"{n.val}\n(id:{n.id})"
            
            # 绘制文本（zorder=5确保在节点上方）
            self.ax.text(
                x, y, label, 
                ha='center', va='center', 
                fontsize=9, 
                zorder=5
            )

        # 6. 调整画布范围与比例
        # 收集所有节点坐标
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        
        if xs and ys:
            # 计算边界（添加1.5的边距）
            xmin, xmax = min(xs) - 1.5, max(xs) + 1.5
            ymin, ymax = min(ys) - 1.5, max(ys) + 1.5
            
            # 设置坐标轴范围
            self.ax.set_xlim(xmin, xmax)
            self.ax.set_ylim(ymin, ymax)
            
            # 设置等比例显示，避免树结构变形
            self.ax.set_aspect('equal', adjustable='box')
        
        # 隐藏坐标轴
        self.ax.axis("off")

        # 7. 刷新画布
        self.canvas.draw_idle()

    def _compute_depth(self, root):
        """计算树的最大深度（层数）"""
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
    
    def open_bst(self):
        """打开BST可视化窗口"""
        self.bst = BSTWindow()
        self.bst.show()
        
    def run_dsl(self):
        """执行DSL脚本"""
        script = self.dsl_input.toPlainText()
        try:
            ast = self.dsl_parser.parse(script)
            self.dsl_executor.execute(ast)
            self.status.setText("DSL 执行完成")
        except Exception as e:
            QMessageBox.critical(self, "DSL 错误", str(e))
            self.status.setText("DSL 执行失败")