import json
import os 
import shutil

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/7_2_Sea/(2022-08-04)_bbox/Duplicated'):
    for file in files:
        if file[-4:] == 'json':
            objects = getjson(path + '/' +file)
            CWfolder = str(objects['ID']).upper()
            os.makedirs(path +'/' + CWfolder , exist_ok=True)
            shutil.move(path + '/' + file[:-5] + '.jpg', path + '/' +CWfolder+ "/" + file[:-5] + '.jpg')
            shutil.move(path + '/' + file, path + '/' +CWfolder+ "/" + file)

