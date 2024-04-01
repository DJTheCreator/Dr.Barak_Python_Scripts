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

medianYCubesStress = createMedianArray(yCubeSheets, 'Stress', 1000000)
medianYCubesStrain = []
for value in findSmallestArray(strainY):
    medianYCubesStrain.append(value * 1000000)

strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
stressX = createArrayFromDataframes(xCubeSheets, 'Stress')

medianXCubesStress = createMedianArray(xCubeSheets, 'Stress', 1000000)
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

# noinspection PyTypeChecker
plt.scatter(medianZCubesStrain, medianZCubesStress, s=2, c='blue')
zCubeMedian_dict = {'Strain': medianZCubesStrain, 'Median Stress': medianZCubesStress}
zCubeDataframe = pd.DataFrame(data=zCubeMedian_dict)
zCubeDataframe.to_excel('MedianExcelFiles/3DP_Beam_Z_Median.xlsx')
# noinspection PyTypeChecker
plt.scatter(medianYCubesStrain, medianYCubesStress, s=2, c='red')
yCubeMedian_dict = {'Strain': medianYCubesStrain, 'Median Stress': medianYCubesStress}
yCubeDataframe = pd.DataFrame(data=yCubeMedian_dict)
yCubeDataframe.to_excel('MedianExcelFiles/3DP_Beam_Y_Median.xlsx')
# noinspection PyTypeChecker
plt.scatter(medianXCubesStrain, medianXCubesStress, s=2, c='green')
xCubeMedian_dict = {'Strain': medianXCubesStrain, 'Median Stress': medianXCubesStress}
xCubeDataframe = pd.DataFrame(data=xCubeMedian_dict)
xCubeDataframe.to_excel('MedianExcelFiles/3DP_Beam_X_Median.xlsx')

ax = plt.subplot()

ZCube = mpatches.Patch(color='blue', label='Z Cubes')
YCube = mpatches.Patch(color='red', label='Y Cubes')
xCube = mpatches.Patch(color='green', label='X Cubes')
ax.legend(handles=[xCube, YCube, ZCube])

plt.xlabel('Microstrain (\u03BC\u03B5)')
plt.ylabel('Stress (Pa)')
# getTitle = input("Enter title (code for \u00B2 is \\u00B2): ")
getTitle = ''
if getTitle != '':
    plt.title(getTitle)
else:
    plt.title('Stress vs Strain on median of each \n 3mm\u00B3 BMF Cubes (All Orientations)')
plt.savefig('CombinedBeamsMedian')
plt.show()
