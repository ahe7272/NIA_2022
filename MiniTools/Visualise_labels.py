import json
import os 
import cv2
import numpy as np

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects


for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/Sunken_Debris/5.Visualised'):
    for file in files:
        if file[-4:] == 'json':
            objects = getjson(path + '/' +file)
            img = cv2.imread(path + '/' + file[:-5] + '.jpg')
            for label in objects['shapes']:
                if label['shape_type'] == 'rectangle': 
                    start = (int(label['points'][0][0]), int(label['points'][0][1]))
                    end = (int(label['points'][1][0]), int(label['points'][1][1]))
                    Text_loc = (int(label['points'][0][0]), int(label['points'][0][1] + 50 ))
                    img = cv2.rectangle(img, start, end, (0, 0, 255), 13)
                    img = cv2.putText(img, label['label'] , Text_loc, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 8)
                
                else:
                    points = []
                    for each_xy in label['points']:
                        x = int(each_xy[0])
                        y = int(each_xy[1])
                        points += [[x, y]]
                    points = np.array(points, np.int32)
                    points = points.reshape((-1,1,2))
                    Text_loc = (points[0][0])
                    img = cv2.polylines(img, [points], True, (0, 0, 255), 5)
                    img = cv2.putText(img, label['label'] , Text_loc, cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 8)
                    # cv2.imshow('d', img)
                    # cv2.waitKey(0)
            cv2.imwrite(path + '/Visualised_' + file[:-5] + '.jpg', img)