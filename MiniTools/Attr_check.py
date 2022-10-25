import json
import glob
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

for (path, dir, files) in os.walk("C:/Users/Administrator/Downloads/TTT"):
    for file in files:
        if file[-5:] == '.json':
            objects = getjson(path + '/' + file)
            if len(objects) != 23:
                
                print(file)

# for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/10월1주차'):
#     for file in files:
#         if file[-4:] == 'json':
#             objects = getjson(path + '/' +file)
#             # if len(objects['shapes'][0]['points']) <= 2:
#             objects['imageData'] = None
#             with open(path + '/' + file, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()
