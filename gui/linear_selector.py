# tree_selector.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton  # 改为PySide6

class LinearSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择线形结构类型")
        self.resize(400, 300)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        btn_list = QPushButton("顺序表可视化")
        btn_list.clicked.connect(self.open_array)
        layout.addWidget(btn_list)
        
        # 顺序表和链表按钮
        btn_list = QPushButton("链表可视化")
        btn_list.clicked.connect(self.open_list)
        layout.addWidget(btn_list)
        
        # 顺序栈按钮
        btn_stack = QPushButton("顺序栈可视化")
        btn_stack.clicked.connect(self.open_stack)
        layout.addWidget(btn_stack)
        
        
    def open_array(self):
        from gui.linear_window import LinearWindow  
        self.array_window = LinearWindow()
        self.array_window.show()
        self.close()

    def open_list(self):
        from gui.ListWindow import ListWindow  
        self.list_window = ListWindow()
        self.list_window.show()
        self.close()

    def open_stack(self):
        from gui.StackWindow import StackWindow  
        self.stack_window = StackWindow()
        self.stack_window.show()
        self.close()

   