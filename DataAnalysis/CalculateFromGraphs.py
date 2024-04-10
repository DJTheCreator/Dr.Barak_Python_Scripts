import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def createArrayFromDataframe(dataframe, collumnName):
    tempArray = []
    for i in dataframe.iterrows():
        tempArray.append(dataframe.loc[i[0], collumnName])
    return tempArray


def calculateSlope(xfunction, yfunction, x1, x2):
    return (yfunction[x2] - yfunction[x1]) / (xfunction[x2] - xfunction[x1])


def findValueInDataframe(dataframe, collumnName, soughtValue):
    array = createArrayFromDataframe(dataframe, collumnName)
    for i in range(len(array)):
        if soughtValue == round(array[i], -2):
            return i + 2


zCubes = pd.read_excel('MedianExcelFiles/BMF_Cube_One_Median.xlsx')
yCubes = pd.read_excel('MedianExcelFiles/BMF_Cube_Two_Median.xlsx')
xCubes = pd.read_excel('MedianExcelFiles/BMF_Cube_Three_Median.xlsx')


def runSlopeCalculations():
    zCubeSlope = calculateSlope(createArrayFromDataframe(zCubes, 'Strain'),
                                createArrayFromDataframe(zCubes, 'Median Stress'),
                                findValueInDataframe(zCubes, 'Strain', 40000),
                                findValueInDataframe(zCubes, 'Strain', 55000))
    yCubeSlope = calculateSlope(createArrayFromDataframe(yCubes, 'Strain'),
                                createArrayFromDataframe(yCubes, 'Median Stress'),
                                findValueInDataframe(yCubes, 'Strain', 40000),
                                findValueInDataframe(yCubes, 'Strain', 55000))
    xCubeSlope = calculateSlope(createArrayFromDataframe(xCubes, 'Strain'),
                                createArrayFromDataframe(xCubes, 'Median Stress'),
                                findValueInDataframe(xCubes, 'Strain', 40000),
                                findValueInDataframe(xCubes, 'Strain', 55000))
    print("Z: " + str(zCubeSlope))
    print("Y: " + str(yCubeSlope))
    print("X: " + str(xCubeSlope))

runSlopeCalculations()
#print(np.trapz(y=createArrayFromDataframe(zCubes, 'Median Stress'), x=createArrayFromDataframe(zCubes, 'Strain')))
