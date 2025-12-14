import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QPushButton, QLineEdit, QLabel, QTextEdit, QSpinBox, 
                               QMessageBox, QFileDialog, QSplitter, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QDateTime, QIODevice, QTextStream, QCoreApplication
from PySide6.QtGui import QTextCursor
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches

# 请确保这些模块路径正确
from core.avl_tree import AVLTree, AVLNode
from dsl.avl.avl_dsl_parser import AVLDslParser, ParserError
from dsl.avl.avl_dsl_executor import AVLDslExecutor

# 常量定义
DEFAULT_NODE_COLOR = '#3498db'  # 蓝色
HIGHLIGHT_COLOR = '#e74c3c'    # 红色
PATH_COLOR = '#2ecc71'         # 绿色
ROTATION_COLOR = '#f39c12'     # 橙色
IMBALANCED_TEXT_COLOR = '#c0392b'  # 深红色
DEFAULT_NODE_SIZE = 0.35  # 默认节点大小
MIN_NODE_SIZE = 0.2       # 最小节点大小
NODE_SIZE_THRESHOLD = 8   # 节点数量阈值


class AVLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVL树可视化 - 支持DSL脚本")
        self.resize(1600, 800)

        # 1. 核心数据结构初始化（必须最先初始化）
        self.tree = AVLTree()
        self.tree.add_listener(self.on_update)
        self.state_list = []  # 用于存储状态快照

        # 2. 步骤日志文本框（必须在布局前初始化）
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.step_text.setPlaceholderText("操作步骤将显示在这里...")

        # 3. 图形对象初始化
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标映射
        self.node_artists = []  # 用于存储节点图形对象

        # 4. 动画相关变量
        self.animating = False
        self.animation_steps = 20
        self.current_step = 0
        self.start_coords = {}
        self.target_coords = {}
        self.rotation_highlight = None
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_rotation)
        
        self.path_timer = QTimer()
        self.path_nodes = []
        self.path_index = 0
        self.current_op_details = None 

        # 5. DSL相关组件
        self.dsl_editor = QTextEdit()
        self.dsl_editor.setPlaceholderText("输入AVL树DSL脚本，每行一个操作...\n例如:\nclear\ninsert 5\ninsert 3\ninsert 7\ninorder")
        self.btn_run_dsl = QPushButton("运行DSL脚本")
        self.btn_run_dsl.clicked.connect(self.run_dsl)
        
        # 加载示例代码按钮
        self.btn_load_example = QPushButton("加载实例代码")
        self.btn_load_example.clicked.connect(self.load_example_code)

        # 6. 初始化DSL解析器和执行器
        self.dsl_parser = AVLDslParser()
        self.dsl_executor = AVLDslExecutor(
            self.tree,
            log_callback=lambda msg: self.add_step(msg),
            update_ui_callback=lambda: self.draw_tree(self.tree.root, show_bf=True)
        )

        # 7. 基础操作控件
        self.inputVal = QLineEdit()
        self.inputVal.setPlaceholderText("输入整数（1-100）")
        self.inputVal.setMaximumWidth(120)
        
        self.btn_insert = QPushButton("插入")
        self.btn_insert.clicked.connect(self.insert)
        
        self.btn_search = QPushButton("查找")
        self.btn_search.clicked.connect(self.search)
        
        self.btn_delete = QPushButton("删除")
        self.btn_delete.clicked.connect(self.delete)
        
        self.btn_inorder = QPushButton("中序遍历")
        self.btn_inorder.clicked.connect(self.show_inorder)

        # 随机生成控件
        self.spinN = QSpinBox()
        self.spinN.setRange(1, 20)
        self.spinN.setValue(10)
        self.spinN.setMaximumWidth(60)
        
        self.btn_random = QPushButton("随机生成 AVL")
        self.btn_random.clicked.connect(self.random_build)

        # 高级功能控件
        self.btn_predecessor = QPushButton("查找前驱")
        self.btn_predecessor.clicked.connect(self.find_predecessor)
        
        self.btn_successor = QPushButton("查找后继")
        self.btn_successor.clicked.connect(self.find_successor)
        
        self.btn_lower_bound = QPushButton("lower_bound（首个≥值）")
        self.btn_lower_bound.clicked.connect(self.find_lower_bound)

        # 文件操作控件
        self.btn_save = QPushButton("保存数据")
        self.btn_save.clicked.connect(self.save_data)
        
        self.btn_load = QPushButton("加载数据")
        self.btn_load.clicked.connect(self.load_data)

        # 状态栏
        self.status = QLabel("就绪 - AVL树自动保持平衡，支持旋转操作可视化")

        # 8. 布局组装
        # 8.1 DSL面板
        dsl_panel = QWidget()
        dsl_layout = QVBoxLayout(dsl_panel)
        dsl_layout.addWidget(QLabel("DSL脚本编辑区"))
        dsl_layout.addWidget(self.dsl_editor)
        dsl_layout.addWidget(self.btn_run_dsl)
        dsl_layout.addWidget(self.btn_load_example) 

        # 8.2 中间操作面板
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(self.inputVal)
        ctrl_layout.addWidget(self.btn_insert)
        ctrl_layout.addWidget(self.btn_search)
        ctrl_layout.addWidget(self.btn_delete)
        ctrl_layout.addWidget(self.btn_inorder)
        ctrl_layout.addWidget(QLabel("随机节点数："))
        ctrl_layout.addWidget(self.spinN)
        ctrl_layout.addWidget(self.btn_random)

        adv_layout = QHBoxLayout()
        adv_layout.addWidget(QLabel("高级查找："))
        adv_layout.addWidget(self.btn_predecessor)
        adv_layout.addWidget(self.btn_successor)
        adv_layout.addWidget(self.btn_lower_bound)

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("文件操作："))
        file_layout.addWidget(self.btn_save)
        file_layout.addWidget(self.btn_load)

        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.addWidget(self.canvas)
        middle_layout.addLayout(ctrl_layout)
        middle_layout.addWidget(QLabel("——— 高级查找功能 ———"))
        middle_layout.addLayout(adv_layout)
        middle_layout.addWidget(QLabel("——— 文件操作 ———"))
        middle_layout.addLayout(file_layout)
        middle_layout.addWidget(self.status)

        # 8.3 日志面板
        log_panel = QWidget()
        log_layout = QVBoxLayout(log_panel)
        log_layout.addWidget(QLabel("操作日志"))
        log_layout.addWidget(self.step_text)

        # 8.4 主布局（三栏分割）
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(dsl_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(log_panel)
        splitter.setSizes([300, 800, 500])  # 三栏宽度比例
        
        main_layout.addWidget(splitter)

        # 绑定节点点击事件
        self.canvas.mpl_connect('button_press_event', self.on_node_click)

        # 初始绘制空树
        self.draw_tree(None)

    # DSL执行方法
    def run_dsl(self):
        """执行DSL脚本"""
        code = self.dsl_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "警告", "请输入DSL脚本")
            return

        try:
            # 解析脚本
            program = self.dsl_parser.parse(code)
            self.add_step("DSL脚本解析成功，开始执行...")
            
            # 清空当前树
            self.tree.root = None
            self.draw_tree(None)
            
            # 执行脚本
            self.dsl_executor.execute(program)
        except ParserError as e:
            QMessageBox.critical(self, "解析错误", str(e))
            self.add_step(f"解析错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "执行错误", f"执行过程中发生错误: {str(e)}")
            self.add_step(f"执行错误: {str(e)}")

    # 树布局计算
    def _calculate_coords(self, node, x=0, y=0, level=1, calculate_only=False):
        if node is None:
            return

        # 计算节点总数
        self.node_count = self._count_nodes(node)
        
        H_SEP = 1.0 / (2 ** (level - 1))
        coords = {}

        def _layout(node, x, y, level, h_sep):
            if node is None:
                return
            _layout(node.left, x - h_sep, y - 1, level + 1, h_sep / 2)
            coords[node.val] = (x, y)
            _layout(node.right, x + h_sep, y - 1, level + 1, h_sep / 2)

        _layout(node, x, y, level, H_SEP)

        if calculate_only:
            return coords
        else:
            self.coords = coords

    def _count_nodes(self, node):
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    # 绘制树
    def draw_tree(self, node, highlight=None, highlight_pair=None, highlight_path=None, show_bf=False, node_color=DEFAULT_NODE_COLOR, bf_text_color='black'):
        self.ax.clear()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')
        self.node_artists = []
        
        self._calculate_coords(node, x=0, y=0)

        # 计算节点大小（根据节点数量自适应）
        if hasattr(self, 'node_count') and self.node_count > NODE_SIZE_THRESHOLD:
            # 超过阈值，按比例缩小
            scale_factor = max(NODE_SIZE_THRESHOLD / self.node_count, 0.5)  # 最小缩小到50%
            node_size = DEFAULT_NODE_SIZE * scale_factor
        else:
            node_size = DEFAULT_NODE_SIZE
        
        # 确保不小于最小节点大小
        node_size = max(node_size, MIN_NODE_SIZE)

        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return
            
        all_coords = self.coords.values()
        xs = [x for x, _ in all_coords]
        ys = [y for _, y in all_coords]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
            self.ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
        
        def _draw_node_recursive(n):
            if n is None or n.val not in self.coords:
                return
                
            x, y = self.coords[n.val]
            
            if n.parent and n.parent.val in self.coords:
                px, py = self.coords[n.parent.val]
                line_color = PATH_COLOR if highlight_path and n.parent in highlight_path else 'gray'
                self.ax.plot([px, x], [py, y], color=line_color, linestyle='-', linewidth=1.5, zorder=1)
                
            current_color = node_color
            text_color = 'white'
            lw = 1

            if highlight_pair and any(hn and n.val == hn.val for hn in highlight_pair):
                current_color = ROTATION_COLOR
                lw = 2
            elif highlight and n.val == highlight.val:
                current_color = HIGHLIGHT_COLOR if node_color == DEFAULT_NODE_COLOR else node_color
                lw = 2
            elif highlight_path and n in highlight_path:
                current_color = PATH_COLOR
            elif node_color != DEFAULT_NODE_COLOR:
                current_color = node_color

            # 使用计算出的节点大小
            circle = patches.Circle((x, y), node_size, facecolor=current_color, edgecolor='black', linewidth=lw, zorder=2)
            self.ax.add_patch(circle)
            self.node_artists.append((circle, n))

            label = f"{n.val}"
            if n.freq > 1:
                label += f"-{n.freq}"
            
            # 根据节点大小调整字体
            font_size = max(8, int(10 * (node_size / DEFAULT_NODE_SIZE)))
            self.ax.text(x, y, label, ha='center', va='center', fontsize=font_size, color=text_color, zorder=3)
            
            if show_bf:
                bf = self.tree._balance_factor(n)
                bf_c = IMBALANCED_TEXT_COLOR if abs(bf) > 1 else bf_text_color
                # 平衡因子字体也相应调整
                bf_font_size = max(6, int(8 * (node_size / DEFAULT_NODE_SIZE)))
                self.ax.text(x, y + node_size + 0.05, f"h={n.height}", ha='center', va='center', fontsize=bf_font_size, color='black', zorder=3)
                self.ax.text(x, y - node_size - 0.05, f"bf={bf}", ha='center', va='center', fontsize=bf_font_size, color=bf_c, zorder=3)
            
            _draw_node_recursive(n.left)
            _draw_node_recursive(n.right)
            
        _draw_node_recursive(node)
        self.canvas.draw_idle()

    # 状态更新回调
    def on_update(self, state):
        action = state.get("action")
        node = state.get("node")
        extra = state.get("extra") or {}
        
        if self.path_timer.isActive() and action not in ("found", "not_found", "trace_path"):
             return
        
        if action in ("bst_insert_complete", "bst_delete_complete"):
            val = node.val if node else "?"
            status_text = "插入" if action == "bst_insert_complete" else "删除"
            self.status.setText(f"BST{status_text}完成：节点 {val}，准备检查平衡")
            
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight=node, 
                                show_bf=True, 
                                node_color=PATH_COLOR)
            return

        if action == "check_balance":
            bf = extra.get("bf")
            is_balanced = extra.get("is_balanced")
            status = "正常" if is_balanced else "失衡"
            self.status.setText(f"检查节点 {node.val}，平衡因子={bf}（{status}）")

            delay = 100
            node_color = HIGHLIGHT_COLOR if not is_balanced else PATH_COLOR
            text_color = 'black' if is_balanced else IMBALANCED_TEXT_COLOR
            
            self._delayed_draw(delay, self.draw_tree, 
                                self.tree.root, 
                                highlight=node, 
                                show_bf=True, 
                                node_color=node_color,
                                bf_text_color=text_color)
            return

        if action == "move_to_parent":
            next_node = extra.get("next_node")
            self.status.setText(f"移动到父节点 {next_node.val} 继续检查")
            
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight=next_node, 
                                show_bf=True, 
                                node_color=PATH_COLOR)
            return

        if action in ("left_imbalance", "right_imbalance"):
            child = extra.get("child")
            
            highlight_pair = [node, child]
            if child:
                if extra.get("type") == "Left-Right" and child.right:
                    highlight_pair.append(child.right)
                elif extra.get("type") == "Right-Left" and child.left:
                    highlight_pair.append(child.left)
            
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight_pair=highlight_pair, 
                                show_bf=True, 
                                node_color=ROTATION_COLOR,
                                bf_text_color=IMBALANCED_TEXT_COLOR)
            return

        if action == "rotation_prepare":
            self.rotation_highlight = extra 
            self.start_coords = self.coords.copy() 
            return

        if action == "rotation":
            self._calculate_coords(self.tree.root, calculate_only=False)
            self.target_coords = self.coords.copy()
            
            if self.start_coords and self.target_coords:
                self.animating = True
                self.current_step = 0
                self.animation_timer.start(30)
            else:
                self.draw_tree(self.tree.root, show_bf=True)
            
            self.start_coords = {}
            return

        if action == "balance_complete":
            self.status.setText("所有节点检查完毕，树已平衡")
            
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                show_bf=True, 
                                node_color=DEFAULT_NODE_COLOR)
            self.rotation_highlight = None
            return
            
        if action == "trace_path":
            self._animate_special_path(extra, node)
            return
            
        if action in ("insert", "delete", "found", "not_found", "increase_freq", "decrease_freq", "build"):
            if action == "build":
                self.draw_tree(self.tree.root, show_bf=True)
                return

            highlight_node = node if action in ("insert", "found", "increase_freq", "decrease_freq") else None
            self.draw_tree(self.tree.root, highlight=highlight_node, show_bf=True)
            return

    # 动画绘制
    def _animate_rotation(self):
        self.current_step += 1
        
        if self.current_step > self.animation_steps:
            self.animating = False
            self.animation_timer.stop()
            self.current_step = 0
            
            highlight_pair = []
            if self.tree.root:
                pivot_val = self.rotation_highlight.get("pivot") if self.rotation_highlight else None
                if pivot_val:
                    def find_node(n, val):
                        if not n: return None
                        if n.val == val: return n
                        return find_node(n.left, val) or find_node(n.right, val)

                    pivot_node = find_node(self.tree.root, pivot_val)
                    if pivot_node:
                        highlight_pair.append(pivot_node)
                        if pivot_node.left: 
                            highlight_pair.append(pivot_node.left)
                        if pivot_node.right: 
                            highlight_pair.append(pivot_node.right)
                        
            self.draw_tree(self.tree.root, highlight_pair=highlight_pair, show_bf=True, node_color=ROTATION_COLOR)
            return

        t = self.current_step / float(self.animation_steps)

        self.ax.clear()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')

        current_coords = {}
        
        # 计算动画中的节点大小
        if hasattr(self, 'node_count') and self.node_count > NODE_SIZE_THRESHOLD:
            scale_factor = max(NODE_SIZE_THRESHOLD / self.node_count, 0.5)
            node_size = DEFAULT_NODE_SIZE * scale_factor
        else:
            node_size = DEFAULT_NODE_SIZE
        node_size = max(node_size, MIN_NODE_SIZE)
        
        all_keys = set(list(self.start_coords.keys()) + list(self.target_coords.keys()))
        for val in all_keys:
            start_c = self.start_coords.get(val, self.target_coords.get(val))
            target_c = self.target_coords.get(val, self.start_coords.get(val))
            
            if start_c and target_c:
                sx, sy = start_c
                tx, ty = target_c
                cx = sx + (tx - sx) * t
                cy = sy + (ty - sy) * t
                current_coords[val] = (cx, cy)
            elif start_c:
                current_coords[val] = start_c
            elif target_c:
                current_coords[val] = target_c

        def _draw_anim_node(n):
            if n is None or n.val not in current_coords:
                return

            x, y = current_coords[n.val]

            if n.parent and n.parent.val in current_coords:
                px, py = current_coords[n.parent.val]
                self.ax.plot([px, x], [py, y], color='gray', linestyle='-', linewidth=1.5, zorder=1)

            current_color = DEFAULT_NODE_COLOR
            if n.val in self.start_coords or n.val in self.target_coords:
                current_color = ROTATION_COLOR

            circle = patches.Circle((x, y), node_size, facecolor=current_color, edgecolor='black', linewidth=1.5, zorder=2)
            self.ax.add_patch(circle)

            label = f"{n.val}"
            if n.freq > 1:
                label += f"-{n.freq}"

            font_size = max(8, int(10 * (node_size / DEFAULT_NODE_SIZE)))
            self.ax.text(x, y, label, ha='center', va='center', fontsize=font_size, color='white', zorder=3)
            
            bf = self.tree._balance_factor(n)
            bf_color = IMBALANCED_TEXT_COLOR if abs(bf) > 1 else 'black'
            bf_font_size = max(6, int(8 * (node_size / DEFAULT_NODE_SIZE)))
            self.ax.text(x, y + node_size + 0.05, f"h={n.height}", ha='center', va='center', fontsize=bf_font_size, color='black', zorder=3)
            self.ax.text(x, y - node_size - 0.05, f"bf={bf}", ha='center', va='center', fontsize=bf_font_size, color=bf_color, zorder=3)

            _draw_anim_node(n.left)
            _draw_anim_node(n.right)
        
        # 修正缩进：这一行应该在 _draw_anim_node 函数定义之外
        _draw_anim_node(self.tree.root)
        
        if current_coords:
            all_c = current_coords.values()
            xs = [x for x, _ in all_c]
            ys = [y for _, y in all_c]
            if xs and ys:
                self.ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
                self.ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
                
        self.canvas.draw_idle()

    # 查找路径动画
    def _animate_special_path(self, path, final_node):
        self.path_nodes = path
        self.path_index = 0
        self.path_timer.stop()
        
        op = ""
        if hasattr(self, 'current_op'):
            if self.current_op == 'predecessor':
                op = "查找前驱"
            elif self.current_op == 'successor':
                op = "查找后继"
            elif self.current_op == 'lower_bound':
                op = "查找lower_bound"
            elif self.current_op == 'search':
                op = "查找"
        
        def animate_step():
            if self.path_index < len(self.path_nodes):
                n = self.path_nodes[self.path_index]
                
                self.draw_tree(self.tree.root, highlight_path=self.path_nodes[:self.path_index], highlight=n, show_bf=True)
                
                if self.path_index < len(self.path_nodes) - 1:
                    self.add_step(f"{op}：正在比较节点 {n.val}")
                
                self.path_index += 1
            else:
                self.path_timer.stop()
                if final_node:
                    self.draw_tree(self.tree.root, highlight=final_node, show_bf=True)
                    self.add_step(f"{op}成功：结果节点 {final_node.val}")
                else:
                    self.draw_tree(self.tree.root, show_bf=True)
                    self.add_step(f"{op}失败：未找到目标")
                    
                QTimer.singleShot(500, lambda: self.draw_tree(self.tree.root, show_bf=True))

        self.path_timer.timeout.disconnect()
        self.path_timer.timeout.connect(animate_step)
        self.path_timer.start(200)

    # 辅助方法：延迟绘制
    def _delayed_draw(self, delay_ms, callback, *args, **kwargs):
        QCoreApplication.processEvents()
        QTimer.singleShot(delay_ms, lambda: callback(*args, **kwargs))

    # 操作实现
    def insert(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"外部执行插入操作：{val}")
        self.tree.insert(val, step_callback=self.add_step)

    def search(self):
        val = self._get_int()
        if val is None:
            return
        self.current_op = 'search'
        self.add_step(f"开始搜索值：{val}")
        self.tree.search(val, step_callback=self.add_step)

    def delete(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"外部执行删除操作：{val}")
        self.tree.delete(val, step_callback=self.add_step)
        
    def show_inorder(self):
        if not self.tree.root:
            QMessageBox.warning(self, "错误", "树为空")
            return
        seq = self.tree.inorder()
        seq_text = " -> ".join(map(str, seq))
        self.status.setText(f"中序遍历（递增序列）: {seq_text}")
        self.add_step(f"中序遍历结果（AVL特性：递增）：{seq_text}")

    def random_build(self):
        n = self.spinN.value()
        self.add_step(f"开始随机生成 {n} 个节点的AVL树（值范围：1-100）")
        values = self.tree.build_random(n=n, value_range=(1, 100), step_callback=self.add_step)
        self.add_step(f"生成完成，值序列：{values}")
        self.status.setText(f"随机生成 {n} 个节点: {values}")

    def find_predecessor(self):
        val = self._get_int()
        if val is None:
            return
        self.current_op = 'predecessor'
        self.add_step(f"查找值 {val} 的前驱（中序遍历前一个节点）")
        self.tree.predecessor(val, step_callback=self.add_step)

    def find_successor(self):
        val = self._get_int()
        if val is None:
            return
        self.current_op = 'successor'
        self.add_step(f"查找值 {val} 的后继（中序遍历后一个节点）")
        self.tree.successor(val, step_callback=self.add_step)

    def find_lower_bound(self):
        val = self._get_int()
        if val is None:
            return
        self.current_op = 'lower_bound'
        self.add_step(f"查找值 {val} 的lower_bound（首个≥{val}的节点）")
        self.tree.lower_bound(val, step_callback=self.add_step)
        
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

    def add_step(self, text):
        current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.step_text.append(f"[{current_time}] {text}")
        QTimer.singleShot(0, lambda: self.step_text.verticalScrollBar().setValue(
            self.step_text.verticalScrollBar().maximum()
        ))

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
            file = QFile(file_path)
            if file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(file)
                content = stream.readAll()
                file.close()
                
                self.tree.root = None
                self.draw_tree(None)
                
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

    def load_example_code(self):
        """加载示例DSL代码"""
        example_code = """clear
insert 50
insert 30
insert 70
insert 20
insert 40
insert 60
insert 80
inorder
delete 50
predecessor 60
successor 40
lower_bound 55
random 5"""
        self.dsl_editor.setPlainText(example_code)
        self.add_step("已加载示例DSL代码")

