import json
import glob
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

prefix = '7_3_'
for (path, dir, files) in os.walk('D:/1st_Original/Test/Bbox'): 
    for item in files:
        # print(item[4:])
        # old = path + '/' + item
        # new = path + '/' + item[4:]
        # os.rename(old, new)
        # # if new[-5:] == '.json':
        # #     objects = getjson(new)
        # #     objects['imagePath'] = prefix + item[:-5] + '.jpg'
        # #     with open(new, 'w') as j:
        # #         json.dump(objects, j, indent='\t')
        # #         j.close()
            

        # if item[:2] == 'GX':    
            old = path + '/' + item
            new = path + '/' + prefix + item
            os.rename(old, new)
            # if new[-5:] == '.json':
            #     objects = getjson(new)
            #     objects['imagePath'] = prefix + item[:-5] + '.jpg'
            #     with open(new, 'w') as j:
            #         json.dump(objects, j, indent='\t')
            #         j.close()
                