# 에러출력되게 변경, error파일 생성-> 완료된 파일만 done파일에 들어가게 
import PySimpleGUI as sg
import base64
import pyperclip
from glob import glob
import os
from integrity_check import check
import subprocess
import numpy as np
import sys
import datetime
import json

class MakeGUI():
    def getimage(self, image):
        with open(image, 'rb') as img:
            base64_string = base64.b64encode(img.read())    
        return base64_string

    def makegui(self):
        sg.theme('DarkAmber')
        Step1 = [
                  [sg.Text('ANNOTATION', font =("Arial", 20))],
                  [sg.Text('Path', font =("Arial", 15)), sg.InputText(key='Path', font =("Arial", 15), size = (12,1)), sg.FolderBrowse('경로 선택',font =("Arial", 15) , size=(12, 1), key='Select_Folder')],
                  [sg.Text('  ID  ', font =("Arial", 15)), sg.InputText(key='ID', font =("Arial", 15), size = (12,1)), sg.Button('Labelme', font =("Arial", 15), size=(12, 1))],
                  [sg.Text('           Echinoid           ', font =("Arial", 15)), sg.Text('               Starfish               ', font =("Arial", 15)), sg.Text('           SeaHare           ',font =("Arial", 15))], 
                  [
                    sg.Button('', image_data=self.getimage('example_image/Echinoid.png'), key='Echinoid'),
                    sg.Button('', image_data=self.getimage('example_image/Starfish.png'), key='Starfish'),
                    sg.Button('', image_data=self.getimage('example_image/SeaHare.png'), key='SeaHare'),
                  ],
                  [sg.Text('               Snail              ', font =("Arial", 15)), sg.Text('          EckloniaCava        ', font =("Arial", 15)), sg.Text('          Sargassum          ', font =("Arial", 15))],
                  [
                    sg.Button('', image_data=self.getimage('example_image/Snail.png'), key='Snail'),
                    sg.Button('', image_data=self.getimage('example_image/EckloniaCava.png'), key='EckloniaCava'),
                    sg.Button('', image_data=self.getimage('example_image/Sargassum.png'), key='Sargassum')
                  ]
                ]
        Step2 = [
                  [sg.Text('FILL IN METADATA', font =("Arial", 20))],
                  [sg.Text('', font =("Arial", 10))],
                  [sg.Text('열린 사진의 개체에 대한 Metadata를 입력해 주세요.', font =("Arial", 15, 'bold'))],
                  [sg.Text(' - Size: 해당 개체의 크기', font =("Arial", 13))],
                  [sg.Text(' - Weight: 해당 개체의 무게', font =("Arial", 13))],
                  [sg.Text('', font =("Arial", 10))],
                  [sg.Text('  Size  ', font =("Arial", 15)), sg.InputText(key='Size', font =("Arial", 15), size = (12,1)), sg.Text('Weight', font =("Arial", 15)), sg.InputText(key='Weight', font =("Arial", 15), size = (12,1)), sg.Button('입력', font =("Arial", 15), size=(13, 1), key='Meta')]
                ] 
        Step3 = [
                  [sg.Text('INTEGRITY CHECK', font =("Arial", 20))],
                  [sg.Text('', font =("Arial", 10))],
                  [sg.Text('에러 메세지를 확인하여 해당 파일을 수정해 주세요.', font =("Arial", 15, 'bold'))],
                  [sg.Text(' - 라벨명 에러의 경우 Labelme를 실행해 해당 annotation의 이름을 수정해 주세요.', font =("Arial", 13))],
                  [sg.Text(' - 속성 개수 에러의 경우 ID 입력 후 Labelme를 실행해 주세요.', font =("Arial", 13))],
                  [sg.Button('무결성 검사', font=("Arial", 15, 'bold'), size=(35, 5), key='integrity')], 
                  [sg.Text('', font =("Arial", 10))],
                  [sg.Button('Exit', font=("Arial", 15, 'bold'),size=(53, 1))]
                ]
        tab_group = [
                     [sg.TabGroup(
                            [[
                            sg.Tab('STEP1', Step1),
                            sg.Tab('STEP2', Step2),
                            sg.Tab('STEP3', Step3)]], 
                            tab_location='centertop',
                            font = ("Arial", 20),
                            tab_border_width = 2,               
                            selected_background_color='White',
                            selected_title_color='Black',
                            border_width=10)]        
                    ]
        window = sg.Window('Processing Data', tab_group, resizable=True, grab_anywhere = True, element_justification='c') 
        return window
        
def runLabelme():
    subprocess.Popen(subprocess.getoutput('type labelme')[11:])

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

m = MakeGUI()
window = m.makegui()

object = ['Echinoid', 'Starfish', 'SeaHare', 'Snail', 'EckloniaCava', 'Sargassum']
minsize = 1024
now = datetime.datetime.now()
date = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)

try:
    while True:    
        event, values = window.read()    
        Path = values['Path']
        ID = values['ID']
        if event in object:
            pyperclip.copy(event)

        if event == 'Labelme':
            imagelist = glob(values['Path'] + '/*.jpg')
            for image in imagelist:
                jpgfile = os.path.split(image)[-1]
                imagename = os.path.splitext(jpgfile)[0]
                jsonfile = Path + '/' + imagename + '.json'
                imagefile = Path + '/' + imagename + '.jpg'
            runLabelme()

        # if event == 'Metadata':
        #     jsonlist = glob(values['Path'] + '/*.json')
        #     for json in jsonlist:
        #     with open(jsonfile) as Jsonfile:
        #         objects = json.load(Jsonfile)
        #         objects['ID'] = ID
        #         with open(jsonfile, 'w') as Jsonfile:
        #             json.dump(objects, Jsonfile, indent=4)

        if event == 'integrity':
            jsonlist = glob(values['Path'] + '/*.json')
            jsonerrors = ""
            for Json in jsonlist:
                jsonfile = os.path.split(Json)[-1]
                jsonerrors += check(jsonfile, minsize, Path)
            if len(jsonerrors) > 0:
                sg.Popup(jsonerrors, font =("Arial", 15), keep_on_top=True)
            else:
                sg.Popup("작업완료된 파일이 Done 폴더에 저장되었습니다. Exit을 누르고 NAS에 업로드를 시작해 주세요.", font =("Arial", 15), keep_on_top=True)

        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
   print(e)
window.close()


