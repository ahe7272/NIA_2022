import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import shutil

path = input("말똥성게를 찾을 폴더 경로를 입력하세요.\n")

savepath = 'C:/Users/Administrator/Desktop/test'
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

def classify_distance_4_debris(maxratio):
    if maxratio <= 20:
        return 'Far'
    elif (maxratio <= 60) and (maxratio > 20): 
        return 'Mid'
    elif maxratio > 60:
        return 'Near'

def classify_distance_4_seaanimal(maxratio, maxlabel):
    if maxlabel == 'Asterias_amurensis':
        farratio = 5.0938
        nearratio = 20.3752
    elif maxlabel == 'Asterina_pectinifera':
        farratio = 1.7
        nearratio = 6.8
    elif maxlabel == 'Conch':
        farratio = 0.3692
        nearratio = 1.4769
    elif maxlabel == 'Ecklonia_cava':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Heliocidaris_crassispina':
        farratio = 1.3 
        nearratio = 5.1
    elif maxlabel == 'Hemicentrotus':
        farratio = 0.6
        nearratio = 2.4
    elif maxlabel == 'Sargassum':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Sea_hare':
        farratio = 3.6
        nearratio = 14.6
    elif maxlabel == 'Turbo_cornutus':
        farratio = 1.5
        nearratio = 5.9
    if maxratio <= farratio:
        return 'Far'
    elif (maxratio <= nearratio) and (maxratio > farratio): 
        return 'Mid'
    elif maxratio > nearratio:
        return 'Near'

len_arr= 0
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        print(root, Json)
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
        if maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']:
            print(maxlabel)
        
        distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)       
        if (maxlabel == 'Heliocidaris_crassispina') and (distance_flag == 'Mid'):
            shutil.copy(root + '/' + Json, savepath +'/Mid' + Json)
            shutil.copy(root + '/' + Json[:-4] + 'jpg', savepath +'/Mid' + Json[:-4] + 'jpg')
        if (maxlabel == 'Heliocidaris_crassispina') and (distance_flag == 'Far'):
            shutil.copy(root + '/' + Json, savepath +'/Far' + Json)
            shutil.copy(root + '/' + Json[:-4] + 'jpg', savepath +'/Far' + Json[:-4] + 'jpg')
        if (maxlabel == 'Asterina_pectinifera') and (objects['Distance'] >= 1.0):
            shutil.copy(root + '/' + Json, savepath +'/Mid' + Json)
            shutil.copy(root + '/' + Json[:-4] + 'jpg', savepath +'/Mid' + Json[:-4] + 'jpg')
        if (maxlabel == 'Asterina_pectinifera') and (objects['Distance'] == 0.5):
            shutil.copy(root + '/' + Json, savepath +'/Near' + Json)
            shutil.copy(root + '/' + Json[:-4] + 'jpg', savepath +'/Near' + Json[:-4] + 'jpg')