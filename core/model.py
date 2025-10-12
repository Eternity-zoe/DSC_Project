# core/model.py
import random
import copy

class ArrayModel:
    """
    纯业务逻辑类（Model）。
    不含任何 GUI 代码，通过 add_listener(cb) 注册回调以通知 UI 状态变化。
    回调接收一个字典：{'array': [...], 'action': {...}}
    """
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.arr = []
        self._listeners = []

    def add_listener(self, cb):
        """cb(state_dict)"""
        self._listeners.append(cb)

    def _notify(self, action=None):
        state = {'array': copy.deepcopy(self.arr), 'action': action}
        for cb in self._listeners:
            try:
                cb(state)
            except Exception as e:
                # Model 不处理 GUI 错误，只打印
                print("Listener error:", e)

    def create_random(self, m=20, n=10, low=0, high=99):
        n = min(n, m, self.max_size)
        self.arr = [random.randint(low, high) for _ in range(n)]
        self._notify({'type':'create','m':m,'n':n})
        return self.arr

    def append(self, v):
        if len(self.arr) >= self.max_size:
            raise ValueError("Array 已满")
        self.arr.append(v)
        self._notify({'type':'append','value':v})

    def insert(self, i, v):
        if i < 0 or i > len(self.arr):
            raise IndexError("索引越界")
        self.arr.insert(i, v)
        self._notify({'type':'insert','index':i,'value':v})

    def remove(self, i):
        if i < 0 or i >= len(self.arr):
            raise IndexError("索引越界")
        val = self.arr.pop(i)
        self._notify({'type':'remove','index':i,'value':val})
        return val

    def update(self, i, v):
        if i < 0 or i >= len(self.arr):
            raise IndexError("索引越界")
        old = self.arr[i]
        self.arr[i] = v
        self._notify({'type':'update','index':i,'old':old,'new':v})
        return old

    def count(self, v):
        c = self.arr.count(v)
        self._notify({'type':'count','value':v,'result':c})
        return c

    def search(self, v):
        res = [i for i, x in enumerate(self.arr) if x == v]
        self._notify({'type':'search','value':v,'result':res})
        return res

    def two_sum(self, target):
        seen = {}
        for i, v in enumerate(self.arr):
            if target - v in seen:
                self._notify({'type':'two_sum','target':target,'result':(seen[target-v], i)})
                return (seen[target-v], i)
            seen[v] = i
        self._notify({'type':'two_sum','target':target,'result':None})
        return None
