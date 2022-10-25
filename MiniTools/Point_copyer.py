import json
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk('C:/Dataset/ori/Polygon'): 
    for item in files:
        if item[-5:] == '.json':
            if os.path.isfile(path + '(b4Check)/' + '_'.join(item.split('_')[2:])):
                from_objects = getjson(path + '(b4Check)/' + '_'.join(item.split('_')[2:]))
                to_objects = getjson(path + '/' + item)
                to_objects['Longitude'] = from_objects['Longitude']
                to_objects['Latitude'] = from_objects['Latitude']
                to_objects['Source_video'] = from_objects['Source_video']
                to_objects['Video_time'] = from_objects['Video_time']
                to_objects['Frame_no'] = from_objects['Frame_no']
                to_objects['Collection_method'] = from_objects['Collection_method']
                to_objects['Distance'] = from_objects['Distance']
                # to_objects.pop('ID')
                with open(path + '/' + item, 'w') as j:
                    json.dump(to_objects, j, indent='\t')
                    j.close()

#Bbox 내 폴리곤 삭제
# for (path, dir, files) in os.walk('C:/Dataset/ori/Bbox/Bbox_in_polygon'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             to_remove = []
#             for k, label in enumerate(objects['shapes']):
#                 if label['label'] in ['Ecklonia_cava', 'Sargassum']:
#                     to_remove += [k]
#             to_remove.reverse()
#             for i in to_remove:
#                 objects['shapes'].pop(i)
#             with open(path + '/' + item, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()