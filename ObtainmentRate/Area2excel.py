import json
import os
import numpy as np
import pandas as pd
import copy
from classes import debris_dict, sea_animal_dict

path = input("면적 산출할 json 경로 \n")
savepath = 'C:/Users/Administrator/Desktop'
classes_dict= sea_animal_dict()

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# 이미지내 객체 비율
def ratio_of_objects(objects):
    height = objects['imageHeight']
    width = objects['imageWidth']
    imagesize = height * width 
    label_with_ratio = [] 
    maxratio = 0
    Etc_list = [] 
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        points = np.array(objects['shapes'][o]['points'])
        if label == 'Etc':
            Etc_list += [label]
            continue
        # bbx
        if objects['shapes'][o]['shape_type'] == 'rectangle':
            object_width = abs(points[0, 0] - points[1, 0])
            object_height = abs(points[0, 1] - points[1, 1])

        # polygon
        else:
            y = points[:, 0]
            x = points[:, 1]
            object_height = max(y) - min(y)    
            object_width = max(x) - min(x)     
        object_size = object_height * object_width
        if maxratio < (object_size / imagesize * 100):
            maxratio = (object_size / imagesize * 100)
        label_with_ratio.append((label, object_size / imagesize * 100))
    if len(Etc_list) == len(objects['shapes']):
        for o in range(len(objects['shapes'])):
            label = objects['shapes'][o]['label']
            points = np.array(objects['shapes'][o]['points'])
            # bbx
            if objects['shapes'][o]['shape_type'] == 'rectangle':
                object_width = abs(points[0, 0] - points[1, 0])
                object_height = abs(points[0, 1] - points[1, 1])

            # polygon
            else:
                y = points[:, 0]
                x = points[:, 1]
                object_height = max(y) - min(y)    
                object_width = max(x) - min(x)
            object_size = object_height * object_width
            if maxratio < (object_size / imagesize * 100):
                maxratio = (object_size / imagesize * 100)
            label_with_ratio.append((label, object_size / imagesize * 100)) 
    return maxratio, label_with_ratio 

len_arr= 0 
df_stat = pd.DataFrame.from_dict(list(copy.deepcopy(classes_dict).keys())).transpose()
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        if objects['shapes'][0]['label'] in ['Ecklonia_cava', 'Sargassum']:
            continue
        labeldict = copy.deepcopy(classes_dict)
        maxratio, label_with_ratio = ratio_of_objects(objects)
        if len(label_with_ratio) > 1:
            for label, ratio in label_with_ratio:
                if maxratio == ratio:
                    maxlabel = label
                    labeldict[maxlabel] = maxratio
        else:
            maxlabel = label_with_ratio[0][0]
            labeldict[maxlabel] = maxratio
        df_single = pd.DataFrame(list(labeldict.values()), columns=[Json]).transpose()    
        df_stat = pd.concat([df_stat, df_single])
        labeldict = copy.deepcopy(classes_dict)

df_stat.to_excel(savepath + '/Heli+Turbo.xlsx')

# dict_total = copy.deepcopy(classes_dict)
# for root, dirs, files in os.walk(path):
#     jsonarr = [Json for Json in files if Json.lower().endswith('json')]
#     for Json in jsonarr:
#         name = os.path.splitext(Json)[0]
#         jsonfile = os.path.join(root, name + '.json')
#         objects = getjson(jsonfile)
#         if len(objects['shapes']) == 0:
#             print(Json)
#             continue   
#         labeldict = copy.deepcopy(classes_dict)
#         for label in objects['shapes']:
#             if label['label'] not in dict_total.keys():
#                 print(Json)
#                 labeldict[label['label']] += 1
#         for k, v in labeldict.items():
#             dict_total[k] += v
         

#         # df_single = pd.DataFrame(list(labeldict.values()), columns=[Json]).transpose()    
#         # df_stat = pd.concat([df_stat, df_single])
# print(dict_total)