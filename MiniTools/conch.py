import json
import os 
import shutil

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/p'): 
    if path.split('\\')[-1] in ['far', 'mid', 'near']:
        continue
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            if objects['Distance'] == 0.5:
                shutil.copy(path + '/' + item, path + '/near/' + item)  
                shutil.copy(path + '/' + item[:-4] + 'jpg',path + '/near/' + item[:-4] + 'jpg') 
                continue
            elif objects['Distance'] == 1.0:
                shutil.copy(path + '/' + item, path + '/mid/' + item)  
                shutil.copy(path + '/' + item[:-4] + 'jpg',path + '/mid/' + item[:-4] + 'jpg')
                continue 
            elif objects['Distance'] == 1.5:
                shutil.copy(path + '/' + item, path + '/far/' + item)  
                shutil.copy(path + '/' + item[:-4] + 'jpg',path + '/far/' + item[:-4] + 'jpg') 