import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QSpinBox, QMessageBox,
    QSplitter, QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QFont, QColor

# 导入DSL相关组件
from core.dsl_parser import (
    DSLParser, DSLParseError, StructureDeclaration, Command,
    StructureType, CommandType, DSLNode
)
from gui.components.dsl_panel import DSLPanel  # 复用之前定义的DSL面板

# 链表节点类（原有逻辑保留）
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None
        self.prev = None

# 链表核心逻辑类（原有逻辑保留）
class LinkedList:
    def __init__(self, is_doubly=False):
        self.head = None
        self.tail = None
        self.size = 0
        self.is_doubly = is_doubly  # 是否为双向链表

    def get_node(self, index):
        if index < 0 or index >= self.size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def insert(self, index, val):
        if index < 0 or index > self.size:
            return False
        new_node = ListNode(val)
        
        if index == 0:
            new_node.next = self.head
            if self.is_doubly and self.head:
                self.head.prev = new_node
            self.head = new_node
            if self.size == 0:
                self.tail = new_node
        elif index == self.size:
            new_node.prev = self.tail
            if self.is_doubly and self.tail:
                self.tail.next = new_node
            self.tail = new_node
            if self.size == 0:
                self.head = new_node
        else:
            prev_node = self.get_node(index - 1)
            new_node.next = prev_node.next
            if self.is_doubly:
                new_node.prev = prev_node
                prev_node.next.prev = new_node
            prev_node.next = new_node
        
        self.size += 1
        return True

    def delete(self, index):
        if index < 0 or index >= self.size:
            return False
        
        if self.size == 1:
            self.head = None
            self.tail = None
        elif index == 0:
            self.head = self.head.next
            if self.is_doubly:
                self.head.prev = None
        elif index == self.size - 1:
            self.tail = self.tail.prev
            if self.is_doubly:
                self.tail.next = None
        else:
            prev_node = self.get_node(index - 1)
            prev_node.next = prev_node.next.next
            if self.is_doubly:
                prev_node.next.prev = prev_node
        
        self.size -= 1
        return True

    def update(self, index, val):
        node = self.get_node(index)
        if not node:
            return False
        node.val = val
        return True

    def search(self, val):
        current = self.head
        index = 0
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        return -1

    def traverse(self):
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

