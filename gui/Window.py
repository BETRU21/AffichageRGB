import os
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import numpy as np
from tools.ThreadWorker import Worker
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

UiPath = os.path.dirname(os.path.realpath(__file__)) + '{0}Window.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(UiPath)

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(application_path + "{0}gui{0}misc{0}logo{0}logo.ico".format(os.sep)))
        self.connect_widgets()
        self.folderpath = ""

    def connect_widgets(self):
        self.graph_rgb.scene().sigMouseMoved.connect(self.mouse_moved)
        self.pb_search.clicked.connect(self.select_save_folder)

    def select_save_folder(self):
        self.folderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.buildMatrix()
        self.create_matrix_rgb()
        self.matrixRGB_replace()
        self.pb_search.setEnabled(False)

    def buildMatrix(self):
        foundFiles = []
        for file in os.listdir(self.folderPath):
            if fnmatch.fnmatch(file, f'*.csv'):
                foundFiles.append(file)

        nb = len(foundFiles)
        print("nombre de fichier :", nb)

        sortedPaths = (foundFiles)
        val1Max = 0
        val2Max = 0
        dataLen = 0

        for i in range(nb):
            nom = sortedPaths[i]
            matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", nom)
            if matchObj:
                val1 = int(matchObj.group(1))
                val2 = int(matchObj.group(2))
                # Nom du fichier à importer
                fich = open(self.folderPath + '/' + nom, "r")
                test_str = list(fich)[14:]
                fich.close()
                x = []
                if val1 > val1Max:
                    val1Max = val1
                if val2 > val2Max:
                    val2Max = val2
                # Nettoyer les informations
                if dataLen == 0:
                    for j in test_str:
                        elem_str = j.replace("\n", "")
                        elem = elem_str.split(",")
                        x.append(float(elem[1]))
                    dataLen = len(x)
                else:
                    pass


        self.matrixRawData = np.zeros((val2Max+1, val1Max+1, dataLen))

        for i in range(nb):
            nom = sortedPaths[i]
            matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", nom)
            if matchObj:
                val1 = int(matchObj.group(1))
                val2 = int(matchObj.group(2))
                # Nom du fichier à importer
                fich = open(self.folderPath + '/' + nom, "r")
                test_str = list(fich)[14:]
                fich.close()
                x = []
                y = []
                # Nettoyer les informations
                for j in test_str:
                    elem_str = j.replace("\n", "")
                    elem = elem_str.split(",")
                    y.append(float(elem[1]))
                self.matrixRawData[val1, val2, :] = y
        print(self.matrixRawData)

    def listNameOfFiles(directory: str, extension="csv") -> list:
        foundFiles = []
        for file in os.listdir(directory):
            if fnmatch.fnmatch(file, f'*.{extension}'):
                foundFiles.append(file)
        return foundFiles

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

    def create_matrix_raw_data(self):  # Model
        self.matrixRawData = np.zeros((self.height, self.width, self.dataLen))

    def create_matrix_rgb(self):
        self.matrixRGB = np.zeros((self.height, self.width, 3))

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

    def update_spectrum_plot(self):
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


    def matrixRGB_replace(self):

        matrix = self.matrixRawData

        lowRed = int(((self.sb_lowRed.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
        highRed = int(((self.sb_highRed.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
        lowGreen = int(((self.sb_lowGreen.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
        highGreen = int(((self.sb_highGreen.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
        lowBlue = int(((self.sb_lowBlue.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))
        highBlue = int(((self.sb_highBlue.value() - self.minWaveLength) / self.rangeLen) * len(self.waves))

        self.matrixRGB[:, :, 0] = matrix[:, :, lowRed:highRed].sum(axis=2)
        self.matrixRGB[:, :, 1] = matrix[:, :, lowGreen:highGreen].sum(axis=2)
        self.matrixRGB[:, :, 2] = matrix[:, :, lowBlue:highBlue].sum(axis=2)

        if self.cmb_set_maximum.currentIndex() == 0:
            self.matrixRGB = (self.matrixRGB / np.max(self.matrixRGB)) * 255

        elif self.cmb_set_maximum.currentIndex() == 1:
            maxima = self.matrixRGB.max(axis=2)
            maxima = np.dstack((maxima,) * 3)
            np.seterr(divide='ignore', invalid='ignore')
            self.matrixRGB /= maxima
            self.matrixRGB[np.isnan(self.matrixRGB)] = 0
            self.matrixRGB *= 255

        self.matrixRGB = self.matrixRGB.round(0)


    def update_rgb_plot(self):
        vb = pg.ImageItem(image=self.matrixRGB)
        self.plotViewBox.addItem(vb)

    def update_spectrum_plot(self):
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