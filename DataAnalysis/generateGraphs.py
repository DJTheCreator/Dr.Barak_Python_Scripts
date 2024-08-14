import math

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import openpyxl
from numpy import median, std, mean


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


settingsDict = {'1': 'ExcelFiles/Compression/',
                '2': 'ExcelFiles/Tension/',
                '3': '3DP/',
                '4': 'BMF/',
                '5': 'Median',
                '6': 'Combined'}
settings = [input("Compression(1) or Tension(2): "), input("3DP(3) or BMF(4): "),
            settingsDict[input("Median(5) or Combined(6): ")]]
filepath = settingsDict[settings[0]] + settingsDict[settings[1]]
print("Please wait while the graph generates...")
if settings[1] == '4':
    key = ['One', 'Two', 'Three']
else:
    key = ['Z', 'Y', 'X']

zCubeSheets = createArrayFromFiles(filepath, key[0])
print("zCubeSheets generated...")
yCubeSheets = createArrayFromFiles(filepath, key[1])
print("yCubeSheets generated...")
xCubeSheets = createArrayFromFiles(filepath, key[2])
print("xCubeSheets generated...")


def findUltimateStrength(dataframeArray, columnName):
    array = createArrayFromDataframes(dataframeArray, columnName)
    maxValueList = []
    for cube in array:
        maxValue = cube[0]
        for _value in cube:
            if _value > maxValue:
                maxValue = _value
        maxValueList.append(maxValue)
    return median(maxValueList)


def calculateArea(x1, x2, stress):
    return 0.5 * abs(x2 - x1) * stress


def findMedianTotalArea(dataframeArray):
    strainArray = createArrayFromDataframes(dataframeArray, 'Strain')
    stressArray = createArrayFromDataframes(dataframeArray, 'Stress')
    areasList = []
    for i in range(len(stressArray)):
        areas = []
        previousValue = 0
        for j in range(len(stressArray[i])):
            if j != 0:
                _area = calculateArea(previousValue, strainArray[i][j], stressArray[i][j] + stressArray[i][j - 1])
                areas.append(_area)
                # print("x1: " + str(previousValue) + " | x2: " + str(strainArray[i][j]) + " | Area: " + str(_area))
                previousValue = strainArray[i][j]
            else:
                areas.append(0)
        # print("areas: " + str(areas))
        areasList.append(sum(areas))
    return median(areasList)


# print("median total energy \n proximal-distal: " + str(findMedianTotalArea(zCubeSheets)))
# print(" cranial-caudal: " + str(findMedianTotalArea(yCubeSheets)))
# print(" medial-lateral: " + str(findMedianTotalArea(xCubeSheets)))
#
# print("Ultimate Z Strength (MPa): " + str(findUltimateStrength(zCubeSheets, 'Stress')))
# print("Ultimate Y Strength (MPa): " + str(findUltimateStrength(yCubeSheets, 'Stress')))
# print("Ultimate X Strength (MPa): " + str(findUltimateStrength(xCubeSheets, 'Stress')))
# input("Stop here")
# print("Continuing...")


def findSmallestArray(array):
    smallestArray = array[0]
    for i in range(len(array)):
        if len(array[i]) < len(smallestArray):
            smallestArray = array[i]
    return smallestArray


def createMedianArray(dataframeArray, columnName, medianStrainArray, scaleFactor=1):
    array = createArrayFromDataframes(dataframeArray, columnName)
    newArray = []
    for i in range(len(medianStrainArray)):
        valueArray = []
        for sheet in array:
            if i < len(sheet):
                valueArray.append(sheet[i] * scaleFactor)
        newArray.append(median(valueArray))
    return newArray


def findMedianMaxStrain(dataframeArray, columnName):
    strain_arrays = createArrayFromDataframes(dataframeArray, columnName)
    max_strain_array = []
    for array in strain_arrays:
        max_strain_array.append(max(array))
    median_max_strain = median(max_strain_array) * 1000000
    difference = 1000000
    closest_array = []
    for array in strain_arrays:
        if abs(median_max_strain - max(array)) < difference:
            difference = abs(median_max_strain - max(array))
            closest_array = array
    return closest_array


if settings[2] == 'Combined':
    strainZ = createArrayFromDataframes(zCubeSheets, 'Strain')
    stressZ = createArrayFromDataframes(zCubeSheets, 'Stress')
    print("zArrays generated")

    strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
    stressY = createArrayFromDataframes(yCubeSheets, 'Stress')
    print("yArrays generated")

    strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
    stressX = createArrayFromDataframes(xCubeSheets, 'Stress')
    print("xArrays generated")

    consolidatedStrainZ = consolidateArray(strainZ)
    consolidatedStressZ = consolidateArray(stressZ)

    consolidatedStrainY = consolidateArray(strainY)
    consolidatedStressY = consolidateArray(stressY)

    consolidatedStrainX = consolidateArray(strainX)
    consolidatedStressX = consolidateArray(stressX)
    print("Consolidated Arrays")

    # noinspection PyTypeChecker
    plt.scatter(consolidatedStrainZ, consolidatedStressZ, s=2, c='blue')
    # noinspection PyTypeChecker
    plt.scatter(consolidatedStrainY, consolidatedStressY, s=2, c='red')
    # noinspection PyTypeChecker
    plt.scatter(consolidatedStrainX, consolidatedStressX, s=2, c='green')
    print("Scattered Arrays")
