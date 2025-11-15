# tree_selector.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton  # 改为PySide6

class TreeSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择树形结构类型")
        self.resize(400, 300)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # 普通二叉树按钮
        btn_binary = QPushButton("普通二叉树可视化")
        btn_binary.clicked.connect(self.open_binary_tree)
        layout.addWidget(btn_binary)
        
        # BST按钮
        btn_bst = QPushButton("二叉搜索树（BST）可视化")
        btn_bst.clicked.connect(self.open_bst)
        layout.addWidget(btn_bst)
        
        # 哈夫曼树按钮
        btn_huffman = QPushButton("哈夫曼树可视化")
        btn_huffman.clicked.connect(self.open_huffman_tree)
        layout.addWidget(btn_huffman)

    def open_binary_tree(self):
        from gui.tree_window import TreeWindow  # 注意：如果tree_window在gui目录下，需要补全路径
        self.binary_window = TreeWindow()
        self.binary_window.show()
        self.close()

    def open_bst(self):
        from gui.bst_window import BSTWindow  # 补全路径（假设在gui目录下）
        self.bst_window = BSTWindow()
        self.bst_window.show()
        self.close()

    def open_huffman_tree(self):
        from gui.huffman_window import HuffmanWindow  # 补全路径（假设在gui目录下）
        self.huffman_window = HuffmanWindow()
        self.huffman_window.show()
        self.close()