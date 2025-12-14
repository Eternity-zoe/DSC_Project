# dsl/huffman/huffman_dsl_parser.py
import re

# ==============================
# AST 节点定义
# ==============================

class DSLCommand:
    pass


class ClearCmd(DSLCommand):
    pass


class BuildCmd(DSLCommand):
    def __init__(self, text: str):
        self.text = text


class DrawCmd(DSLCommand):
    pass


class ShowCodesCmd(DSLCommand):
    pass


class SaveCmd(DSLCommand):
    def __init__(self, path: str):
        self.path = path


class LoadCmd(DSLCommand):
    def __init__(self, path: str):
        self.path = path


# ==============================
# Parser 本体
# ==============================

class HuffmanDSLParser:
    """
    Huffman DSL Parser
    作用：
    - 将 DSL 文本解析为 AST（命令列表）
    - 不做任何执行
    """

    def parse(self, script: str):
        commands = []
        lines = self._preprocess(script)

        for line in lines:
            cmd = self._parse_line(line)
            commands.append(cmd)

        return commands

    # ==========================
    # 预处理
    # ==========================
    def _preprocess(self, script: str):
        lines = []
        for raw in script.splitlines():
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            if line.endswith(";"):
                line = line[:-1]
            lines.append(line)
        return lines

    # ==========================
    # 单行解析
    # ==========================
    def _parse_line(self, line: str) -> DSLCommand:
        if line.startswith("clear"):
            return ClearCmd()

        if line.startswith("build"):
            return self._parse_build(line)

        if line.startswith("draw"):
            return DrawCmd()

        if line.startswith("show_codes"):
            return ShowCodesCmd()

        if line.startswith("save"):
            return self._parse_save(line)

        if line.startswith("load"):
            return self._parse_load(line)

        raise SyntaxError(f"Huffman DSL 语法错误：{line}")

    # ==========================
    # 各命令解析
    # ==========================
    def _parse_build(self, line: str):
        """
        build MyHuff text="abc"
        """
        m = re.search(r'text\s*=\s*"(.+?)"', line)
        if not m:
            raise SyntaxError("build 指令缺少 text 参数")
        return BuildCmd(m.group(1))

    def _parse_save(self, line: str):
        """
        save MyHuff to "xxx.json"
        """
        m = re.search(r'to\s*"(.+?)"', line)
        if not m:
            raise SyntaxError("save 指令缺少 to 参数")
        return SaveCmd(m.group(1))

    def _parse_load(self, line: str):
        """
        load MyHuff from "xxx.json"
        """
        m = re.search(r'from\s*"(.+?)"', line)
        if not m:
            raise SyntaxError("load 指令缺少 from 参数")
        return LoadCmd(m.group(1))
