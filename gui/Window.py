import os
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np
import random
from PyQt5.QtCore import pyqtSignal, Qt, QThreadPool, QThread, QTimer
import ctypes
import sys

application_path = os.path.abspath("")

if sys.platform == "win32":
    myappid = u"mycompany.myproduct.subproduct.version" # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
else:
    pass

UiPath = os.path.dirname(os.path.realpath(__file__)) + '{0}Window.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(UiPath)

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(application_path + "{0}gui{0}misc{0}logo{0}logo.ico".format(os.sep)))





    def connect_widgets(self):
        self.graph_rgb.scene().sigMouseMoved.connect(self.mouse_moved)

    def mouse_moved(self, pos):  # GUI
        try:
            value = self.plotViewBox.mapSceneToView(pos)
            valueSTR = str(value)
            valueMin = valueSTR.find("(")
            valueMax = valueSTR.find(")")
            position = valueSTR[valueMin+1:valueMax]
            position = position.split(",")
            positionX = int(float(position[1]))
            positionY = int(float(position[0]))

            if positionX <= -1 or positionY <= -1:
                pass

            else:
                self.mousePositionX = positionX
                self.mousePositionY = positionY
                self.update_spectrum_plot()
        except Exception:
            pass

    def update_spectrum_plot(self):  # GUI
        if self.visualWithoutBackground:
            matrix = self.matrixDataWithoutBackground
        else:
            matrix = self.matrixRawData
        try:
            maximum = max(matrix[self.mousePositionY, self.mousePositionX, :])
            minimum = min(matrix[self.mousePositionY, self.mousePositionX, :]) - 1
        except Exception:
            maximum = 1
            minimum = 0

        if self.colorRangeViewEnable:
            lowRed = int(((self.sb_lowRed.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
            highRed = int(((self.sb_highRed.value() - self.minWaveLength) / self.rangeLen) * len(self.waves)-1)
            lowGreen = int(((self.sb_lowGreen.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
            highGreen = int(((self.sb_highGreen.value() - self.minWaveLength) / self.rangeLen) * len(self.waves)-1)
            lowBlue = int(((self.sb_lowBlue.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
            highBlue = int(((self.sb_highBlue.value() - self.minWaveLength) / self.rangeLen) * len(self.waves) - 1)

            self.redRange = np.full(len(self.waves), minimum)
            self.redRange[lowRed] = maximum
            self.redRange[highRed] = maximum

            self.greenRange = np.full(len(self.waves), minimum)
            self.greenRange[lowGreen] = maximum
            self.greenRange[highGreen] = maximum

            self.blueRange = np.full(len(self.waves), minimum)
            self.blueRange[lowBlue] = maximum
            self.blueRange[highBlue] = maximum

            self.plotRedRange.setData(self.waves, self.redRange, pen=(255, 0, 0))
            self.plotGreenRange.setData(self.waves, self.greenRange, pen=(0, 255, 0))
            self.plotBlueRange.setData(self.waves, self.blueRange, pen=(0, 0, 255))
            self.plotBlack.setData(self.waves, np.full(len(self.waves), minimum), pen=(0, 0, 0))

        if not self.colorRangeViewEnable:
            self.plotRedRange.setData(self.waves, np.full(len(self.waves), minimum), pen=(0, 0, 0))
            self.plotGreenRange.setData(self.waves, np.full(len(self.waves), minimum), pen=(0, 0, 0))
            self.plotBlueRange.setData(self.waves, np.full(len(self.waves), minimum), pen=(0, 0, 0))
            self.plotBlack.setData(self.waves, np.full(len(self.waves), minimum), pen=(0, 0, 0))

        self.plotSpectrum.setData(self.waves, matrix[self.mousePositionY, self.mousePositionX, :])


    def create_matrix_rgb(self):  # Controller? GUI? TODO
        self.matrixRGB = np.zeros((self.height, self.width, 3))
