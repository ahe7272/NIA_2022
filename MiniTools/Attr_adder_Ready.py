import json
import os 
import cv2

path_input = input('경로: ')
def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk(path_input): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            objects['imageData'] = None
            # img = cv2.imread(path + '/' + item[:-5] + '.jpg')
            # objects['imageHeight'] = img.shape[0]
            # objects['imageWidth'] = img.shape[1]
            objects['Transparency'] = None
            objects['CDist'] = None
            objects['Site_Type'] = None
            objects['Depth'] = None
            objects['Source_video'] = None
            objects['Video_time'] = None
            objects['Frame_no'] = None
            objects['Distance'] = None
            try:
                objects.pop('ID')
                with open(path + '/' + item, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()
            except:
                pass
            if len(objects) != 17:
                print(item)
            objects['Latitude'] = round(float(objects['Latitude']),6)
            objects['Longitude'] = round(float(objects['Longitude']),6)

            with open(path + '/' + item, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()