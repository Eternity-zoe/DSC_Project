# core/list.py
import time
from typing import Any, Optional, List as PyList

class Node:
    """
    链表节点结构
    - 单链表(LL)：仅使用 next 指针
    - 双链表(DLL)：使用 next 和 prev 指针
    """
    def __init__(self, data: Any, vtx_idx: int):
        self.data: Any = data  # 节点存储的数据
        self.id: float = time.time() + vtx_idx / 1000.0  # 唯一标识（用于可视化）
        self.next: Optional['Node'] = None  # 指向下一节点
        self.prev: Optional['Node'] = None  # 指向前一节点（双链表专用）
        
        # 可视化相关属性
        self.vtx_idx: int = vtx_idx  # 可视化索引
        self.x: int = 0  # 节点X坐标
        self.y: int = 100  # 节点Y坐标（默认水平排列）
        self.color: str = "#FFFFFF"  # 节点背景色
        self.label: str = str(data)  # 节点显示文本

    def __repr__(self):
        return f"Node(data={self.data}, vtx_idx={self.vtx_idx})"

class List:
    """
    单链表/双链表核心实现
    支持模式："singly"（单链表）、"doubly"（双链表）
    """
    MAX_NODES = 15  # 最大节点数限制
    MIN_VAL = -99  # 数据最小值
    MAX_VAL = 99  # 数据最大值

    def __init__(self, mode: str = "singly"):
        if mode not in ["singly", "doubly"]:
            raise ValueError("模式仅支持 'singly'（单链表）或 'doubly'（双链表）")
        
        self.mode: str = mode  # 链表模式
        self.head: Optional[Node] = None  # 头节点
        self.tail: Optional[Node] = None  # 尾节点
        self.size: int = 0  # 当前节点数
        self.nodes: PyList[Node] = []  # 存储所有节点（用于可视化）

    def is_doubly(self) -> bool:
        """判断是否为双链表"""
        return self.mode == "doubly"

    def is_empty(self) -> bool:
        """判断链表是否为空"""
        return self.size == 0

    def _create_node(self, data: Any) -> Node:
        """创建新节点并初始化位置"""
        vtx_idx = self.size
        node = Node(data, vtx_idx)
        # 水平布局：每个节点间隔80像素
        node.x = 50 + vtx_idx * 80
        return node

    def _update_layout(self):
        """更新所有节点的索引和位置（用于插入/删除后的重新布局）"""
        current = self.head
        idx = 0
        self.nodes.clear()
        
        while current:
            current.vtx_idx = idx
            current.x = 50 + idx * 80  # 重新计算X坐标
            self.nodes.append(current)
            current = current.next
            idx += 1
        
        self.size = idx

    # ------------------------------ 查找操作 ------------------------------
    def find(self, value: Any) -> Optional[Node]:
        """
        查找指定值的节点
        :return: 找到返回节点，未找到返回None
        时间复杂度：O(N)
        """
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    # ------------------------------ 插入操作 ------------------------------
    def insert_head(self, data: Any) -> None:
        """
        头插入（O(1)）
        :param data: 插入的数据
        """
        if self.size >= self.MAX_NODES:
            raise ValueError(f"链表已满（最大{self.MAX_NODES}个节点）")
        if not (self.MIN_VAL <= data <= self.MAX_VAL):
            raise ValueError(f"数据需在[{self.MIN_VAL}, {self.MAX_VAL}]范围内")

        new_node = self._create_node(data)
        if self.is_empty():
            # 空链表：头尾节点都指向新节点
            self.head = self.tail = new_node
        else:
            # 新节点next指向原头节点
            new_node.next = self.head
            # 双链表：原头节点prev指向新节点
            if self.is_doubly():
                self.head.prev = new_node
            # 更新头节点
            self.head = new_node

        self.size += 1
        self._update_layout()

    def insert_tail(self, data: Any) -> None:
        """
        尾插入（单链表O(N)，双链表O(1)）
        :param data: 插入的数据
        """
        if self.size >= self.MAX_NODES:
            raise ValueError(f"链表已满（最大{self.MAX_NODES}个节点）")
        if not (self.MIN_VAL <= data <= self.MAX_VAL):
            raise ValueError(f"数据需在[{self.MIN_VAL}, {self.MAX_VAL}]范围内")

        new_node = self._create_node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            # 原尾节点next指向新节点
            self.tail.next = new_node
            # 双链表：新节点prev指向原尾节点
            if self.is_doubly():
                new_node.prev = self.tail
            # 更新尾节点
            self.tail = new_node

        self.size += 1
        self._update_layout()

    def insert_at_index(self, data: Any, index: int) -> None:
        """
        中间插入（O(N)）
        :param data: 插入的数据
        :param index: 插入位置（0-based）
        """
        if index < 0 or index > self.size:
            raise IndexError(f"索引越界，有效范围[0, {self.size}]")
        if index == 0:
            return self.insert_head(data)
        if index == self.size:
            return self.insert_tail(data)

        # 找到插入位置的前驱节点
        prev_node = self.head
        for _ in range(index - 1):
            prev_node = prev_node.next

        aft_node = prev_node.next  # 后继节点
        new_node = self._create_node(data)

        # 更新next指针
        new_node.next = aft_node
        prev_node.next = new_node

        # 双链表：更新prev指针
        if self.is_doubly():
            new_node.prev = prev_node
            aft_node.prev = new_node

        self.size += 1
        self._update_layout()

    # ------------------------------ 删除操作 ------------------------------
    def delete_head(self) -> Optional[Any]:
        """
        头删除（O(1)）
        :return: 删除的节点数据
        """
        if self.is_empty():
            raise IndexError("空链表无法删除")

        deleted_node = self.head
        if self.size == 1:
            # 只有一个节点：头尾都置空
            self.head = self.tail = None
        else:
            # 头节点后移
            self.head = self.head.next
            # 双链表：新头节点prev置空
            if self.is_doubly():
                self.head.prev = None

        # 清理删除节点的指针
        deleted_data = deleted_node.data
        deleted_node.next = None
        deleted_node.prev = None

        self.size -= 1
        self._update_layout()
        return deleted_data

    def delete_tail(self) -> Optional[Any]:
        """
        尾删除（单链表O(N)，双链表O(1)）
        :return: 删除的节点数据
        """
        if self.is_empty():
            raise IndexError("空链表无法删除")

        deleted_node = self.tail
        if self.size == 1:
            self.head = self.tail = None
        else:
            if self.is_doubly():
                # 双链表：直接通过prev找到前驱
                prev_node = self.tail.prev
            else:
                # 单链表：遍历找到前驱
                prev_node = self.head
                while prev_node.next != self.tail:
                    prev_node = prev_node.next

            # 前驱节点next置空
            prev_node.next = None
            # 更新尾节点
            self.tail = prev_node

        # 清理删除节点的指针
        deleted_data = deleted_node.data
        deleted_node.next = None
        deleted_node.prev = None

        self.size -= 1
        self._update_layout()
        return deleted_data

    def delete_at_index(self, index: int) -> Optional[Any]:
        """
        中间删除（O(N)）
        :param index: 删除位置（0-based）
        :return: 删除的节点数据
        """
        if index < 0 or index >= self.size:
            raise IndexError(f"索引越界，有效范围[0, {self.size-1}]")
        if index == 0:
            return self.delete_head()
        if index == self.size - 1:
            return self.delete_tail()

        # 找到删除位置的前驱节点
        prev_node = self.head
        for _ in range(index - 1):
            prev_node = prev_node.next

        deleted_node = prev_node.next  # 待删除节点
        aft_node = deleted_node.next  # 后继节点

        # 更新next指针
        prev_node.next = aft_node

        # 双链表：更新prev指针
        if self.is_doubly():
            aft_node.prev = prev_node

        # 清理删除节点的指针
        deleted_data = deleted_node.data
        deleted_node.next = None
        deleted_node.prev = None

        self.size -= 1
        self._update_layout()
        return deleted_data

    # ------------------------------ 可视化支持 ------------------------------
    def get_visual_data(self) -> dict:
        """
        获取可视化所需数据
        :return: 包含节点和边信息的字典
        """
        visual_data = {
            "mode": self.mode,
            "size": self.size,
            "nodes": [],
            "edges": []
        }

        # 节点数据
        head_id = self.head.id if self.head else None
        tail_id = self.tail.id if self.tail else None
        for node in self.nodes:
            visual_data["nodes"].append({
                "id": node.id,
                "data": node.data,
                "vtx_idx": node.vtx_idx,
                "x": node.x,
                "y": node.y,
                "color": node.color,
                "label": node.label,
                "is_head": node.id == head_id,
                "is_tail": node.id == tail_id
            })

        # 边数据（单链表：next边；双链表：next+prev边）
        for node in self.nodes:
            # Next边（正向）
            if node.next:
                visual_data["edges"].append({
                    "source_id": node.id,
                    "target_id": node.next.id,
                    "type": "next",
                    "color": "#008000",
                    "idx": node.vtx_idx
                })
            # Prev边（反向，双链表专用）
            if self.is_doubly() and node.prev:
                visual_data["edges"].append({
                    "source_id": node.id,
                    "target_id": node.prev.id,
                    "type": "prev",
                    "color": "#FFA500",
                    "idx": node.vtx_idx + 5000  # 避免ID冲突
                })

        return visual_data

    # ------------------------------ 辅助操作 ------------------------------
    def clear(self) -> None:
        """清空链表"""
        current = self.head
        while current:
            next_node = current.next
            current.next = None
            current.prev = None
            current = next_node
        
        self.head = self.tail = None
        self.size = 0
        self.nodes.clear()

    def to_list(self) -> PyList[Any]:
        """转换为Python列表"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result