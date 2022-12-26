import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import shutil


inputpath = input('경로: ')
def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

classes_dict= debris_dict()

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
        
for path, dirs, files in os.walk(inputpath):
    os.makedirs(path +'_NoNeed', exist_ok=True)
    if path == path + '_NoNeed':
        continue
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
            if (maxlabel not in ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Wood', 'Rope', 'Rubber_etc', 'Rubber_tire', 'Etc']):
                print(item)
            distance_flag = classify_distance_4_debris(maxratio)
            if (maxlabel == 'Fish_trap'):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Glass'):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Metal'):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Plastic') :
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Wood') and (distance_flag in ['Mid', 'Far']):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Rope') and (distance_flag in ['Near', 'Far']):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Rubber_etc') and (distance_flag in ['Mid', 'Far']):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            elif (maxlabel == 'Rubber_tire'):
                shutil.move(path + '/' + item, path + '_NoNeed/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            else:
                print(maxlabel, distance_flag)
