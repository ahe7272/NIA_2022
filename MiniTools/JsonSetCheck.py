import json
import os 
import shutil

searchpath = input('경로: ')
for (path, dir, files) in os.walk(searchpath): 
    if path.split('\\')[-1].split(' ')[-1] in [ 'Originals', 'Original']:
        continue
    for item in files:
        if item[-5:] == '.json':
            if os.path.isfile(path + '/' + item[:-4] + 'jpg') == False:
                print(path, item)
        elif item[-4:] == '.jpg':
            if os.path.isfile(path + '/' + item[:-4] + '.json') == False:
                print(path, item)