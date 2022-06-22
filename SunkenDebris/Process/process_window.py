# 에러출력되게 변경, error파일 생성-> 완료된 파일만 done파일에 들어가게 
import PySimpleGUI as sg
import base64
import pyperclip
from glob import glob
import os
from integrity_check import check
import subprocess
import sys
import json

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
                  [sg.Text('          etc          ', font =("Arial", 15, 'bold')), sg.Text('      fishtrap      ', font =("Arial",  15, 'bold')), sg.Text('        glass',font =("Arial",  15, 'bold'))], 
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/etc.png'), key='etc'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/fishtrap.png'), key='fishtrap'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/glass.png'), key='glass')
                  ],
                  [sg.Text('        metal        ', font =("Arial",  15, 'bold')), sg.Text('       plastic       ', font =("Arial",  15, 'bold')), sg.Text('         rope', font =("Arial",  15, 'bold'))],
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/metal.png'), key='metal'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/plastic.png'), key='plastic'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/rope.png'), key='rope')
                  ],
                  [sg.Text('       rubber       ', font =("Arial",  15, 'bold')), sg.Text('          tire          ', font =("Arial",  15, 'bold')), sg.Text('        wood', font =("Arial",  15, 'bold'))],
                  [
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/rubber.png'), key='rubber'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/tire.png'), key='tire'),
                    sg.Button('', image_data=self.getimage('C:/Users/Administrator/Documents/Github/NIA_2022/SunkenDebris/Process/example_image/wood.png'), key='wood')
                  ]
                ]
        Step2 = [
                  [sg.Text('INTEGRITY CHECK', font =("Arial", 30, 'bold'), text_color = 'Skyblue')],
                  [sg.Text('에러 메세지를 확인하여 해당 파일을 수정해 주세요.', font =("Arial", 15, 'bold'))],
                  [sg.Text(' - 라벨명 에러: Labelme 재실행 및 annotation 이름 수정', font =("Arial", 13))],
                  [sg.Text(' - 속성 개수 에러: ID 입력 후 Labelme 재실행', font =("Arial", 13))],
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
    subprocess.Popen(subprocess.getoutput('where labelme'))

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

m = MakeGUI()
window = m.makegui()

object = ['etc', 'fishtrap', 'glass', 'metal', 'plastic','rope','rubber',  'tire', 'wood']
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
            for Json in jsonlist:
                jsonfile = os.path.split(Json)[-1]
                jsonerrors += check(jsonfile, minsize, Path)
            if len(jsonerrors) > 0:
                sg.Popup(jsonerrors, font =("Arial", 15), keep_on_top=True)
            else:
                sg.Popup("작업완료된 파일이 Done 폴더에 저장되었습니다. \nExit을 누르고 NAS에 업로드를 시작해 주세요.", font =("Arial", 15), keep_on_top=True)

        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
   print(e)
window.close()


