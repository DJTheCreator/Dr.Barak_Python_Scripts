import shutil

original = r'S:\5F_Trabecular_Tension\5F_1.tiff'
target = r'S:\5F_Trabecular_Tension\5F_'
num = 678

for i in range(503):
    num += 1
    target_name = target + str(num) + '.tiff'
    shutil.copyfile(original, target_name)