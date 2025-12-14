from PySide6.QtWidgets import QApplication
from gui.menu_window import MenuWindow
import sys
import matplotlib

# 配置 matplotlib 字体（确保中文显示正常）
matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

if __name__ == "__main__":
    # 1. 首先创建 QApplication 实例（符合 Qt 要求）
    app = QApplication(sys.argv)
    
    # 2. 创建并显示主窗口（在 QApplication 之后，正确）
    w = MenuWindow()
    w.show()
    
    # 3. 启动事件循环（修正嵌套的 sys.exit()）
    sys.exit(app.exec())