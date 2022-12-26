import json
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

running_path = input('경로: ')

for (path, dir, files) in os.walk(running_path): 
    for item in files:
        space_removed = '_'.join(item.split(' '))
        # Original_removed = space_removed.split('Original_')[-1]

        old = path + '/' + item
        new = path + '/' + space_removed
        os.rename(old, new)
        # if new[-5:] == '.json':
        #     objects = getjson(new)
        #     objects['imagePath'] = space_removed[:-5] + '.jpg'
        #     with open(new, 'w') as j:
        #         json.dump(objects, j, indent='\t')
        #         j.close()
                