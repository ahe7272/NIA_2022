import json
import os
import numpy as np
from classes import sea_animal_dict
import pandas as pd
import copy

running_path = input("경로: ")
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

poly_dict = {'Sargassum_Near': 0 , 'Sargassum_Mid': 0 , 'Sargassum_Far': 0, 'Ecklonia_cava_Near' : 0, 'Ecklonia_cava_Mid' : 0, 'Ecklonia_cava_Far' : 0}
len_arr= 0
for root, dirs, files in os.walk(running_path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        # print(Json)
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        maxratio, label_with_ratio = ratio_of_objects(objects)
        if len(label_with_ratio) > 1:
            for label, ratio in label_with_ratio:
                if maxratio == ratio:
                    maxlabel = label
        else:
            maxlabel = label_with_ratio[0][0] 
        
        if objects['Distance'] == 0.5:
            poly_dict[maxlabel +'_Near'] += 1
        elif objects['Distance'] == 1.0:
            poly_dict[maxlabel +'_Mid'] += 1
        elif objects['Distance'] == 1.5:
            poly_dict[maxlabel +'_Far'] += 1

print(poly_dict)
