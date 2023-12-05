import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def createArrayFromExcel(dataframe, collumnName):
    tempArray = []
    for i in dataframe.iterrows():
        tempArray.append(dataframe.loc[i[0], collumnName])
    return tempArray

selectedCols = [5, 6]
# noinspection PyTypeChecker
cube1Z_sheet = pd.read_excel('ExcelFiles/BMF_Cube_One1.xlsx', usecols=selectedCols, skiprows=3)

strainZ = createArrayFromExcel(cube1Z_sheet, 'Strain')
stressZ = createArrayFromExcel(cube1Z_sheet, 'Stress')

# noinspection PyTypeChecker
plt.scatter(strainZ[9990:10000], stressZ[9990:10000], s=2, c='blue')

plt.xlabel('Strain')
plt.ylabel('Stress (N/mm\u00B2)')
plt.title('Stress vs Strain on \n 3mm\u00B3 BMF Cubes (Z-Orientation CubeOne1)')
# plt.savefig('CombinedCubes')
plt.show()
