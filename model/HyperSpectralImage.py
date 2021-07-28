import numpy as np

class HyperSpectralImage:
    def __init__(self):
        self.data = []
        self.wavelength = []

    def addWavelength(self, wavelength):
        self.wavelength = np.array(wavelength)

    def deleteWavelength(self):
        self.wavelength = []

    def returnWaveNumber(self, laser):
        waveNumber = ((1 / laser) - (1 / self.wavelength)) * 10 ** 7
        return waveNumber.round(0)

    def addSpectrumToData(self, x, y, spectrum):
        self.data.append(((x, y), spectrum))

    def deleteAllSpectrumInData(self):
        self.data = []

    def deleteSpecificSpectrumInData(self, x, y):
        spectrumFound = False
        for i, item in enumerate(self.data):
            if item[0] == (x, y):
                del self.data[i]
                spectrumFound = True

        return spectrumFound

    def returnSpectrum(self, x, y, data):
        spectrum = None
        for item in data:
            if item[0] == (x, y):
                spectrum = item[1]

        return spectrum

    def returnWidthImage(self, data):
        width = -1
        for item in data:
            if item[0][0] > width:
                width = item[0][0]

        return width + 1

    def returnHeightImage(self, data):
        height = -1
        for item in data:
            if item[0][1] > height:
                height = item[0][1]

        return height + 1

    def returnSpectrumLen(self, data): # On s'en fout duquel c'est obligé d`être la même longueur
        try:
            return len(data[0][1])

        except:
            return None

    def returnSpectrumRange(self, data):
        return round(abs(data[0][1][0] - data[0][1][-1]))

    def dataToMatrix(self, data):
        width = returnWidthImage(data)
        height = returnHeightImage(data)
        spectrumLen = returnSpectrumLen(data)
        matrixData = np.zeros((height, width, spectrumLen))

        for item in data:
            matrixData[item[0][1], item[0][0], :] = np.array(item[1])

        return matrixData

    def matrixToRGB(self, data, globalMaximum=True):
        width = returnWidth(data)
        height = returnHeight(data)
        spectrumLen = returnSpectrumLen(data)

        lowRed = 0
        highRed = int(spectrumLen / 3)
        lowGreen = int(spectrumLen / 3)
        highGreen = int(spectrumLen * (2 / 3))
        lowBlue = int(spectrumLen * (2 / 3))
        highBlue = int(spectrumLen)

        matrixRGB = np.zeros((height, width, 3))
        matrix = dataToMatrix(data)

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

    def matrixToRgbButWith7Arguments(self, data, lowRed, highRed, lowGreen, highGreen, lowBlue, highBlue, globalMaximum=True):
        width = returnWidth(data)
        height = returnHeight(data)

        matrixRGB = np.zeros((height, width, 3))
        matrix = dataToMatrix(data)

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
