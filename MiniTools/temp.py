import cv2
import os


def clahe_image(img):
    b, g, r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_b = clahe.apply(b)
    clahe_b = cv2.normalize(clahe_b, None, 0, 255, cv2.NORM_MINMAX)
    clahe_g = clahe.apply(g)
    clahe_g = cv2.normalize(clahe_g, None, 0, 255, cv2.NORM_MINMAX)
    clahe_r = clahe.apply(r)
    clahe_r = cv2.normalize(clahe_r, None, 0, 255, cv2.NORM_MINMAX)
    clahed = cv2.merge((clahe_b, clahe_g, clahe_r))
    return clahed


for root, dirs, files in os.walk('C:/Dataset/ori/oldBbox'):
    for file in files:
        if file[-4:] == ".jpg":
            img = cv2.imread(root + '/' + file)
            cv2.imwrite('C:/Dataset/ori/oldBbox Originals/' + '_'.join(file.split('_')[2:]), clahe_image(img))
