import os
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt, QThreadPool, QThread, QTimer
from PyQt5.QtWidgets import QWidget, QFileDialog
import ctypes
import sys

import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import fnmatch
import time
import re


application_path = os.path.abspath("")

if sys.platform == "win32":
    myappid = u"mycompany.myproduct.subproduct.version" # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
else:
    pass

UiPath = os.path.dirname(os.path.realpath(__file__)) + '{0}WindowUI.ui'.format(os.sep)
print(UiPath)
Ui_MainWindow, QtBaseClass = uic.loadUiType(UiPath)

class WindowControl(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(application_path + "{0}gui{0}misc{0}logo{0}logo.ico".format(os.sep)))
        self.appController = None

        self.rangeLen = 1024
        #self.maxWave = 1024
        self.minWave = 0
        self.doSliderPositionAreInitialize = False
        self.folderpath = ""

        self.mousePositionX = None
        self.mousePositionY = None


        self.connect_widgets()
        self.update_slider_status()

    def connect_widgets(self):
        self.graph_rgb.scene().sigMouseMoved.connect(self.mouse_moved)
        self.pb_search.clicked.connect(self.select_save_folder)

        self.dSlider_red.valueChanged.connect(self.set_red_range)
        self.dSlider_green.valueChanged.connect(self.set_green_range)
        self.dSlider_blue.valueChanged.connect(self.set_blue_range)

        self.sb_highRed.valueChanged.connect(self.update_slider_status)
        self.sb_lowRed.valueChanged.connect(self.update_slider_status)
        self.sb_highGreen.valueChanged.connect(self.update_slider_status)
        self.sb_lowGreen.valueChanged.connect(self.update_slider_status)
        self.sb_highBlue.valueChanged.connect(self.update_slider_status)
        self.sb_lowBlue.valueChanged.connect(self.update_slider_status)

        self.pb_print.clicked.connect(self.signalTest)

    def signalTest(self):
        text = self.appController.get_text()
        self.print_test(text)

    def create_plot_rgb(self):
        self.graph_rgb.clear()
        self.plotViewBox = self.graph_rgb.addViewBox()
        self.plotViewBox.enableAutoRange()
        self.plotViewBox.invertY(True)
        self.plotViewBox.setAspectLocked()

    def create_plot_spectrum(self):
        self.graph_spectre.clear()
        self.plotItem = self.graph_spectre.addPlot()
        self.plotSpectrum = self.plotItem.plot()
        self.plotRedRange = self.plotItem.plot()
        self.plotGreenRange = self.plotItem.plot()
        self.plotBlueRange = self.plotItem.plot()
        self.plotBlack = self.plotItem.plot()
        self.plotItem.enableAutoRange()

    def mouse_moved(self, pos):
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


    def set_red_range(self):  # GUI
        self.sb_lowRed.setValue(self.mapping_on_spinBox(self.dSlider_red.get_left_thumb_value()))
        self.sb_highRed.setValue(self.mapping_on_spinBox(self.dSlider_red.get_right_thumb_value()))

        self.update_color()

    def set_green_range(self):  # GUI
        self.sb_lowGreen.setValue(self.mapping_on_spinBox(self.dSlider_green.get_left_thumb_value()))
        self.sb_highGreen.setValue(self.mapping_on_spinBox(self.dSlider_green.get_right_thumb_value()))

        self.update_color()

    def set_blue_range(self):  # GUI
        self.sb_lowBlue.setValue(self.mapping_on_spinBox(self.dSlider_blue.get_left_thumb_value()))
        self.sb_highBlue.setValue(self.mapping_on_spinBox(self.dSlider_blue.get_right_thumb_value()))

        self.update_color()

    def mapping_on_slider(self, value):  # GUI
        return round(((value - self.minWave)/self.rangeLen) * 1024)

    def mapping_on_spinBox(self, value):  # GUI
        return round((value/1024) * self.rangeLen+self.minWave)

    def update_slider_status(self):  # GUI
        self.dSlider_red.set_left_thumb_value(self.mapping_on_slider(self.sb_lowRed.value()))
        self.dSlider_red.set_right_thumb_value(self.mapping_on_slider(self.sb_highRed.value()))
        self.dSlider_green.set_left_thumb_value(self.mapping_on_slider(self.sb_lowGreen.value()))
        self.dSlider_green.set_right_thumb_value(self.mapping_on_slider(self.sb_highGreen.value()))
        self.dSlider_blue.set_left_thumb_value(self.mapping_on_slider(self.sb_lowBlue.value()))
        self.dSlider_blue.set_right_thumb_value(self.mapping_on_slider(self.sb_highBlue.value()))

        if self.doSliderPositionAreInitialize:
            try:
                self.current_slider_value()
                self.update_spectrum_plot()
            except:
                pass
        else:
            self.doSliderPositionAreInitialize = True

    def current_slider_value(self):
        lowRedValue = self.dSlider_red.get_left_thumb_value() / 1024
        highRedValue = self.dSlider_red.get_right_thumb_value() / 1024
        lowGreenValue = self.dSlider_green.get_left_thumb_value() / 1024
        highGreenValue = self.dSlider_green.get_right_thumb_value() / 1024
        lowBlueValue = self.dSlider_blue.get_left_thumb_value() / 1024
        highBlueValue = self.dSlider_blue.get_right_thumb_value() / 1024
        print([lowRedValue, highRedValue, lowGreenValue, highGreenValue, lowBlueValue, highBlueValue])
        return [lowRedValue, highRedValue, lowGreenValue, highGreenValue, lowBlueValue, highBlueValue]





    def select_save_folder(self):
        self.folderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.GotFolderPath()
        # self.pb_search.setEnabled(False)
        return self.folderPath






    def update_rgb_plot(self, matrixRGB):
        vb = pg.ImageItem(image=matrixRGB)
        self.plotViewBox.addItem(vb)

    def update_spectrum_plot(self, waves, matrixData):
        # Set the maximum to see the RGB limits and the spectrum clearly
        try:
            maximum = max(matrixData[self.mousePositionY, self.mousePositionX, :])
            minimum = min(matrixdata[self.mousePositionY, self.mousePositionX, :]) - 1
        except Exception:
            maximum = 1
            minimum = 0

        wavesLen = len(waves)
        colorValues = current_slider_value()

        # Set the position of the RGB limits
        lowRed = int( colorValues[0] * wavesLen )
        highRed = int( colorValues[1] * wavesLen )
        lowGreen = int( colorValues[2] * wavesLen )
        highGreen = int( colorValues[3] * wavesLen )
        lowBlue = int( colorValues[4] * wavesLen )
        highBlue = int( colorValues[5] * wavesLen )

        redRange = np.full(wavesLen, minimum)
        redRange[lowRed] = maximum
        redRange[highRed] = maximum

        greenRange = np.full(wavesLen, minimum)
        greenRange[lowGreen] = maximum
        greenRange[highGreen] = maximum

        blueRange = np.full(wavesLen, minimum)
        blueRange[lowBlue] = maximum
        blueRange[highBlue] = maximum

        self.plotRedRange.setData(waves, redRange, pen=(255, 0, 0))
        self.plotGreenRange.setData(waves, greenRange, pen=(0, 255, 0))
        self.plotBlueRange.setData(waves, blueRange, pen=(0, 0, 255))
        self.plotBlack.setData(waves, np.full(wavesLen, minimum), pen=(0, 0, 0))

        self.plotSpectrum.setData(waves, matrixData[self.mousePositionY, self.mousePositionX, :])

    def GotFolderPath(self):
        pass
        # LoadData
        # Show the matrixRGB

    def update_color(self):  # Controller
        pass
        # try:
        #     self.matrixRGB_replace()
        #     self.update_rgb_plot()
        #     self.update_spectrum_plot()
        # except:
        #     pass

    def set_range_to_wave(self):  # GUI
        pass
    #     self.sb_highRed.setMaximum(self.maxWave)
    #     self.sb_lowRed.setMaximum(self.maxWave-1)
    #     self.sb_highGreen.setMaximum(self.maxWave)
    #     self.sb_lowGreen.setMaximum(self.maxWave-1)
    #     self.sb_highBlue.setMaximum(self.maxWave)
    #     self.sb_lowBlue.setMaximum(self.maxWave-1)

    #     self.sb_highRed.setMinimum(self.minWave)
    #     self.sb_lowRed.setMinimum(self.minWave)
    #     self.sb_highGreen.setMinimum(self.minWave)
    #     self.sb_lowGreen.setMinimum(self.minWave)
    #     self.sb_highBlue.setMinimum(self.minWave)
    #     self.sb_lowBlue.setMinimum(self.minWave)
    #     self.sb_lowRed.setValue(self.minWave)
    #     self.sb_highRed.setValue(round(self.rangeLen/3) + self.minWave)
    #     self.sb_lowGreen.setValue(round(self.rangeLen/3) + self.minWave + 1)
    #     self.sb_highGreen.setValue(round((self.rangeLen*(2/3)) + self.minWave))
    #     self.sb_lowBlue.setValue(round((self.rangeLen*(2/3)) + self.minWave+1))
    #     self.sb_highBlue.setValue(self.maxWave)