import os
import shutil
import json

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

lookfor_path = input('찾을 파일 경로: ')

for (path, dir, files) in os.walk(lookfor_path):   
    if len(path.split('_Rope')) > 1:
        continue 
    for file in files:
        print(path)
        if file[-4:] == 'json':
            objects = getjson(path + '/' + file)
            for label in objects['shapes']:
                if label['label'] in ['Rope']:
                    os.makedirs(path +'_Rope', exist_ok=True)
                    shutil.move(path + '/' + file[:-5] + '.jpg', path + '_Rope/' + file[:-5] + '.jpg')
                    shutil.move(path + '/' + file, path + '_Rope/' + file)
                    break