elif settings[2] == 'Median':
    medianZStrainArray = findMedianMaxStrain(zCubeSheets, 'Strain')
    medianZCubesStress = createMedianArray(zCubeSheets, 'Stress', medianZStrainArray, 1)
    medianZCubesStrain = createMedianArray(zCubeSheets, 'Strain', medianZStrainArray, 1000000)
    print("zArrays generated")

    medianYStrainArray = findMedianMaxStrain(yCubeSheets, 'Strain')
    medianYCubesStress = createMedianArray(yCubeSheets, 'Stress', medianYStrainArray, 1)
    medianYCubesStrain = createMedianArray(yCubeSheets, 'Strain', medianYStrainArray, 1000000)
    print("yArrays generated")

    medianXStrainArray = findMedianMaxStrain(xCubeSheets, 'Strain')
    medianXCubesStress = createMedianArray(xCubeSheets, 'Stress', medianXStrainArray, 1)
    medianXCubesStrain = createMedianArray(xCubeSheets, 'Strain', medianXStrainArray, 1000000)
    print("xArrays generated")

    medianSettingsDict = {
        'ExcelFiles/Compression/': '_Cube_',
        'ExcelFiles/Tension/': '_Beam_'
    }

    savepath = ('MedianExcelFiles/' + settingsDict[settings[1]][:-1]
                + medianSettingsDict[settingsDict[settings[0]]])

    z_ci = 2.576 * std(medianZCubesStress) / math.sqrt(len(medianZCubesStress))
    plt.fill_between(medianZCubesStrain, (medianZCubesStress - z_ci), (medianZCubesStress + z_ci), color='orange',
                     alpha=0.4)
    y_ci = 2.576 * std(medianYCubesStress) / math.sqrt(len(medianYCubesStress))
    plt.fill_between(medianYCubesStrain, (medianYCubesStress - y_ci), (medianYCubesStress + y_ci), color='blue',
                     alpha=0.4)
    x_ci = 2.576 * std(medianXCubesStress) / math.sqrt(len(medianXCubesStress))
    plt.fill_between(medianXCubesStrain, (medianXCubesStress - x_ci), (medianXCubesStress + x_ci), color='purple',
                     alpha=0.4)

    # noinspection PyTypeChecker
    plt.scatter(medianZCubesStrain, medianZCubesStress, s=.3, c='blue')
    zCubeMedian_dict = {'Strain': medianZCubesStrain, 'Median Stress': medianZCubesStress}
    zCubeDataframe = pd.DataFrame(data=zCubeMedian_dict)
    zCubeDataframe.to_excel(savepath + key[0] + '_Median.xlsx')
    # noinspection PyTypeChecker
    plt.scatter(medianYCubesStrain, medianYCubesStress, s=.3, c='red')
    yCubeMedian_dict = {'Strain': medianYCubesStrain, 'Median Stress': medianYCubesStress}
    yCubeDataframe = pd.DataFrame(data=yCubeMedian_dict)
    yCubeDataframe.to_excel(savepath + key[1] + '_Median.xlsx')
    # noinspection PyTypeChecker
    plt.scatter(medianXCubesStrain, medianXCubesStress, s=.3, c='green')
    xCubeMedian_dict = {'Strain': medianXCubesStrain, 'Median Stress': medianXCubesStress}
    xCubeDataframe = pd.DataFrame(data=xCubeMedian_dict)
    xCubeDataframe.to_excel(savepath + key[2] + '_Median.xlsx')

ax = plt.subplot()

ZCube = mpatches.Patch(color='blue', label='Distal-Proximal')
YCube = mpatches.Patch(color='red', label='Cranial-Caudal')
xCube = mpatches.Patch(color='green', label='Medial-Lateral')
ax.legend(handles=[xCube, YCube, ZCube])

plt.xlabel('Microstrain (\u03BC\u03B5)')
plt.ylabel('Stress (MPa)')
# getTitle = input("Enter title (code for \u00B2 is \\u00B2): ")
getTitle = ''
if getTitle != '':
    plt.title(getTitle)
else:
    plt.title('Stress vs Strain on median of each \n 9mm\u00B3 3DP Beams in Tension (All Orientations)')
plt.savefig('3DPBeamsMedian')
plt.show()

input()
