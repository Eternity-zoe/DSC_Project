# dsl/huffman/huffman_dsl_executor.py

from core.huffman_tree import HuffmanTree
from dsl.huffman.huffman_dsl_parser import (
    ClearCmd, BuildCmd, DrawCmd,
    ShowCodesCmd, SaveCmd, LoadCmd
)


class HuffmanDSLExecutor:
    """
    AST 驱动的 Huffman DSL Executor
    - 不解析 DSL 字符串
    - 只执行 AST
    """

    def __init__(self, window):
        self.window = window  # HuffmanWindow 实例

    # ==============================
    # 生命周期控制
    # ==============================
    def reset_context(self):
        """执行 DSL 前的统一清空逻辑"""
        self.window.timer.stop()

        self.window.tree = HuffmanTree()
        self.window.tree.add_listener(self.window.on_update)

        self.window.code_display.clear()
        self.window.build_steps = []
        self.window.step_index = 0

        self.window.draw_tree(None)

    # ==============================
    # AST 执行入口
    # ==============================
    def execute_ast(self, commands):
        """
        commands: List[DSLCommand]
        """
        self.reset_context()

        for cmd in commands:
            self._execute_cmd(cmd)

    # ==============================
    # 单条命令分发
    # ==============================
    def _execute_cmd(self, cmd):
        if isinstance(cmd, ClearCmd):
            self._cmd_clear()

        elif isinstance(cmd, BuildCmd):
            self._cmd_build(cmd)

        elif isinstance(cmd, DrawCmd):
            self._cmd_draw()

        elif isinstance(cmd, ShowCodesCmd):
            self._cmd_show_codes()

        elif isinstance(cmd, SaveCmd):
            self._cmd_save(cmd)

        elif isinstance(cmd, LoadCmd):
            self._cmd_load(cmd)

        else:
            raise RuntimeError(f"未知 AST 命令类型：{type(cmd)}")

    # ==============================
    # 命令具体实现
    # ==============================
    def _cmd_clear(self):
        self.reset_context()

    def _cmd_build(self, cmd: BuildCmd):
        self.window.tree.build(cmd.text)

    def _cmd_draw(self):
        self.window.draw_tree(self.window.tree.root)

    def _cmd_show_codes(self):
        code_map = self.window.tree.code_map
        text = "哈夫曼编码表：\n"
        for ch, code in code_map.items():
            text += f"'{ch}' -> {code}\n"
        self.window.code_display.setText(text)

    def _cmd_save(self, cmd: SaveCmd):
        self.window.tree.save_to_file(cmd.path)

    def _cmd_load(self, cmd: LoadCmd):
        self.window.tree.load_from_file(cmd.path)
        self.window.draw_tree(self.window.tree.root)
