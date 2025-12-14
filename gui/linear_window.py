# gui\linear_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QSpinBox, QMessageBox, QComboBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import json, os, random
# 配置中文字体
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
from core.sequence_list import SequenceList 
from dsl.sequence.sequence_dsl import SequenceDSLParser

DSL_EXAMPLES = {
    "示例 1：基础操作": """sequence Demo {
    build [10, 20, 30]
    insert 1 99
    delete 2
}""",

    "示例 2：随机构建": """sequence Demo {
    random 6 0 100
    insert 0 5
    insert 3 88
}""",

    "示例 3：连续删除": """sequence Demo {
    build [1,2,3,4,5]
    delete 0
    delete 2
    delete 1
}"""
}



class LinearWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("顺序表可视化系统（平滑动画 + 节点选中）")
        self.resize(950, 600)

        # 当前模式与选中状态
        self.mode = "Sequence"
        self.selected_index = None  # 当前选中的节点

        # 顺序表结构
        self.seq = SequenceList()
        self.seq.add_listener(self.on_update)

        # 动画状态
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._anim_step)
        self.anim_steps = []
        self.anim_index = 0
        self.dsl_cmds = []
        self.dsl_ptr = 0

        # UI 布局
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout(central)

        # 左：DSL 区
        dsl_panel = QVBoxLayout()
        layout.addLayout(dsl_panel, 1)

        # 右：可视化 + 控件
        right_panel = QVBoxLayout()
        layout.addLayout(right_panel, 3)

        # matplotlib 画布
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.canvas.mpl_connect("pick_event", self.on_pick)
        right_panel.addWidget(self.canvas)

        # 控件区
        ctrl = QHBoxLayout()
        right_panel.addLayout(ctrl)

        ctrl.addWidget(QLabel("结构类型:"))
        self.comboType = QComboBox()
        self.comboType.addItem("SequenceList")
        self.comboType.currentTextChanged.connect(self.switch_mode)
        ctrl.addWidget(self.comboType)

        self.inputValue = QLineEdit(); self.inputValue.setPlaceholderText("元素值")
        ctrl.addWidget(self.inputValue)

        self.inputIndex = QSpinBox(); self.inputIndex.setRange(0, 999)
        ctrl.addWidget(QLabel("位置:"))
        ctrl.addWidget(self.inputIndex)

        self.btnBuild = QPushButton("构建(随机)")
        self.btnBuild.clicked.connect(self.build_structure)
        ctrl.addWidget(self.btnBuild)

        self.btnInsert = QPushButton("插入")
        self.btnInsert.clicked.connect(self.insert)
        ctrl.addWidget(self.btnInsert)

        self.btnDelete = QPushButton("删除")
        self.btnDelete.clicked.connect(self.delete)
        ctrl.addWidget(self.btnDelete)

        # 文件操作区
        file_ctrl = QHBoxLayout()
        right_panel.addLayout(file_ctrl)
        self.btnSave = QPushButton("保存结构")
        self.btnSave.clicked.connect(self.save_structure)
        self.btnOpen = QPushButton("打开结构")
        self.btnOpen.clicked.connect(self.load_structure)
        file_ctrl.addWidget(self.btnSave)
        file_ctrl.addWidget(self.btnOpen)

        # 状态栏
        self.status = QLabel("就绪")
        right_panel.addWidget(self.status)

        # ===== 左侧 DSL 面板 =====
        dsl_panel.addWidget(QLabel("DSL 脚本"))

        # 示例选择
        self.comboDSL = QComboBox()
        self.comboDSL.addItem("选择示例...")
        self.comboDSL.addItems(DSL_EXAMPLES.keys())
        self.comboDSL.currentTextChanged.connect(self.load_dsl_example)
        dsl_panel.addWidget(self.comboDSL)

        # DSL 编辑区（用多行，更合理）
        from PySide6.QtWidgets import QTextEdit
        self.dslEdit = QTextEdit()
        self.dslEdit.setPlaceholderText(
            "sequence Demo {\n    build [1,2,3]\n    insert 1 9\n}"
        )
        dsl_panel.addWidget(self.dslEdit,stretch=1)

        # DSL 按钮
        dsl_btns = QHBoxLayout()
        dsl_panel.addLayout(dsl_btns)

        self.btnRunDSL = QPushButton("▶ 执行")
        self.btnRunDSL.clicked.connect(self.run_dsl)
        dsl_btns.addWidget(self.btnRunDSL)

        self.btnStepDSL = QPushButton("⏭ 单步")
        self.btnStepDSL.clicked.connect(self.step_dsl)
        dsl_btns.addWidget(self.btnStepDSL)

        # 拉伸占位（让 DSL 区靠上）
        dsl_panel.addStretch()

        



        self.draw([])

    # ========== 模式切换 ==========
    def switch_mode(self, text):
        self.selected_index = None
        if "Seq" in text:
            self.mode = "Sequence"
        self.status.setText(f"当前为 {self.mode} 模式")
        self.draw([])

    # ========== 构建 ==========
    def build_structure(self):
        data = [random.randint(0, 100) for _ in range(6)]
        self.seq.build(data)
        self.status.setText(f"构建 {self.mode} 成功")
        self.selected_index = None

    # ========== 插入与删除 ==========
    def insert(self):
        try:
            val = int(self.inputValue.text())
        except:
            QMessageBox.warning(self, "输入错误", "请输入数字")
            return
        idx = self.inputIndex.value()
        self.start_animation("insert", idx, val)

    def delete(self):
        """删除当前选中节点或输入索引"""
        idx = self.selected_index if self.selected_index is not None else self.inputIndex.value()
        self.start_animation("delete", idx)

    # ========== 保存与打开 ==========
    def save_structure(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存结构", ".", "JSON 文件 (*.json)"
        )
        if not filename:
            return
        data = self.get_current_data()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.status.setText(f"已保存到 {os.path.basename(filename)}")

    def load_structure(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开结构", ".", "JSON 文件 (*.json)"
        )
        if not filename:
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.restore_data(data)
        self.status.setText(f"已打开 {os.path.basename(filename)}")
        self.selected_index = None

    def get_current_data(self):
        return {"type": self.mode, "data": self.seq.data}

    def restore_data(self, info):
        dtype = info.get("type")
        data = info.get("data", [])
        if dtype == "Sequence":
            self.comboType.setCurrentText("SequenceList")
            self.seq.build(data)

    # ========== 点击事件 ==========
    def on_pick(self, event):
        """点击节点 = 选中（高亮，不删除）"""
        if self.anim_timer.isActive():
            return
        bar = getattr(event, "artist", None)
        if bar is None:
            return
        idx = getattr(bar, "index", None)
        if idx is None:
            return
        self.selected_index = idx
        arr = self.get_current_data()["data"]
        val = arr[idx] if 0 <= idx < len(arr) else "?"
        self.status.setText(f"选中节点 -> 索引 {idx} ，值 {val}")
        self.draw(arr, {"type": "selected", "index": idx})

    # ========== 动画 ==========
    def start_animation(self, op, index=0, value=None):
        if self.anim_timer.isActive():
            return
        arr = self.get_current_data()["data"]
        if not arr and op == "delete":
            QMessageBox.warning(self, "错误", "结构为空")
            return
        # 修正边界检查：插入允许 index = len(arr) (尾部插入)
        if index < 0 or index > len(arr): 
            QMessageBox.warning(self, "错误", "索引越界")
            return

        # 生成动画帧：颜色渐变、插入/删除形变
        steps = []
        if op == "insert":
            # 修正插入动画：高亮待插入位置及其后所有元素
            # 1. 高亮待插入位置及后方元素，模拟后移
            for i in range(6):
                 # index: 待插入位置
                 steps.append(("fade_color", index, 0.2 * i)) 
            # 2. 执行核心操作 (数据结构变化)
            steps.append(("commit_insert", index, value))
            # 3. 强调新插入的元素 (只有 index 变色)
            steps += [("fade_new", index, 1.0 - 0.15 * i) for i in range(7)]
            
        elif op == "delete":
            # 修正删除动画：高亮待删除元素
            # 1. 强调待删除元素，模拟后移
            for i in range(6):
                 steps.append(("fade_color", index, 1 - 0.15 * i)) 
            # 2. 执行核心操作 (数据结构变化)
            steps.append(("commit_delete", index))
            # 3. 强调删除后的元素前移
            # (如果不需要强调前移，直接结束即可)
        else:
            return
            
        self.anim_steps = steps
        self.anim_index = 0
        self.disable_buttons(True)
        self.anim_timer.start(3)  # 慢一点（350ms/frame）

    def _anim_step(self):
        if self.anim_index >= len(self.anim_steps):
            self.anim_timer.stop()
            self.disable_buttons(False)
            self.draw(self.seq.data) # 确保最终状态是正常颜色
            return
        
        step = self.anim_steps[self.anim_index]
        self.anim_index += 1
        arr = self.get_current_data()["data"]

        t = step[0]
        if t == "fade_color":
            # 强调 index 及其右侧所有元素
            idx, alpha = step[1], step[2]
            self.draw(arr, {"type": "highlight_group", "index": idx, "alpha": alpha})
        elif t == "fade_new":
            # 强调新插入的元素 (只强调一个元素)
            idx, alpha = step[1], step[2]
            self.draw(arr, {"type": "selected", "index": idx, "alpha": alpha})
        elif t == "commit_insert":
            idx, val = step[1], step[2]
            self.seq.insert(idx, val)
        elif t == "commit_delete":
            idx = step[1]
            self.seq.delete(idx)
            self.selected_index = None

    def disable_buttons(self, disable=True):
        for b in [self.btnInsert, self.btnDelete, self.btnBuild, self.btnSave, self.btnOpen]:
            b.setEnabled(not disable)

    # ========== 可视化 ==========
    def on_update(self, state):
        arr = state.get("array", [])
        self.draw(arr)

    def draw(self, arr, action=None):
        self.ax.clear()
        if not arr:
            self.ax.text(0.4, 0.5, "(空)", fontsize=16, color="gray")
        else:
            highlight_color = "#FF6347" # 选中/高亮颜色 (珊瑚红)
            move_color = "#FFA07A"      # 移动/后移高亮颜色 (浅鲑鱼红)
            normal_color = "#87CEFA"    # 正常颜色 (浅蓝色)
            alpha = 1.0
            
            # 1. 绘制柱状图
            bars = self.ax.bar(range(len(arr)), arr, color=normal_color, picker=True)
            for i, bar in enumerate(bars):
                bar.index = i
                
                # 2. 应用动画状态
                current_color = normal_color
                
                # A. 选中状态 (永久高亮)
                if i == self.selected_index:
                    current_color = highlight_color
                    alpha = 1.0 # 选中状态不透明
                
                # B. 动画高亮：Highlight Group (删除/插入后移)
                if action and action.get("type") == "highlight_group":
                    idx = action.get("index")
                    # 高亮从 index 开始到末尾的所有元素
                    if i >= idx:
                        current_color = move_color
                        alpha = action.get("alpha", 1)
                        
                # C. 动画高亮：Selected (新插入/待删除元素)
                if action and action.get("type") == "selected" and action.get("index") == i:
                    current_color = highlight_color
                    alpha = action.get("alpha", 1)
                    
                bar.set_facecolor(current_color)
                bar.set_alpha(alpha)
                
                # 3. 绘制元素值和索引
                self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                             str(int(arr[i])), ha='center', va='center', fontsize=12, color='black')
                self.ax.text(bar.get_x() + bar.get_width()/2, -max(arr)*0.05, # 绘制索引
                             f'[{i}]', ha='center', va='top', fontsize=10, color='gray')
            
            # 设置坐标轴范围和标题
            self.ax.set_xlim(-0.5, len(arr) - 0.5)
            self.ax.set_ylim(0, max(arr) + 10 if arr else 10)
            self.ax.set_title("顺序表")
            
        self.canvas.draw_idle()

    def run_dsl(self):
        text = self.dslEdit.toPlainText()
        try:
            self.dsl_cmds = SequenceDSLParser.parse(text)
            self.dsl_ptr = 0
            self.step_dsl()
        except Exception as e:
            QMessageBox.warning(self, "DSL 错误", str(e))
    def step_dsl(self):
        if self.anim_timer.isActive():
            return
        if self.dsl_ptr >= len(self.dsl_cmds):
            self.status.setText("DSL 执行完成")
            return

        cmd = self.dsl_cmds[self.dsl_ptr]
        self.dsl_ptr += 1
        self.execute_dsl_cmd(cmd)
    def execute_dsl_cmd(self, cmd):
        op = cmd[0]

        if op == "build":
            arr = cmd[1]
            self.seq.build(arr)
            self.selected_index = None
            self.status.setText(f"DSL: build {arr}")

        elif op == "random":
            _, n, lo, hi = cmd
            data = [random.randint(lo, hi) for _ in range(n)]
            self.seq.build(data)
            self.status.setText(f"DSL: random {n}")

        elif op == "insert":
            _, idx, val = cmd
            self.start_animation("insert", idx, val)
            self.status.setText(f"DSL: insert {idx} {val}")

        elif op == "delete":
            _, idx = cmd
            self.start_animation("delete", idx)
            self.status.setText(f"DSL: delete {idx}")

        elif op == "show":
            self.draw(self.seq.data)

        # 动画结束后自动走下一条
        if op in ("insert", "delete"):
            self.anim_timer.timeout.connect(self._dsl_auto_continue)
        else:
            QTimer.singleShot(200, self.step_dsl)

    def _dsl_auto_continue(self):
        if not self.anim_timer.isActive():
            self.anim_timer.timeout.disconnect(self._dsl_auto_continue)
            self.step_dsl()

    def load_dsl_example(self, name):
        if name in DSL_EXAMPLES:
            self.dslEdit.setPlainText(DSL_EXAMPLES[name])
            self.status.setText(f"已加载示例：{name}")
