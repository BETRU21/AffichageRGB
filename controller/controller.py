import numpy as np
from gui.Window import Window




class control():
    def __init__(self):
        self.matrixRGB = []
    
    def create_matrix_rgb(self, height, width):
        self.matrixRGB = np.zeros((height, width, 3))


    def matrixRGB_replace(self, matrix, dataLen, rangeLen):
        lowRed = int(((self.sb_lowRed.value() - self.minWaveLength) / rangeLen) * dataLen)
        highRed = int(((self.sb_highRed.value() - self.minWaveLength) / rangeLen) * dataLen)
        lowGreen = int(((self.sb_lowGreen.value() - self.minWaveLength) / rangeLen) * dataLen)
        highGreen = int(((self.sb_highGreen.value() - self.minWaveLength) / rangeLen) * dataLen)
        lowBlue = int(((self.sb_lowBlue.value() - self.minWaveLength) / rangeLen) * dataLen)
        highBlue = int(((self.sb_highBlue.value() - self.minWaveLength) / rangeLen) * dataLen)

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

    def giveRangeInfo(minWaveLength, maxWaveLength, rangeLen):
        pass
        #Window().set_range_to_wave(minWaveLength, maxWaveLength, rangeLen)

    def run(self, path):
        Model().buildMatrix(path)



