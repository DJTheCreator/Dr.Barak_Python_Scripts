import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import openpyxl
from numpy import median


def createArrayFromDataframes(dataframeArray, columnName):
    bigTempArray = []
    for dataframe in dataframeArray:
        tempArray = []
        for i in dataframe.iterrows():
            tempArray.append(dataframe.loc[i[0], columnName])
        bigTempArray.append(tempArray)
    return bigTempArray


selectedCols = [5, 6]


def createArrayFromFiles(location, keyword):
    tempArray = []
    for file in os.listdir(location + '/'):
        if keyword in file:
            # noinspection PyTypeChecker
            esheet = pd.read_excel(location + file, usecols=selectedCols, skiprows=3)
            tempArray.append(esheet)
    return tempArray


def consolidateArray(arrays):
    consolidatedArray = []
    for array in arrays:
        consolidatedArray += array
    return consolidatedArray


zCubeSheets = createArrayFromFiles('ExcelFiles/Tension/3DP/', 'Z')
yCubeSheets = createArrayFromFiles('ExcelFiles/Tension/3DP/', 'Y')
xCubeSheets = createArrayFromFiles('ExcelFiles/Tension/3DP/', 'X')



def findSmallestArray(array):
    smallestArray = array[0]
    for i in range(len(array)):
        if len(array[i]) < len(smallestArray):
            smallestArray = array[i]
    return smallestArray


def createMedianArray(dataframeArray, columnName, scaleFactor=1):
    array = createArrayFromDataframes(dataframeArray, columnName)
    newArray = []
    smallestArray = findSmallestArray(array)
    for i in range(len(smallestArray)):
        valueArray = []
        for sheet in array:
            valueArray.append(sheet[i] * scaleFactor)
        newArray.append(median(valueArray))
    return newArray


strainZ = createArrayFromDataframes(zCubeSheets, 'Strain')
stressZ = createArrayFromDataframes(zCubeSheets, 'Stress')

medianZCubesStress = createMedianArray(zCubeSheets, 'Stress', 1000000)
medianZCubesStrain = []
for value in findSmallestArray(strainZ):
    medianZCubesStrain.append(value * 1000000)

strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
stressY = createArrayFromDataframes(yCubeSheets, 'Stress')