from controller.ApplicationController import AppControl
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.WindowController import WindowControl
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = WindowControl()
    ac = AppControl()
    ac.windowControl = ui
    ui.appControl = ac
    ui.setWindowTitle("affichageRGB")
    ui.show()
    sys.exit(app.exec_())