import json
import os
import numpy as np
import pandas as pd
import copy
from classes import debris_dict, sea_animal_dict

path = input("Clustering을 확인할 폴더 경로를 입력하세요.\n")

def sea_MM_dict():
    object_dic = {
        'Asterias_amurensis_min' : 0, 
        'Asterias_amurensis_max' : 0, 
        'Asterina_pectinifera_min' : 0,
        'Asterina_pectinifera_max' : 0,
        'Conch_min' : 0,
        'Conch_max' : 0,
        'Heliocidaris_crassispina_min' : 0,
        'Heliocidaris_crassispina_max' : 0,
        'Hemicentrotus_min' : 0,
        'Hemicentrotus_max' : 0,
        'Sea_hare_min' : 0,
        'Sea_hare_max' : 0,
        'Turbo_cornutus_min' : 0,
        'Turbo_cornutus_max' : 0
        }
    return object_dic


savepath = 'C:/Users/Administrator/Desktop'
classes_dict= sea_MM_dict()


def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

# 이미지내 객체 비율
def ratio_of_objects(objects):
    height = objects['imageHeight']
    width = objects['imageWidth']
    imagesize = height * width 
    label_with_ratio = sea_animal_dict()

    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        points = np.array(objects['shapes'][o]['points'])
        # try:
        #     size = objects['shapes'][o]['Size']
        # except:
        #     continue
        # if objects['shapes'][o]['Size'] == 0:
        #     continue

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
        ratio = (object_size / imagesize)*100
        if label_with_ratio[label] != 0:
            label_with_ratio[label] += [ratio]
        else:
            label_with_ratio[label] = [ratio]
    return label_with_ratio

len_arr= 0 
df_stat = pd.DataFrame.from_dict(list(copy.deepcopy(classes_dict).keys())).transpose()
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        print(Json)
        name = os.path.splitext(Json)[0]
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        if len(objects['shapes']) == 0:
            print(Json)
            continue   
        if objects['shapes'][0]['label'] in ['Ecklonia_cava', 'Sargassum']:
            continue
        labeldict = copy.deepcopy(classes_dict)
        # labeldict['Distance'] = objects['Distance']
        label_with_ratio = ratio_of_objects(objects)
        # print(label_with_ratio)
        for label, ratio in label_with_ratio.items():
            if ratio == 0:
                continue
            if (ratio != 0) and (len(ratio) > 1):
                labeldict[label+'_max'] = max(ratio)
                labeldict[label+'_min'] = min(ratio)
            elif (ratio != 0) and len(ratio) == 1:
                labeldict[label+'_max'] = max(ratio)
        df_single = pd.DataFrame(list(labeldict.values()), columns=[Json]).transpose()    
        df_stat = pd.concat([df_stat, df_single])
            # labeldict = copy.deepcopy(classes_dict)

df_stat.to_excel(savepath + '/2-3.xlsx')