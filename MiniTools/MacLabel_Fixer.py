import json
import datetime
import os 
import cv2
import numpy as np 

path_input = input('경로: ')
def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
        Jsonfile.close()
    return objects

for (path, dir, files) in os.walk(path_input): 
    for item in files:
        if item[-5:] == '.json':
            objects = getjson(path + '/' + item)
            for label in objects['shapes']:
                label['points'] = np.ndarray.tolist(np.array(label['points'])/100)
                
            with open(path + '/' + item, 'w') as j:
                json.dump(objects, j, indent='\t')
                j.close()