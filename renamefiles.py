import os

folder = r'G:\LIU Research\PythonScripts\DataAnalysis\temp delete\\'
count = 504

for file_name in os.listdir(folder):
    source = folder + file_name
    destination = folder + file_name[:-25] + '.xlsx'

    os.rename(source, destination)
print('ALl Files Renamed')
print('New Names are')

res = os.listdir(folder)
print(res)