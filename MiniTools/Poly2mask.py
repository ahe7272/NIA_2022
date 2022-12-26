import numpy as np
import os
import cv2
import json

running_path = input('경로 : ')
def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

def getMask(objects):
    imgH = objects['imageHeight']
    imgW = objects['imageWidth']
    mask = []
    if len(objects['shapes']) == 1:
        mask = np.zeros((imgH, imgW, 1))
        point = objects['shapes'][0]['points']
        point = np.array(point, np.int32)
        mask = cv2.fillPoly(mask,  np.array([point], dtype=np.int32), (255, 255, 0))

    elif len(objects['shapes']) > 1:
        mask = np.zeros((imgH, imgW, 1))
        for idx in range(len(objects['shapes'])):
            point = objects['shapes'][idx]['points']
            point = np.array(point, np.int32)
            mask = cv2.fillPoly(mask,  np.array([point], dtype=np.int32), (255, 255, 0))
    return mask

# for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/label'): 
#     for item in files:
#         if item[-5:] == '.json':
#             objects = getjson(path + '/' + item)
#             cv2.imwrite(path + '/' + item[:-5]+ '.jpg', getMask(objects))

for (path, dir, files) in os.walk(running_path): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            fish_net_objects = getjson(path + '/' + item)
            rope_obejcts = getjson(path + '/' + item)
            fish_net_shapes = []
            rope_shapes = []
            for label in objects['shapes']:
                if label['label'] == 'Fish_net':
                    fish_net_shapes += [label]
                elif label['label'] == 'Rope':
                    rope_shapes += [label]

            if len(fish_net_shapes) > 0:
                fish_net_objects['shapes'] = fish_net_shapes
                fish_net_mask = getMask(fish_net_objects)
                cv2.imwrite(path + '/' + item[:-5]+ '.jpg', fish_net_mask)
                img = cv2.imread(path + '/' + item[:-5]+ '.jpg', cv2.IMREAD_GRAYSCALE)    
                k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                closing = cv2.morphologyEx(fish_net_mask, cv2.MORPH_CLOSE, k, iterations=3)
                cv2.imwrite(path + '/' + item[:-5]+ '.jpg', closing) 
                src = cv2.imread(path + '/' + item[:-5]+ '.jpg', cv2.IMREAD_GRAYSCALE)
                ret, binary = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                fish_net_objects['shapes'] = []
                for i in range(len(contours)):
                    xy_points = []
                    cnt = 1
                    for xy in contours[i]:
                        cnt += 1
                        if cnt%5 == 0:
                            xy_points.append(xy.flatten().tolist())
                        # if cnt == len(contours[i]):
                        #     xy_points.append(xy.flatten().tolist())
                    fish_net_objects['shapes'] += [{
                            "label": "Fish_net",
                            "group_id": None,
                            "flags": {},
                            "shape_type": "polygon",
                            "points": xy_points
                                        }]
                objects['shapes'] = fish_net_objects['shapes']

            if len(rope_shapes) > 0:    
                rope_obejcts['shapes'] = rope_shapes
                rope_mask = getMask(rope_obejcts)
                cv2.imwrite(path + '/' + item[:-5]+ '.jpg', rope_mask)
                img = cv2.imread(path + '/' + item[:-5]+ '.jpg', cv2.IMREAD_GRAYSCALE)    
                k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
                closing = cv2.morphologyEx(rope_mask, cv2.MORPH_CLOSE, k, iterations=3)
                cv2.imwrite(path + '/' + item[:-5]+ '.jpg', closing) 
                src = cv2.imread(path + '/' + item[:-5]+ '.jpg', cv2.IMREAD_GRAYSCALE)
                ret, binary = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                rope_obejcts['shapes'] = []

                for i in range(len(contours)):
                    xy_points = []
                    cnt = 1
                    for xy in contours[i]:
                        cnt += 1
                        if cnt%5 == 0:
                            xy_points.append(xy.flatten().tolist())
                        # if cnt == len(contours[i]):
                        #     xy_points.append(xy.flatten().tolist())
                    rope_obejcts['shapes'] += [{
                            "label": "Rope",
                            "group_id": None,
                            "flags": {},
                            "shape_type": "polygon",
                            "points": xy_points
                                        }]
                objects['shapes'] = rope_obejcts['shapes'] 
            if (len(fish_net_shapes) > 0) and (len(rope_shapes) > 0): 
                objects['shapes'] = rope_obejcts['shapes'] + fish_net_objects['shapes']
            with open(path + '/' + item[:-5] + '.json', 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()
