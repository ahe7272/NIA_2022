from PIL import Image
import io
import base64
import glob
import cv2
import numpy as np

def b64_to_img(b64):
    f = io.BytesIO()
    f.write(base64.b64decode(b64))
    img = np.array(Image.open(f))
    return img

def img_to_b64(img):
    imgfile = glob.glob(img)[0]
    imgfile = Image.open(imgfile)
    f = io.BytesIO()
    imgfile.save(f, format='PNG')
    img_bin = f.getvalue()
    if hasattr(base64, 'encodebytes'):
        img_b64 = base64.encodebytes(img_bin)
    else:
        img_b64 = base64.encodestring(img_bin)
    return img_b64


bin = img_to_b64("C:/Users/Administrator/Desktop/good/rope_048_03227.jpg")
new = cv2.cvtColor(b64_to_img(bin), cv2.COLOR_BGR2RGB)
cv2.imshow('d', new)

cv2.waitKey()