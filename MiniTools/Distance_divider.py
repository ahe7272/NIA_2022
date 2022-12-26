import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import shutil 

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

classes_dict= sea_animal_dict()

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

running_path = input('경로: ')
        
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

            if (maxlabel == 'Sargassum') and (objects['Distance'] == 0.5):
                os.makedirs(path + '/Sargassum_Near', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Sargassum_Near/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Sargassum_Near/' + item[:-4] + 'jpg') 
            elif (maxlabel == 'Sargassum') and (objects['Distance'] == 1.0):
                os.makedirs(path + '/Sargassum_Mid', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Sargassum_Mid/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Sargassum_Mid/' + item[:-4] + 'jpg') 
            elif (maxlabel == 'Sargassum') and (objects['Distance'] == 1.5):
                os.makedirs(path + '/Sargassum_Far', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Sargassum_Far/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Sargassum_Far/' + item[:-4] + 'jpg') 
            if (maxlabel == 'Ecklonia_cava') and (objects['Distance'] == 0.5):
                os.makedirs(path + '/Ecklonia_cava_Near', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Ecklonia_cava_Near/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Ecklonia_cava_Near/' + item[:-4] + 'jpg') 
            elif (maxlabel == 'Ecklonia_cava') and (objects['Distance'] == 1.0):
                os.makedirs(path + '/Ecklonia_cava_Mid', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Ecklonia_cava_Mid/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Ecklonia_cava_Mid/' + item[:-4] + 'jpg') 
            elif (maxlabel == 'Ecklonia_cava') and (objects['Distance'] == 1.5):
                os.makedirs(path + '/Ecklonia_cava_Far', exist_ok=True)
                shutil.move(path + '/' + item, path + '/Ecklonia_cava_Far/' + item)  
                shutil.move(path + '/' + item[:-4] + 'jpg', path + '/Ecklonia_cava_Far/' + item[:-4] + 'jpg') 