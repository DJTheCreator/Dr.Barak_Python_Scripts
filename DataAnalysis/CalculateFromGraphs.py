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


settingsDict = {'1': 'Cube_',
                '2': 'Beam_',
                '3': '3DP_',
                '4': 'BMF_'}
settings = [input("Compression(1) or Tension(2): "), input("3DP(3) or BMF(4): ")]
filepath = "MedianExcelFiles/" + settingsDict[settings[1]] + settingsDict[settings[0]]
if settings[1] == '4':
    key = ['One', 'Two', 'Three']
else:
    key = ['Z', 'Y', 'X']

zCubes = pd.read_excel(filepath + key[0] + '_Median.xlsx')
yCubes = pd.read_excel('MedianExcelFiles/BMF_Cube_Two_Median.xlsx')
xCubes = pd.read_excel('MedianExcelFiles/BMF_Cube_Three_Median.xlsx')


def runSlopeCalculations(low, high):
    zCubeSlope = calculateSlope(createArrayFromDataframe(zCubes, 'Strain'),
                                createArrayFromDataframe(zCubes, 'Median Stress'),
                                findValueInDataframe(zCubes, 'Strain', low),
                                findValueInDataframe(zCubes, 'Strain', high))
    yCubeSlope = calculateSlope(createArrayFromDataframe(yCubes, 'Strain'),
                                createArrayFromDataframe(yCubes, 'Median Stress'),
                                findValueInDataframe(yCubes, 'Strain', low),
                                findValueInDataframe(yCubes, 'Strain', high))
    xCubeSlope = calculateSlope(createArrayFromDataframe(xCubes, 'Strain'),
                                createArrayFromDataframe(xCubes, 'Median Stress'),
                                findValueInDataframe(xCubes, 'Strain', low),
                                findValueInDataframe(xCubes, 'Strain', high))
    slopes = [zCubeSlope, yCubeSlope, xCubeSlope]
    return slopes


slope_list = runSlopeCalculations(30000, 60000)
print(slope_list)
