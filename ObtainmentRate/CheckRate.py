import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import copy

path = input("달성도 excel 파일 생성을 위한 주차 작업물 폴더 경로를 입력하세요.\n")
D_or_S = input("침적 데이터면 D, 조식동물이면 S를 입력해주세요. ")
if D_or_S == 'D':
    savepath = 'C:/Users/Administrator/Documents/Github/NIA_2022/ObtainmentRate/Rate_excels/SunkenDebris'
    classes_dict= debris_dict()
elif D_or_S == 'S':
    savepath = 'C:/Users/Administrator/Documents/Github/NIA_2022/ObtainmentRate/Rate_excels/SeaAnimals'
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
        farratio = 10
        nearratio = 28
    elif maxlabel == 'Asterina_pectinifera':
        farratio = 12
        nearratio = 32
    elif maxlabel == 'Conch':
        farratio = 3
        nearratio = 10
    elif maxlabel == 'Ecklonia_cava':
        farratio = 17
        nearratio = 43
    elif maxlabel == 'Heliocidaris_crassispina':
        farratio = 7
        nearratio = 20
    elif maxlabel == 'Hemicentrotus':
        farratio = 7
        nearratio = 20
    elif maxlabel == 'Sargassum':
        farratio = 28
        nearratio = 57
    elif maxlabel == 'Sea_hare':
        farratio = 13
        nearratio = 30
    elif maxlabel == 'Turbo_cornutus':
        farratio = 9
        nearratio = 23
    if maxratio <= farratio:
        return 'Far'
    elif (maxratio <= nearratio) and (maxratio > farratio): 
        return 'Mid'
    elif maxratio > nearratio:
        return 'Near'

dict_near = copy.deepcopy(classes_dict)
dict_mid = copy.deepcopy(classes_dict)
dict_far = copy.deepcopy(classes_dict)
dict_total = copy.deepcopy(classes_dict)
len_arr= 0
for root, dirs, files in os.walk(path):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
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
        if (D_or_S == 'S') and (maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']):
            print(Json)
        elif (D_or_S == 'D') and (maxlabel not in ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope', 'Rubber_etc', 'Rubber_tire', 'Etc']):
            print(Json)
        if (D_or_S == 'S'):
            distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
        else:
            distance_flag = classify_distance_4_debris(maxratio)
        if distance_flag == 'Near':
            dict_near[maxlabel] += 1
        elif distance_flag == 'Mid':
            dict_mid[maxlabel] += 1
        elif distance_flag == 'Far':
            dict_far[maxlabel] += 1
        dict_total[maxlabel] += 1

df_near = pd.DataFrame(list(dict_near.items()), columns=['classname', 'Near'])
df_mid = pd.DataFrame(list(dict_mid.items()), columns=['classname', 'Mid'])
df_far = pd.DataFrame(list(dict_far.items()), columns=['classname', 'Far'])
df_total = pd.DataFrame(list(dict_total.items()), columns=['classname', 'Total'])
df = pd.concat([df_near, df_mid.iloc[:, [1]], df_far.iloc[:, [1]], df_total.iloc[:, [1]]], axis=1)
df.to_excel(savepath + '/ObtainmentRate.xlsx')