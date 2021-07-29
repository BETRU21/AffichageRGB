import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.HyperSpectralImage import HyperSpectralImage




class control():
    def __init__(self):
        pass


    def giveRangeInfo(minWaveLength, maxWaveLength, rangeLen):
        pass
        #Window().set_range_to_wave(minWaveLength, maxWaveLength, rangeLen)

    def run(self, path):
        HSI = HyperSpectralImage()



