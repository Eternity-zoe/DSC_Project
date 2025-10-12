# gui/menu_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from gui.main_window import MainWindow
from gui.tree_window import TreeWindow

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据结构可视化系统")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        btnLinear = QPushButton("线性结构可视化")
        btnLinear.clicked.connect(self.open_linear)
        layout.addWidget(btnLinear)

        btnTree = QPushButton("树形结构可视化")
        btnTree.clicked.connect(self.open_tree)
        layout.addWidget(btnTree)

    def open_linear(self):
        self.linear = MainWindow()
        self.linear.show()

    def open_tree(self):
        self.tree = TreeWindow()
        self.tree.show()
