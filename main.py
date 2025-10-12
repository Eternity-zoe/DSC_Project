# main.py
import sys
from PySide6.QtWidgets import QApplication
from core.model import ArrayModel
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    model = ArrayModel(max_size=500)
    win = MainWindow(model)
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
