# gui/bst_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QSpinBox, QTextEdit
)
from PySide6.QtCore import QTimer, QDateTime  # 合并QTimer和QDateTime导入
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
from core.bst_tree import BSTree
import re  
from core.dsl_parser import DSLParser


class BSTWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二叉搜索树（BST）可视化 - 支持步骤记录")
        self.resize(1400, 700)  # 加宽窗口

        # === 初始化核心数据结构 ===
        self.tree = BSTree()
        self.tree.add_listener(self.on_update)  # 绑定更新回调
        self.dsl_parser = DSLParser()
        
        # === 初始化图形对象（修复：添加matplotlib画布） ===
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标映射
        self.node_artists = []

        # === 初始化动画相关变量 ===
        self.path_nodes = []  # 动画路径节点
        self.path_index = 0   # 动画当前索引
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_path)

        # === 步骤记录面板 ===
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.step_text.setPlaceholderText("操作步骤将显示在这里...")

        # === 初始化DSL面板 ===
        self._init_dsl_panel()

        # === 主布局：左右分栏 ===
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)  # 水平布局

        # 左侧容器（包含DSL面板和树图区域）
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        
        # 添加DSL面板到左侧容器
        left_layout.addWidget(self.dsl_panel)

         # 左侧树图和控件区域
        left_panel = QWidget()
        left_panel_layout = QVBoxLayout(left_panel)

        # === 左侧控件区：基础操作 ===
        ctrl = QHBoxLayout()  # 修复：正确定义ctrl布局
        self.inputVal = QLineEdit()  # 修复：初始化输入框
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
        self.spinN = QSpinBox()  # 修复：初始化spinN
        self.spinN.setRange(1, 20)
        self.spinN.setValue(10)
        self.spinN.setMaximumWidth(60)
        ctrl.addWidget(self.spinN)
        self.btn_random = QPushButton("随机生成 BST")
        self.btn_random.clicked.connect(self.random_build)
        ctrl.addWidget(self.btn_random)

        # === 左侧控件区：高级功能 ===
        adv = QHBoxLayout()  # 修复：正确定义adv布局
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

         # === 状态栏 ===
        self.status = QLabel("就绪 - 支持DSL操作和可视化联动")

        # === 组装左侧面板布局 ===
        left_panel_layout.addWidget(self.canvas)
        left_panel_layout.addLayout(ctrl)
        left_panel_layout.addWidget(QLabel("——— 高级查找功能 ———"))
        left_panel_layout.addLayout(adv)
        left_panel_layout.addWidget(QLabel("——— 文件操作 ———"))
        left_panel_layout.addLayout(file_ops)
        left_panel_layout.addWidget(self.status)

        # 将左侧面板添加到左侧容器
        left_layout.addWidget(left_panel, stretch=1)

        # 主布局组装
        main_layout.addWidget(left_container, 7)
        main_layout.addWidget(self.step_text, 3)

        # 初始绘制空树
        self.draw_tree(None)

    
    def _init_dsl_panel(self):
        """初始化DSL执行面板"""
        self.dsl_panel = QWidget()
        dsl_layout = QVBoxLayout(self.dsl_panel)
        dsl_layout.setContentsMargins(5, 5, 5, 5)
        
        # 面板标题
        title_label = QLabel("DSL执行面板")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        dsl_layout.addWidget(title_label)
        
        # 输入区域
        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText("""支持声明式和命令式DSL语句：
// 声明式示例
bst MyTree {
    node root { int val = 5; left = n3; right = n7; }
    node n3 { int val = 3; }
    node n7 { int val = 7; }
}

// 命令式示例
insert MyTree value=9;
search MyTree value=3;
delete MyTree value=7;
find_predecessor MyTree value=5;""")
        self.dsl_input.setMinimumHeight(120)
        dsl_layout.addWidget(self.dsl_input)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        self.btn_execute_dsl = QPushButton("执行DSL")
        self.btn_execute_dsl.clicked.connect(self.execute_dsl)
        self.btn_clear_dsl = QPushButton("清空")
        self.btn_clear_dsl.clicked.connect(lambda: self.dsl_input.clear())
        
        btn_layout.addWidget(self.btn_execute_dsl)
        btn_layout.addWidget(self.btn_clear_dsl)
        dsl_layout.addLayout(btn_layout)
        
        # 结果提示区
        self.dsl_result = QLabel("")
        self.dsl_result.setStyleSheet("color: #666; font-size: 12px;")
        dsl_layout.addWidget(self.dsl_result)

    def execute_dsl(self):
        """执行DSL语句并处理结果"""
        dsl_text = self.dsl_input.toPlainText().strip()
        if not dsl_text:
            self.dsl_result.setText("⚠️ 请输入DSL语句")
            return

        try:
            # 区分声明式和命令式语法
            if re.search(r'bst\s+\w+\s*{', dsl_text, re.IGNORECASE):
                # 声明式：解析并创建新BST
                struct = self.dsl_parser.parse_script(dsl_text)
                self._load_bst_from_dsl(struct)
                self.dsl_result.setText(f"✅ 已创建BST: {struct.name}")
                self.add_step(f"通过DSL创建BST: {struct.name}")
            else:
                # 命令式：执行操作
                self._execute_dsl_command(dsl_text)
                self.dsl_result.setText("✅ DSL操作执行成功")
        except Exception as e:
            error_msg = f"❌ 执行失败: {str(e)}"
            self.dsl_result.setText(error_msg)
            self.add_step(error_msg)
            QMessageBox.warning(self, "DSL执行错误", str(e))

    def _load_bst_from_dsl(self, struct):
        """从DSL解析结果加载BST结构"""
        if struct.type != "bst":
            raise ValueError("仅支持BST类型的声明")

        # 清空现有树
        self.tree.root = None
        
        # 提取节点值映射
        node_values = {}
        for node in struct.nodes:
            val_field = next((f for f in node.fields if f.name == "val"), None)
            if val_field:
                node_values[node.name] = int(val_field.value)
        
        # 先插入所有节点（保证存在性）
        for name, val in node_values.items():
            self.tree.insert(val, step_callback=self.add_step, skip_animation=True)
        
        # 重新构建父子关系
        for node in struct.nodes:
            current_val = node_values[node.name]
            current_node = self.tree.search_node(current_val)
            
            # 处理左子树
            left_link = next((l for l in node.links if l.startswith("left=")), None)
            if left_link:
                left_node_name = left_link.split("=")[1].strip()
                if left_node_name != "null" and left_node_name in node_values:
                    left_val = node_values[left_node_name]
                    left_node = self.tree.search_node(left_val)
                    current_node.left = left_node
                    left_node.parent = current_node
            
            # 处理右子树
            right_link = next((l for l in node.links if l.startswith("right=")), None)
            if right_link:
                right_node_name = right_link.split("=")[1].strip()
                if right_node_name != "null" and right_node_name in node_values:
                    right_val = node_values[right_node_name]
                    right_node = self.tree.search_node(right_val)
                    current_node.right = right_node
                    right_node.parent = current_node
        
        # 刷新视图
        self.draw_tree(self.tree.root)

    def _execute_dsl_command(self, command):
        """解析并执行命令式DSL"""
        # 命令格式：operation struct_name [params]
        cmd_patterns = [
            # 插入命令
            (r'insert\s+(\w+)\s+value=(\d+);?', self._dsl_insert),
            # 查找命令
            (r'search\s+(\w+)\s+value=(\d+);?', self._dsl_search),
            # 删除命令
            (r'delete\s+(\w+)\s+value=(\d+);?', self._dsl_delete),
            # 查找前驱
            (r'find_predecessor\s+(\w+)\s+value=(\d+);?', self._dsl_predecessor),
            # 查找后继
            (r'find_successor\s+(\w+)\s+value=(\d+);?', self._dsl_successor)
        ]

        for pattern, handler in cmd_patterns:
            match = re.match(pattern, command, re.IGNORECASE)
            if match:
                struct_name = match.group(1)
                value = int(match.group(2))
                # 验证结构名称（当前只支持当前树）
                if struct_name != self.tree.name and hasattr(self.tree, 'name'):
                    raise ValueError(f"未知结构: {struct_name}")
                handler(value)
                return

        raise SyntaxError(f"无效的DSL命令: {command}")

    # DSL命令处理函数
    def _dsl_insert(self, value):
        self.add_step(f"DSL操作：插入值 {value}")
        self.tree.insert(value, step_callback=self.add_step)

    def _dsl_search(self, value):
        self.add_step(f"DSL操作：查找值 {value}")
        self.tree.search(value, step_callback=self.add_step)

    def _dsl_delete(self, value):
        self.add_step(f"DSL操作：删除值 {value}")
        self.tree.delete(value, step_callback=self.add_step)

    def _dsl_predecessor(self, value):
        self.add_step(f"DSL操作：查找 {value} 的前驱")
        node, path = self.tree.predecessor(value, step_callback=self.add_step)
        self._animate_special_path("前驱", value, node, path)

    def _dsl_successor(self, value):
        self.add_step(f"DSL操作：查找 {value} 的后继")
        node, path = self.tree.successor(value, step_callback=self.add_step)
        self._animate_special_path("后继", value, node, path)


    # === 基础操作 ===
    def insert(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始插入值：{val}")
        self.tree.insert(val, step_callback=self.add_step)  # 传入步骤回调

    def search(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始搜索值：{val}")
        self.tree.search(val, step_callback=self.add_step)  # 传入步骤回调

    def delete(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始删除值：{val}")
        self.tree.delete(val, step_callback=self.add_step)  # 传入步骤回调

    # === 中序遍历 ===
    def show_inorder(self):
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        seq = self.tree.inorder()
        seq_text = " -> ".join(map(str, seq))
        self.status.setText(f"中序遍历（递增序列）: {seq_text}")
        self.add_step(f"中序遍历结果（BST特性：递增）：{seq_text}")

    # === 随机生成BST ===
    def random_build(self):
        n = self.spinN.value()
        self.add_step(f"开始随机生成 {n} 个节点的BST（值范围：1-100）")
        values = self.tree.build_random(n=n, value_range=(1, 100), step_callback=self.add_step)
        self.add_step(f"生成完成，值序列：{values}")
        self.status.setText(f"随机生成 {n} 个节点: {values}")

    # === 高级查找功能 ===
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

    # === 动画逻辑 ===
    def _animate_special_path(self, op, val, node, path):
        """带路径动画的前驱/后继/lower_bound 查找"""
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
        """通用路径动画"""
        if self.path_index >= len(self.path_nodes):
            self.timer.stop()
            self.draw_tree(self.tree.root)
            return
        node = self.path_nodes[self.path_index]
        self.draw_tree(self.tree.root, highlight=node)
        self.path_index += 1

    # === 数据更新回调（合并重复方法，修复覆盖问题） ===
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
            self.status.setText(f"插入节点 {node.val}")
            self.add_step(f"插入成功：节点 {node.val}")
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
            self.status.setText(f"查找成功: {node.val} (freq={node.freq})")
            self.add_step(f"查找成功：{node.val}（频率：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "not_found":
            self.status.setText("查找失败")
            self.add_step("查找失败：未找到目标节点")
            self.draw_tree(self.tree.root)
        elif action == "build":
            self.status.setText("随机生成 BST 完成")
            self.add_step("随机生成BST完成")
            self.draw_tree(self.tree.root)

    # === 绘制树形结构 ===
    # 在BSTWindow类的draw_tree方法中添加点击事件处理
    def draw_tree(self, node, highlight=None):
        self.ax.clear()
        self.coords = {}
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

        # 节点绘制
        self.node_artists = []  
        for n, (x, y) in self.coords.items():
            color = "#FF6347" if highlight is n else "#87CEFA"
            lw = 2 if highlight is n else 1
            circ = patches.Circle((x, y), 0.28, facecolor=color, edgecolor="black", linewidth=lw)
            self.ax.add_patch(circ)
            label = f"{n.val}" if n.freq == 1 else f"{n.val}-{n.freq}"
            text = self.ax.text(x, y, label, ha="center", va="center", fontsize=9)
            self.node_artists.append((circ, n))  # 保存图形和节点的对应关系

        self.ax.axis("off")
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 1, max(xs) + 1)
            self.ax.set_ylim(min(ys) - 1, max(ys) + 1)
        
        # 绑定点击事件
        self.canvas.mpl_connect('button_press_event', self.on_node_click)
        self.canvas.draw_idle()

    def on_node_click(self, event):
        """处理节点点击事件，实现点击删除功能"""
        if event.inaxes != self.ax:
            return
        
        # 检查点击位置是否在某个节点上
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

    # === 辅助方法：计算树深度 ===
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

    # === 工具函数：获取输入整数 ===
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

    # === 步骤记录方法 ===
    def add_step(self, text):
        """向右侧面板添加步骤记录"""
        current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.step_text.append(f"[{current_time}] {text}")
        # 自动滚动到底部
        self.step_text.verticalScrollBar().setValue(
            self.step_text.verticalScrollBar().maximum()
        )

    # === 文件操作方法 ===
# 添加文件操作方法
    def save_data(self):
        """将当前树数据保存到文件"""
        from PySide6.QtWidgets import QFileDialog
        from PySide6.QtCore import QFile, QIODevice, QTextStream
        
        if not self.tree.root:
            QMessageBox.information(self, "提示", "树为空，无需保存")
            return
                
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存数据", "", "文本文件 (*.txt);;所有文件 (*)"
        )
            
        if not file_path:
            return
                
        # 获取中序遍历数据
        data = self.tree.inorder()
        try:
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
        """从文件加载数据"""
        from PySide6.QtWidgets import QFileDialog
        from PySide6.QtCore import QFile, QIODevice, QTextStream
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载数据", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if not file_path:
            return
            
        try:
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
                    if 1 <= val <= 100:  # 检查值范围
                        self.tree.insert(val, step_callback=self.add_step)
                    else:
                        self.add_step(f"跳过无效值 {val}（必须在1-100之间）")
                
                QMessageBox.information(self, "成功", f"已加载 {len(values)} 个数据")
        except Exception as e:
            self.add_step(f"加载失败：{str(e)}")
            QMessageBox.critical(self, "错误", f"加载失败：{str(e)}")