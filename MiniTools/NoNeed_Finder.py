import json
import os
import numpy as np
from classes import sea_animal_dict
import shutil

match_path = input('경로: ')
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
        farratio = 2.7
        nearratio = 10.9
    elif maxlabel == 'Turbo_cornutus':
        farratio = 2.2
        nearratio = 8.7
    if maxratio <= farratio:
        return 'Far'
    elif (maxratio <= nearratio) and (maxratio > farratio): 
        return 'Mid'
    elif maxratio > nearratio:
        return 'Near'
        
for path, dirs, files in os.walk(match_path):
    # if path == path + '_NoNeed':
    #     continue
    for item in files:
        print(path, item)
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
            if (maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']):
                print(item)
            
            distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
            # if (maxlabel == 'Asterias_amurensis'):
            #     shutil.move(path + '/' + item, path + '_NoNeed/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            # elif (maxlabel == 'Asterina_pectinifera' and (distance_flag in ['Near', 'Mid'])):
            #     shutil.move(path + '/' + item, path + '_NoNeed/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            # elif (maxlabel == 'Conch'):
            #     shutil.move(path + '/' + item, path + '_NoNeed/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            # elif (maxlabel == 'Heliocidaris_crassispina') and (distance_flag in ['Near', 'Mid']):
            #     shutil.move(path + '/' + item, path + '_NoNeed/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            # elif (maxlabel == 'Sea_hare') and (distance_flag in ['Mid', 'Far']):
            #     shutil.move(path + '/' + item, path + '_NoNeed/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_NoNeed/' + item[:-5] + '.jpg')
            # if (maxlabel == 'Sea_hare'):
            #     os.makedirs(path +'_SeaHare', exist_ok=True)

            #     shutil.move(path + '/' + item, path + '_SeaHare/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_SeaHare/' + item[:-5] + '.jpg')
            # if (maxlabel == 'Sea_hare') and (distance_flag in ['Far']):
            #     os.makedirs(path +'_SFAR', exist_ok=True)
            #     shutil.move(path + '/' + item, path + '_SFAR/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_SFAR/' + item[:-5] + '.jpg')
            # if (maxlabel == 'Asterina_pectinifera') and (distance_flag in ['Far']):
            #     os.makedirs(path +'_AFAR', exist_ok=True)
            #     shutil.move(path + '/' + item, path + '_AFAR/' + item)
            #     shutil.move(path + '/' + item[:-5] + '.jpg', path + '_AFAR/' + item[:-5] + '.jpg')
            if (maxlabel == 'Turbo_cornutus') and (distance_flag in ['Near']):
                os.makedirs(path +'_TNear', exist_ok=True)
                shutil.move(path + '/' + item, path + '_TNear/' + item)
                shutil.move(path + '/' + item[:-5] + '.jpg', path + '_TNear/' + item[:-5] + '.jpg')
            
                
