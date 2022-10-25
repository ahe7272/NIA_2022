import json
import datetime
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/ROV_latlon'): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            objects['Longitude'] = 129.423091
            objects['Latitude'] = 37.055586
            # # objects['CDist'] = None
            # # objects['Site_Type'] = None
            # # objects['Depth'] = None
            # objects['imageData'] = None

            # objects['Source_video'] = None
            # objects['Video_time'] = None
            # objects['Frame_no'] = None
            # # Source_video 입력 후 돌리는 수집 방법 구문 
            # if len(objects['Source_video'].split('ROV')) > 1:
            #     objects['Collection_method'] = 'ROV'
            # else:
            #     objects['Collection_method'] = 'Diver'
            # objects['Distance'] = 0.5
            # objects['Latitude'] = round(float(objects['Latitude']),6)
            # objects['Longitude'] = round(float(objects['Longitude']),6)
            # for label in objects['shapes']:
            #     if (max(label['points'][0] + label['points'][1])) > 3840:
            #         print(item, label)
            with open(path + '/' + item, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()

# for (path, dir, files) in os.walk('C:/Dataset/ori/Polygon'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             try:
#                 objects.pop('ID')
#                 with open(path + '/' + item, 'w') as j:
#                     json.dump(objects, j, indent='\t')
#                     j.close()
#             except:
#                 pass
#             if len(objects) != 23:
#                 print(item)
