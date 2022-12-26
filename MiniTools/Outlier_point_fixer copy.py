import json
import os 
import shutil 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

wrong_img = []

for (path, dir, files) in os.walk('C:/Dataset(침적)/라벨링데이터/신규구축 Polygon'):
    for file in files:
        if file[-5:] == '.json':
            old_objects = getjson(path + '/' + file)
            new_objects = getjson('C:/침적 History/신규구축 Polygon(위경도소수점 변경)/' + file)
            for label in old_objects['shapes']:
                for point in label['points']:                   
                    if (point[1] < 0):
                        old_objects['shapes'] = new_objects['shapes']
                        with open('C:/침적 History/New_Polygon_to_copy/' + file, 'w') as j:
                            json.dump(old_objects, j, indent='\t')
                            j.close()