# dsl/stack/stack_dsl_parser.py

class StackDSLParser:
    """
    Stack DSL 解析器
    行级语义，一行一个命令
    """

    @staticmethod
    def parse(text: str):
        cmds = []
        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            op = parts[0].lower()

            if op == "stack":
                cmds.append(("stack", parts[1] if len(parts) > 1 else "Unnamed"))

            elif op == "push":
                cmds.append(("push", int(parts[1])))

            elif op == "pop":
                cmds.append(("pop",))

            elif op == "peek":
                cmds.append(("peek",))

            elif op == "clear":
                cmds.append(("clear",))

            elif op == "random":
                cmds.append(("random", int(parts[1])))

            elif op == "sleep":
                cmds.append(("sleep", int(parts[1])))

            elif op == "end":
                cmds.append(("end",))

            else:
                raise ValueError(f"第 {lineno} 行：未知 DSL 指令 `{line}`")

        return cmds
