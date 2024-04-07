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


bmf_mode = False  # Developer toggle for Formlabs cubes (False) or BMF cubes (True)

if bmf_mode:
    zCubeSheets = createArrayFromFiles('BMFExcelFiles/', 'One')
    yCubeSheets = createArrayFromFiles('BMFExcelFiles/', 'Two')
    xCubeSheets = createArrayFromFiles('BMFExcelFiles/', 'Three')
else:
    zCubeSheets = createArrayFromFiles('FormlabsExcelFiles/', 'Z')
    yCubeSheets = createArrayFromFiles('FormlabsExcelFiles/', 'Y')
    xCubeSheets = createArrayFromFiles('FormlabsExcelFiles/', 'X')

def findSmallestArray(array):
    smallestArray = array[0]
    for i in range(len(array)):
        if len(array[i]) < len(smallestArray):
            smallestArray = array[i]
    return smallestArray


def createMedianArray(dataframeArray, collumnName, scaleFactor=1):
    array = createArrayFromDataframes(dataframeArray, collumnName)
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

medianZCubesStress = createMedianArray(zCubeSheets, 'Stress')
medianZCubesStrain = []
for value in findSmallestArray(strainZ):
    medianZCubesStrain.append(value * 1000000)

strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
stressY = createArrayFromDataframes(yCubeSheets, 'Stress')

medianYCubesStress = createMedianArray(yCubeSheets, 'Stress')
medianYCubesStrain = []
for value in findSmallestArray(strainY):
    medianYCubesStrain.append(value * 1000000)

strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
stressX = createArrayFromDataframes(xCubeSheets, 'Stress')

medianXCubesStress = createMedianArray(xCubeSheets, 'Stress')
medianXCubesStrain = []
for value in findSmallestArray(strainX):
    medianXCubesStrain.append(value * 1000000)

consolidatedStrainZ = consolidateArray(strainZ)
consolidatedStressZ = consolidateArray(stressZ)

consolidatedStrainY = consolidateArray(strainY)
consolidatedStressY = consolidateArray(stressY)

consolidatedStrainX = consolidateArray(strainX)
consolidatedStressX = consolidateArray(stressX)

# noinspection PyTypeChecker
plt.scatter(consolidatedStrainZ, consolidatedStressZ, s=2, c='blue')
# noinspection PyTypeChecker
plt.scatter(consolidatedStrainY, consolidatedStressY, s=2, c='red')
# noinspection PyTypeChecker
plt.scatter(consolidatedStrainX, consolidatedStressX, s=2, c='green')

# # noinspection PyTypeChecker
# plt.scatter(medianZCubesStrain, medianZCubesStress, s=2, c='blue')
# zCubeMedian_dict = {'Strain': medianZCubesStrain, 'Median Stress': medianZCubesStress}
# zCubeDataframe = pd.DataFrame(data=zCubeMedian_dict)
# zCubeDataframe.to_excel('MedianExcelFiles/3DP_Z_Cube_Median.xlsx')
# # noinspection PyTypeChecker
# plt.scatter(medianYCubesStrain, medianYCubesStress, s=2, c='red')
# yCubeMedian_dict = {'Strain': medianYCubesStrain, 'Median Stress': medianYCubesStress}
# yCubeDataframe = pd.DataFrame(data=yCubeMedian_dict)
# yCubeDataframe.to_excel('MedianExcelFiles/3DP_Y_Cube_Median.xlsx')
# # noinspection PyTypeChecker
# plt.scatter(medianXCubesStrain, medianXCubesStress, s=2, c='green')
# xCubeMedian_dict = {'Strain': medianXCubesStrain, 'Median Stress': medianXCubesStress}
# xCubeDataframe = pd.DataFrame(data=xCubeMedian_dict)
# xCubeDataframe.to_excel('MedianExcelFiles/3DP_X_Cube_Median.xlsx')

ax = plt.subplot()

ZCube = mpatches.Patch(color='blue', label='Z Cubes')
YCube = mpatches.Patch(color='red', label='Y Cubes')
xCube = mpatches.Patch(color='green', label='X Cubes')
ax.legend(handles=[xCube, YCube, ZCube])

plt.xlabel('Microstrain (\u03BC\u03B5)')
plt.ylabel('Stress (MPa)')
# getTitle = input("Enter title (code for \u00B2 is \\u00B2): ")
getTitle = ''
if getTitle != '':
    plt.title(getTitle)
else:
    plt.title('Stress vs Strain of 30 \n 9mm\u00B3 3DP Formlabs Cubes (10 per orientation)')
plt.savefig('AllFormlabsCubes')
plt.show()
