import os
import shutil
import json 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects


okay = []
for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/Latlong'):
    for item in files:
        if os.path.isfile('C:/Users/Administrator/Desktop/from/' + item):
            from_objects = getjson(path + '/' + item)
            to_objects = getjson('C:/Users/Administrator/Desktop/from/' + item)
            to_objects['Latitude'] = from_objects['Latitude']
            to_objects['Longitude'] = from_objects['Longitude']
            with open('C:/Users/Administrator/Desktop/from/' + item, 'w') as j:
                    json.dump(to_objects, j, indent='\t')
                    j.close()
