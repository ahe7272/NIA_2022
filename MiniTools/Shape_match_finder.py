import json
import os 
import pandas as pd
import shutil

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

from_path = 'C:/Users/Administrator/Desktop/from'
to_path = 'C:/Users/Administrator/Desktop/to'
# to_path = 'C:/Users/Administrator/Downloads/최종 bbox'
from_files = []
to_files = []
change_log = {}
original_name = []
new_name = []

for (path, dir, files) in os.walk(from_path): 
    from_files += [path + '/' + Json for Json in files if Json.lower().endswith('.json')]
for (path, dir, files) in os.walk(to_path): 
    to_files += [path + '/' + Json for Json in files if Json.lower().endswith('.json')]

# for from_file in from_files:
#     from_objects = getjson(from_file)
#     if from_objects['shapes'][0]['points'] == [[
# 					0.0,
# 					0.0
# 				],
# 				[
# 					1280.0,
# 					720.0
# 				]]:
#         shutil.move(from_file, 'C:/Users/Administrator/Desktop/Manual/From/' + from_file.split('/')[-1])

# for to_file in to_files:
#     to_objects = getjson(to_file)
#     if to_objects['shapes'][0]['points'] == [[
# 					0.0,
# 					0.0
# 				],
# 				[
# 					1280.0,
# 					720.0
# 				]]:
#         shutil.move(to_file, 'C:/Users/Administrator/Desktop/Manual/To/' + to_file.split('/')[-1])

for from_file in from_files:
    from_objects = getjson(from_file)
    try:
        for to_file in to_files:
            if to_file.split('/')[-1] in new_name:
                continue
            to_objects = getjson(to_file)
            if to_objects['shapes'][0]['points'][:2] == from_objects['shapes'][0]['points'][:2]:
                to_objects['Longitude'] = round(float(from_objects['Longitude']),6)
                to_objects['Latitude'] = round(float(from_objects['Latitude']),6)
                original_name += [from_file.split('/')[-1]]
                new_name += [to_file.split('/')[-1]]
                with open(to_file, 'w') as j:
                    json.dump(to_objects, j, indent='\t')
                    j.close()
                break

        
    except:
        print(from_file, to_file)
        continue

# change_log['Old'] = original_name
# change_log['New'] = new_name

# df = pd.DataFrame(change_log)
# df.set_index('Old', inplace = True)

# df.to_csv(to_path + '/Name_change_log_polygon.csv')


# Bbox 내 폴리곤 삭제
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