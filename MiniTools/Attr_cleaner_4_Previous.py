import json
import os 

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

# 기구축에 신규데이터 속성과 일치 작업
# for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/ready_bbox'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             objects['Transparency'] = None
#             objects['Latitude'] = objects['annotation']['metainfo']['location']['latitude']['dd']
#             objects['Longitude'] = objects['annotation']['metainfo']['location']['longitude']['dd']
#             objects.pop('annotation')
#             objects['CDist'] = None
#             objects['Site_Type'] = None
#             objects['Depth'] = None
#             objects['Source_video'] = None
#             objects['Video_time'] = None
#             objects['Frame_no'] = None

#             with open(path + '/' + item, 'w') as j:
#                 json.dump(objects, j, indent='\t')
#                 j.close()
                
# 기구축 내 클래스명 통일 작업

classes = []
for (path, dir, files) in os.walk('C:/Users/Administrator/Downloads/ready_bbox'): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            for label in objects['shapes']:
                if label['label'] not in classes:
                    classes.append(label['label'])

print(classes)
            # objects['Transparency'] = None
            # objects['Latitude'] = objects['annotation']['metainfo']['location']['latitude']['dd']
            # objects['Longitude'] = objects['annotation']['metainfo']['location']['longitude']['dd']
            # objects.pop('annotation')
            # objects['CDist'] = None
            # objects['Site_Type'] = None
            # objects['Depth'] = None
            # objects['Source_video'] = None
            # objects['Video_time'] = None
            # objects['Frame_no'] = None

            # with open(path + '/' + item, 'w') as j:
            #     json.dump(objects, j, indent='\t')
            #     j.close()
                