import PySimpleGUI as sg
import os
from glob import glob
import openpyxl
import cv2
import json
import shutil
import datetime

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')

        layout = [
                  [sg.Text('데이터의 경로(폴더)',font =("Arial", 13, 'bold'), size=(40, 1))],
                  [sg.InputText('Data Folder', font =("Arial", 13), size = (30,1), key='DataPath'), sg.FolderBrowse('SELECT', font =("Arial", 13, 'bold'), size=(10, 1)), sg.Button('Run',font =("Arial", 13, 'bold'), size=(10,1), key='Run')],
                  [sg.ProgressBar(1, orientation='h', size=(40,20), key='progress')]
                 ]

        window = sg.Window('Clahe images', layout, element_justification='c', grab_anywhere = True).Finalize()
        return window

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

def preprocess_img(image, savepath):
    imagenamejpg = os.path.split(image)[-1]
    imagename = os.path.splitext(imagenamejpg)[0]
    image = cv2.imread(image)
    clahe_img = clahe_image(image)
    h, w, _ = image.shape
    # if (h == 3840) and  (w == 2160):
    #     clahe_img = cv2.rotate(clahe_img, cv2.ROTATE_90_CLOCKWISE)
    #     h = 2160
    #     w = 3840
    # elif (h not in [2160, 3840]) or (w not in [3840, 2160]):
    #     sg.Popup(imagename + '이미지 비율이 안 맞습니다.'+str(h) + ' ' + str(w), font =("Arial", 15), keep_on_top=True)
    #     return False
    cv2.imwrite(savepath + "/" + imagenamejpg, clahe_img)

m = MakeGUI()
window = m.makegui()

while True:    
    event, values = window.read()     
    progress_bar = window['progress']
    if event == 'Run':
        Datapath = values['DataPath']
        imagelist = glob(Datapath + "/*.jpg")
        datalength = len(imagelist)
        progress_bar.UpdateBar(0, datalength)
        cnt = 1
        savepath = os.path.split(Datapath)[0] + '/' + str(os.path.split(Datapath)[1]) + '_clahed'
        os.makedirs(savepath, exist_ok=True)
        for image in imagelist:
            progress_bar.UpdateBar(cnt, datalength)
            imagenamejpg = os.path.split(image)[-1]
            imagename = os.path.splitext(imagenamejpg)[0]
            preprocess_img(image, savepath)
            cnt += 1

        if cnt == datalength +1 :
            sg.Popup('정제 완료^^!', font =("Arial", 13), keep_on_top=True)
            break

    if event in (None, 'Exit'):
        break

