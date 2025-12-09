# gui/components/dsl_panel.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QSplitter)
from PySide6.QtCore import Signal,  Qt

class DSLPanel(QWidget):
    """DSL执行面板组件"""
    execute_request = Signal(str)  # 发送DSL文本执行请求
    clear_request = Signal()       # 发送清空请求

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        layout.addWidget(QLabel("DSL执行面板"))
        
        # 分割器
        splitter = QSplitter(Qt.Vertical)
        
        # DSL输入区
        self.dsl_input = QTextEdit()
        self.dsl_input.setPlaceholderText("输入DSL语句（支持声明式和命令式）...")
        self.dsl_input.setMinimumHeight(200)
        splitter.addWidget(self.dsl_input)
        
        # 输出日志区
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setPlaceholderText("执行日志将显示在这里...")
        self.output_log.setMinimumHeight(150)
        splitter.addWidget(self.output_log)
        
        layout.addWidget(splitter)
        
        # 按钮区
        btn_layout = QHBoxLayout()
        self.btn_execute = QPushButton("执行")
        self.btn_execute.clicked.connect(self._on_execute)
        
        self.btn_clear = QPushButton("清空输入")
        self.btn_clear.clicked.connect(self._on_clear)
        
        self.btn_demo = QPushButton("示例DSL")
        self.btn_demo.clicked.connect(self._load_demo)
        
        btn_layout.addWidget(self.btn_execute)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_demo)
        layout.addLayout(btn_layout)

    def _on_execute(self):
        dsl_text = self.dsl_input.toPlainText().strip()
        if dsl_text:
            self.execute_request.emit(dsl_text)
    
    def _on_clear(self):
        self.dsl_input.clear()
        self.clear_request.emit()
    
    def _load_demo(self):
        """加载示例DSL代码"""
        demo = """// 示例：链表操作
singly list demoList {
    node n0 { int val = 10; link to n1; }
    node n1 { int val = 20; link to null; }
}

// 执行操作
demoList.insert(value = 15, index = 1);
demoList.delete(index = 0);
"""
        self.dsl_input.setPlainText(demo)
    
    def log(self, message: str):
        """添加日志信息"""
        self.output_log.append(message)