import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from numpy import median

arrx = [0,1,2,3,4,5]

arr1y = [8,10,12,14,16,18]
arr2y = [0,2,4,6,8,10]

yArray = [arr1y, arr2y]

def createMedianArray(array):
    newArray = []
    smallestArray = array[0]
    for i in range(len(smallestArray)):
        valueArray = []
        for sheet in array:
            valueArray.append(sheet[i])
        newArray.append(median(valueArray))
    return newArray


medianYArray = createMedianArray(yArray)
# noinspection PyTypeChecker
plt.scatter(x=arrx, y=medianYArray, s=2)
plt.show()