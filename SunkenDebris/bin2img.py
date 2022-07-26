from PIL import Image
import io
import base64
import glob
import cv2
import numpy as np
import json

def b64_to_img(jsonlist):
    for jsonfile in glob.glob(jsonlist):
        with open(jsonfile) as Jsonfile:
            objects = json.load(Jsonfile)
            Databin = objects['Origin_img'].encode('utf-8')
            f = io.BytesIO()
            f.write(base64.b64decode(Databin))
            img = np.array(Image.open(f))
            # cv2.imwrite('test.jpg', reversed_img)
            cv2.imshow('d', img) 
            cv2.waitKey()
    
b64_to_img("C:/Users/Administrator/Desktop/20220712/20220712_1-3/*.json")

