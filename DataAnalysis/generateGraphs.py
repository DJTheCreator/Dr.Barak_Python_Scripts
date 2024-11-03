import math

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import openpyxl
from numpy import median, std, mean

ax = plt.subplot()
handles = []
_plot_title = ''

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
            elif columnName == "Stress":
                valueArray.append(0)
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


def hatchBackground(_settings, x, y):
    high = [n + .15 for n in y]
    low = [n - .15 for n in y]
    if _settings[1] == '3':
        plt.fill_between(x, high, low, hatch='|', alpha=0)


def generateGraph():
    settingsDict = {'1': 'ExcelFiles/Compression/',
                    '2': 'ExcelFiles/Tension/',
                    '3': '3DP/',
                    '4': 'BMF/',
                    '5': 'Median',
                    '6': 'Combined'}
    settings = [input("Compression(1) or Tension(2): "), input("3DP(3) or BMF(4): "),
                settingsDict[input("Median(5) or Combined(6): ")],
                input("Which orientations? All that apply (pd, cc, ml): ")]
    filepath = settingsDict[settings[0]] + settingsDict[settings[1]]
    print("Please wait while the graph generates...")
    if settings[1] == '4':
        key = ['One', 'Two', 'Three']
    else:
        key = ['Z', 'Y', 'X']

    zCubeSheets = None
    yCubeSheets = None
    xCubeSheets = None
    if 'pd' in settings[3]:
        zCubeSheets = createArrayFromFiles(filepath, key[0])
        print("zCubeSheets generated...")
    if 'cc' in settings[3]:
        yCubeSheets = createArrayFromFiles(filepath, key[1])
        print("yCubeSheets generated...")
    if 'ml' in settings[3]:
        xCubeSheets = createArrayFromFiles(filepath, key[2])
        print("xCubeSheets generated...")

    # print("median total energy \n proximal-distal: " + str(findMedianTotalArea(zCubeSheets)))
    # print(" cranial-caudal: " + str(findMedianTotalArea(yCubeSheets)))
    # print(" medial-lateral: " + str(findMedianTotalArea(xCubeSheets)))
    #
    # print("Ultimate Z Strength (MPa): " + str(findUltimateStrength(zCubeSheets, 'Stress')))
    # print("Ultimate Y Strength (MPa): " + str(findUltimateStrength(yCubeSheets, 'Stress')))
    # print("Ultimate X Strength (MPa): " + str(findUltimateStrength(xCubeSheets, 'Stress')))
    # input("Stop here")
    # print("Continuing...")

    ZFillColor = ''
    YFillColor = ''
    XFillColor = ''
    ZDotColor = ''
    YDotColor = ''
    XDotColor = ''
    if settings[0] == '1':
        ZFillColor = 'royalblue'
        YFillColor = 'firebrick'
        XFillColor = 'limegreen'
        ZDotColor = 'mediumblue'
        YDotColor = 'darkred'
        XDotColor = 'darkgreen'
    elif settings[0] == '2':
        ZFillColor = 'powderblue'
        YFillColor = 'lightcoral'
        XFillColor = 'lightgreen'
        ZDotColor = 'deepskyblue'
        YDotColor = 'red'
        XDotColor = 'lawngreen'

    if settings[2] == 'Combined':
        if zCubeSheets:
            strainZ = createArrayFromDataframes(zCubeSheets, 'Strain')
            stressZ = createArrayFromDataframes(zCubeSheets, 'Stress')
            print("zArrays generated")
            consolidatedStrainZ = consolidateArray(strainZ)
            consolidatedStressZ = consolidateArray(stressZ)
            # noinspection PyTypeChecker
            plt.scatter(consolidatedStrainZ, consolidatedStressZ, s=2, c=ZDotColor)

        if yCubeSheets:
            strainY = createArrayFromDataframes(yCubeSheets, 'Strain')
            stressY = createArrayFromDataframes(yCubeSheets, 'Stress')
            print("yArrays generated")
            consolidatedStrainY = consolidateArray(strainY)
            consolidatedStressY = consolidateArray(stressY)
            # noinspection PyTypeChecker
            plt.scatter(consolidatedStrainY, consolidatedStressY, s=2, c=YDotColor)

        if xCubeSheets:
            strainX = createArrayFromDataframes(xCubeSheets, 'Strain')
            stressX = createArrayFromDataframes(xCubeSheets, 'Stress')
            print("xArrays generated")
            consolidatedStrainX = consolidateArray(strainX)
            consolidatedStressX = consolidateArray(stressX)
            # noinspection PyTypeChecker
            plt.scatter(consolidatedStrainX, consolidatedStressX, s=2, c=XDotColor)
    elif settings[2] == 'Median':
        medianSettingsDict = {
            'ExcelFiles/Compression/': '_Cube_',
            'ExcelFiles/Tension/': '_Beam_'
        }

        savepath = ('MedianExcelFiles/' + settingsDict[settings[1]][:-1]
                    + medianSettingsDict[settingsDict[settings[0]]])

        if zCubeSheets:
            medianZStrainArray = findMedianMaxStrain(zCubeSheets, 'Strain')
            medianZCubesStress = createMedianArray(zCubeSheets, 'Stress', medianZStrainArray, 1)
            medianZCubesStrain = createMedianArray(zCubeSheets, 'Strain', medianZStrainArray, 1000000)
            print("zArrays generated")
            z_ci = 2.576 * std(medianZCubesStress) / math.sqrt(len(medianZCubesStress))
            plt.fill_between(medianZCubesStrain, (medianZCubesStress - z_ci), (medianZCubesStress + z_ci),
                             color=ZFillColor,
                             alpha=0.4)
            # noinspection PyTypeChecker
            plt.scatter(medianZCubesStrain, medianZCubesStress, s=.3, c=ZDotColor)
            hatchBackground(settings, medianZCubesStrain, medianZCubesStress)

            zCubeMedian_dict = {'Strain': medianZCubesStrain, 'Median Stress': medianZCubesStress}
            zCubeDataframe = pd.DataFrame(data=zCubeMedian_dict)
            zCubeDataframe.to_excel(savepath + key[0] + '_Median.xlsx')

        if yCubeSheets:
            medianYStrainArray = findMedianMaxStrain(yCubeSheets, 'Strain')
            medianYCubesStress = createMedianArray(yCubeSheets, 'Stress', medianYStrainArray, 1)
            medianYCubesStrain = createMedianArray(yCubeSheets, 'Strain', medianYStrainArray, 1000000)
            print("yArrays generated")
            y_ci = 2.576 * std(medianYCubesStress) / math.sqrt(len(medianYCubesStress))
            plt.fill_between(medianYCubesStrain, (medianYCubesStress - y_ci), (medianYCubesStress + y_ci),
                             color=YFillColor,
                             alpha=0.4)
            # noinspection PyTypeChecker
            plt.scatter(medianYCubesStrain, medianYCubesStress, s=.3, c=YDotColor)
            hatchBackground(settings, medianYCubesStrain, medianYCubesStress)

            yCubeMedian_dict = {'Strain': medianYCubesStrain, 'Median Stress': medianYCubesStress}
            yCubeDataframe = pd.DataFrame(data=yCubeMedian_dict)
            yCubeDataframe.to_excel(savepath + key[1] + '_Median.xlsx')

        if xCubeSheets:
            medianXStrainArray = findMedianMaxStrain(xCubeSheets, 'Strain')
            medianXCubesStress = createMedianArray(xCubeSheets, 'Stress', medianXStrainArray, 1)
            medianXCubesStrain = createMedianArray(xCubeSheets, 'Strain', medianXStrainArray, 1000000)
            print("xArrays generated")
            x_ci = 2.576 * std(medianXCubesStress) / math.sqrt(len(medianXCubesStress))
            plt.fill_between(medianXCubesStrain, (medianXCubesStress - x_ci), (medianXCubesStress + x_ci),
                             color=XFillColor,
                             alpha=0.4)
            # noinspection PyTypeChecker
            plt.scatter(medianXCubesStrain, medianXCubesStress, s=.3, c=XDotColor)
            hatchBackground(settings, medianXCubesStrain, medianXCubesStress)

            xCubeMedian_dict = {'Strain': medianXCubesStrain, 'Median Stress': medianXCubesStress}
            xCubeDataframe = pd.DataFrame(data=xCubeMedian_dict)
            xCubeDataframe.to_excel(savepath + key[2] + '_Median.xlsx')

    if settings[1] == '3':
        print("hatching label")
        hatch = '|||'
    else:
        print("not hatching label")
        hatch = ''
    if zCubeSheets:
        ZCube = mpatches.Patch(color=ZDotColor, hatch=hatch, label=settingsDict[settings[1]][:-1] + ' Proximal-Distal ' + settingsDict[settings[0]][11:-1])
        handles.append(ZCube)
    if yCubeSheets:
        YCube = mpatches.Patch(color=YDotColor, hatch=hatch, label=settingsDict[settings[1]][:-1] + ' Cranial-Caudal ' + settingsDict[settings[0]][11:-1])
        handles.append(YCube)
    if xCubeSheets:
        XCube = mpatches.Patch(color=XDotColor, hatch=hatch, label=settingsDict[settings[1]][:-1] + ' Medial-Lateral ' + settingsDict[settings[0]][11:-1])
        handles.append(XCube)
    plotTitle = 'Stress vs Strain on '
    if settings[2].lower() == 'median':
        plotTitle += 'median of '
    if 'pd' in settings[3] and 'cc' in settings[3] and 'ml' in settings[3]:
        plotTitle += 'each orientation of '
    if settings[1] == '3':
        plotTitle += '\n 9mm\u00B3 Formlabs '
    elif settings[1] == '4':
        plotTitle += '\n 3mm\u00B3 BMF '
    if settings[0] == '1':
        plotTitle += 'Cube in Compression'
    elif settings[0] == '2':
        plotTitle += 'Beam in Tension'
    _plot_title = plotTitle


generating = True
graphCount = 0
while generating:
    generating = False
    generateGraph()
    graphCount += 1
    request = str(input("Would you like to generate another graph? (y/n): "))
    print(request)
    if 'y' in request.lower():
        generating = True

ax.legend(handles=handles)

plt.xlabel('Microstrain (\u03BC\u03B5)')
plt.ylabel('Stress (MPa)')

if graphCount > 1:
    plt.title = input("What graphs are you comparing (A vs B)?: ")
else:
    plt.title = _plot_title
plt.xlim(0, 400000)
plt.ylim(0, 17.5)
savename = input("Save file with name: ")
plt.savefig('../Final Graphs/' + savename + '.png', transparent=True)
plt.show()

input()
