import json
import os
import shutil

path = input("폴더 경로를 입력하세요.\n")
    
def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# for root, dirs, files in os.walk(path):
#     for file in files:
#         if file[-5:] == ".json":
#             objects = getjson(root + '/' + file)
#             new_objects = getjson(root + '/' + file)
#             if root.split('\\')[-1] in ['Empty_shapes', 'Bbox', 'Other_objects']:
#                 continue
#             if len(objects['shapes']) == 0:
#                 shutil.move(root +'/' + file, root + '/Empty_shapes/' + file)
#                 shutil.move(root + '/' + file[:-5] + '.jpg', root + '/Empty_shapes/' + file[:-5] + '.jpg') 
#                 continue  
#             for Annotation in objects['shapes']:
#                 if Annotation['label'] in ['bundle of ropes', 'fish net', 'rope', 'bundle of rope']:
#                     new_objects['shapes'].remove(Annotation)
#             with open(root + '/' + file, 'w') as j:
#                 json.dump(new_objects, j, indent='\t')
#                 j.close()

# for root, dirs, files in os.walk(path):
#     for file in files:
#         if file[-5:] == ".json":
#             objects = getjson(root + '/' + file)
#             new_objects = getjson(root + '/' + file)
#             if root.split('\\')[-1] in ['Empty_shapes', 'Bbox', 'Other_objects']:
#                 continue
#             if len(objects['shapes']) == 0:
#                 shutil.move(root +'/' + file, root + '/Empty_shapes/' + file)
#                 shutil.move(root + '/' + file[:-5] + '.jpg', root + '/Empty_shapes/' + file[:-5] + '.jpg') 
#                 continue  
#             for Annotation in objects['shapes']:
#                 if Annotation['label'] in ['other objects','othe objects', 'other objets']:
#                     shutil.move(root +'/' + file, root + '/Other_objects/' + file)
#                     shutil.move(root + '/' + file[:-5] + '.jpg', root + '/Other_objects/' + file[:-5] + '.jpg') 
#                     break
#             try:
#                 shutil.move(root +'/' + file, root + '/Bbox/' + file)
#                 shutil.move(root + '/' + file[:-5] + '.jpg', root + '/Bbox/' + file[:-5] + '.jpg') 
#             except:
#                 pass

# for root, dirs, files in os.walk(path):
#     for file in files:
#         if file[-5:] == ".json":
#             objects = getjson(root + '/' + file)
#             for Annotation in objects['shapes']:
#                 if Annotation['label'] in ['other objects','othe objects', 'other objets', 'bundle of ropes', 'fish net', 'rope', 'bundle of rope' ]:
#                     print(file)


for root, dirs, files in os.walk(path):
    for file in files:
        if file[-5:] == ".json":
            objects = getjson(root + '/' + file)
            for Annotation in objects['shapes']:
                if Annotation['label'] in ['circular fish trap', 'rectangular fish trap', 'eel fish trap', 'spring fish trap']:
                    Annotation['label'] = 'Fish_trap'
                elif Annotation['label'] == 'wood':
                    Annotation['label'] = 'Wood'
                elif Annotation['label'] == 'tire':
                    Annotation['label'] = 'Rubber_tire'
                
            with open(root + '/' + file, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()