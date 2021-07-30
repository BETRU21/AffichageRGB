from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.WindowController import WindowControl
from controller.ApplicationController import AppControl
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = WindowControl()
    ac = AppControl()
    ui.setWindowTitle("affichageRGB")
    ui.show()
    sys.exit(app.exec_())