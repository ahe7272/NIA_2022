import os
import cv2
import numpy as np
from PIL import Image, ImageFilter

running_path = input('필터 입힐 파일 경로: ')
save_path = input('필터 입힌 후 저장할 경로: ')
for (path, dir, files) in os.walk(running_path):
    if path == save_path:
        continue            
    for file in files:
        if file[-4:] == '.jpg':
            src = cv2.imread(path + '/' + file, cv2.IMREAD_COLOR)
            alpha1 = -0.5 
            alpha2 = -0.3
            b, g, r = cv2.split(src)

            bdst = np.clip((1 + alpha1) * b - 128 * alpha1, 0, 255).astype(np.uint8)
            gdst = np.clip((1 + alpha1) * g - 128 * alpha1, 0, 255).astype(np.uint8)
            rdst = np.clip((1 + alpha1) * r - 128 * alpha2, 0, 255).astype(np.uint8)
            
            img = cv2.merge((rdst, gdst, bdst))
            img = Image.fromarray(img)

            blured = img.filter(ImageFilter.BoxBlur(3))  
            blured.save(save_path + '/' + file)