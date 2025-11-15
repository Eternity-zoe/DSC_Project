# gui/main_window.py
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
from core.linked_list import LinkedList
from core.stack import Stack


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("线性结构可视化系统（平滑动画 + 节点选中）")
        self.resize(950, 600)

        # 当前模式与选中状态
        self.mode = "Sequence"
        self.selected_index = None  # 当前选中的节点

        # 三种结构
        self.seq = SequenceList()
        self.linked = LinkedList()
        self.stack = Stack()
        self.seq.add_listener(self.on_update)
        self.linked.add_listener(self.on_update)
        self.stack.add_listener(self.on_update)

        # 动画状态
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._anim_step)
        self.anim_steps = []
        self.anim_index = 0

        # UI 布局
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # matplotlib 画布
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.canvas.mpl_connect("pick_event", self.on_pick)
        layout.addWidget(self.canvas)

        # 控件区
        ctrl = QHBoxLayout()
        layout.addLayout(ctrl)

        ctrl.addWidget(QLabel("结构类型:"))
        self.comboType = QComboBox()
        self.comboType.addItems(["SequenceList", "LinkedList", "Stack"])
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

        self.btnInsert = QPushButton("插入/入栈")
        self.btnInsert.clicked.connect(self.insert)
        ctrl.addWidget(self.btnInsert)

        self.btnDelete = QPushButton("删除/出栈")
        self.btnDelete.clicked.connect(self.delete)
        ctrl.addWidget(self.btnDelete)

        # 文件操作区
        file_ctrl = QHBoxLayout()
        layout.addLayout(file_ctrl)
        self.btnSave = QPushButton("保存结构")
        self.btnSave.clicked.connect(self.save_structure)
        self.btnOpen = QPushButton("打开结构")
        self.btnOpen.clicked.connect(self.load_structure)
        file_ctrl.addWidget(self.btnSave)
        file_ctrl.addWidget(self.btnOpen)

        # 状态栏
        self.status = QLabel("就绪")
        layout.addWidget(self.status)

        self.draw([])

    # ========== 模式切换 ==========
    def switch_mode(self, text):
        self.selected_index = None
        if "Seq" in text:
            self.mode = "Sequence"
        elif "Linked" in text:
            self.mode = "Linked"
        else:
            self.mode = "Stack"
        self.status.setText(f"切换为 {self.mode} 模式")
        self.draw([])

    # ========== 构建 ==========
    def build_structure(self):
        data = [random.randint(0, 100) for _ in range(6)]
        if self.mode == "Sequence":
            self.seq.build(data)
        elif self.mode == "Linked":
            self.linked.build(data)
        else:
            self.stack.data.clear()
            for v in data:
                self.stack.push(v)
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
        if self.mode == "Sequence":
            arr = self.seq.data
        elif self.mode == "Linked":
            arr = []
            cur = self.linked.head
            while cur:
                arr.append(cur.val)
                cur = cur.next
        else:
            arr = self.stack.data
        return {"type": self.mode, "data": arr}

    def restore_data(self, info):
        dtype = info.get("type")
        data = info.get("data", [])
        if dtype == "Sequence":
            self.comboType.setCurrentText("SequenceList")
            self.seq.build(data)
        elif dtype == "Linked":
            self.comboType.setCurrentText("LinkedList")
            self.linked.build(data)
        elif dtype == "Stack":
            self.comboType.setCurrentText("Stack")
            self.stack.data.clear()
            for v in data:
                self.stack.push(v)

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
        if index < 0 or index > len(arr):
            QMessageBox.warning(self, "错误", "索引越界")
            return

        # 生成动画帧：颜色渐变、插入/删除形变
        steps = []
        if op == "insert":
            steps += [("fade_color", index, 0.2*i) for i in range(6)]
            steps.append(("commit_insert", index, value))
            steps += [("fade_color", index, 1 - 0.15*i) for i in range(6)]
        elif op == "delete":
            steps += [("fade_color", index, 1 - 0.15*i) for i in range(6)]
            steps.append(("commit_delete", index))
        else:
            return
        self.anim_steps = steps
        self.anim_index = 0
        self.disable_buttons(True)
        self.anim_timer.start(350)  # 慢一点（350ms/frame）

    def _anim_step(self):
        if self.anim_index >= len(self.anim_steps):
            self.anim_timer.stop()
            self.disable_buttons(False)
            return
        step = self.anim_steps[self.anim_index]
        self.anim_index += 1
        arr = self.get_current_data()["data"]

        t = step[0]
        if t == "fade_color":
            idx, alpha = step[1], step[2]
            self.draw(arr, {"type": "highlight", "index": idx, "alpha": alpha})
        elif t == "commit_insert":
            idx, val = step[1], step[2]
            if self.mode == "Sequence":
                self.seq.insert(idx, val)
            elif self.mode == "Linked":
                self.linked.insert(idx, val)
            else:
                self.stack.push(val)
        elif t == "commit_delete":
            idx = step[1]
            if self.mode == "Sequence":
                self.seq.delete(idx)
            elif self.mode == "Linked":
                self.linked.delete(idx)
            else:
                self.stack.pop()
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
            highlight_color = "#FF6347"
            normal_color = "#87CEFA"
            alpha = 1.0
            if action and action.get("type") == "highlight":
                alpha = action.get("alpha", 1)
            if self.mode in ("Sequence", "Stack"):
                bars = self.ax.bar(range(len(arr)), arr, color=normal_color, picker=True)
                for i, bar in enumerate(bars):
                    bar.index = i
                    self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                                 str(int(arr[i])), ha='center', va='center', fontsize=12)
                    if (action and action.get("index") == i and action.get("type") in ("highlight","selected")) or i == self.selected_index:
                        bar.set_facecolor(highlight_color)
                        bar.set_alpha(alpha)
                self.ax.set_xlim(-1, len(arr))
                self.ax.set_ylim(0, max(arr) + 10)
                self.ax.set_title("顺序栈" if self.mode=="Stack" else "顺序表")
            else:
                # 链表绘制
                for i, v in enumerate(arr):
                    x = i * 1.5
                    color = normal_color
                    a = 1.0
                    if (action and action.get("index") == i and action.get("type") in ("highlight","selected")) or i == self.selected_index:
                        color = highlight_color
                        a = alpha
                    self.ax.add_patch(patches.Rectangle((x, 0), 1.0, 0.6, facecolor=color, edgecolor='black', alpha=a, picker=True))
                    self.ax.text(x + 0.5, 0.3, str(int(v)), ha='center', va='center', fontsize=12)
                    if i < len(arr) - 1:
                        self.ax.arrow(x + 1.0, 0.3, 0.3, 0, head_width=0.1, color='k')
                self.ax.set_xlim(-0.5, len(arr) * 1.7)
                self.ax.set_ylim(-0.2, 1)
                self.ax.axis('off')
                self.ax.set_title("单链表")
        self.canvas.draw_idle()
