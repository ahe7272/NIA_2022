import json
import os
import shutil

path = input("경로 입력: \n")

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        try:
            if objects['Distance'] == 0.5:
                os.makedirs(root + '/Near' , exist_ok=True)
                shutil.move(root + '/' + Json, root + '/Near/' + Json)
                shutil.move(root + '/' + Json[:-5] + '.jpg',  root + '/Near/' + Json[:-5] + '.jpg')
        except:
            os.makedirs(root + '/Near' , exist_ok=True)
            shutil.move(root + '/' + Json, root + '/Near/' + Json)
            shutil.move(root + '/' + Json[:-5] + '.jpg',  root + '/Near/' + Json[:-5] + '.jpg')