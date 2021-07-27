import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch

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

path = "C:/Users/Benjamin/Desktop/RawData"
# donnees_tot_x = []
# donnees_tot_y = []
nb = len(listNameOfFiles(path))
print("nombre de fichier :", nb)

sortedPaths = (listNameOfFiles(path))
for i in range(nb):
    if i == 0:
        pass
    elif i == 1:
        pass
    else:
        nom = sortedPaths[i]
        print(nom)
        # Nom du fichier à importer
        fich = open(path + '/' + nom, "r")
        test_str = list(fich)[14:]
        fich.close()
        x = []
        y = []
        tot = []
        # Nettoyer les informations
        for j in test_str:
            # elem_str = j.replace(",", ".").replace("\n", "").replace("\t", ",")
            elem_str = j.replace(";",",").replace("\n", "").replace("\t", ",")
            elem = elem_str.split(",")
            x.append(float(elem[0]))
            y.append(float(elem[1]))
        tot.append(x)
print(i)
