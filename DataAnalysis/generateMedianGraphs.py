import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from numpy import median


def createArrayFromDataframes(dataframeArray, collumnName):
    bigTempArray = []
    for dataframe in dataframeArray:
        tempArray = []
        for i in dataframe.iterrows():
            tempArray.append(dataframe.loc[i[0], collumnName])
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


zCubeSheets = createArrayFromFiles('ExcelFiles/', 'One')

def findSmallestArray(array):
    smallestArray = array[0]
    for i in range(len(array)):
        if(len(array[i]) < len(smallestArray)):
            smallestArray = array[i]
    return smallestArray


def createMedianArray(dataframArray, collumnName):
    array = createArrayFromDataframes(dataframArray, collumnName)
    newArray = []
    smallestArray = findSmallestArray(array)
    for i in range(len(smallestArray)):
        valueArray = []
        for sheet in array:
            valueArray.append(sheet[i])
        newArray.append(median(valueArray))
    return newArray


medianZCubesStress = createMedianArray(zCubeSheets, 'Stress')
zCubesStrainArray = []
for i in range(len(findSmallestArray(zCubeSheets))):
    zCubesStrainArray.append(i)

# noinspection PyTypeChecker
plt.scatter(zCubesStrainArray, medianZCubesStress, s=2, c='blue')
plt.show()