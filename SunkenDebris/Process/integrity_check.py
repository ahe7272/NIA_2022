import os
import json
import numpy as np
import shutil
import openpyxl

def classname_check(objects):
    classname_error = ""
    total_obj = len(objects['shapes'])
    classnameflag = True
    for t in range(total_obj):
        if objects['shapes'][t]['label'] not in classname:
            classname_error += objects['shapes'][t]['label'] + '가 잘못되었습니다.' + '\n'
            classnameflag = False
    return classnameflag, classname_error

def attribute_value(objects):
    attr_error = ""
    if len(objects) == 12:
        return True, attr_error
    else:
        attr_error += '속성 개수 : ' + str(len(objects)) + ' 개로 속성값에 이상이 있습니다.' + '\n'
        return False, attr_error

def size(objects, minsize):
    total_obj = len(objects['shapes'])
    for t in range(total_obj - 1, -1, -1):
        points = objects['shapes'][t]['points'] 
        points = np.array(points, np.int32)

        # boundingbox
        if objects['shapes'][t]['shape_type'] == 'rectangle':
            lefttopx, lefttopy = points[0]
            rightdownx, rightdowny = points[1]

        #polygon
        else:
            x = points[:, 0]
            y = points[:, 1]
            lefttopx = min(x)
            rightdownx = max(x)
            lefttopy = min(y)
            rightdowny = max(y)
        w = max(lefttopx, rightdownx) - min(lefttopx, rightdownx)
        h = max(lefttopy, rightdowny) - min(lefttopy, rightdowny)
        area = w * h 
        if area <= minsize:
            del(objects['shapes'][t])   
    return objects
    
def savejson(objects, jsonfile):
    with open(jsonfile, 'w') as Jsonfile:
        json.dump(objects, Jsonfile, indent=4)

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

classname =['etc', 'fishtrap', 'glass', 'metal', 'plastic','rope','rubber',  'tire', 'wood']

def check(jsonfile, minsize, path):
    errorlist = ""
    jsonpath = path + '/' + jsonfile
    imagefile = os.path.splitext(jsonfile)[0] + '.jpg'
    imagepath = path + '/' + imagefile
    donepath = os.path.split(path)[0] + '/Done/'
    os.makedirs(donepath, exist_ok=True)

    objects = getjson(jsonpath)
    objects = size(objects, minsize)
    
    savejson(objects, jsonpath)
    classnameflag, classname_error = classname_check(objects)
    if classnameflag:
        classes = True
    else:
        classes = False
        errorlist += str(imagefile) +' 파일 오류: ' + classname_error + '\n'

    attributeflag, attribute_error = attribute_value(objects)
    if attributeflag:
        attribute = True
    else:
        attribute = False
        errorlist += str(imagefile) + ' 파일 오류: ' + attribute_error + '\n'
        
    if classes and attribute:
        shutil.move(jsonpath, donepath + jsonfile)
        shutil.move(imagepath, donepath + imagefile)
    return errorlist 
    


