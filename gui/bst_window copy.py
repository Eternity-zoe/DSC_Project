from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QSpinBox, QTextEdit, QScrollBar
)
from PySide6.QtCore import QTimer, QDateTime, Qt # 导入 Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

from core.bst_tree import BSTree 
from core.dsl_parser import DSLParser 
from dsl.bst.bst_dsl_parser import BSTDSLParser 
from dsl.bst.bst_dsl_executor import BSTDSLExecutor 


class BSTWindow(QMainWindow):
    # 固定的节点半径
    NODE_RADIUS = 0.28 
    # 动画速度（毫秒）
    ANIMATION_SPEED = 450 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("二叉搜索树（BST）可视化 - 支持步骤记录")
        self.resize(1600, 800)

        # === 初始化核心数据结构 ===
        self.tree = BSTree()
        self.tree.add_listener(self.on_update)  # 绑定更新回调

        # === 初始化DSL相关 ===
        self.dsl_parser = BSTDSLParser()
        self.dsl_executor = BSTDSLExecutor(self)

        # === 初始化图形对象 ===
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标映射
        self.node_artists = []

        # === 初始化动画相关变量：统一使用 path_nodes 和 index ===
        self.path_nodes = []  # 动画路径节点 (Node objects)
        self.path_index = 0  # 动画当前索引
        self.animation_target_node = None # 最终目标节点 (用于查找操作)
        self.animation_operation = ""     # 当前操作类型 (用于日志)
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_trace) # 统一连接到 _animate_trace

        # === 步骤记录面板 ===
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.step_text.setPlaceholderText("操作步骤将显示在这里...")
        
        # ... (省略布局和控件初始化部分，与原代码相同)
        
        # === 主布局：左(DSL)-中(画布+控件)-右(记录) ===
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ========== 左侧：DSL面板 ==========
        self._init_dsl_panel()
        main_layout.addWidget(self.dsl_panel, 2)  # 占比2

        # ========== 中间：画布+操作控件 ==========
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setSpacing(8)
        main_layout.addWidget(middle_panel, 7)  # 占比7

        # 画布区域
        canvas_title = QLabel("BST 可视化区域")
        canvas_title.setStyleSheet("font-weight:bold;font-size:14px;padding:5px;")
        middle_layout.addWidget(canvas_title)
        middle_layout.addWidget(self.canvas, stretch=1)

        # === 左侧控件区：基础操作 ===
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
        self.btn_random = QPushButton("随机生成 BST")
        self.btn_random.clicked.connect(self.random_build)
        ctrl.addWidget(self.btn_random)

        # === 左侧控件区：高级功能 ===
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

        # === 状态栏 ===
        self.status = QLabel("就绪")
        self.status.setStyleSheet("padding:5px;background-color:#f0f0f0;border-radius:3px;")

        # 组装中间面板控件
        middle_layout.addLayout(ctrl)
        middle_layout.addWidget(QLabel("——— 高级查找功能 ———"))
        middle_layout.addLayout(adv)
        middle_layout.addWidget(QLabel("——— 文件操作 ———"))
        middle_layout.addLayout(file_ops)
        middle_layout.addWidget(self.status)

        # ========== 右侧：步骤记录面板 ==========
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(right_panel, 3)  # 占比3

        # 右侧标题
        step_title = QLabel("操作步骤记录")
        step_title.setStyleSheet("font-weight:bold;font-size:14px;padding:5px;")
        right_layout.addWidget(step_title)
        
        # 步骤记录文本框
        right_layout.addWidget(self.step_text, stretch=1)

        # 初始绘制空树
        self.draw_tree(None)

    def _init_dsl_panel(self):
        """初始化DSL面板"""
        self.dsl_panel = QWidget()
        layout = QVBoxLayout(self.dsl_panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # DSL标题
        title = QLabel("BST DSL 执行面板")
        title.setStyleSheet("font-weight:bold;font-size:14px;padding:5px;")
        layout.addWidget(title)

        # DSL输入框
        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText("""// BST DSL示例
clear;

// 构建初始树
build [5, 3, 7, 2, 4, 6, 8];
draw;

// 基本操作
insert 1;
insert 9;
draw;

// 查找操作
search 4;
find_predecessor 5;
find_successor 5;

// 删除操作
delete 3;
draw;

// 遍历操作
inorder;
""")
        self.dsl_input.setMinimumHeight(400)
        layout.addWidget(self.dsl_input, stretch=1)

        # DSL按钮区
        btn_layout = QHBoxLayout()
        self.btn_exec_dsl = QPushButton("执行 DSL")
        self.btn_exec_dsl.clicked.connect(self.execute_dsl)
        btn_layout.addWidget(self.btn_exec_dsl)

        self.btn_clear_dsl = QPushButton("清空脚本")
        self.btn_clear_dsl.clicked.connect(lambda: self.dsl_input.clear())
        btn_layout.addWidget(self.btn_clear_dsl)

        self.btn_load_example = QPushButton("加载示例")
        self.btn_load_example.clicked.connect(self._load_dsl_example)
        btn_layout.addWidget(self.btn_load_example)
        layout.addLayout(btn_layout)

        # DSL执行结果
        self.dsl_result = QLabel("就绪")
        self.dsl_result.setStyleSheet("padding:5px;margin-top:5px;border:1px solid #e0e0e0;border-radius:3px;")
        layout.addWidget(self.dsl_result)
        
    # === 基础操作 ===
    def insert(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"开始插入值：{val}")
        self.tree.insert(val, step_callback=self.add_step)  # 传入步骤回调
        # 注意：插入的动画由 on_update 触发

    def search(self):
        val = self._get_int()
        if val is None:
            return
        # 停止所有正在进行的动画
        self.timer.stop() 
        self.animation_target_node = None
        self.path_nodes = []
        
        self.add_step(f"开始搜索值：{val}")
        # search 会在结束时触发 on_update，其中包含完整的路径
        self.tree.search(val, step_callback=self.add_step) 

    def delete(self):
        val = self._get_int()
        if val is None:
            return
        # 停止所有正在进行的动画
        self.timer.stop() 
        self.animation_target_node = None
        self.path_nodes = []
        
        self.add_step(f"开始删除值：{val}")
        # delete 会在结束时触发 on_update，其中包含完整的路径
        self.tree.delete(val, step_callback=self.add_step) 

    # === 中序遍历、随机生成BST ===
    def show_inorder(self):
        # ... (与原代码相同)
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        seq = self.tree.inorder()
        seq_text = " -> ".join(map(str, seq))
        self.status.setText(f"中序遍历（递增序列）: {seq_text}")
        self.add_step(f"中序遍历结果（BST特性：递增）：{seq_text}")

    def random_build(self):
        # ... (与原代码相同)
        n = self.spinN.value()
        self.add_step(f"开始随机生成 {n} 个节点的BST（值范围：1-100）")
        values = self.tree.build_random(n=n, value_range=(1, 100), step_callback=self.add_step)
        self.add_step(f"生成完成，值序列：{values}")
        self.status.setText(f"随机生成 {n} 个节点: {values}")

    # === 高级查找功能：统一使用 on_update 来启动动画 ===
    def find_predecessor(self):
        val = self._get_int()
        if val is None:
            return
        self.timer.stop() 
        self.animation_target_node = None
        self.path_nodes = []
        self.animation_operation = "查找前驱"
        self.add_step(f"查找值 {val} 的前驱（中序遍历前一个节点）")
        # predecessor 需要返回路径并在 on_update 触发动画
        self.tree.predecessor(val, step_callback=self.add_step) 

    def find_successor(self):
        val = self._get_int()
        if val is None:
            return
        self.timer.stop() 
        self.animation_target_node = None
        self.path_nodes = []
        self.animation_operation = "查找后继"
        self.add_step(f"查找值 {val} 的后继（中序遍历后一个节点）")
        self.tree.successor(val, step_callback=self.add_step) 

    def find_lower_bound(self):
        val = self._get_int()
        if val is None:
            return
        self.timer.stop() 
        self.animation_target_node = None
        self.path_nodes = []
        self.animation_operation = "lower_bound"
        self.add_step(f"查找值 {val} 的lower_bound（首个≥{val}的节点）")
        self.tree.lower_bound(val, step_callback=self.add_step) 

    # === 动画逻辑：统一路径高亮并处理结束状态 ===
    def _animate_trace(self):
        """统一的路径动画逻辑"""
        if self.path_index < len(self.path_nodes):
            n = self.path_nodes[self.path_index]
            self.draw_tree(self.tree.root, highlight=n)
            
            # 根据操作类型更新步骤记录
            op = self.animation_operation if self.animation_operation else "操作"
            # 记录当前路径节点值，避免显示复杂的对象引用
            path_val_list = [x.val for x in self.path_nodes[:self.path_index+1]]
            self.add_step(f"【{op}】步骤 {self.path_index+1}：访问节点 {n.val} (路径: {path_val_list})")
            
            self.path_index += 1
        else:
            self.timer.stop()
            op = self.animation_operation if self.animation_operation else "操作"
            
            if self.animation_target_node:
                # 动画结束后，高亮最终结果
                val = self.animation_target_node.val
                freq = self.animation_target_node.freq
                self.status.setText(f"【{op}】完成: {val} (freq={freq})")
                self.draw_tree(self.tree.root, highlight=self.animation_target_node)
                self.add_step(f"【{op}】结束：结果节点 {val}")
            else:
                # 动画结束后，恢复正常视图或显示未找到
                self.status.setText(f"【{op}】结束：未找到目标或操作完成")
                self.draw_tree(self.tree.root)
                self.add_step(f"【{op}】结束：未找到目标")
                
            # 清理动画状态
            self.animation_target_node = None
            self.path_nodes = []
            self.animation_operation = ""
            
    # === 数据更新回调：负责启动动画或立即更新视图 ===
    def on_update(self, state):
        action = state.get("action")
        node = state.get("node")
        extra = state.get("extra") # 期望是一个节点路径列表
        
        # 1. 如果有路径 (extra)，则启动路径动画
        if isinstance(extra, list) and all(hasattr(x, "val") for x in extra) and len(extra) > 0:
            self.timer.stop() # 停止旧动画
            self.path_nodes = extra
            self.path_index = 0
            self.animation_target_node = node # 保存最终结果
            
            # 设定操作类型用于日志
            if action in ["insert", "search", "found", "not_found", "delete", "decrease_freq", "increase_freq"]:
                 self.animation_operation = action
            elif action in ["found_predecessor", "found_successor", "found_lower_bound"]:
                 self.animation_operation = action.split("_")[1] # predecessor/successor/lower
            else:
                 self.animation_operation = "操作"
            
            # 启动动画
            self.timer.start(self.ANIMATION_SPEED)
            return

        # 2. 如果没有路径，则根据 action 立即更新
        self.timer.stop() # 确保没有动画在运行
        self.path_nodes = []
        
        if action == "insert":
            self.status.setText(f"插入节点 {node.val}")
            self.add_step(f"插入成功：节点 {node.val}")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "increase_freq":
            self.status.setText(f"节点 {node.val} 频率 +1 -> {node.freq}")
            self.add_step(f"节点 {node.val} 频率+1（当前：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "decrease_freq":
            # 这种情况通常发生在删除后频率减1，或删除操作完成后
            self.status.setText(f"节点 {node.val} 频率 -1 -> {node.freq}")
            self.add_step(f"节点 {node.val} 频率-1（当前：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "delete":
            # 假设删除操作已经完成
            self.status.setText(f"节点删除完成")
            self.add_step(f"删除操作完成，节点 {node.val if node else '？'} 被移除")
            self.draw_tree(self.tree.root)
        elif action == "build":
            # 随机生成或加载完成
            self.status.setText("BST 构建完成")
            self.add_step("BST 构建/加载完成")
            self.draw_tree(self.tree.root)
        elif action == "found":
            # 查找成功（无路径或路径已走完）
            self.status.setText(f"查找成功: {node.val} (freq={node.freq})")
            self.add_step(f"查找成功：{node.val}（频率：{node.freq}）")
            self.draw_tree(self.tree.root, highlight=node)
        elif action == "not_found":
            # 查找失败（无路径或路径已走完）
            self.status.setText("查找失败")
            self.add_step("查找失败：未找到目标节点")
            self.draw_tree(self.tree.root)
            
    # === 绘制树形结构：使用固定的 NODE_RADIUS ===
    def draw_tree(self, node, highlight=None):
        self.ax.clear()
        self.coords = {}
        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return

        max_depth = self._compute_depth(node)
        
        # 布局函数（使用DFS或BFS确定坐标）
        def layout(n, x, depth, span):
            if not n:
                return
            self.coords[n] = (x, -depth)
            gap = span / 2
            layout(n.left, x - gap, depth + 1, gap)
            layout(n.right, x + gap, depth + 1, gap)
        layout(node, 0, 0, 8) # 初始中心 x=0, depth=0, span=8

        # 连线
        for n, (x, y) in self.coords.items():
            if n.left:
                x2, y2 = self.coords[n.left]
                # 调整连线起点/终点，使其位于圆圈边缘（可选，但更精确）
                dx = x2 - x
                dy = y2 - y
                dist = (dx**2 + dy**2)**0.5
                
                # 计算圆心到圆心之间连线上的圆圈边缘点
                start_x = x + self.NODE_RADIUS * dx / dist
                start_y = y + self.NODE_RADIUS * dy / dist
                end_x = x2 - self.NODE_RADIUS * dx / dist
                end_y = y2 - self.NODE_RADIUS * dy / dist
                
                self.ax.plot([start_x, end_x], [start_y, end_y], "k-", zorder=1) # 设置 zorder=1

            if n.right:
                x2, y2 = self.coords[n.right]
                dx = x2 - x
                dy = y2 - y
                dist = (dx**2 + dy**2)**0.5
                
                start_x = x + self.NODE_RADIUS * dx / dist
                start_y = y + self.NODE_RADIUS * dy / dist
                end_x = x2 - self.NODE_RADIUS * dx / dist
                end_y = y2 - self.NODE_RADIUS * dy / dist

                self.ax.plot([start_x, end_x], [start_y, end_y], "k-", zorder=1) # 设置 zorder=1

        # 节点绘制
        self.node_artists = []
        for n, (x, y) in self.coords.items():
            color = "#FF6347" if highlight is n else "#87CEFA"
            lw = 2 if highlight is n else 1
            # 使用固定的 NODE_RADIUS
            circ = patches.Circle((x, y), self.NODE_RADIUS, facecolor=color, edgecolor="black", linewidth=lw, zorder=3) # 设置 zorder=3
            self.ax.add_patch(circ)
            
            # 显示值和频率 (如果频率 > 1)
            label = f"{n.val}" if n.freq == 1 else f"{n.val}-{n.freq}"
            text = self.ax.text(x, y, label, ha="center", va="center", fontsize=9, zorder=5) # 设置 zorder=5
            self.node_artists.append((circ, n))  # 保存图形和节点的对应关系

        self.ax.axis("off")
        xs = [p[0] for p in self.coords.values()]
        ys = [p[1] for p in self.coords.values()]
        
        # 确保坐标轴范围正确，留出一点边距
        if xs and ys:
            # 加上一个安全边距，至少保证 x 和 y 有足够的范围
            x_min = min(xs) - 1.5
            x_max = max(xs) + 1.5
            y_min = min(ys) - 1.5
            y_max = max(ys) + 1.5
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            self.ax.set_aspect('equal', adjustable='box') # 保持 x y 比例一致

        # 绑定点击事件
        self.canvas.mpl_connect('button_press_event', self.on_node_click)
        self.canvas.draw_idle()

    def on_node_click(self, event):
        # ... (与原代码相同)
        """处理节点点击事件，实现点击删除功能"""
        if event.inaxes != self.ax:
            return
        
        # 检查点击位置是否在某个节点上
        for artist, node in self.node_artists:
            # 使用 artist.contains(event)[0] 来判断点击是否在 patch 范围内
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

    # === 辅助方法：计算树深度、获取输入整数 ===
    def _compute_depth(self, root):
        # ... (与原代码相同)
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

    def _get_int(self):
        # ... (与原代码相同)
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
        # ... (与原代码相同)
        """向右侧面板添加步骤记录"""
        current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.step_text.append(f"[{current_time}] {text}")
        # 自动滚动到底部
        self.step_text.verticalScrollBar().setValue(
            self.step_text.verticalScrollBar().maximum()
        )

    # === 文件操作方法 ===
    def save_data(self):
        # ... (与原代码相同)
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
        # ... (与原代码相同)
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
                values = [int(v.strip()) for v in content.split(',') if v.strip()] # 确保处理空字符串
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

    # === DSL相关方法 ===
    def execute_dsl(self):
        # ... (与原代码相同)
        """执行DSL语句并处理结果"""
        dsl_text = self.dsl_input.toPlainText().strip()
        if not dsl_text:
            self.dsl_result.setText("⚠️ 请输入DSL语句")
            QMessageBox.warning(self, "警告", "请输入DSL脚本内容")
            return

        try:
            # 清空之前的结果提示
            self.dsl_result.setText("✅ DSL脚本执行中...")
            self.add_step("=== 开始执行DSL脚本 ===")
            
            # 解析DSL脚本
            cmds = self.dsl_parser.parse(dsl_text)
            
            # 执行DSL命令
            self.dsl_executor.execute(cmds)
            
            self.dsl_result.setText("✅ DSL脚本执行完成")
            self.add_step("=== DSL脚本执行完成 ===")
            QMessageBox.information(self, "成功", "DSL脚本执行完成")
            
        except Exception as e:
            error_msg = f"❌ 执行失败: {str(e)}"
            self.dsl_result.setText(error_msg)
            self.add_step(f"DSL执行错误：{str(e)}")
            QMessageBox.critical(self, "DSL执行错误", str(e))

    def _load_dsl_example(self):
        # ... (与原代码相同)
        """加载DSL示例脚本"""
        example = """// BST DSL示例
clear;

// 构建初始树
build [5, 3, 7, 2, 4, 6, 8];
draw;

// 基本操作
insert 1;
insert 9;
draw;

// 查找操作
search 4;
find_predecessor 5;
find_successor 5;

// 删除操作
delete 3;
draw;

// 遍历操作
inorder;
"""
        self.dsl_input.setText(example)
        self.dsl_result.setText("📝 已加载示例脚本")