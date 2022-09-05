import json
import os
import numpy as np
from classes import debris_dict, sea_animal_dict
import pandas as pd
import copy
import cv2 

path = input("달성도 excel 파일 생성을 위한 주차 작업물 폴더 경로를 입력하세요.\n")


def resize_img(root, file):
    img = cv2.imread(root+'/'+file)
    img = cv2.resize(img, (3840, 2160))  
    cv2.imwrite(root + '/' +'resized_' + file, img)
    
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

filenames = []
dist = []
labels = []
ratios = []

len_arr= 0
for root, dirs, files in os.walk(path):
    for file in files:
        if file[-5:] == ".json":
            name = os.path.splitext(file)[0]
            jsonfile = os.path.join(root, name + '.json')
            objects = getjson(jsonfile)
            if len(objects['shapes']) == 0:
                print(file)
                continue   
            maxratio, label_with_ratio = ratio_of_objects(objects)
            dist += [root.split('\\')[-1]]
            for label, ratio in label_with_ratio:
                labels += [label]
                ratios += [ratio]
        elif (file[-4:].upper() == '.JPG') and file[:1] != 'r':
        #     resize_img(root, file)
            filenames += [file]


filenames = pd.Series(filenames)
labels = pd.Series(labels)
ratios = pd.Series(ratios)
dist = pd.Series(dist)

df = pd.concat([filenames, dist, labels, ratios], axis =1 )
# df_total = pd.DataFrame(list(dict_total.items()), columns=['classname', 'Total'])
df.to_excel('C:/Users/Administrator/Desktop/Distance_by_labels/Labelled_by_dist/Size_by_dist.xlsx')
print(df)