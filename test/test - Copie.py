import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import time
import re

dir_name = "C:/Users/Benjamin/Desktop/RawData"

def listNameOfFiles(directory: str, extension="csv") -> list:
    foundFiles = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, f'*.{extension}'):
            foundFiles.append(file)
    return foundFiles

def getFilePaths(directory: str, fileNames: list) -> list:
    filesWithFullPath = []
    for fileName in fileNames:
        filesWithFullPath.append(directory+"/"+fileName)
    return filesWithFullPath



nb = len(listNameOfFiles(dir_name))
print("nombre de fichier :", nb)

sortedPaths = (listNameOfFiles(dir_name))
#print(sortedPaths)

# valueSTR = sortedPaths[0]
# valueMin = valueSTR.find("_x")
# valueMax = valueSTR.find("_y")
# valueEnd = valueSTR.find(".csv")
# positionX = valueSTR[valueMin+2:valueMax]
# positionY = valueSTR[valueMax+2:valueEnd]


# print(positionX)
# print(positionY)

matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", sortedPaths[9])
if matchObj:
    val1 = int(matchObj.group(1))
    val2 = int(matchObj.group(2))
    print(val1, val2)
