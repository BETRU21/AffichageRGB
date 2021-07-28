import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import time
import re
import numpy as np





class HyperSpectralImage:
    def __init__(self):
        self.data = []

    def addSpectrum(self, x, y, spectrum):
        self.data.append(((x, y), spectrum))

    def resetSpectrum(self, x, y, spectrum):
        self.data = []

    def returnWidthImage(self, data):
        width = 0
        for i, item in enumerate(data):
            if item[0][0] > width:
                width = item[0][0]
            else:
                pass

        return width + 1

    def returnHeightImage(self, data):
        height = 0
        for i, item in enumerate(data):
            if item[0][1] > height:
                height = item[0][1]
            else:
                pass

        return height + 1

    def returnSpectrumLen(self, data): # On s'en fout duquel c'est obligé d`être la même longueur
        try:
            return len(data[0][1])

        except Exception as e:
            print(f'ERROR : {e}')

    def dataToMatrix(self, data):
        width = returnWidth(data)
        height = returnHeight(data)
        spectrumLen = returnSpectrumLen(data)
        matrixData = np.zeros((height, width, spectrumLen))

        for i, item in enumerate(data):
            matrixData[item[0][1], item[0][0], :] = item[1]

        return matrixData

    def matrixToRGB(self, data):
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

        return matrixRGB


    

# path = "C:/Users/Benjamin/Desktop/RawData"

# class Model():
#     def __init__(self):
#         self.matrixData = None
#         self.dataLen = 0
#         self.width = 0
#         self.height = 0
#         self.rangeLen = 0
#         self.minWaveLength = None
#         self.maxWaveLength = None


#     def listNameOfFiles(self, directory: str, extension="csv") -> list:
#         """Return a list of file in a directory."""
#         foundFiles = []
#         for file in os.listdir(directory):
#             if fnmatch.fnmatch(file, f'*.{extension}'):
#                 foundFiles.append(file)
#         return foundFiles

#     def buildMatrix(self, path):
#         """Build a matrix with the file of each pixel."""
#         nb = len(self.listNameOfFiles(path))
#         sortedPaths = (self.listNameOfFiles(path))


#         for i, name in enumerate(sortedPaths):

#             # Find the position and verify if it's the maximum value in each direction
#             matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", name)
#             if matchObj:
#                 posX = int(matchObj.group(1))
#                 posY = int(matchObj.group(2))
#                 if posX > self.width:
#                     self.width = posX
#                 if posY > self.height:
#                     self.height = posY

#                 fich = open(path + '/' + name, "r")
#                 test_str = list(fich)[14:]
#                 fich.close()
#                 x = []
#                 # Verify and set the dataLen (One time)
#                 if self.dataLen == 0:
#                     for j in test_str:
#                         elem_str = j.replace("\n", "")
#                         elem = elem_str.split(",")
#                         x.append(float(elem[1]))
#                     self.dataLen = len(x)
#                     self.rangeLen = abs(x[-1] - x[0])
#                     self.minWaveLength = round(x[0])
#                     self.maxWaveLength = round(x[-1])
#                 else:
#                     pass

#         # Create the matrixData
#         self.width += 1
#         self.height += 1
#         self.matrixData = np.zeros((self.height, self.width, self.dataLen))
#         self.didGetMatrixInfo()

#         # Put each pixel in the data at the good position
#         for i, name in enumerate(sortedPaths):
#             # Find the position
#             matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", name)
#             if matchObj:
#                 posX = int(matchObj.group(1))
#                 posY = int(matchObj.group(2))

#                 # Open file and put the data in the matrix
#                 fich = open(path + '/' + name, "r")
#                 test_str = list(fich)[14:]
#                 fich.close()
#                 y = []
#                 # clean and split the data
#                 for j in test_str:
#                     elem_str = j.replace("\n", "")
#                     elem = elem_str.split(",")
#                     y.append(float(elem[1]))
#                 self.matrixData[posY, posX, :] = y
#         self.matrixFinished()
#         print(self.matrixData)

#     def matrixFinished(self):
#         control().create_matrix_rgb(self.height, self.width)
#         control().matrixRGB_replace(self.matrixData, self.dataLen, self.rangeLen)

#     def didGetMatrixInfo(self):
#         control().giveRangeInfo(self.minWaveLength, self.maxWaveLength, self.rangeLen)


# if __name__ == "__main__":
#     Model().buildMatrix(path)
