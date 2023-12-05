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


def consolidateArray(arrays):
    consolidatedArray = []
    for array in arrays:
        consolidatedArray += array
    return consolidatedArray


zCubeSheets = createArrayFromFiles('ExcelFiles/', 'One')
yCubeSheets = createArrayFromFiles('ExcelFiles/', 'Two')
xCubeSheets = createArrayFromFiles('ExcelFiles/', 'Three')


def findSmallestArray(array):
    smallestArray = array[0]
    for i in range(len(array)):
        if (len(array[i]) < len(smallestArray)):
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


strainZ = createArrayFromDataframes(zCubeSheets, 'Strain')
stressZ = createArrayFromDataframes(zCubeSheets, 'Stress')

medianZCubesStress = createMedianArray(zCubeSheets, 'Stress')
medianZCubesStrain = []
for value in findSmallestArray(strainZ):
    medianZCubesStrain.append(value)

strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
stressY = createArrayFromDataframes(yCubeSheets, 'Stress')

medianYCubesStress = createMedianArray(yCubeSheets, 'Stress')
medianYCubesStrain = []
for value in findSmallestArray(strainY):
    medianYCubesStrain.append(value)

strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
stressX = createArrayFromDataframes(xCubeSheets, 'Stress')

medianXCubesStress = createMedianArray(xCubeSheets, 'Stress')
medianXCubesStrain = []
for value in findSmallestArray(strainX):
    medianXCubesStrain.append(value)

# consolidatedStrainZ = consolidateArray(strainZ)
# consolidatedStressZ = consolidateArray(stressZ)
#
# consolidatedStrainY = consolidateArray(strainY)
# consolidatedStressY = consolidateArray(stressY)
#
# consolidatedStrainX = consolidateArray(strainX)
# consolidatedStressX = consolidateArray(stressX)

# noinspection PyTypeChecker
# plt.scatter(consolidatedStrainZ, consolidatedStressZ, s=2, c='blue')
# noinspection PyTypeChecker
# plt.scatter(consolidatedStrainY, consolidatedStressY, s=2, c='red')
# # noinspection PyTypeChecker
# plt.scatter(consolidatedStrainX, consolidatedStressX, s=2, c='green')

# noinspection PyTypeChecker
plt.scatter(medianZCubesStrain, medianZCubesStress, s=2, c='blue')
# noinspection PyTypeChecker
plt.scatter(medianYCubesStrain, medianYCubesStress, s=2, c='red')
# noinspection PyTypeChecker
plt.scatter(medianXCubesStrain, medianXCubesStress, s=2, c='green')

ax = plt.subplot()

ZCube = mpatches.Patch(color='blue', label='Z Cubes')
YCube = mpatches.Patch(color='red', label='Y Cubes')
xCube = mpatches.Patch(color='green', label='X Cubes')
ax.legend(handles=[xCube, YCube, ZCube])

plt.xlabel('Strain')
plt.ylabel('Stress (N/mm\u00B2)')
# getTitle = input("Enter title (code for \u00B2 is \\u00B2): ")
getTitle = ''
if getTitle != '':
    plt.title(getTitle)
else:
    plt.title('Stress vs Strain on median of each \n 3mm\u00B3 BMF Cubes (All Orientations)')
plt.savefig('CombinedCubesMedian')
plt.show()
