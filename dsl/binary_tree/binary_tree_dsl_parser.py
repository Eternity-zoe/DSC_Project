import re
from dsl.binary_tree.binary_tree_dsl_ast import *

class BinaryTreeDSLParser:

    def parse(self, script: str):
        cmds = []
        for lineno, raw in enumerate(script.splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            if not line.endswith(";"):
                raise SyntaxError(f"第 {lineno} 行缺少分号")
            line = line[:-1]

            try:
                cmds.append(self._parse_line(line))
            except Exception as e:
                raise SyntaxError(f"第 {lineno} 行: {e}")

        return cmds

    def _parse_line(self, line: str):
        if line == "clear":
            return ClearCmd()

        if line.startswith("build"):
            return self._parse_build(line)

        if line.startswith("insert"):
            val = int(line.split()[1])
            return InsertCmd(val)

        if line.startswith("traverse"):
            mode = line.split()[1]
            if mode not in ("preorder", "inorder", "postorder"):
                raise SyntaxError("traverse 只支持 preorder / inorder / postorder")
            return TraverseCmd(mode)

        if line == "draw":
            return DrawCmd()

        raise SyntaxError(f"无法识别指令：{line}")

    def _parse_build(self, line):
        # build random n=7
        # build complete n=7
        m = re.search(r'build\s+(random|complete)\s+n=(\d+)', line)
        if not m:
            raise SyntaxError("build 语法错误")

        kind = m.group(1)
        n = int(m.group(2))
        return BuildRandomCmd(n, complete=(kind == "complete"))
