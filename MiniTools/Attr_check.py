import json
import glob
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

# for i in glob.glob("C:/Users/Administrator/Downloads/BoundingBox/CW212/*.json"): 
#     objects = getjson(i)
#     if len(objects) != 19:
#         print(i)

for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/8.1'):
    for file in files:
        if file[-4:] == 'json':
            objects = getjson(path + '/' +file)
            # if len(objects['shapes'][0]['points']) <= 2:
            # if objects['CDist'] == 0:
                # print(path + '/' + file)
            if len(objects) != 15:
                print(path + '/' +file)
