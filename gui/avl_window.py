# gui/avl_window.py - MODIFIED
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QSpinBox, QTextEdit, QFileDialog, QScrollBar
)
from PySide6.QtCore import QTimer, QDateTime, QIODevice, QTextStream, QCoreApplication # ADDED QCoreApplication
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import copy # ADDED copy
from core.avl_tree import AVLTree

# 定义颜色常量
HIGHLIGHT_COLOR = '#32CD32'  # 绿色：当前检查节点
ROTATION_COLOR = '#FF6347'   # 红色/橙红：失衡点或旋转相关节点
PATH_COLOR = '#FFA500'       # 橙色：新插入/路径节点
DEFAULT_NODE_COLOR = '#87CEFA' # 蓝色：普通节点
IMBALANCED_TEXT_COLOR = 'red' # 红色：失衡时文本颜色

class AVLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVL树可视化 - 自平衡二叉搜索树")
        self.resize(1400, 700)

        # 初始化核心数据结构
        self.tree = AVLTree()
        self.tree.add_listener(self.on_update)
        self.state_list = []  # 用于存储状态快照

        # 初始化图形对象
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.coords = {}  # 节点坐标映射
        self.node_artists = []  # 用于存储节点图形对象，实现点击功能

        # 初始化动画相关变量
        self.animating = False  # 动画状态标记
        self.animation_steps = 20  # 动画总步数
        self.current_step = 0  # 当前动画步数
        self.start_coords = {}  # 旋转前节点坐标
        self.target_coords = {}  # 旋转后节点坐标
        self.rotation_highlight = None # 旋转高亮节点信息
        self.animation_timer = QTimer() # 旋转动画计时器
        self.animation_timer.timeout.connect(self._animate_rotation)
        
        self.path_timer = QTimer() # 路径动画计时器（查找）
        self.path_nodes = []
        self.path_index = 0
        self.current_op_details = None 

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
        

    # 辅助函数：实现延迟绘制和暂停效果
    def _delayed_draw(self, delay_ms, callback, *args, **kwargs):
        """用 QTimer 实现延迟调用绘图函数，以达到暂停效果"""
        
        # 强制处理事件，避免在大量通知时卡住
        QCoreApplication.processEvents()
        
        # 使用 singleShot 实现延迟
        QTimer.singleShot(delay_ms, lambda: callback(*args, **kwargs))

    # 树的布局计算
    def _calculate_coords(self, node, x=0, y=0, level=1, calculate_only=False):
        """计算节点坐标，使用 AVL 树惯用的水平分隔策略"""
        if node is None:
            return

        H_SEP = 1.0 / (2 ** (level - 1))
        coords = {}

        def _layout(node, x, y, level, h_sep):
            if node is None:
                return
            
            # 递归左子树
            _layout(node.left, x - h_sep, y - 1, level + 1, h_sep / 2)
            
            # 记录当前节点坐标
            coords[node.val] = (x, y)
            
            # 递归右子树
            _layout(node.right, x + h_sep, y - 1, level + 1, h_sep / 2)

        _layout(node, x, y, level, H_SEP)

        if calculate_only:
            return coords
        else:
            self.coords = coords


    # 绘制树结构 (修改以支持多种高亮和颜色)
    def draw_tree(self, node, highlight=None, highlight_pair=None, highlight_path=None, show_bf=False, node_color=DEFAULT_NODE_COLOR, bf_text_color='black'):
        self.ax.clear()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')
        self.node_artists = []
        
        # 1. 计算坐标 (始终需要计算以确保布局正确)
        self._calculate_coords(node, x=0, y=0)

        if not node:
            self.ax.text(0.5, 0.5, "(空树)", ha="center", va="center", fontsize=16, color="gray")
            self.canvas.draw_idle()
            return
            
        # 2. 设置绘图范围
        all_coords = self.coords.values()
        xs = [x for x, _ in all_coords]
        ys = [y for _, y in all_coords]
        if xs and ys:
            self.ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
            self.ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
        
        
        # 3. 递归绘制
        def _draw_node_recursive(n):
            if n is None or n.val not in self.coords:
                return
                
            x, y = self.coords[n.val]
            
            # 绘制连线
            if n.parent and n.parent.val in self.coords:
                px, py = self.coords[n.parent.val]
                line_color = PATH_COLOR if highlight_path and n.parent in highlight_path else 'gray'
                self.ax.plot([px, x], [py, y], color=line_color, linestyle='-', linewidth=1.5, zorder=1)
                
            # 确定节点颜色 (优先级: highlight_pair > highlight > highlight_path > default_color)
            current_color = node_color
            text_color = 'white'
            lw = 1

            # 旋转/失衡高亮 (最高优先级)
            if highlight_pair and any(hn and n.val == hn.val for hn in highlight_pair):
                current_color = ROTATION_COLOR
                lw = 2
            # 单节点高亮 (检查平衡/新插入)
            elif highlight and n.val == highlight.val:
                current_color = HIGHLIGHT_COLOR if node_color == DEFAULT_NODE_COLOR else node_color # 保持传入的颜色
                lw = 2
            # 路径高亮 (查找路径)
            elif highlight_path and n in highlight_path:
                current_color = PATH_COLOR
            # 基础颜色 (如果传入了非默认颜色，则使用传入的颜色)
            elif node_color != DEFAULT_NODE_COLOR:
                 current_color = node_color


            # 绘制节点圆
            circle = patches.Circle((x, y), 0.35, facecolor=current_color, edgecolor='black', linewidth=lw, zorder=2)
            self.ax.add_patch(circle)
            self.node_artists.append((circle, n))

            # 绘制值
            label = f"{n.val}"
            if n.freq > 1:
                label += f"-{n.freq}"
            
            self.ax.text(x, y, label, ha='center', va='center', fontsize=10, color=text_color, zorder=3)
            
            # 绘制平衡因子和高度
            if show_bf:
                bf = self.tree._balance_factor(n)
                # 平衡因子文本颜色
                bf_c = IMBALANCED_TEXT_COLOR if abs(bf) > 1 else bf_text_color
                
                # 绘制高度
                self.ax.text(x, y + 0.45, f"h={n.height}", ha='center', va='center', fontsize=8, color='black', zorder=3)
                # 绘制平衡因子
                self.ax.text(x, y - 0.45, f"bf={bf}", ha='center', va='center', fontsize=8, color=bf_c, zorder=3)
            
            _draw_node_recursive(n.left)
            _draw_node_recursive(n.right)
            
        _draw_node_recursive(node)
        self.canvas.draw_idle()


    # 核心：AVL树状态更新回调函数
    def on_update(self, state):
        action = state.get("action")
        node = state.get("node")
        extra = state.get("extra") or {}
        
        # 查找动画正在进行时，忽略平衡检查通知
        if self.path_timer.isActive() and action not in ("found", "not_found", "trace_path"):
             return
        
        # 1. BST插入/删除完成
        if action in ("bst_insert_complete", "bst_delete_complete"):
            val = node.val if node else "?"
            status_text = "插入" if action == "bst_insert_complete" else "删除"
            self.status.setText(f"BST{status_text}完成：节点 {val}，准备检查平衡")
            
            # 【显示此时的BST树，并高亮新插入的结点，停留0.1秒】
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight=node, 
                                show_bf=True, 
                                node_color=PATH_COLOR) # 新节点使用路径色
            return

        # 2. 检查节点平衡 (正常或失衡)
        if action == "check_balance":
            bf = extra.get("bf")
            is_balanced = extra.get("is_balanced")
            status = "正常" if is_balanced else "失衡"
            self.status.setText(f"检查节点 {node.val}，平衡因子={bf}（{status}）")

            # 【高亮节点 N，停留1秒】/ 【当平衡因子失衡，字体变为红色，停留0.1秒】
            delay = 100
            # 平衡检查时，正常节点用 HIGHLIGHT_COLOR，失衡节点用 ROTATION_COLOR
            node_color = HIGHLIGHT_COLOR if is_balanced else ROTATION_COLOR
            # 平衡因子文本颜色：失衡时用红色，否则用黑色
            text_color = 'black' if is_balanced else IMBALANCED_TEXT_COLOR
            
            self._delayed_draw(delay, self.draw_tree, 
                                self.tree.root, 
                                highlight=node, 
                                show_bf=True, 
                                node_color=node_color,
                                bf_text_color=text_color)
            return

        # 3. 移动到父节点
        if action == "move_to_parent":
            next_node = extra.get("next_node")
            self.status.setText(f"移动到父节点 {next_node.val} 继续检查")
            
            # 【高亮父节点，停留0.1秒】
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight=next_node, 
                                show_bf=True, 
                                node_color=PATH_COLOR)
            return

        # 4. 失衡准备 (左/右偏失衡)
        if action in ("left_imbalance", "right_imbalance"):
            child = extra.get("child")
            
            # 确定要高亮的三个节点 (失衡点, 子节点, 孙节点)
            highlight_pair = [node, child]
            if child:
                # 左旋或右旋中点 (用于双旋：左右或右左)
                # extra["type"] 在 avl_tree.py 的 rotation_prepare 中定义了，此处简化判断
                if extra.get("type") == "Left-Right" and child.right:
                    highlight_pair.append(child.right)
                elif extra.get("type") == "Right-Left" and child.left:
                    highlight_pair.append(child.left)
            
            # 【高亮要旋转的三个结点，停留0.1秒】
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                highlight_pair=highlight_pair, 
                                show_bf=True, 
                                node_color=ROTATION_COLOR,
                                bf_text_color=IMBALANCED_TEXT_COLOR)
            return

        # 5. 旋转准备：记录坐标，但不立即绘制（由上一步的 delayed_draw 负责暂停和高亮）
        if action == "rotation_prepare":
            # 记录旋转相关信息，用于动画期间的高亮
            self.rotation_highlight = extra 
            
            # 确保当前树已绘制且 coords 已更新（这由上一步的 draw_tree 保证）
            self.start_coords = self.coords.copy() 
            return

        # 6. 旋转完成：记录目标坐标并启动动画
        if action == "rotation":
            # 绘制最新树（此时数据结构已更新），记录 target_coords
            self._calculate_coords(self.tree.root, calculate_only=False) # 重新计算新的 coords
            self.target_coords = self.coords.copy()
            
            # 启动动画
            if self.start_coords and self.target_coords:
                self.animating = True
                self.current_step = 0
                self.animation_timer.start(30) # 30ms 启动动画
            else:
                 # 没有 start_coords，直接绘制最终状态
                self.draw_tree(self.tree.root, show_bf=True)
            
            # 清除 start_coords 以免误用（下一次旋转重新准备）
            self.start_coords = {}
            return

        # 7. 平衡检查完成
        if action == "balance_complete":
            self.status.setText("所有节点检查完毕，树已平衡")
            
            # 树已平衡，最终状态显示，取消所有高亮，停留0.1秒
            self._delayed_draw(1000, self.draw_tree, 
                                self.tree.root, 
                                show_bf=True, 
                                node_color=DEFAULT_NODE_COLOR)
            # 清除旋转高亮信息
            self.rotation_highlight = None
            return
            
        # 查找路径高亮 (使用 QTimer 实现动画)
        if action == "trace_path":
            self._animate_special_path(extra, node)
            return
            
        # 其他动作（insert, delete, found, not_found, build）可以立即绘制
        if action in ("insert", "delete", "found", "not_found", "increase_freq", "decrease_freq", "build"):
            # 随机生成后立即绘制最终树
            if action == "build":
                self.draw_tree(self.tree.root, show_bf=True)
                return

            # 其他操作（非平衡检查和旋转）的即时绘制
            highlight_node = node if action in ("insert", "found", "increase_freq", "decrease_freq") else None
            self.draw_tree(self.tree.root, highlight=highlight_node, show_bf=True)
            return

    # 动画绘制（旋转）
    def _animate_rotation(self):
        """旋转动画帧更新"""
        self.current_step += 1
        
        # 当动画结束
        if self.current_step > self.animation_steps:
            self.animating = False
            self.animation_timer.stop()
            self.current_step = 0
            # 动画结束后，继续高亮旋转后的节点（直到平衡检查完成）
            # 此时的 self.tree.root 已经是旋转后的新树结构
            # 确保传递一个高亮集合，例如包含旋转后的新根
            highlight_pair = []
            if self.tree.root:
                 # 简单地高亮根节点及其子节点（如果存在）作为指示
                 pivot = self.tree.root # 假设旋转后的节点成为了局部根
                 if self.rotation_highlight and self.rotation_highlight.get("pivot"):
                     pivot_val = self.rotation_highlight.get("pivot")
                     # 找到旋转后的 pivot 节点，并高亮它和它的子节点
                     def find_node(n, val):
                         if not n: return None
                         if n.val == val: return n
                         return find_node(n.left, val) or find_node(n.right, val)

                     pivot_node = find_node(self.tree.root, pivot_val)
                     if pivot_node:
                          highlight_pair.append(pivot_node)
                          if pivot_node.left: highlight_pair.append(pivot_node.left)
                          if pivot_node.right: highlight_pair.append(pivot_node.right)
                          
            self.draw_tree(self.tree.root, highlight_pair=highlight_pair, show_bf=True, node_color=ROTATION_COLOR)
            return

        t = self.current_step / float(self.animation_steps)  # 0~1之间的插值因子

        # 清除画布
        self.ax.clear()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')

        current_coords = {}
        
        # 线性插值计算当前坐标
        all_keys = set(list(self.start_coords.keys()) + list(self.target_coords.keys()))
        for val in all_keys:
            # 使用节点的 val 属性而不是节点对象作为 key
            start_c = self.start_coords.get(val, self.target_coords.get(val))
            target_c = self.target_coords.get(val, self.start_coords.get(val))
            
            if start_c and target_c:
                sx, sy = start_c
                tx, ty = target_c
                cx = sx + (tx - sx) * t
                cy = sy + (ty - sy) * t
                current_coords[val] = (cx, cy)
            elif start_c: # Node that disappeared (deletion/replaced)
                current_coords[val] = start_c
            elif target_c: # Node that appeared (new root of subtree)
                 current_coords[val] = target_c


        # 绘制当前动画状态
        def _draw_anim_node(n):
            if n is None or n.val not in current_coords:
                return

            x, y = current_coords[n.val]

            # 绘制连线
            if n.parent and n.parent.val in current_coords:
                px, py = current_coords[n.parent.val]
                self.ax.plot([px, x], [py, y], color='gray', linestyle='-', linewidth=1.5, zorder=1)

            # 确定高亮状态（旋转期间高亮旋转节点）
            current_color = DEFAULT_NODE_COLOR
            # 旋转期间所有涉及的节点都高亮 ROTATION_COLOR
            if n.val in self.start_coords or n.val in self.target_coords:
                 current_color = ROTATION_COLOR
            # elif self.rotation_highlight and n.val in [self.rotation_highlight.get("node"), self.rotation_highlight.get("pivot")]:
            #      current_color = ROTATION_COLOR


            # 绘制节点圆
            circle = patches.Circle((x, y), 0.35, facecolor=current_color, edgecolor='black', linewidth=1.5, zorder=2)
            self.ax.add_patch(circle)

            # 绘制值
            label = f"{n.val}"
            if n.freq > 1:
                label += f"-{n.freq}"

            self.ax.text(x, y, label, ha='center', va='center', fontsize=10, color='white', zorder=3)
            
            # 绘制平衡因子和高度（使用最新的计算值，但绘制在过渡坐标上）
            bf = self.tree._balance_factor(n)
            bf_color = IMBALANCED_TEXT_COLOR if abs(bf) > 1 else 'black'
            self.ax.text(x, y + 0.45, f"h={n.height}", ha='center', va='center', fontsize=8, color='black', zorder=3)
            self.ax.text(x, y - 0.45, f"bf={bf}", ha='center', va='center', fontsize=8, color=bf_color, zorder=3)

            # 递归绘制子节点
            _draw_anim_node(n.left)
            _draw_anim_node(n.right)
            
        _draw_anim_node(self.tree.root)
        
        # 设置绘图范围
        if current_coords:
             all_c = current_coords.values()
             xs = [x for x, _ in all_c]
             ys = [y for _, y in all_c]
             if xs and ys:
                 self.ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
                 self.ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
                 
        self.canvas.draw_idle()

    # 查找路径动画逻辑 (与原来的 _animate_special_path 和 _animate_trace 结合)
    def _animate_special_path(self, path, final_node):
        """处理查找路径的动画"""
        self.path_nodes = path
        self.path_index = 0
        self.path_timer.stop() # 停止旧的计时器
        
        op = "" 
        
        def animate_step():
            if self.path_index < len(self.path_nodes):
                n = self.path_nodes[self.path_index]
                
                # 绘制当前路径，并高亮当前节点
                self.draw_tree(self.tree.root, highlight_path=self.path_nodes[:self.path_index], highlight=n, show_bf=True)
                
                # 更新步骤文本 (如果需要)
                if self.path_index < len(self.path_nodes) - 1:
                    self.add_step(f"{op}：正在比较节点 {n.val}")
                
                self.path_index += 1
            else:
                self.path_timer.stop()
                if final_node:
                    # 最终找到的节点高亮
                    self.draw_tree(self.tree.root, highlight=final_node, show_bf=True)
                    self.add_step(f"{op}成功：结果节点 {final_node.val}")
                else:
                    # 未找到结果，清除路径高亮
                    self.draw_tree(self.tree.root, show_bf=True)
                    self.add_step(f"{op}失败：未找到目标")
                    
                # 最终状态停留 500ms 后清除高亮
                QTimer.singleShot(500, lambda: self.draw_tree(self.tree.root, show_bf=True))

        self.path_timer.timeout.disconnect() # 断开旧连接
        self.path_timer.timeout.connect(animate_step)
        self.path_timer.start(200) # 每 200ms 走一步，实现路径动画

    # ... (其他方法保持不变)
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
        self.add_step(f"查找值 {val} 的前驱（中序遍历前一个节点）")
        self.tree.predecessor(val, step_callback=self.add_step)

    def find_successor(self):
        val = self._get_int()
        if val is None:
            return
        self.add_step(f"查找值 {val} 的后继（中序遍历后一个节点）")
        self.tree.successor(val, step_callback=self.add_step)

    def find_lower_bound(self):
        val = self._get_int()
        if val is None:
            return
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