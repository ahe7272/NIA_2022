import json
import datetime
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk('C:/Dataset/라벨링데이터'): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            # objects['ID'] = "CW217"
            # objects['CDist'] = None
            # objects['Site_Type'] = None
            # objects['Depth'] = None
            # objects['imageData'] = None
            # objects['Collection_method'] = 'Diver'
            objects['Source_video'] = None
            objects['Video_time'] = None
            objects['Frame_no'] = None
            # # Source_video 입력 후 돌리는 수집 방법 구문 
            # if len(objects['Source_video'].split('ROV')) > 1:
            #     objects['Collection_method'] = 'ROV'
            # else:
            #     objects['Collection_method'] = 'Diver'
            # objects['Distance'] = None
            # objects['Latitude'] = round(float(objects['Latitude']),2)
            # objects['Longitude'] = round(float(objects['Longitude']),2)
            with open(path + '/' + item, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()

# for (path, dir, files) in os.walk('C:/Dataset'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             try:
#                 objects.pop('ID')
#             except:
#                 pass
#             if len(objects) != 16:
#                 print(item)
#             with open(path + '/' + item, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()
