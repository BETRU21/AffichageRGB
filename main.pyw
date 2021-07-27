from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.Window import Window
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Window()
    ui.setWindowTitle("This is the window title")
    ui.show()
    sys.exit(app.exec_())