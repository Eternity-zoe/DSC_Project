# core/stack.py
from typing import Any, Optional, List as PyList

class Stack:
    """
    栈（基于链表实现）
    遵循LIFO（后进先出）原则
    """
    MAX_SIZE = 10  # 最大栈容量
    MIN_VAL = -99  # 数据最小值
    MAX_VAL = 99  # 数据最大值

    def __init__(self):
        # 栈节点定义（内部类）
        class Node:
            def __init__(self, data: Any):
                self.data: Any = data
                self.next: Optional['Node'] = None
                # 可视化属性
                self.x: int = 350  # 栈节点X坐标（居中）
                self.y: int = 0     # 栈节点Y坐标（垂直排列）
                self.color: str = "#FFFFFF"  # 背景色
                self.label: str = str(data)  # 显示文本

        self.Node = Node  # 内部Node类
        self.top: Optional[Node] = None  # 栈顶指针
        self.size: int = 0  # 当前栈大小
        self.nodes: PyList[Node] = []  # 存储所有节点（用于可视化）

    def is_empty(self) -> bool:
        """判断栈是否为空"""
        return self.size == 0

    def is_full(self) -> bool:
        """判断栈是否已满"""
        return self.size >= self.MAX_SIZE

    # ------------------------------ 核心操作 ------------------------------
    def push(self, data: Any) -> None:
        """
        入栈（O(1)）
        :param data: 入栈数据
        """
        if self.is_full():
            raise ValueError(f"栈已满（最大容量{self.MAX_SIZE}）")
        if not (self.MIN_VAL <= data <= self.MAX_VAL):
            raise ValueError(f"数据需在[{self.MIN_VAL}, {self.MAX_VAL}]范围内")

        # 创建新节点
        new_node = self.Node(data)
        # 新节点成为新栈顶
        new_node.next = self.top
        self.top = new_node
        # 更新节点位置（垂直排列：栈顶在上，依次向下）
        self._update_layout()
        self.size += 1
        self.nodes.insert(0, new_node)  # 栈顶节点插入列表头部

    def pop(self) -> Optional[Any]:
        """
        出栈（O(1)）
        :return: 出栈数据
        """
        if self.is_empty():
            raise IndexError("空栈无法出栈")

        # 栈顶节点出栈
        popped_node = self.top
        self.top = self.top.next
        # 清理节点指针
        popped_data = popped_node.data
        popped_node.next = None
        # 更新布局
        self.size -= 1
        self.nodes.pop(0)  # 移除栈顶节点
        self._update_layout()

        return popped_data

    def peek(self) -> Optional[Any]:
        """
        查看栈顶元素（O(1)）
        :return: 栈顶数据
        """
        if self.is_empty():
            return None
        return self.top.data

    # ------------------------------ 可视化支持 ------------------------------
    def _update_layout(self):
        """更新所有节点的位置（垂直排列）"""
        for i, node in enumerate(self.nodes):
            # 栈顶在上方，每个节点间隔50像素
            node.y = 100 + i * 50

    def get_visual_data(self) -> dict:
        """获取可视化所需数据"""
        visual_data = {
            "size": self.size,
            "max_size": self.MAX_SIZE,
            "nodes": []
        }

        # 节点数据
        for i, node in enumerate(self.nodes):
            visual_data["nodes"].append({
                "data": node.data,
                "x": node.x,
                "y": node.y,
                "color": node.color,
                "label": node.label,
                "is_top": i == 0  # 第一个节点是栈顶
            })

        return visual_data

    # ------------------------------ 辅助操作 ------------------------------
    def clear(self) -> None:
        """清空栈"""
        self.top = None
        self.size = 0
        self.nodes.clear()

    def to_list(self) -> PyList[Any]:
        """转换为Python列表（栈顶在前）"""
        return [node.data for node in self.nodes]