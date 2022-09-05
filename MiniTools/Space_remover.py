import json
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/8_3'): 
    for item in files:
        space_removed = ''.join(item.split(' '))
        old = path + '/' + item
        new = path + '/' + space_removed
        os.rename(old, new)
        if new[-5:] == '.json':
            objects = getjson(new)
            objects['imagePath'] = space_removed[:-5] + '.jpg'
            with open(new, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()
                