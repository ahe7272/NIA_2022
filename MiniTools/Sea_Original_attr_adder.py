import json
import datetime
import os 
from classes import sea_animal_dict
import numpy as np
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

def classify_distance_4_seaanimal(maxratio, maxlabel):
    if maxlabel == 'Asterias_amurensis':
        farratio = 0.9
        nearratio = 8.09
    elif maxlabel == 'Asterina_pectinifera':
        farratio = 0.38
        nearratio = 3.39
    elif maxlabel == 'Conch':
        farratio = 0.06
        nearratio = 0.5
    elif maxlabel == 'Ecklonia_cava':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Heliocidaris_crassispina':
        farratio = 0.2
        nearratio = 1.78
    elif maxlabel == 'Hemicentrotus':
        farratio = 0.6
        nearratio = 0.7
    elif maxlabel == 'Sargassum':
        farratio = 0
        nearratio = 0
    elif maxlabel == 'Sea_hare':
        farratio = 0.84
        nearratio = 7.53
    elif maxlabel == 'Turbo_cornutus':
        farratio = 0.27
        nearratio = 2.43
    if maxratio <= farratio:
        return 'Far'
    elif (maxratio <= nearratio) and (maxratio > farratio): 
        return 'Mid'
    elif maxratio > nearratio:
        return 'Near'
        
last_frame_no = 0
no_to_add = 18090-204
addfrom_path = 'D:/1st_Original/Video_Preprocessed'
addto_path = 'D:/1st_Original/Test/Polygon'
not_exist_path = 'D:/1st_Original/Test/not_exist'
Source_video_list = []
Video_time_list = []
Frame_no_list = []
Collection_method_list = []

for (addfrompath, dir, addfromfiles) in os.walk(addfrom_path): 
    for addfromitem in addfromfiles:
        # if int(addfromitem.split('_')[1].split('.')[0]) < last_frame_no:
        #     no_to_add += last_frame_no
        # print(no_to_add)
        filename = addto_path + '/' + str(no_to_add + int(addfromitem.split('_')[1].split('.')[0])).zfill(5) + '.json'
        if os.path.isfile(filename[:-5] + '.jpg') == False:
            shutil.move(addfrom_path +'/' + addfromitem, not_exist_path + '/' + addfromitem)  
            continue
        objects = getjson(filename)
        objects['Source_video'] = addfromitem.split('_')[0] + '.mp4'
        objects['Video_time'] = str(datetime.timedelta(seconds= ((int(addfromitem.split('_')[1].split('.')[0])*2)-2)))
        objects['Frame_no'] = (int(addfromitem.split('_')[1].split('.')[0])-1)*2*60
        if len(addfromitem.split('ROV')) > 1:
            objects['Collection_method'] = 'ROV'
        else:
            objects['Collection_method'] = 'Diver'
        maxratio, label_with_ratio = ratio_of_objects(objects)
        if len(label_with_ratio) > 1:
            for label, ratio in label_with_ratio:
                if maxratio == ratio:
                    maxlabel = label
        else:
            maxlabel = label_with_ratio[0][0]   
        if (maxlabel not in ['Asterias_amurensis', 'Asterina_pectinifera', 'Conch', 'Ecklonia_cava', 'Heliocidaris_crassispina', 'Hemicentrotus', 'Sargassum', 'Sea_hare', 'Turbo_cornutus']):
            print(addfromitem)
        distance_flag = classify_distance_4_seaanimal(maxratio, maxlabel)
        if maxlabel not in ['Ecklonia_cava', 'Sargassum']:
            if distance_flag == 'Near':
                objects['Distance'] = 0.5
            elif distance_flag == 'Mid':
                objects['Distance'] = 1.0
            elif distance_flag == 'Far':
                objects['Distance'] = 1.5
        objects['Latitude'] = round(float(objects['Latitude']),6)
        objects['Longitude'] = round(float(objects['Longitude']),6)
        with open(filename, 'w') as j:
            json.dump(objects, j, indent='\t')
            j.close()
        last_frame_no = int(addfromitem.split('_')[1].split('.')[0])
        old = addfrompath + '/' + addfromitem
        new = addfrompath + '/' + str(no_to_add + int(addfromitem.split('_')[1].split('.')[0])).zfill(5) + '_original.jpg'
        os.rename(old, new)

