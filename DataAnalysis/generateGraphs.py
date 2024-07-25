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
                '4': 'BMF/'}
settings = [input("Compression(1) or Tension(2): "), input("3DP(3) or BMF(4): ")]
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
    return 0.5 * (x2 - x1) * stress


def findMedianTotalArea(dataframeArray):
    strainArray = createArrayFromDataframes(dataframeArray, 'Strain')
    stressArray = createArrayFromDataframes(dataframeArray, 'Stress')
    areasList = []
    for i in range(len(stressArray)):
        area = 0
        previousValue = 0
        for j in range(len(stressArray[i])):
            if j != 0:
                area += calculateArea(previousValue, stressArray[i][j], stressArray[i][j] + stressArray[i][j - 1])
                previousValue = stressArray[i][j]
            else:
                area += 0
        areasList.append(area)
    return median(areasList)


# print("median total energy \n proximal-distal: " + str(findMedianTotalArea(zCubeSheets)))
# print("medial-lateral: " + str(findMedianTotalArea(xCubeSheets)))
# print("cranial-caudal: " + str(findMedianTotalArea(yCubeSheets)))

# print("Ultimate Z Strength (MPa): " + str(findUltimateStrength(zCubeSheets, 'Stress')))
# print("Ultimate Y Strength (MPa): " + str(findUltimateStrength(yCubeSheets, 'Stress')))
# print("Ultimate X Strength (MPa): " + str(findUltimateStrength(xCubeSheets, 'Stress')))
# input("Stop here")


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

medianZCubesStress = createMedianArray(zCubeSheets, 'Stress', 1)
medianZCubesStrain = []
for value in findSmallestArray(strainZ):
    medianZCubesStrain.append(value * 1000000)

strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
stressY = createArrayFromDataframes(yCubeSheets, 'Stress')

medianYCubesStress = createMedianArray(yCubeSheets, 'Stress', 1)
medianYCubesStrain = []
for value in findSmallestArray(strainY):
    medianYCubesStrain.append(value * 1000000)

strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
stressX = createArrayFromDataframes(xCubeSheets, 'Stress')

medianXCubesStress = createMedianArray(xCubeSheets, 'Stress', 1)
medianXCubesStrain = []
for value in findSmallestArray(strainX):
    medianXCubesStrain.append(value * 1000000)

# consolidatedStrainZ = consolidateArray(strainZ)
# consolidatedStressZ = consolidateArray(stressZ)
#
# consolidatedStrainY = consolidateArray(strainY)
# consolidatedStressY = consolidateArray(stressY)
#
# consolidatedStrainX = consolidateArray(strainX)
# consolidatedStressX = consolidateArray(stressX)
#
# # noinspection PyTypeChecker
# plt.scatter(consolidatedStrainZ, consolidatedStressZ, s=2, c='blue')
# # noinspection PyTypeChecker
# plt.scatter(consolidatedStrainY, consolidatedStressY, s=2, c='red')
# # noinspection PyTypeChecker
# plt.scatter(consolidatedStrainX, consolidatedStressX, s=2, c='green')

medianSettingsDict = {
    'ExcelFiles/Compression/': '_Cube_',
    'ExcelFiles/Tension/': '_Beam_'
}

savepath = ('MedianExcelFiles/' + settingsDict[settings[1]][:-1]
            + medianSettingsDict[settingsDict[settings[0]]])

z_ci = 2.576 * std(medianZCubesStress) / math.sqrt(len(medianZCubesStress))
plt.fill_between(medianZCubesStrain, (medianZCubesStress - z_ci), (medianZCubesStress + z_ci), color='orange', alpha=0.4)
y_ci = 2.576 * std(medianYCubesStress) / math.sqrt(len(medianYCubesStress))
plt.fill_between(medianYCubesStrain, (medianYCubesStress - y_ci), (medianYCubesStress + y_ci), color='blue', alpha=0.4)
x_ci = 2.576 * std(medianXCubesStress) / math.sqrt(len(medianXCubesStress))
plt.fill_between(medianXCubesStrain, (medianXCubesStress - x_ci), (medianXCubesStress + x_ci), color='purple', alpha=0.4)

# noinspection PyTypeChecker
plt.scatter(medianZCubesStrain, medianZCubesStress, s=.3, c='blue')
zCubeMedian_dict = {'Strain': medianZCubesStrain, 'Median Stress': medianZCubesStress}
zCubeDataframe = pd.DataFrame(data=zCubeMedian_dict)
# zCubeDataframe.to_excel(savepath + key[0] + '_Median.xlsx')
# noinspection PyTypeChecker
plt.scatter(medianYCubesStrain, medianYCubesStress, s=.3, c='red')
yCubeMedian_dict = {'Strain': medianYCubesStrain, 'Median Stress': medianYCubesStress}
yCubeDataframe = pd.DataFrame(data=yCubeMedian_dict)
# yCubeDataframe.to_excel(savepath + key[1] + '_Median.xlsx')
# noinspection PyTypeChecker
plt.scatter(medianXCubesStrain, medianXCubesStress, s=.3, c='green')
xCubeMedian_dict = {'Strain': medianXCubesStrain, 'Median Stress': medianXCubesStress}
xCubeDataframe = pd.DataFrame(data=xCubeMedian_dict)
# xCubeDataframe.to_excel(savepath + key[2] + '_Median.xlsx')

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
    plt.title('Stress vs Strain on median of each \n 9mm\u00B3 3DP Form 3 Cubes (All Orientations)')
plt.show()
# plt.savefig('3DPCubesMedian')

input()
