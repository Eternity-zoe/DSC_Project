# core/tree_traversals.py
"""二叉树遍历算法集合（与GUI完全解耦）"""
from typing import List, Callable, TypeVar

# 泛型类型，代表任意树节点类型
TreeNode = TypeVar('TreeNode')

def preorder_traversal(root: TreeNode, get_left: Callable[[TreeNode], TreeNode], 
                       get_right: Callable[[TreeNode], TreeNode]) -> List[TreeNode]:
    """
    前序遍历（根-左-右）
    :param root: 树的根节点
    :param get_left: 获取左子节点的函数
    :param get_right: 获取右子节点的函数
    :return: 按遍历顺序排列的节点列表
    """
    result = []
    def dfs(node: TreeNode) -> None:
        if not node:
            return
        result.append(node)
        dfs(get_left(node))
        dfs(get_right(node))
    dfs(root)
    return result

def inorder_traversal(root: TreeNode, get_left: Callable[[TreeNode], TreeNode], 
                      get_right: Callable[[TreeNode], TreeNode]) -> List[TreeNode]:
    """中序遍历（左-根-右）"""
    result = []
    def dfs(node: TreeNode) -> None:
        if not node:
            return
        dfs(get_left(node))
        result.append(node)
        dfs(get_right(node))
    dfs(root)
    return result

def postorder_traversal(root: TreeNode, get_left: Callable[[TreeNode], TreeNode], 
                       get_right: Callable[[TreeNode], TreeNode]) -> List[TreeNode]:
    """后序遍历（左-右-根）"""
    result = []
    def dfs(node: TreeNode) -> None:
        if not node:
            return
        dfs(get_left(node))
        dfs(get_right(node))
        result.append(node)
    dfs(root)
    return result