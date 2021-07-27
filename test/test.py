import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import time
import re
import numpy as np

path = "C:/Users/Benjamin/Desktop/RawData"

def listNameOfFiles(directory: str, extension="csv") -> list:
    foundFiles = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, f'*.{extension}'):
            foundFiles.append(file)
    return foundFiles



nb = len(listNameOfFiles(path))
print("nombre de fichier :", nb)

sortedPaths = (listNameOfFiles(path))
val1Max = 0
val2Max = 0
dataLen = 0

for i in range(nb):
    nom = sortedPaths[i]
    matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", nom)
    if matchObj:
        val1 = int(matchObj.group(1))
        val2 = int(matchObj.group(2))
        # Nom du fichier à importer
        fich = open(path + '/' + nom, "r")
        test_str = list(fich)[14:]
        fich.close()
        x = []
        if val1 > val1Max:
            val1Max = val1
        if val2 > val2Max:
            val2Max = val2
        # Nettoyer les informations
        if dataLen == 0:
            for j in test_str:
                elem_str = j.replace("\n", "")
                elem = elem_str.split(",")
                x.append(float(elem[1]))
            dataLen = len(x)
        else:
            pass


matrixRawData = np.zeros((val2Max+1, val1Max+1, dataLen))

for i in range(nb):
    nom = sortedPaths[i]
    matchObj = re.match("\\D*?(\\d+)\\D*?(\\d+)\\D*?", nom)
    if matchObj:
        val1 = int(matchObj.group(1))
        val2 = int(matchObj.group(2))
        # Nom du fichier à importer
        fich = open(path + '/' + nom, "r")
        test_str = list(fich)[14:]
        fich.close()
        x = []
        y = []
        # Nettoyer les informations
        for j in test_str:
            elem_str = j.replace("\n", "")
            elem = elem_str.split(",")
            y.append(float(elem[1]))
        matrixRawData[val1, val2, :] = y
print(matrixRawData)
