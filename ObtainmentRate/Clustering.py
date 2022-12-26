import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import copy

path = input("Clustering을 확인할 폴더 경로를 입력하세요.\n")
D_or_S = input("침적 데이터면 D, 조식동물이면 S를 입력해주세요. ")
if D_or_S == 'D':
    savepath = 'C:/Users/Administrator/Desktop'
    classes_dict= debris_dict()
elif D_or_S == 'S':
    savepath = 'C:/Users/Administrator/Desktop'
    classes_dict= sea_animal_dict()
else:
    exit()

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
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        points = np.array(objects['shapes'][o]['points'])
        try:
            size = objects['shapes'][o]['Size']
        except:
            continue
        if objects['shapes'][o]['Size'] == 0:
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
    return maxratio, label_with_ratio 

def classify_distance(maxratio):
    if maxratio <= 20:
        return 'Far'
    elif (maxratio <= 60) and (maxratio > 20): 
        return 'Mid'
    elif maxratio > 60:
        return 'Near'

dict_near = copy.deepcopy(classes_dict)
dict_mid = copy.deepcopy(classes_dict)
dict_far = copy.deepcopy(classes_dict)
dict_total = copy.deepcopy(classes_dict)
len_arr= 0 
df_stat = pd.DataFrame.from_dict(list(copy.deepcopy(classes_dict).keys())).transpose()
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        print(Json)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        labeldict = copy.deepcopy(classes_dict)
        maxratio, label_with_ratio = ratio_of_objects(objects)
        if len(label_with_ratio) > 1:
            for label, ratio in label_with_ratio:
                if labeldict[label] < ratio:
                    labeldict[label] = ratio
        else:
            labeldict[label_with_ratio[0][0]] = maxratio

        df_single = pd.DataFrame(list(labeldict.values()), columns=[Json]).transpose()    
        df_stat = pd.concat([df_stat, df_single])

df_stat.to_excel(savepath + '/Area.xlsx')