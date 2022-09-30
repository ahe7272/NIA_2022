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
                
#신규 파일명과 과거 파일명에 따른 원본 비디오 속성 기입
for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/9_1/Polygon/Attr_errors/CW305'): 
    for item in files:
        if item[-5:] == '.json':
            # print(item)
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


# 올빅뎃에서 파일명 변경 후 과거 GX로만 되어 있었던 비디오명 반영 속성 기입
# for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/8_5_sunken'): 
#     for item in files:
#         if item[-5:] == '.json':
#             if item.split('_')[3] == '1':
#                 objects = getjson(path + '/' + item)
#                 objects['Source_video'] = item.split('_')[5] + '.mp4'
#                 objects['Video_time'] = str(datetime.timedelta(seconds= ((int(item.split('_')[6].split('.')[0])*2)-2)))
#                 objects['Frame_no'] = (int(item.split('_')[6].split('.')[0])-1)*2*60
#                 with open(path + '/' + item, 'w') as j:
#                     json.dump(objects, j, indent='\t')
#                     j.close()
#             else:
#                 print(item)