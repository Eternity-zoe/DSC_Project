# gui/avl_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QSpinBox, QTextEdit, QFileDialog
)
from PySide6.QtCore import QTimer, QDateTime, QIODevice, QTextStream
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
from core.avl_tree import AVLTree

class AVLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVL树可视化 - 自平衡二叉搜索树")
        self.resize(1400, 700)

        # 初始化核心数据结构
        self.tree = AVLTree()
        self.tree.add_listener(self.on_update)

        # 初始化图形对象
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标映射
        self.node_artists = []  # 用于存储节点图形对象，实现点击功能

        # 初始化动画相关变量
        self.path_nodes = []
        self.path_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_path)

        # 步骤记录面板
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.step_text.setPlaceholderText("操作步骤将显示在这里...")

        # 主布局：左右分栏
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # 左侧：树图和控件
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        main_layout.addWidget(left_panel, 7)
        main_layout.addWidget(self.step_text, 3)

        # 左侧控件区：基础操作
        ctrl = QHBoxLayout()
        self.inputVal = QLineEdit()
        self.inputVal.setPlaceholderText("输入整数（1-100）")
        self.inputVal.setMaximumWidth(120)
        ctrl.addWidget(self.inputVal)

        self.btn_insert = QPushButton("插入")
        self.btn_insert.clicked.connect(self.insert)
        ctrl.addWidget(self.btn_insert)
        
        self.btn_search = QPushButton("查找")
        self.btn_search.clicked.connect(self.search)
        ctrl.addWidget(self.btn_search)
        
        self.btn_delete = QPushButton("删除")
        self.btn_delete.clicked.connect(self.delete)
        ctrl.addWidget(self.btn_delete)
        
        self.btn_inorder = QPushButton("中序遍历")
        self.btn_inorder.clicked.connect(self.show_inorder)
        ctrl.addWidget(self.btn_inorder)

        # 随机生成控件
        ctrl.addWidget(QLabel("随机节点数："))
        self.spinN = QSpinBox()
        self.spinN.setRange(1, 20)
        self.spinN.setValue(10)
        self.spinN.setMaximumWidth(60)
        ctrl.addWidget(self.spinN)
        
        self.btn_random = QPushButton("随机生成 AVL")
        self.btn_random.clicked.connect(self.random_build)
        ctrl.addWidget(self.btn_random)

        # 左侧控件区：高级功能
        adv = QHBoxLayout()
        adv.addWidget(QLabel("高级查找："))
        self.btn_predecessor = QPushButton("查找前驱")
        self.btn_predecessor.clicked.connect(self.find_predecessor)
        adv.addWidget(self.btn_predecessor)
        
        self.btn_successor = QPushButton("查找后继")
        self.btn_successor.clicked.connect(self.find_successor)
        adv.addWidget(self.btn_successor)
        
        self.btn_lower_bound = QPushButton("lower_bound（首个≥值）")
        self.btn_lower_bound.clicked.connect(self.find_lower_bound)
        adv.addWidget(self.btn_lower_bound)

        # 文件操作布局
        file_ops = QHBoxLayout()
        file_ops.addWidget(QLabel("文件操作："))
        self.btn_save = QPushButton("保存数据")
        self.btn_save.clicked.connect(self.save_data)
        file_ops.addWidget(self.btn_save)
        
        self.btn_load = QPushButton("加载数据")
        self.btn_load.clicked.connect(self.load_data)
        file_ops.addWidget(self.btn_load)

        # 状态栏
        self.status = QLabel("就绪 - AVL树自动保持平衡，支持旋转操作可视化")

        # 组装左侧布局
        left_layout.addWidget(self.canvas)
        left_layout.addLayout(ctrl)
        left_layout.addWidget(QLabel("——— 高级查找功能 ———"))
        left_layout.addLayout(adv)
        left_layout.addWidget(QLabel("——— 文件操作 ———"))
        left_layout.addLayout(file_ops)
        left_layout.addWidget(self.status)

        # 初始绘制空树
        self.draw_tree(None)

    # 基础操作
    def insert(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始插入值：{val}")
        self.tree.insert(val, step_callback=self.add_step)

    def search(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始搜索值：{val}")
        self.tree.search(val, step_callback=self.add_step)

    def delete(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始删除值：{val}")
        self.tree.delete(val, step_callback=self.add_step)

    # 中序遍历
    def show_inorder(self):
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        seq = self.tree.inorder()
        seq_text = " -> ".join(map(str, seq))
        self.status.setText(f"中序遍历（递增序列）: {seq_text}")
        self.add_step(f"中序遍历结果（AVL特性：递增）：{seq_text}")

    # 随机生成AVL
    def random_build(self):
        n = self.spinN.value()
        self.add_step(f"开始随机生成 {n} 个节点的AVL树（值范围：1-100）")
        values = self.tree.build_random(n=n, value_range=(1, 100), step_callback=self.add_step)
        self.add_step(f"生成完成，值序列：{values}")
        self.status.setText(f"随机生成 {n} 个节点: {values}")

    # 高级查找功能
    def find_predecessor(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"查找值 {val} 的前驱（中序遍历前一个节点）")
        node, path = self.tree.predecessor(val, step_callback=self.add_step)
        self._animate_special_path("前驱", val, node, path)

    def find_successor(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"查找值 {val} 的后继（中序遍历后一个节点）")
        node, path = self.tree.successor(val, step_callback=self.add_step)
        self._animate_special_path("后继", val, node, path)

    def find_lower_bound(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"查找值 {val} 的lower_bound（首个≥{val}的节点）")
        node, path = self.tree.lower_bound(val, step_callback=self.add_step)
        self._animate_special_path("lower_bound", val, node, path)

    # 动画逻辑
    def _animate_special_path(self, op, val, node, path):
        if not path:
            self.status.setText(f"{op}({val})：空树")
            return
        self.path_nodes = path
        self.path_index = 0
        self.timer.stop()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(lambda: self._animate_trace(op, val, node))
        self.timer.start(450)

    def _animate_trace(self, op, val, node):
        if self.path_index < len(self.path_nodes):
            n = self.path_nodes[self.path_index]
            self.draw_tree(self.tree.root, highlight=n)
            self.add_step(f"{op}查找步骤 {self.path_index+1}：比较节点 {n.val}（当前路径：{[x.val for x in self.path_nodes[:self.path_index+1]]}）")
            self.path_index += 1
        else:
            self.timer.stop()
            if node:
                self.status.setText(f"{op}({val}) = {node.val} (freq={node.freq})")
                self.draw_tree(self.tree.root, highlight=node)
            else:
                self.status.setText(f"{op}({val})：未找到结果")
                self.draw_tree(self.tree.root)

    def _animate_path(self):
        if self.path_index >= len(self.path_nodes):
            self.timer.stop()
            self.draw_tree(self.tree.root)
            return
        node = self.path_nodes[self.path_index]
        self.draw_tree(self.tree.root, highlight=node)
        self.path_index += 1

    # 数据更新回调
    def on_update(self, state):
        action = state.get("action")
        node = state.get("node")
        extra = state.get("extra") or []

        # 处理操作路径动画
        if extra and isinstance(extra, list) and all(hasattr(x, "val") for x in extra):
            self.path_nodes = extra
            self.path_index = 0
            self.timer.start(450)

        # 更新状态栏和步骤记录
        if action == "insert":
            self.status.setText(f"插入节点 {node.val}（高度：{node.height}）")
            self.add_step(f"插入成功：节点 {node.val}（高度：{node.height}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "increase_freq":
            self.status.setText(f"节点 {node.val} 频率 +1 -> {node.freq}")
            self.add_step(f"节点 {node.val} 频率+1（当前：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "decrease_freq":
            self.status.setText(f"节点 {node.val} 频率 -1 -> {node.freq}")
            self.add_step(f"节点 {node.val} 频率-1（当前：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "delete":
            self.status.setText(f"删除节点 {node.val if node else '?'}")
            self.add_step(f"删除成功：节点 {node.val if node else '?'}")
            self.draw_tree(self.tree.root)
        elif action == "found":
            self.status.setText(f"查找成功: {node.val} (freq={node.freq}, height={node.height})")
            self.add_step(f"查找成功：{node.val}（频率：{node.freq}，高度：{node.height}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "not_found":
            self.status.setText("查找失败")
            self.add_step("查找失败：未找到目标节点")
            self.draw_tree(self.tree.root)
        elif action == "build":
            self.status.setText("随机生成 AVL 树完成")
            self.add_step("随机生成AVL树完成")
            self.draw_tree(self.tree.root)
        elif action == "trace_path":
            pass  # 路径追踪在动画中处理

    # 绘制树形结构（显示高度信息）
    def draw_tree(self, node, highlight=None):
        self.ax.clear()
        self.coords = {}
        self.node_artists = []  # 重置节点图形列表
        
        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return

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

        # 节点绘制（显示高度）
        for n, (x, y) in self.coords.items():
            color = "#FF6347" if highlight is n else "#87CEFA"
            lw = 2 if highlight is n else 1
            circ = patches.Circle((x, y), 0.35, facecolor=color, edgecolor="black", linewidth=lw)
            self.ax.add_patch(circ)
            # 显示值、频率和高度
            label = f"{n.val}"
            if n.freq > 1:
                label += f"-{n.freq}"
            label += f"\nh={n.height}"
            text = self.ax.text(x, y, label, ha="center", va="center", fontsize=8)
            self.node_artists.append((circ, n))

        # 绑定点击事件
        self.canvas.mpl_connect('button_press_event', self.on_node_click)
        
        self.ax.axis("off")
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 1, max(xs) + 1)
            self.ax.set_ylim(min(ys) - 1, max(ys) + 1)
        self.canvas.draw_idle()

    # 节点点击事件（删除节点）
    def on_node_click(self, event):
        if event.inaxes != self.ax:
            return
        
        for artist, node in self.node_artists:
            if artist.contains(event)[0]:
                val = node.val
                reply = QMessageBox.question(
                    self, "确认删除", 
                    f"确定要删除节点 {val} 吗？",
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.add_step(f"用户点击删除节点：{val}")
                    self.tree.delete(val, step_callback=self.add_step)
                break

    # 计算树深度
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

    # 获取输入整数
    def _get_int(self):
        try:
            val = int(self.inputVal.text().strip())
            if val < 1 or val > 100:
                QMessageBox.warning(self, "范围错误", "请输入1-100之间的整数！")
                return None
            return val
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的整数！")
            return None

    # 步骤记录方法
    def add_step(self, text):
        current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.step_text.append(f"[{current_time}] {text}")
        self.step_text.verticalScrollBar().setValue(
            self.step_text.verticalScrollBar().maximum()
        )

    # 文件操作
    def save_data(self):
        if not self.tree.root:
            QMessageBox.information(self, "提示", "树为空，无需保存")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存数据", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if not file_path:
            return
            
        data = self.tree.inorder()
        try:
            from PySide6.QtCore import QFile
            file = QFile(file_path)
            if file.open(QIODevice.WriteOnly | QIODevice.Text):
                stream = QTextStream(file)
                stream << ",".join(map(str, data))
                file.close()
                self.add_step(f"数据已保存到 {file_path}")
                QMessageBox.information(self, "成功", "数据保存成功")
        except Exception as e:
            self.add_step(f"保存失败：{str(e)}")
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载数据", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if not file_path:
            return
            
        try:
            from PySide6.QtCore import QFile
            file = QFile(file_path)
            if file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(file)
                content = stream.readAll()
                file.close()
                
                # 清空现有树
                self.tree.root = None
                self.draw_tree(None)
                
                # 解析数据并插入
                values = list(map(int, content.split(',')))
                self.add_step(f"从 {file_path} 加载数据：{values}")
                
                for val in values:
                    if 1 <= val <= 100:
                        self.tree.insert(val, step_callback=self.add_step)
                    else:
                        self.add_step(f"跳过无效值 {val}（必须在1-100之间）")
                
                QMessageBox.information(self, "成功", f"已加载 {len(values)} 个数据")
        except Exception as e:
            self.add_step(f"加载失败：{str(e)}")
            QMessageBox.critical(self, "错误", f"加载失败：{str(e)}")