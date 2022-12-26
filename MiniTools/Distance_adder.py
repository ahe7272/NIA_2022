import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

running_path = input('경로: ')
D_or_S = input("침적 데이터면 D, 조식동물이면 S를 입력해주세요. ")
if D_or_S == 'D':
    classes_dict= debris_dict()
elif D_or_S == 'S':
    classes_dict= sea_animal_dict()
else:
    exit()

# 이미지내 객체 비율
def ratio_of_objects(objects):
    height = objects['imageHeight']
    width = objects['imageWidth']
    imagesize = height * width 
    label_with_ratio = [] 
    maxratio = 0
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        objects['shapes'][o]['Size'] = 0
        objects['shapes'][o]['Weight'] = 0
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
        farratio = 5.7
        nearratio = 22.8
    elif maxlabel == 'Asterina_pectinifera':
        farratio = 2.4
        nearratio = 9.5
    elif maxlabel == 'Conch':
        farratio = 0.7
        nearratio = 2.9
    elif maxlabel == 'Ecklonia_cava':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Heliocidaris_crassispina':
        farratio = 1.6
        nearratio = 6.3
    elif maxlabel == 'Hemicentrotus':
        farratio = 0.7
        nearratio = 2.9
    elif maxlabel == 'Sargassum':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Sea_hare':
        farratio = 2.7
        nearratio = 10.8
    elif maxlabel == 'Turbo_cornutus':
        farratio = 2.2
        nearratio = 8.6
    if maxratio <= farratio:
        return 'Far'
    elif (maxratio <= nearratio) and (maxratio > farratio): 
        return 'Mid'
    elif maxratio > nearratio:
        return 'Near'
        
for path, dirs, files in os.walk(running_path):
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            if len(objects['shapes']) == 0:
                print(item)
                continue   
            maxratio, label_with_ratio = ratio_of_objects(objects)
            if len(label_with_ratio) > 1:
                for label, ratio in label_with_ratio:
                    if maxratio == ratio:
                        maxlabel = label
            else:
                maxlabel = label_with_ratio[0][0]   
            if (D_or_S == 'S') and (maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']):
                print(item)
            elif (D_or_S == 'D') and (maxlabel not in ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope', 'Rubber_etc', 'Rubber_tire', 'Etc']):
                print(item)
            if (D_or_S == 'S'):
                distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
                if maxlabel not in ['Ecklonia_cava', 'Sargassum']:
                    if distance_flag == 'Near':
                        objects['Distance'] = 0.5
                    elif distance_flag == 'Mid':
                        objects['Distance'] = 1.0
                    elif distance_flag == 'Far':
                        objects['Distance'] = 1.5
            elif (D_or_S == 'D'):
                distance_flag = classify_distance_4_debris(maxratio)
                if distance_flag == 'Near':
                    objects['Distance'] = 0.5
                elif distance_flag == 'Mid':
                    objects['Distance'] = 1.0
                elif distance_flag == 'Far':
                    objects['Distance'] = 1.5
            with open(path + '/' + item, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()
                