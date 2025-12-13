from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QSpinBox, QComboBox, QMessageBox, QStatusBar,
    QFileDialog, QTextEdit, QSplitter
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPen, QBrush
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import json
import os
import random
from core.list import List

# 配置matplotlib中文字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
matplotlib.rcParams['axes.unicode_minus'] = False
from dsl.list.list_dsl_parser import ListDSLParser
from dsl.list.list_dsl_executor import ListDSLExecutor


class ListWindow(QMainWindow):
    """链表可视化窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("单链表/双链表可视化系统")
        self.resize(1300, 700)  # 加宽窗口以容纳DSL面板
        self.dsl_parser = ListDSLParser()
        self.dsl_executor = ListDSLExecutor(self)

        # 核心数据结构
        self.list = List(mode="singly")  # 默认单链表
        self.selected_node_id = None  # 当前选中的节点ID
        self.operation_log = []  # 操作日志
        
        # 动画状态
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate_step)
        self.anim_steps = []  # 动画步骤队列
        self.anim_index = 0  # 当前动画步骤索引
        
        # 初始化UI
        self._init_ui()
        self._draw_list()

    def _init_ui(self):
        """初始化界面布局"""
        # 主分割器（左侧DSL面板，右侧原有功能区）
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)
        
        # ======================== 左侧DSL面板 ========================
        dsl_widget = QWidget()
        dsl_layout = QVBoxLayout(dsl_widget)
        dsl_widget.setMinimumWidth(350)
        
        # DSL面板标题
        dsl_title = QLabel("<h3>DSL 命令面板</h3>")
        dsl_layout.addWidget(dsl_title)
        
        # DSL命令输入框
        dsl_input_label = QLabel("DSL脚本输入：")
        dsl_layout.addWidget(dsl_input_label)
        
        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText("""指令----------含义
