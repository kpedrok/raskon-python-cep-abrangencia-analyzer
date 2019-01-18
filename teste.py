import os
path = os.getcwd()
files = os.listdir(path)
print(files)

files_xls = [f for f in files if f[-3:] == 'xls']

print (files_xls)