import numpy as np
from typing import NamedTuple

class Pixel(NamedTuple):
    x: int=None
    y: int=None
    spectrum: object=None

class HyperSpectralImage:
    def __init__(self, averageMultipleSpectra=True):
        self.data = []
        self.wavelength = []
        self.averageMultipleSpectra = averageMultipleSpectra

    def addWavelength(self, wavelength):
        self.wavelength = np.array(wavelength)

    def deleteWavelength(self):
        self.wavelength = []

    def returnWaveNumber(self, laser):
        waveNumber = ((1 / laser) - (1 / self.wavelength)) * 10 ** 7
        return waveNumber.round(0)

    def addSpectrumToData(self, x, y, spectrum):
        self.data.append(Pixel(x, y, spectrum))

    def deleteAllSpectrumInData(self):
        self.data = []

    def returnSpectrum(self, x, y, data):
        spectrum = None
        for item in data:
            if item.x == x:
                if item.y == y:
                    spectrum = item.spectrum

        return spectrum

    def returnWidthImage(self, data):
        width = -1
        for item in data:
            if item.x > width:
                width = item.x

        return width + 1

    def returnHeightImage(self, data):
        height = -1
        for item in data:
            if item.y > height:
                height = item.y

        return height + 1

    def returnSpectrumLen(self, data): # Maximum spectral point
        try:
            return len(data[0].spectrum)

        except:
            return None

    def returnSpectrumRange(self, wavelength): # cherchef min et max avant
        try:
            return round(abs(wavelength[-1] - wavelength[0]))
        except:
            return None

    def dataToMatrix(self, data):
        try:
            width = self.returnWidthImage(data)
            height = self.returnHeightImage(data)
            spectrumLen = self.returnSpectrumLen(data)
            matrixData = np.zeros((height, width, spectrumLen))

            for item in data:
                matrixData[item.y, item.x, :] = np.array(item.spectrum)

            return matrixData
        except:
            return None

    def dataToRGB(self, data, colorValues, globalMaximum=True): # color value /1 rel
        try:
            width = self.returnWidthImage(data)
            height = self.returnHeightImage(data)
            spectrumLen = self.returnSpectrumLen(data)

            lowRed = round(colorValues[0] / 255 * spectrumLen)
            highRed = round(colorValues[1] / 255 * spectrumLen)
            lowGreen = round(colorValues[2] / 255 * spectrumLen)
            highGreen = round(colorValues[3] / 255 * spectrumLen)
            lowBlue = round(colorValues[4] / 255 * spectrumLen)
            highBlue = round(colorValues[5] / 255 * spectrumLen)

            matrixRGB = np.zeros((height, width, 3))
            matrix = self.dataToMatrix(data)

            matrixRGB[:, :, 0] = matrix[:, :, lowRed:highRed].sum(axis=2)
            matrixRGB[:, :, 1] = matrix[:, :, lowGreen:highGreen].sum(axis=2)
            matrixRGB[:, :, 2] = matrix[:, :, lowBlue:highBlue].sum(axis=2)

            if globalMaximum:
                matrixRGB = (matrixRGB / np.max(matrixRGB)) * 255

            else:
                maxima = matrixRGB.max(axis=2)
                maxima = np.dstack((maxima,) * 3)
                np.seterr(divide='ignore', invalid='ignore')
                matrixRGB /= maxima
                matrixRGB[np.isnan(matrixRGB)] = 0
                matrixRGB *= 255

            matrixRGB = matrixRGB.round(0)

            return matrixRGB
        except:
            return None
