import heapq
from collections import defaultdict
import json

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char  # 字符，仅叶子节点有值
        self.freq = freq  # 频率
        self.left = left  # 左子树（0）
        self.right = right  # 右子树（1）
        self.code = ""  # 哈夫曼编码
        
    # 用于堆排序
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanTree:
    def __init__(self):
        self.root = None
        self.code_map = {}  # 字符到编码的映射
        self.listeners = []
        
    def add_listener(self, func):
        self.listeners.append(func)
        
    def notify(self, action, node=None, extra=None):
        for f in self.listeners:
            f({"action": action, "node": node, "tree": self.root, "extra": extra})
    
    def build(self, text):
        """从文本构建哈夫曼树"""
        if not text:
            self.root = None
            self.notify("build", None, extra=None)
            return
            
        # 计算频率
        freq_dict = defaultdict(int)
        for char in text:
            freq_dict[char] += 1
            
        # 构建最小堆
        heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
        heapq.heapify(heap)
        
        # 构建哈夫曼树
        steps = []
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # 合并节点
            merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)
            
            steps.append((left, right, merged))  # 记录构建步骤
        
        self.root = heap[0] if heap else None
        # 生成编码
        self._generate_codes(self.root, "")
        self.notify("build", self.root, extra={"steps": steps, "code_map": self.code_map})
        
    def _generate_codes(self, node, current_code):
        """递归生成哈夫曼编码"""
        if node is None:
            return
            
        if node.char is not None:
            node.code = current_code
            self.code_map[node.char] = current_code
            return
            
        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    def serialize(self):
        """将哈夫曼树序列化为 dict"""
        def dfs(node):
            if node is None:
                return None
            if node.char is not None:
                return {
                    "type": "L",
                    "char": node.char,
                    "freq": node.freq
                }
            return {
                "type": "I",
                "freq": node.freq,
                "left": dfs(node.left),
                "right": dfs(node.right)
            }

        return {
            "type": "huffman_tree",
            "version": 1,
            "root": dfs(self.root)
        }

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.serialize(), f, ensure_ascii=False, indent=2)  

    def load_from_dict(self, data):
        """从 dict 恢复哈夫曼树"""
        def build(node_data):
            if node_data is None:
                return None

            if node_data["type"] == "L":
                return HuffmanNode(
                    char=node_data["char"],
                    freq=node_data["freq"]
                )

            node = HuffmanNode(freq=node_data["freq"])
            node.left = build(node_data["left"])
            node.right = build(node_data["right"])
            return node

        self.root = build(data["root"])
        self.code_map.clear()
        self._generate_codes(self.root, "")
        self.notify(
            "build",
            self.root,
            extra={
                "steps": steps,
                "code_map": self.code_map
            }
        )

    def load_from_file(self, path):
        import json
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.load_from_dict(data)
          