import json
import datetime
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

# for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/8_2_sunken/Polygon/CW304'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             objects['Source_video'] = item.split('_')[2] + '.mp4'
#             objects['Video_time'] = str(datetime.timedelta(seconds= ((int(item.split('_')[3].split('.')[0])*2)-2)))
#             objects['Frame_no'] = (int(item.split('_')[3].split('.')[0])-1)*2*60
#             with open(path + '/' + item, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()
                

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/8_3'): 
    for item in files:
        if item[-5:] == '.json':
            if item[:2] == 'GX':
                objects = getjson(path + '/' + item)
                objects['Source_video'] = item.split('_')[0] + '.mp4'
                objects['Video_time'] = str(datetime.timedelta(seconds= ((int(item.split('_')[1].split('.')[0])*2)-2)))
                objects['Frame_no'] = (int(item.split('_')[1].split('.')[0])-1)*2*60
                with open(path + '/' + item, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()
            else:
                objects = getjson(path + '/' + item)
                objects['Source_video'] = '_'.join(item.split('_')[:3]) + '.mp4'
                objects['Video_time'] = str(datetime.timedelta(seconds= ((int(item.split('_')[3].split('.')[0])*2)-2)))
                objects['Frame_no'] = (int(item.split('_')[3].split('.')[0])-1)*2*60
                with open(path + '/' + item, 'w') as j:
                    json.dump(objects, j, indent='\t')
                    j.close()