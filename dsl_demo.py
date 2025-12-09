# 关键：添加当前目录到Python搜索路径（确保能导入api和core）
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入核心API（直接从api导入，因为api和脚本同级）
from api import DataStructureDrawer

# 修复后的DSL文本（紧凑格式，无多余空行，确保正则能匹配）
dsl_text = """array ScoreArray {
    node arr0 { int value = 95; }
    node arr1 { int value = 88; }
    node arr2 { int value = 92; }
    prop length = 3;
}"""

# 初始化工具并解析DSL
drawer = DataStructureDrawer()
mermaid_code = drawer.from_dsl(dsl_text)

# 打印生成的Mermaid代码（复制到在线编辑器即可渲染）
print("="*50)
print("生成的Mermaid代码（复制以下内容到https://mermaid-js.github.io/mermaid-live-editor/）：")
print("="*50)
print(mermaid_code)