import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.HyperSpectralImage import HyperSpectralImage

class AppControl():
    def __init__(self):
        print("hey")
        self.HSI = HyperSpectralImage()
        self.windowController = None

    def giveRangeInfo(minWaveLength, maxWaveLength, rangeLen):
        pass
        #Window().set_range_to_wave(minWaveLength, maxWaveLength, rangeLen)

    def run(self, path):
        pass

    def listNameOfFiles(self, directory: str, extension="csv") -> list:
        """Return a list of file in a directory."""
        foundFiles = []
        for file in os.listdir(directory):
            if fnmatch.fnmatch(file, f'*.{extension}'):
                foundFiles.append(file)
        return foundFiles

    def loadData(self, path):
        pass




