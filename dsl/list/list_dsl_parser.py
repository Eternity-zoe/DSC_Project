# dsl/list/list_dsl_parser.py
import re
from dsl.list.list_dsl_ast import *

class ListDSLParser:

    def parse(self, script: str):
        cmds = []
        for lineno, raw in enumerate(script.splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("//"):
                continue
            if not line.endswith(";"):
                raise SyntaxError(f"第{lineno}行缺少分号")
            line = line[:-1]
            try:
                cmds.append(self._parse_line(line))
            except Exception as e:
                raise SyntaxError(f"第{lineno}行: {e}")
        return cmds

    def _parse_line(self, line: str):
        if line == "clear":
            return ClearCmd()

        if line.startswith("mode"):
            mode = line.split()[1]
            if mode not in ("singly", "doubly"):
                raise SyntaxError("mode 只能是 singly 或 doubly")
            return ModeCmd(mode)

        if line.startswith("build"):
            m = re.search(r"\[(.*)\]", line)
            if not m:
                raise SyntaxError("build 语法错误")
            values = [int(x) for x in m.group(1).split(",") if x.strip()]
            return BuildCmd(values)

        if line.startswith("insert head"):
            return InsertHeadCmd(int(line.split()[-1]))

        if line.startswith("insert tail"):
            return InsertTailCmd(int(line.split()[-1]))

        if line.startswith("insert index"):
            parts = line.split()
            idx = int(parts[2])
            val = int(parts[-1])
            return InsertIndexCmd(idx, val)

        if line == "delete head":
            return DeleteHeadCmd()

        if line == "delete tail":
            return DeleteTailCmd()

        if line.startswith("delete index"):
            return DeleteIndexCmd(int(line.split()[-1]))

        if line == "draw":
            return DrawCmd()

        raise SyntaxError(f"无法识别指令：{line}")