clear;------------------清空链表
mode singly;------------单链表
mode doubly;;-----------双链表
build [1,2,3];----------批量构建
insert head 10;---------头插
insert tail 20;---------尾插
insert index 2 value 99;指定位置插入
delete head;------------头删
delete tail;------------尾删
delete index 3;---------指定位置删除
draw;-------------------强制刷新                        
""")
        self.dsl_input.setMinimumHeight(200)
        dsl_layout.addWidget(self.dsl_input)
        
        # DSL操作按钮
        dsl_btn_layout = QHBoxLayout()
        
        self.btn_dsl_execute = QPushButton("执行DSL")
        self.btn_dsl_execute.clicked.connect(self.execute_dsl)
        dsl_btn_layout.addWidget(self.btn_dsl_execute)
        
        self.btn_dsl_clear = QPushButton("清空脚本")
        self.btn_dsl_clear.clicked.connect(lambda: self.dsl_input.clear())
        dsl_btn_layout.addWidget(self.btn_dsl_clear)
        
        self.btn_dsl_example = QPushButton("加载示例")
        self.btn_dsl_example.clicked.connect(self._load_dsl_example)
        dsl_btn_layout.addWidget(self.btn_dsl_example)
        
        dsl_layout.addLayout(dsl_btn_layout)
        
        # DSL执行日志
        dsl_log_label = QLabel("DSL执行日志：")
        dsl_layout.addWidget(dsl_log_label)
        
        self.dsl_log = QTextEdit()
        self.dsl_log.setReadOnly(True)
        self.dsl_log.setMaximumHeight(150)
        dsl_layout.addWidget(self.dsl_log)
        
        # 把DSL面板添加到分割器
        main_splitter.addWidget(dsl_widget)
        
        # ======================== 右侧原有功能区 ========================
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 1. 可视化画布
        self.fig = Figure(figsize=(10, 3))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.canvas.mpl_connect("pick_event", self._on_node_click)
        right_layout.addWidget(self.canvas, stretch=1)
        
        # 2. 操作控件区
        ctrl_layout = QHBoxLayout()
        right_layout.addLayout(ctrl_layout)
        
        # 模式选择
        ctrl_layout.addWidget(QLabel("链表模式："))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["单链表", "双链表"])
        self.mode_combo.currentTextChanged.connect(self._switch_mode)
        ctrl_layout.addWidget(self.mode_combo)
        
        # 数据输入
        ctrl_layout.addWidget(QLabel("数据："))
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText(
            f"输入{-self.list.MIN_VAL}~{self.list.MAX_VAL}的整数"
        )
        self.data_input.setMaximumWidth(100)
        ctrl_layout.addWidget(self.data_input)
        
        # 索引输入
        ctrl_layout.addWidget(QLabel("位置："))
        self.index_spin = QSpinBox()
        self.index_spin.setRange(0, self.list.MAX_NODES)
        self.index_spin.setMaximumWidth(80)
        ctrl_layout.addWidget(self.index_spin)
        
        # 操作按钮
        self.btn_insert_head = QPushButton("头插入")
        self.btn_insert_head.clicked.connect(self._insert_head)
        ctrl_layout.addWidget(self.btn_insert_head)
        
        self.btn_insert_tail = QPushButton("尾插入")
        self.btn_insert_tail.clicked.connect(self._insert_tail)
        ctrl_layout.addWidget(self.btn_insert_tail)
        
        self.btn_insert_index = QPushButton("指定位置插入")
        self.btn_insert_index.clicked.connect(self._insert_at_index)
        ctrl_layout.addWidget(self.btn_insert_index)
        
        self.btn_delete_head = QPushButton("头删除")
        self.btn_delete_head.clicked.connect(self._delete_head)
        ctrl_layout.addWidget(self.btn_delete_head)
        
        self.btn_delete_tail = QPushButton("尾删除")
        self.btn_delete_tail.clicked.connect(self._delete_tail)
        ctrl_layout.addWidget(self.btn_delete_tail)
        
        self.btn_delete_index = QPushButton("指定位置删除")
        self.btn_delete_index.clicked.connect(self._delete_at_index)
        ctrl_layout.addWidget(self.btn_delete_index)
        
        # 3. 辅助功能区
        aux_layout = QHBoxLayout()
        right_layout.addLayout(aux_layout)
        
        self.btn_clear = QPushButton("清空链表")
        self.btn_clear.clicked.connect(self._clear_list)
        aux_layout.addWidget(self.btn_clear)
        
        self.btn_random = QPushButton("随机生成")
        self.btn_random.clicked.connect(self._random_generate)
        aux_layout.addWidget(self.btn_random)
        
        self.btn_save = QPushButton("保存结构")
        self.btn_save.clicked.connect(self._save_structure)
        aux_layout.addWidget(self.btn_save)
        
        self.btn_load = QPushButton("加载结构")
        self.btn_load.clicked.connect(self._load_structure)
        aux_layout.addWidget(self.btn_load)
        
        # 4. 操作日志区
        log_layout = QHBoxLayout()
        right_layout.addLayout(log_layout)
        
        log_label = QLabel("操作日志：")
        log_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        log_layout.addWidget(self.log_text, stretch=1)
        
        # 把右侧面板添加到分割器
        main_splitter.addWidget(right_widget)
        # 设置分割器初始比例
        main_splitter.setSizes([350, 950])
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 - 点击节点可选中")

    # ------------------------------ DSL相关方法 ------------------------------
    def execute_dsl(self):
        """执行DSL脚本"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法执行DSL脚本")
            return
            
        script = self.dsl_input.toPlainText().strip()
        if not script:
            QMessageBox.warning(self, "警告", "请输入DSL脚本")
            return
            
        try:
            # 清空之前的DSL日志
            self.dsl_log.clear()
            self.status_bar.showMessage("DSL 执行中...")
            
            # 解析并执行DSL脚本
            ast = self.dsl_parser.parse(script)
            self.dsl_executor.execute(ast)
            
            # 记录执行成功日志
            self._log_dsl("✅ DSL脚本执行成功")
            self.status_bar.showMessage("DSL 执行完成", 3000)
            
        except Exception as e:
            # 记录执行错误日志
            error_msg = f"❌ 执行错误: {str(e)}"
            self._log_dsl(error_msg)
            QMessageBox.critical(self, "DSL 错误", str(e))
            self.status_bar.showMessage("DSL 执行失败", 3000)

    def _load_dsl_example(self):
        """DSL示例脚本"""
        example_script = """clear;
mode singly;

build [3, 5, 7];

insert head 1;
insert tail 9;
insert index 2 value 99;

delete index 3;
delete head;

draw;
"""
        self.dsl_input.setText(example_script)
        self._log_dsl("📝 已加载示例DSL脚本")

    def _log_dsl(self, content: str):
        """记录DSL执行日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{time_str}] {content}"
        self.dsl_log.append(log_msg)
        
        # 同时记录到主操作日志
        self._log_operation(f"DSL: {content}")

    # ------------------------------ 原有方法保持不变 ------------------------------
    def _switch_mode(self, text: str):
        """切换单链表/双链表模式"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法切换模式")
            return
        
        mode = "singly" if text == "单链表" else "doubly"
        # 保存当前数据
        current_data = self.list.to_list()
        # 重新初始化链表
        self.list = List(mode=mode)
        # 恢复数据
        for data in current_data:
            self.list.insert_tail(data)
        
        self._log_operation(f"切换为{text}模式")
        self._draw_list()

    def _get_input_data(self) -> int:
        """获取输入数据并验证"""
        try:
            data = int(self.data_input.text().strip())
            if not (self.list.MIN_VAL <= data <= self.list.MAX_VAL):
                raise ValueError
            return data
        except ValueError:
            QMessageBox.warning(
                self, 
                "输入错误", 
                f"请输入{-self.list.MIN_VAL}~{self.list.MAX_VAL}的整数"
            )
            return None

    def _insert_head(self):
        """头插入"""
        data = self._get_input_data()
        if data is None:
            return
        try:
            self._start_animation("insert_head", data)
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _insert_tail(self):
        """尾插入"""
        data = self._get_input_data()
        if data is None:
            return
        try:
            self._start_animation("insert_tail", data)
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _insert_at_index(self):
        """指定位置插入"""
        data = self._get_input_data()
        if data is None:
            return
        index = self.index_spin.value()
        try:
            self._start_animation("insert_index", data, index)
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _delete_head(self):
        """头删除"""
        try:
            self._start_animation("delete_head")
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _delete_tail(self):
        """尾删除"""
        try:
            self._start_animation("delete_tail")
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _delete_at_index(self):
        """指定位置删除"""
        index = self.index_spin.value()
        try:
            self._start_animation("delete_index", index=index)
        except Exception as e:
            QMessageBox.warning(self, "操作失败", str(e))

    def _clear_list(self):
        """清空链表"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法清空")
            return
        self.list.clear()
        self.selected_node_id = None
        self._log_operation("清空链表")
        self._draw_list()

    def _random_generate(self):
        """随机生成链表（3-8个节点）"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法生成")
            return
        
        self.list.clear()
        node_count = random.randint(3, 8)
        for _ in range(node_count):
            data = random.randint(self.list.MIN_VAL, self.list.MAX_VAL)
            self.list.insert_tail(data)
        
        self._log_operation(f"随机生成{node_count}个节点的链表")
        self._draw_list()

    def _save_structure(self):
        """保存链表结构到JSON文件"""
        if self.list.is_empty():
            QMessageBox.warning(self, "警告", "空链表无法保存")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存链表", ".", "JSON文件 (*.json)"
        )
        if not filename:
            return
        
        save_data = {
            "mode": self.list.mode,
            "data": self.list.to_list()
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        self._log_operation(f"保存链表到{os.path.basename(filename)}")
        self.status_bar.showMessage(f"已保存到{os.path.basename(filename)}")

    def _load_structure(self):
        """从JSON文件加载链表结构"""
        if self.anim_timer.isActive():
            QMessageBox.warning(self, "警告", "动画执行中，无法加载")
            return
        
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载链表", ".", "JSON文件 (*.json)"
        )
        if not filename:
            return
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                load_data = json.load(f)
            
            mode = load_data.get("mode", "singly")
            data = load_data.get("data", [])
            
            # 初始化链表
            self.list = List(mode=mode)
            for val in data:
                self.list.insert_tail(val)
            
            # 更新UI
            self.mode_combo.setCurrentText(
                "单链表" if mode == "singly" else "双链表"
            )
            self._log_operation(f"从{os.path.basename(filename)}加载链表")
            self._draw_list()
        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"文件格式错误：{str(e)}")

    def _start_animation(self, op_type: str, data: int = None, index: int = None):
        """开始动画"""
        if self.anim_timer.isActive():
            return
        
        # 生成动画步骤
        self.anim_steps = []
        visual_data = self.list.get_visual_data()
        nodes = visual_data["nodes"]
        
        if op_type.startswith("insert"):
            # 插入动画：高亮插入位置 -> 插入节点 -> 恢复颜色
            if op_type == "insert_head":
                target_idx = 0
                self.anim_steps.append(("highlight", target_idx, 0.3))
                self.anim_steps.append(("insert_head", data))
                self.anim_steps.append(("restore", target_idx))
                self._log_operation(f"头插入数据{data}")
                
            elif op_type == "insert_tail":
                target_idx = len(nodes)
                self.anim_steps.append(("highlight", target_idx, 0.3))
                self.anim_steps.append(("insert_tail", data))
                self.anim_steps.append(("restore", target_idx))
                self._log_operation(f"尾插入数据{data}")
                
            elif op_type == "insert_index":
                target_idx = index
                self.anim_steps.append(("highlight", target_idx, 0.3))
                self.anim_steps.append(("insert_index", data, index))
                self.anim_steps.append(("restore", target_idx))
                self._log_operation(f"在位置{index}插入数据{data}")
                
        elif op_type.startswith("delete"):
            # 删除动画：高亮删除节点 -> 移除节点 -> 重新布局
            if op_type == "delete_head":
                target_idx = 0
                self.anim_steps.append(("highlight", target_idx, 0.8))
                self.anim_steps.append(("delete_head",))
                self._log_operation("头删除")
                
            elif op_type == "delete_tail":
                target_idx = len(nodes) - 1
                self.anim_steps.append(("highlight", target_idx, 0.8))
                self.anim_steps.append(("delete_tail",))
                self._log_operation("尾删除")
                
            elif op_type == "delete_index":
                target_idx = index
                self.anim_steps.append(("highlight", target_idx, 0.8))
                self.anim_steps.append(("delete_index", index))
                self._log_operation(f"删除位置{index}的节点")
        
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
            self._draw_list()
            return
        
        step = self.anim_steps[self.anim_index]
        self.anim_index += 1
        op = step[0]
        
        if op == "highlight":
            # 高亮目标位置
            idx, alpha = step[1], step[2]
            self._draw_list(highlight_idx=idx, highlight_alpha=alpha)
            
        elif op == "restore":
            # 恢复颜色
            self._draw_list()
            
        elif op == "insert_head":
            # 执行头插入
            data = step[1]
            self.list.insert_head(data)
            
        elif op == "insert_tail":
            # 执行尾插入
            data = step[1]
            self.list.insert_tail(data)
            
        elif op == "insert_index":
            # 执行指定位置插入
            data, index = step[1], step[2]
            self.list.insert_at_index(data, index)
            
        elif op == "delete_head":
            # 执行头删除
            self.list.delete_head()
            
        elif op == "delete_tail":
            # 执行尾删除
            self.list.delete_tail()
            
        elif op == "delete_index":
            # 执行指定位置删除
            index = step[1]
            self.list.delete_at_index(index)

    def _disable_buttons(self, disable: bool):
        """禁用/启用操作按钮"""
        buttons = [
            self.btn_insert_head, self.btn_insert_tail, self.btn_insert_index,
            self.btn_delete_head, self.btn_delete_tail, self.btn_delete_index,
            self.btn_clear, self.btn_random, self.btn_save, self.btn_load,
            self.mode_combo, self.btn_dsl_execute
        ]
        for btn in buttons:
            btn.setEnabled(not disable)

    def _draw_list(self, highlight_idx: int = None, highlight_alpha: float = 1.0):
        """绘制链表（修复：固定尺寸节点矩形，解决直线问题）"""
        self.ax.clear()
        # 1. 重新设置坐标系（适配固定尺寸节点）
        node_width = 3.0       # 节点宽度（固定）
        node_height = 1.5      # 节点高度（固定）
        node_spacing = 2.0     # 节点间距（固定）
        canvas_padding = 1.0   # 画布内边距
        
        # 获取链表数据
        visual_data = self.list.get_visual_data()
        nodes = visual_data["nodes"]
        edges = visual_data["edges"]
        node_count = len(nodes)
        
        # 计算画布范围（根据节点数量动态调整，保证所有节点可见）
        total_width = canvas_padding * 2 + node_count * (node_width + node_spacing) - node_spacing
        self.ax.set_xlim(0 - canvas_padding, total_width + canvas_padding)
        self.ax.set_ylim(0 - canvas_padding, node_height + canvas_padding * 2)
        self.ax.axis("off")  # 隐藏坐标轴

        # 2. 绘制边（先绘边，避免遮挡，适配固定尺寸节点）
        for edge in edges:
            # 找到边的起点和终点节点
            source_node = next(n for n in nodes if n["id"] == edge["source_id"])
            target_node = next(n for n in nodes if n["id"] == edge["target_id"])
            
            # 计算节点索引（用于定位固定尺寸节点的坐标）
            source_idx = nodes.index(source_node)
            target_idx = nodes.index(target_node)
            
            # 固定尺寸节点的中心坐标（核心：根据索引计算，而非原始x/y）
            source_x = canvas_padding + source_idx * (node_width + node_spacing) + node_width / 2
            target_x = canvas_padding + target_idx * (node_width + node_spacing) + node_width / 2
            center_y = (node_height + canvas_padding) / 2  # 垂直居中
            
            # 计算箭头起点/终点（节点边缘，避免箭头穿入节点）
            arrow_start_x = source_x + node_width / 2  # 源节点右侧边缘
            arrow_start_y = center_y
            arrow_end_x = target_x - node_width / 2    # 目标节点左侧边缘
            arrow_end_y = center_y
            
            # 绘制箭头（区分next/prev）
            if edge["type"] == "next":
                # 正向指针（next）：绿色实线箭头
                self.ax.annotate(
                    "", xy=(arrow_end_x, arrow_end_y), xytext=(arrow_start_x, arrow_start_y),
                    arrowprops=dict(
                        arrowstyle="->", 
                        color=edge.get("color", "#2E8B57"),  # 绿色
                        lw=2,
                        shrinkA=5,  # 箭头起点缩进（避免贴节点）
                        shrinkB=5   # 箭头终点缩进
                    )
                )
            elif edge["type"] == "prev":
                # 反向指针（prev，双链表）：橙色半透明箭头
                self.ax.annotate(
                    "", xy=(arrow_end_x, arrow_end_y), xytext=(arrow_start_x, arrow_start_y),
                    arrowprops=dict(
                        arrowstyle="->", 
                        color=edge.get("color", "#FF8C00"),  # 橙色
                        lw=2,
                        alpha=0.6,
                        shrinkA=5,
                        shrinkB=5
                    )
                )

        # 3. 绘制固定尺寸的节点矩形（核心修复）
        for i, node in enumerate(nodes):
            # 计算节点左上角坐标（固定尺寸）
            x = canvas_padding + i * (node_width + node_spacing)
            y = canvas_padding  # 垂直居中（可调整y值改变节点垂直位置）
            
            # 节点颜色逻辑（默认/选中/高亮）
            base_color = node.get("color", "#E0E0E0")  # 默认浅灰色
            if self.selected_node_id == node["id"]:
                fill_color = "#FF6347"  # 选中节点：珊瑚红
            elif highlight_idx is not None and i == highlight_idx:
                # 高亮节点：金色（带透明度）
                alpha = highlight_alpha
                fill_color = "#FFD700"
            else:
                fill_color = base_color
                alpha = 0.9
            
            # 绘制固定尺寸的矩形节点（关键：使用固定的width/height）
            rect = patches.Rectangle(
                (x, y),                # 左上角坐标
                node_width,            # 固定宽度
                node_height,           # 固定高度
                linewidth=2,           # 边框宽度
                edgecolor="black",     # 边框颜色
                facecolor=fill_color,  # 填充色
                alpha=alpha,           # 透明度
                picker=True            # 支持点击选择
            )
            # 绑定节点元数据（用于点击事件）
            rect.node_id = node["id"]
            rect.index = i
            self.ax.add_patch(rect)
            
            # 绘制节点文本（数据值，居中显示）
            text_x = x + node_width / 2
            text_y = y + node_height / 2
            self.ax.text(
                text_x, text_y, 
                str(node["label"]),
                ha="center", va="center",  # 水平/垂直居中
                fontsize=12, fontweight="bold",
                color="#000000"  # 文本颜色
            )
            
            # 绘制头/尾节点标记
            if node["is_head"]:
                self.ax.text(
                    text_x, y - 0.2, "HEAD",
                    ha="center", va="top",
                    fontsize=10, color="red", fontweight="bold"
                )
            if node["is_tail"]:
                self.ax.text(
                    text_x, y + node_height + 0.2, "TAIL",
                    ha="center", va="bottom",
                    fontsize=10, color="blue", fontweight="bold"
                )

        # 4. 刷新画布（使绘制生效）
        self.canvas.draw_idle()

    def _on_node_click(self, event):
        """节点点击事件"""
        if self.anim_timer.isActive():
            return
        
        artist = event.artist
        if hasattr(artist, "node_id"):
            # 切换选中状态
            if self.selected_node_id == artist.node_id:
                self.selected_node_id = None
                self.status_bar.showMessage("就绪 - 点击节点可选中")
            else:
                self.selected_node_id = artist.node_id
                # 显示节点信息
                node = next(
                    n for n in self.list.get_visual_data()["nodes"] 
                    if n["id"] == artist.node_id
                )
                self.status_bar.showMessage(
                    f"选中节点：索引{artist.index}，数据{node['data']}"
                )
            
            self._draw_list()

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