import numpy as np




class controller():
    def __init__(self):
        super().__init__(parent)
    
    def create_matrix_rgb(self):
        self.matrixRGB = np.zeros((self.height, self.width, 3))


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

    def run(self):
        pass

if __name__ == "__main__":
    pass


