# gui/StackWindow.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QStatusBar, QFileDialog, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import json
import os
import random
# 假设 core/stack.py 存在并提供 Stack 类
from core.stack import Stack 

# 配置matplotlib中文字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
matplotlib.rcParams['axes.unicode_minus'] = False

class StackWindow(QMainWindow):
    """栈可视化窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("栈可视化系统（LIFO）")
        self.resize(800, 600)
        
        # 核心数据结构
        self.stack = Stack()
        self.selected_node_idx = None  # 当前选中的节点索引
        self.operation_log = []  # 操作日志
        
        # 动画状态
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate_step)
        self.anim_steps = []  # 动画步骤队列
        self.anim_index = 0  # 当前动画步骤索引
        
        # 初始化UI
        self._init_ui()
        self._draw_stack()

    def _init_ui(self):
        """初始化界面布局"""
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. 可视化画布
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.canvas.mpl_connect("pick_event", self._on_node_click)
        main_layout.addWidget(self.canvas, stretch=1)

        # 2. 操作控件区
        ctrl_layout = QHBoxLayout()
        main_layout.addLayout(ctrl_layout)

        # 数据输入
        ctrl_layout.addWidget(QLabel("数据："))
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText(f"输入{-self.stack.MIN_VAL}~{self.stack.MAX_VAL}的整数")
        self.data_input.setMaximumWidth(100)
        ctrl_layout.addWidget(self.data_input)

        # 操作按钮
        self.btn_push = QPushButton("入栈")
        self.btn_push.clicked.connect(self._push)
        ctrl_layout.addWidget(self.btn_push)

        self.btn_pop = QPushButton("出栈")
        self.btn_pop.clicked.connect(self._pop)
        ctrl_layout.addWidget(self.btn_pop)

        self.btn_peek = QPushButton("查看栈顶")
        self.btn_peek.clicked.connect(self._peek)
        ctrl_layout.addWidget(self.btn_peek)

        self.btn_clear = QPushButton("清空栈")
        self.btn_clear.clicked.connect(self._clear_stack)
        ctrl_layout.addWidget(self.btn_clear)

        self.btn_random = QPushButton("随机生成")
        self.btn_random.clicked.connect(self._random_generate)
        ctrl_layout.addWidget(self.btn_random)

        # 3. 文件操作区
        file_layout = QHBoxLayout()
        main_layout.addLayout(file_layout)

        self.btn_save = QPushButton("保存栈结构")
        self.btn_save.clicked.connect(self._save_structure)
        file_layout.addWidget(self.btn_save)

        self.btn_load = QPushButton("加载栈结构")
        self.btn_load.clicked.connect(self._load_structure)
        file_layout.addWidget(self.btn_load)

        # 4. 操作日志区
        log_layout = QHBoxLayout()
        main_layout.addLayout(log_layout)

        log_label = QLabel("操作日志：")
        log_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        log_layout.addWidget(self.log_text, stretch=1)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"就绪 - 栈容量：0/{self.stack.MAX_SIZE}")

    # ------------------------------ 核心操作 ------------------------------
    def _get_input_data(self) -> int:
        """获取输入数据并验证"""
        try:
            data = int(self.data_input.text().strip())
            if not (self.stack.MIN_VAL <= data <= self.stack.MAX_VAL):
                raise ValueError
            return data
        except ValueError:
            QMessageBox.warning(self, "输入错误", f"请输入{-self.stack.MIN_VAL}~{self.stack.MAX_VAL}的整数")
            return None

    def _push(self):
        """入栈"""
        data = self._get_input_data()
        if data is None:
            return

        try:
            self._start_animation("push", data)
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _pop(self):
        """出栈"""
        try:
            self._start_animation("pop")
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _peek(self):
        """查看栈顶"""
        if self.stack.is_empty():
            QMessageBox.information(self, "提示", "栈为空")
            return

        top_data = self.stack.peek()
        QMessageBox.information(self, "栈顶元素", f"当前栈顶数据：{top_data}")
        self._log_operation(f"查看栈顶，数据为{top_data}")

    # ------------------------------ 辅助操作 ------------------------------
    def _clear_stack(self):
        """清空栈"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法清空")
            return

        self.stack.clear()
        self.selected_node_idx = None
        self._log_operation("清空栈")
        self._draw_stack()
        self.status_bar.showMessage(f"就绪 - 栈容量：0/{self.stack.MAX_SIZE}")

    def _random_generate(self):
        """随机生成栈（2-5个节点）"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法生成")
            return

        self.stack.clear()
        node_count = random.randint(2, 5)
        for _ in range(node_count):
            data = random.randint(self.stack.MIN_VAL, self.stack.MAX_VAL)
            self.stack.push(data)
        
        self._log_operation(f"随机生成{node_count}个元素的栈")
        self._draw_stack()

    def _save_structure(self):
        """保存栈结构到JSON文件"""
        if self.stack.is_empty():
            QMessageBox.warning(self, "警告", "空栈无法保存")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "保存栈", ".", "JSON文件 (*.json)"
        )
        if not filename:
            return

        save_data = {
            "type": "stack",
            "data": self.stack.to_list()
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        self._log_operation(f"保存栈到{os.path.basename(filename)}")
        self.status_bar.showMessage(f"已保存到{os.path.basename(filename)}")

    def _load_structure(self):
        """从JSON文件加载栈结构"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法加载")
            return

        filename, _ = QFileDialog.getOpenFileName(
            self, "加载栈", ".", "JSON文件 (*.json)"
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                load_data = json.load(f)
            
            if load_data.get("type") != "stack":
                raise ValueError("不是栈结构文件")
            
            data = load_data.get("data", [])
            # 清空并恢复栈
            self.stack.clear()
            # 注意: 栈的 to_list() 应该是从栈底到栈顶，所以直接 push 即可
            for val in data:
                self.stack.push(val)
            
            self._log_operation(f"从{os.path.basename(filename)}加载栈")
            self._draw_stack()
        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"文件格式错误：{str(e)}")

    # ------------------------------ 动画控制 ------------------------------
    def _start_animation(self, op_type: str, data: int = None):
        """开始动画"""
        if self.anim_timer.isActive():
            return

        # 检查容量限制
        if op_type == "push" and self.stack.is_full():
             raise Exception("栈已满，无法入栈")
        if op_type == "pop" and self.stack.is_empty():
             raise Exception("栈为空，无法出栈")

        # 生成动画步骤
        self.anim_steps = []
        visual_data = self.stack.get_visual_data()

        if op_type == "push":
            # 入栈动画：高亮栈顶（即下一个入栈的位置） -> 入栈 -> 恢复颜色
            # 栈顶索引在 visual_data 中是 0，因为它是 LIFO 结构
            self.anim_steps.append(("highlight", 0, 0.3))
            self.anim_steps.append(("push", data))
            self.anim_steps.append(("restore", 0))
            self._log_operation(f"入栈数据{data}")
        elif op_type == "pop":
            # 出栈动画：高亮栈顶 -> 移除栈顶 -> 重新布局
            # 栈顶索引始终是 0
            self.anim_steps.append(("highlight", 0, 0.8))
            self.anim_steps.append(("pop",))
            self.anim_steps.append(("restore", 0)) # 恢复，因为栈顶已变化
            self._log_operation("出栈")

        # 开始动画
        self.anim_index = 0
        self._disable_buttons(True)
        self.anim_timer.start(300)  # 300ms/帧

    def _animate_step(self):
        """动画步骤执行"""
        if self.anim_index >= len(self.anim_steps):
            # 动画结束
            self.anim_timer.stop()
            self._disable_buttons(False)
            self._draw_stack()
            return

        step = self.anim_steps[self.anim_index]
        self.anim_index += 1
        op = step[0]

        if op == "highlight":
            # 高亮目标位置
            idx, alpha = step[1], step[2]
            self._draw_stack(highlight_idx=idx, highlight_alpha=alpha)
        elif op == "restore":
            # 恢复颜色
            self._draw_stack()
        elif op == "push":
            # 执行入栈
            data = step[1]
            self.stack.push(data)
        elif op == "pop":
            # 执行出栈
            self.stack.pop()

    def _disable_buttons(self, disable: bool):
        """禁用/启用操作按钮"""
        buttons = [
            self.btn_push, self.btn_pop, self.btn_peek,
            self.btn_clear, self.btn_random, self.btn_save, self.btn_load
        ]
        for btn in buttons:
            btn.setEnabled(not disable)

    # ------------------------------ 绘图逻辑 ------------------------------
    def _draw_stack(self, highlight_idx: int = None, highlight_alpha: float = 1.0):
        """
        绘制栈。已修正栈顶(TOP)在上方，栈底(BOTTOM)在下方的逻辑。
        假设：visual_data["nodes"] 列表是 [栈顶, ..., 栈底] 的顺序。
        """
        self.ax.clear()
        self.ax.set_xlim(300, 400)
        self.ax.set_ylim(50, 600)
        self.ax.axis("off")

        visual_data = self.stack.get_visual_data()
        nodes = visual_data["nodes"]
        stack_size = visual_data["size"]
        max_size = visual_data["max_size"]
        
        # 基础坐标定义
        STACK_BASE_Y = 100
        NODE_HEIGHT = 40
        NODE_SPACING = 50 # 50 = 40 + 10 间隔
        STACK_HEIGHT = NODE_SPACING * max_size

        # 绘制栈框 (栈底在 y=100)
        self.ax.add_patch(
            patches.Rectangle(
                (310, STACK_BASE_Y), 80, STACK_HEIGHT, # 绘制栈框高度
                linewidth=3, edgecolor="#888888", facecolor="none"
            )
        )
        
        # 绘制栈顶/栈底标记 (修正：栈顶在上方，栈底在下方)
        self.ax.text(350, STACK_BASE_Y + STACK_HEIGHT + 10, "栈顶", ha="center", va="bottom", fontsize=12, color="red")
        self.ax.text(350, STACK_BASE_Y - 10, "栈底", ha="center", va="top", fontsize=12, color="blue")

        # 绘制节点 (从栈顶开始绘制，y坐标从高到低)
        # 栈顶是 nodes[0]，栈底是 nodes[-1]
        for i, node in enumerate(nodes):
            # i = 0 是栈顶元素，i = stack_size - 1 是栈底元素
            
            # 计算 y 坐标：栈底 Y + 栈底到当前节点占用的空间 - 节点高度
            # nodes 列表是 [栈顶, ..., 栈底] 的顺序
            # 栈底元素 (nodes[-1]) 应该在 Y=100 处
            # 栈顶元素 (nodes[0]) 应该在最高处
            
            # 计算节点在栈中的实际位置 (从 0 开始，0是栈底)
            stack_pos = stack_size - 1 - i 
            
            # y 坐标：栈底 Y + 节点在栈中的位置 * 间隔 + 10 (底部留白)
            y = STACK_BASE_Y + stack_pos * NODE_SPACING + (NODE_SPACING - NODE_HEIGHT)
            x = 350 - 25 # 居中

            width, height = 50, NODE_HEIGHT

            # 节点颜色
            color = node["color"]
            
            # 修正：visual_data 的索引 0 永远是栈顶，但栈顶是动态变化的。
            # 如果是 pop 或 push 动画，highlight_idx=0 始终针对当前/下一个栈顶元素
            if highlight_idx is not None and i == highlight_idx:
                color = f"#FFD700{int(highlight_alpha*255):02X}"  # 高亮：金色透明
            elif self.selected_node_idx is not None and i == self.selected_node_idx:
                 color = "#FF6347"  # 选中节点：珊瑚红

            # 绘制矩形节点
            rect = patches.Rectangle(
                (x, y), width, height,
                linewidth=2, edgecolor="black",
                facecolor=color, alpha=0.9,
                picker=True  # 支持点击选择
            )
            # 存储其在 visual_data 列表中的索引
            rect.index = i 
            self.ax.add_patch(rect)

            # 绘制节点文本（数据）
            self.ax.text(
                x + width/2, y + height/2, node["label"],
                ha="center", va="center", fontsize=12, fontweight="bold"
            )

            # 绘制栈顶标记 (修正：只在最高元素上方显示)
            if node["is_top"]:
                # 栈顶 (i=0) 元素上方的 y 坐标
                self.ax.text(x + width/2, y + height + 5, "TOP", ha="center", va="bottom", fontsize=10, color="red")

        # 更新状态栏
        self.status_bar.showMessage(f"就绪 - 栈容量：{stack_size}/{max_size}")
        self.canvas.draw_idle()

    # ------------------------------ 事件处理 ------------------------------
    def _on_node_click(self, event):
        """节点点击事件"""
        if self.anim_timer.isActive():
            return

        artist = event.artist
        if hasattr(artist, "index"):
            # 切换选中状态
            if self.selected_node_idx == artist.index:
                self.selected_node_idx = None
                self.status_bar.showMessage(f"就绪 - 栈容量：{self.stack.size}/{self.stack.MAX_SIZE}")
            else:
                self.selected_node_idx = artist.index
                # 显示节点信息
                # artist.index 是 visual_data 中从栈顶开始的索引
                node_data = self.stack.to_list()[-1 - artist.index] # 假设 to_list 是 [栈底...栈顶]
                self.status_bar.showMessage(f"选中节点：位置 (栈顶算起) {artist.index + 1}，数据 {node_data}")
            
            self._draw_stack()

    # ------------------------------ 日志记录 ------------------------------
    def _log_operation(self, content: str):
        """记录操作日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.operation_log.append(f"[{time_str}] {content}")
        # 只保留最近20条日志
        if len(self.operation_log) > 20:
            self.operation_log.pop(0)
        # 更新日志显示
        self.log_text.setText("\n".join(self.operation_log))