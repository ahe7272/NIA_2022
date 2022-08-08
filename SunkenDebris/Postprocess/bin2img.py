from PIL import Image, ImageFilter
import io
import base64
import cv2
import numpy as np
import json
import os
import shutil

for (path, dir, files) in os.walk('C:/Users/Administrator/Desktop/NEW_7.3_sunken/BoundingBox/Attr_errors/CW306'):
    for file in files:
        if file[-4:] == 'json':
            with open(path + '/' + file) as Jsonfile:
                objects = json.load(Jsonfile)
                Jsonfile.close()
                try:
                    Databin = objects['Origin_img'].encode('utf-8')
                    f = io.BytesIO()
                    f.write(base64.b64decode(Databin))
                    img = np.array(Image.open(f))
                    objects.pop('Origin_img')
                    cv2.imwrite(path + '/Original_'+ file[:-5] + '.jpg', img)
                    with open(path + '/' + file, 'w') as Jsonfile:
                        json.dump(objects, Jsonfile, indent='\t')
                        Jsonfile.close()
                except:
                    try:
                        if os.path.isfile(path + '/Original_' + file[:-5] + '.jpg'):
                            continue
                        else:
                            src = cv2.imread(path + '/' + file[:-5] + '.jpg' , cv2.IMREAD_COLOR)
                            alpha1 = -0.5 
                            alpha2 = -0.3

                            b, g, r = cv2.split(src)

                            bdst = np.clip((1 + alpha1) * b - 128 * alpha1, 0, 255).astype(np.uint8)
                            gdst = np.clip((1 + alpha1) * g - 128 * alpha1, 0, 255).astype(np.uint8)
                            rdst = np.clip((1 + alpha1) * r - 128 * alpha2, 0, 255).astype(np.uint8)
                            
                            img = cv2.merge((rdst, gdst, bdst))
                            img = Image.fromarray(img)

                            blured = img.filter(ImageFilter.BoxBlur(3))  

                            name = '/Original_' + file[:-5] + '.jpg'
                            blured.save(path + name)
                    except:
                        pass