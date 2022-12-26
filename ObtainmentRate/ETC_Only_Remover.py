import json
import os
import numpy as np
import shutil

path = input("ETC를 제거할 폴더 경로를 입력하세요.\n")

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# # 이미지내 객체 비율
# for root, dirs, files in os.walk(path):
#     jsonarr = [Json for Json in files if Json.lower().endswith('json')]
#     for Json in jsonarr:
#         name = os.path.splitext(Json)[0]
#         jsonfile = os.path.join(root, name + '.json')
#         objects = getjson(jsonfile)
    
#         Etc_list = [] 
#         for o in range(len(objects['shapes'])):
#             label = objects['shapes'][o]['label']
#             points = np.array(objects['shapes'][o]['points'])
#             if label == 'Etc':
#                 Etc_list += [label]
#                 continue
        
#         if len(Etc_list) == len(objects['shapes']):
#             # print('C:/Dataset(침적)/라벨링데이터/신규구축 Bbox/Etc_only/' + name + '.json')
#             shutil.move(jsonfile, 'C:/Dataset(침적)/라벨링데이터/기구축 Bbox/Etc_only/' + name + '.json')

for root, dirs, files in os.walk(path):
    for file in files:
        shutil.move('C:/Dataset(침적)/원천데이터/신규구축 Bbox(화질 개선 전)/' + file[:-5] + '.jpg', 'C:/Dataset(침적)/원천데이터/신규구축 Bbox(화질 개선 전)/Etc_only/' + file[:-5] + '.jpg')