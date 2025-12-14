# gui/menu_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QDialog, QVBoxLayout, QDialogButtonBox
from PySide6.QtCore import Qt
from gui.linear_selector import LinearSelector
from gui.tree_window import TreeWindow
from gui.tree_selector import TreeSelector

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("数据结构可视化DSL语言帮助文档")
        self.resize(400, 600)
        
        # 设置为非模态对话框的关键设置
        self.setModal(False)  # 明确设置为非模态[6,7](@ref)
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建文本浏览器控件
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        
        # 设置简洁的帮助文档内容
        help_content = self._get_clean_help_content()
        self.text_browser.setPlainText(help_content)
        
        # 创建按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        
        # 添加到布局
        layout.addWidget(self.text_browser)
        layout.addWidget(self.button_box)
        
        # 设置对话框关闭时自动删除，避免内存泄漏[6](@ref)
        self.setAttribute(Qt.WA_DeleteOnClose)
    
    def _get_clean_help_content(self):
        """提取并清理帮助文档内容，去除多余标点"""
        content = """
概述
本DSL专为数据结构可视化操作设计
支持多种常见数据结构的创建操作和展示
通过简洁指令集实现二叉树栈序列链表BSTAVL树和哈夫曼树的可视化控制
适用于教学演示算法验证和数据结构学习

通用语法规则
注释以//或#开头的行为注释不参与解析
语句结束大部分数据结构的指令需以分号结尾栈和序列除外
空行会被自动忽略可用于分隔指令提高可读性
大小写指令通常不区分大小写具体以各数据结构说明为准

各数据结构DSL指令说明

二叉树 Binary Tree
清空树
clear
随机构建树
build random n=10
build complete n=7
插入节点
insert 5
遍历操作
traverse preorder
traverse inorder
traverse postorder
绘制树
draw

栈 Stack
栈命名
stack MyStack
元素操作
push 3
pop
peek
栈管理
clear
random 5
流程控制
sleep 1000
end

序列 Sequence
构建序列
build [1, 3, 5, 7]
random 5 1 100
元素操作
insert 2 9
delete 3
展示序列
show

链表 List
清空链表
clear
模式切换
mode singly
mode doubly
构建链表
build [2, 4, 6, 8]
插入操作
insert head 1
insert tail 9
insert index 2 5
删除操作
delete head
delete tail
delete index 1
绘制链表
draw

二叉搜索树 BST
清空树
clear
构建BST
build [3, 1, 4, 2]
元素操作
insert 5
search 3
delete 2
特殊查找
find_predecessor 5
find_successor 5
find_lower_bound 5
遍历与绘制
inorder
draw

AVL树
清空树
clear
元素操作
insert 5
delete 3
search 7
随机生成
random 10
特殊查找
predecessor 5
successor 5
lower_bound 5
遍历与控制
inorder
delay 2000

哈夫曼树 Huffman Tree
清空树
clear
构建哈夫曼树
build text="hello world"
编码与展示
draw
show_codes
文件操作
save to "huffman_codes.json"
load from "huffman_codes.json"

执行流程
编写符合上述语法的DSL脚本
系统会按顺序解析并执行指令
大部分操作会自动触发可视化更新
耗时操作会有动画展示过程
执行完成后会显示DSL执行完成状态

错误处理
缺少分号会提示第X行缺少分号
语法错误会提示第X行无法识别指令
参数错误会提示具体错误原因如随机生成节点数必须大于0
指令格式错误会提示正确格式如insert语法错误正确格式 insert 5

如有其他问题请参考具体数据结构的示例脚本或联系技术支持
"""
        return content.strip()

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据结构可视化系统")
        self.resize(600, 400)
        
        # 存储帮助对话框引用，避免重复创建[1](@ref)
        self.help_dialog = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        btnLinear = QPushButton("线性结构可视化")
        btnLinear.clicked.connect(self.open_linear_selector)
        layout.addWidget(btnLinear)

        btnTree = QPushButton("树形结构可视化")
        btnTree.clicked.connect(self.open_tree_selector)
        layout.addWidget(btnTree)
        
        # 新增帮助文档按钮
        btnHelp = QPushButton("帮助文档")
        btnHelp.clicked.connect(self.open_help_dialog)
        layout.addWidget(btnHelp)

    def open_linear_selector(self):
        self.linear_selector = LinearSelector()
        self.linear_selector.show()  # 使用show()方法显示非模态窗口[3](@ref)

    def open_tree_selector(self):
        self.tree_selector = TreeSelector()
        self.tree_selector.show()  # 使用show()方法显示非模态窗口[3](@ref)
    
    def open_help_dialog(self):
        """打开非模态帮助文档对话框"""
        if self.help_dialog is None or not self.help_dialog.isVisible():
            # 创建新的帮助对话框实例
            self.help_dialog = HelpDialog(self)
            
            # 连接对话框的关闭信号，清理引用[1](@ref)
            self.help_dialog.finished.connect(self.on_help_dialog_closed)
            
            # 使用show()而不是exec()来显示非模态对话框[6,8](@ref)
            self.help_dialog.show()
        else:
            # 如果对话框已经存在，将其置于最前[1](@ref)
            self.help_dialog.raise_()
            self.help_dialog.activateWindow()
    
    def on_help_dialog_closed(self, result):
        """当帮助对话框关闭时清理引用"""
        self.help_dialog = None