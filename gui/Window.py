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

from controller.controller import control

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

        self.rangeLen = 255
        self.maxWaveLength = 255
        self.minWaveLength = 0
        self.doSliderPositionAreInitialize = False


        self.connect_widgets()
        self.update_slider_status()
        self.folderpath = ""

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




    def set_range_to_wave(self, minWaveLength, maxWaveLength, rangeLen):  # GUI
        self.sb_highRed.setMaximum(self.maxWaveLength)
        self.sb_lowRed.setMaximum(self.maxWaveLength-1)
        self.sb_highGreen.setMaximum(self.maxWaveLength)
        self.sb_lowGreen.setMaximum(self.maxWaveLength-1)
        self.sb_highBlue.setMaximum(self.maxWaveLength)
        self.sb_lowBlue.setMaximum(self.maxWaveLength-1)

        self.sb_highRed.setMinimum(self.minWaveLength)
        self.sb_lowRed.setMinimum(self.minWaveLength)
        self.sb_highGreen.setMinimum(self.minWaveLength)
        self.sb_lowGreen.setMinimum(self.minWaveLength)
        self.sb_highBlue.setMinimum(self.minWaveLength)
        self.sb_lowBlue.setMinimum(self.minWaveLength)
        self.sb_lowRed.setValue(self.minWaveLength)
        self.sb_highRed.setValue(round(self.rangeLen/3) + self.minWaveLength)
        self.sb_lowGreen.setValue(round(self.rangeLen/3) + self.minWaveLength + 1)
        self.sb_highGreen.setValue(round((self.rangeLen*(2/3)) + self.minWaveLength))
        self.sb_lowBlue.setValue(round((self.rangeLen*(2/3)) + self.minWaveLength+1))
        self.sb_highBlue.setValue(self.maxWaveLength)


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
        return round(((value - self.minWaveLength)/self.rangeLen) * 255)

    def mapping_on_spinBox(self, value):  # GUI
        return round((value/255) * self.rangeLen+self.minWaveLength)

    def update_slider_status(self):  # GUI
        self.dSlider_red.set_left_thumb_value(self.mapping_on_slider(self.sb_lowRed.value()))
        self.dSlider_red.set_right_thumb_value(self.mapping_on_slider(self.sb_highRed.value()))
        self.dSlider_green.set_left_thumb_value(self.mapping_on_slider(self.sb_lowGreen.value()))
        self.dSlider_green.set_right_thumb_value(self.mapping_on_slider(self.sb_highGreen.value()))
        self.dSlider_blue.set_left_thumb_value(self.mapping_on_slider(self.sb_lowBlue.value()))
        self.dSlider_blue.set_right_thumb_value(self.mapping_on_slider(self.sb_highBlue.value()))

        if self.doSliderPositionAreInitialize:
            try:
                self.update_spectrum_plot()
            except:
                pass
        else:
            self.doSliderPositionAreInitialize = True

    def update_color(self):  # Controller
        pass
        # try:
        #     self.matrixRGB_replace()
        #     self.update_rgb_plot()
        #     self.update_spectrum_plot()
        # except:
        #     pass

    def current_slider_value(self):
        pass





    def select_save_folder(self):
        self.folderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.GotFolderPath()
        # self.buildMatrix()
        # self.create_matrix_rgb()
        # self.matrixRGB_replace()
        self.pb_search.setEnabled(False)






    def update_rgb_plot(self, matrixRGB):
        vb = pg.ImageItem(image=matrixRGB)
        self.plotViewBox.addItem(vb)

    def update_spectrum_plot(self, matrix):
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






    def GotFolderPath(self):
        control().run(self.folderPath)