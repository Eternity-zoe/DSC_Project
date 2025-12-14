import ast

class SequenceDSLParser:
    """
    把 DSL 文本解析成可执行命令列表
    """

    @staticmethod
    def parse(text: str):
        lines = text.splitlines()
        cmds = []

        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("sequence") or line in ("{", "}"):
                continue

            tokens = line.split()
            op = tokens[0]

            if op == "build":
                arr = ast.literal_eval(" ".join(tokens[1:]))
                cmds.append(("build", arr))

            elif op == "random":
                n, lo, hi = map(int, tokens[1:])
                cmds.append(("random", n, lo, hi))

            elif op == "insert":
                idx, val = int(tokens[1]), int(tokens[2])
                cmds.append(("insert", idx, val))

            elif op == "delete":
                idx = int(tokens[1])
                cmds.append(("delete", idx))

            elif op == "show":
                cmds.append(("show",))

            else:
                raise ValueError(f"未知 DSL 指令: {line}")

        return cmds