# 可视化画布类（原有逻辑保留）
class ListCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.linked_list = LinkedList()
        self.setMinimumSize(800, 400)

    def set_linked_list(self, linked_list):
        self.linked_list = linked_list
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor("#333333"), 2, Qt.SolidLine)
        painter.setPen(pen)
        font = QFont("Arial", 12)
        painter.setFont(font)

        current = self.linked_list.head
        x, y = 50, self.height() // 2
        node_width = 80
        node_height = 40
        spacing = 40

        while current:
            # 绘制节点矩形
            painter.drawRoundedRect(x, y - node_height//2, node_width, node_height, 10, 10)
            # 绘制节点值
            painter.drawText(x + node_width//2, y + 4, Qt.AlignCenter, str(current.val))
            
            # 绘制双向链表的prev指针
            if self.linked_list.is_doubly and current.prev:
                painter.drawLine(x, y, x - spacing//2, y)
                painter.drawLine(x - spacing//2, y, x - spacing//2, y - 10)
                painter.drawLine(x - spacing//2, y - 10, x - 5, y - 10)
            
            # 绘制next指针
            if current.next:
                painter.drawLine(x + node_width, y, x + node_width + spacing, y)
                painter.drawLine(x + node_width + spacing, y, x + node_width + spacing, y + 10)
                painter.drawLine(x + node_width + spacing, y + 10, x + node_width + 5, y + 10)

            x += node_width + spacing
            current = current.next

# 主窗口类（核心改造：集成DSL面板+命令处理器）
class ListWindow(QMainWindow):
    def __init__(self, is_doubly=False):
        super().__init__()
        self.is_doubly = is_doubly  # 是否为双向链表
        self.linked_list = LinkedList(is_doubly)
        
        # 初始化DSL解析器
        self.dsl_parser = DSLParser()
        
        # 初始化UI
        self._init_ui()
        
        # 注册命令处理器
        self._register_command_handlers()

    def _init_ui(self):
        self.setWindowTitle("双向链表操作" if self.is_doubly else "单链表操作")
        self.setGeometry(100, 100, 1200, 600)

        # 中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局：左侧DSL面板，右侧原有功能区
        main_layout = QHBoxLayout(central_widget)

        # ========== 左侧：DSL执行面板 ==========
        self.dsl_panel = DSLPanel()
        self.dsl_panel.execute_request.connect(self._execute_dsl)
        self.dsl_panel.clear_request.connect(self._handle_clear_command)
        main_layout.addWidget(self.dsl_panel, 3)  # 30%宽度

        # ========== 右侧：原有功能区 ==========
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        main_layout.addWidget(right_panel, 7)  # 70%宽度

        # 可视化画布
        self.canvas = ListCanvas()
        self.canvas.set_linked_list(self.linked_list)
        right_layout.addWidget(self.canvas, stretch=1)

        # 操作控件区
        control_layout = QVBoxLayout()

        # 插入操作
        insert_layout = QHBoxLayout()
        insert_layout.addWidget(QLabel("插入值:"))
        self.insert_val = QLineEdit()
        insert_layout.addWidget(self.insert_val)
        insert_layout.addWidget(QLabel("位置:"))
        self.insert_idx = QSpinBox()
        self.insert_idx.setMinimum(0)
        insert_layout.addWidget(self.insert_idx)
        self.insert_btn = QPushButton("插入")
        self.insert_btn.clicked.connect(self._on_insert_click)
        insert_layout.addWidget(self.insert_btn)
        control_layout.addLayout(insert_layout)

        # 删除操作
        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel("删除位置:"))
        self.delete_idx = QSpinBox()
        self.delete_idx.setMinimum(0)
        delete_layout.addWidget(self.delete_idx)
        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self._on_delete_click)
        delete_layout.addWidget(self.delete_btn)
        control_layout.addLayout(delete_layout)

        # 更新操作
        update_layout = QHBoxLayout()
        update_layout.addWidget(QLabel("更新位置:"))
        self.update_idx = QSpinBox()
        self.update_idx.setMinimum(0)
        update_layout.addWidget(self.update_idx)
        update_layout.addWidget(QLabel("新值:"))
        self.update_val = QLineEdit()
        update_layout.addWidget(self.update_val)
        self.update_btn = QPushButton("更新")
        self.update_btn.clicked.connect(self._on_update_click)
        control_layout.addLayout(update_layout)

        # 查找操作
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("查找值:"))
        self.search_val = QLineEdit()
        search_layout.addWidget(self.search_val)
        self.search_btn = QPushButton("查找")
        self.search_btn.clicked.connect(self._on_search_click)
        control_layout.addLayout(search_layout)

        # 清空操作
        clear_layout = QHBoxLayout()
        self.clear_btn = QPushButton("清空链表")
        self.clear_btn.clicked.connect(self._on_clear_click)
        clear_layout.addWidget(self.clear_btn)
        control_layout.addLayout(clear_layout)

        right_layout.addLayout(control_layout)

    def _register_command_handlers(self):
        """注册所有DSL命令处理器"""
        self.command_handlers = {
            CommandType.INSERT: self._handle_insert_command,
            CommandType.DELETE: self._handle_delete_command,
            CommandType.UPDATE: self._handle_update_command,
            CommandType.SEARCH: self._handle_search_command,
            CommandType.TRAVERSE: self._handle_traverse_command,
            CommandType.CLEAR: self._handle_clear_command
        }

    # ========== DSL核心处理逻辑 ==========
    def _execute_dsl(self, dsl_text: str):
        """执行DSL脚本"""
        try:
            # 清空日志
            self.dsl_panel.log("=== 开始执行DSL ===")
            
            # 解析DSL脚本
            results = self.dsl_parser.parse_script(dsl_text)
            
            # 处理解析结果
            for item in results:
                if isinstance(item, StructureDeclaration):
                    # 处理结构声明（创建链表）
                    self._create_list_from_declaration(item)
                    self.dsl_panel.log(f"✅ 成功创建链表: {item.name}")
                
                elif isinstance(item, Command):
                    # 处理命令操作
                    handler = self.command_handlers.get(item.type)
                    if handler:
                        handler(item.params)
                        self.dsl_panel.log(f"✅ 执行命令: {item.type.value} {item.params}")
                    else:
                        self.dsl_panel.log(f"❌ 不支持的命令: {item.type.value}")
            
            # 刷新可视化
            self._refresh_canvas()
            
        except DSLParseError as e:
            self.dsl_panel.log(f"❌ 解析错误: {str(e)}")
        except ValueError as e:
            self.dsl_panel.log(f"❌ 参数错误: {str(e)}")
        except Exception as e:
            self.dsl_panel.log(f"❌ 执行错误: {str(e)}")

    def _create_list_from_declaration(self, decl: StructureDeclaration):
        """从DSL声明创建链表"""
        # 校验结构类型
        if decl.type not in [StructureType.SINGLY_LIST, StructureType.DOUBLY_LIST]:
            raise DSLParseError(f"不支持的结构类型: {decl.type.value} (需要链表类型)")
        
        # 清空现有链表
        self.linked_list.clear()
        
        # 设置链表类型（单/双向）
        self.linked_list.is_doubly = (decl.type == StructureType.DOUBLY_LIST)
        self.canvas.set_linked_list(self.linked_list)
        
        # 提取节点值和链接关系
        node_map = {}
        node_values = []
        
        # 第一步：收集所有节点值
        for node_id, dsl_node in decl.nodes.items():
            if "val" not in dsl_node.fields and "value" not in dsl_node.fields:
                raise DSLParseError(f"节点 {node_id} 缺少值字段（val/value）")
            
            # 兼容val/value字段
            node_val = dsl_node.fields.get("val") or dsl_node.fields.get("value")
            node_map[node_id] = {
                "val": node_val,
                "next": dsl_node.links[0] if dsl_node.links else None
            }
        
        # 第二步：构建链表（按节点顺序插入）
        # 找到头节点（通过prop.head或第一个节点）
        head_node_id = decl.props.get("head") or next(iter(node_map.keys()))
        
        # 遍历链表节点并插入
        current_node_id = head_node_id
        inserted_nodes = set()
        
        while current_node_id and current_node_id not in inserted_nodes:
            if current_node_id not in node_map:
                raise DSLParseError(f"节点 {current_node_id} 未定义")
            
            inserted_nodes.add(current_node_id)
            node_val = node_map[current_node_id]["val"]
            
            # 插入到链表末尾
            self.linked_list.insert(self.linked_list.size, node_val)
            
            # 获取下一个节点ID
            current_node_id = node_map[current_node_id]["next"]
            if current_node_id is None:
                break

    # ========== 命令处理器实现 ==========
    def _handle_insert_command(self, params: dict):
        """处理插入命令"""
        # 提取参数
        value = params.get("value")
        index = params.get("index", 0)
        
        # 参数校验
        if value is None:
            raise ValueError("插入命令缺少value参数")
        if not isinstance(value, (int, float, str)):
            raise ValueError(f"无效的value类型: {type(value)}")
        
        # 转换为整数（兼容数值类型）
        try:
            insert_val = int(value)
        except ValueError:
            insert_val = str(value)
        
        # 检查索引范围
        if index < 0 or index > self.linked_list.size:
            raise ValueError(f"插入索引 {index} 超出范围（0~{self.linked_list.size}）")
        
        # 执行插入
        success = self.linked_list.insert(index, insert_val)
        if not success:
            raise ValueError(f"插入失败: 索引 {index} 无效")
        
        # 更新UI控件
        self.insert_idx.setMaximum(self.linked_list.size)
        self.delete_idx.setMaximum(self.linked_list.size - 1)
        self.update_idx.setMaximum(self.linked_list.size - 1)

    def _handle_delete_command(self, params: dict):
        """处理删除命令"""
        # 支持index或value参数
        if "index" in params:
            index = params["index"]
            # 校验索引
            if index < 0 or index >= self.linked_list.size:
                raise ValueError(f"删除索引 {index} 超出范围（0~{self.linked_list.size-1}）")
            # 执行删除
            success = self.linked_list.delete(index)
            if not success:
                raise ValueError(f"删除失败: 索引 {index} 无效")
        
        elif "value" in params:
            # 按值删除（删除第一个匹配项）
            value = params["value"]
            try:
                search_val = int(value)
            except ValueError:
                search_val = str(value)
            
            index = self.linked_list.search(search_val)
            if index == -1:
                raise ValueError(f"删除失败: 未找到值 {value}")
            
            success = self.linked_list.delete(index)
            if not success:
                raise ValueError(f"删除失败: 值 {value} 对应的索引 {index} 无效")
        
        else:
            raise ValueError("删除命令需要index或value参数")
        
        # 更新UI控件
        self.insert_idx.setMaximum(self.linked_list.size)
        self.delete_idx.setMaximum(max(0, self.linked_list.size - 1))
        self.update_idx.setMaximum(max(0, self.linked_list.size - 1))

    def _handle_update_command(self, params: dict):
        """处理更新命令"""
        # 提取参数
        index = params.get("index")
        value = params.get("value")
        
        # 参数校验
        if index is None or value is None:
            raise ValueError("更新命令需要index和value参数")
        if index < 0 or index >= self.linked_list.size:
            raise ValueError(f"更新索引 {index} 超出范围（0~{self.linked_list.size-1}）")
        
        # 转换值类型
        try:
            update_val = int(value)
        except ValueError:
            update_val = str(value)
        
        # 执行更新
        success = self.linked_list.update(index, update_val)
        if not success:
            raise ValueError(f"更新失败: 索引 {index} 无效")

    def _handle_search_command(self, params: dict):
        """处理查找命令"""
        # 提取参数
        value = params.get("value")
        if value is None:
            raise ValueError("查找命令缺少value参数")
        
        # 转换值类型
        try:
            search_val = int(value)
        except ValueError:
            search_val = str(value)
        
        # 执行查找
        index = self.linked_list.search(search_val)
        if index == -1:
            self.dsl_panel.log(f"🔍 未找到值: {value}")
        else:
            self.dsl_panel.log(f"🔍 找到值 {value} 在索引位置: {index}")

    def _handle_traverse_command(self, params: dict):
        """处理遍历命令"""
        # 执行遍历
        values = self.linked_list.traverse()
        self.dsl_panel.log(f"📋 链表遍历结果: {values}")

    def _handle_clear_command(self, params: dict = None):
        """处理清空命令"""
        self.linked_list.clear()
        # 更新UI控件
        self.insert_idx.setMaximum(0)
        self.delete_idx.setMaximum(0)
        self.update_idx.setMaximum(0)
        self.dsl_panel.log("🗑️ 链表已清空")

    # ========== 原有UI事件处理 ==========
    def _on_insert_click(self):
        try:
            val = int(self.insert_val.text())
            idx = self.insert_idx.value()
            success = self.linked_list.insert(idx, val)
            if success:
                self._refresh_canvas()
                self.insert_idx.setMaximum(self.linked_list.size)
                self.delete_idx.setMaximum(self.linked_list.size - 1)
                self.update_idx.setMaximum(self.linked_list.size - 1)
                QMessageBox.information(self, "成功", "插入成功！")
            else:
                QMessageBox.warning(self, "失败", "插入失败，索引超出范围！")
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的整数！")

    def _on_delete_click(self):
        idx = self.delete_idx.value()
        success = self.linked_list.delete(idx)
        if success:
            self._refresh_canvas()
            self.insert_idx.setMaximum(self.linked_list.size)
            self.delete_idx.setMaximum(max(0, self.linked_list.size - 1))
            self.update_idx.setMaximum(max(0, self.linked_list.size - 1))
            QMessageBox.information(self, "成功", "删除成功！")
        else:
            QMessageBox.warning(self, "失败", "删除失败，索引超出范围！")

    def _on_update_click(self):
        try:
            val = int(self.update_val.text())
            idx = self.update_idx.value()
            success = self.linked_list.update(idx, val)
            if success:
                self._refresh_canvas()
                QMessageBox.information(self, "成功", "更新成功！")
            else:
                QMessageBox.warning(self, "失败", "更新失败，索引超出范围！")
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的整数！")

    def _on_search_click(self):
        try:
            val = int(self.search_val.text())
            idx = self.linked_list.search(val)
            if idx != -1:
                QMessageBox.information(self, "查找结果", f"值 {val} 在索引 {idx} 位置！")
            else:
                QMessageBox.information(self, "查找结果", f"未找到值 {val}！")
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的整数！")

    def _on_clear_click(self):
        self.linked_list.clear()
        self._refresh_canvas()
        self.insert_idx.setMaximum(0)
        self.delete_idx.setMaximum(0)
        self.update_idx.setMaximum(0)
        QMessageBox.information(self, "成功", "链表已清空！")

    def _refresh_canvas(self):
        """刷新可视化画布"""
        self.canvas.set_linked_list(self.linked_list)
        self.canvas.update()

# 测试入口
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # 测试单链表窗口
    window = ListWindow(is_doubly=False)
    window.show()
    
    sys.exit(app.exec())