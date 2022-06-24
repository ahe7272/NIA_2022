import PySimpleGUI as sg
import base64
import pyperclip
from glob import glob
import os
from integrity_check import check
import subprocess
import sys
import json
import numpy as np

class MakeGUI():
    def getimage(self, image):
        with open(image, 'rb') as img:
            base64_string = base64.b64encode(img.read())    
        return base64_string

    def makegui(self):
        sg.theme('DarkAmber')
        Step1 = [
                  [sg.Text('ANNOTATION', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text(' PATH', font =("Arial", 15)), sg.InputText(key='Path', font =("Arial", 15), size = (22,1)), sg.FolderBrowse('SELECT',font =("Arial", 15, 'bold') , size=(12, 1), key='Select_Folder')],
                  [sg.Text('  ID  ', font =("Arial", 15)), sg.InputText(key='userID', font =("Arial", 15), size = (23,1)), sg.Button('Labelme', font =("Arial", 15, 'bold'), size=(12, 1))],
                  [sg.Text('      Fish_net      ', font =("Arial", 15, 'bold')), sg.Text('     Fish_trap      ', font =("Arial",  15, 'bold')), sg.Text('       Glass',font =("Arial",  15, 'bold'))], 
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Fish_net.png'), key='Fish_net'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Fish_trap.png'), key='Fish_trap'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Glass.png'), key='Glass')
                  ],
                  [sg.Text('        Metal        ', font =("Arial",  15, 'bold')), sg.Text('       Plastic     ', font =("Arial",  15, 'bold')), sg.Text('Processed_wood', font =("Arial",  15, 'bold'))],
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Metal.png'), key='Metal'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Plastic.png'), key='Plastic'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Processed_wood.png'), key='Processed_wood')
                  ],
                  [sg.Text('        Rope       ', font =("Arial",  15, 'bold')), sg.Text('     Rubber_etc     ', font =("Arial",  15, 'bold')), sg.Text('Rubber_tire', font =("Arial",  15, 'bold'))],
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Rope.png'), key='Rope'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Rubber_etc.png'), key='Rubber_etc'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/Rubber_tire.png'), key='Rubber_tire')
                  ]
                ]
        Step2 = [
                  [sg.Text('INTEGRITY CHECK', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text('에러 메세지를 확인하여 해당 파일을 수정해 주세요.', font =("Arial", 15, 'bold'))],
                  [sg.Text(' - Annotation 이름 에러: Labelme 재실행 및 annotation 이름 수정', font =("Arial", 13))],
                  [sg.Text(' - 속성 개수 에러: json 파일 확인 및 담당 PM과 소통', font =("Arial", 13))],
                  [sg.Text(' - ID 에러: STEP1에 ID 입력 후 다시 Metadata 입력', font =("Arial", 13))],
                  [sg.Button('무결성 검사', font=("Arial", 15, 'bold'), size=(39, 5), key='integrity')], 
                  [sg.Text('', font =("Arial", 10))],
                  [sg.Button('Exit', font=("Arial", 15, 'bold'),size=(39, 5))]
                ]
        tab_group = [
                     [sg.TabGroup(
                            [[
                            sg.Tab('STEP1', Step1),
                            sg.Tab('STEP2', Step2)
                            ]], 
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
    python_file = subprocess.getoutput('where pythonw.exe').split('\n')[0] 
    labelme_file =  python_file[:-11] + "/Lib/site-packages/labelme/__main__.py"
    if np.__version__[:4] == '1.22':
        
        subprocess.Popen(python_file + ' ' + labelme_file)
try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

m = MakeGUI()
window = m.makegui()

object = ['Fish_net', 'Fish_trap', 'Glass', 'Metal', 'Plastic', 'Processed_wood', 'Rope','Rubber_etc',  'Rubber_tire']
minsize = 1024

try:
    while True:    
        event, values = window.read()    
        Path = values['Path']
        userID = values['userID']
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

            jsonlist = glob(values['Path'] + '/*.json')
            for each_json in jsonlist:
                with open(each_json) as jsontosave:
                    objects = json.load(jsontosave)
                    objects['ID'] = userID
                with open(each_json, 'w') as jsontosave:
                    json.dump(objects, jsontosave, indent=4)

        if event == 'integrity':
            jsonlist = glob(values['Path'] + '/*.json')
            jsonerrors = ""
            if values['userID'] == "":
                jsonerrors += 'ID 에러!\nID를 정확하게 입력하고 Metadata 입력을 다시 진행해 주세요.\n'
            for Json in jsonlist:
                jsonfile = os.path.split(Json)[-1]
                jsonerrors += check(jsonfile, minsize, Path)
            if len(jsonerrors) > 0:
                sg.Popup(jsonerrors, font =("Arial", 15), keep_on_top=True)
            else:
                sg.Popup("작업완료된 파일이 Processed 폴더에 저장되었습니다. \n 작업 폴더에 남은 파일이 없는지 확인해주세요.", font =("Arial", 15), keep_on_top=True)
                sg.Popup("모두 Processed 폴더로 옮겨졌다면 Exit을 누르시고 NAS에 업로드를 시작해주세요.\n 담당 PM님과 소통하시기 바라며 오늘도 수고하셨습니다.", font =("Arial", 15), keep_on_top=True)
        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
   print(e)
window.close()


