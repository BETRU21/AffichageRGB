import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import time
import re
import numpy as np

path = "C:/Users/Benjamin/Desktop/RawData"

class Model():
    def __init__(self):
        self.matrixData = None
        self.dataLen = 0
        self.width = 0
        self.height = 0


    def listNameOfFiles(self, directory: str, extension="csv") -> list:
        """Return a list of file in a directory."""
        foundFiles = []
        for file in os.listdir(directory):
            if fnmatch.fnmatch(file, f'*.{extension}'):
                foundFiles.append(file)
        return foundFiles

    def buildMatrix(self, path):
        """Build a matrix with the file of each pixel."""
        nb = len(self.listNameOfFiles(path))
        sortedPaths = (self.listNameOfFiles(path))


        for i, name in enumerate(sortedPaths):

            # Find the position and verify if it's the maximum value in each direction
            matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", name)
            if matchObj:
                posX = int(matchObj.group(1))
                posY = int(matchObj.group(2))
                if posX > self.width:
                    self.width = posX
                if posY > self.height:
                    self.height = posY

                fich = open(path + '/' + name, "r")
                test_str = list(fich)[14:]
                fich.close()
                x = []
                # Verify and set the dataLen (One time)
                if self.dataLen == 0:
                    for j in test_str:
                        elem_str = j.replace("\n", "")
                        elem = elem_str.split(",")
                        x.append(float(elem[1]))
                    self.dataLen = len(x)
                else:
                    pass

        # Create the matrixData
        self.width += 1
        self.height += 1
        self.matrixData = np.zeros((self.height, self.width, self.dataLen))

        # Put each pixel in the data at the good position
        for i, name in enumerate(sortedPaths):
            # Find the position
            matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", name)
            if matchObj:
                posX = int(matchObj.group(1))
                posY = int(matchObj.group(2))

                # Open file and put the data in the matrix
                fich = open(path + '/' + name, "r")
                test_str = list(fich)[14:]
                fich.close()
                y = []
                # clean and split the data
                for j in test_str:
                    elem_str = j.replace("\n", "")
                    elem = elem_str.split(",")
                    y.append(float(elem[1]))
                self.matrixData[posY, posX, :] = y

        print(self.matrixData)


if __name__ == "__main__":
    Model().buildMatrix(path)
