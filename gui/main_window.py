# gui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSpinBox, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    """
    简单的 UI（View+Controller），通过 model.add_listener 注册更新回调。
    所有与业务逻辑相关的调用都通过 model 进行（保持分离）。
    """
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.add_listener(self.on_model_update)

        self.setWindowTitle("大作业：数组可视化（PySide6）")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        vlayout = QVBoxLayout(central)

        # matplotlib canvas
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        vlayout.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)

        # control bar
        ctrl = QHBoxLayout()
        vlayout.addLayout(ctrl)

        ctrl.addWidget(QLabel("M:"))
        self.spinM = QSpinBox(); self.spinM.setRange(1, 500); self.spinM.setValue(20)
        ctrl.addWidget(self.spinM)
        ctrl.addWidget(QLabel("N:"))
        self.spinN = QSpinBox(); self.spinN.setRange(0, 500); self.spinN.setValue(10)
        ctrl.addWidget(self.spinN)
        self.btnCreate = QPushButton("随机创建")
        self.btnCreate.clicked.connect(self.create_random)
        ctrl.addWidget(self.btnCreate)

        ctrl.addWidget(QLabel("Value:"))
        self.inputValue = QLineEdit("7"); self.inputValue.setFixedWidth(80)
        ctrl.addWidget(self.inputValue)
        self.btnAppend = QPushButton("Append")
        self.btnAppend.clicked.connect(self.append_value)
        ctrl.addWidget(self.btnAppend)

        self.btnRemove = QPushButton("Remove idx")
        self.removeIdx = QSpinBox(); self.removeIdx.setRange(0, 499); self.removeIdx.setValue(0)
        self.btnRemove.clicked.connect(self.remove_idx)
        ctrl.addWidget(self.btnRemove)
        ctrl.addWidget(self.removeIdx)

        # status
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignLeft)
        vlayout.addWidget(self.status)

        # initial draw
        self.draw_array([])

    def draw_array(self, arr, highlight=None):
        self.ax.clear()
        if arr:
            idx = list(range(len(arr)))
            bars = self.ax.bar(idx, arr)
            if highlight and 'index' in highlight:
                i = highlight['index']
                if 0 <= i < len(bars):
                    bars[i].set_edgecolor('red')
                    bars[i].set_linewidth(2.5)
            self.ax.set_xlim(-0.5, max(10, len(arr)-0.5))
            self.ax.set_ylim(0, max(10, max(arr)))
        else:
            self.ax.set_xlim(-0.5, 9.5)
            self.ax.set_ylim(0, 10)
        self.ax.set_xlabel("index")
        self.ax.set_ylabel("value")
        self.canvas.draw_idle()

    # UI event handlers (调用 model)
    def create_random(self):
        m = self.spinM.value(); n = self.spinN.value()
        try:
            self.model.create_random(m=m, n=n)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def append_value(self):
        try:
            v = int(self.inputValue.text())
            self.model.append(v)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def remove_idx(self):
        i = self.removeIdx.value()
        try:
            self.model.remove(i)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    # model -> view 回调
    def on_model_update(self, state):
        arr = state.get('array', [])
        action = state.get('action')
        txt = f"动作: {action}" if action else "就绪"
        self.status.setText(txt)
        highlight = None
        if action and action.get('type') in ('insert','remove','update','append'):
            # highlight index if provided, or last element for append
            highlight_index = action.get('index')
            if highlight_index is None and action.get('type') == 'append':
                highlight_index = len(arr) - 1
            highlight = {'index': highlight_index} if highlight_index is not None else None
        self.draw_array(arr, highlight)
