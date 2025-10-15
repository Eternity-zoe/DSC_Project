# main.py
from PySide6.QtWidgets import QApplication
from gui.menu_window import MenuWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MenuWindow()
    w.show()
    sys.exit(app.exec())
#不要完全二叉树