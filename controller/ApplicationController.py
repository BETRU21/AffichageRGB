import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.HyperSpectralImage import HyperSpectralImage

class AppControl():
    def __init__(self):
        self.HSI = HyperSpectralImage()
        self.windowController = None

    def matrixData(self):
        matrixData = self.HSI.matrixData(self.HSI.data)
        return matrixData

    def matrixRGB(self, globalMaximum=True):
        colorValues = self.windowController.current_slider_value()
        matrixRGB = self.HSI.matrixRGB(self.HSI.data, colorValues, globalMaximum)
        return matrixRGB

    def waves(self):
        waves = self.HSI.wavelength
        return waves

    def loadData(self, path):
        self.HSI.loadData(path)
        colorValues = self.windowController.current_slider_value()

    def spectrum(self, x, y):
        spectrum = self.HSI.spectrum(x, y, self.HSI.data)
        return spectrum





