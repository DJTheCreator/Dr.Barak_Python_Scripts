import math

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy
import numpy as np
import pandas


def createArrayFromDataframes(dataframeArray, columnName):
    tempArray = []
    for i in dataframeArray.iterrows():
        tempArray.append(dataframeArray.loc[i[0], columnName])
    return tempArray


CZ_BMF = pandas.read_excel('DataAnalysis/MedianExcelFiles/BMF_Cube_One_Median.xlsx')
BMF_strainZ = createArrayFromDataframes(CZ_BMF, 'Strain')
BMF_stressZ = createArrayFromDataframes(CZ_BMF, 'Median Stress')

CZ_3DP = pandas.read_excel('DataAnalysis/MedianExcelFiles/3DP_Cube_Z_Median.xlsx')
_3DP_strainZ = createArrayFromDataframes(CZ_3DP, 'Strain')
_3DP_stressZ = createArrayFromDataframes(CZ_3DP, 'Median Stress')


plt.scatter(x=BMF_strainZ, y=BMF_stressZ, s=.25, c='blue')
plt.scatter(x=_3DP_strainZ, y=_3DP_stressZ, s=.25, c='red')

ax = plt.subplot()

_3DP_Cube = mpatches.Patch(color='red', label='Formlabs Compression')
BMF_Cube = mpatches.Patch(color='blue', label='BMF Compression')

# _3dp_ci = 2.576 * numpy.std(medianZCubesStress) / math.sqrt(len(medianZCubesStress))
# plt.fill_between(medianZCubesStrain, (medianZCubesStress - z_ci), (medianZCubesStress + z_ci), color='orange', alpha=0.4)
# bmf_ci = 2.576 * std(medianYCubesStress) / math.sqrt(len(medianYCubesStress))
# plt.fill_between(medianYCubesStrain, (medianYCubesStress - y_ci), (medianYCubesStress + y_ci), color='blue', alpha=0.4)

ax.legend(handles=[_3DP_Cube, BMF_Cube])

plt.xlabel('Microstrain (\u03BC\u03B5)')
plt.ylabel('Stress (MPa)')
plt.title('Stress vs Strain on median 9mm\u00B3 Form 3 Cubes \n vs 3mm\u00B3 BMF Cubes (Distal-Proximal Compression)')
plt.savefig('3DP-BMF_Compression_Z')
plt.show()
input()
