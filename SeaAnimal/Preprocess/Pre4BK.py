import PySimpleGUI as sg
import os
from glob import glob
import cv2
from jsonformat import getjsonform
import json
import shutil
import datetime
from PIL import Image
import io
import base64
import numpy as np
import datetime

class MakeGUI():
    def makegui(self):
        sg.theme('DarkAmber')

        layout = [
                  [sg.Text('데이터의 경로(폴더)',font =("Arial", 13, 'bold'), size=(40, 1))],
                  [sg.InputText('Data Folder', font =("Arial", 13), size = (30,1), key='DataPath'), sg.FolderBrowse('SELECT', font =("Arial", 13, 'bold'), size=(10, 1))],
                  [sg.Text('비디오 프레임 추출 간격(초).',font =("Arial", 13, 'bold'), size=(40, 1))],
                  [sg.InputText('Sampling Intervals', font =("Arial", 13),  size = (30,1), key='intervals'), sg.Button('Run',font =("Arial", 13, 'bold'), size=(10,1), key='Run')],
                  [sg.ProgressBar(1, orientation='h', size=(40,20), key='progress')]
                 ]

        window = sg.Window('Preprocessing data', layout, element_justification='c', grab_anywhere = True).Finalize()
        return window

def get_frame(start, end, fps):
    frame_array = [i for i in range(start, end, fps)]
    return frame_array

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

def preprocess_video(video, interval, savepath):
    cap = cv2.VideoCapture(video)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    startframe = int(0 * fps)
    endframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #끝나는시간 * fps
    frame_array = get_frame(startframe, endframe, fps * interval)
    videonamemp4 = os.path.split(video)[-1]
    videoname = os.path.splitext(videonamemp4)[0]
    cnt = 0

    for f in frame_array:
        cnt += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        success, image = cap.read()
        if success == False:
            print("프레임 추출 실패!")
        else:   
            clahe_img = clahe_image(image)
            h, w, _ = image.shape
            if (h == 3840) and  (w == 2160):
                clahe_img = cv2.rotate(clahe_img, cv2.ROTATE_90_CLOCKWISE)
                h = 2160
                w = 3840
            elif (h not in [2160, 3840]) or (w not in [3840, 2160]):
                sg.Popup(videoname + '비디오 비율이 안 맞습니다.'+str(h) + ' ' + str(w), font =("Arial", 15), keep_on_top=True)
                return False 
            video_time = str(datetime.timedelta(seconds= f/60))
            cv2.imwrite(savepath + "/" + videoname +'_' + str(cnt).zfill(3) + '.jpg', clahe_img)
                    
        if cv2.waitKey(10) == 27:
            break    

m = MakeGUI()
window = m.makegui()

while True:    
    event, values = window.read()     
    progress_bar = window['progress']
    if event == 'Run':
        Datapath = values['DataPath']
        video_list = []
        for (path, dir, files) in os.walk(Datapath): 
            for item in files:
                if item[-4:] == '.mp4':
                    video_list += [path + '/' + item]
        datalength = len(video_list) 
        progress_bar.UpdateBar(0, datalength)
        cnt = 0
        for (path, dir, files) in os.walk(Datapath):  
            print(path)     
            for item in files:
                if item[-4:] == '.mp4':
                    interval = int(values['intervals'])
                    
                    savepath = path + '_preprocessed'
                    os.makedirs(savepath, exist_ok=True)
                    print(path + item)
                    preprocess_video(path +'/' + item, interval, savepath)
                    cnt += 1
                    progress_bar.UpdateBar(cnt, datalength)

        if cnt == datalength:
            sg.Popup('정제 완료^^!', font =("Arial", 13), keep_on_top=True)
            break
        
    if event in (None, 'Exit'):
        break

