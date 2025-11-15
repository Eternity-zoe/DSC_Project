# main.py
from PySide6.QtWidgets import QApplication
from gui.menu_window import MenuWindow
import sys
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MenuWindow()
    w.show()
    # sys.exit(app.exec())
    sys.exit(sys.exit(app.exec()))